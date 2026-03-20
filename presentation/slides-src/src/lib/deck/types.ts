import type { ComponentType } from "svelte";

export type ChapterId =
  | "problem"
  | "build"
  | "observe"
  | "evaluate"
  | "scale"
  | "demo"
  | "outcome";

export type SlideDefinition = {
  id: string;
  chapter: ChapterId;
  title: string;
  component: ComponentType;
  notes: string;
};

export type ChapterDefinition = {
  id: ChapterId;
  label: string;
};
