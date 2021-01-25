import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'room-temperature-chart',
  templateUrl: './room-temperature-chart.component.html',
  styleUrls: ['./room-temperature-chart.component.scss']
})
export class RoomTemperatureChartComponent implements OnInit {
  public chartOptions: any;

  constructor() { }

  ngOnInit(): void {
    let hours: Array<string> = ["20:00", "20:10", "20:20", "20:30", "20:40", "20:50", "21:00", "21:10", "21:20", "21:30", "21:40", "21:50", "22:00", "22:10"]
    let temperatures: Array<number> = [19.2, 19.5, 19.5, 19.5, 20, 20.1, 20, 20.2, 20.5, 20, 19.8, 19.5, 19.1, 18.8]

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
          name: 'Temperatura',
          type: 'line',
          data: temperatures,
          itemStyle: {color: "green"},
          lineStyle: {color: "green"}
        }
      ]
    };
  }

}
