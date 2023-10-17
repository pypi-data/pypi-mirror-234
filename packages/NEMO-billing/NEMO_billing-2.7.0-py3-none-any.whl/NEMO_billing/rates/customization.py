from NEMO.decorators import customization
from NEMO.views.customization import CustomizationBase


@customization(key="billing_rates", title="Rates")
class BillingRatesCustomization(CustomizationBase):
    variables = {
        "rates_expand_table": "",
        "allow_blank_rate": "",
        "rates_daily_per_account": "",
        "rates_show_all_categories": "",
    }

    def save(self, request, element=None):
        errors = super().save(request, element)
        if not errors:
            from NEMO.rates import rate_class

            rate_class.load_rates()
        return errors
