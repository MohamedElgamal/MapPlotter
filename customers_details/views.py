from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic.edit import (
    CreateView,
    View,
)
from .forms import CustomersUploadCsvForm

# Create your views here.


class CustomersUploadView(View):
    template_name = "customers_csv_upload.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "form": CustomersUploadCsvForm(),
            },
        )

    def post(self, request):
        upload_form = CustomersUploadCsvForm(request.POST, request.FILES)
        if upload_form.is_valid():
            csv_file = upload_form.cleaned_data["csv_file"]
            print(type(csv_file))
            self.save_csv(csv_file)
        else:
            return render(
                request,
                self.template_name,
                {
                    "form": upload_form,
                },
            )
        return render(
            request,
            self.template_name,
            {
                "form": CustomersUploadCsvForm(),
            },
        )

    def save_csv(self, csv_file):
        with open("customers_details/media/" + csv_file.name, "wb+") as dest:
            for chunk in csv_file.chunks():
                dest.write(chunk)
