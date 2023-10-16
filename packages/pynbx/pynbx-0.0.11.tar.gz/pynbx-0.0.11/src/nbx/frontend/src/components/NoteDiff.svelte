<script lang="ts">
    export let oldStr: string;
    export let oldTitle: string;
    export let newStr: string;
    export let newTitle: string;

    import { createTwoFilesPatch } from "diff";
    import * as Diff2html from "diff2html";
    import 'diff2html/bundles/css/diff2html.min.css'

    const diff = createTwoFilesPatch(oldTitle, newTitle, oldStr, newStr);
    const diffHtml: string = Diff2html.html(diff,
        {matching: "words", drawFileList: false, outputFormat: "side-by-side"}
    );

</script>

<div class="note-diff">
    {@html diffHtml}
</div>

<style>
    .note-diff {
        border: 1px solid black;
    }
</style>
