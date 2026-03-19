<script lang="ts">
  import SlideFrame from "$lib/components/SlideFrame.svelte";
  import Panel from "$lib/components/Panel.svelte";

  const behaviors = [
    {
      label: "Planning",
      title: "Plan what to do",
      copy: "Recommend attractions, neighborhoods, museums, parks, and food options for a destination.",
      accent: "teal",
    },
    {
      label: "Current info",
      title: "Answer fresh questions",
      copy: "Look up weather, advisories, and other changing travel facts when the answer must be current.",
      accent: "pink",
    },
    {
      label: "Explainability",
      title: "Show the work",
      copy: "Capture traces, attach evaluations, and turn failures into specific debugging evidence.",
      accent: "purple",
    },
  ];
</script>

<SlideFrame variant="hero">
  <div class="hero-grid product-hero">
    <div class="hero-copy product-copy">
      <div class="dominant-stack">
        <div>
        <p class="eyebrow ar-kicker">Travel Assistant • LangGraph • Phoenix</p>
        <h1 class="ar-title hero-title">
          Travel Assistant<br />
          that <span class="gradient">Explains Itself</span>
        </h1>
        <p class="lead ar-subtitle">
          A travel assistant that helps plan what to do, answer current travel questions,
          and show how it arrived at each answer.
        </p>
        </div>

        <Panel className="hero-question story-accent">
          <small class="label">Backbone question</small>
          <h4>I have one day in Chicago and love architecture and river walks. What should I do?</h4>
          <p>The rest of the talk follows this one question through runtime, tracing, evaluation, and debugging.</p>
        </Panel>
      </div>
    </div>

    <div class="hero-side product-side">
      <div class="ar-pixel" style="right: 16%; top: 14%; background: linear-gradient(135deg, #d83f9d, #a13f95);"></div>
      <div class="ar-pixel" style="right: 10%; top: 22%; background: linear-gradient(135deg, #5b73c4, #3f5597);"></div>

      <div class="route-intro">
        <h3 class="ar-card-title">One assistant, three clear behaviors</h3>
        <p class="ar-card-copy">Planning help, current information, and trace-backed explainability.</p>
      </div>

      {#each behaviors as behavior, idx}
        <Panel
          className={`story-prompt ${behavior.accent} fragment reveal-card`}
          data-fragment-index={idx + 1}
        >
          <small class="label">{behavior.label}</small>
          <h4>{behavior.title}</h4>
          <p>{behavior.copy}</p>
        </Panel>
      {/each}
    </div>
  </div>
</SlideFrame>

<style>
  .hero-title {
    max-width: 540px;
  }

  .product-copy {
    padding-right: 18px;
  }

  .gradient {
    background: linear-gradient(90deg, var(--ar-pink-1), var(--ar-purple-2), var(--ar-blue-2));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }

  :global(.hero-question) {
    max-width: 560px;
    padding: 22px 24px;
  }

  .product-side {
    display: grid;
    align-content: start;
    gap: 14px;
  }

  .route-intro {
    display: grid;
    gap: 6px;
    position: relative;
    z-index: 2;
    margin-bottom: 4px;
  }

  :global(.story-prompt) {
    min-height: 118px;
    position: relative;
    z-index: 2;
    border-top: 4px solid rgba(166, 236, 255, 0.3);
  }

  :global(.story-prompt.pink) {
    border-top-color: rgba(240, 106, 182, 0.34);
  }

  :global(.story-prompt.purple) {
    border-top-color: rgba(140, 108, 188, 0.4);
  }

  :global(.story-prompt h4) {
    margin-bottom: 10px;
  }
</style>
