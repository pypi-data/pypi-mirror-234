export namespace TOOLBOX_TURTLE {
    let kind: string;
    let contents: {
        kind: string;
        name: string;
        colour: string;
        contents: ({
            kind: string;
            type: string;
            blockxml: string;
        } | {
            kind: string;
            type: string;
            blockxml?: undefined;
        })[];
    }[];
}
