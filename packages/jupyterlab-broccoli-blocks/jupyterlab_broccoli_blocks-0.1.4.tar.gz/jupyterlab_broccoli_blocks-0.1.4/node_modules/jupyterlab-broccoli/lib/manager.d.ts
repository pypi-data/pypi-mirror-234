import { ISessionContext } from '@jupyterlab/apputils';
import { IEditorMimeTypeService } from '@jupyterlab/codeeditor';
import { KernelSpec } from '@jupyterlab/services';
import { ISignal } from '@lumino/signaling';
import * as Blockly from 'blockly';
import type { ToolboxDefinition } from 'blockly/core/utils/toolbox';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { ILabShell } from '@jupyterlab/application';
import { BlocklyRegistry } from './registry';
/**
 * BlocklyManager the manager for each document
 * to select the toolbox and the generator that the
 * user wants to use on a specific document.
 */
export declare class BlocklyManager {
    private _toolbox;
    private _generator;
    private _registry;
    private _selectedKernel;
    private _sessionContext;
    private _mimetypeService;
    private _changed;
    private _language;
    private _app;
    private _shell;
    /**
     * Constructor of BlocklyManager.
     */
    constructor(app: JupyterFrontEnd, registry: BlocklyRegistry, sessionContext: ISessionContext, mimetypeService: IEditorMimeTypeService);
    get shell(): ILabShell;
    /**
     * Returns the selected toolbox.
     */
    get toolbox(): ToolboxDefinition;
    /**
     * Returns the mimeType for the selected kernel.
     *
     * Note: We need the mimeType for the syntax highlighting
     * when rendering the code.
     */
    get mimeType(): string;
    /**
     * Returns the name of the selected kernel.
     */
    get kernel(): string | undefined;
    /**
     *
     */
    get kernelspec(): KernelSpec.ISpecModel;
    /**
     * Returns the selected generator.
     */
    get generator(): Blockly.Generator;
    /**
     * Signal triggered when the manager changes.
     */
    get changed(): ISignal<this, BlocklyManager.Change>;
    /**
     * Send a 'block' signal to BlocklyEditor
     */
    dirty(dirty: boolean): void;
    /**
     * Dispose.
     */
    dispose(): void;
    /**
     * Get the selected toolbox's name.
     *
     * @returns The name of the toolbox.
     */
    getToolbox(): string;
    /**
     * Set the selected toolbox.
     *
     * @argument name The name of the toolbox.
     */
    setToolbox(name: string): void;
    /**
     * List the available toolboxes.
     *
     * @returns the list of available toolboxes for Blockly
     */
    listToolboxes(): {
        label: string;
        value: string;
    }[];
    /**
     * Set the selected kernel.
     *
     * @argument name The name of the kernel.
     */
    selectKernel(name: string): void;
    /**
     * List the available kernels.
     *
     * @returns the list of available kernels for Blockly
     */
    listKernels(): {
        label: string;
        value: string;
    }[];
    private _onKernelChanged;
}
/**
 * BlocklyManager the manager for each document
 * to select the toolbox and the generator that the
 * user wants to use on a specific document.
 */
export declare namespace BlocklyManager {
    /**
     * The argument of the signal manager changed.
     */
    type Change = 'toolbox' | 'kernel' | 'focus' | 'dirty';
}
