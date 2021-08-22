import seedrandom from "seedrandom";

// /**
//  * @returns a pseudorandom number between 0 and 1
//  */
// export function randFloat(): number {
//     return Math.random();
// }

const _seedrands = new Map();
const _seedrandVals: Map<string, number[]> = new Map();

interface _seedrandFloatInput {
    seed: string;
    index: number;
}

export function seedrandFloat(input: _seedrandFloatInput): number {
    const seed: string = input.seed;
    const index = input.index;

    // get rng
    let rng = _seedrands.get(seed);
    if (rng === undefined) {
        console.debug(`Seed rng: ${seed}`);
        rng = seedrandom(seed);
        _seedrands.set(seed, rng);
        _seedrandVals.set(seed, []);
    }
    let vals = _seedrandVals.get(seed) as number[];

    // fill up vals
    for (let i = vals.length; i <= index; i++) {
        vals[i] = rng();
    }
    return vals[index];
}

interface _seedrandIntInput extends _seedrandFloatInput {
    max: number;
}

/**
 * @returns a pseudorandom integer between 0 and given max
 */
export function seedrandInt(seedrandIntInput: _seedrandIntInput): number {
    return Math.floor(seedrandFloat(seedrandIntInput) * seedrandIntInput.max);
}
