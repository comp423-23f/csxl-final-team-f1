import { Component, OnInit, Input } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute, Route } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { equipmentResolver } from '../../equipment.resolver';
import { Profile } from '/workspace/frontend/src/app/profile/profile.service';
import {
  Equipment,
  EquipmentReservationService
} from '../../equipment.service';

@Component({
  selector: 'equipment-card',
  templateUrl: './equipment-card.widget.html',
  styleUrls: ['./equipment-card.widget.css']
})
export class EquipmentCardWidget implements OnInit {
  public static Route: Route = {
    path: 'equipment',
    component: EquipmentCardWidget,
    title: 'Equipment',
    canActivate: [isAuthenticated],
    resolve: { equipment: equipmentResolver }
  };

  /** Inputs and outputs go here */
  @Input() equipment!: Equipment;
  /** The profile of the currently signed in user */
  @Input() profile?: Profile;
  /** @deprecated Stores the permission values for a profile */
  @Input() profilePermissions!: Map<number, number>;

  constructor(
    route: ActivatedRoute,
    protected equipmentService: EquipmentReservationService,
    protected snackBar: MatSnackBar
  ) {
    const data = route.snapshot.data as { equipment: Equipment };
    this.equipment = data.equipment;
  }
  ngOnInit(): void {
    let equipment = this.equipment;
  }

  reserveEquipment(): void {
    this.equipment.reservable = false;
    this.equipmentService.updateEquipment(this.equipment);
  }
}
