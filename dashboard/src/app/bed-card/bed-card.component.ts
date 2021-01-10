import { Component, Input, OnInit } from '@angular/core';
import { Bed } from '../models/bed';

@Component({
  selector: 'bed-card',
  templateUrl: './bed-card.component.html',
  styleUrls: ['./bed-card.component.scss']
})
export class BedCardComponent implements OnInit {
  @Input()
  public bed!: Bed;

  constructor() { }

  ngOnInit(): void {
  }

}
