interface AddDogTileProps {
  onClick: () => void;
}

export default function AddDogTile({ onClick }: AddDogTileProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label="Add dog"
      className="flex flex-col overflow-hidden rounded-2xl border border-dashed border-amber-300/80 bg-white/40 shadow-sm transition hover:border-amber-400 hover:bg-white/60 hover:shadow-md focus:outline-none focus:ring-2 focus:ring-amber-300 focus:ring-offset-2 focus:ring-offset-amber-50"
    >
      <div className="flex aspect-square items-center justify-center">
        <svg
          aria-hidden="true"
          viewBox="0 0 24 24"
          className="h-10 w-10 text-amber-700/70"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
        >
          <path strokeLinecap="round" d="M12 5v14M5 12h14" />
        </svg>
      </div>
      <div className="px-4 py-3" aria-hidden="true">
        <span className="invisible text-lg font-semibold">Placeholder</span>
      </div>
    </button>
  );
}
