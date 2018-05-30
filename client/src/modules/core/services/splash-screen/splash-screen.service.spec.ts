import { TestBed, inject } from '@angular/core/testing';

import { SplashScreenService } from './splash-screen.service';

describe('SplashScreenService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [SplashScreenService]
    });
  });

  it('should be created', inject([SplashScreenService], (service: SplashScreenService) => {
    expect(service).toBeTruthy();
  }));
});
