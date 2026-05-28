import type { ReactNode } from "react";
import type { Dog, DogSex, DogStatus, DogUpdatePayload } from "../types/dog";
import { DOG_SEX_LABELS, DOG_STATUS_LABELS } from "../types/dog";
import { formatBoolean, formatDate, formatOptional } from "../lib/format";

interface ProfileSummaryProps {
  dog: Dog;
  onEditBasics: () => void;
  onEditStatus: () => void;
  onEditKennelClub: () => void;
  onEditDescription: () => void;
}

function SummarySection({
  title,
  onEdit,
  children,
}: {
  title: string;
  onEdit: () => void;
  children: ReactNode;
}) {
  return (
    <section className="rounded-2xl border border-amber-100 bg-white p-5 shadow-sm">
      <div className="mb-4 flex items-center justify-between gap-3">
        <h2 className="text-lg font-semibold text-amber-950">{title}</h2>
        <button
          type="button"
          onClick={onEdit}
          aria-label={`Edit ${title.toLowerCase()}`}
          className="rounded-lg px-3 py-1.5 text-sm font-medium text-amber-800 hover:bg-amber-50"
        >
          Edit
        </button>
      </div>
      <dl className="grid gap-3 sm:grid-cols-2">{children}</dl>
    </section>
  );
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-xs font-medium uppercase tracking-wide text-stone-500">{label}</dt>
      <dd className="mt-1 text-stone-900">{value}</dd>
    </div>
  );
}

export default function ProfileSummary({
  dog,
  onEditBasics,
  onEditStatus,
  onEditKennelClub,
  onEditDescription,
}: ProfileSummaryProps) {
  return (
    <div className="flex flex-col gap-5">
      <SummarySection title="Basics" onEdit={onEditBasics}>
        <Field label="Name" value={dog.name} />
        <Field label="Date of birth" value={formatDate(dog.date_of_birth)} />
        <Field label="Sex" value={DOG_SEX_LABELS[dog.sex]} />
        <Field label="Breed" value={formatOptional(dog.breed)} />
        <Field label="Neutered / spayed" value={formatBoolean(dog.neutered)} />
        <Field label="Microchip" value={formatOptional(dog.microchip)} />
      </SummarySection>

      <SummarySection title="Dog status" onEdit={onEditStatus}>
        <Field label="Status" value={DOG_STATUS_LABELS[dog.status]} />
        <Field label="Status date" value={formatDate(dog.status_date)} />
      </SummarySection>

      <SummarySection title="Kennel club registration" onEdit={onEditKennelClub}>
        <Field label="Registered name" value={formatOptional(dog.kc_registered_name)} />
        <Field label="Registration number" value={formatOptional(dog.kc_number)} />
        <Field label="Registering body" value={formatOptional(dog.kc_body)} />
      </SummarySection>

      <SummarySection title="Description" onEdit={onEditDescription}>
        <div className="sm:col-span-2">
          <Field
            label="Notes"
            value={dog.description?.trim() ? dog.description : "No description yet."}
          />
        </div>
      </SummarySection>
    </div>
  );
}

export type EditSection = "basics" | "status" | "kennel-club" | "description";

export const EDIT_SECTION_TITLES: Record<EditSection, string> = {
  basics: "Edit basics",
  status: "Edit dog status",
  "kennel-club": "Edit kennel club registration",
  description: "Edit description",
};

export function buildUpdatePayload(
  section: EditSection,
  form: FormData,
): DogUpdatePayload {
  switch (section) {
    case "basics":
      return {
        name: String(form.get("name") ?? "").trim(),
        date_of_birth: emptyToNull(String(form.get("date_of_birth") ?? "")),
        sex: String(form.get("sex") ?? "unknown") as DogSex,
        breed: emptyToNull(String(form.get("breed") ?? "")),
        neutered: parseOptionalBoolean(String(form.get("neutered") ?? "")),
        microchip: emptyToNull(String(form.get("microchip") ?? "")),
      };
    case "status":
      return {
        status: String(form.get("status") ?? "current") as DogStatus,
        status_date: emptyToNull(String(form.get("status_date") ?? "")),
      };
    case "kennel-club":
      return {
        kc_registered_name: emptyToNull(String(form.get("kc_registered_name") ?? "")),
        kc_number: emptyToNull(String(form.get("kc_number") ?? "")),
        kc_body: emptyToNull(String(form.get("kc_body") ?? "")),
      };
    case "description":
      return {
        description: emptyToNull(String(form.get("description") ?? "")),
      };
  }
}

function emptyToNull(value: string): string | null {
  const trimmed = value.trim();
  return trimmed ? trimmed : null;
}

function parseOptionalBoolean(value: string): boolean | null {
  if (value === "") {
    return null;
  }
  return value === "true";
}
