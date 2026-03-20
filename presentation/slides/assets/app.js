(() => {
  const chapters = [
    { id: "problem", label: "Problem" },
    { id: "build", label: "Build" },
    { id: "observe", label: "Observe" },
    { id: "evaluate", label: "Evaluate" },
    { id: "scale", label: "Scale" },
    { id: "demo", label: "Demo" },
    { id: "outcome", label: "Outcome" },
  ];

  const buildRail = (activeChapter) => {
    const activeIndex = chapters.findIndex((chapter) => chapter.id === activeChapter);
    return `
      <div class="chapter-rail" aria-hidden="true">
        ${chapters
          .map((chapter, index) => {
            const state =
              index < activeIndex
                ? "is-complete"
                : index === activeIndex
                  ? "is-active"
                  : "";
            return `<div class="rail-stop ${state}"><span>${chapter.label}</span></div>`;
          })
          .join("")}
      </div>
    `;
  };

  document.querySelectorAll(".slides > section").forEach((section) => {
    const chapter = section.dataset.chapter || "problem";
    section.classList.add(`chapter-${chapter}`);
    const frame = section.querySelector(".frame");
    if (frame) {
      frame.insertAdjacentHTML("beforeend", buildRail(chapter));
    }
  });

  const deck = new Reveal({
    controls: true,
    progress: false,
    center: false,
    hash: true,
    fragmentInURL: true,
    slideNumber: "c/t",
    transition: "fade",
    transitionSpeed: "fast",
    autoAnimateEasing: "ease-out",
    autoAnimateDuration: 0.5,
    width: 1600,
    height: 900,
    margin: 0.05,
    plugins: [RevealNotes],
  });

  const initMermaid = async () => {
    if (!window.mermaid) {
      return;
    }
    window.mermaid.initialize({
      startOnLoad: false,
      securityLevel: "loose",
      theme: "base",
      flowchart: {
        useMaxWidth: false,
        htmlLabels: true,
        curve: "basis",
        nodeSpacing: 28,
        rankSpacing: 70,
      },
      themeVariables: {
        background: "#fffaf1",
        primaryColor: "#fffaf1",
        primaryTextColor: "#18221e",
        primaryBorderColor: "#e4ddd1",
        lineColor: "#0f7068",
        tertiaryColor: "#f8e5d8",
        tertiaryBorderColor: "#ca6d3a",
        secondaryColor: "#d9efeb",
        secondaryBorderColor: "#0f7068",
        clusterBkg: "#fffaf1",
        clusterBorder: "#efe6d8",
        fontFamily: "Avenir Next, Segoe UI, Helvetica Neue, sans-serif",
      },
    });
    await window.mermaid.run({ querySelector: ".mermaid" });
  };

  const setIntroOffset = (section) => {
    if (!section || section.dataset.introShift !== "true") {
      return;
    }
    const frame = section.querySelector(".frame");
    const heading = section.querySelector(".intro-heading");
    if (!frame || !heading) {
      return;
    }
    const frameRect = frame.getBoundingClientRect();
    const headingRect = heading.getBoundingClientRect();
    const targetLeft = (frameRect.width - headingRect.width) / 2;
    const targetTop = (frameRect.height * 0.42) - (headingRect.height / 2);
    const currentLeft = headingRect.left - frameRect.left;
    const currentTop = headingRect.top - frameRect.top;
    frame.style.setProperty("--intro-shift-x", `${targetLeft - currentLeft}px`);
    frame.style.setProperty("--intro-shift-y", `${targetTop - currentTop}px`);
  };

  const syncIntroState = (section) => {
    if (!section || section.dataset.introShift !== "true") {
      return;
    }
    const frame = section.querySelector(".frame");
    if (!frame) {
      return;
    }
    setIntroOffset(section);
    const expanded = Boolean(section.querySelector(".fragment.visible"));
    frame.classList.toggle("intro-expanded", expanded);
  };

  deck.initialize().then(async () => {
    await initMermaid();
    deck.layout();
    document.querySelectorAll(".slides > section[data-intro-shift='true']").forEach(setIntroOffset);
    syncIntroState(deck.getCurrentSlide());
  });

  window.addEventListener("resize", () => {
    document.querySelectorAll(".slides > section[data-intro-shift='true']").forEach(syncIntroState);
  });

  deck.on("slidechanged", (event) => {
    syncIntroState(event.previousSlide);
    syncIntroState(event.currentSlide);
  });

  deck.on("fragmentshown", (event) => {
    syncIntroState(event.fragment.closest("section"));
  });

  deck.on("fragmenthidden", (event) => {
    syncIntroState(event.fragment.closest("section"));
  });
})();
