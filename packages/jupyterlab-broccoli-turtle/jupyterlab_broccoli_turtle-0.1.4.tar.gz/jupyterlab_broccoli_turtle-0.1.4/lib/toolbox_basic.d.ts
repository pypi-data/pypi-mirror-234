export namespace TOOLBOX_BASIC {
    let kind: string;
    let contents: ({
        kind: string;
        name: string;
        colour: string;
        contents: ({
            kind: string;
            type: string;
            blockxml?: undefined;
        } | {
            kind: string;
            type: string;
            blockxml: string;
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
        custom: string;
        colour: string;
        name: string;
        contents?: undefined;
    })[];
}
