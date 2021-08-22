import { makeSet, union, find } from "@manubb/union-find";
import { Line } from "../geometry/Line";
import { Point } from "../geometry/Point";

/**
 * This relies on the union-find library: https://www.npmjs.com/package/@manubb/union-find
 */

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
    hasEdge(edge: Line): boolean;
    removeEdge(edges: Line);
    removeEdges(edges: Set<Line>);

    isConnected(v1: Point, v2: Point): boolean;
    isDisjoint(v1: Point, v2: Point): boolean;

    // in progress
    getConnectedComponents(): Set<Graph>;
}

/**
 * A implementation of a Graph.
 */
export class GraphImpl implements Graph {
    /**
     * Unique set of vertices, unsorted.
     */
    private readonly _vertices: Set<Point>;
    /**
     * Unique set of edges, unsorted.
     */
    private readonly _edges: Set<Line>;

    /**
     * Map from vertex to its set of edgdes.
     */
    private readonly _vertexToEdges: WeakMap<Point, Set<Line>>;

    /**
     * Map from vertex to connected component root.
     */
    private readonly _unions: WeakMap<Point, unknown>;

    /**
     * The number of connected components.
     */
    private _numConnectedComponents: number;

    constructor(vertices: Set<Point> | Point[], edges: Set<Line> | Line[]) {
        this._vertices = new Set<Point>();
        this._edges = new Set<Line>();
        this._unions = new WeakMap();
        this._numConnectedComponents = 0;

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
        return this._numConnectedComponents;
    }

    getConnectedComponents(): Set<Graph> {
        const result = new Set<Graph>();

        //////////////////////////////////////////////////////////////////////////////////////////
        // group vertices by connected component
        const verticesByConnectedComponent: Map<unknown, Set<Point>> = new Map();
        const edgesByConnectedComponent: Map<unknown, Set<Line>> = new Map();
        this.vertices.forEach((v) => {
            const rootUnion = this.treeRoot(v);
            // console.log(rootUnion);
            const existingVertices: Set<Point> = verticesByConnectedComponent.get(rootUnion) || new Set<Point>();
            existingVertices.add(v);
            verticesByConnectedComponent.set(rootUnion, existingVertices);

            const existingEdges: Set<Line> = edgesByConnectedComponent.get(rootUnion) || new Set<Line>();
            const vertexEdges: Set<Line> = this.getEdges(v);
            vertexEdges.forEach((e) => {
                existingEdges.add(e);
            });
            edgesByConnectedComponent.set(rootUnion, existingEdges);
        });
        if (this.numConnectedComponents !== verticesByConnectedComponent.size) {
            throw Error(
                `Invalid state. this.numConnectedComponents = ${this.numConnectedComponents}, but found ${verticesByConnectedComponent.size} from vertices roots`
            );
        }
        //////////////////////////////////////////////////////////////////////////////////////////

        console.log(`Found ${this.numConnectedComponents} connected components`);
        verticesByConnectedComponent.forEach((vertices, root, map) => {
            const edges: Set<Line> = edgesByConnectedComponent.get(root) as Set<Line>;
            console.log(`Found connected component with ${vertices.size} vertices and ${edges.size}`);
            const connectedComponent: Graph = new GraphImpl(vertices, edges);
            result.add(connectedComponent);
        });

        return result;
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
        // add vertex with no edges
        this._unions.set(vertex, makeSet());
        this._numConnectedComponents++;
    }

    addEdge(edge: Line): void {
        if (this.hasEdge(edge)) {
            throw `Already contains edge: ${edge}`;
        }
        this._edges.add(edge);
        this._vertexToEdges.get(edge.p1)?.add(edge);
        this._vertexToEdges.get(edge.p2)?.add(edge);
        this.unionEdge(edge);
    }

    private unionEdge(edge: Line): void {
        if (!this.isConnected(edge.p1, edge.p2)) {
            // points were not previously connected, so this connects two subgraphs
            this._numConnectedComponents--;
        }
        // update the union pointer
        union(this._unions.get(edge.p1), this._unions.get(edge.p2));
    }

    getEdges(vertex: Point): Set<Line> {
        return this._vertexToEdges.get(vertex) as Set<Line>;
    }

    hasEdge(edge: Line): boolean {
        return this.edges.has(edge) || this.edges.has(edge.reversed());
    }

    private rebuildUnionFind() {
        this._numConnectedComponents = 0;
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

    treeRoot(v: Point): any {
        if (v === undefined) {
            throw `Bad input: ${v}`;
        }
        const obj: unknown = this._unions.get(v);
        if (obj === undefined) {
            throw `Missing: ${v}`;
        }
        return find(obj);
    }

    isConnected(v1: Point, v2: Point): boolean {
        return this.treeRoot(v1) === this.treeRoot(v2);
    }

    isDisjoint(v1: Point, v2: Point): boolean {
        return !this.isConnected(v1, v2);
    }
}
