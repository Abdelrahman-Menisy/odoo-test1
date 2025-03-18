/** @odoo-module */

import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { KanbanController } from '@web/views/kanban/kanban_controller';
import { kanbanView } from '@web/views/kanban/kanban_view';


class ResPartnerKanbanController extends KanbanController {
    setup() {
        super.setup();
        this.actionService = useService('partner');
    }

    getSales() {
        this.actionService.doAction({
            type: 'ir.actions.act_window',
            name: 'Sales',
            res_model: 'sale.order',
            views: [[false, 'list']],
            // domain: [['partner_id', 'in', this.model.ids]],
        });

}   
}

const resPartnerKanbanView = {
    ...kanbanView,
    Controller: ResPartnerKanbanController,
    buttonTemplate: "res_partner_kanban_sales_button",

};

registry.category('views').add('res_partner_kanban', resPartnerKanbanView);

