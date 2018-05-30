// import angular modules
import { Routes } from '@angular/router';

// import component
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { ForgotPasswordComponent } from './components/forgot-password/forgot-password.component';
import { ResetPasswordComponent } from './components/reset-password/reset-password.component';

// import guards
import { AuthenticationGuard } from '../../core/guards/authentication/authentication.guard';
import { DeauthenticationGuard } from '../../core/guards/deauthentication/deauthentication.guard';


export const RouterConfigurations: Routes = [{
    path: 'login',
    component: LoginComponent,
    canActivate: [DeauthenticationGuard]
  },
  {
    path: 'register',
    component: RegisterComponent,
    canActivate: [DeauthenticationGuard]
  },
  {
    path: 'forgot/password',
    component: ForgotPasswordComponent,
    canActivate: [DeauthenticationGuard]
  },
  {
    path: 'reset/password',
    component: ResetPasswordComponent,
    canActivate: [AuthenticationGuard]
  }
];
