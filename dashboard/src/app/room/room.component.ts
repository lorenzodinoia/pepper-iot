import { DatePipe } from '@angular/common';
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, ParamMap } from '@angular/router';
import { Client } from '../client';
import { Room } from '../models/room';
import { RoomHumidityChartComponent } from '../room-humidity-chart/room-humidity-chart.component';
import { RoomLuxChartComponent } from '../room-lux-chart/room-lux-chart.component';
import { RoomTemperatureChartComponent } from '../room-temperature-chart/room-temperature-chart.component';
import { RoomVocChartComponent } from '../room-voc-chart/room-voc-chart.component';

@Component({
  selector: 'room',
  templateUrl: './room.component.html',
  styleUrls: ['./room.component.scss']
})
export class RoomComponent implements OnInit {
  public room!: Room;
  public lastUpdateAsString!: string;

  @ViewChild("startDate")
  public startDateInput!: ElementRef;
  @ViewChild("endDate")
  public endDateInput!: ElementRef;
  
  public canResetFilter: boolean = false;
  public todayAsString: string = this._datePipe.transform(new Date(), "YYYY-MM-ddTHH:mm") || "";

  @ViewChild("temperatureChart")
  public temperatureChart!: RoomTemperatureChartComponent;
  @ViewChild("humidityChart")
  public humidityChart!: RoomHumidityChartComponent;
  @ViewChild("luxChart")
  public luxChart!: RoomLuxChartComponent;
  @ViewChild("vocChart")
  public vocChart!: RoomVocChartComponent;

  constructor(private _client: Client, private _activatedRoute: ActivatedRoute, private _datePipe: DatePipe) { }

  ngOnInit(): void {
    let urlParams: ParamMap = this._activatedRoute.snapshot.paramMap;
    if (urlParams.has("id")) {
      let id: number = parseInt(urlParams.get("id") || "0");
      if (id != 0) {
        Room.getDetails(this._client, id).subscribe((room) => {
          this.room = room;
          if (room.environmentalData.timestamp != undefined) {
            this.lastUpdateAsString = this._datePipe.transform(room.environmentalData.timestamp, "dd/MM/yyyy HH:mm") || "N/D";
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
        this.humidityChart.getfromInterval(startDate, endDate);
        this.luxChart.getfromInterval(startDate, endDate);
        this.vocChart.getfromInterval(startDate, endDate);
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
    this.humidityChart.reset();
    this.luxChart.reset();
    this.vocChart.reset();
  }
}
