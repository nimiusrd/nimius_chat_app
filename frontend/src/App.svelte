<script lang="ts">
  import nimiusBot from "./assets/nimius_bot.png";
  import { useWebSocket } from "./scripts/webSocket";

  const onMessage = (data: Blob) => {
    console.log("Message received: ", data);

    const audioContext = new AudioContext();
    data.arrayBuffer().then((buffer) => {
      audioContext.decodeAudioData(buffer, (audioBuffer) => {
        const source = audioContext.createBufferSource();
        source.buffer = audioBuffer;
        const gainNode = audioContext.createGain();
        gainNode.gain.value = 2;
        source.connect(gainNode);
        gainNode.connect(audioContext.destination);
        source.start();
      });
    });
  };

  let socket = useWebSocket("ws://localhost:8001", onMessage);
</script>

<main>
  <div>
    <div>
      <img src={nimiusBot} class="logo" alt="Vite Logo" />
    </div>
  </div>
  <h1>WebSocket</h1>
  {#await socket}
    <p>...waiting</p>
  {:then}
    <p>connected</p>
  {:catch error}
    <p style="color: red">{error.message}</p>
  {/await}
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
