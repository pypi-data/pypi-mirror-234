<script lang="ts">
    export let params;
    import { onMount } from "svelte";
    import NoteCards from "../components/NoteCards.svelte";
    import EditNote from "./EditNote.svelte";
    import { webSocket, sessionState } from "../stores";

    let currentNote: object = {};

    onMount(() => {
        sessionState.routing.subscribe((val) => {
            currentNote = val["params"]["currentNote"];
        });
    });

    const onShowNote = (filename: string) => {
        if (webSocket === null) return;
        currentNote = {};
        webSocket.send(
            JSON.stringify({
                type: "show_note",
                data: {
                    filename: filename,
                },
            })
        );
    };
</script>

<div class="list-notes">
    <div
        class="notes-list fixed top-0 left-0 bottom-0 box-border w-64 px-3 py-1 bg-neutral overflow-y-auto"
    >
        <div class="notes-list-content">
            <NoteCards noteInfos={params} {onShowNote} />
        </div>
    </div>
    <div class="content fixed h-full box-border w-[calc(100%-320px)] left-64 overflow-y-auto">
        {#if currentNote && Object.keys(currentNote).length !== 0}
            <EditNote params={currentNote} />
        {/if}
    </div>
</div>
