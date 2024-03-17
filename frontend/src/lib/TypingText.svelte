<script lang="ts">
  export let text: string;
  let delayedText = "";
  let intervalId: number | null = null;

  $: {
    if (delayedText !== text && intervalId === null) {
      delayedText = "";
      intervalId = setInterval(() => {
        delayedText += text[delayedText.length];
      }, 60);
    }
    if (delayedText === text && typeof intervalId === "number") {
      clearInterval(intervalId);
      intervalId = null;
    }
  }
</script>

<div class="text-container">{delayedText}</div>

<style>
  .text-container {
    width: 100%;
    text-align: justify;
    font-size: 28px;
    line-height: 1;
    align-self: center;
  }
</style>
