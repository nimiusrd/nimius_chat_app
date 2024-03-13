<script lang="ts">
  import { onMount, setContext } from "svelte";
  import { writable } from "svelte/store";
  import nimiusBot from "./assets/nimius_bot.png";
  import Status from "./lib/Status.svelte";
  import { useWebSocket } from "./scripts/webSocket";

  const socket = writable(null);

  setContext("socket", socket);

  onMount(() => {
    const { socket } = useWebSocket("ws://localhost:8001");

    console.log("socket", socket);
  });
</script>

<main>
  <div>
    <div>
      <img src={nimiusBot} class="logo" alt="Vite Logo" />
    </div>
  </div>
  <h1>WebSocket</h1>
  <Status />
</main>

<style>
  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
</style>
