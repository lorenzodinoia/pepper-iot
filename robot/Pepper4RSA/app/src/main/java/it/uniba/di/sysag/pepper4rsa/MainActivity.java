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
import com.google.android.material.button.MaterialButton;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Map;
import java.util.TreeMap;

import it.uniba.di.sysag.pepper4rsa.utils.map.RobotHelper;
import it.uniba.di.sysag.pepper4rsa.utils.map.SaveFileHelper;
import it.uniba.di.sysag.pepper4rsa.utils.map.Vector2theta;
import it.uniba.di.sysag.pepper4rsa.utils.provider.Providers;

public class MainActivity extends RobotActivity implements RobotLifecycleCallbacks {
    private static final String CONSOLE_TAG = "Pepper4RSA";
    private static final int PERMISSION_STORAGE = 1;

    private QiContext qiContext;
    private SaveFileHelper saveFileHelper;
    private RobotHelper robotHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Providers.init(getApplicationContext());
        setContentView(R.layout.activity_main);

        if (this.checkSelfPermission(android.Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
            this.init();
        }
        else {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, PERMISSION_STORAGE);
        }

        MaterialButton buttonTest = findViewById(R.id.buttonTest);
        buttonTest.setOnClickListener(v -> {
            Runnable loadLocationsRunnable = () -> {
                try {
                    loadLocations();
                }
                catch (FileNotFoundException e) {
                    e.printStackTrace();
                }
            };
            Thread loadLocationsThread = new Thread(loadLocationsRunnable);
            loadLocationsThread.start();
        });
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
            TreeMap<String, AttachedFrame> savedLocations = new TreeMap<>();
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
}