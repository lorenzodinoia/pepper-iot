import { Inmate } from "./inmate";
import { Model } from "./model";

export class Bed extends Model {
    private _inmate: Inmate;

    constructor(id: number, inmate: Inmate) {
        super(id)
        this._inmate = inmate;
    }

    public get inmate(): Inmate {
        return this._inmate;
    }

    public static fromJSON(json: any): Bed {
        return new Bed(json.id, Inmate.fromJSON(json.inmate));
    }
} 