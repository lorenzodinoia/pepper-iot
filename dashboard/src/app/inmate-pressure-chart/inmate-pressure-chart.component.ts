import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'inmate-pressure-chart',
  templateUrl: './inmate-pressure-chart.component.html',
  styleUrls: ['./inmate-pressure-chart.component.scss']
})
export class InmatePressureChartComponent implements OnInit {
  public chartOptions: any;

  constructor() { }

  ngOnInit(): void {
    let hours: Array<string> = ["20:00", "20:10", "20:20", "20:30", "20:40", "20:50", "21:00", "21:10", "21:20", "21:30", "21:40", "21:50", "22:00", "22:10"]
    let minimum: Array<number> = [80, 82, 80, 85, 91, 92, 85, 86, 81, 78, 81, 80, 82, 80]
    let maximum: Array<number> = [110, 112, 115, 117, 109, 120, 118, 118, 120, 115, 121, 117, 118, 115]

    this.chartOptions = {
      tooltip: {
        show: true
      },
      legend: {
        show: true,
        data: ['Minima', 'Massima'],
        align: 'top'
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
          name: 'Minima',
          type: 'line',
          data: minimum,
          itemStyle: {color: "orange"},
          lineStyle: {color: "orange"}
        },
        {
          name: 'Massima',
          type: 'line',
          data: maximum,
          itemStyle: {color: "brown"},
          lineStyle: {color: "brown"}
        }
      ]
    };
  }

}
