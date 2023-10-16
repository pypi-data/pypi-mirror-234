import { ABCWidgetFactory, DocumentRegistry, DocumentModel } from '@jupyterlab/docregistry';
import { IRenderMimeRegistry } from '@jupyterlab/rendermime';
import { IEditorMimeTypeService } from '@jupyterlab/codeeditor';
import { BlocklyEditor } from './widget';
import { BlocklyRegistry } from './registry';
import { BlocklyManager } from './manager';
import { JupyterFrontEnd } from '@jupyterlab/application';
/**
 * A widget factory to create new instances of BlocklyEditor.
 */
export declare class BlocklyEditorFactory extends ABCWidgetFactory<BlocklyEditor, DocumentModel> {
    private _registry;
    private _rendermime;
    private _mimetypeService;
    private _manager;
    private _app;
    /**
     * Constructor of BlocklyEditorFactory.
     *
     * @param options Constructor options
     */
    constructor(app: JupyterFrontEnd, options: BlocklyEditorFactory.IOptions);
    get registry(): BlocklyRegistry;
    get manager(): BlocklyManager;
    /**
     * Create a new widget given a context.
     *
     * @param context Contains the information of the file
     * @returns The widget
     */
    protected createNewWidget(context: DocumentRegistry.IContext<DocumentModel>): BlocklyEditor;
}
export declare namespace BlocklyEditorFactory {
    interface IOptions extends DocumentRegistry.IWidgetFactoryOptions {
        rendermime: IRenderMimeRegistry;
        mimetypeService: IEditorMimeTypeService;
    }
}
