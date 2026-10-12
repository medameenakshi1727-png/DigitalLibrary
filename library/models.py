from datetime import timedelta
from django.db import models
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    isbn = models.CharField(max_length=20, unique=True)
    genre = models.CharField(max_length=100)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    cover_url = models.URLField(blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Member(models.Model):
    name = models.CharField(max_length=100)
    member_id = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    joined_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.member_id})"


class CirculationRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="circulation_records")
    member = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="circulation_records")
    issue_date = models.DateField(default=timezone.localdate)
    due_date = models.DateField(blank=True)
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    returned = models.BooleanField(default=False)

    class Meta:
        ordering = ["-issue_date", "-id"]

    def save(self, *args, **kwargs):
        if not self.due_date and self.issue_date:
            self.due_date = self.issue_date + timedelta(days=14)
        super().save(*args, **kwargs)

    @property
    def overdue_days(self):
        end_date = self.return_date or timezone.localdate()
        return max((end_date - self.due_date).days, 0) if self.due_date else 0

    def __str__(self):
        return f"{self.book.title} → {self.member.name}"
