import { Component, Input, OnInit, QueryList } from '@angular/core';
import { elementAt, map } from 'rxjs/operators';
import { BedNavItemComponent } from '../bed-nav-item/bed-nav-item.component';
import { Room } from '../models/room';

@Component({
  selector: 'room-nav-item',
  templateUrl: './room-nav-item.component.html',
  styleUrls: ['./room-nav-item.component.scss']
})
export class RoomNavItemComponent implements OnInit {
  @Input()
  public room!: Room;
  public emergency: boolean = false;
  private bedComponentsArray!: Array<BedNavItemComponent>;

  @Input("bedItem")
  public bedComponents!: QueryList<BedNavItemComponent>;

  constructor() { }

  ngOnInit(): void { }

  ngAfterViewInit() {
    this.bedComponents.changes.subscribe((list: QueryList<BedNavItemComponent>) => {
      this.bedComponentsArray = list.toArray();
    });
  }

  public getRoom(): Room {
    return this.room;
  }

  public setEmergency(): void {
    this.emergency = true;
  }

  public removeEmergency(): void {
    this.emergency = false;
  }

  public hasEmergency(): boolean {
    return this.emergency;
  }

  public getBed(bedId: number): BedNavItemComponent | undefined {
    return this.bedComponentsArray.find((element) => element.getBed().id == bedId);
  }
}
