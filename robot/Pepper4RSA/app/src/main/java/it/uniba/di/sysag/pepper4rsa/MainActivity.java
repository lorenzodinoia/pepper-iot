package it.uniba.di.sysag.pepper4rsa;

import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;

import com.aldebaran.qi.sdk.QiContext;
import com.aldebaran.qi.sdk.QiSDK;
import com.aldebaran.qi.sdk.RobotLifecycleCallbacks;
import com.aldebaran.qi.sdk.design.activity.RobotActivity;
import com.google.android.material.button.MaterialButton;

import it.uniba.di.sysag.pepper4rsa.thread.ExplorationThread;
import it.uniba.di.sysag.pepper4rsa.utils.ExplorationUtils;
import it.uniba.di.sysag.pepper4rsa.utils.provider.Providers;

public class MainActivity extends RobotActivity implements RobotLifecycleCallbacks {
    private MaterialButton buttonExploration;
    private QiContext qiContext;
    private ImageView imageView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //Services initialization
        QiSDK.register(this, this);
        Providers.init(getApplicationContext());

        setContentView(R.layout.activity_main);
        this.imageView = this.findViewById(R.id.imageViewMap);
        this.buttonExploration = this.findViewById(R.id.buttonExploration);
        this.buttonExploration.setOnClickListener(v -> {
            new ExplorationThread(MainActivity.this, qiContext, explorationMap -> {
                ExplorationUtils.saveExploration(explorationMap, "Prova", getApplicationContext());
                imageView.setVisibility(View.VISIBLE);
                imageView.setImageBitmap(ExplorationUtils.getBitmap(explorationMap));
            }).execute();
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
    }

    @Override
    public void onRobotFocusLost() {

    }

    @Override
    public void onRobotFocusRefused(String reason) {

    }
}