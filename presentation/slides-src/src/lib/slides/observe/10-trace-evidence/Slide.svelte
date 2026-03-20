<script lang="ts">
  import SlideFrame from "$lib/components/SlideFrame.svelte";
  import HeadingRow from "$lib/components/HeadingRow.svelte";
  import DiagramCard from "$lib/components/DiagramCard.svelte";
  import Panel from "$lib/components/Panel.svelte";

  const traces = [
    { query: "Chicago architecture + river walks", spans: "14 spans", tag: "healthy" },
    { query: "Lisbon weather right now", spans: "11 spans", tag: "web path" },
    { query: "Tokyo nightlife for one night", spans: "12 spans", tag: "routing miss" },
    { query: "Book me a hotel in Rome", spans: "9 spans", tag: "frustrated" },
  ];
</script>

<SlideFrame>
  <HeadingRow
    eyebrow="Observe"
    title="Trace Evidence"
    support="After running 10 queries through the assistant, this is what the system produced inside Phoenix and the exported artifacts."
  />

  <Panel className="evidence-metric-board">
    <div class="snapshot-note">Artifact snapshot from the latest 10-query run. Rerun the query and evaluation scripts to refresh these counts.</div>
    <div class="evidence-storyline">
      <span>10 runs</span>
      <span>132 spans</span>
      <span>2 frustrated</span>
    </div>
    <div class="trace-metrics-strip">
      <div class="evidence-metric">
        <small class="label">Runs</small>
        <strong>10</strong>
        <p>Root traces created from the scripted query set.</p>
      </div>
      <div class="evidence-metric">
        <small class="label">Spans</small>
        <strong>132</strong>
        <p>Total execution spans across model calls, tools, and synthesis.</p>
      </div>
      <div class="evidence-metric">
        <small class="label">Frustrated</small>
        <strong>2</strong>
        <p>Interactions flagged by the user-frustration evaluation.</p>
      </div>
    </div>
  </Panel>

  <div class="trace-evidence-layout top-gap">
    <DiagramCard label="Phoenix sample traces" className="trace-gallery-card">
      <div class="trace-gallery">
        {#each traces as trace}
          <div class="trace-row">
            <div>
              <h4>{trace.query}</h4>
              <p>{trace.spans}</p>
            </div>
            <span class={`trace-badge ${trace.tag.replace(" ", "-")}`}>{trace.tag}</span>
          </div>
        {/each}
      </div>
    </DiagramCard>

    <Panel className="pipeline-panel">
      <small class="label">What came out of the run</small>
      <div class="pipeline-stack">
        <div class="pipeline-node">
          <h4>Export</h4>
          <p>Spans were written to JSON and CSV artifacts so the run could be scored outside the live UI.</p>
        </div>
        <div class="pipeline-arrow">↓</div>
        <div class="pipeline-node">
          <h4>Annotations</h4>
          <p>Evaluation results were written back to Phoenix as trace annotations on the relevant spans.</p>
        </div>
        <div class="pipeline-arrow">↓</div>
        <div class="pipeline-node">
          <h4>Dataset</h4>
          <p>Frustrated interactions were collected into a reusable failure set for follow-up debugging.</p>
        </div>
      </div>
    </Panel>
  </div>
</SlideFrame>

<style>
  :global(.evidence-metric-board) {
    padding: 14px 16px;
  }

  .evidence-storyline {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 4px 0 14px;
    color: var(--ar-subtext);
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  .snapshot-note {
    margin: 0 0 12px;
    color: var(--ar-muted);
    font-size: 0.76rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }

  .evidence-storyline span + span::before {
    content: "→";
    margin-right: 16px;
    color: var(--ar-blue-2);
  }

  .trace-metrics-strip {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
  }

  .evidence-metric {
    padding: 16px 14px 18px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: linear-gradient(180deg, rgba(23, 29, 87, 0.74), rgba(14, 18, 55, 0.9));
  }

  .evidence-metric strong {
    display: block;
    margin: 6px 0 10px;
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(90deg, var(--ar-pink-1), var(--ar-purple-2), var(--ar-blue-2));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }

  .trace-evidence-layout {
    display: grid;
    grid-template-columns: minmax(0, 1.16fr) minmax(300px, 0.84fr);
    gap: 22px;
  }

  .trace-gallery {
    display: grid;
    gap: 12px;
    margin-top: 12px;
    position: relative;
    padding-left: 12px;
  }

  .trace-gallery::before {
    content: "";
    position: absolute;
    left: 0;
    top: 14px;
    bottom: 14px;
    width: 3px;
    border-radius: 999px;
    background: linear-gradient(180deg, rgba(166, 236, 255, 0.18), rgba(166, 236, 255, 0.5));
  }

  .trace-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    padding: 16px 18px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.035);
  }

  .trace-row h4 {
    margin-bottom: 6px;
    font-size: 1.02rem;
  }

  .trace-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 7px 12px;
    border-radius: 999px;
    min-width: 112px;
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  .trace-badge.healthy,
  .trace-badge.web-path {
    background: rgba(102, 169, 221, 0.14);
    color: var(--ar-blue-2);
  }

  .trace-badge.routing-miss,
  .trace-badge.frustrated {
    background: rgba(240, 106, 182, 0.14);
    color: var(--ar-pink-1);
  }

  :global(.pipeline-panel) {
    min-height: 420px;
  }

  .pipeline-stack {
    display: grid;
    gap: 12px;
    margin-top: 14px;
  }

  .pipeline-arrow {
    display: grid;
    place-items: center;
    color: var(--ar-blue-2);
    font-size: 1.2rem;
    font-weight: 700;
  }

  .pipeline-node {
    padding: 16px 18px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.04);
  }
</style>
