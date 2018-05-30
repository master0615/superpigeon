import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { AuthenticationService } from '../../../../core/services/authentication/authentication.service';
import 'rxjs/add/operator/map';

@Injectable()
export class UserService {

  endpoint:string;

  constructor(private http: HttpClient,
    private authenticationService:AuthenticationService ) {
    this.endpoint = 'https://web:8000';
  }

  register(newUser): Observable<any> {
    // create new accoint
    return this.http.post(`${this.endpoint}/api/signup/`, newUser);
  }

  login(credentials): Observable<any> {
    // authenticate user
    return this.http.post(`${this.endpoint}/api/auth/`, credentials).map((profile:any) => {
      this.authenticationService.setToken({value: profile.token});
      return profile;
    });
  }
}
