<script lang="ts">
    export let params: {
        noteContent?: string;
        noteTitle?: string;
        logs?: { [key: string]: string };
        filename?: string;
    };

    import Toc from "svelte-toc";
    import NoteEditor from "../components/NoteEditor.svelte";
    import NoteHistory from "../components/NoteHistory.svelte";
    import RecordCard from "../components/RecordCard.svelte";
    import { webSocket, sessionState, waitForOpenConnection } from "../stores";
    import type { Record } from "../types/record.type";
    import type { NoteView } from "../types/noteview.type";
    import { onMount } from "svelte";
    import { createMemoryHistory } from "history";
    import { WrappedHistory } from "../utils/history";

    const headingSelector: string = ":is(h2):not(.toc-exclude)";

    // Create own history instance.
    let history = new WrappedHistory(createMemoryHistory());

    let relevantRecords: Record[] = [];
    let connectedToBackend: boolean = false;
    let noteTitle: string = "";
    let noteContent: string = "";
    let noteEditor: NoteEditor;
    let allContent: { [key: string]: string } = {};
    // key is filename, value is object that contains current note view information, e.g. cursor position, scrollbar position
    let notesViewInfo: {[key: string]: NoteView} = {};
    let headings: HTMLHeadingElement[] = [];

    //  set when this component is rendered
    let originalNote = {
        filename: params.filename
    };

    // to support clicked prompts history
    let clickedRecord: Record;
    let disabledBackButton = false;
    let disabledForwardButton = true;

    onMount(() => {
        sessionState.relevantRecords.subscribe((val) => {
            relevantRecords = val;
        });

        sessionState.connectedToBackend.subscribe((val) => {
            connectedToBackend = val;
        });
    });

    const requery_headings = () => {
        if (typeof document === `undefined`) {
            return;
        }
        headings = [...document.querySelectorAll(headingSelector)] as HTMLHeadingElement[];
    }

    const updateNoteView = (info: Partial<NoteView>) => {
        // update note view information
        let currentNoteViewInfo = notesViewInfo[params.filename] || {
            cursorPosition: -1, // the cursor position in editor
            scrollPosition: -1, // scroll position in the window
        };
        let update = {
            [params.filename]: {
                ...currentNoteViewInfo,
                ...info
            }
        }
        notesViewInfo = {
            ...notesViewInfo,
            ...update
        };
    }

    const onNoteSave = () => {
        if (webSocket === null) return;
        webSocket.send(
            JSON.stringify({
                type: "save_note",
            })
        );

        noteEditor?.resetFocus(notesViewInfo[params.filename].cursorPosition);
    };

    const onNoteCancel = () => {
        if (webSocket === null) return;
        webSocket.send(
            JSON.stringify({
                type: "exit",
            })
        );
        setTimeout(window.close, 100);
    };

    const onNoteUpdate = (textContent: string, fullContent: string, updateType: string, currentCursorPos: number) => {
        requery_headings()
        if (updateType === "noteContent") { // only update cursor position while updating note content
            updateNoteView({
                cursorPosition: currentCursorPos,
                scrollPosition: document.documentElement.scrollTop || document.body.scrollTop
            });
        }

        if (webSocket === null) return;
        webSocket.send(JSON.stringify({
            "type": "update_note",
            "data": {
                "input": textContent,
                "content": fullContent,
                "updateType": updateType,
            }
        }));
    }

    const onImageUpload = (imgBase64: string) => {
        const imgData = imgBase64.split(",");
        webSocket.send(
            JSON.stringify({
                type: "upload_image",
                data: {
                    image: imgData[1],
                },
            })
        );
    };

    const onShowNote = (filename: string) => {
        if (webSocket === null) return;
        webSocket.send(
            JSON.stringify({
                type: "show_note",
                data: {
                    filename: filename,
                },
            })
        );
    };

    const onAbstractClose = (index: number) => {
        const func = () => {
            const pre_slice = relevantRecords.slice(0, index);
            const pos_slice = relevantRecords.slice(index + 1);
            relevantRecords = pre_slice.concat(pos_slice);
        };
        return func;
    };

    const onPromptClick = (record: Record) => {
        if (record === clickedRecord) {
            return;
        }
        // switch the note content
        onShowNote(record.filename);
        // save the clicked record state
        clickedRecord = record;

        // save the state to self-managed history
        history.push("", record);
    };

    const goBack = () => {
        history.back();
    };

    const goForward = () => {
        history.forward();
    };

    $: {
        if (params.noteContent && noteContent !== params.noteContent) {
            // noteContent is changed from params, this means noteEditor needs to reset to a new content
            noteEditor?.resetContent(params.noteContent);
            noteContent = params.noteContent;
        }

        if (params.noteTitle && noteTitle !== params.noteTitle) {
            noteEditor?.resetTitle(params.noteTitle);
            noteTitle = params.noteTitle;
        }

        // evaluate the content history
        if (params.logs && allContent !== params.logs) {
            allContent = params.logs;
        }

        if (clickedRecord) {
            // need to scroll the window to the target tag location
            let allTargetTags = [
                ...document.getElementsByTagName(clickedRecord.headingType),
            ] as HTMLElement[];
            for (let [idx, element] of allTargetTags.entries()) {
                if (idx === clickedRecord.headingIdx) {
                    window.scrollTo({
                        top: element.offsetTop,
                        behavior: "smooth",
                    });
                }
            }
        } else if (originalNote.filename === params.filename) {
            if (notesViewInfo[params.filename]) {
                // go back to orignal note's scroll location
                window.scrollTo({
                    top: notesViewInfo[params.filename].scrollPosition,
                    behavior: "smooth",
                });

                noteEditor?.resetFocus(notesViewInfo[params.filename].cursorPosition);
            }
        }

        // evaluate the forward/back button state
        disabledBackButton = !history.canBack();
        disabledForwardButton = !history.canForward();
    }

    history.listen(({ action, location }) => {
        // The current location changed.

        let record: Record | null = location.state as Record | null;
        if (record) {
            // switch the note content
            onShowNote(record.filename);
            // save the clicked record state
            clickedRecord = record;
        } else {
            // this might because user try to go back to the orignal note, thus load the orignal note and scroll to saved location
            onShowNote(originalNote.filename);
            // no record is clicked at this moment
            clickedRecord = undefined;
        }
    });
