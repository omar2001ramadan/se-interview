<script lang="ts">
  import SlideFrame from "$lib/components/SlideFrame.svelte";
  import HeadingRow from "$lib/components/HeadingRow.svelte";
  import Panel from "$lib/components/Panel.svelte";

  const cards = [
    {
      label: "Latency",
      title: "Cache repeated work",
      copy: "Frequent destination questions, trace lookups, and web search results should be cached to keep request latency predictable.",
    },
    {
      label: "Cost",
      title: "Use async evaluation",
      copy: "Judge models and trace scoring should run after the request so evaluation cost does not compound the live serving cost.",
    },
    {
      label: "Reliability",
      title: "Bound retries carefully",
      copy: "Search and LLM providers need timeout and retry rules so dependency failures degrade gracefully instead of hanging the whole flow.",
    },
    {
      label: "Observability",
      title: "Sample selectively",
      copy: "Keep full traces in development and targeted sampling in production so the signal remains strong without overwhelming storage.",
    },
  ];
</script>

<SlideFrame>
  <HeadingRow
    eyebrow="Scale"
    title="Operational Tradeoffs"
    support="Scaling the system is not only about more containers. It also means making explicit choices about latency, cost, reliability, and observability."
  />

  <div class="tradeoff-board">
    {#each cards as card, index}
      <Panel className="decision-quadrant fragment reveal-card" data-fragment-index={index}>
        <small class="label">{card.label}</small>
        <h4>{card.title}</h4>
        <p>{card.copy}</p>
      </Panel>
    {/each}
  </div>
</SlideFrame>

<style>
  .tradeoff-board {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
  }

  :global(.decision-quadrant) {
    min-height: 220px;
  }
</style>
