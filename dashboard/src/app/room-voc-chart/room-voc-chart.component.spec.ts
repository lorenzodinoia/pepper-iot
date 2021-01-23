import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RoomVocChartComponent } from './room-voc-chart.component';

describe('RoomVocChartComponent', () => {
  let component: RoomVocChartComponent;
  let fixture: ComponentFixture<RoomVocChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RoomVocChartComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RoomVocChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
