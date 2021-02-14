import { Component, Input, OnInit } from '@angular/core';
import { Bed } from '../models/bed';

@Component({
  selector: 'bed-nav-item',
  templateUrl: './bed-nav-item.component.html',
  styleUrls: ['./bed-nav-item.component.scss']
})
export class BedNavItemComponent implements OnInit {
  @Input()
  public bed!: Bed;
  public emergency: boolean = false;

  constructor() { }

  ngOnInit(): void {
  }

  public getBed(): Bed {
    return this.bed;
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

}
