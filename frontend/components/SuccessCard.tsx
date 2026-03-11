"use client";

import { CheckCircle } from "lucide-react";

type Props = {
  eventsCreated: number;
  onOpenCalendar: () => void;
  onClear: () => void;
};

export default function SuccessCard({
  eventsCreated,
  onOpenCalendar,
  onClear,
}: Props) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-8 text-center">
      <CheckCircle className="mx-auto mb-4 h-16 w-16 text-[var(--accent)]" />
      <h2 className="mb-2 text-xl font-semibold text-zinc-100">Events created</h2>
      <p className="mb-6 text-zinc-400">
        {eventsCreated} {eventsCreated === 1 ? "event" : "events"} added to your Google Calendar.
      </p>
      <div className="flex flex-col gap-3 sm:flex-row sm:justify-center">
        <button
          type="button"
          onClick={onOpenCalendar}
          className="rounded-xl border border-[var(--accent)] bg-[var(--accent)] px-6 py-3 font-medium text-white transition-opacity hover:opacity-90"
        >
          Open Google Calendar
        </button>
        <button
          type="button"
          onClick={onClear}
          className="rounded-xl border border-zinc-600 bg-zinc-800 px-6 py-3 font-medium text-zinc-200 transition-colors hover:bg-zinc-700"
        >
          Clear & start over
        </button>
      </div>
    </div>
  );
}
