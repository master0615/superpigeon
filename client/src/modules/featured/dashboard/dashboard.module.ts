// import angular modules
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

// import shared module
import { SharedModule } from '../../shared/shared.module';

// import routing configurations
import { RouterConfigurations } from './dashboard.routing';

// import component
import { DashboardComponent } from './components/dashboard/dashboard.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    RouterModule.forChild(RouterConfigurations)
  ],
  declarations: [
    DashboardComponent
  ]
})
export class DashboardModule { }
