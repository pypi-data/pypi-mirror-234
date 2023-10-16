__all__ = [
    "ExceptionModel",
]

from django.db import models


class ExceptionModel(models.Model):
    module = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    lineno = models.IntegerField()
    exc_class = models.CharField(max_length=255, verbose_name="Class")
    exc_message = models.CharField(max_length=255, verbose_name="Message")
    exc_traceback = models.TextField(verbose_name="Traceback")
    timestamp = models.FloatField()

    class Meta:
        db_table = "django_exception"
        ordering = ("-timestamp",)
        unique_together = [
            (
                "filename",
                "lineno",
            )
        ]
        verbose_name = "Exception"
        verbose_name_plural = "Exceptions"
