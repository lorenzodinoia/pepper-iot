import { Model } from "./model";

export class VitalSigns extends Model {
    private _bpm: number;
    private _bodyTemperature: number;
    private _bloodPressure: number;
    private _bloodOxygenation: number;
    private _timestamp: Date;

    constructor(id: number, bpm: number, bodyTemperature: number, bloodPressure: number, bloodOxygenation: number, timestamp: Date) {
        super(id);
        this._bpm = bpm;
        this._bodyTemperature = bodyTemperature;
        this._bloodPressure = bloodPressure;
        this._bloodOxygenation = bloodOxygenation;
        this._timestamp = timestamp;
    }

    public get bpm(): number {
        return this._bpm;
    }

    public get bodyTemperature(): number {
        return this._bodyTemperature;
    }

    public get bloodPressure(): number {
        return this._bloodPressure;
    }

    public get bloodOxygenation(): number {
        return this._bloodOxygenation;
    }

    public get timestamp(): Date {
        return this._timestamp;
    }

    public static fromJSON(json: any): VitalSigns {
        return new VitalSigns(json.id, json.bpm, json.body_temperature, json.body_pressure, json.blood_oxygenation, json.tmstp);
    }
}