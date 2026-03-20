<script lang="ts">
  import SlideFrame from "$lib/components/SlideFrame.svelte";
  import HeadingRow from "$lib/components/HeadingRow.svelte";
  import Panel from "$lib/components/Panel.svelte";
</script>

<SlideFrame>
  <HeadingRow
    eyebrow="Evaluate"
    title="Tool Routing"
    support="The custom metric checked whether the system chose the right tool first for the kind of question it was given."
  />

  <div class="routing-layout">
    <Panel className="scoreboard-card fragment reveal-card" data-fragment-index="0">
      <small class="label">Routing scoreboard</small>
      <p class="snapshot-note">Artifact snapshot from the latest 10-query evaluation run.</p>
      <div class="scoreboard">
        <div class="scorebox fragment metric-pop" data-fragment-index="1">
          <strong>9</strong>
          <span>Correct</span>
        </div>
        <div class="scorebox miss fragment metric-pop" data-fragment-index="2">
          <strong>1</strong>
          <span>Incorrect</span>
        </div>
      </div>

      <div class="route-compare">
        <div class="route-line expected fragment reveal-card" data-fragment-index="3">
          <span>Expected</span>
          <p>Tokyo nightlife → attractions tool → structured neighborhood recommendations</p>
        </div>
        <div class="route-line observed fragment reveal-card" data-fragment-index="4">
          <span>Observed</span>
          <p>Tokyo nightlife → generic answer path → tool not used early enough</p>
        </div>
      </div>
    </Panel>

    <Panel className="story-accent pink fragment reveal-card" data-fragment-index="5">
      <small class="label">Observed Miss</small>
      <h4>Tokyo nightlife request</h4>
      <p><strong>Expected:</strong> use the attractions tool for destination planning.</p>
      <p><strong>Observed:</strong> the model stayed too general and did not use the structured planning tool early enough.</p>
      <p>This became the most useful debugging trace in the deck.</p>
    </Panel>
  </div>
</SlideFrame>

<style>
  .routing-layout {
    display: grid;
    grid-template-columns: minmax(0, 0.92fr) minmax(360px, 1.08fr);
    gap: 22px;
  }

  :global(.scoreboard-card) {
    min-height: 420px;
  }

  .scoreboard {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 14px;
    margin-top: 14px;
  }

  .snapshot-note {
    margin: 10px 0 0;
    color: var(--ar-muted);
    font-size: 0.74rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }

  .scorebox {
    padding: 18px 18px 16px;
    border-radius: 18px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.04);
  }

  .scorebox strong {
    display: block;
    margin-bottom: 6px;
    font-size: 2.3rem;
    line-height: 1;
    color: var(--ar-blue-2);
  }

  .scorebox.miss strong {
    color: var(--ar-pink-1);
  }

  .route-compare {
    display: grid;
    gap: 12px;
    margin-top: 18px;
  }

  .route-line {
    padding: 14px 16px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.04);
  }

  .route-line span {
    display: block;
    margin-bottom: 8px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .route-line.expected span {
    color: var(--ar-blue-2);
  }

  .route-line.observed span {
    color: var(--ar-pink-1);
  }
</style>
