import { Component, Input, OnInit } from '@angular/core';
import { Inmate } from '../models/inmate';

@Component({
  selector: 'inmate-summary',
  templateUrl: './inmate-summary.component.html',
  styleUrls: ['./inmate-summary.component.scss']
})
export class InmateSummaryComponent implements OnInit {
  @Input()
  public inmate!: Inmate;

  constructor() { }

  ngOnInit(): void {
  }

}
