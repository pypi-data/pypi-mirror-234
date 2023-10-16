import { Signal } from '@lumino/signaling';
/**
 * BlocklyManager the manager for each document
 * to select the toolbox and the generator that the
 * user wants to use on a specific document.
 */
export class BlocklyManager {
    /**
     * Constructor of BlocklyManager.
     */
    constructor(app, registry, sessionContext, mimetypeService) {
        this._app = app;
        this._registry = registry;
        this._sessionContext = sessionContext;
        this._mimetypeService = mimetypeService;
        this._toolbox = 'default';
        this._generator = this._registry.generators.get('python');
        this._changed = new Signal(this);
        this._sessionContext.kernelChanged.connect(this._onKernelChanged, this);
        this._language = this._registry.language;
        import(`./msg/${this._language}.js`)
            .then(() => {
            this._changed.emit('toolbox');
        })
            .catch(() => {
            if (this._language !== 'En') {
                import(`./msg/En.js`)
                    .then(() => { this._changed.emit('toolbox'); })
                    .catch(() => { });
            }
        });
        this._shell = this._app.shell;
        this._shell.currentChanged.connect((_, change) => {
            this._changed.emit('focus');
        });
    }
    get shell() {
        return this._shell;
    }
    /**
     * Returns the selected toolbox.
     */
    get toolbox() {
        return this._registry.toolboxes.get(this._toolbox);
    }
    /**
     * Returns the mimeType for the selected kernel.
     *
     * Note: We need the mimeType for the syntax highlighting
     * when rendering the code.
     */
    get mimeType() {
        if (this._selectedKernel) {
            return this._mimetypeService.getMimeTypeByLanguage({
                name: this._selectedKernel.language
            });
        }
        else {
            return 'text/plain';
        }
    }
    /**
     * Returns the name of the selected kernel.
     */
    get kernel() {
        var _a;
        return ((_a = this._selectedKernel) === null || _a === void 0 ? void 0 : _a.name) || 'No kernel';
    }
    /**
     *
     */
    get kernelspec() {
        return this._selectedKernel;
    }
    /**
     * Returns the selected generator.
     */
    get generator() {
        return this._generator;
    }
    /**
     * Signal triggered when the manager changes.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Send a 'block' signal to BlocklyEditor
     */
    dirty(dirty) {
        if (dirty) {
            this._changed.emit('dirty');
        }
    }
    /**
     * Dispose.
     */
    dispose() {
        this._sessionContext.kernelChanged.disconnect(this._onKernelChanged, this);
    }
    /**
     * Get the selected toolbox's name.
     *
     * @returns The name of the toolbox.
     */
    getToolbox() {
        return this._toolbox;
    }
    /**
     * Set the selected toolbox.
     *
     * @argument name The name of the toolbox.
     */
    setToolbox(name) {
        if (this._toolbox !== name) {
            const toolbox = this._registry.toolboxes.get(name);
            this._toolbox = toolbox ? name : 'default';
            this._changed.emit('toolbox');
        }
    }
    /**
     * List the available toolboxes.
     *
     * @returns the list of available toolboxes for Blockly
     */
    listToolboxes() {
        const list = [];
        this._registry.toolboxes.forEach((toolbox, name) => {
            list.push({ label: name, value: name });
        });
        return list;
    }
    /**
     * Set the selected kernel.
     *
     * @argument name The name of the kernel.
     */
    selectKernel(name) {
        this._sessionContext.changeKernel({ name });
    }
    /**
     * List the available kernels.
     *
     * @returns the list of available kernels for Blockly
     */
    listKernels() {
        const specs = this._sessionContext.specsManager.specs.kernelspecs;
        const list = [];
        Object.keys(specs).forEach(key => {
            const language = specs[key].language;
            if (this._registry.generators.has(language)) {
                list.push({ label: specs[key].display_name, value: specs[key].name });
            }
        });
        return list;
    }
    _onKernelChanged(sender, args) {
        const specs = this._sessionContext.specsManager.specs.kernelspecs;
        if (args.newValue && specs[args.newValue.name] !== undefined) {
            this._selectedKernel = specs[args.newValue.name];
            const language = specs[args.newValue.name].language;
            this._generator = this._registry.generators.get(language);
            this._changed.emit('kernel');
        }
    }
}
//# sourceMappingURL=manager.js.map