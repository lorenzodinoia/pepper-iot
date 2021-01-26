import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, ParamMap } from '@angular/router';
import { Client } from '../client';
import { Inmate } from '../models/inmate';

@Component({
  selector: 'inmate',
  templateUrl: './inmate.component.html',
  styleUrls: ['./inmate.component.scss']
})
export class InmateComponent implements OnInit {
  public inmate!: Inmate;

  constructor(private _client: Client, private _activatedRoute: ActivatedRoute) { }

  ngOnInit(): void {
    let urlParams: ParamMap = this._activatedRoute.snapshot.paramMap;
    if (urlParams.has("id")) {
      let id: number = parseInt(urlParams.get("id") || "0");
      if (id != 0) {
        Inmate.getDetails(this._client, id).subscribe((inmate) => {
          this.inmate = inmate;
        })
      }
    }
  }

}
