import { IRenderMimeRegistry } from '@jupyterlab/rendermime';
import { ISessionContext } from '@jupyterlab/apputils';
import { CodeCell } from '@jupyterlab/cells';
import { Message } from '@lumino/messaging';
import { SplitLayout, Widget } from '@lumino/widgets';
import { IIterator } from '@lumino/algorithm';
import * as Blockly from 'blockly';
import { BlocklyManager } from './manager';
/**
 * A blockly layout to host the Blockly editor.
 */
export declare class BlocklyLayout extends SplitLayout {
    private _host;
    private _manager;
    private _workspace;
    private _sessionContext;
    private _cell;
    private _finishedLoading;
    private _dock;
    /**
     * Construct a `BlocklyLayout`.
     *
     */
    constructor(manager: BlocklyManager, sessionContext: ISessionContext, rendermime: IRenderMimeRegistry);
    get activeCell(): CodeCell;
    get cell(): CodeCell;
    get workspace(): Blockly.Workspace;
    set workspace(workspace: Blockly.Workspace);
    /**
     * Dispose of the resources held by the widget.
     */
    dispose(): void;
    /**
     * Init the blockly layout
     */
    init(): void;
    /**
     * Create an iterator over the widgets in the layout.
     */
    iter(): IIterator<Widget>;
    /**
     * Remove a widget from the layout.
     *
     * @param widget - The `widget` to remove.
     */
    removeWidget(widget: Widget): void;
    /**
     * Return the extra coded (if it exists), composed of the individual
     * data from each block in the workspace, which are defined in the
     * toplevel_init property. (e.g. : imports needed for the block)
     *
     * Add extra code example:
     * Blockly.Blocks['block_name'].toplevel_init = `import numpy`
     */
    getBlocksToplevelInit(): string;
    run(): void;
    interrupt(): void;
    clearOutputArea(): void;
    setupWidgetView(): void;
    /**
     * Handle `update-request` messages sent to the widget.
     */
    protected onUpdateRequest(msg: Message): void;
    /**
     * Handle `resize-request` messages sent to the widget.
     */
    protected onResize(msg: Widget.ResizeMessage): void;
    /**
     * Handle `fit-request` messages sent to the widget.
     */
    protected onFitRequest(msg: Message): void;
    /**
     * Handle `after-attach` messages sent to the widget.
     */
    protected onAfterAttach(msg: Message): void;
    private _resizeWorkspace;
    private _onManagerChanged;
}
