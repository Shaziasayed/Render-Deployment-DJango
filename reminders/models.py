from django.db import models


from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="customers"
    )
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    statement_pdf = models.FileField(
    upload_to="statements/",
    blank=True,
    null=True
    )

    def __str__(self):
        return self.name



class Reminder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reminders')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateTimeField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    last_sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer.name} - ₹{self.amount}"


class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.CharField(max_length=255, blank=True)

    # ✅ IMAGE PROOF
    proof_image = models.ImageField(
        upload_to="transaction_proofs/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.transaction_type} - ₹{self.amount}"
