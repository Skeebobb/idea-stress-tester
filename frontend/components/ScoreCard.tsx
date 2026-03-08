"use client";

import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";

interface ScoreCardProps {
  ideaScore: number;
  predictedCategory: string;
  competitionLevel: string;
  index?: number;
}

const MotionCard = motion(Card);

export function ScoreCard({
  ideaScore,
  predictedCategory,
  competitionLevel,
  index = 0,
}: ScoreCardProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <MotionCard
        className="p-5 shadow-sm hover:shadow-md transition-shadow duration-200"
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: index * 0.05 }}
      >
        <p className="text-xs font-medium text-slate-500 uppercase tracking-wide mb-2">
          Idea Score
        </p>
        <p className="text-3xl font-semibold text-slate-900 tabular-nums">
          {ideaScore.toFixed(2)}
        </p>
      </MotionCard>
      <MotionCard
        className="p-5 shadow-sm hover:shadow-md transition-shadow duration-200"
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: index * 0.05 + 0.05 }}
      >
        <p className="text-xs font-medium text-slate-500 uppercase tracking-wide mb-2">
          Predicted Category
        </p>
        <p
          className="text-lg font-medium text-slate-900 truncate"
          title={predictedCategory}
        >
          {predictedCategory}
        </p>
      </MotionCard>
      <MotionCard
        className="p-5 shadow-sm hover:shadow-md transition-shadow duration-200"
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: index * 0.05 + 0.1 }}
      >
        <p className="text-xs font-medium text-slate-500 uppercase tracking-wide mb-2">
          Competition Level
        </p>
        <p className="text-lg font-medium capitalize text-slate-900">
          {competitionLevel}
        </p>
      </MotionCard>
    </div>
  );
}
