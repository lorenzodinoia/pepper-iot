package it.uniba.di.sysag.pepper4rsa.thread;

import android.os.AsyncTask;

import com.aldebaran.qi.sdk.QiContext;
import com.aldebaran.qi.sdk.builder.SayBuilder;
import com.aldebaran.qi.sdk.object.conversation.Say;

public class SayThread extends AsyncTask<String, Void, Void>  {
    private QiContext qiContext;

    public SayThread(QiContext qiContext) {
        this.qiContext = qiContext;
    }

    @Override
    protected Void doInBackground(String... strings) {
        Say say = SayBuilder.with(this.qiContext).withText(strings[0]).build();
        say.run();
        return null;
    }
}
