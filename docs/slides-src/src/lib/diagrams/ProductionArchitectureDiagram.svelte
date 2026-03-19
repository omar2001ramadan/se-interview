<div class="prod-lanes">
  <div class="prod-lane request-lane">
    <div class="lane-label">Request path</div>
    <div class="lane-nodes">
      <div class="lane-node strong">Client</div>
      <div class="lane-arrow">→</div>
      <div class="lane-node">Load Balancer</div>
      <div class="lane-arrow">→</div>
      <div class="lane-node strong">FastAPI + LangGraph pods</div>
      <div class="lane-arrow">→</div>
      <div class="lane-node">Redis cache</div>
      <div class="lane-arrow">→</div>
      <div class="lane-node">LLM + search providers</div>
    </div>
  </div>

  <div class="prod-lane trace-lane">
    <div class="lane-label">Trace path</div>
    <div class="lane-nodes">
      <div class="lane-node strong">App spans</div>
      <div class="lane-arrow">→</div>
      <div class="lane-node">OTLP collector</div>
      <div class="lane-arrow">→</div>
      <div class="lane-node strong">Phoenix</div>
      <div class="lane-arrow">→</div>
      <div class="lane-node">Trace inspection</div>
    </div>
  </div>

  <div class="prod-lane eval-lane">
    <div class="lane-label">Eval path</div>
    <div class="lane-nodes">
      <div class="lane-node">Exported traces</div>
      <div class="lane-arrow">→</div>
      <div class="lane-node strong">Async eval workers</div>
      <div class="lane-arrow">→</div>
      <div class="lane-node">Artifacts + datasets</div>
      <div class="lane-arrow">→</div>
      <div class="lane-node">Debug backlog</div>
    </div>
  </div>
</div>

<style>
  .prod-lanes {
    display: grid;
    gap: 18px;
  }

  .prod-lane {
    display: grid;
    grid-template-columns: 190px 1fr;
    gap: 18px;
    align-items: stretch;
  }

  .lane-label {
    display: grid;
    align-content: center;
    padding: 18px 20px;
    border-radius: 18px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: linear-gradient(180deg, rgba(12, 16, 52, 0.94), rgba(10, 12, 38, 0.98));
    color: var(--ar-text);
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }

  .lane-nodes {
    display: grid;
    grid-template-columns: repeat(9, auto);
    gap: 10px;
    align-items: center;
  }

  .lane-node {
    min-height: 88px;
    padding: 14px 16px;
    border-radius: 18px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: linear-gradient(180deg, rgba(18, 24, 73, 0.9), rgba(14, 18, 55, 0.98));
    display: grid;
    align-content: center;
    justify-items: center;
    text-align: center;
    font-size: 0.92rem;
    line-height: 1.35;
    box-shadow: 0 14px 30px rgba(4, 6, 24, 0.22);
  }

  .lane-node.strong {
    border-color: rgba(166, 236, 255, 0.22);
    background: linear-gradient(180deg, rgba(23, 29, 87, 0.92), rgba(14, 18, 55, 0.98));
  }

  .lane-arrow {
    color: var(--ar-blue-2);
    font-size: 1.55rem;
    font-weight: 700;
  }
</style>
