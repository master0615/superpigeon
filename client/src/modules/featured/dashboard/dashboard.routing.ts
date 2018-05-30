// import angular modules
import { Routes } from '@angular/router';

// import component
import { DashboardComponent } from './components/dashboard/dashboard.component';

// import guards
import { AuthenticationGuard } from '../../core/guards/authentication/authentication.guard';
import { DeauthenticationGuard } from '../../core/guards/deauthentication/deauthentication.guard';


export const RouterConfigurations: Routes = [{
    path: '',
    component: DashboardComponent,
    canActivate: [AuthenticationGuard]
  },
];
