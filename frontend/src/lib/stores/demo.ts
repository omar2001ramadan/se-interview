import { writable } from "svelte/store";

export type DemoTab = "chat" | "live" | "traces" | "evaluation" | "embeddings" | "architecture";

export const selectedTab = writable<DemoTab>("chat");
export const selectedTraceId = writable<string | null>(null);
export const recentSessionId = writable<string | null>(null);
