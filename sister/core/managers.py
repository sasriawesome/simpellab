from django.db import models
from django.db.models.functions import Coalesce
from django.utils import translation
from polymorphic.managers import PolymorphicManager

_ = translation.gettext_lazy


# Example
# def count_subquery(model, extra_filter=None):
#     filter = {'rmu_id': models.OuterRef('pk')}
#     if extra_filter:
#         filter.update(extra_filter)
#     sqs = Coalesce(
#         models.Subquery(
#             model.objects.filter(**filter).order_by().values('rmu_id').annotate(
#                 total=models.Count('*')
#             ).values('total'),
#             output_field=models.IntegerField()
#         ), 0)
#     return sqs

# Example
# def cumulative_count_subquery(model, extra_filter=None):
#     filter = {
#         'rmu__tree_id': models.OuterRef('tree_id'),
#         'rmu__lft__gte': models.OuterRef('lft'),
#         'rmu__lft__lte': models.OuterRef('rght')
#     }
#     if extra_filter:
#         filter.update(extra_filter)
#     sqs = Coalesce(
#         models.Subquery(
#             model.objects.filter(
#                 **filter
#             ).order_by().values('rmu__tree_id').annotate(
#                 total=models.Count('*')
#             ).values('total'),
#             output_field=models.IntegerField()
#         ), 0)
#     return sqs


class ParanoidManagerMixin:

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

    def get(self, *args, **kwargs):
        kwargs['deleted'] = False
        return super().get(*args, **kwargs)

    def get_deleted(self):
        return super().get_queryset().filter(deleted=True)


class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class BasePolymorphicManager(PolymorphicManager):
    pass


class ParanoidPolymorphicManager(ParanoidManagerMixin, PolymorphicManager):
    """ Implement paranoid mechanism queryset """

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

    def get(self, *args, **kwargs):
        kwargs['deleted'] = False
        return super().get(*args, **kwargs)

    def get_deleted(self):
        return super().get_queryset().filter(deleted=True)


class ParanoidManager(ParanoidManagerMixin, BaseManager):
    pass