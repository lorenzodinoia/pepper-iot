import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InmatePressureChartComponent } from './inmate-pressure-chart.component';

describe('InmatePressureChartComponent', () => {
  let component: InmatePressureChartComponent;
  let fixture: ComponentFixture<InmatePressureChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InmatePressureChartComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InmatePressureChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
