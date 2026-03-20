<script lang="ts">
  import SlideFrame from "$lib/components/SlideFrame.svelte";
  import HeadingRow from "$lib/components/HeadingRow.svelte";

  export let eyebrow = "";
  export let title = "";
  export let support = "";
  export let variant: "chapter" | "close" = "chapter";
  export let extraClass = "";
</script>

<SlideFrame {variant} extraClass={extraClass}>
  <HeadingRow {eyebrow} {title} {support} />
  <div class="stack top-gap">
    <slot />
  </div>
  <div class="ar-accent-dot" style="left: 8%; bottom: 16%;"></div>
  <div class="ar-pixel" style="right: 11%; top: 18%; background: linear-gradient(135deg, #d83f9d, #a13f95);"></div>
  <div class="ar-pixel" style="right: 8%; top: 24%; background: linear-gradient(135deg, #5b73c4, #3f5597);"></div>
</SlideFrame>
