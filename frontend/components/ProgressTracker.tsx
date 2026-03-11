"use client";

import { motion } from "framer-motion";
import { Check, FileText, Sparkles, Calendar } from "lucide-react";

const STEPS = [
  { id: "read", label: "Reading document", icon: FileText },
  { id: "extract", label: "Extracting dates with AI", icon: Sparkles },
  { id: "push", label: "Pushing to Google Calendar", icon: Calendar },
] as const;

type StepId = (typeof STEPS)[number]["id"];

type Props = {
  currentStep: StepId;
  /** When currentStep is "push", set to true only while create-events request is in progress */
  step3InProgress?: boolean;
};

export default function ProgressTracker({ currentStep, step3InProgress = false }: Props) {
  const currentIndex = STEPS.findIndex((s) => s.id === currentStep);
  const step3Active = currentStep === "push" && step3InProgress;

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-6">
      <p className="mb-4 text-sm font-medium text-zinc-400">Processing steps</p>
      <ul className="flex flex-col gap-3 sm:flex-row sm:gap-6">
        {STEPS.map((step, i) => {
          const isDone =
            step.id === "push" ? false : currentStep === "push" || currentIndex > i;
          const isActive = step.id === "push" ? step3Active : currentIndex === i;
          const Icon = step.icon;
          return (
            <motion.li
              key={step.id}
              initial={false}
              animate={{
                opacity: isDone || isActive ? 1 : 0.6,
              }}
              className="flex items-center gap-3"
            >
              <motion.span
                animate={{
                  scale: isActive ? 1.1 : 1,
                  backgroundColor: isDone
                    ? "var(--accent)"
                    : isActive
                      ? "rgba(59, 130, 246, 0.3)"
                      : "rgb(39 39 42)",
                }}
                className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-zinc-700"
              >
                {isDone ? (
                  <Check className="h-4 w-4 text-white" />
                ) : (
                  <Icon className={`h-4 w-4 ${isActive ? "text-[var(--accent)]" : "text-zinc-500"}`} />
                )}
              </motion.span>
              <span
                className={`text-sm font-medium ${isDone || isActive ? "text-zinc-200" : "text-zinc-500"}`}
              >
                {step.label}
              </span>
            </motion.li>
          );
        })}
      </ul>
    </div>
  );
}
