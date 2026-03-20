<script lang="ts">
  export let eyebrow = "";
  export let title = "";
  export let support = "";
</script>

<div class="heading-row">
  <div>
    {#if eyebrow}
      <p class="eyebrow ar-kicker">{eyebrow}</p>
    {/if}
    <h2 class="ar-title">{title}</h2>
  </div>
  {#if support}
    <p class="support ar-subtitle">{support}</p>
  {/if}
</div>
