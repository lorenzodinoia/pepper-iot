import { Client } from "../client";
import { Bed } from "./bed";
import { Model } from "./model";
import { map } from 'rxjs/operators';
import { Observable } from "rxjs";
import { EnvironmentalData } from "./environmentalData";

export class Room extends Model {
    private _name: string;
    private _beds: Array<Bed>
    private _environmentalData!: EnvironmentalData;

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

    public get environmentalData(): EnvironmentalData {
        return this._environmentalData;
    }

    public set environmentalData(value: EnvironmentalData) {
        this._environmentalData = value;
    }

    public static fromJSON(json: any): Room {
        let beds: Array<Bed> = []
        if ("beds" in json) {
            for (let bed of json.beds) {
                beds.push(Bed.fromJSON(bed));
            }
        }
        let room: Room = new Room(json.id, json.name, beds);
        if ("env_data" in json) {
            room.environmentalData = EnvironmentalData.fromJSON(json.env_data);
        }
        return room;
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

    public static getDetails(client: Client, id: number): Observable<Room> {
        return client.httpClient.get(`${Client.SERVER_URL}/room/?id=${id}`, Client.OPTIONS).pipe(map((response: any) => {
            return Room.fromJSON(response);
          }));
    }
}