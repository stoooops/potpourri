import { makeSet, union, find } from "@manubb/union-find";
import { Line } from "../geometry/Line";
import { Point } from "../geometry/Point";

/**
 * A Graph interface, modeling Graph Theory primitives.
 */
export interface Graph {
    vertices: Set<Point>;
    edges: Set<Line>;
    numVertices: number;
    numEdges: number;
    numConnectedComponents: number;

    addVertex(vertex: Point): void;
    addEdge(edge: Line): void;

    getEdges(vertex: Point): Set<Line>;
    removeEdge(edges: Line);
    removeEdges(edges: Set<Line>);

    isConnected(v1: Point, v2: Point): boolean;
    isDisjoint(v1: Point, v2: Point): boolean;
}

/**
 * A implementation of a Graph.
 */
export class GraphImpl implements Graph {
    private readonly _vertices: Set<Point>;
    private readonly _edges: Set<Line>;

    private readonly _vertexToEdges: WeakMap<Point, Set<Line>>;

    private readonly _unions: WeakMap<Point, unknown>;
    private _numComponents: number;

    constructor(vertices: Set<Point>, edges: Set<Line>) {
        this._vertices = new Set<Point>();
        this._edges = new Set<Line>();
        this._unions = new WeakMap();
        this._numComponents = 0;

        this._vertexToEdges = new WeakMap();

        vertices.forEach((v) => {
            this.addVertex(v);
        });
        edges.forEach((e) => {
            this.addEdge(e);
        });
    }

    get vertices(): Set<Point> {
        return this._vertices;
    }

    get numVertices(): number {
        return this._vertices.size;
    }

    get edges(): Set<Line> {
        return this._edges;
    }

    get numEdges(): number {
        return this._edges.size;
    }

    get numConnectedComponents(): number {
        return this._numComponents;
    }

    addVertex(vertex: Point): void {
        if (this._vertices.has(vertex)) {
            throw `Already contains vertex: ${vertex}`;
        }
        this._vertices.add(vertex);
        this._vertexToEdges.set(vertex, new Set());
        this.unionVertex(vertex);
    }

    private unionVertex(vertex: Point): void {
        this._unions.set(vertex, makeSet());
        this._numComponents++;
    }

    addEdge(edge: Line): void {
        if (this._edges.has(edge) || this._edges.has(edge.reversed())) {
            throw `Already contains edge: ${edge}`;
        }
        this._edges.add(edge);
        this._vertexToEdges.get(edge.p1)?.add(edge);
        this._vertexToEdges.get(edge.p2)?.add(edge);
        this.unionEdge(edge);
    }

    private unionEdge(edge: Line): void {
        if (!this.isConnected(edge.p1, edge.p2)) {
            this._numComponents--;
        }
        union(this._unions.get(edge.p1), this._unions.get(edge.p2));
    }

    getEdges(vertex: Point): Set<Line> {
        return this._vertexToEdges.get(vertex) as Set<Line>;
    }

    private rebuildUnionFind() {
        this._numComponents = 0;
        this._vertices.forEach((v) => {
            this.unionVertex(v);
        });
        this._edges.forEach((e) => {
            this.unionEdge(e);
        });
    }

    removeEdge(edge: Line): void {
        this.removeEdges(new Set([edge]));
    }

    // O(v) + O(e) unions
    removeEdges(edges: Set<Line>): void {
        edges.forEach((e) => {
            this._edges.delete(e);
            this._vertexToEdges.get(e.p1)?.delete(e);
            this._vertexToEdges.get(e.p2)?.delete(e);
        });
        this.rebuildUnionFind();
    }

    isConnected(v1: Point, v2: Point): boolean {
        if (v1 === undefined) {
            throw `Bad input v1: ${v1}`;
        }
        if (v2 === undefined) {
            throw `Bad input v2: ${v2}`;
        }
        const obj1: unknown = this._unions.get(v1);
        if (obj1 === undefined) {
            throw `Missing: ${v1}`;
        }
        const obj2: unknown = this._unions.get(v2);
        if (obj2 === undefined) {
            throw `Missing: ${v2}`;
        }
        return find(obj1) === find(obj2);
    }

    isDisjoint(v1: Point, v2: Point): boolean {
        return !this.isConnected(v1, v2);
    }
}
