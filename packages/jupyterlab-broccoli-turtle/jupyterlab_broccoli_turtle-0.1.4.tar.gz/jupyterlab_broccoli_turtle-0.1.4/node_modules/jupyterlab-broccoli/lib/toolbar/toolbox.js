import { HTMLSelect } from '@jupyterlab/ui-components';
import React from 'react';
import { BlocklyButton } from './utils';
export class SelectToolbox extends BlocklyButton {
    constructor(props) {
        super(props);
        this.handleChange = (event) => {
            this._manager.setToolbox(event.target.value);
            this.update();
        };
        this._manager = props.manager;
        this._manager.changed.connect(this.update, this);
    }
    dispose() {
        super.dispose();
        this._manager.changed.disconnect(this.update, this);
    }
    render() {
        return (React.createElement(HTMLSelect, { onChange: this.handleChange, value: this._manager.getToolbox(), options: this._manager.listToolboxes() }));
    }
}
//# sourceMappingURL=toolbox.js.map