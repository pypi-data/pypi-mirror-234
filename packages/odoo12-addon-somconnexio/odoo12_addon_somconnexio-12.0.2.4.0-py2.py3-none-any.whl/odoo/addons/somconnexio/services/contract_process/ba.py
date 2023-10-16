import logging

from odoo.exceptions import UserError

from .base import BaseContractProcess


_logger = logging.getLogger(__name__)


class BAContractProcess(BaseContractProcess):
    _description = """
        Mobile Contract creation
    """

    def _get_router_product_id(self, router_code):
        router_product = (
            self.env["product.product"]
            .sudo()
            .search(
                [
                    ("default_code", "=", router_code),
                ]
            )
        )
        if router_product:
            return router_product
        else:
            raise UserError("No router product with code %s" % router_code)

    def _create_router_lot_id(self, serial_number, mac_address, product):
        return (
            self.env["stock.production.lot"]
            .sudo()
            .create(
                {
                    "product_id": product.id,
                    "router_mac_address": mac_address,
                    "name": serial_number,
                }
            )
        )
