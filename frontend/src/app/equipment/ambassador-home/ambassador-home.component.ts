import { Component, OnDestroy, OnInit } from '@angular/core';
import { Route } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Observable, Subscription, map, mergeMap, tap, timer } from 'rxjs';
import { Reservation } from '../equipment.models';
import { AmbassadorService } from './ambassador.service';

@Component({
  selector: 'app-equipment-ambassador-home',
  templateUrl: './ambassador-home.component.html',
  styleUrls: ['./ambassador-home.component.css']
})
export class EquipmentAmbassadorPageComponent implements OnInit, OnDestroy {
  /** Route information to be used in App Routing Module */
  public static Route: Route = {
    path: 'ambassador',
    component: EquipmentAmbassadorPageComponent,
    title: 'XL Ambassador',
    canActivate: [permissionGuard('equipment.reservation.*', '*')],
    resolve: { profile: profileResolver }
  };

  reservations$: Observable<Reservation[]>;
  upcomingReservations$: Observable<Reservation[]>;
  activeReservations$: Observable<Reservation[]>;

  columnsToDisplay = ['id', 'name', 'equipment', 'start', 'end', 'actions'];

  private refreshSubscription!: Subscription;

  constructor(public ambassadorService: AmbassadorService) {
    this.reservations$ = this.ambassadorService.reservations$;
    this.upcomingReservations$ = this.reservations$.pipe(
      map((reservations) => reservations.filter((r) => r.state === 'CONFIRMED'))
    );
    this.activeReservations$ = this.reservations$.pipe(
      map((reservations) =>
        reservations.filter((r) => r.state === 'CHECKED_IN')
      )
    );
  }

  ngOnInit(): void {
    this.refreshSubscription = timer(0, 5000)
      .pipe(tap((_) => this.ambassadorService.fetchReservations()))
      .subscribe();
  }

  ngOnDestroy(): void {
    this.refreshSubscription.unsubscribe();
  }
}
