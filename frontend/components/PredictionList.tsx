"use client";

import { motion } from "framer-motion";
import type { PredictionItem } from "@/types";
import { Card } from "@/components/ui/card";

interface PredictionListProps {
  predictions: PredictionItem[];
  index?: number;
}

const MotionCard = motion(Card);

export function PredictionList({ predictions, index = 0 }: PredictionListProps) {
  if (predictions.length === 0) return null;

  return (
    <MotionCard
      className="p-5 shadow-sm hover:shadow-md transition-shadow duration-200"
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.05 }}
    >
      <h3 className="text-xs font-medium text-slate-500 uppercase tracking-wide mb-3">
        Top Predictions
      </h3>
      <ul className="space-y-3">
        {predictions.map((p, i) => (
          <motion.li
            key={i}
            className="flex justify-between items-center py-1.5 px-3 rounded-lg hover:bg-white/5 transition-colors"
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: index * 0.05 + i * 0.03 }}
          >
            <span className="text-sm text-slate-800">{p.category}</span>
            <span className="text-sm text-sky-600 font-medium tabular-nums">
              {(p.probability * 100).toFixed(1)}%
            </span>
          </motion.li>
        ))}
      </ul>
    </MotionCard>
  );
}
