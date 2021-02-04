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

  constructor() { }

  ngOnInit(): void {
  }

}
