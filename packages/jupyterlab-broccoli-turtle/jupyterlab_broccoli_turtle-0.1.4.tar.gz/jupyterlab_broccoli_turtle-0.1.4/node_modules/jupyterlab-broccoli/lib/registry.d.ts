import * as Blockly from 'blockly';
import { IBlocklyRegistry } from './token';
import type { ToolboxDefinition } from 'blockly/core/utils/toolbox';
import { BlockDefinition } from 'blockly/core/blocks';
/**
 * BlocklyRegistry is the class that JupyterLab-Blockly exposes
 * to other plugins. This registry allows other plugins to register
 * new Toolboxes, Blocks and Generators that users can use in the
 * Blockly editor.
 */
export declare class BlocklyRegistry implements IBlocklyRegistry {
    private _toolboxes;
    private _generators;
    private _language;
    /**
     * Constructor of BlocklyRegistry.
     */
    constructor();
    /**
     * Returns a map with all the toolboxes.
     */
    get toolboxes(): Map<string, ToolboxDefinition>;
    /**
     * Returns a map with all the generators.
     */
    get generators(): Map<string, Blockly.Generator>;
    /**
     * Returns language (2 charactors).
     */
    get language(): string;
    /**
     * Register a toolbox for the editor.
     *
     * @argument name The name of the toolbox.
     *
     * @argument toolbox The toolbox to register.
     */
    registerToolbox(name: string, toolbox: ToolboxDefinition): void;
    /**
     * Register block definitions.
     *
     * @argument blocks A list of block definitions to register.
     */
    registerBlocks(blocks: BlockDefinition[]): void;
    /**
     * Register a language generator.
     *
     * @argument language The language output by the generator.
     *
     * @argument generator The generator to register.
     *
     * #### Notes
     * If a generator already exists for the given language it is overwritten.
     */
    registerGenerator(language: string, generator: Blockly.Generator): void;
    /**
     * Register blocks codes.
     *
     * @argument language The name of the programming language. python, lua, javascript, ...
     *
     * @argument funcs Imported functions.
     */
    registerCodes(language: string, funcs: {
        [name: string]: Function;
    }): void;
    setlanguage(language: string): void;
}
