"use client";

import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";

interface RecommendationsProps {
  recommendations: string[];
  index?: number;
}

const MotionCard = motion(Card);

export function Recommendations({
  recommendations,
  index = 0,
}: RecommendationsProps) {
  if (recommendations.length === 0) return null;

  return (
    <MotionCard
      className="p-5 shadow-sm hover:shadow-md transition-shadow duration-200"
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.05 }}
    >
      <h3 className="text-xs font-medium text-slate-500 uppercase tracking-wide mb-3">
        Recommendations
      </h3>
      <ul className="space-y-3 text-sm text-slate-800">
        {recommendations.map((rec, i) => (
          <motion.li
            key={i}
            className="flex items-start gap-3 py-1.5 px-3 rounded-lg hover:bg-slate-50 transition-colors"
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: index * 0.05 + i * 0.03 }}
          >
            <span className="text-sky-600 font-medium shrink-0 mt-0.5">
              {i + 1}.
            </span>
            {rec}
          </motion.li>
        ))}
      </ul>
    </MotionCard>
  );
}
