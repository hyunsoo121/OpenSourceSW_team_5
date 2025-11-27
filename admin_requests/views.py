import logging
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import AdminRequestForm, AdminReviewForm
from .models import AdminRequest

logger = logging.getLogger(__name__)


@login_required
def request_list(request):
    # Admins see all requests, users see their own
    if request.user.is_staff:
        qs = AdminRequest.objects.all()
    else:
        qs = AdminRequest.objects.filter(requester=request.user)
    return render(request, "admin_request/request_list.html", {"requests": qs})


@login_required
def request_detail(request, request_id):
    req = get_object_or_404(AdminRequest, pk=request_id)

    # handle admin review form
    if request.method == "POST" and request.user.is_staff:
        form = AdminReviewForm(request.POST, instance=req)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.save()
            return redirect("admin_request:request_detail", request_id=req.pk)

    review_form = AdminReviewForm(instance=req)
    return render(
        request,
        "admin_request/request_detail.html",
        {"request": req, "review_form": review_form},
    )


@login_required
def request_create(request):
    if request.method == "POST":
        form = AdminRequestForm(request.POST)
        if form.is_valid():
            ar = form.save(commit=False)
            ar.requester = request.user
            ar.save()
            # send notification email to admin
            try:
                from_email = (
                    os.environ.get("DEFAULT_FROM_EMAIL") or settings.DEFAULT_FROM_EMAIL
                )
                subject = f"[관리자 요청] {ar.title}"
                detail_url = request.build_absolute_uri(
                    reverse("admin_request:request_detail", args=[ar.pk])
                )
                message = (
                    f"요청자: {ar.requester}\n"
                    f"요청 유형: {ar.get_request_type_display()}\n\n"
                    f"{ar.content}\n\n"
                    f"요청 상세 보기: {detail_url}\n"
                )
                # determine recipients: ADMIN_NOTIFICATION_EMAIL env var (comma-separated) or DEFAULT_FROM_EMAIL
                recipients = os.environ.get("ADMIN_NOTIFICATION_EMAIL")
                if recipients:
                    recipient_list = [
                        r.strip() for r in recipients.split(",") if r.strip()
                    ]
                else:
                    recipient_list = [from_email]
                send_mail(
                    subject,
                    message,
                    from_email,
                    recipient_list,
                    fail_silently=False,
                )
            except Exception as exc:
                logger.exception(
                    "Failed sending admin request email for AdminRequest %s: %s",
                    ar.pk,
                    exc,
                )

            return redirect("admin_request:request_list")
    else:
        form = AdminRequestForm()
    return render(request, "admin_request/request_create.html", {"form": form})


@login_required
def request_edit(request, request_id):
    req = get_object_or_404(AdminRequest, pk=request_id)
    if req.requester != request.user:
        # only owner can edit
        return redirect("admin_request:request_detail", request_id=req.pk)

    if request.method == "POST":
        form = AdminRequestForm(request.POST, instance=req)
        if form.is_valid():
            form.save()
            return redirect("admin_request:request_detail", request_id=req.pk)
    else:
        form = AdminRequestForm(instance=req)

    return render(
        request, "admin_request/request_edit.html", {"form": form, "object": req}
    )


@login_required
def request_delete(request, request_id):
    req = get_object_or_404(AdminRequest, pk=request_id)
    if req.requester != request.user and not request.user.is_staff:
        return redirect("admin_request:request_detail", request_id=req.pk)

    if request.method == "POST":
        req.delete()
        return redirect("admin_request:request_list")

    return render(request, "admin_request/request_delete.html", {"request_obj": req})
