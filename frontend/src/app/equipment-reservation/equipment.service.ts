import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs';

export interface Equipment {
  id: number | null;
  name: string;
  reservable: boolean;
  image: string;
}

@Injectable({
  providedIn: 'root'
})
export class EquipmentReservationService {
  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService,
    protected snackBar: MatSnackBar
  ) {}

  /** Returns all equipment entries from the backend database table using the backend HTTP get request.
   * @returns {Observable<Equipment[]>}
   */
  getEquipment(): Observable<Equipment[]> {
    return this.http.get<Equipment[]>('/api/equipment');
  }

  /** Returns the new equipment object from the backend database table using the backend HTTP post request.
   * @param equipment: EquipmentSummary representing the new equipment
   * @returns {Observable<Equipment>}
   */
  createEquipment(equipment: Equipment): Observable<Equipment> {
    return this.http.post<Equipment>('/api/equipment', equipment);
  }

  /** Returns the updated equipment object from the backend database table using the backend HTTP put request.
   * @param equipment: EquipmentSummary representing the updated equipment

export { Equipment };
   * @returns {Observable<Equipment>}
   */
  updateEquipment(equipment: Equipment): Observable<Equipment> {
    return this.http.put<Equipment>('/api/equipment', equipment);
  }
}
