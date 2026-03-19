<script lang="ts">
  import SectionIntro from "$lib/components/SectionIntro.svelte";
  import Panel from "$lib/components/Panel.svelte";

  const cards = [
    {
      label: "Instrumentation",
      title: "OpenTelemetry + OpenInference",
      copy: "The app is instrumented so the runtime emits model and tool spans as first-class trace data.",
      exampleLabel: "Mock span",
      example: 'span.kind="tool" · tool.name="search_attractions" · session_id="chi-01"',
    },
    {
      label: "Phoenix",
      title: "Readable Request History",
      copy: "One user request becomes one inspectable trace, with model calls, tool calls, and metadata attached.",
      exampleLabel: "Mock trace",
      example: "Chicago request -> /chat -> llm_call -> search_attractions -> final_synthesis",
    },
    {
      label: "Why It Matters",
      title: "Failure Localization",
      copy: "Bad answers can be traced back to routing, tool evidence, or final synthesis instead of guessed from logs.",
      exampleLabel: "Mock debugging note",
      example: "Routing chose web search instead of attractions tool, so the answer missed destination-specific evidence.",
    },
  ];
</script>

<SectionIntro
  eyebrow="Observe"
  title="Observe"
  support="Now that the app runs, the next question is: how do we see what it actually did?"
  variant="chapter"
>
  <div class="observe-path">
    <div class="observe-line"></div>
    <div class="observe-stop stop-1"></div>
    <div class="observe-stop stop-2 fragment sequence-glow" data-fragment-index="1"></div>
    <div class="observe-stop stop-3 fragment sequence-glow" data-fragment-index="2"></div>
    {#each cards as card, idx}
      <Panel
        className={idx === 0 ? `soft observe-card stage-${idx + 1}` : `soft observe-card fragment sequence-glow stage-${idx + 1}`}
        data-fragment-index={idx === 0 ? undefined : idx}
      >
        <div class="observe-head">
          <span class="observe-number">0{idx + 1}</span>
          <small class="label">{card.label}</small>
        </div>
        <h4>{card.title}</h4>
        <p>{card.copy}</p>
        <div class="observe-example">
          <small class="label">{card.exampleLabel}</small>
          <p>{card.example}</p>
        </div>
      </Panel>
    {/each}
  </div>
</SectionIntro>

<style>
  .observe-path {
    position: relative;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 18px;
    padding-top: 54px;
  }

  .observe-line {
    position: absolute;
    left: 8%;
    right: 8%;
    top: 28px;
    height: 5px;
    border-radius: 999px;
    background: linear-gradient(90deg, rgba(166, 236, 255, 0.2), rgba(240, 106, 182, 0.22), rgba(166, 236, 255, 0.2));
  }

  .observe-stop {
    position: absolute;
    top: 14px;
    width: 18px;
    height: 18px;
    margin-left: -9px;
    border-radius: 50%;
    border: 2px solid rgba(166, 236, 255, 0.88);
    background: rgba(11, 16, 56, 0.96);
    box-shadow: 0 0 0 6px rgba(166, 236, 255, 0.05);
    z-index: 2;
  }

  .stop-1 {
    left: 16%;
  }

  .stop-2 {
    left: 50%;
  }

  .stop-3 {
    left: 84%;
  }

  :global(.observe-card) {
    position: relative;
    min-height: 260px;
    z-index: 1;
  }

  .observe-head {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
  }

  .observe-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    border-radius: 999px;
    background: linear-gradient(135deg, rgba(102, 169, 221, 0.28), rgba(166, 236, 255, 0.16));
    border: 1px solid rgba(166, 236, 255, 0.2);
    color: var(--ar-blue-2);
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.08em;
  }

  :global(.observe-card.stage-2) {
    margin-top: 42px;
  }

  :global(.observe-card.stage-3) {
    margin-top: 84px;
  }

  .observe-example {
    margin-top: 18px;
    padding: 12px 14px;
    border-radius: 14px;
    border: 1px solid rgba(166, 236, 255, 0.12);
    background: rgba(255, 255, 255, 0.04);
  }

  .observe-example p {
    margin: 0;
    font-size: 0.92rem;
    line-height: 1.45;
  }
</style>
