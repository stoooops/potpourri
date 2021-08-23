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

interface RGB {
    r: number;
    g: number;
    b: number;
}

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r: number, g: number, b: number) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}
function hexToRgb(hex: string): RGB {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    if (!result) {
        throw Error(`Bad hex string: ${hex}`);
    }
    return {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
    };
}

interface HSL {
    /**
     * Hue degrees [0, 360]
     */
    h: number;

    /**
     * Saturation percent [0-1]
     */
    s: number;

    /**
     * Lightness percent [0-1]
     */
    l: number;
}

/**
 * Converts an RGB color value to HSL. Conversion formula
 * adapted from http://en.wikipedia.org/wiki/HSL_color_space.
 * Assumes r, g, and b are contained in the set [0, 255] and
 * returns h, s, and l in the set [0, 1].
 *
 * @param   {number}  r       The red color value
 * @param   {number}  g       The green color value
 * @param   {number}  b       The blue color value
 * @return  {Array}           The HSL representation
 */
function rgbToHsl(rgb: RGB): HSL {
    let r = rgb.r / 255;
    let g = rgb.g / 255;
    let b = rgb.b / 255;
    let max = Math.max(r, g, b);
    let min = Math.min(r, g, b);

    let h, s;
    let l = (max + min) / 2;

    if (max == min) {
        h = s = 0; // achromatic
    } else {
        let d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch (max) {
            case r:
                h = (g - b) / d + (g < b ? 6 : 0);
                break;
            case g:
                h = (b - r) / d + 2;
                break;
            case b:
                h = (r - g) / d + 4;
                break;
        }
        h /= 6;
    }

    return { h: h * 360, s: s, l: l };
}

/**
 * A color.
 */
export class Color {
    public readonly hex: string;
    public readonly rgb: RGB;
    public readonly hsl: HSL;

    constructor(hex: string) {
        this.hex = rgbShadeColor(hex, 0);
        this.rgb = hexToRgb(hex);
        this.hsl = rgbToHsl(this.rgb);

        console.log(
            `${this.hex} -> (${this.rgb.r},${this.rgb.g},${this.rgb.b}) -> (${this.hsl.h},${this.hsl.s},${this.hsl.l})`
        );
    }

    shade(percent: number): Color {
        return new Color(rgbShadeColor(this.hex, percent));
    }
}
