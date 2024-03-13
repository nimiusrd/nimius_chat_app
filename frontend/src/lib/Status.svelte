<script lang="ts">
  import { getContext } from "svelte";
  const socket = getContext("socket");
  console.log("socket", socket);
</script>

<p>Status: {$socket.readyState}</p>
