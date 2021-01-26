package it.uniba.di.sysag.pepper4rsa.utils.models;

import android.os.Parcel;

public class EnvData extends Model{

    private int lux;
    private float voc;
    private float degree;
    private int humidity;
    private int roomId;

    public EnvData (){

    }

    public static final Creator<EnvData> CREATOR = new Creator<EnvData>() {
        @Override
        public EnvData createFromParcel(Parcel in) {
            return new EnvData(in);
        }

        @Override
        public EnvData[] newArray(int size) {
            return new EnvData[size];
        }
    };

    public EnvData(Parcel in) {
        super(in);
        this.lux = in.readInt();
        this.voc = in.readFloat();
        this.degree = in.readFloat();
        this.humidity = in.readInt();
        this.roomId = in.readInt();
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        super.writeToParcel(dest, flags);
        dest.writeInt(this.lux);
        dest.writeFloat(this.voc);
        dest.writeFloat(this.degree);
        dest.writeInt(this.humidity);
        dest.writeInt(this.roomId);
    }

    public int getLux() {
        return lux;
    }

    public void setLux(int lux) {
        this.lux = lux;
    }

    public float getVoc() {
        return voc;
    }

    public void setVoc(float voc) {
        this.voc = voc;
    }

    public float getDegree() {
        return degree;
    }

    public void setDegree(float degree) {
        this.degree = degree;
    }

    public int getHumidity() {
        return humidity;
    }

    public void setHumidity(int humidity) {
        this.humidity = humidity;
    }

    public int getRoomId() {
        return roomId;
    }

    public void setRoomId(int roomId) {
        this.roomId = roomId;
    }
}
