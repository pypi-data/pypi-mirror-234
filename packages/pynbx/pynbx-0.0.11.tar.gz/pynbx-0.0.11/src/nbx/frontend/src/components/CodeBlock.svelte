<script lang="ts">
    import type { NodeViewProps } from "@tiptap/core";
    import { NodeViewWrapper, editable } from "svelte-tiptap";
    import { lowlight } from "lowlight/lib/common.js";

    export let updateAttributes: NodeViewProps["updateAttributes"];
    let selectedLanguage: string = "null";
</script>

<NodeViewWrapper class="code-block">
    <select
        class="select"
        bind:value={selectedLanguage}
        on:change={() => updateAttributes({ language: selectedLanguage })}
    >
        <option value="null"> auto </option>
        <option disabled> — </option>
        {#each lowlight.listLanguages() as lang}
            <option value={lang}>
                {lang}
            </option>
        {/each}
    </select>
    <div class="pre" use:editable>
        <code />
    </div>
</NodeViewWrapper>

<style>
    :global(.code-block) {
        position: relative;
    }
    :global(.code-block select) {
        position: absolute;
        right: 0.5rem;
        top: 0.5rem;
    }

    .pre {
        background: #0d0d0d;
        color: #fff;
        font-family: "JetBrainsMono", monospace;
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
    }
</style>
