from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from view_breadcrumbs import DetailBreadcrumbMixin, ListBreadcrumbMixin

from open_inwoner.accounts.forms import ActionListForm, DocumentForm
from open_inwoner.accounts.views.actions import ActionCreateView, BaseActionFilter
from open_inwoner.utils.mixins import ExportDetailMixin

from .forms import PlanForm, PlanGoalForm
from .models import Plan


class PlanListView(LoginRequiredMixin, ListBreadcrumbMixin, ListView):
    template_name = "pages/plans/list.html"
    model = Plan

    def get_queryset(self):
        return Plan.objects.connected(self.request.user)


class PlanDetailView(
    LoginRequiredMixin, DetailBreadcrumbMixin, BaseActionFilter, DetailView
):
    template_name = "pages/plans/detail.html"
    model = Plan
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    breadcrumb_use_pk = False

    def get_queryset(self):
        return Plan.objects.connected(self.request.user)

    def get_context_data(self, **kwargs):
        actions = self.object.actions.all()
        context = super().get_context_data(**kwargs)
        context["action_form"] = ActionListForm(
            data=self.request.GET, users=actions.values_list("created_by_id", flat=True)
        )
        context["actions"] = self.get_actions(actions)
        return context


class PlanCreateView(LoginRequiredMixin, CreateView):
    template_name = "pages/plans/create.html"
    model = Plan
    form_class = PlanForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(user=self.request.user)
        return kwargs

    def form_valid(self, form):
        self.object = form.save(self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()


class PlanEditView(LoginRequiredMixin, UpdateView):
    template_name = "pages/plans/create.html"
    model = Plan
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    form_class = PlanForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(user=self.request.user)
        return kwargs

    def form_valid(self, form):
        self.object = form.save(self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()


class PlanGoalEditView(LoginRequiredMixin, UpdateView):
    template_name = "pages/plans/goal_edit.html"
    model = Plan
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    form_class = PlanGoalForm
    breadcrumb_use_pk = False

    def get_queryset(self):
        return Plan.objects.connected(self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()


class PlanFileUploadView(LoginRequiredMixin, UpdateView):
    template_name = "pages/plans/file.html"
    model = Plan
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    form_class = DocumentForm

    def get_queryset(self):
        return Plan.objects.connected(self.request.user)

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({"instance": None})
        return kwargs

    def form_valid(self, form):
        form.save(self.request.user, plan=self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()


class PlanActionCreateView(ActionCreateView):
    model = Plan

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plan = self.get_object()
        context["plan"] = plan
        context["object"] = plan
        return context

    def get_object(self):
        try:
            return Plan.objects.connected(self.request.user).get(
                uuid=self.kwargs.get("uuid")
            )
        except ObjectDoesNotExist as e:
            raise Http404

    def form_valid(self, form):
        self.object = self.get_object()
        form.save(self.request.user, plan=self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()


class PlanExportView(LoginRequiredMixin, ExportDetailMixin, DetailView):
    template_name = "export/plans/plan_export.html"
    model = Plan
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_queryset(self):
        return Plan.objects.connected(self.request.user).prefetch_related("actions")
