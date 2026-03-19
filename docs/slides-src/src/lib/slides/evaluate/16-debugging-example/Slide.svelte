<script lang="ts">
  import SlideFrame from "$lib/components/SlideFrame.svelte";
  import HeadingRow from "$lib/components/HeadingRow.svelte";
  import DiagramCard from "$lib/components/DiagramCard.svelte";
  import Panel from "$lib/components/Panel.svelte";
</script>

<SlideFrame>
  <HeadingRow
    eyebrow="Evaluate"
    title="Debugging Example"
    support="The Tokyo nightlife miss turned the evaluation system into a concrete debugging workflow instead of just a score report."
  />

  <div class="debug-layout">
    <DiagramCard label="Tokyo trace branch" className="debug-card fragment reveal-card" data-fragment-index="0">
      <div class="debug-prompt">
        <small class="label">Prompt</small>
        <h4>“I’m visiting Tokyo for one night. I like nightlife and neighborhoods with bars. Where should I go?”</h4>
      </div>

      <div class="debug-route-board">
        <div class="debug-route expected fragment reveal-card" data-fragment-index="1">
          <span>Expected branch</span>
          <p>Tokyo planning request → attractions tool → structured neighborhood recommendations</p>
        </div>
        <div class="debug-route observed fragment reveal-card" data-fragment-index="2">
          <span>Observed branch</span>
          <p>Tokyo planning request → generic answer path → attractions tool not used early enough</p>
        </div>
      </div>
    </DiagramCard>

    <div class="stack">
      <Panel className="story-accent pink fragment reveal-card" data-fragment-index="3">
        <small class="label">What happened</small>
        <p>The trace showed that the routing decision stayed too general instead of committing to the planning tool early in the conversation.</p>
      </Panel>
      <Panel className="story-accent fragment reveal-card" data-fragment-index="4">
        <small class="label">What to change</small>
        <p>Tighten prompt rules around destination-planning language and add nightlife-style examples to the routing tests so the decision boundary becomes sharper.</p>
      </Panel>
    </div>
  </div>
</SlideFrame>

<style>
  .debug-layout {
    display: grid;
    grid-template-columns: minmax(0, 1.12fr) minmax(320px, 0.88fr);
    gap: 22px;
  }

  .debug-prompt {
    display: grid;
    gap: 8px;
    margin-bottom: 18px;
  }

  .debug-route-board {
    display: grid;
    gap: 14px;
  }

  .debug-route {
    padding: 18px 18px;
    border-radius: 18px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.04);
  }

  .debug-route span {
    display: block;
    margin-bottom: 8px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .debug-route.expected span {
    color: var(--ar-blue-2);
  }

  .debug-route.observed {
    border-color: rgba(240, 106, 182, 0.24);
    background: rgba(240, 106, 182, 0.08);
  }

  .debug-route.observed span {
    color: var(--ar-pink-1);
  }
</style>
