/* eslint-disable prettier/prettier */
import { Component, OnDestroy, OnInit } from '@angular/core';
import { Route } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Observable, Subscription, map, mergeMap, tap, timer } from 'rxjs';
import { Reservation } from '../coworking.models';
import { Reservation as EquipmentReservation } from '../../equipment/equipment.models';
import { AmbassadorService } from './ambassador.service';

@Component({
  selector: 'app-coworking-ambassador-home',
  templateUrl: './ambassador-home.component.html',
  styleUrls: ['./ambassador-home.component.css']
})
export class AmbassadorPageComponent implements OnInit, OnDestroy {
  /** Route information to be used in App Routing Module */
  public static Route: Route = {
    path: 'ambassador',
    component: AmbassadorPageComponent,
    title: 'XL Ambassador',
    canActivate: [permissionGuard('coworking.reservation.*', '*')],
    resolve: { profile: profileResolver }
  };

  reservations$: Observable<Reservation[]>;
  equipmentReservations$: Observable<EquipmentReservation[]>; //Ours
  upcomingReservations$: Observable<Reservation[]>;
  upcomingEquipmentReservations$: Observable<EquipmentReservation[]>; //Ours
  activeReservations$: Observable<Reservation[]>;
  activeEquipmentReservations$: Observable<EquipmentReservation[]>; //Ours

  columnsToDisplay = ['id', 'name', 'seat', 'start', 'end', 'actions'];
  columnsToDisplay2 = ['id', 'name', 'equipment', 'start', 'end', 'actions'];

  private refreshSubscription!: Subscription;

  constructor(public ambassadorService: AmbassadorService) {
    this.reservations$ = this.ambassadorService.reservations$;
    this.equipmentReservations$ = this.ambassadorService.equipmentReservation$; //Ours

    this.upcomingReservations$ = this.reservations$.pipe(
      map((reservations) => reservations.filter((r) => r.state === 'CONFIRMED'))
    );

    this.upcomingEquipmentReservations$ = this.equipmentReservations$.pipe(
      map((reservations) => reservations.filter((r) => r.state === 'CONFIRMED'))
    ); //Ours

    this.activeReservations$ = this.reservations$.pipe(
      map((reservations) =>
        reservations.filter((r) => r.state === 'CHECKED_IN')
      )
    );

    this.activeEquipmentReservations$ = this.equipmentReservations$.pipe(
      map((reservations) =>
        reservations.filter((r) => r.state === 'CHECKED_IN')
      )
    );
  }

  ngOnInit(): void {
    this.refreshSubscription = timer(0, 5000)
      .pipe(tap((_) => this.ambassadorService.fetchReservations()))
      .subscribe();
    this.refreshSubscription = timer(0, 5000) //Ours
      .pipe(tap((_) => this.ambassadorService.fetchEquipmentReservations()))
      .subscribe();
  }

  ngOnDestroy(): void {
    this.refreshSubscription.unsubscribe();
  }
}
