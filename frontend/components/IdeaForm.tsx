"use client";

import { motion } from "framer-motion";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

interface IdeaFormProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  loading: boolean;
  error?: string | null;
  minLength?: number;
}

export function IdeaForm({
  value,
  onChange,
  onSubmit,
  loading,
  error,
  minLength = 10,
}: IdeaFormProps) {
  const trimmedLength = value.trim().length;
  const isTooShort = trimmedLength > 0 && trimmedLength < minLength;

  return (
    <motion.div
      className="space-y-4"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
    >
      <div className="space-y-2">
        <div className="flex items-baseline justify-between gap-2">
          <label className="text-sm font-medium text-slate-900">
            Describe your idea
          </label>
          <p className="text-xs text-slate-500">
            {trimmedLength}/{minLength} characters minimum
          </p>
        </div>
        <Textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Describe your idea in a few clear sentences so we can give meaningful feedback."
          disabled={loading}
          className={
            isTooShort || error
              ? "border-red-300 focus-visible:ring-red-500 focus-visible:ring-offset-red-50"
              : ""
          }
        />
        <div className="flex items-center justify-between text-xs mt-1">
          <span
            className={
              isTooShort || error ? "text-red-500" : "text-slate-500"
            }
          >
            {error
              ? error
              : isTooShort
              ? `Your idea is a bit short. Try adding a few more details.`
              : "We only store your idea for this analysis session."}
          </span>
        </div>
      </div>

      <Separator className="my-1" />

      <div className="flex items-center justify-end">
        <motion.div
          whileHover={{
            y: loading || !value.trim() || isTooShort ? 0 : -1,
          }}
          whileTap={{
            y: loading || !value.trim() || isTooShort ? 0 : 0,
          }}
          transition={{ duration: 0.15 }}
        >
          <Button
            onClick={onSubmit}
            disabled={loading || !value.trim() || isTooShort}
            size="lg"
          >
            {loading ? "Analyzing…" : "Run analysis"}
          </Button>
        </motion.div>
      </div>
    </motion.div>
  );
}
