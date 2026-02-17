import { useSeed } from "../hooks/useSeed";

export default function SeedButton() {
  const seed = useSeed();

  return (
    <button
      className="btn btn--primary"
      onClick={() => seed.mutate()}
      disabled={seed.isPending}
    >
      {seed.isPending ? "Seeding..." : "Seed Database"}
    </button>
  );
}
