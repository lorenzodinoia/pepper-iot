package it.uniba.di.sysag.pepper4rsa.utils.models;

import com.aldebaran.qi.sdk.object.conversation.PhraseSet;

public class EmergencyMatch {

    private PhraseSet phraseSet;
    private int phrase;

    public EmergencyMatch(PhraseSet phraseSet, int phrase){
        this.phraseSet = phraseSet;
        this.phrase = phrase;
    }

    public PhraseSet getPhraseSet() {
        return phraseSet;
    }

    public void setPhraseSet(PhraseSet phraseSet) {
        this.phraseSet = phraseSet;
    }

    public int getPhrase() {
        return phrase;
    }

    public void setPhrase(int phrase) {
        this.phrase = phrase;
    }

}
