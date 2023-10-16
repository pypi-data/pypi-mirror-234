from django import template

from mizdb_inlines.renderers import InlineFormsetRenderer

register = template.Library()


@register.simple_tag
def inline_formset(formset, **kwargs):
    return InlineFormsetRenderer(formset, **kwargs).render()
