<script lang="ts">
  import SlideFrame from "$lib/components/SlideFrame.svelte";
  import HeadingRow from "$lib/components/HeadingRow.svelte";
  import Panel from "$lib/components/Panel.svelte";
  import CodeCard from "$lib/components/CodeCard.svelte";

  const sample = `{
  "destination": "Chicago",
  "attractions": [
    {
      "name": "Chicago Architecture Center River Cruise",
      "category": "architecture",
      "summary": "A guided river cruise focused on landmark buildings.",
      "estimated_cost": "$55",
      "rationale": "Fits architecture interest and river-walk theme.",
      "source_url": "https://..."
    }
  ],
  "notes": ["Use source-backed evidence in the final answer."]
}`;

  const snippets = [
    "Architecture cruise, river walk, Millennium Park, deep-dish pizza...",
    "One snippet mentions cost, another mentions neighborhood fit, another has the source.",
    "The model still has to recover structure before it can write a coherent itinerary.",
  ];
</script>

<SlideFrame>
  <HeadingRow
    eyebrow="Build"
    title="Structured Tool Output"
    support="The planning tool returns organized evidence, not raw search snippets. That makes the model easier to guide and the behavior easier to evaluate."
  />

  <div class="comparison-grid">
    <Panel className="snippet-panel">
      <small class="label">Raw snippets</small>
      <h4>Unstructured evidence</h4>
      <div class="snippet-stack">
        {#each snippets as snippet, index}
          <div
            class="snippet-card fragment reveal-card"
            data-fragment-index={index}
          >
            {snippet}
          </div>
        {/each}
      </div>
      <p class="tiny-note">The model still has to infer what matters, what belongs together, and what it should cite.</p>
    </Panel>

    <div class="dominant-stack">
      <div class="fragment reveal-card" data-fragment-index={3}>
        <CodeCard
          label="Structured JSON"
          code={sample}
          foot="The model receives organized evidence instead of recovering meaning from a pile of snippets."
        />
      </div>

      <div class="support-strip support-strip-3">
        <Panel className="soft fragment reveal-card" data-fragment-index={4}>
          <small class="label">Rationale</small>
          <p>Why the attraction fits the user’s interests.</p>
        </Panel>
        <Panel className="soft fragment reveal-card" data-fragment-index={5}>
          <small class="label">Source</small>
          <p>Where the evidence came from so the answer can stay grounded.</p>
        </Panel>
        <Panel className="soft fragment reveal-card" data-fragment-index={6}>
          <small class="label">Cost</small>
          <p>A preserved field the final answer can use without re-parsing text.</p>
        </Panel>
      </div>
    </div>
  </div>
</SlideFrame>

<style>
  .comparison-grid {
    display: grid;
    grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr);
    gap: 22px;
  }

  :global(.snippet-panel) {
    min-height: 520px;
  }

  .snippet-stack {
    display: grid;
    gap: 12px;
    margin-top: 18px;
  }

  .snippet-card {
    padding: 14px 16px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.04);
    color: var(--ar-subtext);
    line-height: 1.45;
  }
</style>
