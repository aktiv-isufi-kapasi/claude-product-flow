# Record shapes

Copy-paste starting points. Every one of these installs on Odoo Online.

## Manifest

The only Python in the module. A plain dict — no imports, no logic.

```python
# -*- coding: utf-8 -*-
{
    'name': 'Human readable name',
    'version': '18.0.1.0.0',
    'category': 'Website',
    'summary': 'One line the client would recognise',
    'author': 'Your company',
    'depends': ['base', 'website', 'product'],
    'data': [
        'data/01_models.xml',
        'security/ir.model.access.csv',
        'views/<module>_views.xml',
        'views/<module>_website.xml',
        'data/02_seed.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '<module>/static/src/scss/home.scss',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}
```

Declare a dependency explicitly when you write its records, even if it arrives
transitively. `website_sale` for `is_published` on products and the `/shop` routes;
`mail` if you set `ir.model.is_mail_thread`.

## New model and fields

```xml
<record id="model_x_ex_home_section" model="ir.model">
    <field name="name">Home Page Section</field>
    <field name="model">x_ex_home_section</field>
    <field name="state">manual</field>
</record>

<!-- x_name is the _rec_name for a custom model — define it or breadcrumbs
     and any m2o pointing here show ids. -->
<record id="field_x_ex_home_section__x_name" model="ir.model.fields">
    <field name="name">x_name</field>
    <field name="model_id" ref="model_x_ex_home_section"/>
    <field name="model">x_ex_home_section</field>
    <field name="field_description">Section</field>
    <field name="ttype">char</field>
    <field name="required">1</field>
    <field name="state">manual</field>
</record>

<record id="field_x_ex_home_section__x_title" model="ir.model.fields">
    <field name="name">x_title</field>
    <field name="model_id" ref="model_x_ex_home_section"/>
    <field name="model">x_ex_home_section</field>
    <field name="field_description">Heading</field>
    <field name="ttype">char</field>
    <field name="translate">1</field>
    <field name="state">manual</field>
</record>
```

Selection field:
```xml
<field name="ttype">selection</field>
<field name="selection">[('draft','Draft'),('open','Open')]</field>
```

Many2one:
```xml
<field name="ttype">many2one</field>
<field name="relation">product.template</field>
<field name="on_delete">set null</field>
```

## Field on a core model

`model_id` refs the core model's own xml_id; `model` repeats the technical name.

```xml
<record id="field_product_template__x_ex_featured_on_home" model="ir.model.fields">
    <field name="name">x_ex_featured_on_home</field>
    <field name="model_id" ref="product.model_product_template"/>
    <field name="model">product.template</field>
    <field name="field_description">Show in Product Carousel</field>
    <field name="ttype">boolean</field>
    <field name="state">manual</field>
</record>
```

Show it on the standard form with an inherit, and gate it on whatever makes it
meaningful so it never appears where it does nothing:

```xml
<record id="product_template_form_inherit" model="ir.ui.view">
    <field name="name">product.template.form.bs</field>
    <field name="model">product.template</field>
    <field name="inherit_id" ref="product.product_template_form_view"/>
    <field name="arch" type="xml">
        <field name="list_price" position="after">
            <field name="x_ex_featured_on_home" invisible="not is_published"/>
        </field>
    </field>
</record>
```

## Security

`security/ir.model.access.csv`:
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_x_ex_home_section_editor,x_ex_home_section.editor,model_x_ex_home_section,website.group_website_restricted_editor,1,1,1,0
access_x_ex_home_section_designer,x_ex_home_section.designer,model_x_ex_home_section,website.group_website_designer,1,1,1,1
```

Group and record rule:
```xml
<record id="group_portal_rep" model="res.groups">
    <field name="name">Rep Agency (region-filtered)</field>
    <field name="category_id" ref="module_category_myapp"/>
</record>

<record id="rule_content_region" model="ir.rule">
    <field name="name">Content: own regions only</field>
    <field name="model_id" ref="model_x_my_content"/>
    <field name="groups" eval="[(4, ref('group_portal_rep'))]"/>
    <field name="domain_force">
        ['|', ('x_region_ids','=',False),
              ('x_region_ids','in', user.x_region_ids.ids)]
    </field>
</record>
```

A group that declares no `implied_ids` stays independent of user types. A group implying
a user-type group cannot be ticked on a user of a different type.

## Backend screens

```xml
<record id="view_home_section_list" model="ir.ui.view">
    <field name="name">x_ex_home_section.list</field>
    <field name="model">x_ex_home_section</field>
    <field name="arch" type="xml">
        <list><field name="x_name"/><field name="x_code"/></list>
    </field>
</record>

<record id="action_home_section" model="ir.actions.act_window">
    <field name="name">Home Page Sections</field>
    <field name="res_model">x_ex_home_section</field>
    <field name="view_mode">list,form</field>
</record>

<menuitem id="menu_ex_root" name="Example Home"
          parent="website.menu_website_global_configuration"
          groups="website.group_website_restricted_editor"
          sequence="95"/>
<menuitem id="menu_ex_sections" name="Home Page Sections"
          parent="menu_ex_root" action="action_home_section" sequence="10"/>
