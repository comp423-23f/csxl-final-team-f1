/* eslint-disable prettier/prettier */
/**
 * The Equipment Routing Module holds all of the routes that are children
 * to the path /equipment/...
 */

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EquipmentPageComponent } from './equipment-page/equipment-page.component';

const routes: Routes = [EquipmentPageComponent.Route];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EquipmentRoutingModule {}
