import { Component } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { Room } from '../models/room';
import { Client } from '../client';

@Component({
  selector: 'navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent {
  private _rooms: Array<Room> = [];

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
}
