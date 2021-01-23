import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RoomHumidityChartComponent } from './room-humidity-chart.component';

describe('RoomHumidityChartComponent', () => {
  let component: RoomHumidityChartComponent;
  let fixture: ComponentFixture<RoomHumidityChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RoomHumidityChartComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RoomHumidityChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
