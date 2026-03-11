"use client";

import { useCallback } from "react";
import { motion } from "framer-motion";
import { FileText } from "lucide-react";
import toast from "react-hot-toast";

type Props = {
  file: File | null;
  onFileSelect: (file: File) => void;
  disabled?: boolean;
};

const PDF_TYPE = "application/pdf";

export default function Dropzone({ file, onFileSelect, disabled }: Props) {
  const validateAndSet = useCallback(
    (f: File) => {
      if (f.type !== PDF_TYPE) {
        toast.error("Invalid file type. Please upload a PDF.");
        return;
      }
      onFileSelect(f);
    },
    [onFileSelect]
  );

  const onDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      if (disabled) return;
      const f = e.dataTransfer.files[0];
      if (f) validateAndSet(f);
    },
    [disabled, validateAndSet]
  );

  const onDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
  }, []);

  const onInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const f = e.target.files?.[0];
      if (f) validateAndSet(f);
      e.target.value = "";
    },
    [validateAndSet]
  );

  return (
    <motion.div
      onDrop={onDrop}
      onDragOver={onDragOver}
      whileHover={disabled ? {} : { scale: 1.01 }}
      whileTap={disabled ? {} : { scale: 0.99 }}
      className={`flex flex-col items-center justify-center rounded-xl border-2 border-dashed border-zinc-700 bg-zinc-900/50 p-10 transition-colors ${
        disabled ? "cursor-not-allowed opacity-60" : "cursor-pointer hover:border-zinc-600 hover:bg-zinc-800/50"
      }`}
      onClick={() => !disabled && document.getElementById("file-input")?.click()}
    >
      <input
        id="file-input"
        type="file"
        accept={PDF_TYPE}
        className="hidden"
        onChange={onInputChange}
        disabled={disabled}
      />
      {file ? (
        <>
          <FileText className="mb-3 h-14 w-14 text-[var(--accent)]" />
          <p className="text-center font-medium text-zinc-200">{file.name}</p>
          <p className="mt-1 text-sm text-zinc-500">PDF selected</p>
        </>
      ) : (
        <>
          <FileText className="mb-3 h-14 w-14 text-zinc-500" />
          <p className="text-center font-medium text-zinc-300">
            Drop your syllabus PDF here, or click to browse
          </p>
          <p className="mt-1 text-sm text-zinc-500">PDF only</p>
        </>
      )}
    </motion.div>
  );
}
