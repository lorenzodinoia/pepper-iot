package it.uniba.di.sysag.pepper4rsa.utils.models;

import android.os.Parcel;

public class VitalData extends Model {

    private int bpm;
    private float body_temperature;
    private int min_body_pressure;
    private int max_body_pressure;
    private int blood_oxygenation;
    private int inmate_id;


    public void VitalData(){

    }

    public static final Creator<VitalData> CREATOR = new Creator<VitalData>() {
        @Override
        public VitalData createFromParcel(Parcel in) {
            return new VitalData(in);
        }

        @Override
        public VitalData[] newArray(int size) {
            return new VitalData[size];
        }
    };

    public VitalData(Parcel in) {
        super(in);
        this.bpm = in.readInt();
        this.body_temperature = in.readFloat();
        this.min_body_pressure = in.readInt();
        this.max_body_pressure = in.readInt();
        this.blood_oxygenation = in.readInt();
        this.inmate_id = in.readInt();
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        super.writeToParcel(dest, flags);
        dest.writeInt(this.bpm);
        dest.writeFloat(this.body_temperature);
        dest.writeInt(this.min_body_pressure);
        dest.writeInt(this.max_body_pressure);
        dest.writeInt(this.blood_oxygenation);
        dest.writeInt(this.inmate_id);
    }

    public int getBpm() {
        return bpm;
    }

    public void setBpm(int bpm) {
        this.bpm = bpm;
    }

    public float getBody_temperature() {
        return body_temperature;
    }

    public void setBody_temperature(float body_temperature) {
        this.body_temperature = body_temperature;
    }

    public int getMin_body_pressure() {
        return min_body_pressure;
    }

    public void setMin_body_pressure(int min_body_pressure) {
        this.min_body_pressure = min_body_pressure;
    }

    public int getMax_body_pressure() {
        return max_body_pressure;
    }

    public void setMax_body_pressure(int max_body_pressure) {
        this.max_body_pressure = max_body_pressure;
    }

    public int getBlood_oxygenation() {
        return blood_oxygenation;
    }

    public void setBlood_oxygenation(int blood_oxygenation) {
        this.blood_oxygenation = blood_oxygenation;
    }

    public int getInmate_id() {
        return inmate_id;
    }

    public void setInmate_id(int inmate_id) {
        this.inmate_id = inmate_id;
    }
}
