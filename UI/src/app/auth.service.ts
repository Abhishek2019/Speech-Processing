import { Injectable } from '@angular/core';
import {Http, Headers} from '@angular/http';
import { map, filter, catchError, mergeMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: Http) { }

  sendData(data) {
    const headers = new Headers();
    headers.append('Content-Type', ' application/json');
    return this.http.post('/getData', data, {headers: headers}).pipe(map(res => res.json()));
  }
}
