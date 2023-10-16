<script lang="ts">
    import CommandPalette, { defineActions, createStoreMethods } from 'svelte-command-palette';

     // define actions using the defineActions API
    const commands = defineActions([
        {
            actionId: 1,
            title: "Open Svelte Command Palette on github",
            subTitle: "This opens github in a new tab!",
            onRun: ({ action, storeProps, storeMethods }) => {
                if (!storeProps.isVisible) {
                    return;
                }
                window.open("https://github.com/rohitpotato/svelte-command-palette");
            },
            shortcut: "Space k"
        }
    ]);
</script>

<CommandPalette {commands}/>
