import { HttpClient } from '@angular/common/http';
import { Injectable, OnDestroy } from '@angular/core';
import { Observable, Subscription, map, tap } from 'rxjs';
import {
  EquipmentStatus,
  EquipmentStatusJSON,
  Reservation,
  ReservationJSON,
  EquipmentAvailability,
  parseEquipmentStatusJSON,
  parseReservationJSON
} from './equipment.models';
import { ProfileService } from '../profile/profile.service';
import { Profile } from '../models.module';
import { RxEquipmentStatus } from './rx-equipment-status';

const ONE_HOUR = 60 * 60 * 1000;

@Injectable({
  providedIn: 'root'
})
export class EquipmentService implements OnDestroy {
  private status: RxEquipmentStatus = new RxEquipmentStatus();
  public status$: Observable<EquipmentStatus> = this.status.value$;

  private profile: Profile | undefined;
  private profileSubscription!: Subscription;

  public constructor(
    protected http: HttpClient,
    protected profileSvc: ProfileService
  ) {
    this.profileSubscription = this.profileSvc.profile$.subscribe(
      (profile) => (this.profile = profile)
    );
  }

  ngOnDestroy(): void {
    this.profileSubscription.unsubscribe();
  }

  pollStatus(): void {
    this.http
      .get<EquipmentStatusJSON>('/api/equipment/status')
      .pipe(map(parseEquipmentStatusJSON))
      .subscribe((status) => this.status.set(status));
  }

  draftReservation(equipmentSelection: EquipmentAvailability[]) {
    if (this.profile === undefined) {
      throw new Error('Only allowed for logged in users.');
    }

    let start = equipmentSelection[0].availability[0].start;
    let end = new Date(start.getTime() + 2 * ONE_HOUR);
    let reservation = {
      users: [this.profile],
      equipment: equipmentSelection.map((equipmentAvailability) => {
        return { id: equipmentAvailability.id };
      }),
      start,
      end
    };

    return this.http
      .post<ReservationJSON>('/api/equipment/reservation', reservation)
      .pipe(map(parseReservationJSON));
  }
}
