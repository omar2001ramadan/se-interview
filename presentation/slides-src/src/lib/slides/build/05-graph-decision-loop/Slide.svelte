<script lang="ts">
  import SlideFrame from "$lib/components/SlideFrame.svelte";
  import HeadingRow from "$lib/components/HeadingRow.svelte";
  import CodeCard from "$lib/components/CodeCard.svelte";
  import DiagramCard from "$lib/components/DiagramCard.svelte";
  import Panel from "$lib/components/Panel.svelte";
  import LoopStateDiagram from "$lib/diagrams/LoopStateDiagram.svelte";

  const code = `graph_builder.add_edge(START, "llm_call")
graph_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", END],
)
graph_builder.add_edge("tool_node", "llm_call")`;

</script>

<SlideFrame>
  <HeadingRow
    eyebrow="Build"
    title="Graph Decision Loop"
    support="Inside the runtime architecture, the LangGraph loop keeps calling the model until it stops requesting tools."
  />

  <div class="loop-grid">
    <DiagramCard label="Decision Flow" className="loop-card">
      <div class="loop-graphic-stage">
        <LoopStateDiagram />

        <Panel className="soft loop-stage stage-left">
          <small class="label">LLM Call</small>
          <p>The first model call decides whether a tool is needed.</p>
        </Panel>

        <Panel className="soft loop-stage stage-middle">
          <small class="label">Tool Node</small>
          <p>If a tool is called, its JSON output is written back into the conversation.</p>
        </Panel>

        <Panel className="soft loop-stage stage-right">
          <small class="label">End</small>
          <p>The loop ends only when the model stops emitting tool calls.</p>
        </Panel>
      </div>
    </DiagramCard>

    <CodeCard
      label="LangGraph"
      {code}
      foot="Small topology, explicit routing, readable traces."
      className="loop-code-card"
    />
  </div>
</SlideFrame>

<style>
  .loop-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.28fr) minmax(380px, 0.72fr);
    gap: 22px;
    min-height: 580px;
  }

  :global(.loop-card),
  :global(.loop-code-card) {
    min-height: 580px;
    min-width: 0;
  }

  :global(.loop-code-card) {
    display: flex;
    flex-direction: column;
    gap: 18px;
    overflow: hidden;
  }

  :global(.loop-code-card pre) {
    display: block;
    box-sizing: border-box;
    width: 100%;
    max-width: 100%;
    margin: 0;
    font-size: 0.86rem;
    line-height: 1.5;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    word-break: break-word;
    overflow-x: hidden;
    overflow-y: auto;
  }

  :global(.loop-code-card .code-foot) {
    max-width: 100%;
  }

  .loop-graphic-stage {
    position: relative;
    min-height: 520px;
    padding: 6px 18px 12px;
  }

  :global(.loop-stage) {
    position: absolute;
    z-index: 2;
    width: 250px;
  }

  :global(.stage-left) {
    left: 10px;
    bottom: 18px;
  }

  :global(.stage-middle) {
    left: 50%;
    bottom: 18px;
    transform: translateX(-50%);
  }

  :global(.stage-right) {
    right: 10px;
    bottom: 18px;
  }

</style>
