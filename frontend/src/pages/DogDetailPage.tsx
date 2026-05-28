import { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getDog } from "../api/dogs";
import type { Dog } from "../types/dog";
import { DOG_STATUS_LABELS } from "../types/dog";
import ProfileSummary from "../components/ProfileSummary";
import QuickEditOverlay from "../components/QuickEditOverlay";
import type { EditSection } from "../components/ProfileSummary";

export default function DogDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [dog, setDog] = useState<Dog | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editSection, setEditSection] = useState<EditSection | null>(null);

  const loadDog = useCallback(async () => {
    if (!id) {
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const result = await getDog(id);
      setDog(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load dog.");
      setDog(null);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    void loadDog();
  }, [loadDog]);

  if (loading) {
    return (
      <main className="mx-auto min-h-screen max-w-3xl px-6 py-8">
        <p className="text-stone-600">Loading profile…</p>
      </main>
    );
  }

  if (error || !dog) {
    return (
      <main className="mx-auto min-h-screen max-w-3xl px-6 py-8">
        <Link to="/" className="text-sm font-medium text-amber-800 hover:text-amber-900">
          ← Back to home
        </Link>
        <p className="mt-6 text-red-600">{error ?? "Dog not found."}</p>
      </main>
    );
  }

  return (
    <main className="mx-auto min-h-screen max-w-3xl px-6 py-8">
      <Link to="/" className="text-sm font-medium text-amber-800 hover:text-amber-900">
        ← Back to home
      </Link>

      <header className="mt-6 flex flex-col gap-4 sm:flex-row sm:items-center">
        <div
          className={`flex h-24 w-24 shrink-0 items-center justify-center rounded-2xl ${
            dog.status === "current" ? "bg-amber-100" : "bg-stone-200"
          }`}
          aria-hidden="true"
        >
          <span className="text-4xl">{dog.status === "current" ? "🐕" : "🕯️"}</span>
        </div>
        <div>
          <h1 className="text-3xl font-bold text-amber-950">{dog.name}</h1>
          {dog.status !== "current" && (
            <p className="mt-1 text-sm font-medium uppercase tracking-wide text-stone-500">
              {DOG_STATUS_LABELS[dog.status]}
            </p>
          )}
        </div>
      </header>

      <div className="mt-8">
        <ProfileSummary
          dog={dog}
          onEditBasics={() => setEditSection("basics")}
          onEditStatus={() => setEditSection("status")}
          onEditKennelClub={() => setEditSection("kennel-club")}
          onEditDescription={() => setEditSection("description")}
        />
      </div>

      {editSection && (
        <QuickEditOverlay
          dog={dog}
          section={editSection}
          onClose={() => setEditSection(null)}
          onSaved={setDog}
        />
      )}
    </main>
  );
}
