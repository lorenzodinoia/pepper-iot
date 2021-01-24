import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InmateTemperatureChartComponent } from './inmate-temperature-chart.component';

describe('InmateTemperatureChartComponent', () => {
  let component: InmateTemperatureChartComponent;
  let fixture: ComponentFixture<InmateTemperatureChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InmateTemperatureChartComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InmateTemperatureChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
