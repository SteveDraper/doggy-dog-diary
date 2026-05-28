import { useState, type FormEvent } from "react";
import { updateDog } from "../api/dogs";
import type { Dog } from "../types/dog";
import { DOG_SEX_LABELS, DOG_STATUS_LABELS } from "../types/dog";
import Overlay from "./Overlay";
import {
  buildUpdatePayload,
  EDIT_SECTION_TITLES,
  type EditSection,
} from "./ProfileSummary";

interface QuickEditOverlayProps {
  dog: Dog;
  section: EditSection;
  onClose: () => void;
  onSaved: (dog: Dog) => void;
}

const inputClassName =
  "rounded-lg border border-stone-300 px-3 py-2 text-base text-stone-900 focus:border-amber-400 focus:outline-none focus:ring-2 focus:ring-amber-200";

export default function QuickEditOverlay({
  dog,
  section,
  onClose,
  onSaved,
}: QuickEditOverlayProps) {
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const payload = buildUpdatePayload(section, form);

    if (section === "basics" && !payload.name) {
      setError("Name is required.");
      return;
    }

    setSaving(true);
    setError(null);
    try {
      const updated = await updateDog(dog.id, payload);
      onSaved(updated);
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not save changes.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Overlay title={EDIT_SECTION_TITLES[section]} onClose={onClose}>
      <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
        {section === "basics" && (
          <>
            <label className="flex flex-col gap-1 text-sm font-medium text-stone-700">
              Name
              <input
                name="name"
                defaultValue={dog.name}
                className={inputClassName}
                required
              />
            </label>
            <label className="flex flex-col gap-1 text-sm font-medium text-stone-700">
              Date of birth
              <input
                name="date_of_birth"
                type="date"
                defaultValue={dog.date_of_birth ?? ""}
                className={inputClassName}
              />
            </label>
            <label className="flex flex-col gap-1 text-sm font-medium text-stone-700">
              Sex
              <select name="sex" defaultValue={dog.sex} className={inputClassName}>
                {Object.entries(DOG_SEX_LABELS).map(([value, label]) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </select>
            </label>
            <label className="flex flex-col gap-1 text-sm font-medium text-stone-700">
              Breed
              <input name="breed" defaultValue={dog.breed ?? ""} className={inputClassName} />
            </label>
            <label className="flex flex-col gap-1 text-sm font-medium text-stone-700">
              Neutered / spayed
              <select
                name="neutered"
                defaultValue={
                  dog.neutered === null || dog.neutered === undefined
                    ? ""
                    : String(dog.neutered)
                }
                className={inputClassName}
              >
                <option value="">Unknown</option>
                <option value="true">Yes</option>
                <option value="false">No</option>
              </select>
            </label>
            <label className="flex flex-col gap-1 text-sm font-medium text-stone-700">
              Microchip
              <input
                name="microchip"
                defaultValue={dog.microchip ?? ""}
                className={inputClassName}
              />
            </label>
          </>
        )}

        {section === "status" && (
          <>
            <label className="flex flex-col gap-1 text-sm font-medium text-stone-700">
              Status
              <select name="status" defaultValue={dog.status} className={inputClassName}>
                {Object.entries(DOG_STATUS_LABELS).map(([value, label]) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </select>
            </label>
            <label className="flex flex-col gap-1 text-sm font-medium text-stone-700">
              Status date
              <input
                name="status_date"
                type="date"
                defaultValue={dog.status_date ?? ""}
                className={inputClassName}
              />
            </label>
          </>
        )}

        {section === "kennel-club" && (
          <>
            <label className="flex flex-col gap-1 text-sm font-medium text-stone-700">
              Registered name
              <input
                name="kc_registered_name"
                defaultValue={dog.kc_registered_name ?? ""}
                className={inputClassName}
              />
            </label>
            <label className="flex flex-col gap-1 text-sm font-medium text-stone-700">
              Registration number
              <input name="kc_number" defaultValue={dog.kc_number ?? ""} className={inputClassName} />
            </label>
            <label className="flex flex-col gap-1 text-sm font-medium text-stone-700">
              Registering body
              <input name="kc_body" defaultValue={dog.kc_body ?? ""} className={inputClassName} />
            </label>
          </>
        )}

        {section === "description" && (
          <label className="flex flex-col gap-1 text-sm font-medium text-stone-700">
            Description
            <textarea
              name="description"
              defaultValue={dog.description ?? ""}
              rows={5}
              className={inputClassName}
            />
          </label>
        )}

        {error && <p className="text-sm text-red-600">{error}</p>}

        <div className="flex justify-end gap-2">
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg px-4 py-2 text-stone-600 hover:bg-stone-100"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={saving}
            className="rounded-lg bg-amber-700 px-4 py-2 font-medium text-white hover:bg-amber-800 disabled:opacity-60"
          >
            {saving ? "Saving…" : "Save"}
          </button>
        </div>
      </form>
    </Overlay>
  );
}
