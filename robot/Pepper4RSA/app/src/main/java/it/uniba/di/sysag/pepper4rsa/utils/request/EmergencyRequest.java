package it.uniba.di.sysag.pepper4rsa.utils.request;

import com.android.volley.Request;

import java.util.Collection;

import it.uniba.di.sysag.pepper4rsa.utils.Constants;
import it.uniba.di.sysag.pepper4rsa.utils.models.Emergency;
import it.uniba.di.sysag.pepper4rsa.utils.provider.Providers;
import it.uniba.di.sysag.pepper4rsa.utils.request.core.CRUD;
import it.uniba.di.sysag.pepper4rsa.utils.request.core.CRUDRequest;
import it.uniba.di.sysag.pepper4rsa.utils.request.core.ObjectRequest;
import it.uniba.di.sysag.pepper4rsa.utils.request.core.RequestExceptionFactory;
import it.uniba.di.sysag.pepper4rsa.utils.request.core.RequestListener;

public class EmergencyRequest extends CRUDRequest<Emergency> implements CRUD<Emergency> {
    @Override
    public void create(Emergency model, RequestListener<Emergency> requestListener) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void read(long id, RequestListener<Emergency> requestListener) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void readAll(RequestListener<Collection<Emergency>> requestListener) {
        super.readAll("emergency/", requestListener, Emergency.class);
    }

    @Override
    public void update(Emergency model, RequestListener<Emergency> requestListener) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void delete(long id, RequestListener<Boolean> requestListener) {
        throw new UnsupportedOperationException();
    }

    public void setAsDone(long id, RequestListener<Boolean> requestListener){

        String url = String.format("emergency?id=%d", id);
        ObjectRequest request = new ObjectRequest(Request.Method.PUT, String.format("%s/api/%s", Constants.SERVER_HOST, url), null,
                response -> {
                    requestListener.successResponse(true);
                },
                error ->requestListener.errorResponse(RequestExceptionFactory.createExceptionFromError(error)));

        Providers.getRequestProvider().addToQueue(request);
    }
}
