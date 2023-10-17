from django.core.exceptions import ValidationError
from django.db import models

from allianceauth.eveonline.models import (
    EveAllianceInfo, EveCharacter, EveCorporationInfo,
)


class AlumniSetup(models.Model):
    alumni_corporations = models.ManyToManyField(
        EveCorporationInfo,
        blank=True,
        help_text="Characters with these Corps in their History will be given Alumni Status")
    alumni_alliances = models.ManyToManyField(
        EveAllianceInfo,
        blank=True,
        help_text="Characters with these Alliances in their History will be given Alumni Status")

    def save(self, *args, **kwargs):
        if not self.pk and AlumniSetup.objects.exists():
            # Force a single object
            raise ValidationError('There is can be only one \
                                AlumniCorp instance')
        self.pk = self.id = 1  # If this happens to be deleted and recreated, force it to be 1
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Alumni Config"


class CorporationAllianceHistory(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['corporation_id', 'record_id'], name="CorporationAllianceRecord"),
        ]
    corporation_id = models.PositiveIntegerField(db_index=True)
    alliance_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    is_deleted = models.BooleanField(
        default=False,
        help_text='True if the corporation has been deleted')
    record_id = models.IntegerField(
        help_text='An incrementing ID that can be used to canonically establish order of records in cases where dates may be ambiguous')
    start_date = models.DateTimeField()


class CharacterCorporationHistory(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['character', 'record_id'], name="CharacterCorporationRecord"),
        ]
    character = models.ForeignKey(
        EveCharacter,
        on_delete=models.CASCADE)
    corporation_id = models.PositiveIntegerField()
    is_deleted = models.BooleanField(
        default=False,
        help_text='True if the corporation has been deleted')
    record_id = models.IntegerField(
        help_text='An incrementing ID that can be used to canonically establish order of records in cases where dates may be ambiguous')
    start_date = models.DateTimeField()
