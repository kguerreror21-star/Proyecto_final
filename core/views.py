from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
from django.views.generic.base import View

from .forms import BookingForm, CommentForm, RegisterForm, TourForm
from .models import Booking, Category, Comment, Tour


class CustomLoginView(LoginView):
    authentication_form = AuthenticationForm
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy("home")

    def form_valid(self, form):
        user = authenticate(
            self.request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user is None:
            return self.form_invalid(form)
        login(self.request, user)
        messages.success(self.request, "Inicio de sesion correcto.")
        return redirect(self.get_success_url())


class CustomLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "Sesion cerrada correctamente.")
        return redirect("home")


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        profile = getattr(user, "profile", None)
        return user.is_staff or bool(profile and profile.can_manage_tours)


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_tours"] = Tour.objects.filter(is_active=True, is_featured=True)[:3]
        context["categories"] = Category.objects.all()[:4]
        return context


class StaticPageView(TemplateView):
    pass


class TourListView(ListView):
    model = Tour
    template_name = "core/tour_list.html"
    context_object_name = "tours"
    paginate_by = 9

    def get_queryset(self):
        queryset = Tour.objects.select_related("category").filter(is_active=True)
        query = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("category", "").strip()
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(country__icontains=query) | Q(place__icontains=query))
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["selected_category"] = self.request.GET.get("category", "")
        context["query"] = self.request.GET.get("q", "")
        return context


class TourDetailView(DetailView):
    model = Tour
    template_name = "core/tour_detail.html"
    context_object_name = "tour"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["booking_form"] = BookingForm(tour=self.object)
        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.filter(is_visible=True).select_related("user")
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesion para comentar.")
            return redirect("login")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.tour = self.object
            comment.save()
            messages.success(request, "Comentario publicado.")
            return redirect(self.object)
        return self.render_to_response(self.get_context_data(comment_form=form))


class TourCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Tour
    form_class = TourForm
    template_name = "core/tour_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Tour creado correctamente.")
        return super().form_valid(form)


class TourUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Tour
    form_class = TourForm
    template_name = "core/tour_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Tour actualizado correctamente.")
        return super().form_valid(form)


class TourDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Tour
    template_name = "core/tour_confirm_delete.html"
    success_url = reverse_lazy("tour_list")

    def form_valid(self, form):
        messages.success(self.request, "Tour eliminado correctamente.")
        return super().form_valid(form)


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "core/booking_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.tour = get_object_or_404(Tour, pk=kwargs["pk"], is_active=True)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["tour"] = self.tour
        return kwargs

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.user = self.request.user
        booking.tour = self.tour
        booking.save()
        messages.success(self.request, "Reserva registrada. Te contactaremos para confirmarla.")
        return redirect("my_bookings")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tour"] = self.tour
        return context


class MyBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "core/my_bookings.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related("tour", "tour__category")


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Cuenta creada correctamente.")
        return response
