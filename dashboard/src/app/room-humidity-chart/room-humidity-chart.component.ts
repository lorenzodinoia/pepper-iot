import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'room-humidity-chart',
  templateUrl: './room-humidity-chart.component.html',
  styleUrls: ['./room-humidity-chart.component.scss']
})
export class RoomHumidityChartComponent implements OnInit {
  public chartOptions: any;
  public latest!: number;

  constructor() { }

  ngOnInit(): void {
    let hours: Array<string> = ["20:00", "20:10", "20:20", "20:30", "20:40", "20:50", "21:00", "21:10", "21:20", "21:30", "21:40", "21:50", "22:00", "22:10"]
    let humidities: Array<number> = [37, 36, 36, 36, 36, 35, 35, 35, 36, 36, 37, 37, 38, 38]
    this.latest = humidities[humidities.length - 1];

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
          name: 'Umidità',
          type: 'line',
          data: humidities,
          itemStyle: {color: "blue"},
          lineStyle: {color: "blue"}
        }
      ]
    };
  }

}
