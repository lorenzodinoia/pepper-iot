import { Client } from "../client";
import { Bed } from "./bed";
import { Model } from "./model";
import { map } from 'rxjs/operators';
import { Observable } from "rxjs";

export class Room extends Model {
    private _name: string;
    private _beds: Array<Bed>

    constructor(id: number, name: string, beds: Array<Bed>) {
        super(id);
        this._name = name;
        this._beds = beds;
    }

    public get name(): string {
        return this._name;
    }

    public get beds(): Array<Bed> {
        return this._beds;
    }

    public static fromJSON(json: any): Room {
        let beds: Array<Bed> = []
        if ("beds" in json) {
            for (let bed of json.beds) {
                beds.push(Bed.fromJSON(bed));
            }
        }
        return new Room(json.id, json.name, beds);
    }

    public static getAll(client: Client): Observable<Array<Room>> {
        return client.httpClient.get(`${Client.SERVER_URL}/room/all`, Client.OPTIONS).pipe(map((response: any) => {
            let rooms: Array<Room> = []
            for (let index in response) {
                rooms.push(Room.fromJSON(response[index])) 
            }
            return rooms;
          }));
    }
}