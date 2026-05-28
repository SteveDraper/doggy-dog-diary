import { useState, type FormEvent } from "react";
import { createDog } from "../api/dogs";
import type { DogCreatePayload } from "../types/dog";
import Overlay from "./Overlay";

interface AddDogOverlayProps {
  onClose: () => void;
  onCreated: () => void;
}

export default function AddDogOverlay({ onClose, onCreated }: AddDogOverlayProps) {
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    const trimmed = name.trim();
    if (!trimmed) {
      setError("Name is required.");
      return;
    }

    setSaving(true);
    setError(null);
    try {
      const payload: DogCreatePayload = { name: trimmed };
      await createDog(payload);
      onCreated();
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not create dog.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Overlay title="Add dog" onClose={onClose}>
      <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
        <label className="flex flex-col gap-1 text-sm font-medium text-stone-700">
          Name
          <input
            type="text"
            value={name}
            onChange={(event) => setName(event.target.value)}
            className="rounded-lg border border-stone-300 px-3 py-2 text-base font-normal text-stone-900 focus:border-amber-400 focus:outline-none focus:ring-2 focus:ring-amber-200"
            autoFocus
          />
        </label>
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
            {saving ? "Saving…" : "Add"}
          </button>
        </div>
      </form>
    </Overlay>
  );
}
