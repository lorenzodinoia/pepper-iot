import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable({
    providedIn: 'root'
})
export class Client {
    public static readonly SERVER_URL: string = "http://localhost:5000"
    public static readonly OPTIONS = {
        headers: new HttpHeaders({
            'Content-Type':  'application/json',
            'Accept': 'application/json',
        })
    };

    constructor(private _httpClient: HttpClient) { }

    public get httpClient(): HttpClient {
        return this._httpClient;
    }
}