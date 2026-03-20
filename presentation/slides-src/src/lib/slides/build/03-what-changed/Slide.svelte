<script lang="ts">
  import SlideFrame from "$lib/components/SlideFrame.svelte";
  import HeadingRow from "$lib/components/HeadingRow.svelte";
  import Panel from "$lib/components/Panel.svelte";

  const moves = [
    {
      index: "01",
      title: "Planning Tool",
      copy: "Add `search_attractions` so destination questions return organized travel evidence.",
      payoff: "Closes the generic-search limitation.",
    },
    {
      index: "02",
      title: "Tracing",
      copy: "Instrument the app so one request becomes one trace with model and tool spans.",
      payoff: "Makes runtime behavior inspectable in Phoenix.",
    },
    {
      index: "03",
      title: "Evaluations",
      copy: "Score those traces for user frustration and tool-routing correctness.",
      payoff: "Turns quality into something measurable.",
    },
    {
      index: "04",
      title: "Production Shape",
      copy: "Add tests, Docker, scripts, docs, and architecture thinking around the agent.",
      payoff: "Makes the repo credible beyond a local demo.",
    },
  ];
</script>

<SlideFrame>
  <HeadingRow
    eyebrow="Build"
    title="What Changed"
    support="To turn the starter into a useful and explainable travel assistant, four concrete capabilities had to be added."
  />

  <Panel className="change-route-board">
    <div class="route-base">
      <small class="label">Starting point</small>
      <h4>Starter repo</h4>
      <p>API + LangGraph loop + one generic search behavior.</p>
    </div>

    <div class="upgrade-ladder">
      {#each moves as move, idx}
        <div
          class={idx === 0 ? "move-card upgrade-node" : "move-card upgrade-node fragment reveal-card"}
          data-fragment-index={idx === 0 ? undefined : idx + 1}
        >
          <div class="move-index">{move.index}</div>
          <h4>{move.title}</h4>
          <p>{move.copy}</p>
          <div class="upgrade-payoff">{move.payoff}</div>
        </div>
      {/each}
    </div>
  </Panel>
</SlideFrame>

<style>
  :global(.change-route-board) {
    position: relative;
    min-height: 560px;
    overflow: hidden;
    padding: 30px 28px 32px;
  }

  :global(.change-route-board)::before {
    content: "";
    position: absolute;
    left: 190px;
    right: 84px;
    top: 212px;
    height: 6px;
    border-radius: 999px;
    background: linear-gradient(90deg, rgba(240, 106, 182, 0.34), rgba(140, 108, 188, 0.32), rgba(166, 236, 255, 0.28));
    box-shadow: 0 0 26px rgba(140, 108, 188, 0.16);
  }

  .route-base {
    width: 230px;
    padding: 20px 22px;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: linear-gradient(180deg, rgba(12, 16, 52, 0.94), rgba(10, 12, 38, 0.98));
    box-shadow: 0 14px 28px rgba(4, 6, 24, 0.24);
  }

  .upgrade-ladder {
    position: relative;
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 18px;
    margin-top: 56px;
    margin-left: 170px;
  }

  :global(.upgrade-node) {
    position: relative;
    min-height: 210px;
    overflow: hidden;
    z-index: 2;
  }

  .move-index {
    color: rgba(166, 236, 255, 0.32);
  }

  .upgrade-payoff {
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    color: var(--ar-blue-2);
    font-size: 0.82rem;
    font-weight: 600;
  }

  :global(.upgrade-node) p {
    margin-top: 10px;
  }
</style>
