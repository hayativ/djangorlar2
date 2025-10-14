from django.db.models import (
    Model,
    DateTimeField,
)
from django.utils import timezone
from .admin import SoftDeleteManager


class AbstractSoftDeletableModel(Model):
    """
    Abstract model that provides soft delete behavior via deleted_at.
    By default Model.objects returns only alive records.
    Use Model.all_objects.all() to get all records (including deleted).
    """

    deleted_at = DateTimeField(null=True, blank=True, db_index=True)

    objects = SoftDeleteManager()
    # separate manager that returns all (including deleted)
    all_objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def soft_delete(self):
        """Mark record as deleted."""
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def restore(self):
        """Restore a soft-deleted record."""
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])

    def hard_delete(self):
        """Permanently delete from DB."""
        super().delete()

    # override delete() to soft-delete by default
    def delete(self, using=None, keep_parents=False):
        self.soft_delete()
