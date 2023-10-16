<script lang="ts">
  import axios from "axios";
  import { onMount } from "svelte";

  import CommandPalette from "./components/CommandPalette.svelte";

  import EditInsight from "./pages/EditInsight.svelte";
  import EditNote from "./pages/EditNote.svelte";
  import ListNotes from "./pages/ListNotes.svelte";

  import { baseUrl, initSessionState, setupWebSocket, sessionState } from "./stores";

  onMount(async () => {
		const dataUrl = new URL("/data", baseUrl).href;
		let resp = await axios.get(dataUrl);

		// get the initial session state
		const initState = resp.data;
		initSessionState(initState);

		// setup websocket for exchanging data with python space
		const socketUrl = new URL("/stream", baseUrl);
		socketUrl.protocol = socketUrl.protocol.replace("http", "ws");
		setupWebSocket(socketUrl.href);
  });

  const getTitle = (content: string) => {
    let parser = new DOMParser();
    let htmlDoc = parser.parseFromString(content, 'text/html');
    let h1 = htmlDoc.getElementsByTagName("h1");
    let h2 = htmlDoc.getElementsByTagName("h2");
    let p = htmlDoc.getElementsByTagName("p");
    if (h1.length > 0) {
      return h1[0].textContent;
    }
    if (h2.length > 0) {
      return h2[0].textContent;
    }
    if (p.length > 0) {
      return p[0].textContent;
    }
    return "NBX: Next Gen Notebook";
  };

  let page: string;
  let params: any;

  sessionState.routing.subscribe((val) => {
    page = val["page"];
    params = val["params"];
  });

</script>

<svelte:head>
    {#if page === "EditNote"}
      <title>{getTitle(params["noteContent"])}</title>
    {:else}
      <title>NBX: Next Gen Notebook</title>
    {/if}
</svelte:head>

<main>
  {#if page === "EditInsight"}
    <EditInsight/>
  {:else if page === "EditNote"}
    <EditNote params={params}/>
  {:else if page === "ListNotes"}
    <ListNotes params={params}/>
  {/if}
  <CommandPalette/>
</main>

<style>
</style>
