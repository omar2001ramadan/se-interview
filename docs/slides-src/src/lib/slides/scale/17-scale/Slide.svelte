<script lang="ts">
  import SectionIntro from "$lib/components/SectionIntro.svelte";
  import Panel from "$lib/components/Panel.svelte";

  const ideas = [
    {
      label: "Traffic",
      copy: "Real traffic means horizontal serving, timeouts, and cache boundaries.",
    },
    {
      label: "Dependencies",
      copy: "LLM and search providers become external systems that can slow down or fail.",
    },
    {
      label: "Observability",
      copy: "Trace ingestion and evaluation have to scale without blocking the live response path.",
    },
  ];
</script>

<SectionIntro
  eyebrow="Scale"
  title="Scale"
  support="If this stopped being a local demo and became a real service, the system would need a production runtime, an external dependency strategy, and a trace path that scales."
  variant="chapter"
>
  <div class="scale-triad">
    {#each ideas as idea, index}
      <Panel className="soft scale-word fragment reveal-card" data-fragment-index={index}>
        <small class="label">Production concern</small>
        <h3>{idea.label}</h3>
        <p>{idea.copy}</p>
      </Panel>
    {/each}
  </div>
</SectionIntro>

<style>
  .scale-triad {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 18px;
  }

  :global(.scale-word) {
    min-height: 220px;
    display: grid;
    align-content: center;
    text-align: center;
  }

  :global(.scale-word h3) {
    margin-bottom: 10px;
    font-size: 2rem;
    line-height: 1;
    letter-spacing: -0.04em;
  }
</style>
