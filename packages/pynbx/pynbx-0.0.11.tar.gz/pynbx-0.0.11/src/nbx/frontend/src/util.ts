import type { Writable } from "svelte/store";

export const loadWritable = (writable: Writable<any>) => {
    let val: any;
    writable.subscribe((value: any) => {
        val = value;
    });
    return val;
}


export const formatTimestamp = (timestamp: string) => {
    const strs = timestamp.split("-");
    return `${strs[0]}-${strs[1]}-${strs[2]} ${strs[3]}:${strs[4]}:${strs[5]}`
};
