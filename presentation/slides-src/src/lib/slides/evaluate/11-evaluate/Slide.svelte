<script lang="ts">
  import SlideFrame from "$lib/components/SlideFrame.svelte";
  import HeadingRow from "$lib/components/HeadingRow.svelte";
  import Panel from "$lib/components/Panel.svelte";

  const stages = [
    {
      label: "Trace-Based",
      title: "Score actual executions",
      copy: "The pipeline runs on exported traces instead of synthetic examples detached from the app.",
    },
    {
      label: "Two Views",
      title: "User experience + system behavior",
      copy: "The system scores both frustration and tool-routing correctness so quality is not reduced to one number.",
    },
    {
      label: "Debug Loop",
      title: "Write results back",
      copy: "Annotations flow back into Phoenix so traces and evaluation outcomes stay attached to the same request history.",
    },
  ];
</script>

<SlideFrame variant="chapter">
  <HeadingRow
    eyebrow="Evaluate"
    title="Evaluate"
    support="Once the runtime was visible as traces, the next step was to score behavior instead of judging quality by feel."
  />

  <Panel className="bridge-board">
    <div class="bridge-line"></div>
    <div class="bridge-flow">
      {#each stages as stage, idx}
        <div
          class={idx === 0 ? "bridge-step" : "bridge-step fragment reveal-card"}
          data-fragment-index={idx === 0 ? undefined : idx}
        >
          <div class="bridge-number">0{idx + 1}</div>
          <small class="label">{stage.label}</small>
          <h4>{stage.title}</h4>
          <p>{stage.copy}</p>
        </div>
        {#if idx < stages.length - 1}
          <div class={idx === 0 ? "bridge-arrow" : "bridge-arrow fragment reveal-up"} data-fragment-index={idx === 0 ? undefined : idx}>→</div>
        {/if}
      {/each}
    </div>
  </Panel>
</SlideFrame>

<style>
  :global(.bridge-board) {
    padding: 28px;
    min-height: 460px;
    position: relative;
  }

  .bridge-flow {
    height: 100%;
    display: grid;
    grid-template-columns: 1fr auto 1fr auto 1fr;
    gap: 18px;
    align-items: center;
    position: relative;
    z-index: 1;
  }

  .bridge-line {
    position: absolute;
    left: 11%;
    right: 11%;
    top: 50%;
    height: 4px;
    transform: translateY(-50%);
    border-radius: 999px;
    background: linear-gradient(90deg, rgba(166, 236, 255, 0.12), rgba(166, 236, 255, 0.42), rgba(240, 106, 182, 0.18));
  }

  .bridge-step {
    min-height: 240px;
    padding: 24px 22px;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: linear-gradient(180deg, rgba(18, 24, 73, 0.94), rgba(14, 18, 55, 0.98));
  }

  .bridge-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    margin-bottom: 14px;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(166, 236, 255, 0.22), rgba(102, 169, 221, 0.12));
    border: 1px solid rgba(166, 236, 255, 0.2);
    color: var(--ar-blue-2);
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.08em;
  }

  .bridge-arrow {
    color: var(--ar-blue-2);
    font-size: 2rem;
    font-weight: 700;
  }
</style>
