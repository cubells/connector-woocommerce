# © 2009 Tech-Receptives Solutions Pvt. Ltd.
# © 2018 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# See LICENSE file for full copyright and licensing details.

from odoo import _, api, exceptions, models


class QueueJob(models.Model):
    _inherit = 'queue.job'

    @api.multi
    def related_action_woo_link(self, backend_id_pos=0, external_id_pos=1):
        """ Open a WooCommerce URL on the admin page to view/edit the record
        related to the job.
        """
        self.ensure_one()
        model_name = self.model_name
        backend = self.args[backend_id_pos]
        external_id = self.args[external_id_pos]
        with backend.work_on(model_name) as work:
            adapter = work.component(usage='backend.adapter')
            try:
                url = adapter.admin_url(external_id)
            except ValueError:
                raise exceptions.UserError(
                    _('No admin URL configured on the backend or '
                      'no admin path is defined for this record.')
                )

        action = {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': url,
        }
        return action
