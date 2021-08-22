/**
 * @returns a pseudorandom number between 0 and 1
 */
export function randFloat(): number {
    return Math.random();
}

/**
 * @returns a pseudorandom integer between 0 and given max
 */
export function randInt(max: number): number {
    return Math.floor(Math.random() * max);
}
