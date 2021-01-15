package it.uniba.di.sysag.pepper4rsa.utils.provider;

import java.util.HashMap;
import java.util.Map;

import it.uniba.di.sysag.pepper4rsa.utils.adapter.Adapter;
import it.uniba.di.sysag.pepper4rsa.utils.models.Model;
import it.uniba.di.sysag.pepper4rsa.utils.models.Room;


public final class AdapterProvider {
    private static final Map<Class<? extends Model>, Adapter<? extends Model>> adapters = new HashMap<>();

    static {
        adapters.put(Room.class, new Adapter<Room>());
    }

    public static <T extends Model> Adapter<T> getAdapterFor(Class<T> modelClass) {
        return (Adapter<T>) adapters.get(modelClass);
    }
}
