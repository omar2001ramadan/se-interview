import type { ChapterDefinition, SlideDefinition } from "$lib/deck/types";
import ProductSlide from "$lib/slides/problem/01-product/Slide.svelte";
import StartingPointSlide from "$lib/slides/problem/02-starting-point/Slide.svelte";
import WhatChangedSlide from "$lib/slides/build/03-what-changed/Slide.svelte";
import RuntimeArchitectureSlide from "$lib/slides/build/04-runtime-architecture/Slide.svelte";
import GraphDecisionLoopSlide from "$lib/slides/build/05-graph-decision-loop/Slide.svelte";
import ToolContractsSlide from "$lib/slides/build/06-tool-contracts/Slide.svelte";
import StructuredToolOutputSlide from "$lib/slides/build/07-structured-tool-output/Slide.svelte";
import ObserveSlide from "$lib/slides/observe/08-observe/Slide.svelte";
import OneRequestAsTraceSlide from "$lib/slides/observe/09-one-request-as-a-trace/Slide.svelte";
import TraceEvidenceSlide from "$lib/slides/observe/10-trace-evidence/Slide.svelte";
import EvaluateSlide from "$lib/slides/evaluate/11-evaluate/Slide.svelte";
import TestCorpusSlide from "$lib/slides/evaluate/12-test-corpus/Slide.svelte";
import EvaluationPipelineSlide from "$lib/slides/evaluate/13-evaluation-pipeline/Slide.svelte";
import UserFrustrationSlide from "$lib/slides/evaluate/14-user-frustration/Slide.svelte";
import ToolRoutingSlide from "$lib/slides/evaluate/15-tool-routing/Slide.svelte";
import DebuggingExampleSlide from "$lib/slides/evaluate/16-debugging-example/Slide.svelte";
import ScaleSlide from "$lib/slides/scale/17-scale/Slide.svelte";
import ProductionArchitectureSlide from "$lib/slides/scale/18-production-architecture/Slide.svelte";
import OperationalTradeoffsSlide from "$lib/slides/scale/19-operational-tradeoffs/Slide.svelte";
import LiveProofSlide from "$lib/slides/demo/20-live-proof/Slide.svelte";
import OutcomeSlide from "$lib/slides/outcome/21-outcome/Slide.svelte";

export const chapters: ChapterDefinition[] = [
  { id: "problem", label: "Problem" },
  { id: "build", label: "Build" },
  { id: "observe", label: "Observe" },
  { id: "evaluate", label: "Evaluate" },
  { id: "scale", label: "Scale" },
  { id: "demo", label: "Demo" },
  { id: "outcome", label: "Outcome" },
];

export const slides: SlideDefinition[] = [
  {
    id: "product",
    chapter: "problem",
    title: "Travel Assistant",
    component: ProductSlide,
    notes: "Open with the product in plain English before introducing implementation details.",
  },
  {
    id: "starting-point",
    chapter: "problem",
    title: "Starting Point",
    component: StartingPointSlide,
    notes: "Contrast the starter repo with the finished system in one minute.",
  },
  {
    id: "what-changed",
    chapter: "build",
    title: "What Changed",
    component: WhatChangedSlide,
    notes: "Use this as the bridge into implementation. The four changes frame the rest of the build chapter.",
  },
  {
    id: "runtime-architecture",
    chapter: "build",
    title: "Runtime Architecture",
    component: RuntimeArchitectureSlide,
    notes: "This is the anchor architecture slide. Revisit it when traces and evaluations appear later.",
  },
  {
    id: "graph-decision-loop",
    chapter: "build",
    title: "Graph Decision Loop",
    component: GraphDecisionLoopSlide,
    notes: "Explain how the LangGraph loop repeats until the model stops requesting tools.",
  },
  {
    id: "tool-contracts",
    chapter: "build",
    title: "Tool Contracts",
    component: ToolContractsSlide,
    notes: "Tie each behavior to a recognizable user intent and emphasize the honest refusal case.",
  },
  {
    id: "structured-tool-output",
    chapter: "build",
    title: "Structured Tool Output",
    component: StructuredToolOutputSlide,
    notes: "Explain why structured tool output makes synthesis and evaluation easier.",
  },
  {
    id: "observe",
    chapter: "observe",
    title: "Observe",
    component: ObserveSlide,
    notes: "Transition from runtime behavior to observability: one request becomes one trace.",
  },
  {
    id: "trace",
    chapter: "observe",
    title: "One Request As A Trace",
    component: OneRequestAsTraceSlide,
    notes: "Define traces and spans using the same Chicago request flow from the runtime slide.",
  },
  {
    id: "trace-evidence",
    chapter: "observe",
    title: "Trace Evidence",
    component: TraceEvidenceSlide,
    notes: "Present the actual trace counts only after trace semantics are clear.",
  },
  {
    id: "evaluate",
    chapter: "evaluate",
    title: "Evaluate",
    component: EvaluateSlide,
    notes: "Bridge from observing the runtime to scoring the runtime.",
  },
  {
    id: "test-corpus",
    chapter: "evaluate",
    title: "Test Corpus",
    component: TestCorpusSlide,
    notes: "Explain why the prompt set intentionally covers planning, current information, and unsupported actions.",
  },
  {
    id: "evaluation-pipeline",
    chapter: "evaluate",
    title: "Evaluation Pipeline",
    component: EvaluationPipelineSlide,
    notes: "Show the trace export, scoring, annotation loop, and failure dataset.",
  },
  {
    id: "user-frustration",
    chapter: "evaluate",
    title: "User Frustration",
    component: UserFrustrationSlide,
    notes: "Use frustration as the user-centered evaluation before diving into tool correctness.",
  },
  {
    id: "tool-routing",
    chapter: "evaluate",
    title: "Tool Routing",
    component: ToolRoutingSlide,
    notes: "Explain expected versus observed routing and why one miss is useful for debugging credibility.",
  },
  {
    id: "debugging-example",
    chapter: "evaluate",
    title: "Debugging Example",
    component: DebuggingExampleSlide,
    notes: "Use the Tokyo nightlife miss as the concrete debugging story.",
  },
  {
    id: "scale",
    chapter: "scale",
    title: "Scale",
    component: ScaleSlide,
    notes: "Introduce production thinking only after the runtime and evaluation loops are clear.",
  },
  {
    id: "production-architecture",
    chapter: "scale",
    title: "Production Architecture",
    component: ProductionArchitectureSlide,
    notes: "Explain the stateless app, external dependencies, OTLP path, and async eval workers.",
  },
  {
    id: "operational-tradeoffs",
    chapter: "scale",
    title: "Operational Tradeoffs",
    component: OperationalTradeoffsSlide,
    notes: "Close the scale chapter with latency, cost, and reliability decisions.",
  },
  {
    id: "live-proof",
    chapter: "demo",
    title: "Live Proof",
    component: LiveProofSlide,
    notes: "Frame the demo as three proof points, not logistics.",
  },
  {
    id: "outcome",
    chapter: "outcome",
    title: "Outcome",
    component: OutcomeSlide,
    notes: "Close on what was built, what was learned, and why the system is explainable.",
  },
];
