import { Model } from "./model";

export class EnvironmentalData extends Model {
    private _temperature: number;
    private _humidity: number;
    private _lux: number;
    private _voc: number;
    private _timestamp: Date;

    constructor(id: number, temperature: number, humidity: number, lux: number, voc: number, timestamp: Date) {
        super(id);
        this._temperature = temperature;
        this._humidity = humidity;
        this._lux = lux;
        this._voc = voc;
        this._timestamp = timestamp;
    }

    public get temperature(): number {
        return this._temperature;
    }

    public get humidity(): number {
        return this._humidity;
    }

    public get lux(): number {
        return this._lux;
    }

    public get voc(): number {
        return this._voc;
    }

    public get timestamp(): Date {
        return this._timestamp;
    }

    public static fromJSON(json: any): EnvironmentalData {
        return new EnvironmentalData(json.id, json.degree, json.humidity, json.lux, json.voc, json.tmstp);
    }
}