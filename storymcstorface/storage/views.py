from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from storage.models import Facility
from storage.forms import StorageLogForm


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request,
        template_name="storage/login.html",
        context={"login_form": form},
    )


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your password was successfully updated!")
            return redirect("/")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "storage/password.html", {"form": form})


def logout_request(request):
    logout(request)
    return redirect("/")


def facility_list(request):
    facilities = Facility.objects.all().order_by("name")
    return render(request, "storage/facility_list.html", {"facilities": facilities})


def facility_detail(request, slug):
    facility = get_object_or_404(Facility, slug=slug)
    locations = facility.location_set.order_by("row", "column")
    return render(
        request,
        "storage/facility_detail.html",
        {"locations": locations, "facility": facility},
    )


def facility_modify(request, slug):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    if request.method == "POST":
        form = StorageLogForm(request.POST, facility=slug)
        if form.is_valid():
            form.clean()
            item = form.cleaned_data["item"]
            qty = form.cleaned_data["quantity"]
            comment = form.cleaned_data["comment"]

            if request.POST["action"] == "add":
                item.add(qty, user=request.user, comment=comment)
                log_text = "added"
            if request.POST["action"] == "remove":
                item.remove(qty, user=request.user, comment=comment)
                log_text = "removed"

            messages.success(
                request, f"Successfully {log_text} {qty}x {item.product.name}"
            )
        else:
            messages.error(request, form.errors.as_text())
    else:
        form = StorageLogForm(facility=slug)

    return render(
        request,
        "storage/facility_modify.html",
        {"form": form, "facility": Facility.objects.get(slug=slug)},
    )
