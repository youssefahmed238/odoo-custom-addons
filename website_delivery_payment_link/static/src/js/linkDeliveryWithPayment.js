/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.WebsiteCustomActions = publicWidget.Widget.extend({
    selector: '#wrapwrap',

    async start() {
        if (window.location.href.includes('/shop/payment')) {
            const $deliveryContainer = this.$('#delivery_method');
            const $paymentContainer = this.$('#payment_method');

            if (!$deliveryContainer.length || !$paymentContainer.length) return Promise.resolve();

            const res = await fetch('/delivery_payment/map', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({jsonrpc: "2.0", method: "call", params: {}, id: Date.now()}),
                credentials: 'same-origin',
            }).then(r => r.json());

            this.deliveryPaymentMap = res.result?.delivery_payment_map || {};
            this.paymentDeliveryMap = res.result?.payment_delivery_map || {};

            const $initialDelivery = $deliveryContainer.find('input[name="delivery_type"]:checked');
            if ($initialDelivery.length) {
                const deliveryId = $initialDelivery.val();
                const paymentId = this.deliveryPaymentMap[deliveryId];
                if (paymentId) {
                    const $paymentInput = $paymentContainer.find(`input[name="o_payment_radio"][data-payment-option-id="${paymentId}"]`);
                    if ($paymentInput.length) {
                        $paymentInput.prop('checked', true).trigger('change');
                        console.log(`Auto-selected payment on load: ${paymentId}`);
                    }
                }
            }

            this._addDeliveryMethodListener($deliveryContainer, $paymentContainer);
            this._addPaymentMethodListener($paymentContainer, $deliveryContainer);
        }
        return Promise.resolve();
    },

    _addDeliveryMethodListener($deliveryContainer, $paymentContainer) {
        if (!$deliveryContainer.length) {
            console.warn('delivery_method container not found');
            return;
        }

        $deliveryContainer.on('click', 'li.o_delivery_carrier_select', (e) => {
            const $input = $(e.currentTarget).find('input[name="delivery_type"]');
            if ($input.length) {
                const deliveryId = $input.val();
                console.log("Delivery selected:", deliveryId);

                const paymentId = this.deliveryPaymentMap[deliveryId];
                if (paymentId) {
                    const $paymentInput = $paymentContainer.find(`input[name="o_payment_radio"][data-payment-option-id="${paymentId}"]`);
                    if ($paymentInput.length) {
                        $paymentInput.prop('checked', true).trigger('change');
                        console.log(`Auto-selected payment: ${paymentId}`);
                    } else {
                        console.warn(`Payment with id ${paymentId} not found`);
                    }
                }
            }
        });
    },

    _addPaymentMethodListener($paymentContainer, $deliveryContainer) {
        if (!$paymentContainer.length) {
            console.warn('payment_method container not found');
            return;
        }

        $paymentContainer.on('click', 'input[name="o_payment_radio"]', (e) => {
            const $input = $(e.currentTarget);
            if ($input.length) {
                const paymentId = $input.data('payment-option-id');
                console.log("Payment selected:", paymentId);

                const deliveryId = this.paymentDeliveryMap[paymentId];
                if (deliveryId) {
                    const $deliveryInput = $deliveryContainer.find(`input[name="delivery_type"][value="${deliveryId}"]`);
                    if ($deliveryInput.length) {
                        $deliveryInput.prop('checked', true).trigger('change');
                        console.log(`Auto-selected delivery: ${deliveryId}`);
                    }
                }
            }
        });
    }
});