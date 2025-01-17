package it.uniba.di.sysag.pepper4rsa;

import android.content.Context;
import android.graphics.PointF;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import com.airbnb.lottie.LottieAnimationView;
import com.aldebaran.qi.Future;
import com.aldebaran.qi.sdk.QiContext;
import com.aldebaran.qi.sdk.builder.ChatBuilder;
import com.aldebaran.qi.sdk.builder.ListenBuilder;
import com.aldebaran.qi.sdk.builder.PhraseSetBuilder;
import com.aldebaran.qi.sdk.builder.QiChatbotBuilder;
import com.aldebaran.qi.sdk.builder.TopicBuilder;
import com.aldebaran.qi.sdk.object.actuation.AttachedFrame;
import com.aldebaran.qi.sdk.object.actuation.Frame;
import com.aldebaran.qi.sdk.object.actuation.OrientationPolicy;
import com.aldebaran.qi.sdk.object.conversation.Chat;
import com.aldebaran.qi.sdk.object.conversation.Listen;
import com.aldebaran.qi.sdk.object.conversation.ListenResult;
import com.aldebaran.qi.sdk.object.conversation.PhraseSet;
import com.aldebaran.qi.sdk.object.conversation.QiChatbot;
import com.aldebaran.qi.sdk.object.conversation.Topic;
import com.aldebaran.qi.sdk.object.geometry.Transform;
import com.aldebaran.qi.sdk.object.locale.Language;
import com.aldebaran.qi.sdk.object.locale.Locale;
import com.aldebaran.qi.sdk.object.locale.Region;
import com.aldebaran.qi.sdk.util.PhraseSetUtil;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Stack;
import java.util.StringTokenizer;
import java.util.Timer;
import java.util.TimerTask;
import java.util.TreeMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import it.uniba.di.sysag.pepper4rsa.utils.map.GoToHelper;
import it.uniba.di.sysag.pepper4rsa.utils.map.PointsOfInterestView;
import it.uniba.di.sysag.pepper4rsa.utils.map.RobotHelper;
import it.uniba.di.sysag.pepper4rsa.utils.models.Emergency;
import it.uniba.di.sysag.pepper4rsa.utils.request.EmergencyRequest;
import it.uniba.di.sysag.pepper4rsa.utils.request.core.RequestException;
import it.uniba.di.sysag.pepper4rsa.utils.request.core.RequestListener;

public class NavigationFragment extends Fragment implements EmergencyListener {
    public static final String FRAGMENT_TAG = "navigation_fragment";
    private static final String MAP_FRAME = "mapFrame";

    private MainActivity mainActivity;
    private RobotHelper robotHelper;
    private QiContext qiContext;
    private ScheduledExecutorService scheduledExecutorService;

    private Emergency emergency;
    private TreeMap<String, AttachedFrame> savedLocations;

    private EmergencyListener emergencyListener;

    private TextView gotoText;
    private LottieAnimationView gotoLoader;
    private TextView gotoFinishedText;
    private Frame robotFrame;
    private Frame mapFrame;
    private List<PointF> poiPositions;
    private String label;
    private Button btnStopNavigation;

    private Chat chat;
    private Stack<String> topics = new Stack<>();

    private Boolean atMapFrame = false;

    private Boolean stopGoToHuman = false;

    public static final HashMap<String, Integer> topicsMap = new HashMap<>();
    static{
        topicsMap.put("lux-", R.string.lux_minus_say);
        topicsMap.put("lux+", R.string.lux_plus_say);
        topicsMap.put("voc+", R.string.voc_plus_say);
        topicsMap.put("degree-", R.string.degree_minus_say);
        topicsMap.put("degree+", R.string.degree_plus_say);
        topicsMap.put("humidity+", R.string.humidity_plus_say);
    }

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

        gotoText = view.findViewById(R.id.goto_text);
        gotoText.setVisibility(View.GONE);
        gotoLoader = view.findViewById(R.id.goto_loader);
        gotoLoader.setVisibility(View.GONE);
        gotoFinishedText = view.findViewById(R.id.goto_finished_text);

