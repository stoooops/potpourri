export class Queue<T> {
    _store: T[] = [];
    push(val: T): void {
        this._store.push(val);
    }
    pop(): T | undefined {
        return this._store.shift();
    }
    empty(): boolean {
        return this.size === 0;
    }
    get size(): number {
        return this._store.length;
    }
}
