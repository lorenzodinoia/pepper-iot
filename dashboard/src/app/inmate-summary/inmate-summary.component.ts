import { Component, Input, OnInit } from '@angular/core';
import { Client } from '../client';
import { Inmate } from '../models/inmate';

@Component({
  selector: 'inmate-summary',
  templateUrl: './inmate-summary.component.html',
  styleUrls: ['./inmate-summary.component.scss']
})
export class InmateSummaryComponent implements OnInit {
  @Input()
  public inmate!: Inmate;

  constructor(private _client: Client) { }

  ngOnInit(): void {
  }

  public sendPepper(): void {
    this.inmate.sendPepper(this._client).subscribe((response) => {
      if (response) {
        alert("Pepper inviato");
      }
    })
  }
}