        btnStopNavigation = view.findViewById(R.id.stop_navigation_button);

        btnStopNavigation.setVisibility(View.GONE);
        btnStopNavigation.setOnClickListener(v -> {
            stopGoToHuman = true;
            mainActivity.getRobotHelper().goToHelper.checkAndCancelCurrentGoto();
        });

        // Retrieve the robot Frame
        robotFrame = (mainActivity.getQiContext().getActuationAsync()).getValue().async().robotFrame().getValue();

        // Retrieve the origin of the map Frame
        mapFrame = (mainActivity.getQiContext().getMappingAsync()).getValue().async().mapFrame().getValue();

        PointsOfInterestView explorationMapView = view.findViewById(R.id.explorationMapViewPopup);

        mainActivity.getRobotHelper().localizeAndMapHelper.buildStreamableExplorationMap().andThenConsume(value -> {
            poiPositions = new ArrayList<>(mainActivity.getSavedLocations().size() + 1);
            for (Map.Entry<String, AttachedFrame> stringAttachedFrameEntry : mainActivity.getSavedLocations().entrySet()) {
                Transform transform = (((stringAttachedFrameEntry.getValue()).async().frame()).getValue().async().computeTransform(mapFrame)).getValue().getTransform();
                poiPositions.add(new PointF(((float) transform.getTranslation().getX()), (float) transform.getTranslation().getY()));
            }

            explorationMapView.setExplorationMap(value.getTopGraphicalRepresentation());
            explorationMapView.setMapFramPosition();
            explorationMapView.setPoiPositions(poiPositions);
        }).andThenConsume(value -> {
            int delay = 0;
            int period = 500;  // repeat every sec.
            Timer timer = new Timer();
            timer.scheduleAtFixedRate(new TimerTask() {
                public void run() {
                    // Compute the position of the robot relatively to the map Frame
                    Transform robotPos = robotFrame.computeTransform(mapFrame).getTransform();
                    // Set the position in the ExplorationMapView widget, it will be displayed as a red circle
                    explorationMapView.setRobotPosition(robotPos);
                }
            }, delay, period);
        });
        return view;
    }

    @Override
    public void onStart() {
        super.onStart();
        this.emergencyListener = this;
        //Request routine for emergency check
        scheduledExecutorService = Executors.newSingleThreadScheduledExecutor();
        scheduledExecutorService.scheduleAtFixedRate(() -> {
            EmergencyRequest emergencyRequest = new EmergencyRequest();
            emergencyRequest.getNext(new RequestListener<Emergency>() {
                @Override
                public void successResponse(Emergency response) {
                    if ((response == null) && (emergency != null)) {
                        emergency = null;
                        goToLocation(MAP_FRAME, null);
                    }
                    else if (response != null && emergencyListener != null) {
                        emergencyListener.onNewEmergency(response);
                    }
                }

                @Override
                public void errorResponse(RequestException error) {
                    Log.d(MainActivity.CONSOLE_TAG, error.getMessage());
                }
            });
        }, 0, 1, TimeUnit.MINUTES);
    }

    @Override
    public void onAttach(@NonNull Context context) {
        super.onAttach(context);
        if(context instanceof MainActivity){
            mainActivity = (MainActivity) context;
            robotHelper = mainActivity.getRobotHelper();
            qiContext = mainActivity.getQiContext();
            savedLocations = mainActivity.getSavedLocations();
        }
    }

    @Override
    public void onStop() {
        super.onStop();
        scheduledExecutorService.shutdownNow();
    }

    /**
     * Init the listeners for robot movement
     */
    private void registerListener(){
        robotHelper.goToHelper.addOnStartedMovingListener(() -> mainActivity.runOnUiThread(() -> {
            Log.d(MainActivity.CONSOLE_TAG, "Movement started");
            mainActivity.runOnUiThread(() -> {
                gotoText.setVisibility(View.VISIBLE);
                btnStopNavigation.setVisibility(View.VISIBLE);
                if(emergency == null){
                    gotoText.setText(getString(R.string.back_to_mapFrame));
                }
                else {
                    if (emergency.getType() == 0) {
                        gotoText.setText(getString(R.string.goto_text) + emergency.getEnvData().getRoom().getName());
                    } else {
                        gotoText.setText(getString(R.string.goto_text) + emergency.getBedLabel());
                    }
                }
                gotoLoader.setVisibility(View.VISIBLE);
            });
            robotHelper.goToHelper.removeOnStartedMovingListeners();
        }));

        robotHelper.goToHelper.addOnFinishedMovingListener((goToStatus) -> {
            mainActivity.runOnUiThread(() -> {
                gotoText.setVisibility(View.GONE);
                gotoLoader.setVisibility(View.GONE);
                btnStopNavigation.setVisibility(View.GONE);
            });

            if(goToStatus == GoToHelper.GoToStatus.FINISHED) {
                robotHelper.releaseAbilities().andThenConsume(value -> {
                    Log.d(MainActivity.CONSOLE_TAG, "Navigation Finished");
                    if (emergencyListener == null) {
                        if(emergency != null) {
                            Thread thread = new Thread(() -> handleEmergency(emergency));
                            thread.start();
                        }
                    }
                });
            }
            else if(goToStatus == GoToHelper.GoToStatus.CANCELLED){
                Log.d(MainActivity.CONSOLE_TAG, "Navigation Cancelled");
                if(stopGoToHuman) {
                    stopGoToHuman = false;
                    mainActivity.getSupportFragmentManager().popBackStack(NavigationFragment.FRAGMENT_TAG, FragmentManager.POP_BACK_STACK_INCLUSIVE);
                    robotHelper.say(getString(R.string.navigation_cancelled_by_human));
                }
                else{
                    robotHelper.say(getString(R.string.navigation_cancelled));
                }
            }
            else{
                Log.d(MainActivity.CONSOLE_TAG, "Navigation Failed");
                robotHelper.say(getString(R.string.navigation_failed));
            }

            robotHelper.goToHelper.removeOnFinishedMovingListeners();
        });
    }



    /**
     * Send the robot to the desired position.
     */
    public void goToLocation(String locationLabel, AttachedFrame location) {
        this.label = locationLabel;
        Log.d(MainActivity.CONSOLE_TAG, "goToLocation: " + locationLabel);
        registerListener();
        robotHelper.goToHelper.checkAndCancelCurrentGoto().thenConsume(aVoid -> {
            robotHelper.holdAbilities(true);
            if (locationLabel.equalsIgnoreCase(MAP_FRAME)) {
                robotHelper.goToHelper.goToMapFrame(false, false, OrientationPolicy.FREE_ORIENTATION);
                atMapFrame = false;
            }
            else {
                robotHelper.goToHelper.goTo(location, false, false, OrientationPolicy.FREE_ORIENTATION);
                atMapFrame = true;

            }
        });
    }

    @Override
    public void onNewEmergency(Emergency emergency) {
        this.emergencyListener = null;
        this.emergency = emergency;
        String locationLabel;
        if(emergency.getType() == 0){
            locationLabel = emergency.getEnvData().getRoom().getName();
        }
        else{
            locationLabel = emergency.getBedLabel();
        }

        if(locationLabel != null) {
            AttachedFrame location = savedLocations.get(locationLabel);
            if(location != null){
                goToLocation(locationLabel, location);
            }
        }


    }

    @Override
    public void onEmergencyHandled() {
        EmergencyRequest emergencyRequest = new EmergencyRequest();
        emergencyRequest.setAsDone(emergency.getId(), new RequestListener<Boolean>() {
            @Override
            public void successResponse(Boolean response) {
                Log.d(MainActivity.CONSOLE_TAG, "SetAdDone success");
            }

            @Override
            public void errorResponse(RequestException error) {
                Log.d(MainActivity.CONSOLE_TAG, "SetAdDone failed");
            }
        });
    }

    private void handleEmergency(Emergency emergency){
        PhraseSet phraseSetYes = PhraseSetBuilder.with(qiContext).withTexts("si", "ok", "certo", "si, grazie", "si, certo").build();
        PhraseSet phraseSetNo = PhraseSetBuilder.with(qiContext).withTexts("no", "no, grazie", "non serve").build();

        robotHelper.saySync(getString(R.string.hello)).run();

        switch (emergency.getType()) {
            case 0:
                Listen listen = ListenBuilder.with(qiContext).withPhraseSets(phraseSetYes, phraseSetNo).build();
                String tags = emergency.getTags();
                Log.d(MainActivity.CONSOLE_TAG, "tags: " + tags);
                StringTokenizer stringTokenizer = new StringTokenizer(tags, ";");
                while (stringTokenizer.hasMoreTokens()){
                    String tag = stringTokenizer.nextToken();
                    Log.d(MainActivity.CONSOLE_TAG, tag);
                    if(topicsMap.containsKey(tag)){
                        robotHelper.saySync(getString(topicsMap.get(tag))).run();
                        ListenResult listenResult = listen.run();
                        PhraseSet matchedPhraseSet = listenResult.getMatchedPhraseSet();
                        if(PhraseSetUtil.equals(matchedPhraseSet, phraseSetYes)){
                            Log.d(MainActivity.CONSOLE_TAG, "PhraseSet Yes");
                        }
                        else{
                            Log.d(MainActivity.CONSOLE_TAG, "PhraseSet No");
                        }
                        robotHelper.saySync("Ok").run();
                    }
                }

                robotHelper.saySync("Posso fare altro per te o posso andare?").run();
                startTopic(R.raw.emergency, endReason -> {
                    robotHelper.releaseAbilities();
                    emergencyListener = NavigationFragment.this;
                    emergencyListener.onEmergencyHandled();
                    NavigationFragment.this.emergency = null;
                    goToLocation(MAP_FRAME, null);
                });
                break;
            case 1:
                robotHelper.saySync(getString(R.string.vital_sings_em_phrase)).run();
                startTopic(R.raw.emergency, endReason -> {
                    robotHelper.releaseAbilities();
                    emergencyListener = NavigationFragment.this;
                    emergencyListener.onEmergencyHandled();
                    NavigationFragment.this.emergency = null;
                    goToLocation(MAP_FRAME, null);
                });
                break;
            case 2:
                robotHelper.saySync(getString(R.string.emergency_button_phrase)).run();
                startTopic(R.raw.emergency, endReason -> {
                    robotHelper.releaseAbilities();
                    emergencyListener = NavigationFragment.this;
                    emergencyListener.onEmergencyHandled();
                    NavigationFragment.this.emergency = null;
                    goToLocation(MAP_FRAME, null);
                });
                break;
            case 3:
                robotHelper.saySync(getString(R.string.send_pepper_phrase)).run();
                startTopic(R.raw.emergency, endReason -> {
                    robotHelper.releaseAbilities();
                    emergencyListener = NavigationFragment.this;
                    emergencyListener.onEmergencyHandled();
                    NavigationFragment.this.emergency = null;
                    goToLocation(MAP_FRAME, null);
                });
                break;
            default:
                break;
        }
    }

    private void startTopic(Integer topicResource, QiChatbot.OnEndedListener chatEndedListener){
        Locale locale = new Locale(Language.ITALIAN, Region.ITALY);
        Topic topic = TopicBuilder.with(qiContext)
                .withResource(topicResource)
                .build();

        QiChatbot qiChatbot = QiChatbotBuilder.with(qiContext)
                .withTopic(topic)
                .withLocale(locale)
                .build();

        chat = ChatBuilder.with(qiContext)
                .withChatbot(qiChatbot)
                .withLocale(locale)
                .build();

        chat.addOnStartedListener(() -> {
            Log.d(MainActivity.CONSOLE_TAG, "Topic started");
            if (chat != null) {
                chat.removeAllOnStartedListeners();
            }
        });

        Future<Void> chatFuture = chat.async().run();

        qiChatbot.addOnEndedListener(endReason -> {
            chatFuture.requestCancellation();
        });
        qiChatbot.addOnEndedListener(chatEndedListener);

        chatFuture.thenConsume(value -> {
            if (value.hasError()) {
                Log.d(MainActivity.CONSOLE_TAG, "Discussion finished with error.", value.getError());
            }
        });
    }
}
