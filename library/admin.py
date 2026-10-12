from django.contrib import admin
from .models import Author, Book, Member, CirculationRecord


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "genre", "isbn", "available_copies", "total_copies"]
    list_filter = ["genre"]
    search_fields = ["title", "author__name", "isbn"]


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["name", "member_id", "email", "phone", "joined_date"]
    search_fields = ["name", "member_id", "email"]


@admin.register(CirculationRecord)
class CirculationRecordAdmin(admin.ModelAdmin):
    list_display = ["book", "member", "issue_date", "due_date", "returned", "fine_amount"]
    list_filter = ["returned", "issue_date"]
    search_fields = ["book__title", "member__name", "member__member_id"]
