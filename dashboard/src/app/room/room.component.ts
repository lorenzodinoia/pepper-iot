import { DatePipe } from '@angular/common';
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
  public lastUpdateAsString!: string;

  constructor(private _client: Client, private _activatedRoute: ActivatedRoute, private _datePipe: DatePipe) { }

  ngOnInit(): void {
    let urlParams: ParamMap = this._activatedRoute.snapshot.paramMap;
    if (urlParams.has("id")) {
      let id: number = parseInt(urlParams.get("id") || "0");
      if (id != 0) {
        Room.getDetails(this._client, id).subscribe((room) => {
          this.room = room;
          if (room.environmentalData.timestamp != undefined) {
            this.lastUpdateAsString = this._datePipe.transform(room.environmentalData.timestamp, "dd/MM/yyyy HH:mm") || "N/D";
          }
        })
      }
    }
  }
}
