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

function componentToHex(c: number) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(rgb: RGB) {
    return "#" + componentToHex(rgb.r) + componentToHex(rgb.g) + componentToHex(rgb.b);
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
 * Converts an HSL color value to RGB. Conversion formula
 * adapted from http://en.wikipedia.org/wiki/HSL_color_space.
 * Assumes h, s, and l are contained in the set [0, 1] and
 * returns r, g, and b in the set [0, 255].
 *
 * @param   {number}  h       The hue
 * @param   {number}  s       The saturation
 * @param   {number}  l       The lightness
 * @return  {Array}           The RGB representation
 */
function hslToRgb(hsl: HSL): RGB {
    let h = hsl.h / 360;
    let s = hsl.s;
    let l = hsl.l;
    let r, g, b;

    if (s == 0) {
        r = g = b = l; // achromatic
    } else {
        let hue2rgb = function hue2rgb(p, q, t) {
            if (t < 0) t += 1;
            if (t > 1) t -= 1;
            if (t < 1 / 6) return p + (q - p) * 6 * t;
            if (t < 1 / 2) return q;
            if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
            return p;
        };

        let q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        let p = 2 * l - q;
        r = hue2rgb(p, q, h + 1 / 3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1 / 3);
    }

    return {
        r: Math.round(r * 255),
        g: Math.round(g * 255),
        b: Math.round(b * 255),
    };
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

function hslToHex(hsl: HSL): string {
    return rgbToHex(hslToRgb(hsl));
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

    rotate(degrees: number) {
        return new Color(
            rgbToHex(
                hslToRgb({
                    h: (this.hsl.h + degrees) % 360,
                    s: this.hsl.s,
                    l: this.hsl.l,
                })
            )
        );
    }

    analagous(rotation: number, quantity: number): Color[] {
        if (quantity < 3 || quantity % 2 === 0) {
            throw Error(`Bad quantity: ${quantity}`);
        }
        const result: Color[] = [this];
        let i = 0;
        while (result.length < quantity) {
            i++;
            result.push(this.rotate(rotation * i));
            result.push(this.rotate(-rotation * i));
        }
        return result;
    }

    complimentary(): Color[] {
        return [this, this.rotate(180)];
    }

    triadic(): Color[] {
        return [this, this.rotate(120), this.rotate(240)];
    }

    tetradic(): Color[] {
        return [this, this.rotate(90), this.rotate(180), this.rotate(270)];
    }
}
