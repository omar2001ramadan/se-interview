<script lang="ts">
  export let variant: "default" | "hero" | "chapter" | "close" = "default";
  export let extraClass = "";

  $: themeClass =
    variant === "hero" ? "ar-hero" : variant === "default" ? "ar-content" : "ar-section";

  $: classes = [
    "frame",
    "ar-shell",
    themeClass,
    variant !== "default" ? variant : "",
    extraClass,
  ]
    .filter(Boolean)
    .join(" ");
</script>

<div {...$$restProps} class={classes}>
  <slot />
</div>
