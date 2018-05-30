import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, Router, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs/Observable';
import { AuthenticationService } from '../../services/authentication/authentication.service';

@Injectable()
export class AuthenticationGuard implements CanActivate {

  constructor(private router:Router,
    private authenticationService: AuthenticationService) {}

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean> | Promise<boolean> | boolean {

      if(this.authenticationService.getAuthorizationHeader()) {
        return true;
      }
      else {
        this.router.navigate(['/user/login']);
        return false;
      }
  }
}
