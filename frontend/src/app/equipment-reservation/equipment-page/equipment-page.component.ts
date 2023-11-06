import { Component } from '@angular/core';
import { profileResolver } from '/workspace/frontend/src/app/profile/profile.resolver';
//import { Organization } from '../organization.model';
import { ActivatedRoute } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Profile } from '/workspace/frontend/src/app/profile/profile.service';
//import { organizationResolver } from '../organization.resolver';

@Component({
  selector: 'app-equipment-page',
  templateUrl: './equipment-page.component.html',
  styleUrls: ['./equipment-page.component.css']
})
export class EquipmentPageComponent {
  public static Route = {
    path: 'equipment-reservation',
    component: EquipmentPageComponent
    //canActivate: [],
    //resolve: { profile: profileResolver, organizations: organizationResolver }
  };

  /** Store Observable list of Organizations */
  //public organizations: Organization[];

  /** Store searchBarQuery */
  public searchBarQuery = '';

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** Stores the user permission value for current organization. */
  public permValues: Map<number, number> = new Map();

  constructor(
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar
  ) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      profile: Profile;
      //organizations: Organization[];
    };
    this.profile = data.profile;
    //this.organizations = data.organizations;
  }
}
