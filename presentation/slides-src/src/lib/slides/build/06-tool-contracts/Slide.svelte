<script lang="ts">
  import SlideFrame from "$lib/components/SlideFrame.svelte";
  import HeadingRow from "$lib/components/HeadingRow.svelte";
  import Panel from "$lib/components/Panel.svelte";

  const contracts = [
    {
      label: "Planning",
      sample: "“What should I do in Chicago?”",
      route: "search_attractions",
      outcome: "Gather structured destination evidence and return source-backed recommendations.",
    },
    {
      label: "Current Info",
      sample: "“What is the weather in Lisbon?”",
      route: "search_web",
      outcome: "Use the web branch when the answer depends on changing information.",
    },
    {
      label: "Unsupported",
      sample: "“Book me a hotel in Rome.”",
      route: "honest limitation",
      outcome: "Do not pretend to transact. State the limit clearly and redirect into planning help instead.",
    },
  ];
</script>

<SlideFrame>
  <HeadingRow
    eyebrow="Build"
    title="Tool Contracts"
    support="The assistant only needs three behaviors: planning, fresh facts, and an honest answer when the request requires a transaction."
  />

  <div class="tool-router">
    {#each contracts as contract, idx}
      <Panel className="intent-lane fragment reveal-up" data-fragment-index={idx + 1}>
        <small class="label">{contract.label}</small>
        <div class="intent-sample">{contract.sample}</div>
        <div class="intent-arrow">↓</div>
        <div class="intent-route">{contract.route}</div>
        <p>{contract.outcome}</p>
      </Panel>
    {/each}
  </div>
</SlideFrame>

<style>
  .tool-router {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 18px;
  }

  :global(.intent-lane) {
    min-height: 400px;
    display: grid;
    gap: 18px;
    align-content: start;
  }

  .intent-sample {
    padding: 16px 18px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.04);
    color: var(--ar-text);
    font-size: 1.02rem;
    line-height: 1.42;
  }

  .intent-arrow {
    color: var(--ar-blue-2);
    font-size: 1.8rem;
    font-weight: 700;
  }

  .intent-route {
    padding: 10px 14px;
    border-radius: 999px;
    width: fit-content;
    border: 1px solid rgba(166, 236, 255, 0.18);
    background: rgba(166, 236, 255, 0.08);
    color: var(--ar-text);
    font-size: 0.86rem;
    font-weight: 700;
    letter-spacing: 0.04em;
  }
</style>
