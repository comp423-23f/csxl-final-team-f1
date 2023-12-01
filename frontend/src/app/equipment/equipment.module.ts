/* eslint-disable prettier/prettier */
import { AsyncPipe, CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { EquipmentRoutingModule } from './equipment-routing.module';
import { EquipmentPageComponent } from './equipment-home/equipment-home.component';
import { EquipmentAmbassadorPageComponent } from './ambassador-home/ambassador-home.component';
import { MatCardModule } from '@angular/material/card';
import { EquipmentReservationCard } from './widgets/equipment-reservation-card/equipment-reservation-card';
import { MatDividerModule } from '@angular/material/divider';
import { EquipmentDropInCard } from './widgets/dropin-availability-card/dropin-availability-card.widget';
import { MatListModule } from '@angular/material/list';
import { EquipmentHoursCard } from './widgets/operating-hours-panel/operating-hours-panel.widget';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { ReservationComponent } from './reservation/reservation.component';

@NgModule({
  declarations: [
    EquipmentPageComponent,
    ReservationComponent,
    EquipmentAmbassadorPageComponent,
    EquipmentDropInCard,
    EquipmentReservationCard,
    EquipmentHoursCard
  ],
  imports: [
    CommonModule,
    EquipmentRoutingModule,
    MatCardModule,
    MatDividerModule,
    MatListModule,
    MatExpansionModule,
    MatButtonModule,
    MatTableModule,
    AsyncPipe
  ]
})
export class EquipmentModule {}
