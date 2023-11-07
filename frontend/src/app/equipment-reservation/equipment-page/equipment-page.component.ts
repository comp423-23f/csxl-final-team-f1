import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { EquipmentReservationService } from '../equipment-reservation.service';

@Component({
  selector: 'app-equipment-page',
  templateUrl: './equipment-page.component.html',
  styleUrls: ['./equipment-page.component.css']
})
export class EquipmentPageComponent implements OnInit {
  public static Route = {
    path: 'equipment-reservation',
    component: EquipmentPageComponent
  };

  public searchBarQuery = '';
  public permValues: Map<number, number> = new Map();

  constructor(
    private route: ActivatedRoute,
    private equipmentService: EquipmentReservationService
  ) {}

  ngOnInit(): void {
    this.getEquipmentData();
  }

  getEquipmentData(): void {
    this.equipmentService.getEquipment().subscribe(
      (equipment) => {
        console.log('Equipment Data:', equipment);
      },
      (error) => {
        console.error('Error fetching equipment data:', error);
      }
    );
  }
}
