import { Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { AuthenticationService } from '../../services/authentication/authentication.service';

@Injectable()
export class AuthenticationInterceptor implements HttpInterceptor {
  constructor(private authenticationService: AuthenticationService) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Get the authorization header from the service.
    const authorizationHeader = this.authenticationService.getAuthorizationHeader();
    if(authorizationHeader) {
      // Clone the request to add the new header.
      const authenticationRequest
        = request.clone({headers: request.headers.set('Authorization', authorizationHeader)});
      // Pass on the cloned request instead of the original request.
      return next.handle(authenticationRequest);
    }
    else {
      return next.handle(request);
    }
  }
}
