import { TestBed, async, inject } from '@angular/core/testing';

import { DeauthenticationGuard } from './deauthentication.guard';

describe('UnAuthenticatedGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [DeauthenticationGuard]
    });
  });

  it('should ...', inject([DeauthenticationGuard], (guard: DeauthenticationGuard) => {
    expect(guard).toBeTruthy();
  }));
});
