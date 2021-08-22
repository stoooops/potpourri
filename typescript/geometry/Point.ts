/**
 * A 2D point
 */
export class Point {
    public readonly x: number;
    public readonly y: number;

    constructor(x: number, y: number) {
        this.x = x;
        this.y = y;
    }

    toString(): string {
        return `(${this.x}, ${this.y})`;
    }

    distance(p2: Point): number {
        return distance(this, p2);
    }

    // findClosest(candidates: Point[]): Point[] {
    //     let closest: Point[] = [];

    //     let dist = Number.MAX_SAFE_INTEGER;
    //     for (let i = 0; i < candidates.length; i++) {
    //         const p2 = candidates[i];
    //         if (this.x === p2.x && this.y === p2.y) {
    //             continue
    //         }
    //         const d = distance(this, p2);
    //         if (d < dist) {
    //             dist = d;
    //             closest = [];
    //             closest.push(p2);
    //         } else if (d == dist) {
    //             closest.push(p2);
    //         }
    //     }

    //     console.log(`Found num closest: ${closest.length}`)
    //     return closest;
    // }
}

export function distance(p1: Point, p2: Point): number {
    return Math.sqrt(Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2));
}
