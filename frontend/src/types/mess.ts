export type MealType = "breakfast" | "lunch" | "snacks" | "dinner";
export type RegistrationStatus = "confirmed" | "cancelled";

export interface Dish {
  id: string;
  name: string;
  is_veg: boolean;
}

export interface Registration {
  id: string;
  meal_id: string;
  status: RegistrationStatus;
  created_at: string;
}

export interface Meal {
  id: string;
  mess_name: string;
  date: string; // ISO date, e.g. "2026-08-26"
  meal_type: MealType;
  dishes: Dish[];
  cutoff_at: string; // ISO datetime
  is_open: boolean;
  registration: Registration | null;
}

export interface DayMenu {
  date: string;
  meals: Meal[];
}

export interface ApiError {
  detail: string;
}
