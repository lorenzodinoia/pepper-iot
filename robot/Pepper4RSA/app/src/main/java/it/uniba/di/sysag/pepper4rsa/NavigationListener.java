package it.uniba.di.sysag.pepper4rsa;

public interface NavigationListener {

    void onNavigationStarted();

    void onNavigationFinished();

    void onNavigationCancelled();

    void onNavigationFailed();
}
