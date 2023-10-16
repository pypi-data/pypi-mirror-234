<script lang="ts">
    import Mark from "mark.js";
    import { afterUpdate } from "svelte";

    import { sessionState } from "../stores";

    let statementHtmls: string[] = [];

    sessionState.statementHtmls.subscribe((val) => {
        statementHtmls = val;
    });

    afterUpdate(() => {
        sessionState["insightGraph"].subscribe(
            (graph: { selectedNodes: string[] }) => {
                let statementCards: HTMLElement = document.querySelector(
                    "div.statement-cards"
                );
                let marker = new Mark(statementCards);

                marker.unmark({
                    done: (marksTotal: number) => {
                        // display all statements back
                        let allStatements =
                            statementCards.children as HTMLCollectionOf<HTMLElement>;
                        for (let statement of allStatements) {
                            statement.hidden = false;
                        }

                        let markedStatements = [];
                        marker.mark(graph.selectedNodes, {
                            accuracy: "exactly",
                            each: (element: Element) => {
                                let statementElement: HTMLElement =
                                    element.closest(".statement");
                                markedStatements.push(statementElement);
                            },
                            done: (marksTotal: number) => {
                                if (marksTotal > 0) {
                                    let statementCards: HTMLElement =
                                        document.querySelector(
                                            "div.statement-cards"
                                        );
                                    let allStatements =
                                        statementCards.children as HTMLCollectionOf<HTMLElement>;
                                    let notMarkedStatements = [];
                                    for (let statement of allStatements) {
                                        if (
                                            !markedStatements.includes(
                                                statement
                                            )
                                        ) {
                                            notMarkedStatements.push(statement);
                                        }
                                    }
                                    for (let statement of notMarkedStatements) {
                                        statement.hidden = true;
                                    }
                                }
                            },
                        });
                    },
                });
            }
        );
    });
</script>

<div class="statement-cards flex flex-col">
    {#each statementHtmls as statementHtml}
        <div class="statement prose lg:prose-xl rounded-md bg-white mb-5 overflow-auto max-h-40 pl-1">{@html statementHtml}</div>
    {/each}
</div>
