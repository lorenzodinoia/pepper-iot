package it.uniba.di.sysag.pepper4rsa.utils.request;

import java.util.Collection;

import it.uniba.di.sysag.pepper4rsa.utils.models.Room;
import it.uniba.di.sysag.pepper4rsa.utils.request.core.CRUD;
import it.uniba.di.sysag.pepper4rsa.utils.request.core.CRUDRequest;
import it.uniba.di.sysag.pepper4rsa.utils.request.core.RequestListener;

public class RoomRequest extends CRUDRequest<Room> implements CRUD<Room> {

    @Override
    public void create(Room model, RequestListener<Room> requestListener) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void read(long id, RequestListener<Room> requestListener) {

    }

    @Override
    public void readAll(RequestListener<Collection<Room>> requestListener) {
        super.readAll("room/list", requestListener, Room.class);
    }

    @Override
    public void update(Room model, RequestListener<Room> requestListener) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void delete(long id, RequestListener<Boolean> requestListener) {
        throw new UnsupportedOperationException();
    }
}
