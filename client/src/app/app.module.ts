import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { TranslateModule } from '@ngx-translate/core';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { RouterModule } from '@angular/router';

import { CoreModule } from '../modules/core/core.module';
import { UserModule } from '../modules/featured/user/user.module';

// import routing configurations
import { RouterConfigurations } from './app.routing';


// import bootstrap component
import { AppComponent } from './app.component';


@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    CoreModule,
    UserModule,
    HttpClientModule,
    BrowserAnimationsModule,
    RouterModule.forRoot(RouterConfigurations),
    TranslateModule.forRoot()
  ],
  providers: [
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
