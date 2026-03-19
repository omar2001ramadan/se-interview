<script lang="ts">
  export let label = "";
  export let title = "";
  export let className = "";
</script>

<div {...$$restProps} class={`stage-card ar-panel pad-md ${className}`.trim()}>
  {#if label}
    <small class="label ar-label">{label}</small>
  {/if}
  {#if title}
    <h4 class="ar-card-title">{title}</h4>
  {/if}
  <slot />
</div>
