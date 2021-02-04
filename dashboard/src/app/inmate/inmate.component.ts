import { DatePipe } from '@angular/common';
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, ParamMap } from '@angular/router';
import { Client } from '../client';
import { InmateBpmChartComponent } from '../inmate-bpm-chart/inmate-bpm-chart.component';
import { InmateOxygenationChartComponent } from '../inmate-oxygenation-chart/inmate-oxygenation-chart.component';
import { InmatePressureChartComponent } from '../inmate-pressure-chart/inmate-pressure-chart.component';
import { InmateTemperatureChartComponent } from '../inmate-temperature-chart/inmate-temperature-chart.component';
import { Inmate } from '../models/inmate';

@Component({
  selector: 'inmate',
  templateUrl: './inmate.component.html',
  styleUrls: ['./inmate.component.scss']
})
export class InmateComponent implements OnInit {
  public inmate!: Inmate;
  public lastUpdateAsString!: string;

  @ViewChild("startDate")
  public startDateInput!: ElementRef;
  @ViewChild("endDate")
  public endDateInput!: ElementRef;
  
  public canResetFilter: boolean = false;
  public todayAsString: string = this._datePipe.transform(new Date(), "YYYY-MM-ddTHH:mm") || "";

  @ViewChild("temperatureChart")
  public temperatureChart!: InmateTemperatureChartComponent;
  @ViewChild("bpmChart")
  public bpmChart!: InmateBpmChartComponent;
  @ViewChild("oxygenationChart")
  public oxygenationChart!: InmateOxygenationChartComponent;
  @ViewChild("pressureChart")
  public pressureChart!: InmatePressureChartComponent;

  constructor(private _client: Client, private _activatedRoute: ActivatedRoute, private _datePipe: DatePipe) { }

  ngOnInit(): void {
    let urlParams: ParamMap = this._activatedRoute.snapshot.paramMap;
    if (urlParams.has("id")) {
      let id: number = parseInt(urlParams.get("id") || "0");
      if (id != 0) {
        Inmate.getDetails(this._client, id).subscribe((inmate) => {
          this.inmate = inmate;
          if (this.inmate.vitalSigns.timestamp != undefined) {
            this.lastUpdateAsString = this._datePipe.transform(this.inmate.vitalSigns.timestamp, "dd/MM/yyyy HH:mm") || "N/D";
          }
        })
      }
    }
  }

  public applyFilter(): void {
    let startDateAsString: string = this.startDateInput.nativeElement.value;
    let endDateAsString: string = this.endDateInput.nativeElement.value;

    if (startDateAsString) {
      if (endDateAsString) {
        let startDate: Date = new Date(startDateAsString);
        let endDate: Date = new Date(endDateAsString);

        this.canResetFilter = true;
        this.temperatureChart.getfromInterval(startDate, endDate);
        this.bpmChart.getfromInterval(startDate, endDate);
        this.oxygenationChart.getfromInterval(startDate, endDate);
        this.pressureChart.getfromInterval(startDate, endDate);
      }
      else {
        alert("Seleziona una data di fine");
      }
    }
    else {
      alert("Seleziona una data di partenza");
    }
  }

  public resetFilter(): void {
    this.startDateInput.nativeElement.value = null;
    this.endDateInput.nativeElement.value = null;
    this.canResetFilter = false;

    this.temperatureChart.reset();
    this.bpmChart.reset();
    this.oxygenationChart.reset();
    this.pressureChart.reset();
  }
}
