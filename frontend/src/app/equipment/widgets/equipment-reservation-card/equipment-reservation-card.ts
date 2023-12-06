import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Reservation } from '../../equipment.models';
import { Observable, map, mergeMap, timer } from 'rxjs';
import { ActivatedRoute, Route } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { Router } from '@angular/router';
import { ReservationService } from '../../reservation/reservation.service';
import { profileResolver } from '../../../profile/profile.resolver';
import { Profile, ProfileService } from '../../../profile/profile.service';

@Component({
  selector: 'equipment-reservation-card',
  templateUrl: './equipment-reservation-card.html',
  styleUrls: ['./equipment-reservation-card.css']
})
export class EquipmentReservationCard implements OnInit {
  public static Route: Route = {
    path: 'profile',
    title: 'Profile',
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };

  public profile: Profile;

  @Input() reservation!: Reservation;

  public liabilityMessage: Boolean;

  public draftConfirmationDeadline$!: Observable<string>;

  constructor(
    route: ActivatedRoute,
    public router: Router,
    public reservationService: ReservationService
  ) {
    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;
    this.liabilityMessage = false;
  }

  ngOnInit(): void {
    this.draftConfirmationDeadline$ = this.initDraftConfirmationDeadline();
  }

  checkinDeadline(reservationStart: Date): Date {
    return new Date(reservationStart.getTime() + 10 * 60 * 1000);
  }

  cancel() {
    this.reservationService.cancel(this.reservation).subscribe();
  }

  confirm() {
    if (this.profile.signed_agreement != true) {
      this.liabilityMessage = true;
    } else {
      this.reservationService.confirm(this.reservation).subscribe();
    }
  }

  checkout() {
    this.reservationService.checkout(this.reservation).subscribe();
  }

  private initDraftConfirmationDeadline(): Observable<string> {
    const fiveMinutes =
      5 /* minutes */ * 60 /* seconds */ * 1000; /* milliseconds */

    const reservationDraftDeadline = (reservation: Reservation) =>
      reservation.created_at.getTime() + fiveMinutes;

    const deadlineString = (deadline: number): string => {
      const now = new Date().getTime();
      const delta = (deadline - now) / 1000; /* milliseconds */
      if (delta > 60) {
        return `Confirm in ${Math.ceil(delta / 60)} minutes`;
      } else if (delta > 0) {
        return `Confirm in ${Math.ceil(delta)} seconds`;
      } else {
        this.cancel();
        return 'Cancelling...';
      }
    };

    return timer(0, 1000).pipe(
      map(() => this.reservation),
      map(reservationDraftDeadline),
      map(deadlineString)
    );
  }
}
