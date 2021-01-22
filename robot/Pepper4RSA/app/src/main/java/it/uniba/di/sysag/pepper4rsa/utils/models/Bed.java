package it.uniba.di.sysag.pepper4rsa.utils.models;

import android.os.Parcel;

public class Bed extends Model{

    private int roomId;
    private int inmateId;

    public Bed (){

    }

    public static final Creator<Bed> CREATOR = new Creator<Bed>() {
        @Override
        public Bed createFromParcel(Parcel in) {
            return new Bed(in);
        }

        @Override
        public Bed[] newArray(int size) {
            return new Bed[size];
        }
    };

    public Bed(Parcel in) {
        super(in);
        this.roomId = in.readInt();
        this.inmateId = in.readInt();
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        super.writeToParcel(dest, flags);
        dest.writeInt(this.roomId);
        dest.writeInt(this.inmateId);
    }

    public int getRoomId() {
        return roomId;
    }

    public void setRoomId(int roomId) {
        this.roomId = roomId;
    }

    public int getInmateId() {
        return inmateId;
    }

    public void setInmateId(int inmateId) {
        this.inmateId = inmateId;
    }
}
