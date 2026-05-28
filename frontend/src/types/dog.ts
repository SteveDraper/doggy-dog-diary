export type DogSex = "male" | "female" | "unknown";
export type DogStatus = "current" | "deceased" | "rehomed";

export interface Dog {
  id: string;
  name: string;
  date_of_birth: string | null;
  sex: DogSex;
  breed: string | null;
  neutered: boolean | null;
  microchip: string | null;
  status: DogStatus;
  status_date: string | null;
  kc_registered_name: string | null;
  kc_number: string | null;
  kc_body: string | null;
  description: string | null;
  profile_photo_path: string | null;
  created_at: string;
  updated_at: string;
}

export type DogCreatePayload = Pick<Dog, "name"> &
  Partial<
    Omit<Dog, "id" | "name" | "profile_photo_path" | "created_at" | "updated_at">
  >;

export type DogUpdatePayload = Partial<
  Omit<Dog, "id" | "profile_photo_path" | "created_at" | "updated_at">
>;

export const DOG_SEX_LABELS: Record<DogSex, string> = {
  male: "Male",
  female: "Female",
  unknown: "Unknown",
};

export const DOG_STATUS_LABELS: Record<DogStatus, string> = {
  current: "Current",
  deceased: "Deceased",
  rehomed: "Rehomed",
};
