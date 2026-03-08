"use client";

import { motion } from "framer-motion";
import type { SimilarIdea } from "@/types";
import { Card } from "@/components/ui/card";

interface SimilarIdeasProps {
  ideas: SimilarIdea[];
  index?: number;
}

const MotionCard = motion(Card);

export function SimilarIdeas({ ideas, index = 0 }: SimilarIdeasProps) {
  if (ideas.length === 0) return null;

  return (
    <MotionCard
      className="p-5 shadow-sm hover:shadow-md transition-shadow duration-200"
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.05 }}
    >
      <h3 className="text-xs font-medium text-slate-500 uppercase tracking-wide mb-3">
        Similar Ideas
      </h3>
      <ul className="space-y-3">
        {ideas.map((item, i) => (
          <motion.li
            key={i}
            className="text-sm py-2 px-3 rounded-lg hover:bg-slate-50 transition-colors"
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: index * 0.05 + i * 0.03 }}
          >
            <p className="text-slate-800">{item.idea}</p>
            <p className="text-slate-500 text-xs mt-1">
              {item.category} · {(item.similarity * 100).toFixed(1)}% similar
            </p>
          </motion.li>
        ))}
      </ul>
    </MotionCard>
  );
}
