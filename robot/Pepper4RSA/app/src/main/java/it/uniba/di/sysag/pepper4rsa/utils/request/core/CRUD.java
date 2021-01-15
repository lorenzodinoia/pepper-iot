package it.uniba.di.sysag.pepper4rsa.utils.request.core;

import java.util.Collection;

import it.uniba.di.sysag.pepper4rsa.utils.models.Model;

public interface CRUD<T extends Model> {
    void create(T model, RequestListener<T> requestListener);

    void read(long id, RequestListener<T> requestListener);

    void readAll(RequestListener<Collection<T>> requestListener);

    void update(T model, RequestListener<T> requestListener);

    void delete(long id, RequestListener<Boolean> requestListener);
}
