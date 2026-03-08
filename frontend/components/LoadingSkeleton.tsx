"use client";

import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";

export function LoadingSkeleton() {
  return (
    <motion.div
      className="mt-6"
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Card className="p-5 shadow-sm space-y-4">
        <div className="flex gap-4">
          <motion.div
            className="h-20 flex-1 rounded-xl bg-slate-100"
            animate={{ opacity: [0.4, 0.9, 0.4] }}
            transition={{ duration: 1.4, repeat: Infinity }}
          />
          <motion.div
            className="h-20 flex-1 rounded-xl bg-slate-100"
            animate={{ opacity: [0.4, 0.9, 0.4] }}
            transition={{ duration: 1.4, repeat: Infinity, delay: 0.2 }}
          />
          <motion.div
            className="h-20 flex-1 rounded-xl bg-slate-100"
            animate={{ opacity: [0.4, 0.9, 0.4] }}
            transition={{ duration: 1.4, repeat: Infinity, delay: 0.4 }}
          />
        </div>
        <motion.div
          className="h-3 rounded-full bg-slate-100 w-3/4"
          animate={{ opacity: [0.4, 0.9, 0.4] }}
          transition={{ duration: 1.4, repeat: Infinity, delay: 0.3 }}
        />
        <motion.div
          className="h-3 rounded-full bg-slate-100 w-1/2"
          animate={{ opacity: [0.4, 0.9, 0.4] }}
          transition={{ duration: 1.4, repeat: Infinity, delay: 0.5 }}
        />
      </Card>
    </motion.div>
  );
}
