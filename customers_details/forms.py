from django import forms
from django.core.exceptions import ValidationError

ALLOWED_FILE_TYPE = ["text/csv"]


class CustomersUploadCsvForm(forms.Form):
    csv_file = forms.FileField(
        label="Select csv file that contain customers records.  ",
    )

    def clean_csv_file(self):
        uploaded_file = self.cleaned_data["csv_file"]
        if uploaded_file.content_type not in ALLOWED_FILE_TYPE:
            raise ValidationError(
                f"your are trying to upload unsupported file ext. allowed ext {', '.join(ALLOWED_FILE_TYPE)}."
            )
        return uploaded_file
