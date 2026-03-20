<div class="loop-svg-frame" aria-label="LangGraph decision loop">
  <svg class="loop-svg" viewBox="0 0 860 300" aria-hidden="true">
    <defs>
      <marker id="loop-arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="#a6ecff"></path>
      </marker>
      <marker id="loop-arrow-light" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="rgba(228, 232, 255, 0.92)"></path>
      </marker>
      <filter id="loop-shadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="8" stdDeviation="8" flood-color="rgba(4,6,24,0.28)" />
      </filter>
    </defs>

    <path class="edge edge-start" d="M 116 148 L 234 148" marker-end="url(#loop-arrow-blue)"></path>
    <path class="edge edge-top" d="M 392 112 C 452 72, 520 72, 582 112" marker-end="url(#loop-arrow-light)"></path>
    <path class="edge edge-return" d="M 582 184 C 516 224, 448 224, 392 184" marker-end="url(#loop-arrow-light)"></path>
    <path class="edge edge-stop" d="M 392 148 L 724 148" marker-end="url(#loop-arrow-light)"></path>

    <text class="edge-label" x="476" y="52">tool requested</text>
    <text class="edge-label" x="444" y="246">JSON written back</text>
    <text class="edge-label" x="526" y="132">stop</text>

    <g filter="url(#loop-shadow)">
      <rect class="state state-start" x="28" y="104" rx="22" ry="22" width="96" height="88"></rect>
      <rect class="state state-llm" x="236" y="80" rx="24" ry="24" width="156" height="136"></rect>
      <rect class="state state-tool" x="584" y="108" rx="22" ry="22" width="158" height="80"></rect>
      <circle class="state state-end" cx="790" cy="148" r="38"></circle>
    </g>

    <text class="state-text" x="76" y="154" text-anchor="middle">START</text>

    <text class="state-text" x="314" y="146" text-anchor="middle">
      <tspan x="314" dy="-6">LLM CALL</tspan>
    </text>

    <text class="state-text" x="663" y="153" text-anchor="middle">TOOL NODE</text>
    <text class="state-text" x="790" y="154" text-anchor="middle">END</text>
  </svg>
</div>

<style>
  .loop-svg-frame {
    width: 100%;
    min-height: 280px;
  }

  .loop-svg {
    display: block;
    width: 100%;
    height: auto;
    overflow: visible;
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

  .state {
    fill: rgba(16, 20, 64, 0.96);
    stroke: rgba(255, 255, 255, 0.16);
    stroke-width: 2;
  }

  .state-llm {
    fill: rgba(102, 169, 221, 0.16);
    stroke: var(--ar-blue-2);
  }

  .state-end {
    fill: rgba(240, 106, 182, 0.12);
    stroke: var(--ar-pink-1);
  }

  .state-text {
    fill: var(--ar-text);
    font-family: var(--sans);
    font-size: 18px;
    font-weight: 700;
    dominant-baseline: middle;
  }
</style>
