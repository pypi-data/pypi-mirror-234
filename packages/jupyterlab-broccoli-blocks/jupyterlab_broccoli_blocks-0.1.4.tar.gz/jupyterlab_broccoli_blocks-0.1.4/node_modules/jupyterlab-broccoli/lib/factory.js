import { ABCWidgetFactory } from '@jupyterlab/docregistry';
import { BlocklyEditor, BlocklyPanel } from './widget';
import { BlocklyRegistry } from './registry';
import { BlocklyManager } from './manager';
//import { TranslationBundle, nullTranslator } from '@jupyterlab/translation';
/*
namespace CommandIDs {
  export const copyToClipboard = 'jupyterlab-broccoli:copy-to-clipboard';
}
/**/
/**
 * A widget factory to create new instances of BlocklyEditor.
 */
export class BlocklyEditorFactory extends ABCWidgetFactory {
    /**
     * Constructor of BlocklyEditorFactory.
     *
     * @param options Constructor options
     */
    constructor(app, options) {
        super(options);
        this._app = app;
        this._registry = new BlocklyRegistry();
        this._rendermime = options.rendermime;
        this._mimetypeService = options.mimetypeService;
        //this._trans = (options.translator || nullTranslator).load('jupyterlab');
        /*
            app.commands.addCommand(CommandIDs.copyToClipboard, {
              label: this._trans.__('ZZZZ Copy Output to Clipboard'),
              execute: args => { alert("OK") }
            });
        
            app.contextMenu.addItem({
              command: CommandIDs.copyToClipboard,
              selector: '.jp-OutputArea-child',
              rank: 0
            });
        /**/
    }
    get registry() {
        return this._registry;
    }
    get manager() {
        return this._manager;
    }
    /**
     * Create a new widget given a context.
     *
     * @param context Contains the information of the file
     * @returns The widget
     */
    createNewWidget(context) {
        // Set a map to the model. The widgets manager expects a Notebook model
        // but the only notebook property it uses is the metadata.
        context.model['metadata'] = new Map();
        const manager = new BlocklyManager(this._app, this._registry, context.sessionContext, this._mimetypeService);
        this._manager = manager;
        const content = new BlocklyPanel(context, manager, this._rendermime);
        return new BlocklyEditor(this._app, { context, content, manager });
    }
}
//# sourceMappingURL=factory.js.map