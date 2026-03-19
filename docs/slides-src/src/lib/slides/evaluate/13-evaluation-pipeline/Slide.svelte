<script lang="ts">
  import SlideFrame from "$lib/components/SlideFrame.svelte";
  import HeadingRow from "$lib/components/HeadingRow.svelte";
  import DiagramCard from "$lib/components/DiagramCard.svelte";
  import Panel from "$lib/components/Panel.svelte";
  import EvalPipelineDiagram from "$lib/diagrams/EvalPipelineDiagram.svelte";
</script>

<SlideFrame>
  <HeadingRow
    eyebrow="Evaluate"
    title="Evaluation Pipeline"
    support="Trace export, scoring, annotation, and failure collection happen as one loop so evaluation stays attached to real executions."
  />

  <DiagramCard label="Trace-based scoring loop" className="eval-pipeline-card fragment reveal-card" data-fragment-index="0">
    <EvalPipelineDiagram />
  </DiagramCard>

  <Panel className="top-gap story-accent fragment reveal-card" data-fragment-index="1">
    <small class="label">Why this loop matters</small>
    <p>The trace, the score, and the follow-up dataset all stay attached to the same execution history instead of living in separate tools.</p>
  </Panel>
</SlideFrame>

<style>
  :global(.eval-pipeline-card) {
    min-height: 310px;
  }
</style>
