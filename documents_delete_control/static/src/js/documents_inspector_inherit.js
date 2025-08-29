/** @odoo-module **/

import { DocumentsInspector } from "@documents/views/inspector/documents_inspector";
import { patch } from "@web/core/utils/patch";

console.log("Loading custom DocumentsInspector override...");

patch(DocumentsInspector.prototype, {

    canDeleteDocuments() {

        if (!this.props.documents || this.props.documents.length === 0) {
            return false;
        }



        return false;
    },
});
