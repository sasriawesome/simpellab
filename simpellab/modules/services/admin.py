from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from simpellab.admin.admin import ModelAdmin
from simpellab.modules.products.admin import ProductMixin, ProductFeeInline, SpecificationInline
from .models import (
    Service, Parameter, 
    LaboratoriumService, LaboratoriumServiceParameter,
    InspectionService, InspectionServiceParameter,
    CalibrationService,
    SertificationService,
    TrainingService, TrainingTopic,
    ResearchService,
    ConsultancyService,
    MiscService
    )


@admin.register(Parameter)
class TarifAdmin(admin.ModelAdmin):
    raw_id_fields = ['unit_of_measure']


@admin.register(Service)
class ServiceAdmin(PolymorphicParentModelAdmin, ModelAdmin):
    list_display = []
    child_models = [
        LaboratoriumService,
        InspectionService,
        CalibrationService,
        SertificationService,
        TrainingService,
        ResearchService,
        ConsultancyService,
        MiscService
    ]

class LaboratoriumServiceParameterInline(admin.TabularInline):
    extra = 0
    model = LaboratoriumServiceParameter
    raw_id_fields = ['parameter']
    readonly_fields = ['price', 'date_effective']


@admin.register(LaboratoriumService)
class ServiceAdmin(ProductMixin, PolymorphicChildModelAdmin, ModelAdmin):
    list_display = []
    inlines = [ProductFeeInline, LaboratoriumServiceParameterInline]


class InspectionServiceParameterInline(admin.TabularInline):
    extra = 0
    model = InspectionServiceParameter
    raw_id_fields = ['parameter']
    readonly_fields = ['price', 'date_effective']


@admin.register(InspectionService)
class InspectionServiceAdmin(ProductMixin, PolymorphicChildModelAdmin, ModelAdmin):
    list_display = []
    inlines = [ProductFeeInline, InspectionServiceParameterInline]


@admin.register(CalibrationService)
class CalibrationServiceAdmin(ProductMixin, PolymorphicChildModelAdmin, ModelAdmin):
    list_display = []
    inlines = [ProductFeeInline, SpecificationInline]


@admin.register(SertificationService)
class SertificationServiceAdmin(ProductMixin, PolymorphicChildModelAdmin, ModelAdmin):
    list_display = []
    inlines = [ProductFeeInline, SpecificationInline]


class TrainingTopicInline(admin.TabularInline):
    extra = 0
    model = TrainingTopic


@admin.register(TrainingService)
class TrainingServiceAdmin(ProductMixin, PolymorphicChildModelAdmin, ModelAdmin):
    list_display = []
    inlines = [ProductFeeInline, SpecificationInline, TrainingTopicInline]


@admin.register(ConsultancyService)
class ConsultancyServiceAdmin(ProductMixin, PolymorphicChildModelAdmin, ModelAdmin):
    list_display = []
    inlines = [ProductFeeInline, SpecificationInline]


@admin.register(ResearchService)
class ResearchServiceAdmin(ProductMixin, PolymorphicChildModelAdmin, ModelAdmin):
    list_display = []
    inlines = [ProductFeeInline, SpecificationInline]


@admin.register(MiscService)
class MiscServiceAdmin(ProductMixin, PolymorphicChildModelAdmin, ModelAdmin):
    list_display = []
    inlines = [ProductFeeInline, SpecificationInline]