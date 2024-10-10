from django.db import models

# Create your models here.


class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=256, default="", blank=False)
    customer_created_at = models.DateTimeField(auto_now_add=True)
    customer_updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(customer_name__length__gte=2),
                name="customer_name_length",
            )
        ]
        db_table = "customers"

    def __str__(self):
        return self.customer_name


class OsoulCustomersDetails(models.Model):
    osoul_person_id = models.AutoField(primary_key=True)
    osoul_account_num = models.IntegerField(default=0)
    osoul_person_code = models.IntegerField()
    osoul_address = models.CharField(max_length=512, default="", blank=False)
    osoul_person_created_at = models.DateTimeField(auto_now_add=True)
    osoul_person_update_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "osoul_customers_details"

    def __str__(self):
        return f"Account: {self.osoul_account_num}, Code: {self.osoul_person_code}"


class CustomerPhones(models.Model):
    phone_num = models.CharField(max_length=25, default="", blank=False)
    customer = models.ForeignKey(
        Customers, on_delete=models.CASCADE, related_name="phones"
    )
    phone_created_at = models.DateTimeField(auto_now_add=True)
    phone_updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("phone_num", "customer")
        db_table = "customer_phones"

    def __str__(self):
        return self.phone_num


class OsmAddresses(models.Model):
    osm_address_id = models.AutoField(primary_key=True)
    osm_geo_location = models.JSONField()
    customer = models.ForeignKey(
        Customers, on_delete=models.CASCADE, related_name="osm_addresses"
    )
    osm_created_at = models.DateTimeField(auto_now_add=True)
    osm_updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "osm_addresses"

    def __str__(self):
        return f"Address ID: {self.osm_address_id}, Customer: {self.customer}"
