import { Queue } from "../collections/Queue";
import { Line } from "../geometry/Line";
import { Point } from "../geometry/Point";
import { Graph, GraphImpl } from "./Graph";

/**
 * BFS from the given vertex outward
 *
 * @param vertex The vertex to start from.
 * @param graph The base graph to search.
 * @param sizeLimit The maximum number of vertices to check
 */
export function breadthFirstSearch(startVertex: Point, graph: Graph, sizeLimit: number): Graph {
    console.log(
        `BFS on (<V>=${graph.numVertices},<E>=${graph.numEdges},cc=${graph.numConnectedComponents}) from ${startVertex} until size ${sizeLimit}`
    );
    const vertices: Point[] = [];
    const edges: Line[] = [];

    // Mark all the vertices as not visited
    const visited: Map<string, boolean> = new Map();
    graph.vertices.forEach((v) => {
        visited.set(v.toString(), false);
    });

    const vertexQueue: Queue<Point> = new Queue();

    // Mark the current node as visited and enqueue it
    visited.set(startVertex.toString(), true);
    vertices.push(startVertex);
    vertexQueue.push(startVertex);

    while (!vertexQueue.empty() && vertices.length < sizeLimit) {
        // Dequeue next vertex to check
        const v: Point = vertexQueue.pop() as Point;

        // Get all adjacent vertices of the dequeued
        // vertex s. If a adjacent has not been visited,
        // then mark it visited and enqueue it
        const vertexEdges: Line[] = Array.from(graph.getEdges(v));
        for (let i = 0; i < vertexEdges.length; i++) {
            const edge: Line = vertexEdges[i];

            const other: Point = edge.opposite(v);
            const isVisited = visited.get(other.toString());
            console.log(`Visited ${other}: ${isVisited}`);
            if (!isVisited) {
                visited.set(other.toString(), true);
                if (vertices.length < sizeLimit) {
                    vertices.push(other);
                    edges.push(edge);
                }
                vertexQueue.push(other);
            }
        }
    }

    console.log(`BFS found <V> = ${vertices.length}, <E> = ${edges.length}`);
    vertices.forEach((v) => {
        console.log(v);
    });
    edges.forEach((e) => {
        console.log(e);
    });

    return new GraphImpl(vertices, edges);
}
