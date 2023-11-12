/**
 * The Equipment Page Component serves as a hub for students to browse all of the CS
 * equipment at UNC. Students are also able to check out equipment.
 */

import { Component } from '@angular/core';
import { profileResolver } from '/workspace/frontend/src/app/profile/profile.resolver';
import { Equipment } from '../equipment.model';
import { ActivatedRoute } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Profile } from '/workspace/frontend/src/app/profile/profile.service';
import { equipmentResolver } from '../equipment.resolver';

@Component({
  selector: 'app-equipment-page',
  templateUrl: './equipment-page.component.html',
  styleUrls: ['./equipment-page.component.css']
})
export class EquipmentPageComponent {
  /** Route information to be used in Equipment Routing Module */
  public static Route = {
    path: '',
    title: 'CS Equipment',
    component: EquipmentPageComponent,
    canActivate: [],
    resolve: { profile: profileResolver, equipment: equipmentResolver }
  };

  /** Store Observable list of Equipment */
  public equipment: Equipment[];

  /** Store searchBarQuery */
  public searchBarQuery = '';

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** Stores the user permission value for current equipment. */
  public permValues: Map<number, number> = new Map();

  constructor(
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar
  ) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      profile: Profile;
      equipment: Equipment[];
    };
    this.profile = data.profile;
    this.equipment = data.equipment;
  }
}
