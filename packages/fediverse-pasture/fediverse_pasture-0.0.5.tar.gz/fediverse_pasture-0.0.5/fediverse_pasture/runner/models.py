from tortoise.models import Model
from tortoise import fields


class TestRecord(Model):
    id = fields.IntField(pk=True)
    test_name = fields.CharField(max_length=255)
    application_name = fields.CharField(max_length=255)

    data = fields.JSONField()

    class Meta:
        unique_together = (("test_name", "application_name"),)
