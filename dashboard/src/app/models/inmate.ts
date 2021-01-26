import { Observable } from "rxjs";
import { map } from "rxjs/operators";
import { Client } from "../client";
import { Model } from "./model";
import { VitalSigns } from "./vitalSigns";

export class Inmate extends Model {
    private _name: string;
    private _surname: string;
    private _cf: string;
    private _birthDate: Date;
    private _vitalSigns!: VitalSigns;

    constructor(id: number, name: string, surname: string, cf: string, birthDate: Date) {
        super(id);
        this._name = name;
        this._surname = surname;
        this._cf = cf;
        this._birthDate = birthDate;
    }

    public get name(): string {
        return this._name;
    }

    public get surname(): string {
        return this._surname;
    }

    public get cf(): string {
        return this._cf;
    }

    public get birthDate(): Date {
        return this._birthDate;
    }

    public get vitalSigns(): VitalSigns {
        return this._vitalSigns;
    }

    public set vitalSigns(vitalSigns: VitalSigns) {
        this._vitalSigns = vitalSigns;
    }

    public static fromJSON(json: any): Inmate {
        let birthDate: Date = new Date();
        if ("birthdate" in json) {
            birthDate = new Date(json.birthDate);
        }
        let cf: string = "";
        if ("cf" in json) {
            cf = json.cf;
        }
        let inmate = new Inmate(json.id, json.name, json.surname, cf, birthDate);
        if ("vital_signs" in json) {
            inmate.vitalSigns = VitalSigns.fromJSON(json.vital_signs);
        }
        return inmate;
    }

    public static getDetails(client: Client, id: number): Observable<Inmate> {
        return client.httpClient.get(`${Client.SERVER_URL}/inmate/?id=${id}`, Client.OPTIONS).pipe(map((response: any) => {
            return Inmate.fromJSON(response);
          }));
    }
}