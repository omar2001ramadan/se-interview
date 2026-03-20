<script lang="ts">
  import SlideFrame from "$lib/components/SlideFrame.svelte";
  import HeadingRow from "$lib/components/HeadingRow.svelte";
  import DiagramCard from "$lib/components/DiagramCard.svelte";
  import Panel from "$lib/components/Panel.svelte";
  import TraceDiagram from "$lib/diagrams/TraceDiagram.svelte";
</script>

<SlideFrame>
  <HeadingRow
    eyebrow="Observe"
    title="One Request As A Trace"
    support="This is the same request flow from the runtime slide, now seen through Phoenix as a root trace with child spans."
  />

  <div class="split trace-explainer">
    <DiagramCard label="Trace View" className="trace-diagram-card">
      <TraceDiagram />
    </DiagramCard>

    <div class="stack glossary-stack">
      <Panel className="story-accent">
        <small class="label">Trace</small>
        <h4>One request and everything it triggered</h4>
        <p>The root trace holds the full Chicago conversation path from API entry to final response.</p>
      </Panel>
      <Panel className="story-accent pink">
        <small class="label">Span</small>
        <h4>One measurable step inside the trace</h4>
        <p>LLM calls, tool calls, and final synthesis appear as child spans with timing and metadata.</p>
      </Panel>
      <Panel className="story-accent purple">
        <small class="label">Debug Value</small>
        <h4>Visible boundaries</h4>
        <p>When the answer is wrong, the trace shows whether the issue came from routing, tool evidence, or synthesis.</p>
      </Panel>
    </div>
  </div>
</SlideFrame>

<style>
  .trace-explainer {
    grid-template-columns: minmax(0, 1.32fr) minmax(280px, 0.68fr);
    gap: 18px;
  }

  :global(.trace-diagram-card) {
    min-height: 820px;
  }

  .glossary-stack {
    gap: 14px;
    align-content: start;
  }

  :global(.glossary-stack .panel) {
    min-height: 150px;
  }
</style>
