/**
 * @returns the prime factors of the given number
 */
export function primeFactors(n: number): number[] {
    const factors: number[] = [];
    let divisor = 2;

    while (n >= 2) {
        if (n % divisor == 0) {
            factors.push(divisor);
            n = n / divisor;
        } else {
            divisor++;
        }
    }

    return factors;
}
