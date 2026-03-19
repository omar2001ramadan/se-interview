<script lang="ts">
  import type { ChapterDefinition, ChapterId } from "$lib/deck/types";

  export let chapters: ChapterDefinition[] = [];
  export let activeChapter: ChapterId = "problem";
</script>

<div class="chapter-rail">
  {#each chapters as chapter, index}
    {@const activeIndex = chapters.findIndex((item) => item.id === activeChapter)}
    <div
      class:rail-stop={true}
      class:is-complete={index < activeIndex}
      class:is-active={index === activeIndex}
    >
      <span>{chapter.label}</span>
    </div>
  {/each}
</div>
