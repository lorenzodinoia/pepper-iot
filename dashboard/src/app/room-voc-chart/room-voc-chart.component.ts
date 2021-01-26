import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'room-voc-chart',
  templateUrl: './room-voc-chart.component.html',
  styleUrls: ['./room-voc-chart.component.scss']
})
export class RoomVocChartComponent implements OnInit {
  public chartOptions: any;

  constructor() { }

  ngOnInit(): void {
    let hours: Array<string> = ["20:00", "20:10", "20:20", "20:30", "20:40", "20:50", "21:00", "21:10", "21:20", "21:30", "21:40", "21:50", "22:00", "22:10"]
    let voc: Array<number> = [0.5, 0.6, 0.5, 0.7, 1, 0.8, 0.8, 0.5, 0.5, 0.6, 0.7, 0.6, 0.7, 0.7]

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
          data: voc,
          itemStyle: {color: "purple"},
          lineStyle: {color: "purple"}
        }
      ]
    };
  }

}
