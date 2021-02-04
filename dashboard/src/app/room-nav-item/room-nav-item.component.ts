import { Component, Input, OnInit } from '@angular/core';
import { Room } from '../models/room';

@Component({
  selector: 'room-nav-item',
  templateUrl: './room-nav-item.component.html',
  styleUrls: ['./room-nav-item.component.scss']
})
export class RoomNavItemComponent implements OnInit {
  @Input()
  public room!: Room;

  constructor() { }

  ngOnInit(): void { }
}
