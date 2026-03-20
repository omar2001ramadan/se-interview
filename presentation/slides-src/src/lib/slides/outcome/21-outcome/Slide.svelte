<script lang="ts">
  import SectionIntro from "$lib/components/SectionIntro.svelte";
  import Panel from "$lib/components/Panel.svelte";
</script>

<SectionIntro
  eyebrow="Outcome"
  title="Outcome"
  support="The starter repo became a travel assistant that is easier to understand, easier to inspect, and easier to judge with real evidence."
  variant="close"
>
  <div class="stack outcome-stack">
    <div class="grid grid-3 outcome-summary">
      <Panel className="fragment reveal-card" data-fragment-index="0">
        <small class="label">Built</small>
        <h4>Travel-aware agent plus frontend</h4>
        <p>A LangGraph assistant with structured planning output, current-info fallback, honest unsupported behavior, and a browser demo surface.</p>
      </Panel>
      <Panel className="fragment reveal-card" data-fragment-index="1">
        <small class="label">Observed</small>
        <h4>Traceable and explorable runtime</h4>
        <p>Phoenix traces, exported spans, attached annotations, and the embeddings view make one request inspectable from more than one angle.</p>
      </Panel>
      <Panel className="fragment reveal-card" data-fragment-index="2">
        <small class="label">Learned</small>
        <h4>Specific failures</h4>
        <p>The Tokyo routing miss, frustrated booking examples, and live boundary prompts point directly to prompt and recovery improvements.</p>
      </Panel>
    </div>

    <div class="outcome-lower fragment reveal-card" data-fragment-index="3">
      <Panel className="outcome-wide next-panel">
        <small class="label">Next Step</small>
        <h4>Prompt and recovery tuning</h4>
        <p>The clearest next improvements are better planning-tool triggers and stronger unsupported-action recovery.</p>
        <div class="next-list">
          <div>1. tighten planning-tool trigger language</div>
          <div>2. add nightlife-style routing tests</div>
          <div>3. improve unsupported-action recovery</div>
        </div>
      </Panel>
    </div>
  </div>
</SectionIntro>

<style>
  .outcome-stack {
    gap: 22px;
    min-height: 700px;
  }

  .outcome-summary {
    align-items: stretch;
  }

  .outcome-lower {
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: 18px;
    min-height: 250px;
  }

  :global(.outcome-summary .panel) {
    min-height: 196px;
  }

  :global(.outcome-wide) {
    min-height: 250px;
  }

  .next-list div {
    display: inline-flex;
    align-items: center;
    padding: 8px 12px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: var(--ar-subtext);
    font-size: 0.8rem;
    line-height: 1;
  }

  .next-list {
    display: grid;
    gap: 10px;
    margin-top: 18px;
  }
</style>
