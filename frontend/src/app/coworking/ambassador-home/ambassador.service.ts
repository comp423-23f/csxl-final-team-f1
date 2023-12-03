/* eslint-disable prettier/prettier */
import { Injectable } from '@angular/core';
import { RxEquipmentReservations, RxReservations } from './rx-reservations';
import { Observable, map } from 'rxjs';
import {
  Reservation,
  ReservationJSON,
  parseReservationJSON
} from '../coworking.models';
import {
  Reservation as EquipmentReservation,
  ReservationJSON as EquipmentReservationJSON,
  parseReservationJSON as parseEquipmentReservationJSON
} from '../../equipment/equipment.models';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class AmbassadorService {
  private reservations: RxReservations = new RxReservations();
  private equipmentReservations: RxEquipmentReservations =
    new RxEquipmentReservations();
  public reservations$: Observable<Reservation[]> = this.reservations.value$;
  public equipmentReservation$: Observable<EquipmentReservation[]> =
    this.equipmentReservations.value$;

  constructor(private http: HttpClient) {}

  fetchReservations(): void {
    this.http
      .get<ReservationJSON[]>('/api/coworking/ambassador')
      .subscribe((reservations) => {
        this.reservations.set(reservations.map(parseReservationJSON));
      });
  }

  fetchEquipmentReservations(): void {
    this.http
      .get<EquipmentReservationJSON[]>('/api/equipment/ambassador')
      .subscribe((equipmentReservations) => {
        this.equipmentReservations.set(
          equipmentReservations.map(parseEquipmentReservationJSON)
        );
      });
  }

  checkIn(reservation: Reservation): void {
    this.http
      .put<ReservationJSON>(`/api/coworking/ambassador/checkin`, {
        id: reservation.id,
        state: 'CHECKED_IN'
      })
      .subscribe((reservationJson) => {
        this.reservations.updateReservation(
          parseReservationJSON(reservationJson)
        );
      });
  }

  checkInEquipment(reservation: EquipmentReservation): void {
    this.http
      .put<EquipmentReservationJSON>(`/api/equipment/ambassador/checkin`, {
        id: reservation.id,
        state: 'CHECKED_IN'
      })
      .subscribe((equipmentreservationJson) => {
        this.equipmentReservations.updateReservation(
          parseEquipmentReservationJSON(equipmentreservationJson)
        );
      });
  }

  checkOut(reservation: Reservation) {
    this.http
      .put<ReservationJSON>(`/api/coworking/reservation/${reservation.id}`, {
        id: reservation.id,
        state: 'CHECKED_OUT'
      })
      .subscribe((reservationJson) => {
        this.reservations.updateReservation(
          parseReservationJSON(reservationJson)
        );
      });
  }

  checkOutEquipment(reservation: EquipmentReservation) {
    this.http
      .put<EquipmentReservationJSON>(
        `/api/equipment/reservation/${reservation.id}`,
        {
          id: reservation.id,
          state: 'CHECKED_OUT'
        }
      )
      .subscribe((reservationJson) => {
        this.equipmentReservations.updateReservation(
          parseEquipmentReservationJSON(reservationJson)
        );
      });
  }

  cancel(reservation: Reservation) {
    this.http
      .put<ReservationJSON>(`/api/coworking/reservation/${reservation.id}`, {
        id: reservation.id,
        state: 'CANCELLED'
      })
      .subscribe({
        next: (_) => {
          this.reservations.remove(reservation);
        },
        error: (err) => {
          alert(err);
        }
      });
  }

  cancelEquipment(reservation: EquipmentReservation) {
    this.http
      .put<ReservationJSON>(`/api/equipment/reservation/${reservation.id}`, {
        id: reservation.id,
        state: 'CANCELLED'
      })
      .subscribe({
        next: (_) => {
          this.equipmentReservations.remove(reservation);
        },
        error: (err) => {
          alert(err);
        }
      });
  }
}
