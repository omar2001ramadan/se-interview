<script lang="ts">
  export let label = "";
  export let className = "";
</script>

<div {...$$restProps} class={`diagram-card ar-panel pad-md ${className}`.trim()}>
  {#if label}
    <small class="label ar-label">{label}</small>
  {/if}
  <slot />
</div>
