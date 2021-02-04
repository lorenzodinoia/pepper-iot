package it.uniba.di.sysag.pepper4rsa.utils.models;

import android.os.Parcel;

import androidx.annotation.NonNull;

import com.google.gson.annotations.SerializedName;

import java.util.HashMap;

public class Emergency extends Model{

    private int type;
    private int level;
    @SerializedName("env_data")
    private EnvData envData;
    @SerializedName("vital_signs")
    private VitalData vitalSigns;
    private String bedLabel;
    private String tags;

    public Emergency(){

    }

    public static final Creator<Emergency> CREATOR = new Creator<Emergency>() {
        @Override
        public Emergency createFromParcel(Parcel in) {
            return new Emergency(in);
        }

        @Override
        public Emergency[] newArray(int size) {
            return new Emergency[size];
        }
    };

    public Emergency(Parcel in) {
        super(in);
        this.type = in.readInt();
        this.level = in.readInt();
        this.envData = in.readParcelable(EnvData.class.getClassLoader());
        this.vitalSigns = in.readParcelable(VitalData.class.getClassLoader());
        this.bedLabel = in.readString();
        this.tags = in.readString();
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        super.writeToParcel(dest, flags);
        dest.writeInt(this.type);
        dest.writeInt(this.level);
        dest.writeParcelable(this.envData, flags);
        dest.writeParcelable(this.vitalSigns, flags);
        dest.writeString(this.bedLabel);
        dest.writeString(this.tags);
    }

    public int getType() {
        return type;
    }

    public void setType(int type) {
        this.type = type;
    }

    public int getLevel() {
        return level;
    }

    public void setLevel(int level) {
        this.level = level;
    }

    public EnvData getEnvData() {
        return envData;
    }

    public void setEnvData(EnvData envData) {
        this.envData = envData;
    }

    public VitalData getVitalSigns() {
        return vitalSigns;
    }

    public void setVitalSigns(VitalData vitalSigns) {
        this.vitalSigns = vitalSigns;
    }

    public String getBedLabel() {
        return bedLabel;
    }

    public void setBedLabel(String bedLabel) {
        this.bedLabel = bedLabel;
    }

    public String getTags() {
        return tags;
    }

    public void setTags(String tags) {
        this.tags = tags;
    }
}
