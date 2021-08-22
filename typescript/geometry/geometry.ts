import { Line } from "./Line";
import { Point } from "./Point";

/**
 * @returns true if and only if the given line intersects the given point.
 */
export function lineIntersectsPoint(l: Line, p: Point): boolean {
    // straight horizontal and point between
    const lowX = Math.min(l.x1, l.x2);
    const highX = Math.max(l.x1, l.x2);
    const lowY = Math.min(l.y1, l.y2);
    const highY = Math.max(l.y1, l.y2);

    if ((highX - lowX) < 1 && lowX < p.x && p.x < highX) {
        return true;
    }
    if (lowY == highY && lowY < p.y && p.y < highY) {
        return true;
    }

    return _intersects(l.x1, l.y1, l.x2, l.y2, p.x, p.y, p.x, p.y);
}

/**
 * @returns true if and only if the given lines intersect.
 */
export function linesIntersect(l1: Line, l2: Line): boolean {
    return _intersects(l1.x1, l1.y1, l1.x2, l1.y2, l2.x1, l2.y1, l2.x2, l2.y2);
}

/**
 * @returns true if the line from (a,b)->(c,d) intersects with (p,q)->(r,s)
 */
function _intersects(a: number, b: number, c: number, d: number, p: number, q: number, r: number, s: number): boolean {
    const det = (c - a) * (s - q) - (r - p) * (d - b);
    if (det === 0) {
      return false;
    } else {
      const lambda = ((s - q) * (r - a) + (p - r) * (s - b)) / det;
      const gamma = ((b - d) * (r - a) + (c - a) * (s - b)) / det;
      return (0 < lambda && lambda < 1) && (0 < gamma && gamma < 1);
    }
  }
