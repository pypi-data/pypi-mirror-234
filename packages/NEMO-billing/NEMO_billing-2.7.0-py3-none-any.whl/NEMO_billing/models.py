import pytz
from NEMO.exceptions import ProjectChargeException
from NEMO.models import (
    Area,
    BaseCategory,
    BaseModel,
    Consumable,
    Project,
    SerializationByNameModel,
    StaffCharge,
    Tool,
    User,
)
from django.core.exceptions import ValidationError
from django.db import models

from NEMO_billing.templatetags.billing_tags import cap_discount_installed


class CoreFacility(BaseModel):
    name = models.CharField(max_length=200, unique=True, help_text="The name of this core facility.")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Core facilities"


class CoreRelationship(BaseModel):
    core_facility = models.ForeignKey(CoreFacility, on_delete=models.CASCADE)
    tool = models.OneToOneField(Tool, related_name="core_rel", blank=True, null=True, on_delete=models.CASCADE)
    area = models.OneToOneField(Area, related_name="core_rel", blank=True, null=True, on_delete=models.CASCADE)
    staff_charge = models.OneToOneField(
        StaffCharge, related_name="core_rel", blank=True, null=True, on_delete=models.CASCADE
    )
    consumable = models.OneToOneField(
        Consumable, related_name="core_rel", blank=True, null=True, on_delete=models.CASCADE
    )

    def get_item(self):
        return self.area or self.tool or self.consumable or self.staff_charge

    def __str__(self):
        return f"{self.get_item()} - {self.core_facility}"


class CustomCharge(BaseModel):
    name = models.CharField(max_length=255, help_text="The name of this custom charge.")
    additional_details = models.CharField(
        max_length=255, null=True, blank=True, help_text="Additional details for this charge."
    )
    customer = models.ForeignKey(
        User, related_name="custom_charge_customer", on_delete=models.CASCADE, help_text="The customer to charge."
    )
    creator = models.ForeignKey(
        User,
        related_name="custom_charge_creator",
        on_delete=models.CASCADE,
        help_text="The person who created this charge.",
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, help_text="The project to bill for this charge.")
    date = models.DateTimeField(help_text="The date of the custom charge.")
    amount = models.DecimalField(
        decimal_places=2, max_digits=8, help_text="The amount of the charge. Use a negative amount for adjustments."
    )
    core_facility = models.ForeignKey(CoreFacility, null=True, blank=True, on_delete=models.SET_NULL)
    cap_eligible = models.BooleanField(default=False, help_text="Check this box to make this charge count towards CAP")

    def clean(self):
        errors = {}
        if self.amount == 0:
            errors["amount"] = "Please enter a positive or negative amount"
        if self.project_id and self.customer_id:
            try:
                from NEMO.policy import policy_class as policy

                policy.check_billing_to_project(self.project, self.customer, self)
            except ProjectChargeException as e:
                errors["project"] = e.msg
        if cap_discount_installed():
            # If this custom charge is cap eligible, check that there is actually a matching CAP configuration
            if self.cap_eligible:
                if self.customer_id and self.project_id:
                    from NEMO_billing.cap_discount.models import CAPDiscountConfiguration

                    rate_category = self.project.projectbillingdetails.category
                    from NEMO_billing.invoices.models import BillableItemType

                    cap_filter = CAPDiscountConfiguration.objects.filter(
                        rate_category=rate_category,
                        charge_types__contains=BillableItemType.CUSTOM_CHARGE.value,
                    )
                    if self.core_facility:
                        cap_filter = cap_filter.filter(core_facilities__in=[self.core_facility])
                    else:
                        cap_filter = cap_filter.filter(core_facilities__isnull=True)
                    if not cap_filter.exists():
                        errors[
                            "cap_eligible"
                        ] = f"No CAP configuration accepting Custom charges exists for this rate category ({rate_category})"
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.name


# Create and add a shortcut function to get core_facility from Tool, Consumable, Area or Staff Charge
def get_core_facility(self):
    # Add an exception for tool children, whose core facility is the parent's core facility
    if isinstance(self, Tool) and self.is_child_tool():
        return self.parent_tool.core_facility
    if hasattr(self, "core_rel"):
        return self.core_rel.core_facility


class Department(BaseCategory):
    pass


class InstitutionType(BaseCategory):
    pass


class Institution(SerializationByNameModel):
    name = models.CharField(max_length=255, unique=True, help_text="The unique name for this institution")
    institution_type = models.ForeignKey(InstitutionType, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=2, choices=sorted(pytz.country_names.items(), key=lambda c: c[1]))
    zip_code = models.CharField(max_length=12, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


setattr(Tool, "core_facility", property(get_core_facility))
setattr(Consumable, "core_facility", property(get_core_facility))
setattr(Area, "core_facility", property(get_core_facility))
setattr(StaffCharge, "core_facility", property(get_core_facility))
