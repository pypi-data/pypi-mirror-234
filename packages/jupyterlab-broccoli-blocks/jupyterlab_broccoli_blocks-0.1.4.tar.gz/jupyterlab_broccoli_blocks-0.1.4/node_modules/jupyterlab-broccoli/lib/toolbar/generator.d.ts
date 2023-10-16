/// <reference types="react" />
import { ToolbarButtonComponent } from '@jupyterlab/apputils';
import { BlocklyManager } from './../manager';
import { BlocklyButton } from './utils';
export declare namespace SelectGenerator {
    interface IOptions extends ToolbarButtonComponent.IProps {
        manager: BlocklyManager;
    }
}
export declare class SelectGenerator extends BlocklyButton {
    private _manager;
    constructor(props: SelectGenerator.IOptions);
    dispose(): void;
    private handleChange;
    render(): JSX.Element;
}
