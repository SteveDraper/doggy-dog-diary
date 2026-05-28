import { useCallback, useEffect, useState } from "react";
import { listDogs } from "../api/dogs";
import type { Dog } from "../types/dog";
import AddDogOverlay from "../components/AddDogOverlay";
import AddDogTile from "../components/AddDogTile";
import DogTile from "../components/DogTile";

export default function HomePage() {
  const [dogs, setDogs] = useState<Dog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAddDog, setShowAddDog] = useState(false);

  const loadDogs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await listDogs();
      setDogs(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load dogs.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadDogs();
  }, [loadDogs]);

  return (
    <main className="mx-auto min-h-screen max-w-5xl px-6 py-10">
      <header className="mb-8">
        <h1 className="text-4xl font-bold tracking-tight text-amber-900">Doggy Dog Diary</h1>
        <p className="mt-2 text-stone-600">Your household pet diary.</p>
      </header>

      {loading && <p className="text-stone-600">Loading dogs…</p>}
      {error && <p className="text-red-600">{error}</p>}

      {!loading && !error && (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
          {dogs.map((dog) => (
            <DogTile key={dog.id} dog={dog} />
          ))}
          <AddDogTile onClick={() => setShowAddDog(true)} />
        </div>
      )}

      {showAddDog && (
        <AddDogOverlay onClose={() => setShowAddDog(false)} onCreated={loadDogs} />
      )}
    </main>
  );
}
