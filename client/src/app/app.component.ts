import { Component } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';

import { SplashScreenService } from '../modules/core/services/splash-screen/splash-screen.service';
import { TranslationLoaderService } from '../modules/core/services/translation-loader/translation-loader.service';
import { NavigationService } from '../modules/core/services/navigation/navigation.service';

import { NavigationModel } from '../modules/core/navigation/navigation.model';
import { locale as navigationEnglish } from '../modules/core/navigation/i18n/en';
import { locale as navigationTurkish } from '../modules/core/navigation/i18n/tr';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  constructor(
    private navigationService: NavigationService,
    private splashScreen: SplashScreenService,
    private translate: TranslateService,
    private translationLoader: TranslationLoaderService
  ) {
    // Add languages
    this.translate.addLangs(['en', 'tr']);

    // Set the default language
    this.translate.setDefaultLang('en');

    // Use a language
    this.translate.use('en');

    // Set the navigation model
    this.navigationService.setNavigationModel(new NavigationModel());

    // Set the navigation translations
    this.translationLoader.loadTranslations(navigationEnglish, navigationTurkish);
  }
}
