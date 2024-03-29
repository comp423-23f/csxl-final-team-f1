import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute, Route } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from '../profile.resolver';
import { Profile, ProfileService } from '../profile.service';

@Component({
  selector: 'app-profile-editor',
  templateUrl: './profile-editor.component.html',
  styleUrls: ['./profile-editor.component.css']
})
export class ProfileEditorComponent implements OnInit {
  public static Route: Route = {
    path: 'profile',
    component: ProfileEditorComponent,
    title: 'Profile',
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };

  public profile: Profile;

  public profileForm = this.formBuilder.group({
    first_name: '',
    last_name: '',
    email: '',
    pronouns: ''
  });

  constructor(
    route: ActivatedRoute,
    protected formBuilder: FormBuilder,
    protected profileService: ProfileService,
    protected snackBar: MatSnackBar
  ) {
    const form = this.profileForm;
    form.get('first_name')?.addValidators(Validators.required);
    form.get('lastname')?.addValidators(Validators.required);
    form
      .get('email')
      ?.addValidators([
        Validators.required,
        Validators.email,
        Validators.pattern(/unc\.edu$/)
      ]);
    form.get('pronouns')?.addValidators(Validators.required);

    const data = route.snapshot.data as { profile: Profile };
    console.log(data.profile);
    this.profile = data.profile;
    if (this.profile.signed_agreement != true) {
      this.profile.signed_agreement = false;
    }
    console.log(data.profile);
  }

  ngOnInit(): void {
    let profile = this.profile;

    this.profileForm.setValue({
      first_name: profile.first_name,
      last_name: profile.last_name,
      email: profile.email,
      pronouns: profile.pronouns
    });
  }

  onSubmit(): void {
    if (this.profileForm.valid) {
      Object.assign(this.profile, this.profileForm.value);
      this.profileService.put(this.profile).subscribe({
        next: (user) => this.onSuccess(user),
        error: (err) => this.onError(err)
      });
    }
  }

  agreeToTerms(): void {
    this.profile.signed_agreement = true;
    this.profileService.put(this.profile).subscribe({
      next: (user) => this.onSuccess(user),
      error: (err) => this.onError(err)
    });
  }

  private onSuccess(profile: Profile) {
    this.snackBar.open('Profile Saved', '', { duration: 2000 });
  }

  private onError(err: any) {
    console.error('How to handle this?');
  }

  linkWithGitHub(): void {
    this.profileService.getGitHubOAuthLoginURL().subscribe((url) => {
      window.location.href = url;
    });
  }

  unlinkGitHub() {
    this.profileService.unlinkGitHub().subscribe({
      next: () => (this.profile.github = '')
    });
  }

  //   agreeToTerms(event: any) {
  //     // Your logic when the checkbox state changes
  //     if (event.checked) {
  //       console.log('Checkbox is checked');
  //     } else {
  //       console.log('Checkbox is unchecked');
  //       // Handle the unchecked state if needed
  //     }
  //   }
}
