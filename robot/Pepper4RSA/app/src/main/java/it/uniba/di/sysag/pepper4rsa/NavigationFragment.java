package it.uniba.di.sysag.pepper4rsa;

import android.content.Context;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import com.aldebaran.qi.sdk.QiContext;
import com.aldebaran.qi.sdk.object.actuation.AttachedFrame;
import com.aldebaran.qi.sdk.object.actuation.OrientationPolicy;
import com.aldebaran.qi.sdk.object.streamablebuffer.StreamableBuffer;
import com.aldebaran.qi.sdk.util.FutureUtils;

import java.util.concurrent.TimeUnit;

import it.uniba.di.sysag.pepper4rsa.utils.map.GoToHelper;
import it.uniba.di.sysag.pepper4rsa.utils.map.LocalizeAndMapHelper;
import it.uniba.di.sysag.pepper4rsa.utils.map.RobotHelper;

public class NavigationFragment extends Fragment{

    public static final String ARG_LABEL_FRAME = "labelFrame";
    private MainActivity mainActivity;
    private RobotHelper robotHelper;
    private QiContext qiContext;

    private AttachedFrame location;
    private String locationLabel = "Gioconda";

    private Button buttonLocalize;
    private Button buttonGioconda;
    private Button buttonMapFrame;

    public NavigationFragment() {
        // Required empty public constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view = inflater.inflate(R.layout.fragment_navigation, container, false);

        /**
        buttonLocalize = view.findViewById(R.id.buttonLocalization);
        buttonGioconda = view.findViewById(R.id.buttonGioconda);
        buttonMapFrame = view.findViewById(R.id.buttonMapFrame);

        buttonLocalize.setOnClickListener(v -> {
            mainActivity.startLocalizing();
        });

        buttonGioconda.setOnClickListener(v -> {
            locationLabel = "Gioconda";
            if (locationLabel != null) {
                location = mainActivity.getSavedLocations().get(locationLabel);
                if(location != null){
                    goToLocation();
                }
            }
        });

        buttonMapFrame.setOnClickListener(v -> {
            locationLabel = "mapFrame";
            if (locationLabel != null) {
                goToLocation();
            }
        });
        **/


        return view;
    }

    @Override
    public void onStart() {
        super.onStart();
    }

    @Override
    public void onAttach(@NonNull Context context) {
        super.onAttach(context);
        if(context instanceof MainActivity){
            mainActivity = (MainActivity) context;
            robotHelper = mainActivity.getRobotHelper();
            qiContext = mainActivity.getQiContext();
            init();
        }
    }

    /**
     * Init the listeners for robot movement
     */
    private void init(){
        //TODO set listener
        robotHelper.goToHelper.addOnStartedMovingListener(() -> mainActivity.runOnUiThread(() -> {
            Log.d(MainActivity.CONSOLE_TAG, "Movement started");

            mainActivity.onNavigationStarted();
            robotHelper.goToHelper.removeOnStartedMovingListeners();
        }));
        robotHelper.goToHelper.addOnFinishedMovingListener((goToStatus) -> {
            if(goToStatus == GoToHelper.GoToStatus.FINISHED){
                Log.d(MainActivity.CONSOLE_TAG, "Navigation Finished");

                mainActivity.onNavigationFinished();
            }
            else if(goToStatus == GoToHelper.GoToStatus.CANCELLED){
                Log.d(MainActivity.CONSOLE_TAG, "Navigation Cancelled");

                mainActivity.onNavigationCancelled();
            }
            else{
                Log.d(MainActivity.CONSOLE_TAG, "Navigation Failed");

                mainActivity.onNavigationFailed();
            }
            robotHelper.goToHelper.removeOnFinishedMovingListeners();
        });
    }



    /**
     * Send the robot to the desired position.
     */
    public void goToLocation() {
        Log.d(MainActivity.CONSOLE_TAG, "goToLocation: " + locationLabel);
        robotHelper.say("Let's go to " + locationLabel + "!!");
        robotHelper.goToHelper.checkAndCancelCurrentGoto().thenConsume(aVoid -> {
            robotHelper.holdAbilities(true);
            if (this.locationLabel.equalsIgnoreCase("mapFrame")) {
                robotHelper.goToHelper.goToMapFrame(false, false, OrientationPolicy.FREE_ORIENTATION);
            }
            else {
                robotHelper.goToHelper.goTo(this.location, false, false, OrientationPolicy.FREE_ORIENTATION);
            }
        });
    }

}