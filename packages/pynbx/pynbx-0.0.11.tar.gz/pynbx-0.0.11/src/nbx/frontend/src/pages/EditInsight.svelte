<script lang="ts">
    import InsightGraph from "../components/InsightGraph.svelte";
    import InsightEditor from "../components/InsightEditor.svelte";
    import StatementCards from "../components/StatementCards.svelte";
    import "boxicons";
</script>

<div class="edit-insight">
    <div class="insight-list fixed top-0 left-0 bottom-0 box-border w-64 px-3 py-1 bg-neutral overflow-y-auto">
        <div class="insight-list-header flex h-14 items-center justify-center	text-white">
            <box-icon name='bulb' color='#ffffff' ></box-icon>
            <h1 class="text-2xl">Insights</h1>
        </div>
        <div class="insight-list-content">
            <StatementCards />
        </div>
    </div>
    <div class="content fixed h-full box-border w-[calc(100%-320px)] left-64">
        <InsightGraph />
        <InsightEditor />
    </div>
</div>
