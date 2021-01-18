import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InmateSummaryComponent } from './inmate-summary.component';

describe('InmateSummaryComponent', () => {
  let component: InmateSummaryComponent;
  let fixture: ComponentFixture<InmateSummaryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InmateSummaryComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InmateSummaryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
