from django.db import models
from psqlextra.models import PostgresPartitionedModel
from psqlextra.types import PostgresPartitioningMethod


class DifferentialAnalysis(PostgresPartitionedModel):
    """
    A Model to store differential analysis tables as textfield
    """
    name = models.TextField(max_length=100)
    description = models.TextField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    index_col = models.TextField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class PartitioningMeta:
        method = PostgresPartitioningMethod.RANGE
        key = ["id"]
        ordering = ["id"]
        app_label = "clavicle"
        using = "clavicle"


class RawData(PostgresPartitionedModel):
    """
    A Model to store raw data tables as textfield
    """
    name = models.TextField(max_length=100)
    description = models.TextField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    index_col = models.TextField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class PartitioningMeta:
        method = PostgresPartitioningMethod.RANGE
        key = ["id"]
        ordering = ["id"]
        app_label = "clavicle"
        using = "clavicle"

