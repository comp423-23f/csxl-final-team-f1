import { Profile } from '../models.module';

export interface TimeRangeJSON {
  start: string;
  end: string;
}

export interface TimeRange {
  start: Date;
  end: Date;
}

export interface OperatingHoursJSON extends TimeRangeJSON {
  id: number;
}

export interface OperatingHours extends TimeRange {
  id: number;
}

export const parseTimeRange = (json: TimeRangeJSON): TimeRange => {
  return {
    start: new Date(json.start),
    end: new Date(json.end)
  };
};

export const parseOperatingHoursJSON = (
  json: OperatingHoursJSON
): OperatingHours => {
  return Object.assign({}, json, parseTimeRange(json));
};

export interface Equipment {
  id: number;
  name: string;
  reservable: boolean;
  is_keyboard: boolean;
  is_mouse: boolean;
  is_vr: boolean;
}

export interface ReservationJSON extends TimeRangeJSON {
  id: number;
  users: Profile[];
  equipment: Equipment[];
  walkin: boolean;
  created_at: string;
  updated_at: string;
  state: string;
}

export interface Reservation extends TimeRange {
  id: number;
  users: Profile[];
  equipment: Equipment[];
  walkin: boolean;
  created_at: Date;
  updated_at: Date;
  state: string;
}

export const parseReservationJSON = (json: ReservationJSON): Reservation => {
  const timestamps = {
    created_at: new Date(json.created_at),
    updated_at: new Date(json.updated_at)
  };
  return Object.assign({}, json, parseTimeRange(json), timestamps);
};

export interface EquipmentAvailabilityJSON extends Equipment {
  availability: TimeRangeJSON[];
}

export interface EquipmentAvailability extends Equipment {
  availability: TimeRange[];
}

export const parseEquipmentAvailabilityJSON = (
  json: EquipmentAvailabilityJSON
): EquipmentAvailability => {
  let availability = json.availability.map(parseTimeRange);
  return Object.assign({}, json, { availability });
};

export interface EquipmentStatusJSON {
  my_reservations: ReservationJSON[];
  equipment_availability: EquipmentAvailabilityJSON[];
  operating_hours: OperatingHoursJSON[];
}

export interface EquipmentStatus {
  my_reservations: Reservation[];
  equipment_availability: EquipmentAvailability[];
  operating_hours: OperatingHours[];
}

export const parseEquipmentStatusJSON = (
  json: EquipmentStatusJSON
): EquipmentStatus => {
  return {
    my_reservations: json.my_reservations.map(parseReservationJSON),
    equipment_availability: json.equipment_availability.map(
      parseEquipmentAvailabilityJSON
    ),
    operating_hours: json.operating_hours.map(parseOperatingHoursJSON)
  };
};

export interface ReservationRequest extends TimeRange {
  users: Profile[];
  equipment: Equipment[];
}
