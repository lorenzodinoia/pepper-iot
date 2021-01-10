import { Component, Input, OnInit } from '@angular/core';
import { Room } from '../models/room';

@Component({
  selector: 'room-card',
  templateUrl: './room-card.component.html',
  styleUrls: ['./room-card.component.scss']
})
export class RoomCardComponent implements OnInit {
  @Input()
  public room!: Room;

  constructor() { }

  ngOnInit(): void {

  }

}
