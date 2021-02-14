import { Component, QueryList, ViewChildren } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { interval, Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { Room } from '../models/room';
import { Client } from '../client';
import { RoomNavItemComponent } from '../room-nav-item/room-nav-item.component';
import { BedNavItemComponent } from '../bed-nav-item/bed-nav-item.component';

@Component({
  selector: 'navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent {
  private _rooms: Array<Room> = [];
  private roomComponentsArray!: Array<RoomNavItemComponent>;
  private bedComponentsArray!: Array<BedNavItemComponent>;

  @ViewChildren("roomItem")
  public roomComponents!: QueryList<RoomNavItemComponent>;
  @ViewChildren("bedItem")
  public bedComponents!: QueryList<BedNavItemComponent>;

  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );

  public get rooms(): Array<Room> {
    return this._rooms;
  }

  public set rooms(value: Array<Room>) {
    this._rooms = value;
  }
  
  constructor(private breakpointObserver: BreakpointObserver, private _client: Client) {}

  ngOnInit(): void {
    Room.getAll(this._client).subscribe((successResponse) => {
      if (successResponse instanceof Array) {
        this.rooms = successResponse;
      }
    });    
  }

  ngAfterViewInit() {
    this.roomComponents.changes.subscribe((rooms: QueryList<RoomNavItemComponent>) => {
      this.roomComponentsArray = rooms.toArray();
      this.bedComponents.changes.subscribe((beds: QueryList<BedNavItemComponent>) => {
        this.bedComponentsArray = beds.toArray();
        if ((this.bedComponentsArray.length > 0) && (this.roomComponentsArray.length > 0)) {
          this.updateEmergencies();
          interval(60000).subscribe(() => this.updateEmergencies());
        }
      })
    });
  }

  private updateEmergencies(): void {
    this._client.httpClient.get(`${Client.SERVER_URL}/emergency/`, Client.OPTIONS).pipe(map((response: any) => {
      return response;
    })).subscribe((response) => {
        let markedRooms: Array<number> = [];
        let markedBeds: Array<number> = [];

        for (let index in response) {
          let emergency: any = response[index];
          if ("room" in emergency) {
            let room: Room = Room.fromJSON(emergency.room);
            let foundedRoomComponent: RoomNavItemComponent | undefined = this.roomComponentsArray.find((element) => element.getRoom().id == room.id);
            if ((foundedRoomComponent) && (!markedRooms.includes(foundedRoomComponent.getRoom().id))) {
              foundedRoomComponent.setEmergency();
              markedRooms.push(room.id);
            }
          }
          else if ("bed_id" in emergency) {
            let bedId: number = emergency.bed_id;
            let foundedBedComponent: BedNavItemComponent | undefined = this.bedComponentsArray.find((element) => element.getBed().id == bedId);
            if ((foundedBedComponent) && (!markedBeds.includes(foundedBedComponent.getBed().id))) {
              foundedBedComponent.setEmergency();
              markedBeds.push(bedId);
            }
          }
        }

        this.resetEmergencies(markedRooms, markedBeds);
    });
  }

  private resetEmergencies(markedRooms: Array<number>, markedBeds: Array<number>): void {
    let roomsWithNoEmergency: Array<RoomNavItemComponent> = this.roomComponentsArray.filter((element) => !markedRooms.includes(element.getRoom().id));
    for (let roomComponent of roomsWithNoEmergency) {
      roomComponent.removeEmergency();
    }

    let bedsWithNoEmergency: Array<BedNavItemComponent> = this.bedComponentsArray.filter((element) => !markedBeds.includes(element.getBed().id))
    for (let bedComponent of bedsWithNoEmergency) {
      bedComponent.removeEmergency();
    }
  }
}