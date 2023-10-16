# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from inspect import getmembers

from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MixinTransaction(models.AbstractModel):
    """
    Abstract model to transaction object
    """

    _name = "mixin.transaction"
    _inherit = [
        "mail.activity.mixin",
        "mail.thread",
        "mixin.decorator",
        "mixin.sequence",
        "mixin.policy",
        "mixin.print_document",
    ]
    _description = "Transaction Mixin"
    _draft_state = "draft"
    _create_sequence_state = False
    _document_number_field = "name"
    _automatically_insert_view_element = False
    _automatically_insert_print_button = True

    _automatically_reconfigure_statusbar_visible = True
    _policy_field_order = False
    _header_button_order = False

    _statusbar_visible_label = "draft"
    _policy_field_xpath = (
        "/form/sheet/notebook/page[@name='policy']"
        "/group[@name='policy_2']/field[@name='restart_ok']"
    )

    # Attributes related to add element on search view automatically
    _state_filter_xpath = "/search/group[@name='dom_state']/filter[@name='dom_draft']"
    _state_filter_order = False

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
        copy=True,
    )

    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        required=True,
        default=lambda self: self._default_user_id(),
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    note = fields.Text(
        string="Note",
        copy=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
        ],
        default="draft",
        required=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
        compute_sudo=True,
    )
    manual_number_ok = fields.Boolean(
        string="Can Input Manual Document Number",
        compute="_compute_policy",
        compute_sudo=True,
    )

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_user_id(self):
        return self.env.user.id

    def _compute_policy(self):
        _super = super(MixinTransaction, self)
        _super._compute_policy()

    # TODO: Dynamic field name
    @api.constrains(
        "name",
    )
    def _constrains_duplicate_document_number(self):
        for record in self.sudo():
            if not record._check_duplicate_document_number():
                error_message = """
                Context: Change %s document number
                Database ID: %s
                Problem: Duplicate document number
                Solution: Change document number into different number
                """ % (
                    self._description.lower(),
                    record.id,
                )
                raise UserError(_(error_message))

    def name_get(self):
        result = []
        for record in self:
            if getattr(record, self._document_number_field) == "/":
                name = "*" + str(record.id)
            else:
                name = record.name
            result.append((record.id, name))
        return result

    def unlink(self):
        force_unlink = self.env.context.get("force_unlink", False)
        for record in self:
            if not record._check_state_unlink(force_unlink):
                error_message = """
                Context: Delete %s
                Database ID: %s
                Problem: Document state is not draft
                Solution: Cancel and restart document
                """ % (
                    self._description.lower(),
                    record.id,
                )
                raise UserError(_(error_message))
            if not record._check_document_number_unlink(force_unlink):
                error_message = """
                Context: Delete %s
                Database ID: %s
                Problem: Document number is not equal to /
                Solution: Change document number into /
                """ % (
                    self._description.lower(),
                    record.id,
                )
                raise UserError(_(error_message))
        _super = super(MixinTransaction, self)
        _super.unlink()

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        result = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        View = self.env["ir.ui.view"]

        view_arch = etree.XML(result["arch"])

        if view_type == "form" and self._automatically_insert_view_element:
            view_arch = self._reorder_header_button(view_arch)
            view_arch = self._reorder_policy_field(view_arch)
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        elif view_type == "search" and self._automatically_insert_view_element:
            view_arch = self._reorder_state_filter_on_search_view(view_arch)

        if view_id and result.get("base_model", self._name) != self._name:
            View = View.with_context(base_model_name=result["base_model"])
        new_arch, new_fields = View.postprocess_and_fields(view_arch, self._name)
        result["arch"] = new_arch
        new_fields.update(result["fields"])
        result["fields"] = new_fields

        return result

    def action_restart(self):
        for record in self.sudo():
            record._run_pre_restart_check()
            record._run_pre_restart_action()
            record.write(record._prepare_restart_data())
            record._run_post_restart_check()
            record._run_post_restart_action()

    def _run_pre_restart_check(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_pre_restart_check"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_post_restart_check(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_post_restart_check"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_pre_restart_action(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_pre_restart_action"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_post_restart_action(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_post_restart_action"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": self._draft_state,
        }

    def _check_document_number_unlink(self, force_unlink=False):
        self.ensure_one()
        result = True
        if getattr(self, self._document_number_field) != "/" and not force_unlink:
            result = False
        return result

    def _check_state_unlink(self, force_unlink=False):
        self.ensure_one()
        result = True
        if self.state != "draft" and not force_unlink:
            result = False
        return result

    def _check_duplicate_document_number(self):
        self.ensure_one()
        result = True
        criteria = [
            (
                self._document_number_field,
                "=",
                getattr(self, self._document_number_field),
            ),
            (self._document_number_field, "!=", "/"),
            ("id", "!=", self.id),
        ]
        ObjectMixin = self.env[self._name]
        count_duplicate = ObjectMixin.search_count(criteria)
        if count_duplicate > 0:
            result = False
        return result

    @api.model
    def _reorder_header_button(self, view_arch):
        if not self._header_button_order:
            return view_arch
        _xpath = "/form/header"
        if len(view_arch.xpath(_xpath)) == 0:
            return view_arch
        node_xpath = view_arch.xpath(_xpath)[0]
        for node in node_xpath:
            if node.get("name") in self._header_button_order:
                node.set(
                    "order", str(self._header_button_order.index(node.get("name")))
                )
        to_sort = (e for e in node_xpath if e.tag == "button")
        no_sort = (e for e in node_xpath if e.tag == "field")
        node_xpath[:] = sorted(
            to_sort, key=lambda child: int(child.get("order", "100"))
        ) + list(no_sort)
        return view_arch

    @api.model
    def _reorder_policy_field(self, view_arch):
        if not self._policy_field_order:
            return view_arch
        _xpath = "/form/sheet/notebook/page[@name='policy']/group[@name='policy_2']"
        if len(view_arch.xpath(_xpath)) == 0:
            return view_arch
        node_xpath = view_arch.xpath(_xpath)[0]
        for node in node_xpath:
            if node.get("name") in self._policy_field_order:
                node.set("order", str(self._policy_field_order.index(node.get("name"))))
        to_sort = (e for e in node_xpath if e.tag == "field")
        node_xpath[:] = sorted(
            to_sort, key=lambda child: int(child.get("order", "100"))
        )
        return view_arch

    @api.model
    def _reconfigure_statusbar_visible(self, view_arch):
        if not self._automatically_reconfigure_statusbar_visible:
            return view_arch
        _xpath = "/form/header/field[@name='state']"
        if len(view_arch.xpath(_xpath)) == 0:
            return view_arch
        node_xpath = view_arch.xpath(_xpath)[0]
        node_xpath.set("statusbar_visible", self._statusbar_visible_label)
        return view_arch

    @api.model
    def _reorder_state_filter_on_search_view(self, view_arch):
        if not self._state_filter_order:
            return view_arch
        _xpath = "/search/group[@name='dom_state']"  # TODO: Make it as class attribute
        if len(view_arch.xpath(_xpath)) == 0:
            return view_arch
        node_xpath = view_arch.xpath(_xpath)[0]
        for node in node_xpath:
            if node.get("name") in self._state_filter_order:
                node.set("order", str(self._state_filter_order.index(node.get("name"))))
        to_sort = (e for e in node_xpath if e.tag == "filter")
        node_xpath[:] = sorted(
            to_sort, key=lambda child: int(child.get("order", "100"))
        )
        return view_arch
