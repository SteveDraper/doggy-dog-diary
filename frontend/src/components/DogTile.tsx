import { Link } from "react-router-dom";
import type { Dog } from "../types/dog";
import { DOG_STATUS_LABELS } from "../types/dog";

interface DogTileProps {
  dog: Dog;
}

export default function DogTile({ dog }: DogTileProps) {
  const isCurrent = dog.status === "current";

  return (
    <Link
      to={`/dogs/${dog.id}`}
      className={`group flex flex-col overflow-hidden rounded-2xl border bg-white shadow-sm transition hover:shadow-md ${
        isCurrent ? "border-amber-200" : "border-stone-300 opacity-90"
      }`}
    >
      <div
        className={`flex aspect-square items-center justify-center ${
          isCurrent ? "bg-amber-100" : "bg-stone-200"
        }`}
        aria-hidden="true"
      >
        <span className="text-5xl">{isCurrent ? "🐕" : "🕯️"}</span>
      </div>
      <div className="flex flex-col gap-1 px-4 py-3">
        <span className="text-lg font-semibold text-amber-950 group-hover:text-amber-800">
          {dog.name}
        </span>
        {!isCurrent && (
          <span className="text-xs font-medium uppercase tracking-wide text-stone-500">
            {DOG_STATUS_LABELS[dog.status]}
          </span>
        )}
      </div>
    </Link>
  );
}
