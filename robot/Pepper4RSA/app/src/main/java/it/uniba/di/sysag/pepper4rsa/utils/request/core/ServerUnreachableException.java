package it.uniba.di.sysag.pepper4rsa.utils.request.core;

import com.android.volley.VolleyError;

public class ServerUnreachableException extends RequestException {
    public ServerUnreachableException(VolleyError volleyError, String message) {
        super(volleyError, message);
    }
}
