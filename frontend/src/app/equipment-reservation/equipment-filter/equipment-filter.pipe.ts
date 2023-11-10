/* eslint-disable prettier/prettier */
/**
 * This is the pipe used to filter equipment on the equipment page.
 */

import { Pipe, PipeTransform } from '@angular/core';
import { Equipment } from '../equipment.model';

@Pipe({
  name: 'equipmentFilter'
})
export class EquipmentFilterPipe implements PipeTransform {
  /** Returns a mapped array of equipment that start with the input string (if search query provided).
   * @param {Observable<Equipment[]>} equipment: observable list of valid Equipment models
   * @param {String} searchQuery: input string to filter by
   * @returns {Observable<Equipment[]>}
   */
  transform(equipment: Equipment[], searchQuery: String): Equipment[] {
    // Sort the organizations list alphabetically by name
    equipment = equipment.sort((a: Equipment, b: Equipment) => {
      return a.name.toLowerCase().localeCompare(b.name.toLowerCase());
    });

    // If a search query is provided, return the organizations that start with the search query.
    if (searchQuery) {
      return equipment.filter((equipment) =>
        equipment.name.toLowerCase().includes(searchQuery.toLowerCase())
      );
    } else {
      // Otherwise, return the original list.
      return equipment;
    }
  }
}
