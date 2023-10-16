from django.forms.formsets import DELETION_FIELD_NAME
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext
from django_bootstrap5.core import get_field_renderer
from django_bootstrap5.css import merge_css_classes
from django_bootstrap5.renderers import FieldRenderer, FormRenderer, FormsetRenderer


class DeleteFieldRenderer(FieldRenderer):
    """
    A field renderer for the delete field of an inline form.

    The default delete checkbox input will be hidden (display: none) and a
    button will be presented instead.
    """

    checkbox_classes = ("delete-cb", "d-none")

    def __init__(self, field, **kwargs):
        super().__init__(field, **kwargs)
        self.field_class = merge_css_classes(self.field_class, *self.checkbox_classes)

    def add_widget_class_attrs(self, widget=None):
        # Add self.field_class to the widget classes.
        # https://github.com/zostera/django-bootstrap5/issues/287
        if widget is None:  # pragma: no cover
            widget = self.widget
        super().add_widget_class_attrs(widget)
        classes = widget.attrs.get("class", "")
        if self.field_class:
            classes += f" {self.field_class}"
        widget.attrs["class"] = classes

    def get_button_class(self):
        """Return the CSS classes for the delete button."""
        return "btn w-100 btn-outline-secondary btn-sm inline-delete-btn"

    def get_button_title(self):
        """Return the title attribute for the delete button."""
        return gettext("Delete")

    def get_button_content(self):
        """Return the content for the delete button."""
        return """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-delete"><path d="M21 4H8l-7 8 7 8h13a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z"></path><line x1="18" y1="9" x2="12" y2="15"></line><line x1="12" y1="9" x2="18" y2="15"></line></svg>"""  # noqa

    def get_button_html(self):
        """Render the HTML for the delete button."""
        return (
            f'<button type="button" class="{self.get_button_class()}" '
            f'title="{self.get_button_title()}">{self.get_button_content()}</button>'
        )

    def render(self):
        """Render the delete checkbox and the delete button."""
        return mark_safe(self.get_field_html() + self.get_button_html())


class InlineFormRenderer(FormRenderer):
    """
    Renderer for the forms of an inline formset.

    The form will be rendered with two columns; a wider column for all the
    fields and a narrower (col-1) column for the delete field with a delete
    button.
    """

    delete_field_renderer = DeleteFieldRenderer

    def __init__(self, form, is_extra=False, **kwargs):
        super().__init__(form, **kwargs)
        self.is_extra = is_extra

    def get_form_container_class(self):
        """
        Return the CSS classes for the div that wraps the form fields and the
        delete button.
        """
        classes = "row mb-1 align-items-center py-1 form-container"
        if self.is_extra:
            classes += " extra-form"
        return classes

    def get_field_container_class(self):
        """Return the CSS classes for the div that wraps the form fields."""
        return "col fields-container"

    def get_delete_container_class(self):
        """Return the CSS classes for the div that wraps the delete button."""
        return "col-1 delete-container"

    def render(self):
        return format_html(
            '<div class="{container_class}">{form}</div>',
            container_class=self.get_form_container_class(),
            form=super().render(),
        )

    def render_delete_field(self, field, **kwargs):
        return self.delete_field_renderer(field, **kwargs).render()

    def render_fields(self):
        rendered_fields = rendered_delete = mark_safe("")
        kwargs = self.get_kwargs()
        renderer = get_field_renderer(**kwargs)
        for field in self.form:
            if field.name == DELETION_FIELD_NAME:
                rendered_delete = self.render_delete_field(field, **kwargs)
            else:
                rendered_fields += renderer(field, **kwargs).render()
        return format_html(
            '<div class="{field_container_class}">{fields}</div><div class="{delete_wrapper_class}">{delete}</div>',
            field_container_class=self.get_field_container_class(),
            fields=rendered_fields,
            delete_wrapper_class=self.get_delete_container_class(),
            delete=rendered_delete,
        )


class InlineFormsetRenderer(FormsetRenderer):
    """
    Renderer for inline formsets.

    The formset will be rendered with a button that allows adding more inline
    forms. The forms will be rendered in two columns, one for the form fields
    and one for a delete button.

    A rendered formset will have the following structure:
        <div class="formset-container">
            <div class="form-container row">
                <div class="fields-container col">FORM FIELDS</div>
                <div class="delete-container col-1">DELETE BUTTON</div>
            </div>
            ...
            <div class="add-row">
                <div class="empty-form">EMPTY FORM TEMPLATE</div>
                <button class="inline-add-btn">ADD BUTTON</button>
            </div>
        </div>

    Use the `add_text` keyword argument to modify the text for the add button.
    """

    form_renderer = InlineFormRenderer

    def __init__(self, formset, add_text="", **kwargs):
        super().__init__(formset, **kwargs)
        self.add_text = add_text

    def get_formset_container_class(self):
        """Return the CSS classes for the div that wraps the formset."""
        return f"{self.formset.prefix} formset-container mb-3"

    def get_add_button_class(self):
        """Return the CSS classes for the add button."""
        return "btn btn-outline-success inline-add-btn"

    def get_add_button_text(self):
        """Return the text for the add button label."""
        if self.add_text:
            return self.add_text
        return gettext("Add another %(verbose_name)s") % {"verbose_name": self.formset.model._meta.verbose_name}

    def get_add_button_label(self):
        """Return the label for the add button."""
        img = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-plus"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>"""  # noqa
        return img + f'<span class="align-middle">{self.get_add_button_text()}</span'

    def get_add_button_html(self):
        """Return the HTML for the button that adds another form to the formset."""
        return mark_safe(f'<button class="{self.get_add_button_class()}">{self.get_add_button_label()}</button>')

    def get_add_row_html(self):
        """
        Return the HTML for the div with the add button and the empty form
        template.
        """
        kwargs = self.get_kwargs()
        kwargs["is_extra"] = True
        empty_form = self.render_form(self.formset.empty_form, **kwargs)
        return mark_safe(
            '<div class="add-row">'
            f'<div class="empty-form d-none">{empty_form}</div>'
            f"{self.get_add_button_html()}</div>"
        )

    def render_form(self, form, **kwargs):
        return self.form_renderer(form, **kwargs).render()

    def render_forms(self):
        rendered_forms = mark_safe("")
        kwargs = self.get_kwargs()
        for form in self.formset.forms:
            kwargs["is_extra"] = form in self.formset.extra_forms
            rendered_forms += self.render_form(form, **kwargs)
        return rendered_forms

    def render(self):
        return format_html(
            '<div class="{formset_container}" data-prefix={prefix}>{html}{add_row}</div>',
            formset_container=self.get_formset_container_class(),
            prefix=self.formset.prefix,
            html=super().render(),
            add_row=self.get_add_row_html(),
        )
