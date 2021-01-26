import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'room-lux-chart',
  templateUrl: './room-lux-chart.component.html',
  styleUrls: ['./room-lux-chart.component.scss']
})
export class RoomLuxChartComponent implements OnInit {
  public chartOptions: any;

  constructor() { }

  ngOnInit(): void {
    let hours: Array<string> = ["20:00", "20:10", "20:20", "20:30", "20:40", "20:50", "21:00", "21:10", "21:20", "21:30", "21:40", "21:50", "22:00", "22:10"]
    let lux: Array<number> = [210, 210, 205, 200, 205, 150, 160, 250, 230, 230, 230, 245, 250, 240]

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
          data: lux,
          itemStyle: {color: "orange"},
          lineStyle: {color: "orange"}
        }
      ]
    };
  }

}
