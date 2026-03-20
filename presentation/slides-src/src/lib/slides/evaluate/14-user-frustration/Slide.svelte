<script lang="ts">
  import SlideFrame from "$lib/components/SlideFrame.svelte";
  import HeadingRow from "$lib/components/HeadingRow.svelte";
  import Panel from "$lib/components/Panel.svelte";
</script>

<SlideFrame>
  <HeadingRow
    eyebrow="Evaluate"
    title="User Frustration"
    support="The first evaluation asked a user-centered question: did the interaction still feel frustrating, even if the answer was technically honest?"
  />

  <div class="frustration-layout">
    <div class="stack">
      <div class="metric-card frustration-score fragment metric-pop" data-fragment-index="0">
        <small class="label">Result</small>
        <strong>2</strong>
        <p>Two interactions were flagged as frustrated and collected into a Phoenix dataset.</p>
      </div>
      <Panel className="story-accent pink fragment reveal-card" data-fragment-index="1">
        <small class="label">Lesson</small>
        <h4>Honest limits still matter</h4>
        <p>A truthful “I can’t book that” answer can still create a poor user experience if the transition is abrupt or unhelpful.</p>
      </Panel>
    </div>

    <div class="frustration-compare">
      <Panel className="good-path fragment reveal-card" data-fragment-index="2">
        <small class="label">Non-Frustrated Example</small>
        <h4>Chicago planning request</h4>
        <p>The user gets structured, source-backed recommendations that match the original intent.</p>
      </Panel>
      <Panel className="bad-path fragment reveal-card" data-fragment-index="3">
        <small class="label">Frustrated Example</small>
        <h4>Unsupported booking request</h4>
        <p>The system is honest about the limit, but the interaction still feels like a dead end without a better recovery path.</p>
      </Panel>
    </div>
  </div>
</SlideFrame>

<style>
  .frustration-layout {
    display: grid;
    grid-template-columns: minmax(320px, 0.72fr) minmax(0, 1.28fr);
    gap: 22px;
  }

  .frustration-score {
    min-height: 240px;
  }

  .frustration-compare {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
  }

  :global(.good-path) {
    border-top: 4px solid rgba(166, 236, 255, 0.42);
  }

  :global(.bad-path) {
    border-top: 4px solid rgba(240, 106, 182, 0.42);
  }
</style>
