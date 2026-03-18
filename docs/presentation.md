# Presentation Outline

## Story Arc
- Product
- Starting point
- What changed
- One request through runtime, tracing, evaluation, and production

## Slide Flow
- Product: what the assistant does and the Chicago backbone request
- Starting Point: what the starter repo could do and what it could not explain
- What Changed: planning tool, tracing, evaluations, production shape
- Runtime Architecture: the main request flow through `/chat`, LangGraph, tools, and final synthesis
- Graph Decision Loop: how tool calls loop until the model stops requesting them
- Tool Contracts: planning, current info, and honest refusal for transactions
- Structured Tool Output: why normalized evidence matters
- Observe: why one request needs to become one trace
- One Request As A Trace: root trace and child spans for the Chicago flow
- Trace Evidence: 10 traces, 137 spans, and what those numbers mean
- Evaluate: why traces make scoring possible
- Test Corpus: planning, current info, unsupported booking
- Evaluation Pipeline: export, score, annotate, collect failures
- User Frustration: two frustrated interactions and the product lesson
- Tool Routing: expected first tool vs observed first tool
- Debugging Example: the Tokyo nightlife misroute
- Scale: moving from laptop demo to service architecture
- Production Architecture: serving, dependencies, observability, storage
- Operational Tradeoffs: latency, cost, reliability
- Live Proof: three queries plus Phoenix annotations
- Outcome: what was built, what was learned, and submission proof
