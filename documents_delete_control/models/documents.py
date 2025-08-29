from odoo import models, api


class Document(models.Model):
    _inherit = 'documents.document'

    @api.model
    def cannot_delete_documents(self):
        return self.env.user.has_group('documents_delete_control.group_delete_documents')
