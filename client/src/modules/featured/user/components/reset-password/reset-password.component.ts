import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ConfigService } from '../../../../core/services/config/config.service';
import { Animations } from '../../../../shared/animations';

@Component({
  selector: 'reset-password-component',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.scss'],
  animations: Animations
})
export class ResetPasswordComponent implements OnInit {
  resetPasswordForm: FormGroup;
  resetPasswordFormErrors: any;

  constructor(
    private config: ConfigService,
    private formBuilder: FormBuilder
  ) {
    this.config.setSettings({
      layout: {
        navigation: 'none',
        toolbar: 'none',
        footer: 'none'
      }
    });

    this.resetPasswordFormErrors = {
      email: {},
      password: {},
      passwordConfirm: {}
    };
  }

  ngOnInit() {
    this.resetPasswordForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
      passwordConfirm: ['', [Validators.required, confirmPassword]]
    });

    this.resetPasswordForm.valueChanges.subscribe(() => {
      this.onResetPasswordFormValuesChanged();
    });
  }

  onResetPasswordFormValuesChanged() {
    for (const field in this.resetPasswordFormErrors) {
      if (!this.resetPasswordFormErrors.hasOwnProperty(field)) {
        continue;
      }

      // Clear previous errors
      this.resetPasswordFormErrors[field] = {};

      // Get the control
      const control = this.resetPasswordForm.get(field);

      if (control && control.dirty && !control.valid) {
        this.resetPasswordFormErrors[field] = control.errors;
      }
    }
  }
}

function confirmPassword(control: AbstractControl) {
  if (!control.parent || !control) {
    return;
  }

  const password = control.parent.get('password');
  const passwordConfirm = control.parent.get('passwordConfirm');

  if (!password || !passwordConfirm) {
    return;
  }

  if (passwordConfirm.value === '') {
    return;
  }

  if (password.value !== passwordConfirm.value) {
    return {
      passwordsNotMatch: true
    };
  }
}
