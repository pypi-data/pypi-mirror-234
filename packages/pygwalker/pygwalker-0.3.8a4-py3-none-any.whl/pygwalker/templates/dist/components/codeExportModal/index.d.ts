import React from "react";
import type { IGlobalStore } from "@kanaries/graphic-walker/dist/store";
interface ICodeExport {
    globalStore: React.MutableRefObject<IGlobalStore | null>;
    sourceCode: string;
    open: boolean;
    setOpen: (open: boolean) => void;
}
declare const CodeExport: React.FC<ICodeExport>;
export default CodeExport;
