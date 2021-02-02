import { Component, Input, OnInit } from '@angular/core';
import { map } from 'rxjs/operators';
import { Client } from '../client';

@Component({
  selector: 'inmate-bpm-chart',
  templateUrl: './inmate-bpm-chart.component.html',
  styleUrls: ['./inmate-bpm-chart.component.scss']
})
export class InmateBpmChartComponent implements OnInit {
  @Input()
  public id!: number;
  public chartOptions: any;
  public latest!: number;

  constructor(private _client: Client) { }

  ngOnInit(): void {
    this.getLatest24Hours(); 
  }

  private getLatest24Hours(): void {
    this._client.httpClient.get(`${Client.SERVER_URL}/vital_signs/series/?inmate_id=${this.id}&field=bpm`, Client.OPTIONS).pipe(map((response: any) => {
      return response;
    })).subscribe((response) => {
      let hours: Array<string> = [];
      let values: Array<number> = [];
      let valuesJson: any = response["values"];

      for (let index in valuesJson) {
        let item: any = valuesJson[index];
        hours.push(item["hour"]);
        values.push(item["value"]);
      }

      if (values.length != 0) {
        this.setData(hours, values, true);
      }
    });   
  }

  private setData(hours: Array<string>, values: Array<number>, changeLatest: boolean = false): void {
    if (changeLatest) {
      this.latest = values[values.length - 1];
    }
    
    this.chartOptions = {
      tooltip: {
        show: true
      },
      dataZoom: [
      {
          id: 'dataZoomX',
          type: 'slider',
          xAxisIndex: [0],
          filterMode: 'filter',
          start: 80 //TODO Adattare al numero di valori con una formula
      },
      {
          id: 'dataZoomY',
          type: 'slider',
          yAxisIndex: [0],
          filterMode: 'empty'
      }],
      xAxis: {
        data: hours,
        silent: false,
        splitLine: {
          show: false,
        },
      },
      yAxis: {
        type: 'value',
        scale: true
      },
      series: [
        {
          name: 'Temperatura',
          type: 'line',
          data: values,
          itemStyle: {color: "orange"},
          lineStyle: {color: "orange"}
        }
      ]
    };
  }

  public getfromInterval(start: Date, end: Date): void {
    let startAsString: string = start.toISOString();
    let endAsString: string = end.toISOString();
    
    this._client.httpClient.get(`${Client.SERVER_URL}/vital_signs/series/?inmate_id=${this.id}&field=bpm&start=${startAsString}&end=${endAsString}`, Client.OPTIONS).pipe(map((response: any) => {
      return response;
    })).subscribe((response) => {
      let hours: Array<string> = [];
      let values: Array<number> = [];
      let valuesJson: any = response["values"];

      for (let index in valuesJson) {
        let item: any = valuesJson[index];
        hours.push(item["hour"]);
        values.push(item["value"]);
      }

      if (values.length != 0) {
        this.setData(hours, values, true);
      }
    });   
  }

  public reset(): void {
    this.getLatest24Hours();
  }
}
