import { Component, Input, OnInit } from '@angular/core';
import { map } from 'rxjs/operators';
import { Client } from '../client';

@Component({
  selector: 'inmate-oxygenation-chart',
  templateUrl: './inmate-oxygenation-chart.component.html',
  styleUrls: ['./inmate-oxygenation-chart.component.scss']
})
export class InmateOxygenationChartComponent implements OnInit {
  @Input()
  public id!: number;
  public chartOptions: any;

  constructor(private _client: Client) { }

  ngOnInit(): void {
    this._client.httpClient.get(`${Client.SERVER_URL}/vital_signs/series/?inmate_id=${this.id}&field=blood_oxygenation`, Client.OPTIONS).pipe(map((response: any) => {
      return response;
    })).subscribe((response) => {
      let hours: Array<string> = [];
      let values: Array<number> = [];
      let valuesJson: any = response["values"];
      for(let index in valuesJson) {
        let item: any = valuesJson[index];
        hours.push(item["hour"]);
        values.push(item["value"]);
      }
      this.setData(hours, values);
    });
  }

  private setData(hours: Array<string>, values: Array<number>): void {
    this.chartOptions = {
      tooltip: {
        show: true
      },
      dataZoom: [
      {
          id: 'dataZoomX',
          type: 'slider',
          xAxisIndex: [0],
          filterMode: 'filter'
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
          name: 'Ossigenazione',
          type: 'line',
          data: values,
          itemStyle: {color: "blue"},
          lineStyle: {color: "blue"}
        }
      ]
    };
  }
}
