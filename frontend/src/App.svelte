<script lang="ts">
  import nimiusBot from "./assets/nimius_bot.png";
  import TypingText from "./lib/TypingText.svelte";
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

  let webSocket = useWebSocket("ws://localhost:8001", onMessage);
</script>

<main>
  {#await webSocket}
    <span>...waiting</span>
  {:then webSocket}
    {#if webSocket.socket.readyState === WebSocket.CONNECTING}
      <span>Connecting</span>
    {:else if webSocket.socket.readyState === WebSocket.OPEN}
      <div class="container">
        <div>
          <img src={nimiusBot} class="logo" alt="Vite Logo" />
        </div>
        <TypingText {text} />
      </div>
    {:else}
      <span>Disconnected</span>
    {/if}
  {:catch error}
    <span style="color: red">{error.message}</span>
  {/await}
</main>

<style>
  .logo {
    height: 125px;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .container {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: center;
  }
</style>
