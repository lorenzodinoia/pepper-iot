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

import it.uniba.di.sysag.pepper4rsa.utils.map.LocalizeAndMapHelper;
import it.uniba.di.sysag.pepper4rsa.utils.map.RobotHelper;

public class MainFragment extends Fragment {

    public static final String FRAGMENT_TAG = "main_fragment";

    private Button buttonStartLocalize;
    private Button buttonStartService;

    private MainActivity mainActivity;
    private RobotHelper robotHelper;

    public MainFragment() {
        // Required empty public constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view = inflater.inflate(R.layout.fragment_main, container, false);

        robotHelper = mainActivity.getRobotHelper();
        robotHelper.say(getString(R.string.starting_phrase));
        buttonStartLocalize = view.findViewById(R.id.buttonStartLocalize);
        buttonStartService = view.findViewById(R.id.buttonStartService);

        robotHelper.localizeAndMapHelper.addOnFinishedLocalizingListener(result -> {
            robotHelper.releaseAbilities();
            mainActivity.runOnUiThread(() -> {
                if (result == LocalizeAndMapHelper.LocalizationStatus.LOCALIZED) {
                    robotHelper.localizeAndMapHelper.removeOnFinishedLocalizingListeners();
                    robotHelper.say(getString(R.string.localization_finished));
                    Log.d(MainActivity.CONSOLE_TAG, "Localized");
                    mainActivity.setLocalized(true);
                    buttonStartService.setEnabled(true);
                    buttonStartService.setAlpha(1);
                    buttonStartService.setCompoundDrawablesWithIntrinsicBounds(0, R.drawable.ic_icn_goto_frame, 0, 0);
                    buttonStartLocalize.setCompoundDrawablesWithIntrinsicBounds(0, R.drawable.ic_icn_localize_robot_burgermenu_oklocation, 0, 0);
                } else if (result == LocalizeAndMapHelper.LocalizationStatus.MAP_MISSING) {
                    robotHelper.localizeAndMapHelper.removeOnFinishedLocalizingListeners();
                    robotHelper.say(getString(R.string.map_missing));
                    Log.d(MainActivity.CONSOLE_TAG, "Map_Missing");
                } else if (result == LocalizeAndMapHelper.LocalizationStatus.FAILED) {
                    robotHelper.say(getString(R.string.localization_failed));
                    Log.d(MainActivity.CONSOLE_TAG, "Failed");
                } else {
                    Log.d(MainActivity.CONSOLE_TAG, "onViewCreated: Unable to localize in Map");
                }
            });
        });

        buttonStartLocalize.setOnClickListener(v -> {
            if(robotHelper.askToCloseIfFlapIsOpened(mainActivity)){
                Log.d(MainActivity.CONSOLE_TAG, "Flat opened");
            }
            else {
                Log.d(MainActivity.CONSOLE_TAG, "Localize Button");
                mainActivity.startLocalizing();
            }
        });

        buttonStartService.setOnClickListener(v -> {
            if(robotHelper.askToCloseIfFlapIsOpened(mainActivity)){
                Log.d(MainActivity.CONSOLE_TAG, "Flat opened");
            }
            else{
                if(mainActivity.isLocalized()) {
                    Log.d(MainActivity.CONSOLE_TAG, "Start Service Button");
                    NavigationFragment navigationFragment = new NavigationFragment();
                    mainActivity.getSupportFragmentManager().beginTransaction().replace(R.id.frame_fragment, navigationFragment).addToBackStack(NavigationFragment.FRAGMENT_TAG).commit();
                }
                else{
                    robotHelper.say(getString(R.string.localize_before_start_service));
                }
            }
        });
        return view;
    }

    @Override
    public void onAttach(@NonNull Context context) {
        super.onAttach(context);
        if(context instanceof MainActivity){
            mainActivity = (MainActivity) context;
        }
    }
}