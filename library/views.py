from datetime import timedelta
from decimal import Decimal
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BookSearchForm, IssueBookForm, MemberForm
from .models import Book, CirculationRecord, Member

FINE_PER_DAY = Decimal("5.00")


def catalog(request):
    form = BookSearchForm(request.GET or None)
    books = Book.objects.select_related("author").all()
    query = request.GET.get("q", "").strip()
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__name__icontains=query) |
            Q(genre__icontains=query) |
            Q(isbn__icontains=query)
        )
    return render(request, "library/catalog.html", {"books": books, "form": form, "query": query})


def dashboard(request):
    active_records = CirculationRecord.objects.filter(returned=False).select_related("book", "member")
    overdue_records = [record for record in active_records if record.due_date < timezone.localdate()]
    return render(request, "library/dashboard.html", {
        "book_count": Book.objects.count(),
        "member_count": Member.objects.count(),
        "active_count": active_records.count(),
        "overdue_records": overdue_records,
        "recent_records": CirculationRecord.objects.select_related("book", "member")[:8],
    })


def issue_book(request):
    if request.method == "POST":
        form = IssueBookForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data["book"]
            member = form.cleaned_data["member"]
            with transaction.atomic():
                book = Book.objects.select_for_update().get(pk=book.pk)
                if book.available_copies < 1:
                    messages.error(request, "No copies are currently available.")
                else:
                    today = timezone.localdate()
                    CirculationRecord.objects.create(
                        book=book, member=member, issue_date=today,
                        due_date=today + timedelta(days=14)
                    )
                    book.available_copies -= 1
                    book.save(update_fields=["available_copies"])
                    messages.success(request, f'"{book.title}" issued to {member.name}. Due in 14 days.')
                    return redirect("dashboard")
    else:
        form = IssueBookForm()
    return render(request, "library/issue_book.html", {"form": form})


def return_book(request, record_id):
    record = get_object_or_404(CirculationRecord.objects.select_related("book", "member"), pk=record_id)
    if request.method == "POST":
        if record.returned:
            messages.info(request, "This book has already been returned.")
        else:
            today = timezone.localdate()
            overdue_days = max((today - record.due_date).days, 0)
            fine = FINE_PER_DAY * overdue_days
            with transaction.atomic():
                record.returned = True
                record.return_date = today
                record.fine_amount = fine
                record.save(update_fields=["returned", "return_date", "fine_amount"])
                book = Book.objects.select_for_update().get(pk=record.book_id)
                book.available_copies = min(book.available_copies + 1, book.total_copies)
                book.save(update_fields=["available_copies"])
            messages.success(request, f'Book returned. Overdue fine: ₹{fine:.2f} ({overdue_days} day(s) overdue).')
        return redirect("dashboard")
    return render(request, "library/return_confirm.html", {"record": record})


def members(request):
    member_list = Member.objects.all()
    return render(request, "library/members.html", {"members": member_list})


def add_member(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Member added successfully.")
            return redirect("members")
    else:
        form = MemberForm()
    return render(request, "library/member_form.html", {"form": form})


def member_history(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    records = member.circulation_records.select_related("book").all()
    return render(request, "library/member_history.html", {"member": member, "records": records})
