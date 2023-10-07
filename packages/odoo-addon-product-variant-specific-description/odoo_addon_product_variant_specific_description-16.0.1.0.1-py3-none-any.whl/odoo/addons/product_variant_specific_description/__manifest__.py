# Copyright 2023 ForgeFlow, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Variant Specific Description",
    "version": "16.0.1.0.1",
    "category": "Product",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-variant",
    "license": "AGPL-3",
    "depends": [
        "product",
    ],
    "data": [
        "views/product_view.xml",
        "views/product_template_view.xml",
    ],
    "installable": True,
    "post_init_hook": "post_init_hook",
}
