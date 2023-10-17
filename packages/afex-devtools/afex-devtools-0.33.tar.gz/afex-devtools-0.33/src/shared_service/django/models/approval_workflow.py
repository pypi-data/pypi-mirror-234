from django.db import models

class ApprovalWorkflowModel(models.Model):
    approval_workflow = models.JSONField(null=True, blank=True)