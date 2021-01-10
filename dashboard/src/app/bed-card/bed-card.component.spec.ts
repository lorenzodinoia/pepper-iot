import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BedCardComponent } from './bed-card.component';

describe('BedCardComponent', () => {
  let component: BedCardComponent;
  let fixture: ComponentFixture<BedCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BedCardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BedCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
