package it.uniba.di.sysag.pepper4rsa;

import it.uniba.di.sysag.pepper4rsa.utils.models.Emergency;

public interface EmergencyListener {

    void onNewEmergency(Emergency emergency);

    void onEmergencyHandled();
}
