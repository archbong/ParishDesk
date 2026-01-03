from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Church
from contact.models import Contact


class WelfareCase(models.Model):
    URGENCY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]

    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("APPROVED", "Approved"),
        ("DISBURSED", "Disbursed"),
        ("CLOSED", "Closed"),
    ]

    church = models.ForeignKey(Church, on_delete=models.CASCADE, related_name="welfare_cases")

    beneficiary_user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )
    beneficiary_contact = models.ForeignKey(
        Contact, null=True, blank=True, on_delete=models.SET_NULL
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class WelfareDisbursement(models.Model):
    welfare_case = models.ForeignKey(
        WelfareCase, on_delete=models.CASCADE, related_name="disbursements"
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(blank=True)

    disbursed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    disbursed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.amount} - {self.welfare_case.title}"

class WelfareDocument(models.Model):
    welfare_case = models.ForeignKey(
        WelfareCase, on_delete=models.CASCADE, related_name="documents"
    )
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    document = models.FileField(upload_to="welfare_documents/")
    description = models.TextField(blank=True)

    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Document for {self.welfare_case.title} uploaded by {self.uploaded_by.username if self.uploaded_by else 'Unknown'}"
    
class WelfareNote(models.Model):
    welfare_case = models.ForeignKey(
        WelfareCase, on_delete=models.CASCADE, related_name="notes"
    )
    noted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    note = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Note for {self.welfare_case.title} by {self.noted_by.username if self.noted_by else 'Unknown'}"
    
class WelfareFollowUp(models.Model):
    welfare_case = models.ForeignKey(
        WelfareCase, on_delete=models.CASCADE, related_name="follow_ups"
    )
    followed_up_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    follow_up_date = models.DateField()
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Follow-up for {self.welfare_case.title} by {self.followed_up_by.username if self.followed_up_by else 'Unknown'}"
    
class WelfareApproval(models.Model):
    welfare_case = models.ForeignKey(
        WelfareCase, on_delete=models.CASCADE, related_name="approvals"
    )
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    approval_date = models.DateTimeField(default=timezone.now)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"Approval for {self.welfare_case.title} by {self.approved_by.username if self.approved_by else 'Unknown'}"
    
class WelfareAssessment(models.Model):
    welfare_case = models.ForeignKey(
        WelfareCase, on_delete=models.CASCADE, related_name="assessments"
    )
    assessed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    assessment_date = models.DateTimeField(default=timezone.now)
    findings = models.TextField()
    recommendations = models.TextField()

    def __str__(self):
        return f"Assessment for {self.welfare_case.title} by {self.assessed_by.username if self.assessed_by else 'Unknown'}"

class WelfareExpense(models.Model):
    welfare_case = models.ForeignKey(
        WelfareCase, on_delete=models.CASCADE, related_name="expenses"
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()

    incurred_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    incurred_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Expense of {self.amount} for {self.welfare_case.title}"
    