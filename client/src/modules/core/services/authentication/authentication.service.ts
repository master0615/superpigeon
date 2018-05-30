import { Injectable } from '@angular/core';
import { Token } from '../../interfaces/token.interface';

@Injectable()
export class AuthenticationService {

  token: Token;

  constructor() { }

  getToken() {
    if(!this.token) {
      this.token = JSON.parse(localStorage.getItem('authentication'));
    }
    return this.token;
  }

  setToken(token) {
    this.token = token;
    localStorage.setItem('authentication', JSON.stringify(token));
  }

  getAuthorizationHeader() {
    const token = this.getToken();
    if(token) {
      return token.value;
    }
    else {
      return null;
    }
  }

  forgetToken() {
    this.token = null;
    localStorage.setItem('authentication', null);
  }

}
