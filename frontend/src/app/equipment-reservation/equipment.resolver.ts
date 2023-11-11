/**
 * The Equipment Resolver allows the equipment to be injected into the routes
 * of components.
 */

import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { Equipment } from './equipment.model';
import { EquipmentReservationService } from './equipment.service';

/** This resolver injects the list of equipment into the equipment component. */
export const equipmentResolver: ResolveFn<Equipment[] | undefined> = (
  route,
  state
) => {
  return inject(EquipmentReservationService).getEquipment();
};