```

## Public page

```xml
<record id="home_page_view" model="ir.ui.view">
    <field name="name">Example home page</field>
    <field name="type">qweb</field>
    <field name="key"><module>.home_page_view</field>
    <field name="arch" type="xml">
        <t t-name="<module>.home_page_view">
            <t t-call="website.layout">
                <t t-set="sections"
                   t-value="request.env['x_ex_home_section'].sudo().search([])"/>
                <t t-set="sec" t-value="sections.filtered(lambda s: s.x_code == 'hero')"/>
                <section class="bs-hero">
                    <p t-if="sec.x_eyebrow" class="bs-eyebrow" t-field="sec.x_eyebrow"/>
                    <h1 t-field="sec.x_title"/>
                </section>
                <t t-call="<module>.testimonials_band"/>
            </t>
        </t>
    </field>
</record>

<record id="home_page" model="website.page">
    <field name="name">Home</field>
    <field name="url">/example-home</field>
    <field name="view_id" ref="home_page_view"/>
    <field name="is_published" eval="True"/>
    <field name="website_indexed" eval="True"/>
    <field name="header_overlay" eval="True"/>
    <field name="footer_visible" eval="False"/>
    <field name="website_meta_title">...</field>
    <field name="website_meta_description">...</field>
</record>
```

`t-field` for anything the client should edit on the page. `t-esc` only for values that
must not be editable.

## Free-form block, isolated

The `oe_structure` lives alone in its own view so the pinning cannot reach the page:

```xml
<record id="testimonials_band" model="ir.ui.view">
    <field name="name">Testimonials band</field>
    <field name="type">qweb</field>
    <field name="key"><module>.testimonials_band</field>
    <field name="arch" type="xml">
        <t t-name="<module>.testimonials_band">
            <section class="oe_structure" id="oe_structure_ex_testimonials">
                <!-- seed content the client replaces -->
            </section>
        </t>
    </field>
</record>
```

The `id` must contain `oe_structure` — `extract_oe_structures` matches
`//*[hasclass("oe_structure")][contains(@id,"oe_structure")]`.

## Changing an existing page

```xml
<record id="hide_price_product" model="ir.ui.view">
    <field name="name">Hide price on product page</field>
    <field name="inherit_id" ref="website_sale.product"/>
    <field name="arch" type="xml">
        <xpath expr="//div[@itemprop='offers']" position="attributes">
            <attribute name="class">d-none</attribute>
        </xpath>
    </field>
</record>
```

This is presentation-level. Removing a price from the markup stops it being read or
scraped from the page; it is not access control, because the JSON endpoints can still be
asked. Say so explicitly when that distinction matters to the client.

## First-install-only configuration

```xml
<data noupdate="1">
    <function model="website" name="write">
        <value model="website" eval="obj().search([('homepage_url','=',False)]).ids"/>
        <value eval="{'homepage_url': '/example-home'}"/>
    </function>
</data>
```

Runs once, on install. A re-import never touches it again, so the client's later change
stands.

## Scheduled job

```xml
<record id="cron_archive_expired" model="ir.cron">
    <field name="name">Archive expired content</field>
    <!-- neutral model: the job walks several through env[] -->
    <field name="model_id" ref="base.model_ir_cron"/>
    <field name="state">code</field>
    <field name="user_id" ref="base.user_root"/>
    <field name="interval_number">1</field>
    <field name="interval_type">days</field>
    <field name="active" eval="True"/>
    <field name="code">
today = datetime.date.today().strftime('%Y-%m-%d')
for model, field in [('x_my_doc', 'x_date_end'), ('x_my_event', 'x_date_end')]:
    records = env[model].search([(field, '!=', False), (field, '&lt;', today)])
    if records:
        records.write({'x_active': False})
        log('Archived %s %s records' % (len(records), model))
    </field>
</record>
```

No `nextcall`. `fields` is not in the sandbox. `&lt;` because this is XML.

## Button logic

```xml
<record id="action_grant_access" model="ir.actions.server">
    <field name="name">Grant Rep Access</field>
    <field name="model_id" ref="base.model_res_users"/>
    <field name="binding_model_id" ref="base.model_res_users"/>
    <field name="state">code</field>
    <field name="code">
for user in records:
    user.write({'groups_id': [(4, env.ref('<module>.group_portal_rep').id)]})
    </field>
</record>
```

Bind it to a form button with a header inherit:
```xml
<xpath expr="//header" position="inside">
    <button name="%(<module>.action_grant_access)d" type="action"
            string="Grant Rep Access" class="btn-primary"/>
</xpath>
```

## Client-side data, no controller

```javascript
fetch("/web/dataset/call_kw", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
        jsonrpc: "2.0",
        method: "call",
        params: {
            model: "x_my_content",
            method: "search_read",
            args: [[["x_active", "=", true]], ["x_name", "x_summary"]],
            kwargs: {},
        },
    }),
}).then(r => r.json()).then(d => render(d.result));
```

Runs as the logged-in user. Record rules apply automatically — never reach for sudo to
make this work, the filtering is the point.
