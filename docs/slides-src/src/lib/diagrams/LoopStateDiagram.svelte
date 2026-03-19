<div class="loop-simple-frame" aria-label="LangGraph decision loop">
  <svg class="loop-simple-svg" viewBox="0 0 860 320" aria-hidden="true">
    <defs>
      <marker id="loop-arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="#a6ecff"></path>
      </marker>
      <marker id="loop-arrow-light" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="rgba(228, 232, 255, 0.92)"></path>
      </marker>
    </defs>

    <path class="edge edge-start" d="M 100 160 L 222 160" marker-end="url(#loop-arrow-blue)"></path>
    <path class="edge edge-top" d="M 344 124 C 402 78, 498 78, 560 124" marker-end="url(#loop-arrow-light)"></path>
    <path class="edge edge-return" d="M 560 192 C 490 236, 392 236, 344 192" marker-end="url(#loop-arrow-light)"></path>
    <path class="edge edge-stop" d="M 344 174 L 724 174" marker-end="url(#loop-arrow-light)"></path>

    <text class="edge-label edge-label-top" x="440" y="54">tool requested</text>
    <text class="edge-label edge-label-bottom" x="428" y="258">JSON written back</text>
    <text class="edge-label edge-label-stop" x="514" y="156">stop</text>
  </svg>

  <div class="loop-state state-start">START</div>
  <div class="loop-state state-llm">LLM CALL</div>
  <div class="loop-state state-tool">TOOL NODE</div>
  <div class="loop-state state-end">END</div>
</div>

<style>
  .loop-simple-frame {
    position: relative;
    width: 100%;
    min-height: 300px;
  }

  .loop-simple-svg {
    display: block;
    width: 100%;
    height: auto;
    overflow: visible;
  }

  .loop-state {
    position: absolute;
    display: grid;
    place-items: center;
    color: var(--ar-text);
    font-family: var(--sans);
    font-size: 1.02rem;
    font-weight: 700;
    text-align: center;
    border-radius: 26px;
    background: rgba(16, 20, 64, 0.96);
    border: 2px solid rgba(255, 255, 255, 0.16);
    box-shadow: 0 10px 22px rgba(4, 6, 24, 0.28);
  }

  .state-start {
    left: 24px;
    top: 110px;
    width: 98px;
    height: 88px;
    border-radius: 24px;
  }

  .state-llm {
    left: 226px;
    top: 88px;
    width: 132px;
    height: 132px;
    border-color: var(--ar-blue-2);
    box-shadow: inset 0 0 0 2px rgba(166, 236, 255, 0.08), 0 10px 22px rgba(4, 6, 24, 0.28);
    background: rgba(102, 169, 221, 0.16);
  }

  .state-tool {
    left: 560px;
    top: 112px;
    width: 164px;
    height: 88px;
  }

  .state-end {
    left: 748px;
    top: 126px;
    width: 72px;
    height: 72px;
    border-radius: 999px;
    border-color: var(--ar-pink-1);
    background: rgba(240, 106, 182, 0.12);
  }

  .edge {
    fill: none;
    stroke: rgba(228, 232, 255, 0.92);
    stroke-width: 4;
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  .edge-start {
    stroke: var(--ar-blue-2);
  }

  .edge-label {
    fill: var(--ar-subtext);
    font-family: var(--sans);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
</style>
