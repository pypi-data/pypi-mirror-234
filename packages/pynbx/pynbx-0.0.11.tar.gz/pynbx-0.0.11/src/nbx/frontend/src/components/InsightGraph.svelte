<script lang="ts">
    import { onMount } from "svelte";
    import { get } from "svelte/store";
    import Graph from "graphology";
    import Sigma from "sigma";
    import circular from "graphology-layout/circular";
    import forceLayout from "graphology-layout-force";
    import forceAtlas2 from "graphology-layout-forceatlas2";

    import { sessionState, webSocket } from "../stores";

    let divEl: HTMLDivElement = null;
    const graph = new Graph();
    let selectedNodes: string[];

    sessionState["insightGraph"].subscribe((graphData) => {
        graph.clear();
        selectedNodes = graphData["selectedNodes"];
        for (const node of graphData["nodes"]) {
            let color = "blue";
            if (selectedNodes.includes(node)) {
                color = "red";
            }
            graph.addNode(node, { size: 12, label: node, color });
        }
        for (const edge of graphData["edges"]) {
            graph.addEdge(edge[0], edge[1]);
        }
        const nodeSize = graphData["nodes"].length;
        if (nodeSize < 30) {
            circular.assign(graph);
        } else if (nodeSize >= 30 && nodeSize < 100) {
            forceLayout.assign(graph, 50);
        } else {
            forceAtlas2.assign(graph, 50);
        }
    });

    onMount(() => {
        const render = new Sigma(graph, divEl, {
            allowInvalidContainer: true,
        });

        render.on("clickNode", ({ node }) => {
            if (selectedNodes.includes(node)) {
                // deselect
                graph.setNodeAttribute(node, "color", "blue");
                const index = selectedNodes.indexOf(node);
                if (index > -1) {
                    selectedNodes.splice(index, 1);
                }
            } else {
                // select
                graph.setNodeAttribute(node, "color", "red");
                selectedNodes.push(node);
            }
            // update session state
            sessionState["insightGraph"].set({
                ...get(sessionState["insightGraph"]),
                selectedNodes,
            });
            // update session state in the python space
            webSocket.send(
                JSON.stringify({
                    "type": "update_insightGraph_node_selection",
                    selectedNodes,
                })
            );
        });
    });
</script>

<div bind:this={divEl} class="nbx-insight-graph" />

<style>
    .nbx-insight-graph {
        min-width: 512px;
        min-height: 512px;
        /* text-align need explicitly to be left, otherwise the inheried center will shift the canvas */
        text-align: left;
    }
</style>
