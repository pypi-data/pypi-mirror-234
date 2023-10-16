from unittest.mock import patch

import pytest
from django import forms
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import FormMixin

from mizdb_inlines.views import InlineFormsetMixin
from tests.testapp.models import Contact, PhoneNumber


class NumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = forms.ALL_FIELDS

    class Media:
        js = ["should/be/included"]


class BaseViewMixin(InlineFormsetMixin):
    model = Contact
    fields = forms.ALL_FIELDS
    formset_classes = (forms.inlineformset_factory(Contact, PhoneNumber, form=NumberForm, extra=1),)
    success_url = "/"


class FormsetUpdateView(BaseViewMixin, UpdateView):
    pass


class FormsetCreateView(BaseViewMixin, CreateView):
    pass


@pytest.fixture
def prefix():
    """Return the prefix for the inline formset forms."""
    return "phone_numbers"


@pytest.fixture
def management_form_data(prefix):
    """Return the data for the formset management form."""
    return {f"{prefix}-INITIAL_FORMS": 0, f"{prefix}-TOTAL_FORMS": 1}


@pytest.fixture
def valid_form_data():
    """Return valid data for the model form."""
    return {"first_name": "Bob", "last_name": "Testman"}


@pytest.fixture
def invalid_form_data(valid_form_data):
    """Return invalid data for the model form."""
    data = valid_form_data.copy()
    data.pop("last_name")
    return data


@pytest.fixture
def valid_formset_data(prefix, management_form_data, view_object):
    """Return valid data for the inline formset."""
    formset_data = {
        f"{prefix}-0-contact": str(view_object.pk) if view_object else "",
        f"{prefix}-0-label": "Home",
        f"{prefix}-0-number": "1234",
    }
    return {**management_form_data, **formset_data}


@pytest.fixture
def invalid_formset_data(prefix, valid_formset_data):
    """Return invalid data for the inline formset."""
    data = valid_formset_data.copy()
    data.pop(f"{prefix}-0-number")
    return data


@pytest.fixture
def form_valid():
    # Default value for the request_data fixture.
    # Override with test method parametrization.
    return True


@pytest.fixture
def formset_valid():
    # Default value for the request_data fixture.
    # Override with test method parametrization.
    return True


@pytest.fixture
def request_data(
    form_valid,
    formset_valid,
    valid_form_data,
    invalid_form_data,
    valid_formset_data,
    invalid_formset_data,
):
    """Return the data for the POST request."""
    data = {}
    if form_valid:
        data.update(valid_form_data)
    else:
        data.update(invalid_form_data)
    if formset_valid:
        data.update(valid_formset_data)
    else:
        data.update(invalid_formset_data)
    return data


@pytest.fixture
def post_request(rf, request_data, contact_obj):
    """Return a POST request."""
    return rf.post(str(contact_obj.pk), request_data)


@pytest.fixture
def view_object(view_class, contact_obj):
    """Return the model instance under test or None."""
    if issubclass(view_class, UpdateView):
        return contact_obj
    return None


@pytest.fixture
def view(view_class, post_request, view_object):
    """Return a view instance with request and kwargs attributes set."""
    view = view_class()
    view.request = post_request
    view.kwargs = {view_class.pk_url_kwarg: str(view_object.pk)} if view_object else {}
    return view


@pytest.fixture
def template_context(view, view_object):
    """Return the template context data."""
    view.object = view_object
    return view.get_context_data()


@pytest.mark.django_db
@pytest.mark.parametrize("view_class", [FormsetUpdateView, FormsetCreateView])
class TestInlineFormsetMixin:
    @pytest.mark.parametrize("form_valid, formset_valid", [(True, False)])
    def test_form_valid_formsets_invalid(self, view, form_valid, formset_valid):
        """
        Assert that `form_invalid` is called if the form is valid but the
        formsets are invalid.
        """
        with patch.object(FormMixin, "form_invalid") as form_invalid_mock:
            view.post(view.request)
            form_invalid_mock.assert_called()

    def test_formsets_added_to_context(self, template_context):
        """Assert that the formsets are added to the template context."""
        assert "formsets" in template_context

    def test_formset_media_added_to_context(self, template_context):
        """Assert that the formset media is added to the template context."""
        assert "combined_media" in template_context
        assert "should/be/included" in template_context["combined_media"]._js

    @pytest.mark.parametrize("form_valid, formset_valid", [(True, True)])
    def test_form_saved(self, view, form_valid, formset_valid):
        """Assert that the form is saved if everything is valid."""
        view.post(view.request)
        assert view.object.first_name == "Bob"  # was "Alice"

    @pytest.mark.parametrize("form_valid, formset_valid", [(True, True)])
    def test_formset_saved(self, view, form_valid, formset_valid):
        """Assert that the formsets are saved if everything is valid."""
        view.post(view.request)
        assert ("Home", "1234") in view.object.phone_numbers.values_list("label", "number")
