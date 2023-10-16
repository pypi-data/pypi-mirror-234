<script lang="ts">
    import type { Record } from "../types/record.type";

    export let record: Record;
    export let onClose: any;
    export let onClick: any;
</script>
<div class="card w-96 bg-base-100 card-bordered border-2 my-3">
    <div class="card-body">
        <h2 class="card-title toc-exclude">{record.heading}</h2>
        <p>{record.content}</p>
        <div class="card-actions justify-end">
            <button class="btn" on:click={onClick(record)}>Open</button>
            <button class="btn" on:click={onClose}>Close</button>
            <button class="btn btn-error">Irrelevant</button>
        </div>
    </div>
</div>

<style>
</style>
