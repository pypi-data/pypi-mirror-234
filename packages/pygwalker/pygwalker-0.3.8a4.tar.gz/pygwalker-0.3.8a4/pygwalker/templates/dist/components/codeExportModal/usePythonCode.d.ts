import { IVisSpec } from "@kanaries/graphic-walker/dist/interfaces";
export declare function usePythonCode(props: {
    sourceCode: string;
    specList: IVisSpec[];
    version: string;
}): {
    pyCode: string;
};
