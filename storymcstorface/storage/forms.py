from django import forms
from django_select2 import forms as s2forms

from storage.models import StorageLog, StorageItem


class StorageItemWidget(s2forms.ModelSelect2Widget):
    search_fields = ["product__name__icontains"]


class StorageLogForm(forms.ModelForm):
    class Meta:
        model = StorageLog
        fields = fields = ("item", "quantity", "comment")
        widgets = {"item": StorageItemWidget}

    def __init__(self, *args, **kwargs):
        facility = kwargs.pop("facility")
        super(StorageLogForm, self).__init__(*args, **kwargs)
        print(facility)
        if facility:
            self.fields["item"].queryset = StorageItem.objects.filter(
                location__facility__slug=facility
            )
