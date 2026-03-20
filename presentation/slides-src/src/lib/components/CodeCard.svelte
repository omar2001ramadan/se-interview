<script lang="ts">
  export let label = "";
  export let code = "";
  export let foot = "";
  export let className = "";
</script>

<div {...$$restProps} class={`code-card ar-panel pad-md ${className}`.trim()}>
  {#if label}
    <small class="label ar-label">{label}</small>
  {/if}
  <pre class="ar-code-block">{code}</pre>
  {#if foot}
    <div class="code-foot">{foot}</div>
  {/if}
  <slot />
</div>
