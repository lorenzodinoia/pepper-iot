import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RoomNavItemComponent } from './room-nav-item.component';

describe('RoomNavItemComponent', () => {
  let component: RoomNavItemComponent;
  let fixture: ComponentFixture<RoomNavItemComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RoomNavItemComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RoomNavItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
