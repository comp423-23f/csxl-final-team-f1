import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EquipmentReservationComponent } from './equipment-reservation.component';

describe('EquipmentReservationComponent', () => {
  let component: EquipmentReservationComponent;
  let fixture: ComponentFixture<EquipmentReservationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EquipmentReservationComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EquipmentReservationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
