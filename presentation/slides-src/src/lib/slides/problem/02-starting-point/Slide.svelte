<script lang="ts">
  import SlideFrame from "$lib/components/SlideFrame.svelte";
  import HeadingRow from "$lib/components/HeadingRow.svelte";
  import Panel from "$lib/components/Panel.svelte";

  const starterSteps = [
    {
      badge: "API",
      title: "Accepted a question through an API",
      copy: "FastAPI received the request and handed it into the LangGraph runtime.",
    },
    {
      badge: "LOOP",
      title: "Ran a small LangGraph loop",
      copy: "The model could decide whether to answer directly or call a tool before returning a response.",
    },
    {
      badge: "SEARCH",
      title: "Used one generic search tool",
      copy: "The system could retrieve information, but it did not yet distinguish planning work from fresh-facts work.",
    },
  ];

  const gaps = [
    {
      title: "Specialize for travel planning",
      why: "Destination questions needed structured planning evidence, not just a generic search answer.",
    },
    {
      title: "Show LLM and tool steps in Phoenix",
      why: "Without visible spans, there was no way to inspect where a bad answer came from.",
    },
    {
      title: "Score real behavior on real traces",
      why: "Evaluation needed to run on actual executions instead of detached examples or intuition.",
    },
    {
      title: "Tell a credible production story",
      why: "The repo needed runtime, testing, and deployment thinking beyond a local-only demo.",
    },
  ];
</script>

<SlideFrame>
  <HeadingRow
    eyebrow="Problem"
    title="Starting Point"
    support="The starter repo already worked end to end, but it still behaved like a generic agent demo instead of a travel system you could inspect and trust."
  />

  <div class="starting-layout">
    <Panel className="baseline-panel">
      <small class="label">What the starter already did</small>
      <div class="baseline-flow">
        {#each starterSteps as step, idx}
          <div
            class="baseline-step fragment reveal-card"
            data-fragment-index={idx + 1}
          >
            <div class="baseline-marker">{idx + 1}</div>
            <div class="baseline-copy">
              <div class="baseline-head">
                <span class="baseline-badge">{step.badge}</span>
              </div>
              <h4>{step.title}</h4>
              <p>{step.copy}</p>
            </div>
          </div>
        {/each}
      </div>
    </Panel>

    <div class="gap-stack">
      {#each gaps as gap, idx}
        <Panel
          className="gap-card stage-card fragment reveal-card"
          data-fragment-index={idx + 4}
        >
          <div class="gap-card-head">
            <small class="label">What it could not yet do</small>
            <span class="gap-step">{idx + 1} / {gaps.length}</span>
          </div>
          <h4>{gap.title}</h4>
          <div class="gap-why">
            <span>Why needed</span>
            <p>{gap.why}</p>
          </div>
        </Panel>
      {/each}
    </div>
  </div>
</SlideFrame>

<style>
  .starting-layout {
    display: grid;
    grid-template-columns: minmax(0, 0.84fr) minmax(0, 1.16fr);
    gap: 22px;
  }

  :global(.baseline-panel) {
    min-height: 548px;
    padding: 26px 26px 28px;
  }

  .baseline-flow {
    display: grid;
    gap: 16px;
    margin-top: 18px;
  }

  .baseline-step {
    position: relative;
    display: grid;
    grid-template-columns: 48px 1fr;
    gap: 16px;
    align-items: start;
    padding: 16px 16px 18px;
    border-radius: 22px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.035);
  }

  .baseline-marker {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    margin-top: 2px;
    font-size: 0.94rem;
    font-weight: 700;
    color: var(--ar-text);
    background: linear-gradient(135deg, rgba(102, 169, 221, 0.34), rgba(166, 236, 255, 0.18));
    border: 1px solid rgba(166, 236, 255, 0.22);
    box-shadow: 0 10px 24px rgba(4, 6, 24, 0.22);
  }

  .baseline-copy {
    display: grid;
    gap: 10px;
  }

  .baseline-head {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .baseline-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 62px;
    padding: 5px 10px;
    border-radius: 999px;
    background: rgba(166, 236, 255, 0.08);
    border: 1px solid rgba(166, 236, 255, 0.16);
    color: var(--ar-blue-2);
    font-size: 0.66rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .gap-stack {
    display: grid;
    gap: 18px;
    align-content: start;
  }

  :global(.gap-card) {
    min-height: 0;
    padding: 20px 22px 18px;
    border-radius: 24px;
  }

  .gap-card-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
  }

  .gap-step {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 52px;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--ar-blue-2);
    background: rgba(166, 236, 255, 0.08);
    border: 1px solid rgba(166, 236, 255, 0.16);
  }

  .gap-why {
    display: grid;
    gap: 6px;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }

  .gap-why span {
    color: var(--ar-blue-2);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
</style>
