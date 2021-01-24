import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'inmate-oxygenation-chart',
  templateUrl: './inmate-oxygenation-chart.component.html',
  styleUrls: ['./inmate-oxygenation-chart.component.scss']
})
export class InmateOxygenationChartComponent implements OnInit {
  public chartOptions: any;

  constructor() { }

  ngOnInit(): void {
    let hours: Array<string> = ["20:00", "20:10", "20:20", "20:30", "20:40", "20:50", "21:00", "21:10", "21:20", "21:30", "21:40", "21:50", "22:00", "22:10"]
    let oxygenations: Array<number> = [99, 98, 98, 99, 97, 99, 98, 97, 98, 99, 99, 97, 100, 97]

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
          name: 'BPM',
          type: 'line',
          data: oxygenations,
          itemStyle: {color: "blue"},
          lineStyle: {color: "blue"}
        }
      ]
    };
  }

}
