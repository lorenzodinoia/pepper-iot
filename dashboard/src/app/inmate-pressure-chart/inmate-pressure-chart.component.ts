import { Component, Input, OnInit } from '@angular/core';
import { map } from 'rxjs/operators';
import { Client } from '../client';

@Component({
  selector: 'inmate-pressure-chart',
  templateUrl: './inmate-pressure-chart.component.html',
  styleUrls: ['./inmate-pressure-chart.component.scss']
})
export class InmatePressureChartComponent implements OnInit {
  @Input()
  public id!: number;
  public chartOptions: any;
  public latest!: string;

  constructor(private _client: Client) { }

  ngOnInit(): void {
    this.getLatest24Hours();
  }

  private getLatest24Hours(): void {
    this._client.httpClient.get(`${Client.SERVER_URL}/vital_signs/series/?inmate_id=${this.id}&field=pressure`, Client.OPTIONS).pipe(map((response: any) => {
      return response;
    })).subscribe((response) => {
      let hours: Array<string> = [];
      let minValues: Array<number> = [];
      let maxValues: Array<number> = [];
      let valuesJson: any = response["values"];

      for (let index in valuesJson) {
        let item: any = valuesJson[index];
        hours.push(item["hour"]);
        minValues.push(item["value_min"]);
        maxValues.push(item["value_max"]);
      }

      if (minValues.length != 0) {
        this.setData(hours, minValues, maxValues, true);
      }
    });
  }

  private setData(hours: Array<string>, minValues: Array<number>, maxValues: Array<number>, changeLatest: boolean = false): void {
    let length: number = minValues.length
    if (changeLatest) {
      let minLatest: number = minValues[minValues.length - 1];
      let maxLatest: number = maxValues[maxValues.length - 1];
      this.latest = `${minLatest}/${maxLatest}`;
    }

    let sliderStart: number = ((length <= 40) ? 0 : ((100 * (length - 40) / length))); //Show always 40 points
    
    this.chartOptions = {
      tooltip: {
        show: true
      },
      dataZoom: [
      {
          id: 'dataZoomX',
          type: 'slider',
          xAxisIndex: [0, 1],
          filterMode: 'filter',
          start: sliderStart
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
          name: 'Pressione minima',
          type: 'line',
          data: minValues,
          itemStyle: {color: "brown"},
          lineStyle: {color: "brown"}
        },
        {
          name: 'Pressione massima',
          type: 'line',
          data: maxValues,
          itemStyle: {color: "brown"},
          lineStyle: {color: "brown"}
        }
      ]
    };
  }

  public getfromInterval(start: Date, end: Date): void {
    let startAsString: string = start.toISOString();
    let endAsString: string = end.toISOString();
    
    this._client.httpClient.get(`${Client.SERVER_URL}/vital_signs/series/?inmate_id=${this.id}&field=pressure&start=${startAsString}&end=${endAsString}`, Client.OPTIONS).pipe(map((response: any) => {
      return response;
    })).subscribe((response) => {
      let hours: Array<string> = [];
      let minValues: Array<number> = [];
      let maxValues: Array<number> = [];
      let valuesJson: any = response["values"];

      for (let index in valuesJson) {
        let item: any = valuesJson[index];
        hours.push(item["hour"]);
        minValues.push(item["value_min"]);
        maxValues.push(item["value_max"]);
      }

      if (minValues.length != 0) {
        this.setData(hours, minValues, maxValues);
      }
    });   
  }

  public reset(): void {
    this.getLatest24Hours();
  }
}
