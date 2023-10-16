<script lang="ts">
    export let content: { [key: string]: string };

    import NoteDiff from "./NoteDiff.svelte";
    import { formatTimestamp } from "../util";

    let selectedDate: string = "";

    const onDateClick = (date: string) => {
        selectedDate = date;
    };

    const updateDates: string[] = [];
    for (const updateDate of Object.keys(content)) {
        updateDates.push(updateDate);
    }
    updateDates.sort().reverse();

</script>

<div class="history">
    <div>History</div>
    <ul>
        {#each updateDates as updateDate, index}
            <li>
                Version {updateDates.length-index}: <button class="link" on:click={()=>{onDateClick(updateDate)}}>{formatTimestamp(updateDate)}</button>
            </li>
        {/each}
    </ul>
</div>
{#each updateDates as date, index}
    {#if selectedDate === date}
        <NoteDiff
            oldStr={index === updateDates.length-1 ? "" : content[updateDates[index+1]]}
            oldTitle={index === updateDates.length-1 ? "Scratch": formatTimestamp(updateDates[index+1])}
            newStr={content[date]}
            newTitle={formatTimestamp(date)}
        />
    {/if}
{/each}

<style>
    .history {
        text-align: center
    }
</style>
