# mizdb-inlines

Django inline formsets with bootstrap for the MIZDB app.

Requires [django_bootstrap5](https://github.com/zostera/django-bootstrap5).

Formsets will be rendered in a layout with two columns. One column is for the formset
form, and the other column is for the delete button of a given formset form.

## Installation

Install using pip:

```shell
pip install mizdb-inlines
```

Add to your `INSTALLED_APPS` in your `settings.py`:

```python
INSTALLED_APPS = [
    ...,
    "mizdb_inlines",
]
```

## Usage

Add `mizdb_inlines/js/mizdb_inlines.js` javascript and render the formset using the `inline_formset` template tag from the `mizdb_inlines` template tag library:

```html
<!DOCTYPE html>
{% load static mizdb_inlines django_bootstrap5 %}
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Awesome Form</title>
    {{ combined_media }}
    <script src="{% static 'mizdb_inlines/js/mizdb_inlines.js' %}"></script>
    {% bootstrap_css %}
    {% bootstrap_javascript %}
</head>
<body>
<form class="container mt-3" method="post">
    {% csrf_token %}

    {% bootstrap_form form %}
    {% inline_formset formset layout="horizontal" %}
    {% bootstrap_button button_type="submit" button_class="btn-success" content="Save" %}
    {% bootstrap_button button_type="reset" button_class="btn-warning" content="Reset" %}
</form>
</body>
</html>
```
The template tag instantiates an `InlineFormsetRenderer` and returns the renderers `render()` output. 
The template tag passes all keyword arguments along to the renderer. 
The renderer takes an additional keyword argument `add_text` with which you can set the text of the add button (defaults to the verbose name of the inline formset model).
For example, in a template:
```html
{% inline_formset formset layout="horizontal" add_text="Add another delicious Topping" %}
```


### View mixin for inline formsets

Use the `InlineFormsetMixin` view mixin to remove some of the boilerplate from handling inline formsets. 
Simply declare the formset classes to use in the `formset_classes` attribute.

```python
from mizdb_inlines.views import InlineFormsetMixin


class MyView(InlineFormsetMixin, UpdateView):
    model = Pizza
    fields = "__all__"
    template_name = "pizza.html"
    success_url = "/"

    formset_classes = (
        inlineformset_factory(Pizza, Toppings, fields="__all__", extra=1),
        MyAwesomeFormset,
    )
```

This will add formset instances to the template context with the context variable `formsets`. 
The combined media of the formsets and the view's model form is available with the variable `combined_media` :
```html
{{ combined_media }}

{% for formset in formsets %}
    {% inline_formset formset %}
{% endfor %}
```

To perform additional actions after the form and formsets have been saved, you can use 
the `post_save` hook:
```python
class MyView(InlineFormsetMixin, UpdateView):
    ...
    
    def post_save(self, form, formsets):
        # Log that the form was saved:
        create_logentry(form, formsets)
```

## Development & Demo

```bash
python3 -m venv venv
source venv/bin/activate
make init
```

See the demo for a preview: run `make init-demo` and then start the demo server `python demo/manage.py runserver`.

Run tests with `make test`. To install required browsers for playwright: `playwright install`.