</script>

<div class="edit-note">
    <div class="fixed top-0 w-full h-8 pl-5 flex gap-4">
        <button
            class="disabled:opacity-40"
            disabled={disabledBackButton}
            on:click={goBack}
        >
            <box-icon class="" name="left-arrow-alt" />
        </button>
        <button
            class="disabled:opacity-40"
            disabled={disabledForwardButton}
            on:click={goForward}
        >
            <box-icon name="right-arrow-alt" />
        </button>
    </div>
    <div class="sidebar fixed top-8 bottom-0 left-0 w-64">
        <Toc
            --toc-li-padding="0.5em"
            --toc-max-height="calc(100vh - 2rem)"
            title="Table of content"
            titleTag="strong"
            headingSelector={headingSelector}
            headings={headings}
        />
    </div>
    <div class="mt-8">
        <NoteEditor
            bind:this={noteEditor}
            onSave={onNoteSave}
            onCancel={onNoteCancel}
            onUpdate={onNoteUpdate}
            {onImageUpload}
            editable={connectedToBackend}
            title={noteTitle}
            content={noteContent}
        />
    </div>
    <div class="recordcards fixed top-8 right-0 bottom-0 overflow-y-auto">
        {#each relevantRecords as record, index}
            <RecordCard
                {record}
                onClose={onAbstractClose(index)}
                onClick={onPromptClick}
            />
        {/each}
    </div>

    {#key allContent}
        <NoteHistory content={allContent} />
    {/key}
</div>

<svelte:window on:load={async () => {
    if (!connectedToBackend) {
        if (webSocket === null || webSocket.readyState !== webSocket.OPEN) {
            try {
                await waitForOpenConnection(webSocket);
                webSocket.send(JSON.stringify({
                    "type": "exit"
                }));
            } catch (err) { console.error(err); }
        } else {
            webSocket.send(JSON.stringify({
                    "type": "exit"
            }));
        }
    }
}}/>

<style>
    @keyframes pop {
        0% {
            transform: scale(0.9);
            opacity: 0;
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }
    :global(.recordcards > *) {
        animation: pop 0.25s ease-out;

        /* hide scrollbar */
        -ms-overflow-style: none;
        overflow: -moz-scrollbars-none;
        scrollbar-width: none;
    }

    :global(.sidebar nav) {
        height: calc(100vh - 2rem);
    }

    .recordcards::-webkit-scrollbar {
        display: none; /* Safari and Chrome */
    }
</style>
