/** @odoo-module */

import { KanbanController } from '@web/views/kanban/kanban_controller';
import { useService } from "@web/core/utils/hooks";
import { patch } from '@web/core/utils/patch';


const OwlKanbanController = {

    setup() {
        super.setup();
        this.actionService = useService("action");
    },

    getALLProducts: async function () {
        this.actionService.doAction({
            type: 'ir.actions.act_window',
            res_model: 'product.template',
            views: [[false, 'list']],
            target: 'current',
        });
    },
}

patch(KanbanController.prototype, OwlKanbanController);