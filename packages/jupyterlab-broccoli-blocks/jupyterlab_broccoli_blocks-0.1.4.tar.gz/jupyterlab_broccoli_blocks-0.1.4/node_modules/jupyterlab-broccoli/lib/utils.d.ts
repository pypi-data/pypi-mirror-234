import * as Blockly from 'blockly';
export declare const TOOLBOX: {
    kind: string;
    contents: ({
        kind: string;
        name: string;
        colour: string;
        contents: ({
            kind: string;
            type: string;
            blockxml?: undefined;
        } | {
            kind: string;
            blockxml: string;
            type: string;
        })[];
        custom?: undefined;
    } | {
        kind: string;
        name?: undefined;
        colour?: undefined;
        contents?: undefined;
        custom?: undefined;
    } | {
        kind: string;
        colour: string;
        custom: string;
        name: string;
        contents?: undefined;
    })[];
};
export declare const THEME: Blockly.Theme;
