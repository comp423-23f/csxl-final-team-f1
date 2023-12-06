/* eslint-disable prettier/prettier */
import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  Output,
  SimpleChanges
} from '@angular/core';
import {
  Equipment,
  EquipmentAvailability
} from 'src/app/equipment/equipment.models';

class EquipmentCategory {
  public title: string;

  public reservable_now: boolean = false;
  public equipment_available_now: EquipmentAvailability[] = [];

  public reservable_soon: boolean = false;
  public next_available?: EquipmentAvailability;
  public equipment_available_soon: EquipmentAvailability[] = [];

  // TODO: Handle edge case where only openings are < 1hr
  // public truncated: boolean = false;
  // public truncated_at?: Date;

  constructor(title: string) {
    this.title = title;
  }

  push(equipment: EquipmentAvailability) {
    const epsilon = 59 /* seconds */ * 1000; /* milliseconds */
    /* We use an epsilon of ~1 min to combat the potential for clock drift on
             devices relative to the server's time. Difficult to reproduce in dev due
             to server and client sharing the same system clock, but experienced in
             prod on day 0 with many laptops having slightly drifted system clocks. */
    const now = new Date(Date.now() + epsilon);
    if (equipment.availability[0].start <= now) {
      this.equipment_available_now.push(equipment);
      if (this.equipment_available_now.length === 1) {
        this.reservable_now = true;
        this.next_available = equipment;
      }
    } else {
      this.equipment_available_soon.push(equipment);
      if (!this.reservable_now && this.equipment_available_soon.length === 1) {
        this.reservable_soon = true;
        this.next_available = equipment;
      }
    }
  }

  availabilityString(): string {
    let result = 'Available ';
    if (this.reservable_now) {
      result += 'now';
    } else if (this.reservable_soon) {
      result += ' in ';
      let now = new Date();
      let start = this.equipment_available_soon[0].availability[0].start;
      let delta = Math.ceil((start.getTime() - now.getTime()) / (60 * 1000));
      result += ` ${delta} minutes`;
    } else {
      return 'None available';
    }
    return result;
  }
}

const KEYBOARD = 0;
const MOUSE = 1;
const VR = 2;

@Component({
  selector: 'equipment-dropin-availability-card',
  templateUrl: './dropin-availability-card.widget.html',
  styleUrls: ['./dropin-availability-card.widget.css']
})
export class EquipmentDropInCard implements OnChanges {
  @Input() equipment_availability!: EquipmentAvailability[];
  @Output() equipmentSelected = new EventEmitter<EquipmentAvailability[]>();

  public categories: EquipmentCategory[];

  constructor() {
    this.categories = this.initCategories();
  }

  //Might Need?
  ngOnChanges(changes: SimpleChanges): void {
    this.equipment_availability =
      changes['equipment_availability'].currentValue;
    this.categories = this.initCategories();
    for (let equipment of this.equipment_availability) {
      if (equipment.is_keyboard) {
        this.categories[KEYBOARD].push(equipment);
      } else if (equipment.is_mouse) {
        this.categories[MOUSE].push(equipment);
      } else {
        this.categories[VR].push(equipment);
      }
    }
  }

  reserve(category: EquipmentCategory): void {
    this.equipmentSelected.emit([
      ...category.equipment_available_now,
      ...category.equipment_available_soon
    ]);
  }

  private initCategories(): EquipmentCategory[] {
    return [
      new EquipmentCategory('Keyboards'),
      new EquipmentCategory('Mouses'),
      new EquipmentCategory('VR Headsets')
    ];
  }
}
