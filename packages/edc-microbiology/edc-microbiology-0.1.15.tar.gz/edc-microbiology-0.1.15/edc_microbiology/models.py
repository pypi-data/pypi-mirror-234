from django.db import models
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow

from .model_mixins import (
    BloodCultureModelMixin,
    HistopathologyModelMixin,
    SputumAfbModelMixin,
    SputumCultureModelMixin,
    SputumGenexpertModelMixin,
    UrinaryLamModelMixin,
    UrineCultureModelMixin,
)


class MicrobiologyModelMixin(
    BloodCultureModelMixin,
    HistopathologyModelMixin,
    SputumAfbModelMixin,
    SputumCultureModelMixin,
    SputumGenexpertModelMixin,
    UrinaryLamModelMixin,
    UrineCultureModelMixin,
    models.Model,
):
    class Meta:
        abstract = True


class Microbiology(
    UniqueSubjectIdentifierFieldMixin,
    MicrobiologyModelMixin,
    SiteModelMixin,
    BaseUuidModel,
):
    report_datetime = models.DateTimeField(default=get_utcnow)

    objects = models.Manager()
    on_site = CurrentSiteManager()
    history = HistoricalRecords()

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Microbiology"
        verbose_name_plural = "Microbiology"
