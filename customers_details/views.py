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
import csv
from .models import (
    Customers,
    CustomerPhones,
    OsoulCustomersDetails,
)

# Create your views here.


class CustomersUploadView(View):
    template_name = "customers_csv_upload.html"

    def get(self, request, **kwargs):
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

    def get(self, request, file):
        return render(
            request,
            self.template_name,
        )

    def post(self, request, file):
        csv_file = urllib.parse.unquote(file)
        is_file_found = self.check_file_exists(csv_file)
        if is_file_found:
            csv_dict = self.read_csv_file(f"customers_details/media/{csv_file}")
            self.migrate_into_customers_schema(csv_dict)
        else:
            return render(
                request,
                CustomersUploadView.template_name,
                {
                    "form": CustomersUploadCsvForm(),
                    "error_msg": "Please try to upload same file again, uploaded file is missing from server!!",
                },
            )
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

    def read_csv_file(self, file_path):
        print(f" file location : {file_path}")
        try:
            with open(file_path, mode="r", encoding="utf-8") as file_obj:
                reader_obj = csv.DictReader(file_obj)
                rows = list(reader_obj)
            return rows
        except Exception:
            return None

    def migrate_into_customers_schema(self, customers_dict):
        for row in customers_dict:
            customer = Customers(
                customer_name=row["nameperson"],
                customer_created_at=row["persondatecreate"],
            )
            customer.save()
            phone = CustomerPhones(
                phone_num=row["Phonenumber"],
                customer=customer,
                phone_created_at=row["persondatecreate"],
            )
            phone.save()
            if row["mobilenumber"] is not "":
                phone = CustomerPhones(
                    phone_num=row["mobilenumber"],
                    customer=customer,
                    phone_created_at=row["persondatecreate"],
                )
            phone.save()
            osoul_customer_details = OsoulCustomersDetails(
                osoul_person_id=row["idperson"],
                customer=customer,
                osoul_account_num=row["AccountNumber"],
                osoul_person_code=row["codeperson"],
                osoul_address=row["address"],
                osoul_person_created_at=row["persondatecreate"],
            )
            osoul_customer_details.save()
            print(row)

    # get passed query para (Done)
    # search for file that has passed name (Done)
    # if not exists print error message you need to upload file again (Done)
    # else:
    # read csv file line by line and start map it into corresponding tables
    # after the process completed move operated file into media/operated directory
