/** @odoo-module **/

import { DocumentsInspector } from "@documents/views/inspector/documents_inspector";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { useState, onWillStart } from "@odoo/owl";

patch(DocumentsInspector.prototype, {
    setup() {
        super.setup();
        this.rpc = useService("rpc");
        this.state = useState({ canDelete: true });

        onWillStart(() => this.loadDeletePermission());
    },

    async loadDeletePermission() {
        try {
            const cannotDelete = await this.rpc("/web/dataset/call_kw", {
                model: "documents.document",
                method: "cannot_delete_documents",
                args: [],
                kwargs: {},
            });

            this.state.canDelete = !cannotDelete;
        } catch (error) {
            this.state.canDelete = true;
            console.error("Error: ", error);
        }
    },

    get documentsActive() {
        return this.props.documents.length > 0 && this.props.documents.every(doc => doc.data.active);
    },

    canMoveToTrash() {
        return this.documentsActive && this.state.canDelete;
    },

    canDelete() {
        return !this.documentsActive && this.state.canDelete;
    },

    canRestore() {
        return !this.documentsActive;
    },
});
