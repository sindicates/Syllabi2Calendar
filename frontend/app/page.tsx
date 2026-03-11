"use client";

import { useState, useCallback } from "react";
import Header from "@/components/Header";
import Dropzone from "@/components/Dropzone";
import ProgressTracker from "@/components/ProgressTracker";
import ReviewTable from "@/components/ReviewTable";
import SuccessCard from "@/components/SuccessCard";
import { scanPdf, createEvents, type Extraction, type Assignment } from "@/lib/api";

type Phase = "idle" | "uploading" | "reviewing" | "pushing" | "success";

type ProgressStep = "read" | "extract" | "push";

export default function Home() {
  const [phase, setPhase] = useState<Phase>("idle");
  const [file, setFile] = useState<File | null>(null);
  const [extraction, setExtraction] = useState<Extraction | null>(null);
  const [editableAssignments, setEditableAssignments] = useState<Assignment[]>([]);
  const [eventsResult, setEventsResult] = useState<{
    events_created: number;
    links: string[];
  } | null>(null);
  const [progressStep, setProgressStep] = useState<ProgressStep>("read");

  const handleFileSelect = useCallback(async (selectedFile: File) => {
    setFile(selectedFile);
    setPhase("uploading");
    setProgressStep("read");
    const stepTwoTimeout = setTimeout(() => setProgressStep("extract"), 600);
    try {
      const result = await scanPdf(selectedFile);
      setExtraction(result);
      setEditableAssignments(result.assignments ?? []);
      setPhase("reviewing");
    } catch {
      setPhase("idle");
      setFile(null);
    } finally {
      clearTimeout(stepTwoTimeout);
    }
  }, []);

  const handlePush = useCallback(async () => {
    if (!extraction) return;
    setPhase("pushing");
    setProgressStep("push");
    try {
      const result = await createEvents({
        timezone: extraction.timezone,
        assignments: editableAssignments,
      });
      setEventsResult(result);
      setPhase("success");
    } catch {
      setPhase("reviewing");
    }
  }, [extraction, editableAssignments]);

  const handleOpenCalendar = useCallback(() => {
    window.open("https://calendar.google.com", "_blank");
  }, []);

  const handleClear = useCallback(() => {
    setPhase("idle");
    setFile(null);
    setExtraction(null);
    setEditableAssignments([]);
    setEventsResult(null);
    setProgressStep("read");
  }, []);

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <main className="mx-auto flex min-h-screen max-w-4xl flex-col gap-8 px-4 py-8 sm:px-6">
        <Header />

        {phase === "idle" && (
          <Dropzone
            file={file}
            onFileSelect={handleFileSelect}
            disabled={false}
          />
        )}

        {(phase === "uploading" || phase === "reviewing" || phase === "pushing") && (
          <>
            <ProgressTracker
              currentStep={
                phase === "uploading"
                  ? progressStep
                  : "push"
              }
              step3InProgress={phase === "pushing"}
            />
            {phase === "uploading" && (
              <p className="text-center text-sm text-zinc-500">
                Uploading and analyzing your syllabus…
              </p>
            )}
          </>
        )}

        {phase === "reviewing" && extraction && (
          <ReviewTable
            assignments={editableAssignments}
            setAssignments={setEditableAssignments}
            timezone={extraction.timezone}
            onPush={handlePush}
            pushing={false}
          />
        )}

        {phase === "pushing" && (
          <p className="text-center text-sm text-zinc-500">
            Creating events in Google Calendar…
          </p>
        )}

        {phase === "success" && eventsResult && (
          <SuccessCard
            eventsCreated={eventsResult.events_created}
            onOpenCalendar={handleOpenCalendar}
            onClear={handleClear}
          />
        )}
      </main>
    </div>
  );
}
