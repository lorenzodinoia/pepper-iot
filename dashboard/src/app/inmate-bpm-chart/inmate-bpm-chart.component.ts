import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'inmate-bpm-chart',
  templateUrl: './inmate-bpm-chart.component.html',
  styleUrls: ['./inmate-bpm-chart.component.scss']
})
export class InmateBpmChartComponent implements OnInit {
  public chartOptions: any;

  constructor() { }

  ngOnInit(): void {
    let hours: Array<string> = ["20:00", "20:10", "20:20", "20:30", "20:40", "20:50", "21:00", "21:10", "21:20", "21:30", "21:40", "21:50", "22:00", "22:10"]
    let bpms: Array<number> = [78, 79, 78, 78, 80, 81, 78, 81, 82, 78, 85, 87, 87, 81]

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
          data: bpms,
          itemStyle: {color: "red"},
          lineStyle: {color: "red"}
        }
      ]
    };
  }

}
