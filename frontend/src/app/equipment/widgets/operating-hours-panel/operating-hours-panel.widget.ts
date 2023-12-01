import { Component, Input } from '@angular/core';
import { OperatingHours } from 'src/app/equipment/equipment.models';

@Component({
  selector: 'equipment-operating-hours-panel',
  templateUrl: './operating-hours-panel.widget.html',
  styleUrls: ['./operating-hours-panel.widget.css']
})
export class EquipmentHoursCard {
  @Input() operatingHours!: OperatingHours[];
  @Input() openOperatingHours?: OperatingHours;
}
