from django import forms
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext_lazy as _

from mayan.apps.backends.forms import FormDynamicModelBackend
from mayan.apps.converter.fields import ImageField
from mayan.apps.templating.fields import ModelTemplateField
from mayan.apps.views.forms import FilteredSelectionForm

from .classes import WorkflowAction
from .models import (
    Workflow, WorkflowStateEscalation, WorkflowInstance, WorkflowState,
    WorkflowStateAction, WorkflowTransition
)


class WorkflowActionSelectionForm(forms.Form):
    klass = forms.ChoiceField(
        choices=(), help_text=_('The action type for this action entry.'),
        label=_('Action'), widget=forms.Select(
            attrs={'class': 'select2'}
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['klass'].choices = WorkflowAction.get_choices()


class WorkflowForm(forms.ModelForm):
    class Meta:
        fields = ('label', 'internal_name', 'auto_launch')
        model = Workflow


class WorkflowMultipleSelectionForm(FilteredSelectionForm):
    class Meta:
        allow_multiple = True
        field_name = 'workflows'
        label = _('Workflows')
        required = False
        widget_attributes = {'class': 'select2'}


class WorkflowStateActionDynamicForm(FormDynamicModelBackend):
    class Meta:
        fields = ('label', 'when', 'enabled', 'condition', 'backend_data')
        model = WorkflowStateAction
        widgets = {'backend_data': forms.widgets.HiddenInput}

    def __init__(self, request, user=None, *args, **kwargs):
        self.request = request
        self.user = user
        result = super().__init__(*args, **kwargs)

        self.fields['condition'] = ModelTemplateField(
            initial_help_text=self.fields['condition'].help_text,
            label=self.fields['condition'].label, model=WorkflowInstance,
            model_variable='workflow_instance', required=False
        )

        return result


class WorkflowStateEscalationForm(forms.ModelForm):
    def __init__(self, workflow_template_state, *args, **kwargs):
        self.workflow_template_state = workflow_template_state
        super().__init__(*args, **kwargs)

        self.fields[
            'transition'
        ].queryset = self.workflow_template_state.workflow.transitions.filter(
            origin_state=self.workflow_template_state
        )

        self.fields['condition'] = ModelTemplateField(
            initial_help_text=self.fields['condition'].help_text,
            label=self.fields['condition'].label, model=WorkflowInstance,
            model_variable='workflow_instance', required=False
        )

    class Meta:
        fields = (
            'enabled', 'transition', 'priority', 'unit', 'amount',
            'condition'
        )
        model = WorkflowStateEscalation


class WorkflowStateForm(forms.ModelForm):
    class Meta:
        fields = ('initial', 'label', 'completion')
        model = WorkflowState


class WorkflowTransitionForm(forms.ModelForm):
    def __init__(self, workflow, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[
            'origin_state'
        ].queryset = self.fields[
            'origin_state'
        ].queryset.filter(workflow=workflow)

        self.fields[
            'destination_state'
        ].queryset = self.fields[
            'destination_state'
        ].queryset.filter(workflow=workflow)

        self.fields['condition'] = ModelTemplateField(
            initial_help_text=self.fields['condition'].help_text,
            label=self.fields['condition'].label, model=WorkflowInstance,
            model_variable='workflow_instance', required=False
        )

    class Meta:
        fields = ('label', 'origin_state', 'destination_state', 'condition')
        model = WorkflowTransition


class WorkflowTransitionTriggerEventRelationshipForm(forms.Form):
    namespace = forms.CharField(
        label=_('Namespace'), required=False,
        widget=forms.TextInput(
            attrs={'readonly': 'readonly'}
        )
    )
    label = forms.CharField(
        label=_('Label'), required=False,
        widget=forms.TextInput(
            attrs={'readonly': 'readonly'}
        )
    )
    relationship = forms.ChoiceField(
        choices=(
            ('no', _('No')),
            ('yes', _('Yes')),
        ), label=_('Enabled'), widget=forms.RadioSelect()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['namespace'].initial = self.initial['event_type'].namespace
        self.fields['label'].initial = self.initial['event_type'].label

        relationship = self.initial['transition'].trigger_events.filter(
            event_type=self.initial['event_type']
        )

        if relationship.exists():
            self.fields['relationship'].initial = 'yes'
        else:
            self.fields['relationship'].initial = 'no'

    def save(self):
        relationship = self.initial['transition'].trigger_events.filter(
            event_type=self.initial['event_type']
        )

        if self.cleaned_data['relationship'] == 'no':
            relationship.delete()
        elif self.cleaned_data['relationship'] == 'yes':
            if not relationship.exists():
                self.initial['transition'].trigger_events.create(
                    event_type=self.initial['event_type']
                )


WorkflowTransitionTriggerEventRelationshipFormSet = formset_factory(
    form=WorkflowTransitionTriggerEventRelationshipForm, extra=0
)


class WorkflowInstanceTransitionSelectForm(forms.Form):
    def __init__(self, user, workflow_instance, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[
            'transition'
        ].queryset = workflow_instance.get_transition_choices(user=user)

    transition = forms.ModelChoiceField(
        help_text=_('Select a transition to execute in the next step.'),
        label=_('Transition'), queryset=WorkflowTransition.objects.none()
    )


class WorkflowPreviewForm(forms.Form):
    workflow = ImageField(
        image_alt_text=_('Workflow template preview image')
    )

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['workflow'].initial = instance
