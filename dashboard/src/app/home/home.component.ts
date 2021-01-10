import { Component, OnInit } from '@angular/core';
import { Client } from '../client';
import { Room } from '../models/room';

@Component({
  selector: 'home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  private _rooms: Array<Room> = [];

  constructor(private _client: Client) { }

  public get rooms(): Array<Room> {
    return this._rooms;
  }

  public set rooms(value: Array<Room>) {
    this._rooms = value;
  }

  ngOnInit(): void {
    Room.getAll(this._client).subscribe((successResponse) => {
      if (successResponse instanceof Array) {
        this.rooms = successResponse;
      }
    });
  }
  
}
