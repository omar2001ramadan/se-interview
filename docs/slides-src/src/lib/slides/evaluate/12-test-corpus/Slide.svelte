<script lang="ts">
  import SlideFrame from "$lib/components/SlideFrame.svelte";
  import HeadingRow from "$lib/components/HeadingRow.svelte";
  import Panel from "$lib/components/Panel.svelte";

  const groups = [
    {
      label: "Planning",
      sample: "“I have one day in Chicago and love architecture and river walks. What should I do?”",
      expected: "Use `search_attractions` and return source-backed recommendations.",
      experience: "Should feel helpful, specific, and grounded.",
    },
    {
      label: "Current Info",
      sample: "“What is the weather in Lisbon right now?”",
      expected: "Use `search_web` because freshness matters.",
      experience: "Should feel current instead of generic or stale.",
    },
    {
      label: "Unsupported",
      sample: "“Book me a hotel in Rome.”",
      expected: "Be honest about the limit and redirect into planning help.",
      experience: "Should avoid a dead end even when the answer is a refusal.",
    },
  ];
</script>

<SlideFrame>
  <HeadingRow
    eyebrow="Evaluate"
    title="Test Corpus"
    support="The 10-query corpus intentionally covered three kinds of user needs so the traces would include both successful and difficult interactions."
  />

  <div class="corpus-lanes">
    {#each groups as group, idx}
      <Panel
        className={idx === 0 ? "corpus-lane" : "corpus-lane fragment reveal-card"}
        data-fragment-index={idx === 0 ? undefined : idx}
      >
        <div class="lane-head">
          <span class="lane-number">0{idx + 1}</span>
          <small class="label">{group.label}</small>
        </div>
        <div class="lane-sample">{group.sample}</div>
        <div class="expectation">
          <span>Expected route / behavior</span>
          <p>{group.expected}</p>
        </div>
        <div class="expectation">
          <span>Expected user experience</span>
          <p>{group.experience}</p>
        </div>
      </Panel>
    {/each}
  </div>
</SlideFrame>

<style>
  .corpus-lanes {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 18px;
  }

  :global(.corpus-lane) {
    min-height: 430px;
    display: grid;
    gap: 18px;
    align-content: start;
  }

  .lane-head {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .lane-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    border-radius: 999px;
    background: linear-gradient(135deg, rgba(166, 236, 255, 0.28), rgba(166, 236, 255, 0.12));
    border: 1px solid rgba(166, 236, 255, 0.18);
    color: var(--ar-blue-2);
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.08em;
  }

  .lane-sample {
    padding: 16px 18px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.04);
    color: var(--ar-text);
    line-height: 1.45;
  }

  .expectation {
    display: grid;
    gap: 8px;
    padding-top: 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }

  .expectation span {
    color: var(--ar-blue-2);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
</style>
