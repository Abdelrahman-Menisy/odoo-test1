/** @odoo-module */

import { FormController } from '@web/views/form/form_controller';
import { patch } from '@web/core/utils/patch';
import { useService } from '@web/core/utils/hooks';



const formControllerReloadButton = {
    setup() {
        super.setup();
        this.actionService = useService('action');
    },
    async onReloadButtonClicked() {
        this.actionService.doAction({
            type: 'ir.actions.client',
            tag: 'reload',
        });
    },

}

patch(FormController.prototype, formControllerReloadButton);
