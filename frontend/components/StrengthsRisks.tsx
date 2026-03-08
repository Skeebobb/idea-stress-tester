"use client";

import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";

interface StrengthsRisksProps {
  strengths: string[];
  risks: string[];
  index?: number;
}

const MotionCard = motion(Card);

export function StrengthsRisks({
  strengths,
  risks,
  index = 0,
}: StrengthsRisksProps) {
  const hasContent = strengths.length > 0 || risks.length > 0;
  if (!hasContent) return null;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <MotionCard
        className="p-5 shadow-sm hover:shadow-md transition-shadow duration-200"
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: index * 0.05 }}
      >
        <h3 className="text-xs font-medium text-emerald-700 uppercase tracking-wide mb-3">
          Strengths
        </h3>
        {strengths.length === 0 ? (
          <p className="text-sm text-slate-500">None identified yet.</p>
        ) : (
          <ul className="space-y-2 text-sm text-slate-800">
            {strengths.map((s, i) => (
              <motion.li
                key={i}
                className="flex items-start gap-2"
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.05 + i * 0.03 }}
              >
                <span className="text-emerald-500 shrink-0 mt-1">•</span>
                {s}
              </motion.li>
            ))}
          </ul>
        )}
      </MotionCard>
      <MotionCard
        className="p-5 shadow-sm hover:shadow-md transition-shadow duration-200"
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: index * 0.05 + 0.05 }}
      >
        <h3 className="text-xs font-medium text-amber-700 uppercase tracking-wide mb-3">
          Risks
        </h3>
        {risks.length === 0 ? (
          <p className="text-sm text-slate-500">No major risks identified.</p>
        ) : (
          <ul className="space-y-2 text-sm text-slate-800">
            {risks.map((r, i) => (
              <motion.li
                key={i}
                className="flex items-start gap-2"
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.05 + i * 0.03 }}
              >
                <span className="text-amber-500 shrink-0 mt-1">•</span>
                {r}
              </motion.li>
            ))}
          </ul>
        )}
      </MotionCard>
    </div>
  );
}
