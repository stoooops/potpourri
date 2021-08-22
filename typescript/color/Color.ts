/**
 * Shade the given color by the given percent via RGB darkening/lightening
 * @param color
 * @param percent
 * @returns
 */
function rgbShadeColor(color: string, percent: number): string {
    let R = parseInt(color.substring(1, 3), 16);
    let G = parseInt(color.substring(3, 5), 16);
    let B = parseInt(color.substring(5, 7), 16);

    R = (R * (100 + percent)) / 100;
    G = (G * (100 + percent)) / 100;
    B = (B * (100 + percent)) / 100;

    // min 0
    R = R >= 0 ? R : 0;
    G = G >= 0 ? G : 0;
    B = B >= 0 ? B : 0;

    // max 255
    R = R <= 255 ? R : 255;
    G = G <= 255 ? G : 255;
    B = B <= 255 ? B : 255;

    const RR = R.toString(16).length == 1 ? "0" + R.toString(16) : R.toString(16);
    const GG = G.toString(16).length == 1 ? "0" + G.toString(16) : G.toString(16);
    const BB = B.toString(16).length == 1 ? "0" + B.toString(16) : B.toString(16);

    return "#" + RR + GG + BB;
}

/**
 * A color.
 */
export class Color {
    public readonly hex: string;

    constructor(hex: string) {
        this.hex = rgbShadeColor(hex, 0);
    }

    shade(percent: number): Color {
        return new Color(rgbShadeColor(this.hex, percent));
    }
}
