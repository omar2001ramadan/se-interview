<script lang="ts">
  import { browser } from "$app/environment";
  import { recentSessionId, selectedTab, selectedTraceId, type DemoTab } from "$lib/stores/demo";
  import { onMount } from "svelte";
  import { get } from "svelte/store";

  type ChatSource = {
    url: string;
    label?: string | null;
  };

  type ChatUIResponse = {
    response: string;
    session_id: string;
    sources: ChatSource[];
    tool_hints: string[];
    notes: string[];
  };

  type ChatMessage = {
    id: string;
    role: "user" | "assistant";
    content: string;
    sessionId?: string;
    sources?: ChatSource[];
    notes?: string[];
  };

  type DemoOverview = {
    available: boolean;
    message?: string | null;
    trace_count: number;
    total_spans: number;
    total_queries: number;
    tool_usage_incorrect: number;
    frustrated_count: number;
    incorrect_rate?: number | null;
    frustration_rate?: number | null;
    phoenix_base_url?: string | null;
    phoenix_project_name?: string | null;
  };

  type CorpusDescriptor = {
    id: string;
    label: string;
    description?: string | null;
    count: number;
    session_ids: string[];
    prompts: string[];
    download_url: string;
  };

  type CorpusManifest = {
    available: boolean;
    message?: string | null;
    corpora: CorpusDescriptor[];
  };

  type TraceListItem = {
    trace_id: string;
    span_id?: string | null;
    session_id?: string | null;
    name: string;
    prompt_preview?: string | null;
    start_time?: string | null;
    end_time?: string | null;
    status_code?: string | null;
    span_count: number;
    llm_span_count: number;
    tool_names: string[];
    phoenix_url?: string | null;
  };

  type TraceListResponse = {
    available: boolean;
    message?: string | null;
    traces: TraceListItem[];
  };

  type EvaluationResult = {
    kind: string;
    session_id?: string | null;
    span_id?: string | null;
    label: string;
    score?: number | null;
    explanation?: string | null;
    prompt?: string | null;
    scenario_type?: string | null;
    observed_tool_names: string[];
  };

  type SpanSummary = {
    span_id: string;
    parent_id?: string | null;
    name: string;
    span_kind?: string | null;
    status_code?: string | null;
    start_time?: string | null;
    end_time?: string | null;
    duration_ms?: number | null;
    input_preview?: string | null;
    output_preview?: string | null;
    error_message?: string | null;
    tool_name?: string | null;
  };

  type TraceDetail = {
    available: boolean;
    message?: string | null;
    trace?: TraceListItem | null;
    spans: SpanSummary[];
    evaluations: EvaluationResult[];
  };

  type EvaluationSummary = {
    available: boolean;
    message?: string | null;
    project_name?: string | null;
    total_queries: number;
    tool_usage_incorrect: number;
    frustrated_count: number;
    incorrect_rate?: number | null;
    frustration_rate?: number | null;
    frustrated_dataset_name?: string | null;
  };

  type EvaluationResultsResponse = {
    available: boolean;
    message?: string | null;
    user_frustration: EvaluationResult[];
    tool_usage: EvaluationResult[];
  };

  type FrustratedInteraction = {
    session_id: string;
    span_id?: string | null;
    prompt: string;
    response: string;
    scenario_type?: string | null;
    label: string;
    score?: number | null;
    explanation?: string | null;
  };

  type FrustratedInteractionsResponse = {
    available: boolean;
    message?: string | null;
    items: FrustratedInteraction[];
  };

  type ArchitectureContent = {
    available: boolean;
    message?: string | null;
    mermaid_diagram?: string | null;
    runtime_flow: string[];
    observability_flow: string[];
    evaluation_flow: string[];
    production_tradeoffs: string[];
    deck_url?: string | null;
    deck_path?: string | null;
  };

  type BoundaryEmbeddingPoint = {
    id: number;
    prompt: string;
    category: string;
    expected_behavior: string;
    response: string;
    session_id: string;
    success_label: string;
    success_score: number;
    tool_hints: string[];
    notes: string[];
    source: string;
    expected_refusal?: boolean | null;
    actual_refusal?: boolean | null;
    confusion_label?: string | null;
    coords: { x: number; y: number; z: number };
  };

  type BoundaryProjectionResponse = {
    available: boolean;
    message?: string | null;
    point?: BoundaryEmbeddingPoint | null;
  };

  type ProjectedBoundaryPoint = BoundaryEmbeddingPoint & {
    screenX: number;
    screenY: number;
    size: number;
    opacity: number;
    perspective: number;
    zIndex: number;
    depth: number;
    glow: number;
  };

  type LiveSessionRow = {
    sessionId: string;
    prompt: string;
    response: string;
    point: BoundaryEmbeddingPoint | null;
  };

  type BoundaryEmbeddingResponse = {
    available: boolean;
    message?: string | null;
    generated_at?: string | null;
    dataset_name?: string | null;
    embedding_model?: string | null;
    dimensions: number;
    summary: {
      total_prompts: number;
      worked: number;
      partial: number;
      failed: number;
      success_rate?: number | null;
    };
    points: BoundaryEmbeddingPoint[];
    category_similarity_matrix: {
      row: string;
      values: { column: string; similarity: number }[];
    }[];
  };

  type DiagramNode = { id: string; label: string };
  type DiagramEdge = { from: string; to: string; label: string };

  const API_BASE_URL = (import.meta.env.PUBLIC_API_BASE_URL || "http://localhost:8000").replace(/\/$/, "");
  const STORAGE_KEY = "travel-assistant-chat";
  const tabs: { id: DemoTab; label: string }[] = [
    { id: "chat", label: "Chat" },
    { id: "live", label: "Live" },
    { id: "traces", label: "Traces" },
    { id: "evaluation", label: "Evaluation" },
    { id: "embeddings", label: "Embeddings" },
    { id: "architecture", label: "Architecture" },
  ];

  let prompt = "";
  let selectedCorpusId = "evaluation";
  let corpusDownloadsOpen = false;
  let corporaManifest: CorpusManifest | null = null;
  let visiblePromptSuggestions: string[] = [];
  let messages: ChatMessage[] = [];
  let isLoading = false;
  let errorMessage = "";
  let healthStatus: "checking" | "up" | "down" = "checking";

  let overview: DemoOverview | null = null;
  let traces: TraceListItem[] = [];
  let visibleTraces: TraceListItem[] = [];
  let tracesAvailable = true;
  let tracesMessage = "";
  let traceDetail: TraceDetail | null = null;
  let evaluationSummary: EvaluationSummary | null = null;
  let evaluationResults: EvaluationResultsResponse | null = null;
  let frustratedInteractions: FrustratedInteraction[] = [];
  let visibleUserFrustration: EvaluationResult[] = [];
  let visibleToolUsage: EvaluationResult[] = [];
  let visibleFrustratedInteractions: FrustratedInteraction[] = [];
  let boundaryData: BoundaryEmbeddingResponse | null = null;
  let architecture: ArchitectureContent | null = null;
  let architectureDiagram: { nodes: DiagramNode[]; edges: DiagramEdge[] } = { nodes: [], edges: [] };
  let liveBoundaryPoints: BoundaryEmbeddingPoint[] = [];
  let projectedBoundaryPoints: ProjectedBoundaryPoint[] = [];
  let selectedBoundaryPointId: number | null = null;
  let selectedBoundaryPoint: ProjectedBoundaryPoint | null = null;
  let selectedBoundaryCategory = "all";
  let sceneRotationX = -0.55;
  let sceneRotationY = 0.9;
  let sceneZoom = 1.25;
  let sceneWidth = 1;
  let sceneHeight = 1;
  let sceneDragging = false;
  let lastPointerX = 0;
  let lastPointerY = 0;
  let allBoundaryPoints: BoundaryEmbeddingPoint[] = [];
  let corpusScopedBoundaryPoints: BoundaryEmbeddingPoint[] = [];
  let filteredBoundaryPoints: BoundaryEmbeddingPoint[] = [];
  let boundaryCategories: string[] = [];
  let categoryConfusionRows: Array<{
    category: string;
    total: number;
    tp: number;
    tn: number;
    fp: number;
    fn: number;
    accuracy: number;
  }> = [];
  let visibleCategoryRows: Array<{
    category: string;
    total: number;
    tp: number;
    tn: number;
    fp: number;
    fn: number;
    accuracy: number;
  }> = [];
  let liveSessionRows: LiveSessionRow[] = [];
  let cubeEdges: Array<{ x1: number; y1: number; x2: number; y2: number }> = [];

  let tracesLoading = false;
  let evaluationLoading = false;
  let boundaryLoading = false;
  let architectureLoading = false;

  function persistMessages() {
    if (!browser) return;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
  }

  function hydrateMessages() {
    if (!browser) return;
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return;
    try {
      messages = JSON.parse(stored) as ChatMessage[];
    } catch {
      localStorage.removeItem(STORAGE_KEY);
    }
  }

  async function fetchJson<T>(path: string): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${path}`);
    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`);
    }
    return (await response.json()) as T;
  }

  async function checkHealth() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      healthStatus = response.ok ? "up" : "down";
    } catch {
      healthStatus = "down";
    }
  }

  async function loadCorpora() {
    try {
      corporaManifest = await fetchJson<CorpusManifest>("/demo/corpora");
    } catch {
      corporaManifest = null;
    }
  }

  async function loadOverview() {
    try {
      overview = await fetchJson<DemoOverview>("/demo/overview");
    } catch {
      overview = null;
    }
  }

  async function loadTraces(targetSessionId?: string) {
    tracesLoading = true;
    try {
      const payload = await fetchJson<TraceListResponse>("/demo/traces");
      traces = payload.traces;
      tracesAvailable = payload.available;
      tracesMessage = payload.message || "";

      const targetTraceId =
        payload.traces.find((trace) => trace.session_id && trace.session_id === targetSessionId)?.trace_id ||
        payload.traces.find((trace) => trace.trace_id === get(selectedTraceId))?.trace_id ||
        payload.traces[0]?.trace_id ||
        null;

      if (targetTraceId) {
        await selectTrace(targetTraceId);
      } else {
        traceDetail = null;
        selectedTraceId.set(null);
      }
    } catch (error) {
      tracesAvailable = false;
      tracesMessage = error instanceof Error ? error.message : "Unable to load traces.";
      traces = [];
      traceDetail = null;
    } finally {
      tracesLoading = false;
    }
  }

  async function selectTrace(traceId: string) {
    selectedTraceId.set(traceId);
    try {
      traceDetail = await fetchJson<TraceDetail>(`/demo/traces/${traceId}`);
    } catch (error) {
      traceDetail = {
        available: false,
        message: error instanceof Error ? error.message : "Unable to load the trace.",
        spans: [],
        evaluations: [],
      };
    }
  }

  async function loadEvaluation() {
    evaluationLoading = true;
    try {
      const [summary, results, frustrated] = await Promise.all([
        fetchJson<EvaluationSummary>("/demo/evaluations/summary"),
        fetchJson<EvaluationResultsResponse>("/demo/evaluations/results"),
        fetchJson<FrustratedInteractionsResponse>("/demo/evaluations/frustrated"),
      ]);
      evaluationSummary = summary;
      evaluationResults = results;
      frustratedInteractions = frustrated.items;
    } catch {
      evaluationSummary = null;
      evaluationResults = null;
      frustratedInteractions = [];
    } finally {
      evaluationLoading = false;
    }
  }

  async function loadArchitecture() {
    architectureLoading = true;
    try {
      architecture = await fetchJson<ArchitectureContent>("/demo/architecture");
    } catch {
      architecture = null;
    } finally {
      architectureLoading = false;
    }
  }

  async function loadBoundaries() {
    boundaryLoading = true;
    try {
      boundaryData = await fetchJson<BoundaryEmbeddingResponse>("/demo/boundaries");
    } catch {
      boundaryData = null;
    } finally {
      boundaryLoading = false;
    }
  }

  function noteLabel(note: string) {
    if (note === "planning_only") return "Planning Only";
    if (note === "current_info") return "Current Info";
    if (note === "planning") return "Planning";
    return note.replaceAll("_", " ");
  }

  function renderMessageContent(content: string) {
    return content.replace(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g, "$1");
  }

  function applyPromptSuggestion(text: string) {
    prompt = text;
  }

  function selectCorpus(corpusId: string) {
    selectedCorpusId = corpusId;
    corpusDownloadsOpen = false;
    selectedBoundaryCategory = "all";
  }

  function toggleCorpusDownloads() {
    corpusDownloadsOpen = !corpusDownloadsOpen;
  }

  function percent(value?: number | null) {
    if (value === undefined || value === null) return "N/A";
    return `${Math.round(value * 100)}%`;
  }

  function accuracyPercent(incorrectRate?: number | null) {
    if (incorrectRate === undefined || incorrectRate === null) return "N/A";
    return `${Math.round((1 - incorrectRate) * 100)}%`;
  }

  function toneForLabel(label: string) {
    if (label === "frustrated" || label === "incorrect" || label === "fails") return "bad";
    if (label === "ok" || label === "correct" || label === "works") return "good";
    return "neutral";
  }

  function formatDate(value?: string | null) {
    if (!value) return "Unknown";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value;
    return date.toLocaleString();
  }

  function formatDuration(value?: number | null) {
    if (value === undefined || value === null) return "N/A";
    return `${Math.round(value)} ms`;
  }

  function categoryLabel(value: string) {
    return value.replaceAll("_", " ");
  }

  function selectBoundaryCategory(category: string) {
    selectedBoundaryCategory = category;
  }

  function jumpToLivePoint(sessionId: string) {
    const point = liveBoundaryPoints.find((entry) => entry.session_id === sessionId);
    if (!point) return;
    selectedBoundaryCategory = "live";
    selectedBoundaryPointId = point.id;
    selectedTab.set("embeddings");
  }

  function boundaryOutcomeText(label: string) {
    if (label === "works") return "Success / refused properly";
    if (label === "partial") return "Partial / weak refusal";
    if (label === "fails") return "Failure / did not refuse properly";
    return label;
  }

  function sourceLabel(source: string) {
    return source === "live" ? "Live Prompt" : "Corpus Prompt";
  }

  function confusionLabelText(label?: string | null) {
    if (label === "tp") return "True Positive";
    if (label === "tn") return "True Negative";
    if (label === "fp") return "False Positive";
    if (label === "fn") return "False Negative";
    return "Unclassified";
  }

  function confusionSummary(label?: string | null) {
    if (label === "tp") return "Should refuse, did refuse";
    if (label === "tn") return "Should answer, did answer";
    if (label === "fp") return "Should answer, refused instead";
    if (label === "fn") return "Should refuse, answered instead";
    return "The prompt has not been classified.";
  }

  function outlineClassForPoint(point: BoundaryEmbeddingPoint) {
    return point.confusion_label || "unknown";
  }

  function sourceClassForPoint(point: BoundaryEmbeddingPoint) {
    return point.source === "live" ? "live" : "corpus";
  }

  function stateClassForPoint(point: BoundaryEmbeddingPoint) {
    if (point.success_label === "works") return "works";
    if (point.success_label === "partial") return "partial";
    return "fails";
  }

  function truthCellTone(value: number) {
    if (value <= 0) return "neutral";
    return "truth";
  }

  function clamp(value: number, min: number, max: number) {
    return Math.min(max, Math.max(min, value));
  }

  function project3dPoint(
    x: number,
    y: number,
    z: number,
    rotationX: number,
    rotationY: number,
    zoom: number,
    viewportWidth: number,
    viewportHeight: number,
  ) {
    const cosY = Math.cos(rotationY);
    const sinY = Math.sin(rotationY);
    const rotatedX = x * cosY - z * sinY;
    const rotatedZ = x * sinY + z * cosY;

    const cosX = Math.cos(rotationX);
    const sinX = Math.sin(rotationX);
    const rotatedY = y * cosX - rotatedZ * sinX;
    const finalZ = y * sinX + rotatedZ * cosX;

    const depth = (finalZ + 1) / 2;
    const perspective = 0.65 + depth * 0.75;
    const baseScale = 31 * zoom * perspective;
    const aspectRatio = viewportWidth / Math.max(viewportHeight, 1);
    const horizontalScale = aspectRatio >= 1 ? baseScale / aspectRatio : baseScale;
    const verticalScale = aspectRatio <= 1 ? baseScale * aspectRatio : baseScale;

    return {
      screenX: 50 + rotatedX * horizontalScale,
      screenY: 50 - rotatedY * verticalScale,
      depth,
      perspective,
    };
  }

  function handleSceneMouseDown(event: MouseEvent) {
    sceneDragging = true;
    lastPointerX = event.clientX;
    lastPointerY = event.clientY;
  }

  function handleSceneWheel(event: WheelEvent) {
    event.preventDefault();
    const delta = event.deltaY < 0 ? 0.08 : -0.08;
    sceneZoom = clamp(sceneZoom + delta, 0.7, 1.8);
  }

  function handleWindowMouseMove(event: MouseEvent) {
    if (!sceneDragging) return;
    const deltaX = event.clientX - lastPointerX;
    const deltaY = event.clientY - lastPointerY;
    sceneRotationY -= deltaX * 0.01;
    sceneRotationX = clamp(sceneRotationX + deltaY * 0.01, -1.25, 1.25);
    lastPointerX = event.clientX;
    lastPointerY = event.clientY;
  }

  function handleWindowMouseUp() {
    sceneDragging = false;
  }

  function openTraceForSession(sessionId?: string) {
    if (!sessionId) return;
    selectedTab.set("traces");
    recentSessionId.set(sessionId);
    void loadTraces(sessionId);
  }

  async function projectPromptIntoBoundarySpace(payload: ChatUIResponse, promptText: string) {
    try {
      const response = await fetch(`${API_BASE_URL}/demo/boundaries/project`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: promptText,
          response: payload.response,
          session_id: payload.session_id,
          notes: payload.notes,
          tool_hints: payload.tool_hints,
        }),
      });
      if (!response.ok) {
        return;
      }
      const projection = (await response.json()) as BoundaryProjectionResponse;
      if (!projection.available || !projection.point) {
        return;
      }
      liveBoundaryPoints = [...liveBoundaryPoints, projection.point];
      selectedBoundaryPointId = projection.point.id;
    } catch {
      // Live embedding projection is a demo enhancement and should not block chat.
    }
  }

  async function submitPrompt() {
    const trimmedPrompt = prompt.trim();
    if (!trimmedPrompt || isLoading) return;

    errorMessage = "";
    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: trimmedPrompt,
    };
    messages = [...messages, userMessage];
    const currentPrompt = trimmedPrompt;
    prompt = "";
    persistMessages();
    isLoading = true;

    try {
      const response = await fetch(`${API_BASE_URL}/chat/ui`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: currentPrompt }),
      });

      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}`);
      }

      const payload = (await response.json()) as ChatUIResponse;
      messages = [
        ...messages,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: payload.response,
          sessionId: payload.session_id,
          sources: payload.sources,
          notes: payload.notes,
        },
      ];
      recentSessionId.set(payload.session_id);
      persistMessages();
      await projectPromptIntoBoundarySpace(payload, currentPrompt);
      await Promise.all([checkHealth(), loadOverview(), loadTraces(payload.session_id), loadEvaluation()]);
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : "The request failed.";
      prompt = currentPrompt;
      messages = messages.filter((message) => message.id !== userMessage.id);
      persistMessages();
    } finally {
      isLoading = false;
    }
  }

  function resetConversation() {
    prompt = "";
    messages = [];
    errorMessage = "";
    traces = [];
    traceDetail = null;
    liveBoundaryPoints = [];
    selectedBoundaryPointId = null;
    recentSessionId.set(null);
    selectedTraceId.set(null);
    selectedTab.set("chat");
    persistMessages();
  }

  function switchTab(tab: DemoTab) {
    selectedTab.set(tab);
    if (tab === "traces" && traces.length === 0) {
      void loadTraces();
    }
    if (tab === "evaluation" && !evaluationSummary && !evaluationLoading) {
      void loadEvaluation();
    }
    if (tab === "embeddings" && !boundaryData && !boundaryLoading) {
      void loadBoundaries();
    }
    if (tab === "architecture" && !architecture && !architectureLoading) {
      void loadArchitecture();
    }
  }

  function parseMermaid(diagram?: string | null): { nodes: DiagramNode[]; edges: DiagramEdge[] } {
    if (!diagram) return { nodes: [], edges: [] };
    const nodeMap = new Map<string, string>();
    const edges: DiagramEdge[] = [];

    for (const rawLine of diagram.split("\n")) {
      const line = rawLine.trim();
      if (!line || line.startsWith("flowchart")) continue;

      for (const match of line.matchAll(/([a-zA-Z0-9_]+)\["([^"]+)"\]/g)) {
        nodeMap.set(match[1], match[2]);
      }

      const edgeMatch = line.match(/([a-zA-Z0-9_]+)\s*-->\s*([a-zA-Z0-9_]+)/);
      if (edgeMatch) {
        const from = edgeMatch[1];
        const to = edgeMatch[2];
        edges.push({
          from,
          to,
          label: `${nodeMap.get(from) || from} -> ${nodeMap.get(to) || to}`,
        });
      }
    }

    const nodes = Array.from(nodeMap.entries()).map(([id, label]) => ({ id, label }));
    return { nodes, edges };
  }

  function selectedCorpus() {
    return corporaManifest?.corpora.find((corpus) => corpus.id === selectedCorpusId) ?? null;
  }

  function selectedCorpusPromptSet() {
    return new Set(selectedCorpus()?.prompts ?? []);
  }

  function selectedCorpusSessionSet() {
    return new Set(selectedCorpus()?.session_ids ?? []);
  }

  $: architectureDiagram = parseMermaid(architecture?.mermaid_diagram);
  $: visiblePromptSuggestions = (selectedCorpus()?.prompts ?? []).slice(0, 3);
  $: visibleTraces = (() => {
    const sessions = selectedCorpusSessionSet();
    return traces.filter((trace) => trace.session_id && sessions.has(trace.session_id));
  })();
  $: visibleUserFrustration = (() => {
    const sessions = selectedCorpusSessionSet();
    return (evaluationResults?.user_frustration ?? []).filter((row) => row.session_id && sessions.has(row.session_id));
  })();
  $: visibleToolUsage = (() => {
    const sessions = selectedCorpusSessionSet();
    return (evaluationResults?.tool_usage ?? []).filter((row) => row.session_id && sessions.has(row.session_id));
  })();
  $: visibleFrustratedInteractions = (() => {
    const sessions = selectedCorpusSessionSet();
    return frustratedInteractions.filter((row) => sessions.has(row.session_id));
  })();
  $: allBoundaryPoints = [...(boundaryData?.points ?? []), ...liveBoundaryPoints];
  $: corpusScopedBoundaryPoints =
    selectedCorpusId === "boundary"
      ? allBoundaryPoints
      : liveBoundaryPoints.filter((point) => !point.expected_refusal);
  $: filteredBoundaryPoints =
    selectedBoundaryCategory === "all"
      ? corpusScopedBoundaryPoints
      : selectedBoundaryCategory === "live"
        ? corpusScopedBoundaryPoints.filter((point) => point.source === "live")
        : corpusScopedBoundaryPoints.filter((point) => point.category === selectedBoundaryCategory);
  $: projectedBoundaryPoints =
    filteredBoundaryPoints
      .map((point) => {
        const projection = project3dPoint(
          point.coords.x,
          point.coords.y,
          point.coords.z,
          sceneRotationX,
          sceneRotationY,
          sceneZoom,
          sceneWidth,
          sceneHeight,
        );
        return {
          ...point,
          screenX: projection.screenX,
          screenY: projection.screenY,
          size: (point.source === "live" ? 12 : 10) + projection.depth * 12,
          opacity: 0.45 + projection.depth * 0.5,
          perspective: projection.perspective,
          zIndex: Math.round(projection.depth * 100),
          depth: projection.depth,
          glow: 10 + projection.depth * 22,
        };
      })
      .sort((left, right) => left.zIndex - right.zIndex);
  $: selectedBoundaryPoint = projectedBoundaryPoints.find((point) => point.id === selectedBoundaryPointId) ?? null;
  $: categoryConfusionRows = (() => {
    const grouped = new Map<
      string,
      { category: string; total: number; tp: number; tn: number; fp: number; fn: number; accuracy: number }
    >();
    for (const point of corpusScopedBoundaryPoints) {
      const current = grouped.get(point.category) ?? {
        category: point.category,
        total: 0,
        tp: 0,
        tn: 0,
        fp: 0,
        fn: 0,
        accuracy: 0,
      };
      current.total += 1;
      if (point.confusion_label === "tp") current.tp += 1;
      else if (point.confusion_label === "tn") current.tn += 1;
      else if (point.confusion_label === "fp") current.fp += 1;
      else if (point.confusion_label === "fn") current.fn += 1;
      grouped.set(point.category, current);
    }
    return Array.from(grouped.values())
      .map((row) => ({ ...row, accuracy: (row.tp + row.tn) / Math.max(row.total, 1) }))
      .sort((left, right) => (right.fp + right.fn) - (left.fp + left.fn) || left.category.localeCompare(right.category));
  })();
  $: boundaryCategories = categoryConfusionRows.map((row) => row.category).filter((category) => category !== "live_prompt");
  $: visibleCategoryRows =
    selectedBoundaryCategory === "all"
      ? categoryConfusionRows
      : selectedBoundaryCategory === "live"
        ? []
      : categoryConfusionRows.filter((row) => row.category === selectedBoundaryCategory);
  $: liveSessionRows = (() => {
    const rows: LiveSessionRow[] = [];
    const promptSet = selectedCorpusPromptSet();
    for (let index = 0; index < messages.length; index += 1) {
      const message = messages[index];
      if (message.role !== "assistant" || !message.sessionId) continue;
      const promptMessage = messages[index - 1];
      const promptText = promptMessage?.role === "user" ? promptMessage.content : "Prompt unavailable.";
      const point = liveBoundaryPoints.find((entry) => entry.session_id === message.sessionId) ?? null;
      if (selectedCorpusId === "boundary" && point && !point.expected_refusal) continue;
      if (selectedCorpusId === "evaluation" && point?.expected_refusal) continue;
      if (selectedCorpusId === "evaluation" && promptSet.size > 0 && promptText !== "Prompt unavailable." && !promptSet.has(promptText) && point === null) {
        continue;
      }
      rows.push({
        sessionId: message.sessionId,
        prompt: promptText,
        response: message.content,
        point,
      });
    }
    return rows.reverse();
  })();
  $: if (selectedBoundaryPointId !== null && !filteredBoundaryPoints.some((point) => point.id === selectedBoundaryPointId)) {
    selectedBoundaryPointId = null;
  }
  $: cubeEdges = (() => {
    const corners = [
      { id: "000", x: -1, y: -1, z: -1 },
      { id: "001", x: -1, y: -1, z: 1 },
      { id: "010", x: -1, y: 1, z: -1 },
      { id: "011", x: -1, y: 1, z: 1 },
      { id: "100", x: 1, y: -1, z: -1 },
      { id: "101", x: 1, y: -1, z: 1 },
      { id: "110", x: 1, y: 1, z: -1 },
      { id: "111", x: 1, y: 1, z: 1 },
    ];
    const edgePairs = [
      ["000", "001"], ["000", "010"], ["000", "100"],
      ["001", "011"], ["001", "101"],
      ["010", "011"], ["010", "110"],
      ["011", "111"],
      ["100", "101"], ["100", "110"],
      ["101", "111"],
      ["110", "111"],
    ];
    const projected = new Map(
      corners.map((corner) => [
        corner.id,
        project3dPoint(corner.x, corner.y, corner.z, sceneRotationX, sceneRotationY, sceneZoom, sceneWidth, sceneHeight),
      ]),
    );
    return edgePairs.map(([from, to]) => {
      const start = projected.get(from)!;
      const end = projected.get(to)!;
      return { x1: start.screenX, y1: start.screenY, x2: end.screenX, y2: end.screenY };
    });
  })();

  onMount(async () => {
    hydrateMessages();
    await Promise.all([checkHealth(), loadCorpora(), loadOverview(), loadTraces(), loadEvaluation(), loadBoundaries(), loadArchitecture()]);
  });
</script>

<svelte:head>
  <title>Travel Assistant</title>
  <meta
    name="description"
    content="Travel assistant with chat, Phoenix traces, evaluation results, and architecture context."
  />
</svelte:head>

<svelte:window on:mousemove={handleWindowMouseMove} on:mouseup={handleWindowMouseUp} />

<div class="app-shell">
  <div class="chat-shell">
    <header class="app-header">
      <div>
        <h1 class="chat-title">Travel Assistant</h1>
        <p class="chat-subtitle">Plan trips, inspect traces, review evaluations, and explain the system from one place.</p>
      </div>

      <div class="header-actions">
        <span class:down={healthStatus === "down"} class="status-pill">
          {#if healthStatus === "checking"}
            Connecting
          {:else if healthStatus === "up"}
            Online
          {:else}
            Offline
          {/if}
        </span>
        <button class="action subtle" type="button" on:click={resetConversation} disabled={isLoading}>
          Reset
        </button>
      </div>
    </header>

    <div class="corpus-bar">
      <div class="corpus-tabs" aria-label="Corpus filters">
        {#each corporaManifest?.corpora ?? [] as corpus}
          <button
            class:active={selectedCorpusId === corpus.id}
            class="tab-button corpus-pill"
            type="button"
            on:click={() => selectCorpus(corpus.id)}
          >
            {corpus.label}
          </button>
        {/each}
        <button
          class:active={corpusDownloadsOpen}
          class="tab-button corpus-pill"
          type="button"
          on:click={toggleCorpusDownloads}
        >
          Download
        </button>
      </div>

      {#if corpusDownloadsOpen}
        <div class="download-row">
          {#each corporaManifest?.corpora ?? [] as corpus}
            <a class="filter-chip download-chip" href={`${API_BASE_URL}${corpus.download_url}`} download>
              {corpus.label} JSON
            </a>
          {/each}
        </div>
      {/if}
    </div>

    <nav class="tab-bar" aria-label="Demo sections">
      {#each tabs as tab}
        <button
          class:active={$selectedTab === tab.id}
          class="tab-button"
          type="button"
          on:click={() => switchTab(tab.id)}
        >
          {tab.label}
        </button>
      {/each}
    </nav>

    {#if overview?.message}
      <p class="inline-message">{overview.message}</p>
    {/if}

    <main class="tab-panel">
      {#if $selectedTab === "chat"}
        <section class="chat-view">
          <div class="transcript">
            {#if messages.length === 0}
              <div class="empty-state panel">
                <div class="empty-copy">
                  <h2>Ask for an itinerary, a travel update, or a destination idea.</h2>
                </div>

                <div class="prompt-row">
                  {#each visiblePromptSuggestions as suggestion}
                    <button class="chip" type="button" on:click={() => applyPromptSuggestion(suggestion)}>
                      {suggestion}
                    </button>
                  {/each}
                </div>
              </div>
            {:else}
              {#each messages as message}
                <article class:assistant-card={message.role === "assistant"} class:user-card={message.role === "user"} class="bubble">
                  <div class="bubble-meta">
                    <span>{message.role === "user" ? "You" : "Assistant"}</span>
                    {#if message.role === "assistant" && message.sessionId}
                      <button class="text-action" type="button" on:click={() => openTraceForSession(message.sessionId)}>
                        Trace
                      </button>
                    {/if}
                  </div>

                  <div class="message-copy">{renderMessageContent(message.content)}</div>

                  {#if message.role === "assistant" && ((message.notes?.length ?? 0) > 0 || (message.sources?.length ?? 0) > 0)}
                    <div class="meta-stack">
                      {#if (message.notes?.length ?? 0) > 0}
                        <div class="meta-row">
                          {#each message.notes ?? [] as note}
                            <span class="note-badge">{noteLabel(note)}</span>
                          {/each}
                        </div>
                      {/if}

                      {#if (message.sources?.length ?? 0) > 0}
                        <div class="source-list">
                          {#each message.sources ?? [] as source}
                            <a href={source.url} target="_blank" rel="noreferrer">{source.label || source.url}</a>
                          {/each}
                        </div>
                      {/if}
                    </div>
                  {/if}
                </article>
              {/each}

              {#if isLoading}
                <article class="bubble assistant-card">
                  <div class="bubble-meta">
                    <span>Assistant</span>
                    <span>Thinking</span>
                  </div>
                  <div class="message-copy">Working through the request.</div>
                </article>
              {/if}
            {/if}
          </div>

          <section class="composer-panel">
            <form class="composer" on:submit|preventDefault={submitPrompt}>
              <textarea
                bind:value={prompt}
                placeholder="Ask for a travel plan, current travel information, or an unsupported booking request."
              ></textarea>

              <div class="composer-actions">
                <div class="footer-note">
                  {#if errorMessage}
                    <span class="status-pill down">Error: {errorMessage}</span>
                  {/if}
                </div>

                <button class="action primary" type="submit" disabled={isLoading || !prompt.trim()}>
                  {#if isLoading}Sending...{:else}Send{/if}
                </button>
              </div>
            </form>
          </section>
        </section>
      {:else if $selectedTab === "live"}
        <section class="stack-layout">
          {#if liveSessionRows.length === 0}
            <div class="empty-panel panel">
              <h2>No live prompts yet</h2>
              <p class="muted">Send a prompt in Chat and it will appear here with its live boundary classification and trace link.</p>
            </div>
          {:else}
            <div class="result-stack">
              {#each liveSessionRows as row}
                <article class={`result-card ${toneForLabel(row.point?.success_label || "neutral")}`}>
                  <div class="result-header">
                    <strong>{row.point ? boundaryOutcomeText(row.point.success_label) : "Pending classification"}</strong>
                    <span class="muted">{row.point ? confusionLabelText(row.point.confusion_label) : "Awaiting projection"}</span>
                  </div>
                  <p><strong>Prompt:</strong> {row.prompt}</p>
                  <p><strong>Response:</strong> {renderMessageContent(row.response)}</p>
                  {#if row.point}
                    <div class="badge-row">
                      <span class={`status-pill ${toneForLabel(row.point.success_label) === "bad" ? "down" : ""}`}>
                        {confusionSummary(row.point.confusion_label)}
                      </span>
                      {#if row.point.tool_hints.length > 0}
                        <span class="note-badge">{row.point.tool_hints.join(", ")}</span>
                      {/if}
                    </div>
                  {/if}
                  <div class="popup-actions">
                    <button class="text-action" type="button" on:click={() => openTraceForSession(row.sessionId)}>
                      Open Trace
                    </button>
                    {#if row.point}
                      <button class="text-action" type="button" on:click={() => jumpToLivePoint(row.sessionId)}>
                        Show In Embeddings
                      </button>
                    {/if}
                  </div>
                </article>
              {/each}
            </div>
          {/if}
        </section>
      {:else if $selectedTab === "traces"}
        <section class="split-layout">
          <article class="panel list-panel">
            <div class="section-header">
              <h2>Recent Traces</h2>
              {#if tracesLoading}<span class="status-pill">Refreshing</span>{/if}
            </div>

            {#if tracesMessage}
              <p class="inline-message">{tracesMessage}</p>
            {/if}

            {#if visibleTraces.length === 0}
              <p class="muted">No traces are available yet.</p>
            {:else}
              <div class="trace-list">
                {#each visibleTraces as trace}
                  <button
                    class:active={$selectedTraceId === trace.trace_id}
                    class:highlight={trace.session_id && trace.session_id === $recentSessionId}
                    class="trace-row"
                    type="button"
                    on:click={() => selectTrace(trace.trace_id)}
                  >
                    <div class="trace-row-top">
                      <strong>{trace.prompt_preview || trace.name}</strong>
                      <span class="muted">{trace.span_count} spans</span>
                    </div>
                    <div class="trace-row-bottom">
                      <span>{formatDate(trace.start_time)}</span>
                      <div class="badge-row">
                        {#each trace.tool_names as toolName}
                          <span class="tool-badge">{toolName.replace("search_", "")}</span>
                        {/each}
                      </div>
                    </div>
                  </button>
                {/each}
              </div>
            {/if}
          </article>

          <article class="panel detail-panel">
            {#if traceDetail?.trace}
              <div class="section-header">
                <h2>Trace Detail</h2>
                {#if traceDetail.trace.phoenix_url}
                  <a class="action-link" href={traceDetail.trace.phoenix_url} target="_blank" rel="noreferrer">Open Phoenix</a>
                {/if}
              </div>

              <div class="trace-summary-card">
                <strong>{traceDetail.trace.prompt_preview || traceDetail.trace.name}</strong>
                <div class="trace-meta-grid">
                  <span>Status: {traceDetail.trace.status_code || "Unknown"}</span>
                  <span>Started: {formatDate(traceDetail.trace.start_time)}</span>
                  <span>LLM spans: {traceDetail.trace.llm_span_count}</span>
                  <span>Tools: {traceDetail.trace.tool_names.join(", ") || "None"}</span>
                </div>
              </div>

              {#if traceDetail.evaluations.length > 0}
                <div class="evaluation-strip">
                  {#each traceDetail.evaluations as evaluation}
                    <article class={`mini-card ${toneForLabel(evaluation.label)}`}>
                      <span class="eyebrow">{evaluation.kind.replaceAll("_", " ")}</span>
                      <strong>{evaluation.label}</strong>
                      {#if evaluation.explanation}
                        <p>{evaluation.explanation}</p>
                      {/if}
                    </article>
                  {/each}
                </div>
              {/if}

              <div class="span-stack">
                {#each traceDetail.spans as span}
                  <article class="span-card">
                    <div class="span-header">
                      <div>
                        <strong>{span.tool_name || span.name}</strong>
                        <span class="muted">{span.span_kind || "Span"} · {formatDuration(span.duration_ms)}</span>
                      </div>
                      <span class:down={span.status_code && span.status_code !== "OK"} class="status-pill">
                        {span.status_code || "Unknown"}
                      </span>
                    </div>

                    {#if span.input_preview}
                      <p><strong>Input:</strong> {span.input_preview}</p>
                    {/if}
                    {#if span.output_preview}
                      <p><strong>Output:</strong> {span.output_preview}</p>
                    {/if}
                    {#if span.error_message}
                      <p class="error-copy"><strong>Error:</strong> {span.error_message}</p>
                    {/if}
                  </article>
                {/each}
              </div>
            {:else}
              <div class="empty-panel">
                <h2>Select a trace</h2>
                <p class="muted">{traceDetail?.message || "Choose a trace from the list to inspect its spans and evaluations."}</p>
              </div>
            {/if}
          </article>
        </section>
      {:else if $selectedTab === "evaluation"}
        <section class="stack-layout">
          {#if evaluationLoading}
            <div class="section-header">
              <span class="status-pill">Refreshing</span>
            </div>
          {/if}

          {#if !evaluationSummary}
            <p class="muted">Evaluation artifacts are not available.</p>
          {/if}

          <div class="split-layout">
            <article class="panel">
              <div class="section-header">
                <h2>User Frustration</h2>
              </div>

              {#if visibleUserFrustration.length > 0}
                <div class="result-stack">
                  {#each visibleUserFrustration as result}
                    <article class={`result-card ${toneForLabel(result.label)}`}>
                      <div class="result-header">
                        <strong>{result.label}</strong>
                        <span class="muted">{result.scenario_type || "Scenario"}</span>
                      </div>
                      <p>{result.prompt || "No prompt available."}</p>
                      {#if result.explanation}
                        <p class="muted">{result.explanation}</p>
                      {/if}
                    </article>
                  {/each}
                </div>
              {:else}
                <p class="muted">No user-frustration rows are available.</p>
              {/if}
            </article>

            <article class="panel">
              <div class="section-header">
                <h2>Tool Usage</h2>
              </div>

              {#if visibleToolUsage.length > 0}
                <div class="result-stack">
                  {#each visibleToolUsage as result}
                    <article class={`result-card ${toneForLabel(result.label)}`}>
                      <div class="result-header">
                        <strong>{result.label}</strong>
                        <span class="muted">{result.observed_tool_names.join(", ") || "No tools"}</span>
                      </div>
                      <p>{result.prompt || "No prompt available."}</p>
                      {#if result.explanation}
                        <p class="muted">{result.explanation}</p>
                      {/if}
                    </article>
                  {/each}
                </div>
              {:else}
                <p class="muted">No tool-usage rows are available.</p>
              {/if}
            </article>
          </div>

          <article class="panel">
            <div class="section-header">
              <h2>Frustrated Interactions</h2>
            </div>

            {#if visibleFrustratedInteractions.length > 0}
              <div class="result-stack">
                {#each visibleFrustratedInteractions as item}
                  <article class="result-card bad">
                    <div class="result-header">
                      <strong>{item.label}</strong>
                      <span class="muted">{item.scenario_type || "Scenario"}</span>
                    </div>
                    <p><strong>Prompt:</strong> {item.prompt}</p>
                    <p><strong>Response:</strong> {renderMessageContent(item.response)}</p>
                    {#if item.explanation}
                      <p class="muted">{item.explanation}</p>
                    {/if}
                  </article>
                {/each}
              </div>
            {:else}
              <p class="muted">No frustrated interactions were captured.</p>
            {/if}
          </article>
        </section>
      {:else if $selectedTab === "embeddings"}
        <section class="stack-layout">
          <article class="panel">
            {#if boundaryLoading}
              <div class="section-header">
                <span class="status-pill">Refreshing</span>
              </div>
            {/if}

            {#if boundaryData?.available}
              <article class="panel embedding-scene-panel">
                <div class="section-header">
                  <span class="muted">
                    {boundaryData.embedding_model} · {boundaryData.dimensions}D · {liveBoundaryPoints.length} live prompt{liveBoundaryPoints.length === 1 ? "" : "s"} this session
                  </span>
                </div>

                <div class="filter-row">
                  <button
                    class:active={selectedBoundaryCategory === "all"}
                    class="filter-chip"
                    type="button"
                    on:click={() => selectBoundaryCategory("all")}
                  >
                    All
                  </button>
                  <button
                    class:active={selectedBoundaryCategory === "live"}
                    class="filter-chip"
                    type="button"
                    on:click={() => selectBoundaryCategory("live")}
                  >
                    Live
                  </button>
                  {#each boundaryCategories as category}
                    <button
                      class:active={selectedBoundaryCategory === category}
                      class="filter-chip"
                      type="button"
                      on:click={() => selectBoundaryCategory(category)}
                    >
                      {categoryLabel(category)}
                    </button>
                  {/each}
                </div>

                <!-- svelte-ignore a11y_no_static_element_interactions -->
                <div
                  class:dragging={sceneDragging}
                  class="embedding-scene"
                  bind:clientWidth={sceneWidth}
                  bind:clientHeight={sceneHeight}
                  on:mousedown={handleSceneMouseDown}
                  on:wheel|preventDefault={handleSceneWheel}
                >
                  <div class="embedding-cube">
                    <svg class="embedding-wireframe" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
                      {#each cubeEdges as edge}
                        <line x1={edge.x1} y1={edge.y1} x2={edge.x2} y2={edge.y2}></line>
                      {/each}
                    </svg>

                    {#each projectedBoundaryPoints as point (point.id)}
                      <button
                        class:active={selectedBoundaryPointId === point.id}
                        class="embedding-point"
                        data-source={sourceClassForPoint(point)}
                        data-state={stateClassForPoint(point)}
                        data-outline={outlineClassForPoint(point)}
                        type="button"
                        style={`left:${point.screenX}%; top:${point.screenY}%; width:${point.size}px; height:${point.size}px; opacity:${point.opacity}; z-index:${point.zIndex}; --depth-glow:${point.glow}px; --depth-alpha:${0.18 + point.depth * 0.3};`}
                        title={point.prompt}
                        on:click={() => {
                          selectedBoundaryPointId = point.id;
                        }}
                      ></button>
                    {/each}
                  </div>
                </div>

                <p class="muted">
                  Drag to rotate. Scroll to zoom. Border color shows TP/TN/FP/FN, core shape shows works or fails, and live prompts get the brighter outer glow.
                </p>
              </article>

              <article class="panel">
                <div class="embedding-legend-grid">
                  <div class="legend-block">
                    <h3>Source</h3>
                    <div class="legend-list">
                      <div class="legend-item"><span class="legend-dot" data-source="corpus" data-state="works"></span><span>Corpus prompt</span></div>
                      <div class="legend-item"><span class="legend-dot" data-source="live" data-state="works"></span><span>Live prompt</span></div>
                    </div>
                  </div>

                  <div class="legend-block">
                    <h3>Core State</h3>
                    <div class="legend-list">
                      <div class="legend-item"><span class="legend-dot" data-source="corpus" data-state="works"></span><span>Worked: solid core</span></div>
                      <div class="legend-item"><span class="legend-dot" data-source="corpus" data-state="partial"></span><span>Partial: split core</span></div>
                      <div class="legend-item"><span class="legend-dot" data-source="corpus" data-state="fails"></span><span>Failed: hollow core</span></div>
                    </div>
                  </div>

                  <div class="legend-block">
                    <h3>Border Color</h3>
                    <div class="legend-list">
                      <div class="legend-item"><span class="legend-dot" data-source="corpus" data-state="works" data-outline="tp"></span><span>True positive: should refuse, did refuse</span></div>
                      <div class="legend-item"><span class="legend-dot" data-source="corpus" data-state="works" data-outline="tn"></span><span>True negative: should answer, did answer</span></div>
                      <div class="legend-item"><span class="legend-dot" data-source="corpus" data-state="works" data-outline="fp"></span><span>False positive: refused when it should answer</span></div>
                      <div class="legend-item"><span class="legend-dot" data-source="corpus" data-state="works" data-outline="fn"></span><span>False negative: answered when it should refuse</span></div>
                    </div>
                  </div>
                </div>
              </article>

              <article class="panel">
                {#if selectedBoundaryPoint}
                  <div class="embedding-detail-grid">
                    <div class={`embedding-popup static ${toneForLabel(selectedBoundaryPoint.success_label)}`}>
                      <div class="result-header">
                        <strong>{boundaryOutcomeText(selectedBoundaryPoint.success_label)}</strong>
                        <span class="muted">{sourceLabel(selectedBoundaryPoint.source)}</span>
                      </div>
                      <p>{selectedBoundaryPoint.prompt}</p>
                      <p class="muted">{renderMessageContent(selectedBoundaryPoint.response)}</p>
                      <div class="popup-actions">
                        <button class="text-action" type="button" on:click={() => openTraceForSession(selectedBoundaryPoint.session_id)}>
                          Open Trace
                        </button>
                        <button class="text-action" type="button" on:click={() => (selectedBoundaryPointId = null)}>
                          Clear
                        </button>
                      </div>
                    </div>

                    <div class="mini-card">
                      <div class="badge-row">
                        <span class={`status-pill ${toneForLabel(selectedBoundaryPoint.success_label) === "bad" ? "down" : ""}`}>
                          {confusionLabelText(selectedBoundaryPoint.confusion_label)}
                        </span>
                        <span class="note-badge">{categoryLabel(selectedBoundaryPoint.category)}</span>
                      </div>
                      <p>{confusionSummary(selectedBoundaryPoint.confusion_label)}</p>
                      <div class="detail-list">
                        <div><strong>Expected refusal:</strong> {selectedBoundaryPoint.expected_refusal ? "Yes" : "No"}</div>
                        <div><strong>Actual refusal:</strong> {selectedBoundaryPoint.actual_refusal ? "Yes" : "No"}</div>
                        <div><strong>Source:</strong> {sourceLabel(selectedBoundaryPoint.source)}</div>
                        <div><strong>Tools:</strong> {selectedBoundaryPoint.tool_hints.length > 0 ? selectedBoundaryPoint.tool_hints.join(", ") : "None"}</div>
                      </div>
                    </div>
                  </div>
                {:else}
                  <div class="empty-panel">
                    <h2>Pick a point</h2>
                    <p class="muted">Select any point in the 3D space to inspect the prompt, its TP/TN/FP/FN classification, and its trace link.</p>
                  </div>
                {/if}
              </article>

              <article class="panel">
                <div class="matrix-table">
                  {#if visibleCategoryRows.length > 0}
                    <div class="matrix-header-row">
                      <span>Category</span>
                      <span>TP</span>
                      <span>TN</span>
                      <span>FP</span>
                      <span>FN</span>
                      <span>Accuracy</span>
                    </div>

                    {#each visibleCategoryRows as row}
                      <div class="matrix-row">
                        <strong>{categoryLabel(row.category)}</strong>
                        <span class={`matrix-cell ${truthCellTone(row.tp)}`} style={`background: rgba(230, 117, 255, ${0.14 + row.tp / Math.max(row.total, 1) * 0.56});`}>
                          {row.tp}/{row.total}
                        </span>
                        <span class={`matrix-cell ${truthCellTone(row.tn)}`} style={`background: rgba(76, 220, 196, ${0.14 + row.tn / Math.max(row.total, 1) * 0.56});`}>
                          {row.tn}/{row.total}
                        </span>
                        <span class={`matrix-cell ${row.fp > 0 ? "bad" : "neutral"}`} style={`background: rgba(255, 201, 84, ${0.14 + row.fp / Math.max(row.total, 1) * 0.56});`}>
                          {row.fp}/{row.total}
                        </span>
                        <span class={`matrix-cell ${row.fn > 0 ? "bad" : "neutral"}`} style={`background: rgba(255, 120, 120, ${0.14 + row.fn / Math.max(row.total, 1) * 0.56});`}>
                          {row.fn}/{row.total}
                        </span>
                        <span class="matrix-cell rate" style={`background: rgba(166, 236, 255, ${0.12 + row.accuracy * 0.5});`}>
                          {percent(row.accuracy)}
                        </span>
                      </div>
                    {/each}
                  {/if}
                </div>
              </article>

              <article class="panel">
                <div class="result-stack">
                  {#each filteredBoundaryPoints.filter((point) => point.success_label !== "works") as point}
                    <article class={`result-card ${toneForLabel(point.success_label)}`}>
                      <div class="result-header">
                        <strong>{boundaryOutcomeText(point.success_label)}</strong>
                        <span class="muted">{categoryLabel(point.category)} · {confusionLabelText(point.confusion_label)}</span>
                      </div>
                      <p>{point.prompt}</p>
                      <p class="muted">{renderMessageContent(point.response)}</p>
                    </article>
                  {/each}
                </div>
              </article>
            {:else}
              <p class="muted">{boundaryData?.message || "Boundary embedding data is not available yet."}</p>
            {/if}
          </article>
        </section>
      {:else if $selectedTab === "architecture"}
        <section class="stack-layout">
          <article class="panel">
            <div class="section-header">
              <h2>Production Architecture</h2>
              {#if architecture?.deck_url}
                <a class="action-link" href={architecture.deck_url} target="_blank" rel="noreferrer">Open Presentation</a>
              {/if}
            </div>

            {#if architecture?.mermaid_diagram}
              <div class="diagram-board">
                <div class="diagram-node-grid">
                  {#each architectureDiagram.nodes as node}
                    <article class="diagram-node">{node.label}</article>
                  {/each}
                </div>
                <div class="diagram-edges">
                  {#each architectureDiagram.edges as edge}
                    <span>{edge.label}</span>
                  {/each}
                </div>
              </div>
            {:else}
              <p class="muted">Architecture diagram content is unavailable.</p>
            {/if}
          </article>

          <div class="split-layout">
            <article class="panel">
              <div class="section-header">
                <h2>Runtime Flow</h2>
              </div>
              <ul class="bullet-list">
                {#each architecture?.runtime_flow ?? [] as item}
                  <li>{item}</li>
                {/each}
              </ul>
            </article>

            <article class="panel">
              <div class="section-header">
                <h2>Observability</h2>
              </div>
              <ul class="bullet-list">
                {#each architecture?.observability_flow ?? [] as item}
                  <li>{item}</li>
                {/each}
              </ul>
            </article>
          </div>

          <div class="split-layout">
            <article class="panel">
              <div class="section-header">
                <h2>Evaluation Loop</h2>
              </div>
              <ul class="bullet-list">
                {#each architecture?.evaluation_flow ?? [] as item}
                  <li>{item}</li>
                {/each}
              </ul>
            </article>

            <article class="panel">
              <div class="section-header">
                <h2>Operational Tradeoffs</h2>
              </div>
              <ul class="bullet-list">
                {#each architecture?.production_tradeoffs ?? [] as item}
                  <li>{item}</li>
                {/each}
              </ul>
            </article>
          </div>
        </section>
      {/if}
    </main>
  </div>
</div>
