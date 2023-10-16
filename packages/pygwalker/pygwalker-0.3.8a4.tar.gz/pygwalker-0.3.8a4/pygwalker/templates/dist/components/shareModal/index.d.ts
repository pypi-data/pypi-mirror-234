import React from "react";
import type { IGWHandler } from "@kanaries/graphic-walker/dist/interfaces";
import type { IGlobalStore } from "@kanaries/graphic-walker/dist/store";
interface IShareModal {
    gwRef: React.MutableRefObject<IGWHandler | null>;
    storeRef: React.MutableRefObject<IGlobalStore | null>;
    open: boolean;
    setOpen: (open: boolean) => void;
}
declare const ShareModal: React.FC<IShareModal>;
export default ShareModal;
