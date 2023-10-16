<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { Editor } from "@tiptap/core";
    import Document from "@tiptap/extension-document";
    import Paragraph from "@tiptap/extension-paragraph";
    import Text from "@tiptap/extension-text";
    import Highlight from "@tiptap/extension-highlight";
    import Placeholder from "@tiptap/extension-placeholder";
    import History from "@tiptap/extension-history";

    import { webSocket } from "../stores";

    let divEl: HTMLDivElement = null;
    let editor: Editor = null;

    const CustomDocument = Document.extend({
        addKeyboardShortcuts() {
            return {
                "Control-Enter": () => {
                    onTextAdd();
                    return true;
                },
            };
        },
    });

    onMount(() => {
        editor = new Editor({
            element: divEl,
            extensions: [
                CustomDocument,
                Paragraph,
                Text,
                Highlight,
                History.configure({
                    newGroupDelay: 200
                }),
                Placeholder.configure({
                    placeholder:
                        "Start from writing a short abstract of your idea",
                }),
            ],
            onTransaction: () => {
                // force re-render so `editor.isActive` works as expected
                editor = editor;
            },
        });
    });

    onDestroy(() => {
        if (editor) {
            editor.destroy();
        }
    });

    const onTextAdd = () => {
        if (editor.getText().trim().length > 0) {
            const statementHtml = editor.getHTML();
            // send to python backend for processing
            webSocket.send(
                JSON.stringify({
                    type: "save_statement",
                    statementHtml: statementHtml,
                })
            );
            editor.commands.clearContent(true);
        }
    };

    const highlight = (colorCode: string) => {
        // highlight selected texts
        editor.chain().focus().setHighlight({ color: colorCode }).run();
        // clear selection and stop highlighting new texts
        editor.chain().focus("end").unsetHighlight().run();
    };
</script>

<div bind:this={divEl} class="border-solid border-2 rounded-md my-6 mx-10 pl-1" />
{#if editor}
    <div class="flex justify-center gap-4">
        <button
            class="btn"
            on:click={() => highlight("#ffc078")}
            class:active={editor.isActive("highlight", { color: "#ffc078" })
                ? "is-active"
                : ""}
        >
            Label Entity
        </button>
        <button class="btn" on:click={onTextAdd}> Add to Graph </button>
    </div>
{/if}

<style>
    :global(.ProseMirror:focus) {
        outline: none;
    }

    :global(.nbx-editor .ProseMirror:focus) {
        outline: none;
    }

    /* Placeholder */
    :global(.nbx-editor .ProseMirror p.is-editor-empty:first-child::before) {
        content: attr(data-placeholder);
        float: left;
        color: #adb5bd;
        pointer-events: none;
        height: 0;
    }
</style>
