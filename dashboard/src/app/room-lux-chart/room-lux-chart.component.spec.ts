import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RoomLuxChartComponent } from './room-lux-chart.component';

describe('RoomLuxChartComponent', () => {
  let component: RoomLuxChartComponent;
  let fixture: ComponentFixture<RoomLuxChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RoomLuxChartComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RoomLuxChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
