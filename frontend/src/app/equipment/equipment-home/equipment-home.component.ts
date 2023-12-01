/**
 * The Equipment Component serves as the hub for students to create reservations
 * for tables, rooms, and equipment from the CSXL.
 *
 * @author Kris Jordan, Ajay Gandecha
 * @copyright 2023
 * @license MIT
 */

import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { EquipmentService } from '../equipment.service';
import {
  EquipmentStatus,
  OperatingHours,
  Reservation,
  EquipmentAvailability
} from '../equipment.models';
import {
  Observable,
  Subscription,
  filter,
  map,
  mergeMap,
  of,
  timer
} from 'rxjs';
import { ReservationService } from '../reservation/reservation.service';

@Component({
  selector: 'app-equipment-home',
  templateUrl: './equipment-home.component.html',
  styleUrls: ['./equipment-home.component.css']
})
export class EquipmentPageComponent implements OnInit, OnDestroy {
  public status$: Observable<EquipmentStatus>;

  public openOperatingHours$: Observable<OperatingHours | undefined>;
  public isOpen$: Observable<boolean>;

  public activeReservation$: Observable<Reservation | undefined>;

  private timerSubscription!: Subscription;

  /** Route information to be used in App Routing Module */
  public static Route: Route = {
    path: '',
    component: EquipmentPageComponent,
    title: 'Equipment',
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };

  constructor(
    route: ActivatedRoute,
    public equipmentService: EquipmentService,
    private router: Router,
    private reservationService: ReservationService
  ) {
    this.status$ = equipmentService.status$;
    this.openOperatingHours$ = this.initNextOperatingHours();
    this.isOpen$ = this.initIsOpen();
    this.activeReservation$ = this.initActiveReservation();
  }

  reserve(equipmentSelection: EquipmentAvailability[]) {
    this.equipmentService.draftReservation(equipmentSelection).subscribe({
      next: (reservation) => {
        this.router.navigateByUrl(`/equipment/reservation/${reservation.id}`);
      }
    });
  }

  ngOnInit(): void {
    this.timerSubscription = timer(0, 10000).subscribe(() =>
      this.equipmentService.pollStatus()
    );
  }

  ngOnDestroy(): void {
    this.timerSubscription.unsubscribe();
  }

  private initNextOperatingHours(): Observable<OperatingHours | undefined> {
    return this.status$.pipe(
      map((status) => {
        let now = new Date();
        return status.operating_hours.find((hours) => hours.start <= now);
      })
    );
  }

  private initIsOpen(): Observable<boolean> {
    return this.openOperatingHours$.pipe(
      map((hours) => {
        let now = new Date();
        return hours !== undefined && hours.start <= now && hours.end > now;
      })
    );
  }

  private initActiveReservation(): Observable<Reservation | undefined> {
    return this.status$.pipe(
      map((status) => {
        let reservations = status.my_reservations;
        let now = new Date();
        return reservations.find(
          (reservation) => reservation.start <= now && reservation.end > now
        );
      }),
      mergeMap((reservation) =>
        reservation
          ? this.reservationService.get(reservation.id)
          : of(undefined)
      )
    );
  }
}
