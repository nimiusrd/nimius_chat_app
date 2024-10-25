<script lang="ts">
  import nimiusBot from "./assets/nimius_bot.png";
  import TypingText from "./lib/TypingText.svelte";
  import { useWebSocket } from "./scripts/webSocket";

  $: text = "connected";
  $: promiseChain = Promise.resolve(0);

  const onMessage = (data: ArrayBuffer | string) => {
    if (data instanceof ArrayBuffer) {
      promiseChain = promiseChain.then(
        (id) =>
          new Promise((resolve, reject) => {
            console.log("Playing audio", id);
            const audioContext = new AudioContext();
            audioContext.decodeAudioData(data).then((audioBuffer) => {
              const source = audioContext.createBufferSource();
              source.buffer = audioBuffer;
              const gainNode = audioContext.createGain();
              gainNode.gain.value = 2;
              source.connect(gainNode);
              gainNode.connect(audioContext.destination);
              source.start();
              source.onended = () => {
                console.log("Audio ended", id);
                source.disconnect();
                gainNode.disconnect();
                audioContext.close();
                resolve(id + 1);
              };
            });
          }),
      );
    } else {
      text = data;
    }
  };

  let webSocket = useWebSocket(import.meta.env.VITE_SERVER_URL, onMessage);
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
          <img src={nimiusBot} class="logo" alt="nimius Bot" />
        </div>
        <TypingText {text} />
      </div>
    {:else}
      <span>Disconnected</span>
    {/if}
  {:catch error}
    <span style="color: red">Something went wrong</span>
    <a href={window.location.host + window.location.pathname}>Reconnect</a>
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
