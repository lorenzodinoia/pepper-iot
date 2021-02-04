import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BedNavItemComponent } from './bed-nav-item.component';

describe('BedNavItemComponent', () => {
  let component: BedNavItemComponent;
  let fixture: ComponentFixture<BedNavItemComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BedNavItemComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BedNavItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
