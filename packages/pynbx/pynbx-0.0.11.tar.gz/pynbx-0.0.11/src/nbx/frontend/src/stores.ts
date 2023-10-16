import deepEqual from "deep-equal";
import { get, writable } from "svelte/store";

export const baseUrl = "http://localhost:8000/";

// the state within app.py is the source of truth
export const sessionState = {
    "routing": writable({"page": "", "params": {}}),
    // EditNote
    "relevantRecords": writable([]),
    "uploadedImageUrl": writable(""),
    "noteTitle": writable(""),
    "noteContent": writable(""),
    // EditInsight
    "insightGraph": writable({
        "nodes": [],
        "edges": [],
        "selectedNodes": []
    }),
    "statementHtmls": writable([]),
    // ListNotes
    "selectedNoteIdx": writable(-1),
    // Network Connection
    "connectedToBackend": writable(true)
};

export const initSessionState = (initState: any) => {
    for (const stateKey in initState) {
        const stateVal = initState[stateKey];
        if (!(stateKey in sessionState)) {
            //@TODO Warning LOG
            continue;
        }
        sessionState[stateKey].set(stateVal);
    }
};

export let webSocket: WebSocket = null;
export const setupWebSocket = (url: string) => {
    webSocket = new WebSocket(url);
    webSocket.onmessage = (wsEvent: { data: string }) => {
        const newSessionState = JSON.parse(wsEvent.data);
        for (const stateKey in newSessionState) {
            const stateVal = newSessionState[stateKey];
            if (stateKey in sessionState) {
                if (!deepEqual(stateVal, get(sessionState[stateKey]))) {
                    sessionState[stateKey].set(stateVal);
                }
            } else {
                sessionState[stateKey] = writable(stateVal);
            }
        }
    };
    webSocket.onclose = () => {
        sessionState["connectedToBackend"].set(false);
    }
};

// wait a configurable period time till websocket is opened
export const waitForOpenConnection = (socket: WebSocket, maxNumberOfAttempts: number = 20, intervalTime: number = 200) => {
    return new Promise<void>((resolve, reject) => {
        let currentAttempt = 0;
        const interval = setInterval(() => {
            if (currentAttempt > maxNumberOfAttempts - 1) {
                clearInterval(interval);
                reject(new Error('Maximum number of attempts exceeded'));
            } else if (socket.readyState === socket.OPEN) {
                clearInterval(interval)
                resolve()
            }
            currentAttempt++;
        }, intervalTime);
    });
};
