import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InmateBpmChartComponent } from './inmate-bpm-chart.component';

describe('InmateBpmChartComponent', () => {
  let component: InmateBpmChartComponent;
  let fixture: ComponentFixture<InmateBpmChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InmateBpmChartComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InmateBpmChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
