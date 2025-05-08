from django.db import models
from django.utils import timezone

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., "Business", "Personal", "Tax"

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., "Income", "Expense"

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)  # Category belongs to a Type

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Subcategory belongs to a Category

    def __str__(self):
        return self.name

class CashFlowRecord(models.Model):
    date = models.DateField(
        default=timezone.now,  # Auto-fills with current date
        verbose_name="Record Date"
    )
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # e.g., 1000.00 RUB
    comment = models.TextField(blank=True, null=True)  # Optional

    def __str__(self):
        return f"{self.date} - {self.amount}"