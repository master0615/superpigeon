// import angular modules
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

// import animations
import { Animations } from '../../../../shared/animations';

// import services
import { ConfigService } from '../../../../core/services/config/config.service';
import { UserService } from '../../services/user/user.service';

@Component({
  selector: 'login-component',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  animations: Animations
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  loginFormErrors: any;

  constructor(private config: ConfigService,
    private formBuilder: FormBuilder,
    private router: Router,
    public userService: UserService) {
    this.config.setSettings({
      layout: {
        navigation: 'none',
        toolbar: 'none',
        footer: 'none'
      }
    });

    this.loginFormErrors = {
      email: {},
      password: {}
    };
  }

  ngOnInit() {
    this.loginForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });

    this.loginForm.valueChanges.subscribe(() => {
      this.onLoginFormValuesChanged();
    });
  }

  onLoginFormValuesChanged() {
    for (const field in this.loginFormErrors) {
      if (!this.loginFormErrors.hasOwnProperty(field)) {
        continue;
      }

      // Clear previous errors
      this.loginFormErrors[field] = {};

      // Get the control
      const control = this.loginForm.get(field);

      if (control && control.dirty && !control.valid) {
        this.loginFormErrors[field] = control.errors;
      }
    }
  }

  login() {
    console.log(this.userService);
    this.userService.login(this.loginForm.value).subscribe((response)=> {
      this.router.navigate(['/']);
    });
  }
}
