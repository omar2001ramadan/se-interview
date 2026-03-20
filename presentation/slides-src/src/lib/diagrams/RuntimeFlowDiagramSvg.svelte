<svg class="runtime-flow-svg" viewBox="0 0 2380 460" aria-label="Runtime request flow">
  <defs>
    <marker id="runtime-arrow-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#a6ecff"></path>
    </marker>
    <marker id="runtime-arrow-pink" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#f06ab6"></path>
    </marker>
  </defs>

  <g class="runtime-primary">
    <path d="M 220 188 L 378 188" marker-end="url(#runtime-arrow-teal)"></path>
    <path d="M 586 188 L 742 188" marker-end="url(#runtime-arrow-teal)"></path>
    <path d="M 1030 230 L 1118 230" marker-end="url(#runtime-arrow-teal)"></path>
    <path d="M 1322 230 L 1396 190 L 1488 190" marker-end="url(#runtime-arrow-teal)"></path>
    <path d="M 1718 190 L 1806 190 L 1888 230" marker-end="url(#runtime-arrow-teal)"></path>
    <path d="M 2080 230 L 2144 230" marker-end="url(#runtime-arrow-teal)"></path>
  </g>

  <g class="runtime-fallback">
    <path d="M 286 324 C 432 324, 598 324, 712 272" marker-end="url(#runtime-arrow-pink)"></path>
    <path d="M 1322 230 L 1404 320 L 1488 320" marker-end="url(#runtime-arrow-pink)"></path>
    <path d="M 1716 320 L 1804 320 L 1888 250" marker-end="url(#runtime-arrow-pink)"></path>
  </g>

  <g class="runtime-node">
    <rect x="40" y="128" width="180" height="120" rx="34"></rect>
    <text x="130" y="182">
      <tspan x="130" dy="0">User</tspan>
      <tspan x="130" dy="30">Request</tspan>
    </text>
  </g>

  <g class="runtime-node">
    <rect x="378" y="128" width="208" height="120" rx="34"></rect>
    <text x="482" y="182">
      <tspan x="482" dy="0">Chat</tspan>
      <tspan x="482" dy="30">API</tspan>
    </text>
  </g>

  <g class="runtime-node runtime-node-warm">
    <rect x="66" y="264" width="220" height="120" rx="34"></rect>
    <text x="176" y="318">
      <tspan x="176" dy="0">Session</tspan>
      <tspan x="176" dy="30">Context</tspan>
    </text>
  </g>

  <g class="runtime-node">
    <rect x="742" y="144" width="284" height="128" rx="36"></rect>
    <text x="884" y="194">
      <tspan x="884" dy="0">LangGraph</tspan>
      <tspan x="884" dy="30">Model Call</tspan>
    </text>
  </g>

  <g class="runtime-diamond">
    <polygon points="1118,230 1220,128 1322,230 1220,332"></polygon>
    <text x="1220" y="197">
      <tspan x="1220" dy="0">Tool</tspan>
      <tspan x="1220" dy="30">Routing</tspan>
    </text>
  </g>

  <g class="runtime-node runtime-node-teal">
    <rect x="1488" y="120" width="230" height="136" rx="36"></rect>
    <text x="1603" y="176">
      <tspan x="1603" dy="0">Attractions</tspan>
      <tspan x="1603" dy="30">Tool</tspan>
    </text>
  </g>

  <g class="runtime-node runtime-node-warm">
    <rect x="1488" y="276" width="228" height="120" rx="34"></rect>
    <text x="1602" y="332">
      <tspan x="1602" dy="0">Web</tspan>
      <tspan x="1602" dy="30">Search</tspan>
    </text>
  </g>

  <g class="runtime-node">
    <rect x="1888" y="180" width="192" height="100" rx="30"></rect>
    <text x="1984" y="218">
      <tspan x="1984" dy="0">Final</tspan>
      <tspan x="1984" dy="28">Synthesis</tspan>
    </text>
  </g>

  <g class="runtime-node">
    <rect x="2144" y="180" width="220" height="100" rx="30"></rect>
    <text x="2254" y="218">
      <tspan x="2254" dy="0">Travel</tspan>
      <tspan x="2254" dy="28">Guidance</tspan>
    </text>
  </g>
</svg>

<style>
  .runtime-flow-svg {
    display: block;
    width: 100%;
    height: auto;
    overflow: visible;
  }

  .runtime-primary path,
  .runtime-fallback path {
    fill: none;
    stroke-linecap: round;
    stroke-linejoin: round;
    stroke-width: 3.5;
    filter: drop-shadow(0 8px 18px rgba(4, 6, 24, 0.18));
  }

  .runtime-primary path {
    stroke: var(--ar-blue-2);
  }

  .runtime-fallback path {
    stroke: var(--ar-pink-1);
    stroke-dasharray: 1 0;
  }

  .runtime-node rect,
  .runtime-diamond polygon {
    fill: rgba(16, 20, 64, 0.96);
    stroke: rgba(255, 255, 255, 0.18);
    stroke-width: 2.4;
    filter: drop-shadow(0 12px 24px rgba(4, 6, 24, 0.28));
  }

  .runtime-node-teal rect {
    fill: rgba(31, 79, 116, 0.42);
    stroke: var(--ar-blue-2);
    stroke-width: 4;
  }

  .runtime-node-warm rect {
    fill: rgba(93, 30, 86, 0.42);
    stroke: var(--ar-pink-1);
    stroke-width: 4;
  }

  .runtime-node text,
  .runtime-diamond text {
    fill: var(--ar-text);
    font-family: var(--sans);
    font-size: 24px;
    font-weight: 600;
    text-anchor: middle;
    dominant-baseline: middle;
  }
</style>
