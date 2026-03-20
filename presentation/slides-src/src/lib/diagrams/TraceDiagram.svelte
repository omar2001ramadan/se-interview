<script lang="ts">
  const steps = [
    {
      label: "Root Trace",
      title: "Chicago Planning Request",
      copy: "One user request becomes one trace with timing, metadata, and child spans.",
      chips: ["request_id=chi-01", "duration=1.8s", "spans=3"],
      accent: "root",
      fragment: 0,
    },
    {
      label: "Span 1",
      title: "FastAPI /chat",
      copy: "Request enters the service, attaches session metadata, and starts the traced runtime.",
      chips: ["kind=server", "session_id=chi-01"],
      accent: "span",
      fragment: 1,
    },
    {
      label: "Span 2",
      title: "LLM + Tool Branch",
      copy: "The graph calls the model, routes to a tool, and records the tool evidence that came back.",
      chips: ["model=gpt-4o", "tool=search_attractions"],
      accent: "span",
      fragment: 2,
    },
    {
      label: "Span 3",
      title: "Final Answer",
      copy: "The model synthesizes the evidence into the user-facing answer and closes the request path.",
      chips: ["kind=synthesis", "sources=3"],
      accent: "span",
      fragment: 3,
    },
  ];
</script>

<div class="trace-timeline">
  <div class="trace-legend">
    <div class="legend-pill">
      <span class="legend-swatch root"></span>
      <span>Root trace</span>
    </div>
    <div class="legend-pill">
      <span class="legend-swatch span"></span>
      <span>Child spans</span>
    </div>
  </div>

  <div class="trace-rail"></div>

  {#each steps as step, index}
    <div
      class={`trace-row trace-row-${step.accent} ${index === 0 ? "" : "fragment reveal-up"}`.trim()}
      data-fragment-index={index === 0 ? undefined : step.fragment}
    >
      <div class={`trace-stop ${step.accent}`}></div>
      <div class={`trace-card ${step.accent}`}>
        <small class="label">{step.label}</small>
        <h4>{step.title}</h4>
        <p>{step.copy}</p>
        <div class="trace-meta">
          {#each step.chips as chip}
            <span>{chip}</span>
          {/each}
        </div>
      </div>
    </div>
  {/each}

</div>

<style>
  .trace-timeline {
    position: relative;
    min-height: 760px;
    padding: 18px 22px 18px 22px;
  }

  .trace-legend {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-bottom: 24px;
  }

  .legend-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    font-size: 0.76rem;
    color: var(--ar-subtext);
  }

  .legend-swatch {
    width: 10px;
    height: 10px;
    border-radius: 999px;
    display: inline-block;
  }

  .legend-swatch.root {
    background: var(--ar-pink-1);
  }

  .legend-swatch.span {
    background: var(--ar-blue-2);
  }

  .trace-rail {
    position: absolute;
    left: 94px;
    top: 90px;
    bottom: 42px;
    width: 4px;
    border-radius: 999px;
    background: linear-gradient(180deg, rgba(240, 106, 182, 0.72), rgba(166, 236, 255, 0.72));
    opacity: 0.78;
  }

  .trace-row {
    position: relative;
    display: grid;
    grid-template-columns: 92px minmax(0, 1fr);
    gap: 22px;
    align-items: start;
    margin-bottom: 24px;
  }

  .trace-stop {
    position: relative;
    width: 28px;
    height: 28px;
    margin: 38px auto 0;
    border-radius: 999px;
    background: rgba(11, 16, 56, 0.96);
    z-index: 1;
  }

  .trace-stop.root {
    border: 4px solid rgba(240, 106, 182, 0.9);
    box-shadow: 0 0 0 8px rgba(240, 106, 182, 0.08);
  }

  .trace-stop.span {
    border: 4px solid rgba(166, 236, 255, 0.9);
    box-shadow: 0 0 0 8px rgba(166, 236, 255, 0.08);
  }

  .trace-card {
    padding: 22px 24px 20px;
    border-radius: 22px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: linear-gradient(180deg, rgba(18, 24, 73, 0.94), rgba(14, 18, 55, 0.98));
    box-shadow: 0 16px 30px rgba(4, 6, 24, 0.24);
    max-width: 760px;
  }

  .trace-card.root {
    border-left: 4px solid rgba(240, 106, 182, 0.72);
  }

  .trace-card.span {
    border-left: 4px solid rgba(166, 236, 255, 0.66);
  }

  .trace-card h4 {
    margin: 0 0 12px;
  }

  .trace-card p {
    margin: 0;
  }

  .trace-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 16px;
  }

  .trace-meta span {
    display: inline-flex;
    align-items: center;
    padding: 5px 10px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: var(--ar-subtext);
    font-size: 0.76rem;
    line-height: 1;
  }

</style>
