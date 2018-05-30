
// import angular modules
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PlatformModule } from '@angular/cdk/platform';
import { HttpClientModule, HTTP_INTERCEPTORS} from '@angular/common/http';

// import services
import { ConfigService } from './services/config/config.service';
import { NavigationService } from './services/navigation/navigation.service';
import { SplashScreenService } from './services/splash-screen/splash-screen.service';
import { TranslationLoaderService } from './services/translation-loader/translation-loader.service';
import { AuthenticationService } from './services/authentication/authentication.service';

// import interceptors
import { AuthenticationInterceptor } from './interceptors/authentication/authentication.interceptor';

// import gurds
import { AuthenticationGuard } from './guards/authentication/authentication.guard';
import { DeauthenticationGuard } from './guards/deauthentication/deauthentication.guard';


@NgModule({
  imports: [
    CommonModule,
    PlatformModule
  ],
  providers:[
    ConfigService,
    NavigationService,
    SplashScreenService,
    TranslationLoaderService,
    AuthenticationService,
    AuthenticationGuard,
    DeauthenticationGuard,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthenticationInterceptor,
      multi: true
    }
  ],
  declarations: [],
})
export class CoreModule { }
