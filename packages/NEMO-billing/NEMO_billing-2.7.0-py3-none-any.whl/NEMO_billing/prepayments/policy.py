import datetime
from http import HTTPStatus
from typing import List, Optional, Union

from NEMO.models import (
    Area,
    AreaAccessRecord,
    Consumable,
    ConsumableWithdraw,
    Project,
    Reservation,
    StaffCharge,
    Tool,
    UsageEvent,
    User,
)
from NEMO.policy import NEMOPolicy
from django.http import HttpResponse, HttpResponseBadRequest

from NEMO_billing.invoices.models import BillableItemType
from NEMO_billing.prepayments.exceptions import (
    ChargeTypeNotAllowedForProjectException,
    ProjectFundsFacilityNotAllowedException,
    ProjectFundsNotSetException,
    ProjectInsufficientFundsException,
)


# Some validation for charges are tricky:
# 1. Tool usage, all good we have a policy method containing the project
# 2. Staff charge, all good we can use check_billing_to_project directly
# 3. Area access record is not possible because we don't have the project
# 4. Training we don't have the project either
# 5. Consumables we don't know if those charges are from post usage or not. Either way we cannot separate at the moment
# 6. Custom charges we can use check_billing_to_project
# 7. Missed reservation cannot be dissociated from tool usage or area access
# Bonus: we are also preventing reservation on tool and areas if those are not enabled

# Decided to use signals in models.py to prevent any charge not authorized by the fund


class PrepaymentPolicy(NEMOPolicy):
    def check_to_enable_tool(
        self, tool: Tool, operator: User, user: User, project: Project, staff_charge: bool, remote_work: bool = False
    ):
        response = super().check_to_enable_tool(tool, operator, user, project, staff_charge)
        if response.status_code != HTTPStatus.OK:
            return response
        try:
            billable_type = (
                BillableItemType.STAFF_CHARGE if (staff_charge or remote_work) else BillableItemType.TOOL_USAGE
            )
            self.check_project_prepayment_charge(project, billable_type)
        except ChargeTypeNotAllowedForProjectException as e:
            return HttpResponseBadRequest(e.msg)
        return HttpResponse()

    def check_to_save_reservation(
        self,
        cancelled_reservation: Optional[Reservation],
        new_reservation: Reservation,
        user_creating_reservation: User,
        explicit_policy_override: bool,
    ) -> (List[str], bool):
        try:
            charge_type = BillableItemType.TOOL_USAGE if new_reservation.tool else BillableItemType.AREA_ACCESS
            self.check_project_prepayment_charge(new_reservation.project, charge_type)
        except ChargeTypeNotAllowedForProjectException as e:
            return [e.msg], False
        return super().check_to_save_reservation(
            cancelled_reservation, new_reservation, user_creating_reservation, explicit_policy_override
        )

    def check_project_prepayment_charge(self, project: Project, billable_item_type: BillableItemType):
        if (
            hasattr(project, "projectprepaymentdetail")
            and billable_item_type not in project.projectprepaymentdetail.billable_charge_types
        ):
            raise ChargeTypeNotAllowedForProjectException(project, billable_item_type)

    def check_billing_to_project(
        self,
        project: Project,
        user: User,
        item: Union[Tool, Area, Consumable, StaffCharge] = None,
        charge: Union[UsageEvent, AreaAccessRecord, ConsumableWithdraw, StaffCharge, Reservation] = None,
        *args,
        **kwargs
    ):
        super().check_billing_to_project(project, user, item, charge, *args, **kwargs)
        if hasattr(project, "projectprepaymentdetail"):
            if isinstance(item, StaffCharge):
                self.check_project_prepayment_charge(project, BillableItemType.STAFF_CHARGE)
            self.check_prepayment_allowed_for_core_facility(project, item)
            self.check_prepayment_status_for_project(project)

    def check_prepayment_allowed_for_core_facility(self, project: Project, item):
        only_facilities = project.projectprepaymentdetail.only_core_facilities.all()
        check_item = not isinstance(item, Consumable) or item.core_facility
        if only_facilities and check_item and item.core_facility not in only_facilities:
            raise ProjectFundsFacilityNotAllowedException(project, only_facilities)

    def check_prepayment_status_for_project(self, project: Project):
        # Project has to have prepayments
        if not project.projectprepaymentdetail.fund_set.exists():
            raise ProjectFundsNotSetException(project)
        else:
            prepayment = project.projectprepaymentdetail
            date_to_check = datetime.date.today()
            # This function will raise ProjectFundsExpiredException and ProjectFundsInactiveException
            # At least one prepayment has to be active and not expired
            if not prepayment.active_funds(date_to_check).exists():
                raise ProjectInsufficientFundsException(project)
            else:
                # check total available funds (check since last balance update)
                # we have to check each month separately and calculate available funds and charges
                # otherwise we would miss expiring funds or funds not active yet
                # This method will throw an exception if any month period between dates has insufficient funds
                prepayment.get_prepayment_info(until=date_to_check, raise_exception=True)
