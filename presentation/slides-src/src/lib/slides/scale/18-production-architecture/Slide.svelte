<script lang="ts">
  import SlideFrame from "$lib/components/SlideFrame.svelte";
  import HeadingRow from "$lib/components/HeadingRow.svelte";
  import DiagramCard from "$lib/components/DiagramCard.svelte";
  import Panel from "$lib/components/Panel.svelte";
  import ProductionArchitectureDiagram from "$lib/diagrams/ProductionArchitectureDiagram.svelte";
</script>

<SlideFrame>
  <HeadingRow
    eyebrow="Scale"
    title="Production Architecture"
    support="The production design separates the stateless app, external providers, trace pipeline, and offline evaluation work so scaling concerns stay explicit."
  />

  <DiagramCard label="Three production lanes" className="production-system-card fragment reveal-card" data-fragment-index="0">
    <ProductionArchitectureDiagram />
  </DiagramCard>

  <div class="support-strip support-strip-3 top-gap">
    <Panel className="soft fragment reveal-card" data-fragment-index="1">
      <small class="label">Scale Path</small>
      <p>App pods scale horizontally behind the load balancer without changing the external LLM or search interfaces.</p>
    </Panel>
    <Panel className="soft fragment reveal-card" data-fragment-index="2">
      <small class="label">Trace Path</small>
      <p>OTLP ingestion and Phoenix remain visible system boundaries instead of being hidden inside app code.</p>
    </Panel>
    <Panel className="soft fragment reveal-card" data-fragment-index="3">
      <small class="label">Eval Path</small>
      <p>Evaluation workers and storage stay off the request path so analysis does not block the user response.</p>
    </Panel>
  </div>
</SlideFrame>

<style>
  :global(.production-system-card) {
    min-height: 420px;
  }
</style>
