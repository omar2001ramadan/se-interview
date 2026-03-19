<script lang="ts">
  import { onMount } from "svelte";
  import Reveal from "reveal.js";
  import Notes from "reveal.js/plugin/notes";
  import ChapterRail from "$lib/components/ChapterRail.svelte";
  import { chapters, slides } from "$lib/deck/registry";
  import type { ChapterId } from "$lib/deck/types";

  let revealRoot: HTMLDivElement;
  let currentChapter: ChapterId = slides[0].chapter;
  let deck: any = null;

  const updateChapter = (section: Element | null | undefined) => {
    if (!section) return;
    currentChapter = ((section as HTMLElement).dataset.chapter as ChapterId) || "problem";
  };

  onMount(() => {
    const init = async () => {
      deck = new Reveal(revealRoot, {
        controls: true,
        progress: false,
        center: false,
        hash: true,
        fragmentInURL: true,
        slideNumber: "c/t",
        transition: "fade",
        transitionSpeed: "fast",
        width: 1600,
        height: 1024,
        margin: 0.01,
        plugins: [Notes],
      });

      await deck.initialize();
      updateChapter(deck.getCurrentSlide());

      deck.on("slidechanged", (event: any) => {
        updateChapter(event.currentSlide);
      });
    };

    init();

    return () => {
      deck?.destroy?.();
      deck = null;
    };
  });
</script>

<div class="deck-shell">
  <div class="reveal" bind:this={revealRoot}>
    <div class="slides">
      {#each slides as slide (slide.id)}
        <section data-chapter={slide.chapter}>
          <svelte:component this={slide.component} />
          <aside class="notes">{slide.notes}</aside>
        </section>
      {/each}
    </div>
  </div>

  <ChapterRail {chapters} activeChapter={currentChapter} />
</div>
