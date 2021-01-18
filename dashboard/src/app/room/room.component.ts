import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, ParamMap } from '@angular/router';
import { Client } from '../client';
import { Room } from '../models/room';

@Component({
  selector: 'room',
  templateUrl: './room.component.html',
  styleUrls: ['./room.component.scss']
})
export class RoomComponent implements OnInit {
  public room!: Room;

  constructor(private _client: Client, private _activatedRoute: ActivatedRoute) { }

  ngOnInit(): void {
    let urlParams: ParamMap = this._activatedRoute.snapshot.paramMap;
    if (urlParams.has("id")) {
      let id: number = parseInt(urlParams.get("id") || "0");
      if (id != 0) {
        Room.getDetails(this._client, id).subscribe((room) => {
          this.room = room;
        })
      }
    }
  }

}
