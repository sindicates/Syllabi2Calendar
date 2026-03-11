"use client";

import { useState } from "react";
import { Pencil, Trash2 } from "lucide-react";
import type { Assignment } from "@/lib/api";

function formatDate(start: string): string {
  if (start.includes("T")) {
    return start.slice(0, 10);
  }
  return start;
}

function formatTime(start: string, end: string): string {
  if (!start.includes("T")) return "All Day";
  const s = start.slice(11, 16);
  const e = end.includes("T") ? end.slice(11, 16) : "";
  return e ? `${s} – ${e}` : s;
}

type Props = {
  assignments: Assignment[];
  setAssignments: React.Dispatch<React.SetStateAction<Assignment[]>>;
  timezone: string;
  onPush: () => void;
  pushing: boolean;
};

export default function ReviewTable({
  assignments,
  setAssignments,
  timezone,
  onPush,
  pushing,
}: Props) {
  const [editingIndex, setEditingIndex] = useState<number | null>(null);
  const [editRow, setEditRow] = useState<Assignment | null>(null);

  const startEdit = (index: number) => {
    setEditingIndex(index);
    setEditRow({ ...assignments[index] });
  };

  const saveEdit = () => {
    if (editingIndex === null || editRow === null) return;
    setAssignments((prev) => {
      const next = [...prev];
      next[editingIndex] = editRow;
      return next;
    });
    setEditingIndex(null);
    setEditRow(null);
  };

  const cancelEdit = () => {
    setEditingIndex(null);
    setEditRow(null);
  };

  const deleteRow = (index: number) => {
    setAssignments((prev) => prev.filter((_, i) => i !== index));
    if (editingIndex === index) {
      setEditingIndex(null);
      setEditRow(null);
    } else if (editingIndex !== null && index < editingIndex) {
      setEditingIndex(editingIndex - 1);
    }
  };

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-4 sm:p-6">
      <div className="mb-4 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h2 className="text-lg font-semibold text-zinc-100">Review & edit</h2>
        <button
          type="button"
          onClick={onPush}
          disabled={pushing || assignments.length === 0}
          className="rounded-xl border border-[var(--accent)] bg-[var(--accent)] px-5 py-2.5 font-medium text-white transition-opacity hover:opacity-90 disabled:opacity-50"
        >
          {pushing ? "Pushing…" : "Push to Google Calendar"}
        </button>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[500px] text-left text-sm">
          <thead>
            <tr className="border-b border-zinc-700 text-zinc-400">
              <th className="pb-3 pr-4 font-medium">Assignment</th>
              <th className="pb-3 pr-4 font-medium">Date</th>
              <th className="pb-3 pr-4 font-medium">Time</th>
              <th className="w-24 pb-3 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            {assignments.map((row, index) => (
              <tr
                key={index}
                className="border-b border-zinc-800 text-zinc-200 last:border-0"
              >
                {editingIndex === index && editRow ? (
                  <>
                    <td className="py-3 pr-4">
                      <input
                        value={editRow.summary}
                        onChange={(e) =>
                          setEditRow((p) => (p ? { ...p, summary: e.target.value } : null))
                        }
                        className="w-full rounded border border-zinc-600 bg-zinc-800 px-2 py-1.5 text-zinc-100 outline-none focus:ring-1 focus:ring-[var(--accent)]"
                      />
                    </td>
                    <td className="py-3 pr-4">
                      <input
                        value={formatDate(editRow.start)}
                        onChange={(e) => {
                          const d = e.target.value;
                          const isTimed = editRow.start.includes("T");
                          setEditRow((p) =>
                            p
                              ? {
                                  ...p,
                                  start: isTimed ? `${d}T${editRow.start.slice(11)}` : d,
                                  end: isTimed ? `${d}T${editRow.end.slice(11)}` : d,
                                }
                              : null
                          );
                        }}
                        type="date"
                        className="rounded border border-zinc-600 bg-zinc-800 px-2 py-1.5 text-zinc-100 outline-none focus:ring-1 focus:ring-[var(--accent)]"
                      />
                    </td>
                    <td className="py-3 pr-4">
                      <input
                        value={
                          editRow.start.includes("T")
                            ? editRow.start.slice(11, 16)
                            : ""
                        }
                        onChange={(e) => {
                          const t = e.target.value;
                          const date = editRow.start.slice(0, 10);
                          setEditRow((p) =>
                            p
                              ? {
                                  ...p,
                                  start: t ? `${date}T${t}:00` : date,
                                  end: t ? `${date}T${parseInt(t, 10) + 1}:00:00` : date,
                                }
                              : null
                          );
                        }}
                        type="time"
                        className="rounded border border-zinc-600 bg-zinc-800 px-2 py-1.5 text-zinc-100 outline-none focus:ring-1 focus:ring-[var(--accent)]"
                      />
                    </td>
                    <td className="py-3">
                      <button
                        type="button"
                        onClick={saveEdit}
                        className="text-[var(--accent)] hover:underline"
                      >
                        Save
                      </button>
                      <button
                        type="button"
                        onClick={cancelEdit}
                        className="ml-2 text-zinc-400 hover:underline"
                      >
                        Cancel
                      </button>
                    </td>
                  </>
                ) : (
                  <>
                    <td className="py-3 pr-4">{row.summary}</td>
                    <td className="py-3 pr-4">{formatDate(row.start)}</td>
                    <td className="py-3 pr-4">{formatTime(row.start, row.end)}</td>
                    <td className="py-3">
                      <div className="flex gap-2">
                        <button
                          type="button"
                          onClick={() => startEdit(index)}
                          className="rounded p-1 text-zinc-400 hover:bg-zinc-700 hover:text-zinc-200"
                          aria-label="Edit"
                        >
                          <Pencil className="h-4 w-4" />
                        </button>
                        <button
                          type="button"
                          onClick={() => deleteRow(index)}
                          className="rounded p-1 text-zinc-400 hover:bg-red-900/30 hover:text-red-400"
                          aria-label="Delete"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
