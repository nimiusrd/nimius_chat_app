<script lang="ts">
  import nimiusBot from "./assets/nimius_bot.png";
  import { useWebSocket } from "./scripts/webSocket";

  $: text = "connected";

  const onMessage = (data: ArrayBuffer | string) => {
    console.log("Message received: ", data);
    if (data instanceof ArrayBuffer) {
      const audioContext = new AudioContext();
      audioContext.decodeAudioData(data, (audioBuffer) => {
        const source = audioContext.createBufferSource();
        source.buffer = audioBuffer;
        const gainNode = audioContext.createGain();
        gainNode.gain.value = 2;
        source.connect(gainNode);
        gainNode.connect(audioContext.destination);
        source.start();
      });
    } else {
      text = data;
    }
  };

  let socket = useWebSocket("ws://localhost:8001", onMessage);
</script>

<main>
  <div>
    <div>
      <img src={nimiusBot} class="logo" alt="Vite Logo" />
    </div>
  </div>
  {#await socket}
    <p>...waiting</p>
  {:then}
    <p>{text}</p>
  {:catch error}
    <p style="color: red">{error.message}</p>
  {/await}
</main>

<style>
  .logo {
    height: 6em;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
</style>
