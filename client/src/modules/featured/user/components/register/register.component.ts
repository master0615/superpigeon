// import angular modules
import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

// import animations
import { Animations } from '../../../../shared/animations';

// import services
import { ConfigService } from '../../../../core/services/config/config.service';
import { UserService } from '../../services/user/user.service';

@Component({
  selector: 'register-component',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
  animations: Animations
})
export class RegisterComponent implements OnInit {
  registerForm: FormGroup;
  registerFormErrors: any;

  constructor( private config: ConfigService,
    private formBuilder: FormBuilder,
    private router: Router,
    private userService: UserService) {
    this.config.setSettings({
      layout: {
        navigation: 'none',
        toolbar: 'none',
        footer: 'none'
      }
    });

    this.registerFormErrors = {
      name: {},
      email: {},
      password: {},
      passwordConfirm: {}
    };
  }

  ngOnInit() {
    this.registerForm = this.formBuilder.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
      passwordConfirm: ['', [Validators.required, confirmPassword]]
    });

    this.registerForm.valueChanges.subscribe(() => {
      this.onRegisterFormValuesChanged();
    });
  }

  onRegisterFormValuesChanged() {
    for (const field in this.registerFormErrors) {
      if (!this.registerFormErrors.hasOwnProperty(field)) {
        continue;
      }

      // Clear previous errors
      this.registerFormErrors[field] = {};

      // Get the control
      const control = this.registerForm.get(field);

      if (control && control.dirty && !control.valid) {
        this.registerFormErrors[field] = control.errors;
      }
    }
  }

  register() {
    this.userService.register(this.registerForm.value).subscribe((newUser)=> {
      this.userService.login(this.registerForm.value).subscribe((user)=> {
          this.router.navigate(['/']);
      });
    });
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
