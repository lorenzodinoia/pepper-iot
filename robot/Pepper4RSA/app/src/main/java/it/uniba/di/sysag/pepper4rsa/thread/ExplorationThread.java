package it.uniba.di.sysag.pepper4rsa.thread;

import android.app.Activity;
import android.os.AsyncTask;

import com.aldebaran.qi.Future;
import com.aldebaran.qi.sdk.QiContext;
import com.aldebaran.qi.sdk.builder.LocalizeAndMapBuilder;
import com.aldebaran.qi.sdk.object.actuation.ExplorationMap;
import com.aldebaran.qi.sdk.object.actuation.LocalizationStatus;
import com.aldebaran.qi.sdk.object.actuation.LocalizeAndMap;
import it.uniba.di.sysag.pepper4rsa.ExplorationListener;

public class ExplorationThread extends AsyncTask<Object, Void, Void> {
    private Future<Void> localizingAndMap;
    private ExplorationMap explorationMap;
    private ExplorationListener explorationListener;
    private Activity activity;
    private QiContext qiContext;

    public ExplorationThread(Activity activity, QiContext qiContext, ExplorationListener explorationListener) {
        this.activity = activity;
        this.explorationListener = explorationListener;
        this.qiContext = qiContext;
    }

    @Override
    protected Void doInBackground(Object... objects) {
        LocalizeAndMap localizeAndMap = LocalizeAndMapBuilder.with(this.qiContext).build();
        localizeAndMap.addOnStatusChangedListener(status -> {
            if (status == LocalizationStatus.LOCALIZED) {
                localizingAndMap.requestCancellation();
                explorationMap = localizeAndMap.dumpMap();
                activity.runOnUiThread(() -> explorationListener.onSuccess(explorationMap));
            }
        });
        localizingAndMap = localizeAndMap.async().run();
        return null;
    }
}