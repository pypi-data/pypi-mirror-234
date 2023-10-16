import { HTMLSelect } from '@jupyterlab/ui-components';
import React from 'react';
import { BlocklyButton } from './utils';
export class SelectGenerator extends BlocklyButton {
    constructor(props) {
        super(props);
        this.handleChange = (event) => {
            this._manager.selectKernel(event.target.value);
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
        const kernels = this._manager.listKernels();
        if (this._manager.kernel === 'No kernel') {
            kernels.push({ label: 'No kernel', value: 'No kernel' });
        }
        return (React.createElement(HTMLSelect, { onChange: this.handleChange, value: this._manager.kernel, options: kernels }));
    }
}
//# sourceMappingURL=generator.js.map