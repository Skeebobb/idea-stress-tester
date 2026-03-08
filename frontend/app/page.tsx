"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { analyzeIdea } from "@/lib/api";
import type { AnalyzeResponse } from "@/types";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import {
  IdeaForm,
  LoadingSkeleton,
  ScoreCard,
  PredictionList,
  SimilarIdeas,
  StrengthsRisks,
  Recommendations,
} from "@/components";

const MIN_IDEA_LENGTH = 10;

export default function Home() {
  const [idea, setIdea] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [inputError, setInputError] = useState<string | null>(null);

  async function handleAnalyze() {
    const trimmed = idea.trim();
    if (!trimmed) {
      setInputError("Please describe your idea before running an analysis.");
      return;
    }
    if (trimmed.length < MIN_IDEA_LENGTH) {
      setInputError(
        `Add a bit more detail so we can analyze this properly (at least ${MIN_IDEA_LENGTH} characters).`,
      );
      return;
    }

    setLoading(true);
    setError(null);
    setInputError(null);
    setResult(null);
    try {
      const data = await analyzeIdea(trimmed);
      setResult(data);
    } catch {
      setError("Failed to analyze idea. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen max-w-4xl mx-auto px-6 py-12 md:py-16">
      <motion.header
        className="mb-10 md:mb-12 flex flex-col gap-3"
        initial={{ opacity: 0, y: -12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45 }}
      >
        <Badge className="w-fit">Productivity · Idea validation</Badge>
        <div>
          <h1 className="text-3xl md:text-4xl font-semibold tracking-tight text-slate-900">
            Idea Stress Tester
          </h1>
          <p className="mt-2 text-base md:text-lg text-slate-600 max-w-2xl">
            A calm space to sanity‑check your product ideas with structured,
            AI‑powered feedback.
          </p>
        </div>
      </motion.header>

      <motion.section
        className="mb-8"
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, delay: 0.05 }}
      >
        <Card className="shadow-sm">
          <CardHeader>
            <CardTitle>Analyze a new idea</CardTitle>
            <CardDescription>
              Share a concise description, and we&apos;ll score it, assess
              competition, and surface strengths, risks, and recommendations.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <IdeaForm
              value={idea}
              onChange={setIdea}
              onSubmit={handleAnalyze}
              loading={loading}
              error={inputError}
              minLength={MIN_IDEA_LENGTH}
            />
          </CardContent>
        </Card>
      </motion.section>

      <AnimatePresence mode="wait">
        {loading ? (
          <LoadingSkeleton key="loading" />
        ) : error ? (
          <motion.div
            key="error"
            className="mt-4"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            <Card className="border-red-100 bg-red-50">
              <CardContent className="py-3.5 text-sm text-red-700">
                {error}
              </CardContent>
            </Card>
          </motion.div>
        ) : result ? (
          <motion.section
            key="results"
            className="space-y-6 mt-6"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 4 }}
            transition={{ duration: 0.4 }}
          >
            <div className="flex items-baseline justify-between gap-2">
              <h2 className="text-lg font-medium text-slate-900">
                Analysis summary
              </h2>
              <p className="text-xs text-slate-500">
                Based on the latest run for this idea
              </p>
            </div>
            <ScoreCard
              ideaScore={result.idea_score}
              predictedCategory={result.predicted_category}
              competitionLevel={result.competition_level}
            />
            <PredictionList predictions={result.top_predictions} index={1} />
            <SimilarIdeas ideas={result.similar_ideas} index={2} />
            <StrengthsRisks
              strengths={result.strengths}
              risks={result.risks}
              index={3}
            />
            <Recommendations
              recommendations={result.recommendations}
              index={4}
            />
          </motion.section>
        ) : (
          <motion.div
            key="empty"
            className="mt-6"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 4 }}
          >
            <Card className="shadow-sm border-dashed border-slate-200 bg-slate-50/60">
              <CardContent className="py-6 text-sm text-slate-600 flex flex-col gap-1.5">
                <span className="font-medium text-slate-700">
                  No analysis yet.
                </span>
                <span>
                  Describe your next idea above and run an analysis to see
                  scores, predictions, and tailored recommendations here.
                </span>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}
