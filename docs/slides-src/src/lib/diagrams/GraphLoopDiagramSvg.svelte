<svg class="loop-svg" viewBox="0 0 1320 560" aria-label="LangGraph decision loop">
  <defs>
    <marker id="loop-arrowhead" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#e4e8ff"></path>
    </marker>
    <marker id="loop-arrowhead-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#a6ecff"></path>
    </marker>
  </defs>

  <path class="loop-start-path" d="M 190 300 L 320 300" marker-end="url(#loop-arrowhead-teal)"></path>
  <path class="loop-arc-top" d="M 470 266 L 470 168 L 924 168 L 924 232" marker-end="url(#loop-arrowhead)"></path>
  <path class="loop-arc-bottom" d="M 924 328 L 924 384 L 430 384 L 430 370" marker-end="url(#loop-arrowhead)"></path>
  <path class="loop-stop-path" d="M 470 330 L 610 330 L 610 438 L 1038 438" marker-end="url(#loop-arrowhead)"></path>

  <g class="loop-node-svg node-start">
    <rect x="74" y="246" width="116" height="108" rx="28"></rect>
    <text x="132" y="300">START</text>
  </g>

  <g class="loop-node-svg node-llm">
    <rect x="320" y="216" width="150" height="152" rx="36"></rect>
    <text x="395" y="300">LLM CALL</text>
  </g>

  <g class="loop-node-svg node-tool">
    <rect x="824" y="232" width="224" height="96" rx="28"></rect>
    <text x="936" y="280">TOOL NODE</text>
  </g>

  <g class="loop-node-svg node-end">
    <circle cx="1086" cy="442" r="44"></circle>
    <text x="1086" y="450">END</text>
  </g>

  <g class="loop-edge-labels">
    <text x="694" y="132">TOOL REQUESTED</text>
    <text x="734" y="414">JSON RESULT WRITTEN BACK</text>
    <text x="850" y="496">STOP</text>
  </g>
</svg>

<style>
  .loop-svg {
    display: block;
    width: min(1120px, 100%);
    height: auto;
    margin: 28px auto 0;
    overflow: visible;
  }

  .loop-arc-top,
  .loop-arc-bottom,
  .loop-stop-path,
  .loop-start-path {
    fill: none;
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  .loop-arc-top,
  .loop-arc-bottom,
  .loop-stop-path {
    stroke: rgba(228, 232, 255, 0.92);
    stroke-width: 4;
  }

  .loop-start-path {
    stroke: var(--ar-blue-2);
    stroke-width: 4.5;
  }

  .loop-node-svg rect,
  .loop-node-svg circle {
    fill: rgba(16, 20, 64, 0.96);
    stroke: rgba(255, 255, 255, 0.16);
    stroke-width: 2.2;
    filter: drop-shadow(0 10px 22px rgba(4, 6, 24, 0.28));
  }

  .loop-node-svg.node-llm rect {
    fill: rgba(102, 169, 221, 0.18);
    stroke: var(--ar-blue-2);
    stroke-width: 4;
  }

  .loop-node-svg.node-end circle {
    fill: rgba(240, 106, 182, 0.12);
    stroke: var(--ar-pink-1);
    stroke-width: 4;
  }

  .loop-node-svg text {
    fill: var(--ar-text);
    font-family: var(--sans);
    font-size: 24px;
    font-weight: 600;
    text-anchor: middle;
    dominant-baseline: middle;
  }

  .loop-edge-labels text {
    fill: var(--ar-subtext);
    font-family: var(--sans);
    font-size: 17px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-anchor: middle;
  }
</style>
