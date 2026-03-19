import "reveal.js/reveal.css";
import "$lib/styles/base.css";
import "$lib/styles/layout.css";
import "$lib/styles/motion.css";
import "$lib/styles/diagrams.css";
import App from "./App.svelte";
import { mount } from "svelte";

mount(App, {
  target: document.getElementById("app")!,
});
