from django.db import models
# Create your models here.


class SampleData(models.Model):
    url = models.CharField(max_length=100)
    node_id = models.CharField(max_length=50, default="x1")
    data = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['url', 'node_id'], name='unique_url_node_id')
        ]
