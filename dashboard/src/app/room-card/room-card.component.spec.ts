import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RoomCardComponent } from './room-card.component';

describe('RoomComponent', () => {
  let component: RoomCardComponent;
  let fixture: ComponentFixture<RoomCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RoomCardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RoomCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
