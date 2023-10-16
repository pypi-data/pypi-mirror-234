<script lang="ts">
    export let onSave;
    export let onCancel;
    export let onUpdate;
    export let onImageUpload;
    export let editable;
    export let title: string;
    export let content: string;

    export const resetContent = (newContent) => {
        contentEditor?.commands.setContent(newContent);
    }

    export const resetTitle = (newTitle) => {
        titleEditor?.commands.setContent(newTitle);
    }

    import "highlight.js/styles/github-dark.css";
    import { onMount, onDestroy } from "svelte";
    import { SvelteNodeViewRenderer } from 'svelte-tiptap';
    import { lowlight } from "lowlight/lib/common.js";
    import { Editor } from "@tiptap/core";
    import Bold from "@tiptap/extension-bold";
    import BubbleMenu from "@tiptap/extension-bubble-menu";
    import Code from "@tiptap/extension-code";
    import CodeBlockLowlight from "@tiptap/extension-code-block-lowlight";
    import Document from "@tiptap/extension-document";
    import Dropcursor from "@tiptap/extension-dropcursor";
    import FloatingMenu from "@tiptap/extension-floating-menu";
    import Heading from "@tiptap/extension-heading";
    import History from "@tiptap/extension-history";
    import Image from "@tiptap/extension-image";
    import Link from "@tiptap/extension-link";
    import ListItem from "@tiptap/extension-list-item";
    import OrderedList from "@tiptap/extension-ordered-list";
    import Paragraph from "@tiptap/extension-paragraph";
    import Placeholder from "@tiptap/extension-placeholder";
    import Strike from "@tiptap/extension-strike";
    import Text from "@tiptap/extension-text";

    import { sessionState } from "../stores";
    import CodeBlock from './CodeBlock.svelte';

    let contentDivEl: null | HTMLElement = null;
    let titleDivEl: null | HTMLElement = null;
    let contentEditor: null | Editor = null;
    let titleEditor: null | Editor = null;
    let textBubbleMenuEl: null | HTMLElement = null;
    let floatingMenuEl: null | HTMLElement = null;
    let imageInput: null | HTMLElement = null;

    let images;

    const TitleDocument = Document.extend({
        addKeyboardShortcuts() {
            return {
                "Enter": () => {
                    contentEditor?.commands.focus('end');
                    return true;
                },
            };
        }
    });

    export const resetFocus = (pos: number | undefined) => {
        if (!!pos) {
            contentEditor?.commands.focus(pos);
        } else {
            contentEditor?.commands.focus();
        }
    }

    const onContentUpdate = (e) => {
        const editorNode = e.transaction.curSelection.$cursor?.nodeBefore;
        const textContent = editorNode ? editorNode.textContent : "";
        onUpdate(textContent, contentEditor.getHTML(), "noteContent", e.transaction.curSelection.$cursor?.pos);
    };

    const onTitleUpdate = (e) => {
        console.log(e);
        const editorNode = e.transaction.curSelection.$cursor?.nodeBefore;
        const textContent = editorNode ? editorNode.textContent : "";
        onUpdate(textContent, titleEditor.getHTML(), "noteTitle");
    }

    const getBase64 = (image) => {
        const reader = new FileReader();
        reader.readAsDataURL(image);
        reader.onload = (e) => {
            image = e.target.result;
            onImageUpload(image);
        };
    };

    sessionState.uploadedImageUrl.subscribe((val) => {
        // remove the "/" character
        const currentCursorPos = contentEditor?.state.selection.$anchor.pos;
        contentEditor?.commands.deleteRange({
            from: currentCursorPos - 1,
            to: currentCursorPos,
        });

        // insert image
        let uploadedImageUrl = val;
        contentEditor?.chain().focus().setImage({ src: uploadedImageUrl }).run();
    });

    onMount(() => {
        contentEditor = new Editor({
            element: contentDivEl,
            editorProps: {
                attributes: {
                    class: "focus:outline-none container mx-auto prose",
                },
                editable: () => editable,
            },
            extensions: [
                BubbleMenu.configure({
                    pluginKey: "text-bubble-menu",
                    element: textBubbleMenuEl,
                    shouldShow: ({ editor, view, state, from, to }) => {
                        // don't show for images
                        if (editor.isActive("image")) {
                            return false;
                        }

                        const isHeading = editor.isActive("heading");
                        const isCodeblock = editor.isActive("codeBlock");
                        return !(
                            state.selection.empty ||
                            !editable ||
                            isHeading ||
                            isCodeblock
                        );
                    },
                }),
                FloatingMenu.configure({
                    pluginKey: "commands-menu",
                    element: floatingMenuEl,
                    tippyOptions: {
                        duration: 100,
                    },
                    shouldShow: ({ editor, view, state, oldState }) => {
                        const { selection } = state;
                        const { $anchor, empty } = selection;
                        const isRootDepth = $anchor.depth === 1;
                        const isTextBlock = $anchor.parent.isTextblock;
                        const isSlashCharacter =
                            ($anchor.parentOffset > 0
                                ? $anchor.parent.textContent.charAt(
                                      $anchor.parentOffset - 1
                                  )
                                : "") === "/";
                        if (
                            !view.hasFocus() ||
                            !empty ||
                            !isRootDepth ||
                            !isTextBlock ||
                            !isSlashCharacter
                        ) {
                            return false;
                        }
                        return true;
                    },
                }),
                Bold,
                Code,
                CodeBlockLowlight.extend({
                    addNodeView() {
                        return SvelteNodeViewRenderer(CodeBlock);
                    },
                    addKeyboardShortcuts() {
                        return {
                            // allows to insert tabs while editing the text in code block
                            Tab: () => {
                                if (this.editor.isActive("codeBlock")) {
                                    return this.editor.commands.insertContent(
                                        "\t"
                                    );
                                }
                            },
                        };
                    },
                }).configure({
                    lowlight,
                }),
                Document,
                Dropcursor,
                Image.configure({
                    allowBase64: true,
                }),
                ListItem,
                Link,
                OrderedList,
                Strike,
                Heading.configure({
                    levels: [2],
                }),
                History.configure({
                    newGroupDelay: 200,
                }),
                Paragraph,
                Placeholder.configure({
                    placeholder: "Write something here...",
                }),
                Text,
            ],
            onUpdate: onContentUpdate,
            onTransaction: () => {
                // force re-render so `editor.isActive` works as expected
                contentEditor = contentEditor;
            },
        });
        contentEditor.commands.setContent(content);

        titleEditor = new Editor({
            element: titleDivEl,
            editorProps: {
                attributes: {
                    class: "focus:outline-none container mx-auto prose",
                },
                editable: () => editable,
            },
            extensions: [
                TitleDocument,
                Text,
                Heading.configure({
                    levels: [1],
                }),
                Placeholder.configure({
                    placeholder: "Untitled note...",
                }),
            ],
            onUpdate: onTitleUpdate,
            onTransaction: () => {
                // force re-render so `titleEditor.isActive` works as expected
                titleEditor = titleEditor;
            },
        });
        titleEditor.commands.setContent(title);
    });

    onDestroy(() => {
        if (contentEditor) {
            contentEditor.destroy();
        }
        if (titleEditor) {
            titleEditor.destroy();
        }
    });

    const onSaveLogic = () => {
        onSave(contentEditor.getHTML());
    };

    const onCancelLogic = () => {
        onCancel();
    };
