# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Transaction Mixin",
    "version": "14.0.4.1.1",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "mail",
        "ssi_policy_mixin",
        "ssi_sequence_mixin",
        "ssi_decorator",
        "ssi_print_mixin",
    ],
    "data": [
        "menu.xml",
        "views/mixin_transaction_views.xml",
    ],
}
