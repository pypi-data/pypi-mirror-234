from NEMO.serializers import ModelSerializer
from NEMO.views.api import ModelViewSet
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.fields import CharField

from NEMO_billing.models import CustomCharge, Department, Institution, InstitutionType


class CustomChargeSerializer(FlexFieldsModelSerializer, ModelSerializer):
    class Meta:
        model = CustomCharge
        fields = "__all__"
        expandable_fields = {
            "customer": "NEMO.serializers.UserSerializer",
            "creator": "NEMO.serializers.UserSerializer",
            "project": "NEMO.serializers.ProjectSerializer",
        }

    customer_name = CharField(source="customer.get_name")
    creator_name = CharField(source="creator.get_name")


class CustomChargeViewSet(ModelViewSet):
    filename = "custom_charges"
    queryset = CustomCharge.objects.all()
    serializer_class = CustomChargeSerializer
    filterset_fields = {
        "name": ["exact"],
        "customer": ["exact", "in"],
        "creator": ["exact", "in"],
        "project": ["exact", "in"],
        "date": ["exact", "month", "year", "gte", "gt", "lte", "lt"],
        "amount": ["exact", "gte", "gt", "lte", "lt"],
        "core_facility": ["exact", "in", "isnull"],
    }


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class DepartmentViewSet(ModelViewSet):
    filename = "departments"
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filterset_fields = {
        "name": ["exact", "contains"],
    }


class InstitutionTypeSerializer(ModelSerializer):
    class Meta:
        model = InstitutionType
        fields = "__all__"


class InstitutionTypeViewSet(ModelViewSet):
    filename = "institution_types"
    queryset = InstitutionType.objects.all()
    serializer_class = InstitutionTypeSerializer
    filterset_fields = {
        "name": ["exact", "contains"],
    }


class InstitutionSerializer(FlexFieldsModelSerializer, ModelSerializer):
    class Meta:
        model = Institution
        fields = "__all__"
        expandable_fields = {
            "institution_type": "NEMO_billing.api.InstitutionTypeSerializer",
        }


class InstitutionViewSet(ModelViewSet):
    filename = "institutions"
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    filterset_fields = {
        "name": ["exact", "contains"],
        "institution_type_id": ["exact", "in"],
        "state": ["exact", "contains"],
        "country": ["exact", "contains"],
        "zip_code": ["exact", "contains"],
    }
