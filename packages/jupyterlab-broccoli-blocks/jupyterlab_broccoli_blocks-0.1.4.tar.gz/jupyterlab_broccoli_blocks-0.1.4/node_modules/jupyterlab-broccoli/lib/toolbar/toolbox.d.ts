/// <reference types="react" />
import { ToolbarButtonComponent } from '@jupyterlab/apputils';
import { BlocklyManager } from './../manager';
import { BlocklyButton } from './utils';
export declare namespace SelectToolbox {
    interface IOptions extends ToolbarButtonComponent.IProps {
        manager: BlocklyManager;
    }
}
export declare class SelectToolbox extends BlocklyButton {
    private _manager;
    constructor(props: SelectToolbox.IOptions);
    dispose(): void;
    private handleChange;
    render(): JSX.Element;
}
