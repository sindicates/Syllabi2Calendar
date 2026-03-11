import { CalendarDays } from "lucide-react";

export default function Header() {
  return (
    <header className="flex items-center gap-3 rounded-xl border border-zinc-800 bg-zinc-900/80 px-5 py-3">
      <CalendarDays className="h-7 w-7 text-[var(--accent)]" />
      <span className="text-xl font-semibold tracking-tight text-zinc-100">
        Syllabi2Calendar
      </span>
      <span className="rounded-md border border-zinc-600 bg-zinc-800 px-2 py-0.5 text-xs font-medium text-zinc-400">
        Beta
      </span>
    </header>
  );
}
