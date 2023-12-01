import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EquipmentPageComponent } from './equipment-home/equipment-home.component';
import { EquipmentAmbassadorPageComponent } from './ambassador-home/ambassador-home.component';
import { ReservationComponent } from './reservation/reservation.component';

const routes: Routes = [
  EquipmentPageComponent.Route,
  ReservationComponent.Route,
  EquipmentAmbassadorPageComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EquipmentRoutingModule {}
