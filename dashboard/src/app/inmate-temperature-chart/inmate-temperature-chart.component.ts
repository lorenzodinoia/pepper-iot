import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'inmate-temperature-chart',
  templateUrl: './inmate-temperature-chart.component.html',
  styleUrls: ['./inmate-temperature-chart.component.scss']
})
export class InmateTemperatureChartComponent implements OnInit {
  public chartOptions: any;

  constructor() { }

  ngOnInit(): void {
    let hours: Array<string> = ["20:00", "20:10", "20:20", "20:30", "20:40", "20:50", "21:00", "21:10", "21:20", "21:30", "21:40", "21:50", "22:00", "22:10"]
    let temperatures: Array<number> = [35.5, 35.5, 35.6, 35.4, 35.5, 35.6, 35.6, 35.6, 35.9, 36, 36.1, 36.3, 36, 35.9]

    this.chartOptions = {
      tooltip: {
        show: true
      },
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
