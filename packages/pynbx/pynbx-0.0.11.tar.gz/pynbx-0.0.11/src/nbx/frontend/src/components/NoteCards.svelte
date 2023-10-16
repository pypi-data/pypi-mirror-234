<script lang="ts">
    export let noteInfos;
    export let onShowNote;

    let selectedNoteFilename: string;
    let titles: string[] = [];
    for (let noteInfo of noteInfos) {
        titles.push(noteInfo["title"]);
    }

    const onOpenNote = (filename: string) => {
        if (filename === selectedNoteFilename) {
            return;
        }
        selectedNoteFilename = filename;
        onShowNote(filename);
    };
</script>

<div class="note-cards flex flex-col">
    {#each noteInfos as noteInfo}
        <button
            class="note btn btn-outline btn-xs no-animation normal-case justify-start text-left inline-block rounded-sm bg-white mb-1 truncate"
            on:click={() => onOpenNote(noteInfo["filename"])}
            >{noteInfo["title"]}</button
        >
    {/each}
</div>
