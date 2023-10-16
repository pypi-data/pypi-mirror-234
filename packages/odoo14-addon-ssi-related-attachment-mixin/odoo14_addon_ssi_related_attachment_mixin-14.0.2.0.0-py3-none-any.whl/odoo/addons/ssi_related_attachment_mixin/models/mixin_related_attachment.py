# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval

from odoo.addons.ssi_decorator import ssi_decorator


class MixinRelatedAttachment(models.AbstractModel):
    _name = "mixin.related_attachment"
    _inherit = [
        "mixin.decorator",
    ]
    _description = "Mixin Object for Related Attachment"

    _related_attachment_create_page = False
    _related_attachment_page_xpath = "//page[last()]"

    def _compute_allowed_related_attachment_template_ids(self):
        obj_template = self.env["attachment.related_attachment_template"]
        for record in self:
            criteria = [("model", "=", self._name)]
            result = obj_template.search(criteria).ids
            record.allowed_related_attachment_template_ids = result

    related_attachment_template_id = fields.Many2one(
        string="Related Attachment Template",
        comodel_name="attachment.related_attachment_template",
        copy=False,
        domain=lambda self: [("model", "=", self._name)],
    )
    allowed_related_attachment_template_ids = fields.Many2many(
        string="Allowed Related Attachment Template",
        comodel_name="attachment.related_attachment_template",
        compute="_compute_allowed_related_attachment_template_ids",
        store=False,
    )
    related_attachment_ids = fields.One2many(
        string="Related Attachments",
        comodel_name="attachment.related_attachment",
        inverse_name="res_id",
        domain=lambda self: [("model", "=", self._name)],
        auto_join=True,
    )

    @ssi_decorator.insert_on_form_view()
    def _related_attachment_insert_form_element(self, view_arch):
        if self._related_attachment_create_page:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id="ssi_related_attachment_mixin.related_attachment_page",
                xpath=self._related_attachment_page_xpath,
                position="after",
            )
        return view_arch

    def _get_related_attachment_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    def _evaluate_related_attachment(self, template):
        self.ensure_one()
        res = False
        localdict = self._get_related_attachment_localdict()
        try:
            safe_eval(template.python_code, localdict, mode="exec", nocopy=True)
            if "result" in localdict:
                res = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error)
        return res

    def _get_template_related_attachment(self):
        result = False
        obj_related_attachment_template = self.env[
            "attachment.related_attachment_template"
        ]
        criteria = [
            ("model_id.model", "=", str(self._name)),
        ]
        template_id = obj_related_attachment_template.search(
            criteria,
            limit=1,
        )
        if self._evaluate_related_attachment(template_id):
            result = template_id.id
        return result

    @api.onchange(
        "related_attachment_template_id",
    )
    def onchange_related_attachment_ids(self):
        res = []
        if self.related_attachment_ids:
            to_check = self.related_attachment_ids.mapped("attachment_id")
            if to_check:
                error_msg = _("Attachment already exist")
                raise UserError(_("%s") % (error_msg))
        self.related_attachment_ids = [(5, 0, 0)]
        if self.related_attachment_template_id:
            res = self.create_related_attachment_ids()
        self.related_attachment_ids = res

    def create_related_attachment_ids(self):
        self.ensure_one()
        obj_related_attachment_template_detail = self.env[
            "attachment.related_attachment_template_detail"
        ]
        obj_related_attachment = res = self.env["attachment.related_attachment"]
        sequence = 0

        criteria = [("template_id", "=", self.related_attachment_template_id.id)]
        related_attachment_ids = obj_related_attachment_template_detail.search(
            criteria, order="sequence"
        )
        if related_attachment_ids:
            for related_attachment in related_attachment_ids:
                sequence += 1
                res += obj_related_attachment.create(
                    {
                        "model": self._name,
                        "res_id": self.id,
                        "template_id": self.related_attachment_template_id.id,
                        "template_detail_id": related_attachment.id,
                    }
                )
        return res

    def action_reload_rel_attachment_template(self):
        for record in self.sudo():
            record.write(
                {
                    "related_attachment_template_id": self._get_template_related_attachment(),
                }
            )
            record._reload_rel_attachment_detail()

    def action_reload_rel_attachment_detail(self):
        for record in self.sudo():
            record._reload_rel_attachment_detail()

    def _reload_rel_attachment_detail(self):
        self.ensure_one()
        if self.related_attachment_template_id:
            template = self.related_attachment_template_id
            allowed_details = template.detail_ids
            self.related_attachment_ids.filtered(
                lambda r: r.template_detail_id.id not in allowed_details.ids
            ).unlink()
            to_be_added = template.detail_ids - self.related_attachment_ids.mapped(
                "template_detail_id"
            )
            for detail in to_be_added:
                self.related_attachment_ids.create(
                    {
                        "model": self._name,
                        "res_id": self.id,
                        "template_id": template.id,
                        "template_detail_id": detail.id,
                    }
                )
        else:
            self.related_attachment_ids.unlink()

    def unlink(self):
        related_attachments = self.mapped("related_attachment_ids")
        res = super(MixinRelatedAttachment, self).unlink()
        if res:
            related_attachments.unlink()
        return res

    @api.model
    def create(self, values):
        _super = super(MixinRelatedAttachment, self)
        result = _super.create(values)
        if not result.related_attachment_template_id:
            template_id = result._get_template_related_attachment()
            if template_id:
                result.sudo().write({"related_attachment_template_id": template_id})
                result.sudo().action_reload_rel_attachment_detail()
        return result
