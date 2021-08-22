import { Point } from "./Point";

/**
 * A 2D line.
 */
export class Line {
    private readonly _p1: Point;
    private readonly _p2: Point;
    public readonly length: number;

    constructor(p1: Point, p2: Point) {
        this._p1 = p1;
        this._p2 = p2;
        this.length = Math.sqrt(Math.pow(this.x2 - this.x1, 2) + Math.pow(this.y2 - this.y1, 2));
    }

    get p1(): Point {
        return this._p1;
    }

    get p2(): Point {
        return this._p2;
    }

    get start(): Point {
        return this.p1;
    }

    get end(): Point {
        return this.p2;
    }

    get x1(): number {
        return this.p1.x;
    }

    get x2(): number {
        return this.p2.x;
    }

    get y1(): number {
        return this.p1.y;
    }

    get y2(): number {
        return this.p2.y;
    }

    reversed(): Line {
        return new Line(this.p2, this.p1);
    }
}
