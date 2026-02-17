// ── Enums ──

export type ShotStatus =
  | "pending"
  | "in_progress"
  | "review"
  | "approved"
  | "final";

export type ReviewStatus = "approved" | "needs_revision" | "note";

export const SHOT_STATUSES: ShotStatus[] = [
  "pending",
  "in_progress",
  "review",
  "approved",
  "final",
];

// ── Shows ──

export interface Show {
  id: number;
  title: string;
  code: string;
  status: string;
  created_at: string;
}

export interface ShowDetail extends Show {
  sequences: Sequence[];
}

// ── Sequences ──

export interface Sequence {
  id: number;
  show_id: number;
  code: string;
  description: string | null;
  created_at: string;
}

export interface SequenceDetail extends Sequence {
  shots: Shot[];
}

// ── Shots ──

export interface Shot {
  id: number;
  sequence_id: number;
  code: string;
  status: ShotStatus;
  assigned_to: string | null;
  frame_start: number;
  frame_end: number;
  created_at: string;
  updated_at: string;
}

export interface ShotDetail extends Shot {
  reviews: Review[];
}

export interface ShotUpdate {
  status?: ShotStatus;
  assigned_to?: string | null;
  frame_start?: number;
  frame_end?: number;
}

// ── Reviews ──

export interface Review {
  id: number;
  shot_id: number;
  author: string;
  status: ReviewStatus;
  body: string;
  department: string | null;
  created_at: string;
}

export interface ReviewCreate {
  author: string;
  status: ReviewStatus;
  body: string;
  department?: string;
}

export interface ReviewSearchResult {
  id: number;
  shot_id: number;
  author: string;
  status: string;
  body: string;
  department: string | null;
  score: number;
}

// ── Seed ──

export interface SeedResponse {
  message: string;
  shows: number;
  sequences: number;
  shots: number;
  reviews: number;
}
