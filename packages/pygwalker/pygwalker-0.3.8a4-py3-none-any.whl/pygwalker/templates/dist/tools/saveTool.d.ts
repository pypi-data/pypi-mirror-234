import React from 'react';
import type { IAppProps } from '../interfaces';
import type { IGWHandler } from '@kanaries/graphic-walker/dist/interfaces';
import type { ToolbarButtonItem } from "@kanaries/graphic-walker/dist/components/toolbar/toolbar-button";
import type { IGlobalStore } from '@kanaries/graphic-walker/dist/store';
export declare function hidePreview(id: string): void;
export declare function getSaveTool(props: IAppProps, gwRef: React.MutableRefObject<IGWHandler | null>, storeRef: React.MutableRefObject<IGlobalStore | null>): ToolbarButtonItem;
