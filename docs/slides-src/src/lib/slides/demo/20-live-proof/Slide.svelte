<script lang="ts">
  import SectionIntro from "$lib/components/SectionIntro.svelte";
  import Panel from "$lib/components/Panel.svelte";

  const proofs = [
    {
      label: "Proof 1",
      title: "Chicago planning run",
      copy: "Show the attractions tool being used and the final source-backed answer returned to the user.",
    },
    {
      label: "Proof 2",
      title: "Current-information run",
      copy: "Show the web-tool branch answering a question where freshness matters.",
    },
    {
      label: "Proof 3",
      title: "Phoenix trace + annotation",
      copy: "Open Phoenix and show how traces, spans, and evaluation feedback stay attached to one request.",
    },
  ];
</script>

<SectionIntro
  eyebrow="Demo"
  title="Live Proof"
  support="The live section focuses on three proof points: a successful planning run, a current-information run, and a trace with attached evaluation evidence."
  variant="chapter"
>
  <div class="proof-route">
    <div class="proof-line"></div>
    {#each proofs as proof, idx}
      <Panel className={`soft proof-stop fragment reveal-card stop-${idx + 1}`} data-fragment-index={idx + 1}>
        <small class="label">{proof.label}</small>
        <h4>{proof.title}</h4>
        <p>{proof.copy}</p>
      </Panel>
    {/each}
  </div>
</SectionIntro>

<style>
  .proof-route {
    position: relative;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 18px;
    padding-top: 46px;
  }

  .proof-line {
    position: absolute;
    left: 10%;
    right: 10%;
    top: 116px;
    height: 4px;
    border-radius: 999px;
    background: linear-gradient(90deg, rgba(166, 236, 255, 0.2), rgba(240, 106, 182, 0.22), rgba(166, 236, 255, 0.2));
  }

  :global(.proof-stop) {
    position: relative;
    min-height: 220px;
    z-index: 1;
  }
</style>
