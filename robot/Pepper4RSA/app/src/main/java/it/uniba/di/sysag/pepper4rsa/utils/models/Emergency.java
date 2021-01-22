package it.uniba.di.sysag.pepper4rsa.utils.models;

import android.os.Parcel;

public class Emergency extends Model{

    private int type_em;
    private int level_em;
    private int env_data_id;
    private int vital_signs_id;
    private int bed_id;

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
        this.type_em = in.readInt();
        this.level_em = in.readInt();
        this.env_data_id = in.readInt();
        this.vital_signs_id = in.readInt();
        this.bed_id = in.readInt();
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        super.writeToParcel(dest, flags);
        dest.writeInt(this.type_em);
        dest.writeInt(this.level_em);
        dest.writeInt(this.env_data_id);
        dest.writeInt(this.vital_signs_id);
        dest.writeInt(this.bed_id);
    }

    public int getType_em() {
        return type_em;
    }

    public void setType_em(int type_em) {
        this.type_em = type_em;
    }

    public int getLevel_em() {
        return level_em;
    }

    public void setLevel_em(int level_em) {
        this.level_em = level_em;
    }

    public int getEnv_data_id() {
        return env_data_id;
    }

    public void setEnv_data_id(int env_data_id) {
        this.env_data_id = env_data_id;
    }

    public int getVital_signs_id() {
        return vital_signs_id;
    }

    public void setVital_signs_id(int vital_signs_id) {
        this.vital_signs_id = vital_signs_id;
    }

    public int getBed_id() {
        return bed_id;
    }

    public void setBed_id(int bed_id) {
        this.bed_id = bed_id;
    }
}
