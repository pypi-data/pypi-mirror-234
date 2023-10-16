import { DocumentWidget } from '@jupyterlab/docregistry';
import { runIcon, stopIcon, saveIcon, circleEmptyIcon, } from '@jupyterlab/ui-components';
import { SplitPanel } from '@lumino/widgets';
import { Signal } from '@lumino/signaling';
import { BlocklyLayout } from './layout';
import { BlocklyButton, SelectGenerator, SelectToolbox, Spacer } from './toolbar';
import { nullTranslator } from '@jupyterlab/translation';
import { sessionContextDialogs } from '@jupyterlab/apputils';
import { closeDialog } from './dialog';
const DIRTY_CLASS = 'jp-mod-dirty';
/**
 * DocumentWidget: widget that represents the view or editor for a file type.
 */
export class BlocklyEditor extends DocumentWidget {
    constructor(app, options) {
        super(options);
        this._dirty = false;
        this._context = options.context;
        this._manager = options.manager;
        // Loading the ITranslator
        this._trans = (this._context.translator || nullTranslator).load('jupyterlab');
        // this.content is BlocklyPanel
        this._blayout = this.content.layout;
        // Create and add a button to the toolbar to execute
        // the code.
        const button_save = new BlocklyButton({
            label: '',
            icon: saveIcon,
            className: 'jp-blockly-saveFile',
            onClick: () => this.save(true),
            tooltip: 'Save File'
        });
        const button_run = new BlocklyButton({
            label: '',
            icon: runIcon,
            className: 'jp-blockly-runButton',
            onClick: () => this._blayout.run(),
            tooltip: 'Run Code'
        });
        const button_stop = new BlocklyButton({
            label: '',
            icon: stopIcon,
            className: 'jp-blockly-stopButton',
            onClick: () => this._blayout.interrupt(),
            tooltip: 'Stop Code'
        });
        const button_clear = new BlocklyButton({
            label: '',
            icon: circleEmptyIcon,
            className: 'jp-blockly-clearButton',
            onClick: () => this._blayout.clearOutputArea(),
            tooltip: 'Clear Output'
        });
        this.toolbar.addItem('save', button_save);
        this.toolbar.addItem('run', button_run);
        this.toolbar.addItem('stop', button_stop);
        this.toolbar.addItem('clear', button_clear);
        this.toolbar.addItem('spacer', new Spacer());
        this.toolbar.addItem('toolbox', new SelectToolbox({
            label: 'Toolbox',
            tooltip: 'Select tollbox',
            manager: options.manager
        }));
        this.toolbar.addItem('generator', new SelectGenerator({
            label: 'Kernel',
            tooltip: 'Select kernel',
            manager: options.manager
        }));
        //
        this._manager.changed.connect(this._onBlockChanged, this);
    } /* End of constructor */
    // for dialog.ts
    get trans() {
        return this._trans;
    }
    /**
     * Sets the dirty boolean while also toggling the DIRTY_CLASS
     */
    dirty(dirty) {
        this._dirty = dirty;
        //
        if (this._dirty && !this.title.className.includes(DIRTY_CLASS)) {
            this.title.className += ' ' + DIRTY_CLASS;
        }
        else if (!this._dirty) {
            this.title.className = this.title.className.replace(DIRTY_CLASS, '');
        }
        this.title.className = this.title.className.replace('  ', ' ');
    }
    // 
    async save(exiting = false) {
        exiting ? await this._context.save() : this._context.save();
        this.dirty(false);
    }
    /**
     * Dispose of the resources held by the widget.
     */
    async dispose() {
        if (!this.isDisposed && this._dirty) {
            const isclose = await closeDialog(this);
            if (!isclose)
                return;
        }
        this.content.dispose();
        super.dispose();
    }
    //
    _onBlockChanged(sender, change) {
        if (change === 'dirty') {
            this.dirty(true);
        }
        else if (change === 'focus') {
            this._blayout.setupWidgetView();
        }
    }
}
/**
 * Widget that contains the main view of the DocumentWidget.
 */
export class BlocklyPanel extends SplitPanel {
    /**
     * Construct a `BlocklyPanel`.
     *
     * @param context - The documents context.
     */
    constructor(context, manager, rendermime) {
        super({
            layout: new BlocklyLayout(manager, context.sessionContext, rendermime)
        });
        this.addClass('jp-BlocklyPanel');
        this._context = context;
        this._rendermime = rendermime;
        this._manager = manager;
        // Load the content of the file when the context is ready
        this._context.ready.then(() => this._load());
        // Connect to the save signal
        this._context.saveState.connect(this._onSave, this);
    }
    /*
     * The code cell.
     */
    get cell() {
        return this.layout.cell;
    }
    /*
     * The rendermime instance used in the code cell.
     */
    get rendermime() {
        return this._rendermime;
    }
    get context() {
        return this._context;
    }
    get content() {
        return this._content;
    }
    get manager() {
        return this._manager;
    }
    get activeLayout() {
        return this.layout;
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        Signal.clearData(this);
        super.dispose();
    }
    _load() {
        // Loading the content of the document into the workspace
        let kernelname = '';
        this._content = this._context.model.toJSON();
        if (this._content != null) {
            if (('metadata' in this._content) &&
                ('kernelspec' in this._content['metadata']) &&
                ('name' in this._content['metadata']['kernelspec'])) {
                kernelname = this._content['metadata']['kernelspec']['name'];
            }
        }
        if (kernelname === '') {
            sessionContextDialogs.selectKernel(this._context.sessionContext, this._context.translator);
        }
        else {
            this._manager.selectKernel(kernelname);
        }
        this.layout.workspace = this._content;
        // Set Block View, Output View and Code View to DockPanel
        this.layout.setupWidgetView();
    }
    _onSave(sender, state) {
        if (state === 'started') {
            const workspace = this.layout.workspace;
            //
            if (this._manager['kernelspec'] != undefined) {
                workspace['metadata'] = {
                    'kernelspec': {
                        'display_name': this._manager.kernelspec.display_name,
                        'language': this._manager.kernelspec.language,
                        'name': this._manager.kernelspec.name
                    }
                };
            }
            this._context.model.fromJSON(workspace);
        }
    }
}
//# sourceMappingURL=widget.js.map