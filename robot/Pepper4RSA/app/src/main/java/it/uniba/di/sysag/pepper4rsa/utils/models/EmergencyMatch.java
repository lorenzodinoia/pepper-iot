package it.uniba.di.sysag.pepper4rsa.utils.models;

public class EmergencyMatch {

    private int topic;
    private int phrase;

    public EmergencyMatch(int topic, int phrase){
        this.topic = topic;
        this.phrase = phrase;
    }

    public int getTopic() {
        return topic;
    }

    public void setTopic(int topic) {
        this.topic = topic;
    }

    public int getPhrase() {
        return phrase;
    }

    public void setPhrase(int phrase) {
        this.phrase = phrase;
    }

}
