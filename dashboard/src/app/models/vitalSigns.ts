import { Model } from "./model";

export class VitalSigns extends Model {
    private _bpm: number;
    private _bodyTemperature: number;
    private _bloodMinPressure: number;
    private _bloodMaxPressure: number;
    private _bloodOxygenation: number;
    private _timestamp: Date;

    constructor(id: number, bpm: number, bodyTemperature: number, bloodMaxPressure: number, bloodMinPressure: number,bloodOxygenation: number, timestamp: Date) {
        super(id);
        this._bpm = bpm;
        this._bodyTemperature = bodyTemperature;
        this._bloodMaxPressure = bloodMaxPressure;
        this._bloodMinPressure = bloodMinPressure;
        this._bloodOxygenation = bloodOxygenation;
        this._timestamp = timestamp;
    }

    public get bpm(): number {
        return this._bpm;
    }

    public get bodyTemperature(): number {
        return this._bodyTemperature;
    }

    public get bloodMaxPressure(): number {
        return this._bloodMaxPressure;
    }

    public get bloodMinPressure(): number {
        return this._bloodMinPressure;
    }

    public get bloodOxygenation(): number {
        return this._bloodOxygenation;
    }

    public get timestamp(): Date {
        return this._timestamp;
    }

    public static fromJSON(json: any): VitalSigns {
        return new VitalSigns(json.id, json.bpm, json.body_temperature, json.max_body_pressure, json.min_body_pressure, json.blood_oxygenation, json.tmstp);
    }
}