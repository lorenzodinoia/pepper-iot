package it.uniba.di.sysag.pepper4rsa.utils.request.core;

public interface RequestListener<T> {
    void successResponse(T response);
    void errorResponse(RequestException error);
}
