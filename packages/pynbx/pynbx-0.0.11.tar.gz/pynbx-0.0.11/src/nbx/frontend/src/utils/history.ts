
import type { BrowserHistory, Location, To, Listener, MemoryHistory, HashHistory } from "history";

// a wrapper of npm history package
export class WrappedHistory {
    newestLocation: Location;

    constructor(public history: BrowserHistory | HashHistory | MemoryHistory) { }

    canForward(): boolean {
        // whether it can go forward or not
        return this.newestLocation && this.newestLocation !== this.history.location;
    }

    canBack(): boolean {
        // whether it can go back or not
        return !!this.history.location.state;
    }

    forward(): void {
        this.history.forward();
    }

    back(): void {
        this.history.back();
    }

    push(to: To, state?: any): void {
        this.history.push(to, state);
        this.newestLocation = this.history.location;
    }

    listen(listener: Listener): () => void {
        return this.history.listen(listener);
    }
}
