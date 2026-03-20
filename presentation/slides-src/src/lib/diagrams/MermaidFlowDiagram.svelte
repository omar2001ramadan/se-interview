<script lang="ts">
  import { onMount } from "svelte";
  import mermaid from "mermaid";

  export let graph = "";
  export let className = "";

  let container: HTMLDivElement;
  let initialized = false;

  const init = () => {
    if (initialized) return;
    mermaid.initialize({
      startOnLoad: false,
      securityLevel: "loose",
      theme: "base",
      flowchart: {
        useMaxWidth: false,
        htmlLabels: true,
        curve: "linear",
        nodeSpacing: 88,
        rankSpacing: 168,
      },
      themeVariables: {
        background: "#0b1038",
        primaryColor: "rgba(18, 24, 73, 0.92)",
        primaryTextColor: "rgba(255, 255, 255, 0.96)",
        primaryBorderColor: "rgba(255, 255, 255, 0.18)",
        lineColor: "#a6ecff",
        tertiaryColor: "rgba(240, 106, 182, 0.18)",
        tertiaryBorderColor: "#f06ab6",
        secondaryColor: "rgba(102, 169, 221, 0.2)",
        secondaryBorderColor: "#66a9dd",
        clusterBkg: "rgba(18, 24, 73, 0.88)",
        clusterBorder: "rgba(255, 255, 255, 0.12)",
        fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif",
        fontSize: "16px",
      },
    });
    initialized = true;
  };

  const renderDiagram = async () => {
    if (!container || !graph) return;
    init();
    const id = `mermaid-${Math.random().toString(36).slice(2)}`;
    const { svg } = await mermaid.render(id, graph);
    container.innerHTML = svg;
  };

  onMount(() => {
    renderDiagram();
  });
</script>

<div class={`mermaid-flow ${className}`.trim()} bind:this={container}></div>
