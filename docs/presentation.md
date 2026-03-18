# Presentation Outline

## Slide 1: Objective and Rubric
- Travel assistant assessment goals
- What the starter repo provided
- What was added

## Slide 2: Baseline vs Final Architecture
- Original two-file FastAPI + LangGraph setup
- Refactored production-shaped package

## Slide 3: Agent Workflow
- User request enters `/chat`
- LangGraph LLM node chooses between `search_attractions` and `search_web`
- Tool results loop back into the model for final synthesis

## Slide 4: New Structured Tool
- Why attractions were chosen
- Input schema, output schema, normalization strategy
- Example structured payload

## Slide 5: Observability
- Phoenix local deployment with Docker
- `phoenix.otel.register(...)`
- OpenInference + LangChain instrumentation

## Slide 6: OpenTelemetry, OpenInference, Traces, and Spans
- Trace = one end-to-end user interaction
- Span = one step inside that interaction
- LLM spans vs tool spans

## Slide 7: Query Experiment Design
- 10 prompts across planning, current info, and unsupported booking
- Why frustrated interactions were included intentionally

## Slide 8: Evaluation Methodology
- Built-in user frustration evaluation on traces
- Custom `tool_usage_correctness` metric from expected vs observed tool routing

## Slide 9: Debugging Insights
- What the traces show when the wrong tool is chosen
- How tool spans help isolate prompt or routing issues

## Slide 10: Production Architecture
- Stateless API, cache, async workers, Phoenix, storage
- Scaling and latency strategy

## Slide 11: Cost and Reliability
- Model sizing, caching, retries, timeouts, sampling
- Why evaluation runs are asynchronous

## Slide 12: Live Demo
- Attraction planning query
- Current-information query
- Unsupported booking query
- Phoenix trace and evaluation annotations
