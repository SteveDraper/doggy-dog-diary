export function formatDate(value: string | null): string {
  if (!value) {
    return "—";
  }
  const date = new Date(`${value}T00:00:00`);
  return date.toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export function formatOptional(value: string | null | undefined): string {
  if (!value) {
    return "—";
  }
  return value;
}

export function formatBoolean(value: boolean | null | undefined): string {
  if (value === null || value === undefined) {
    return "—";
  }
  return value ? "Yes" : "No";
}