</script>

<div class="text-menu" bind:this={textBubbleMenuEl}>
    <button
        class="text-menu-item"
        on:click={() => contentEditor.chain().focus().toggleBold().run()}
        class:active={contentEditor && contentEditor.isActive("bold")}
    >
        bold
    </button>
    <button
        class="text-menu-item"
        on:click={() => contentEditor.chain().focus().toggleCode().run()}
        class:active={contentEditor && contentEditor.isActive("code")}
    >
        code
    </button>
    <button
        class="text-menu-item"
        on:click={() => contentEditor.chain().focus().toggleStrike().run()}
        class:active={contentEditor && contentEditor.isActive("strike")}
    >
        strike
    </button>
</div>

<div class="commands-menu" bind:this={floatingMenuEl}>
    <button
        class="commands-menu-item"
        on:click={() => imageInput.click()}
        class:active={contentEditor && contentEditor.isActive("image")}
    >
        Image
    </button>
</div>

<div bind:this={titleDivEl} />
<br/>
<div bind:this={contentDivEl} />

{#if contentEditor}
    <div class="flex justify-center ... gap-4" style="padding-top: 32px">
        {#if editable}
            <button on:click={onSaveLogic} class="btn"> Save </button>
            <button on:click={onCancelLogic} class="btn"> Close </button>
        {:else}
            <button on:click={onCancelLogic} class="btn"> Close </button>
        {/if}
    </div>
    <input
        class="hidden"
        type="file"
        accept=".png,.jpg"
        bind:files={images}
        bind:this={imageInput}
        on:change={() => getBase64(images[0])}
    />
{/if}

<style>
    /* Title Placeholder */
    :global(.ProseMirror h1.is-editor-empty:first-child::before) {
        content: attr(data-placeholder);
        float: left;
        color: #adb5bd;
        pointer-events: none;
        height: 0;
    }
    /* Content Placeholder */
    :global(.ProseMirror p.is-editor-empty:first-child::before) {
        content: attr(data-placeholder);
        float: left;
        color: #adb5bd;
        pointer-events: none;
        height: 0;
    }

    :global(img.ProseMirror-selectednode) {
        outline: 3px solid #68cef8;
    }

    .commands-menu {
        display: flex;
        flex-direction: column;
        padding: 0.2rem;
        position: relative;
        border-radius: 0.5rem;
        background: rgb(240, 240, 240);
        color: rgba(0, 0, 0, 0.8);
        overflow: hidden;
        font-size: 0.9rem;
        box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.05),
            0px 10px 20px rgba(0, 0, 0, 0.1);
    }

    .commands-menu-item {
        display: block;
        margin: 0;
        width: 100%;
        text-align: left;
        background: transparent;
        border-radius: 0.4rem;
        border: 1px solid transparent;
        padding: 0.2rem 0.4rem;
    }

    .commands-menu-item:hover {
        border: 2px solid gray;
    }

    .text-menu {
        display: flex;
        flex-direction: row;
        padding: 0.2rem;
        position: relative;
        border-radius: 0.5rem;
        background: rgb(240, 240, 240);
        color: rgba(0, 0, 0, 0.8);
        overflow: hidden;
        font-size: 0.9rem;
        box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.05),
            0px 10px 20px rgba(0, 0, 0, 0.1);
    }

    .text-menu-item {
        display: block;
        margin: 0;
        width: 100%;
        text-align: left;
        background: transparent;
        border: 1px solid transparent;
        padding: 0.2rem 0.4rem;
        border-left: 1px solid gray;
        opacity: 0.7;
    }

    .text-menu .text-menu-item:first-child {
        border-left: none;
    }

    .text-menu-item:hover {
        opacity: 1;
    }
</style>
