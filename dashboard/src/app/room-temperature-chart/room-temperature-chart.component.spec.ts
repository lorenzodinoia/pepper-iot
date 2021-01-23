import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RoomTemperatureChartComponent } from './room-temperature-chart.component';

describe('RoomTemperatureChartComponent', () => {
  let component: RoomTemperatureChartComponent;
  let fixture: ComponentFixture<RoomTemperatureChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RoomTemperatureChartComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RoomTemperatureChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
