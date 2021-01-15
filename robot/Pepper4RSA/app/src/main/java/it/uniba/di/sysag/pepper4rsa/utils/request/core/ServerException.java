package it.uniba.di.sysag.pepper4rsa.utils.request.core;

import com.android.volley.VolleyError;

public class ServerException extends RequestException {
    public ServerException(VolleyError volleyError, String message) {
        super(volleyError, message);
    }
}
