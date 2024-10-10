from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import (
    CreateView,
    View,
)
from .forms import CustomersUploadCsvForm
import urllib.parse
import os

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
        csv_file = None
        if upload_form.is_valid():
            csv_file = upload_form.cleaned_data["csv_file"]
            self.save_csv(csv_file)
        else:
            return render(
                request,
                self.template_name,
                {
                    "form": upload_form,
                },
            )
        success_url = reverse_lazy("customers_migration", kwargs={"file": csv_file})
        return redirect(success_url)

    def save_csv(self, csv_file):
        with open("customers_details/media/" + csv_file.name, "wb+") as dest:
            for chunk in csv_file.chunks():
                dest.write(chunk)


class CustomersMigrationView(View):
    template_name = "customers_migration.html"

    def get(self, request, **kwargs):
        return render(
            request,
            self.template_name,
        )

    def post(self, request, **kwargs):
        csv_file = urllib.parse.unquote(kwargs.get("file"))
        print("hitted")
        is_file_found = self.check_file_exists(csv_file)
        return render(
            request,
            self.template_name,
            {},
        )

    def check_file_exists(self, file):
        file_list = os.listdir("customers_details/media/")
        for f in file_list:
            if f == file:
                return True
        return False

    # get passed query para (Done)
    # search for file that has passed name (Done)
    # if not exists print error message you need to upload file again
    # else:
    # read csv file line by line and start map it into corresponding tabels
