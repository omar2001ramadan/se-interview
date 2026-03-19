<div class="eval-pipeline-strip">
  <div class="eval-stage">
    <small class="label">Export</small>
    <h4>Phoenix traces</h4>
    <p>Take the real request traces out of Phoenix as structured span data.</p>
  </div>
  <div class="eval-stage-arrow">→</div>
  <div class="eval-stage">
    <small class="label">Join</small>
    <h4>Corpus context</h4>
    <p>Attach the expected scenario, tool choice, and user intent for each run.</p>
  </div>
  <div class="eval-stage-arrow">→</div>
  <div class="eval-stage wide">
    <small class="label">Score</small>
    <h4>Frustration + routing</h4>
    <p>Run both the user-centered and system-centered evaluators on the same trace history.</p>
  </div>
  <div class="eval-stage-arrow">→</div>
  <div class="eval-stage">
    <small class="label">Write Back</small>
    <h4>Annotations + dataset</h4>
    <p>Send results back to Phoenix and save failures into a reusable debugging set.</p>
  </div>
</div>

<style>
  .eval-pipeline-strip {
    display: grid;
    grid-template-columns: 1fr auto 1fr auto 1.18fr auto 1fr;
    gap: 14px;
    align-items: stretch;
  }

  .eval-stage {
    min-height: 184px;
    padding: 18px 20px;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: linear-gradient(180deg, rgba(18, 24, 73, 0.94), rgba(14, 18, 55, 0.98));
    box-shadow: 0 14px 30px rgba(4, 6, 24, 0.24);
  }

  .eval-stage.wide {
    background: linear-gradient(180deg, rgba(23, 29, 87, 0.9), rgba(14, 18, 55, 0.98));
    border-color: rgba(166, 236, 255, 0.22);
  }

  .eval-stage-arrow {
    align-self: center;
    color: var(--ar-blue-2);
    font-size: 2rem;
    font-weight: 700;
  }
</style>
