// import angular modules
import { Routes } from '@angular/router';

// import app featured modules
import { UserModule } from '../modules/featured/user/user.module';

export const RouterConfigurations: Routes = [{
    path: '',
    redirectTo: 'dashboard',
    pathMatch: 'full'
  },
  {
    path: 'dashboard',
    loadChildren: '../modules/featured/dashboard/dashboard.module#DashboardModule'
  },
  {
    path: 'user',
    loadChildren: '../modules/featured/user/user.module#UserModule'
  },
];
