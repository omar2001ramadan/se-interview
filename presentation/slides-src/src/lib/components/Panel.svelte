<script lang="ts">
  export let className = "";
</script>

<div {...$$restProps} class={`panel ar-panel pad-md ${className}`.trim()}>
  <slot />
</div>
