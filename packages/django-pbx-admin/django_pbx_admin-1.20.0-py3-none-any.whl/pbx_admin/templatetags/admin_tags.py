from math import floor, log

from django.template import Library, loader

register = Library()


@register.simple_tag(takes_context=True)
def fieldset(context, fieldset, form=None, formset=None, nested_list=None, sub_object=None):
    context_dict = context.flatten()

    if form:
        context_dict["form"] = form
        context_dict["fields"] = [form[field] for field in fieldset["fields"]]

    if formset:
        context_dict["formset"] = formset

    if nested_list:
        context_dict["nested_list"] = nested_list
        context_dict["nested_admin"] = fieldset["nested_admin"]
        context_dict["nested_queryset"] = fieldset["nested_queryset"]
        context_dict["nested_fields"] = fieldset.get(
            "nested_fields", fieldset["nested_admin"].list_display
        )
        if sub_object:
            context_dict["sub_object"] = True
            context_dict["sub_admin"] = fieldset["sub_admin"]
            context_dict["sub_related_field"] = fieldset["sub_related_field"]
            context_dict["sub_fields"] = fieldset.get(
                "sub_fields", fieldset["sub_admin"].list_display
            )
            context_dict["sub_title"] = fieldset["sub_title"]

    context_dict["fieldsets"] = fieldset.get("fieldsets")

    if "template_name" in fieldset:
        template_name = fieldset["template_name"]
    elif formset:
        template_name = "pbx_admin/formset.html"
    else:
        template_name = "pbx_admin/forms/form.html"

    if "html" in fieldset and callable(fieldset["html"]):
        func = fieldset["html"]
        kwargs = {}
        if form:
            kwargs["form"] = form
        if formset:
            kwargs["formset"] = formset
        fieldset["html"] = func(**kwargs) or ""

    template = loader.get_template(template_name)
    return template.render(context_dict, context.request)


@register.inclusion_tag("pbx_admin/list_row.html", takes_context=True)
def render_list_row(context, admin, obj, fields_list=None, show_actions=True, outer_tag=True):
    obj_id = None
    if admin.pk_url_kwarg is not None:
        obj_id = obj.pk
    if admin.slug_field is not None:
        obj_id = getattr(obj, admin.slug_field)

    fields = []
    fields_list = fields_list or admin.list_display
    for field_name in fields_list:
        tooltip = None

        if hasattr(admin, field_name):
            field = getattr(admin, field_name)
            value = field(obj) if callable(field) else field
            if hasattr(field, "tooltip"):
                tooltip = field.tooltip
                tooltip = tooltip(obj) if callable(tooltip) else tooltip
        else:
            value = getattr(obj, field_name)

        fields.append({"is_bool": isinstance(value, bool), "value": value, "tooltip": tooltip})

    row = {
        "obj": obj,
        "obj_id": obj_id,
        "fields": fields,
        "show_actions": show_actions,
        "menu_actions": show_actions or admin.only_menu_actions,
        "outer_tag": outer_tag,
    }

    if show_actions or admin.only_menu_actions:
        actions = admin.get_list_actions(context.request, obj)
        row.update(
            {
                "default_action": actions[0] if actions else None,
                "actions": actions[1:] if len(actions) > 1 else None,
            }
        )
    return row


@register.simple_tag
def tooltip(field):
    if hasattr(field, "tooltip"):
        return field.tooltip
    if hasattr(field.field, "tooltip"):
        return field.field.tooltip
    return ""


@register.filter
def widget_has_attribute(field, attr_name):
    widget = field.field.widget
    return attr_name in widget.attrs


@register.filter
def humanize_number(num):
    if num == 0:
        return "0"
    units = ["", "K", "M", "B", "T", "Q"]
    k = 1000
    magnitude = floor(log(num, k))
    if num >= 1_000_000:  # use higher precision
        num = floor(num / k**magnitude * 10) / 10
    else:
        num = floor(num / k**magnitude)
    formatted_num = f"{num:2f}".rstrip("0").rstrip(".")
    try:
        return f"{formatted_num}{units[magnitude]}"
    except IndexError:
        return "INF"
