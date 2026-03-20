<script lang="ts">
  import SlideFrame from "$lib/components/SlideFrame.svelte";
  import HeadingRow from "$lib/components/HeadingRow.svelte";
  import DiagramCard from "$lib/components/DiagramCard.svelte";
  import Panel from "$lib/components/Panel.svelte";
  import RuntimeFlowDiagramSvg from "$lib/diagrams/RuntimeFlowDiagramSvg.svelte";
</script>

<SlideFrame>
  <HeadingRow
    eyebrow="Build"
    title="Runtime Architecture"
    support="One Chicago question enters the API, the graph decides which tool to use, the tool returns evidence, and the model turns that evidence into the final answer."
  />

  <div class="example-card backbone-callout">
    <small class="label">Backbone Request</small>
    <p>“I have one day in Chicago and love architecture and river walks. What should I do?”</p>
  </div>

  <DiagramCard label="Decision Flow" className="runtime-card">
    <div class="runtime-legend">
      <span class="legend-item legend-main">primary answer path</span>
      <span class="legend-item legend-alt">fresh-facts fallback</span>
    </div>

    <RuntimeFlowDiagramSvg />

    <div class="support-strip support-strip-4 runtime-detail-grid">
      <Panel className="soft fragment metric-pop" data-fragment-index="1">
        <small class="label">User → API</small>
        <p>The Chicago request enters <code>/chat</code> and becomes a traced runtime request.</p>
      </Panel>
      <Panel className="soft fragment metric-pop" data-fragment-index="2">
        <small class="label">Metadata → LLM</small>
        <p><code>session_id</code>, route metadata, and project naming travel with the model call.</p>
      </Panel>
      <Panel className="soft fragment metric-pop" data-fragment-index="3">
        <small class="label">Router → Tool</small>
        <p>The graph decides whether planning evidence or fresh-facts search is the right behavior.</p>
      </Panel>
      <Panel className="soft fragment metric-pop" data-fragment-index="4">
        <small class="label">Tool → Answer</small>
        <p>The model reads tool evidence, cites sources, and writes the user-facing response.</p>
      </Panel>
    </div>
  </DiagramCard>
</SlideFrame>

<style>
  .backbone-callout {
    margin-bottom: 18px;
    border-left: 6px solid var(--ar-blue-2);
    background: linear-gradient(180deg, rgba(23, 29, 87, 0.88), rgba(14, 18, 55, 0.96));
  }

  :global(.runtime-card) {
    min-height: 500px;
  }

  :global(.runtime-card svg) {
    min-height: 360px;
  }

  .runtime-legend {
    display: flex;
    justify-content: flex-end;
    gap: 24px;
    margin-bottom: 10px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.58rem;
  }

  .legend-item::before {
    content: "";
    display: inline-block;
    width: 42px;
    height: 4px;
    margin-right: 10px;
    border-radius: 999px;
    vertical-align: middle;
  }

  .legend-main::before {
    background: var(--ar-blue-2);
  }

  .legend-alt::before {
    background: var(--ar-pink-1);
  }

  .runtime-detail-grid {
    margin-top: 18px;
  }
</style>
