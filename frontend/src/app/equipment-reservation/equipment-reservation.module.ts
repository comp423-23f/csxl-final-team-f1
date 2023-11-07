import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../shared/shared.module';
import { MatCardModule } from '@angular/material/card';
import { EquipmentCard } from './widgets/equipment-card/equipment-card.widget';
import { EquipmentRoutingModule } from './equipment-reservation-routing.module';
import { EquipmentPageComponent } from './equipment-page/equipment-page.component';
import { RouterModule } from '@angular/router';

@NgModule({
  declarations: [EquipmentPageComponent, EquipmentCard],
  imports: [
    MatCardModule,
    EquipmentRoutingModule,
    RouterModule,
    CommonModule,
    SharedModule
  ]
})
export class EquipmentReservationModule {}
