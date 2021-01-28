package it.uniba.di.sysag.pepper4rsa;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.util.Log;

import androidx.annotation.NonNull;
import androidx.core.app.ActivityCompat;

import com.aldebaran.qi.sdk.QiContext;
import com.aldebaran.qi.sdk.QiSDK;
import com.aldebaran.qi.sdk.RobotLifecycleCallbacks;
import com.aldebaran.qi.sdk.design.activity.RobotActivity;
import com.aldebaran.qi.sdk.object.actuation.AttachedFrame;
import com.aldebaran.qi.sdk.object.actuation.Frame;
import com.aldebaran.qi.sdk.object.geometry.Transform;
import com.aldebaran.qi.sdk.object.streamablebuffer.StreamableBuffer;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Collection;
import java.util.Map;
import java.util.TreeMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import it.uniba.di.sysag.pepper4rsa.utils.map.LocalizeAndMapHelper;
import it.uniba.di.sysag.pepper4rsa.utils.map.RobotHelper;
import it.uniba.di.sysag.pepper4rsa.utils.map.SaveFileHelper;
import it.uniba.di.sysag.pepper4rsa.utils.map.Vector2theta;
import it.uniba.di.sysag.pepper4rsa.utils.models.Emergency;
import it.uniba.di.sysag.pepper4rsa.utils.models.Room;
import it.uniba.di.sysag.pepper4rsa.utils.models.VitalData;
import it.uniba.di.sysag.pepper4rsa.utils.provider.Providers;
import it.uniba.di.sysag.pepper4rsa.utils.request.EmergencyRequest;
import it.uniba.di.sysag.pepper4rsa.utils.request.RoomRequest;
import it.uniba.di.sysag.pepper4rsa.utils.request.core.RequestException;
import it.uniba.di.sysag.pepper4rsa.utils.request.core.RequestListener;

public class MainActivity extends RobotActivity implements RobotLifecycleCallbacks {
    public static final String CONSOLE_TAG = "Pepper4RSA";
    private static final int PERMISSION_STORAGE = 1;

    private QiContext qiContext;
    private SaveFileHelper saveFileHelper;
    private RobotHelper robotHelper;

    private TreeMap<String, AttachedFrame> savedLocations;

    private NavigationFragment navigationFragment;

    private boolean localized;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Providers.init(getApplicationContext());
        setContentView(R.layout.activity_main);

        //Check android permission
        if (this.checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
            this.init();
        } else {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, PERMISSION_STORAGE);
        }

    }

    @Override
    protected void onDestroy() {
        QiSDK.unregister(this, this);
        super.onDestroy();
    }

    @Override
    public void onRobotFocusGained(QiContext qiContext) {
        this.qiContext = qiContext;
        this.robotHelper.onRobotFocusGained(qiContext);

        try {
            loadLocations();

            //TODO aggiungere logica di get delle emergenze
            /*Bundle bundle = new Bundle();
            bundle.putString(NavigationFragment.ARG_LABEL_FRAME, "Gioconda");
            navigationFragment = new NavigationFragment();
            navigationFragment.setArguments(bundle);
            this.getSupportFragmentManager().beginTransaction().add(R.id.frame_fragment, navigationFragment).addToBackStack(null).commit();*/
            MainFragment mainFragment = new MainFragment();
            this.getSupportFragmentManager().beginTransaction().add(R.id.frame_fragment, mainFragment).addToBackStack(null).commit();
        }
        catch (FileNotFoundException e) {
            e.printStackTrace();
        }

    }

    @Override
    public void onRobotFocusLost() {

    }

    @Override
    public void onRobotFocusRefused(String reason) {

    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        if (requestCode == PERMISSION_STORAGE) {
            this.init();
        }
        else {
            finish();
        }
    }

    private void init() {
        QiSDK.register(this, this);
        this.saveFileHelper = new SaveFileHelper();
        this.robotHelper = new RobotHelper();
    }

    private void loadLocations() throws FileNotFoundException {
        // Read file into a temporary hashmap.
        File file = new File("/sdcard/Maps", "points.json");
        if (file.exists()) {
            Map<String, Vector2theta> vectors = saveFileHelper.getLocationsFromFile("/sdcard/Maps", "points.json");

            // Clear current savedLocations.
            savedLocations = new TreeMap<>();
            Frame mapFrame = robotHelper.getMapFrame();

            // Build frames from the vectors.
            for (Map.Entry<String, Vector2theta> entry : vectors.entrySet()) {
                // Create a transform from the vector2theta.
                Transform t = entry.getValue().createTransform();
                Log.d(CONSOLE_TAG, "loadLocations: " + entry.getKey());

                // Create an AttachedFrame representing the current robot frame relatively to the MapFrame.
                AttachedFrame attachedFrame = mapFrame.async().makeAttachedFrame(t).getValue();

                // Store the FreeFrame.
                savedLocations.put(entry.getKey(), attachedFrame);
            }
            Log.d(CONSOLE_TAG, "loadLocations: Done");
        }
        else {
            throw new FileNotFoundException();
        }
    }

    public QiContext getQiContext() {
        return qiContext;
    }

    public RobotHelper getRobotHelper() {
        return robotHelper;
    }

    public TreeMap<String, AttachedFrame> getSavedLocations() {
        return savedLocations;
    }

    public SaveFileHelper getSaveFileHelper() {
        return saveFileHelper;
    }

    public void startLocalizing() {
        robotHelper.say("Start localizing");
        if (robotHelper.localizeAndMapHelper.getStreamableMap() == null) {
            StreamableBuffer mapData = getSaveFileHelper().readStreamableBufferFromFile("/sdcard/Maps", "mapData.txt");;
            if (mapData == null) {
                Log.d(CONSOLE_TAG, "startLocalizing: No Map Available");
                robotHelper.localizeAndMapHelper.raiseFinishedLocalizing(LocalizeAndMapHelper.LocalizationStatus.MAP_MISSING);
            } else {
                Log.d(CONSOLE_TAG, "startLocalizing: get and set map");

                robotHelper.localizeAndMapHelper.setStreamableMap(mapData);

                robotHelper.holdAbilities(true).andThenConsume((useless) ->
                        robotHelper.localizeAndMapHelper.animationToLookInFront().andThenConsume(aVoid ->
                                robotHelper.localizeAndMapHelper.localize()));
            }
        } else {
            robotHelper.holdAbilities(true).andThenConsume((useless) ->
                    robotHelper.localizeAndMapHelper.animationToLookInFront().andThenConsume(aVoid ->
                            robotHelper.localizeAndMapHelper.localize()));
        }
    }

    public boolean isLocalized(){
        return localized;
    }

    public void setLocalized(boolean localized) { this.localized = localized;}
}