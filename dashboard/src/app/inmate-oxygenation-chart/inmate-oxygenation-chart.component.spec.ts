import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InmateOxygenationChartComponent } from './inmate-oxygenation-chart.component';

describe('InmateOxygenationChartComponent', () => {
  let component: InmateOxygenationChartComponent;
  let fixture: ComponentFixture<InmateOxygenationChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InmateOxygenationChartComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InmateOxygenationChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
