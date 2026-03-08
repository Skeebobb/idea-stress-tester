export interface PredictionItem {
  category: string;
  probability: number;
}

export interface SimilarIdea {
  idea: string;
  category: string;
  similarity: number;
}

export interface AnalyzeResponse {
  input_idea: string;
  predicted_category: string;
  confidence: number;
  idea_score: number;
  competition_level: string;
  top_predictions: PredictionItem[];
  similar_ideas: SimilarIdea[];
  strengths: string[];
  risks: string[];
  recommendations: string[];
}
