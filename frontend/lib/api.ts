import type { AnalyzeResponse } from "@/types";

const API_BASE = "http://localhost:8000";

export async function analyzeIdea(idea: string): Promise<AnalyzeResponse> {
  const res = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ idea }),
  });
  if (!res.ok) throw new Error("Failed to analyze idea");
  return res.json();
}

export async function getCategories(): Promise<unknown> {
  const res = await fetch(`${API_BASE}/categories`);
  if (!res.ok) throw new Error("Failed to fetch categories");
  return res.json();
}

export async function getModelInfo(): Promise<unknown> {
  const res = await fetch(`${API_BASE}/model-info`);
  if (!res.ok) throw new Error("Failed to fetch model info");
  return res.json();
}
