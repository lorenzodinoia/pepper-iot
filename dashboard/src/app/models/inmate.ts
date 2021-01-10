import { Model } from "./model";

export class Inmate extends Model {
    private _name: string;
    private _surname: string;
    private _cf: string;
    private _birthDate: Date;

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

    public static fromJSON(json: any): Inmate {
        let birthDate: Date = new Date();
        if ("birthdate" in json) {
            birthDate = new Date(json.birthDate);
        }
        let cf: string = "";
        if ("cf" in json) {
            cf = json.cf;
        }
        return new Inmate(json.id, json.name, json.surname, cf, birthDate);
    }
}