# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

'''
This file contains forms used in the application
'''

from django.forms import Form
from django.forms import ModelForm
from django.forms import DateField
from django.forms import CharField
from django.forms import DecimalField
from django.forms import widgets
from django.forms import ModelChoiceField
from django.utils.translation import ugettext as _

from captcha.fields import ReCaptchaField

from wger.exercises.models import Exercise
from wger.manager.models import WorkoutSession
from wger.manager.models import Workout
from wger.manager.models import Day
from wger.manager.models import Set
from wger.manager.models import WorkoutLog
from wger.utils.widgets import TranslatedSelectMultiple
from wger.utils.widgets import ExerciseAjaxSelect
from wger.utils.constants import DATE_FORMATS
from wger.utils.widgets import Html5DateInput
from wger.utils.widgets import Html5NumberInput


class DemoUserForm(Form):
    captcha = ReCaptchaField(attrs={'theme': 'clean'},
                             label=_('Confirmation text'),
                             help_text=_('As a security measure, please enter the previous words'),)


class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        exclude = ('user',)


class WorkoutCopyForm(Form):
    comment = CharField(max_length=100,
                        help_text=_('The goal or description of the new workout.'),
                        required=False)


class DayForm(ModelForm):
    class Meta:
        model = Day

        widgets = {'day': TranslatedSelectMultiple()}


class SetForm(ModelForm):
    class Meta:
        model = Set
        widgets = {'exercises': ExerciseAjaxSelect(), }

    # We need to overwrite the init method here because otherwise Django
    # will outut a default help text, regardless of the widget used
    # https://code.djangoproject.com/ticket/9321
    def __init__(self, *args, **kwargs):
        super(SetForm, self).__init__(*args, **kwargs)
        self.fields['exercises'].help_text = _('You can search for more than one exercise, '
                                               'they will be grouped together for a superset.')


class SetFormMobile(ModelForm):
    '''
    Don't use the autocompleter when accessing the mobile version
    '''
    exercise_list = ModelChoiceField(Exercise.objects)

    class Meta:
        model = Set

    # We need to overwrite the init method here because otherwise Django
    # will outut a default help text, regardless of the widget used
    # https://code.djangoproject.com/ticket/9321
    def __init__(self, *args, **kwargs):
        super(SetFormMobile, self).__init__(*args, **kwargs)
        self.fields['exercise_list'].help_text = _('You can search for more than one exercise, '
                                                   'they will be grouped together for a superset.')


class HelperDateForm(Form):
    '''
    A helper form used in the workout log view
    '''
    date = DateField(input_formats=DATE_FORMATS, widget=Html5DateInput())


class WorkoutLogForm(ModelForm):
    '''
    Helper form for a WorkoutLog.

    The field for the weight is overwritten here, activating localization (so a
    German user can  use ',' as the separator)
    '''
    weight = DecimalField(decimal_places=2,
                          max_digits=5,
                          localize=True,
                          widget=Html5NumberInput())

    class Meta:
        model = WorkoutLog
        exclude = ('exercise', )


class HelperWorkoutSessionForm(ModelForm):
    '''
    A helper form used in the workout log view
    '''
    class Meta:
        model = WorkoutSession
        exclude = ('date', 'user')


class WorkoutSessionForm(ModelForm):
    '''
    Workout Session form
    '''
    class Meta:
        model = WorkoutSession
        exclude = ('user', )


class WorkoutSessionHiddenFieldsForm(ModelForm):
    '''
    Workout Session form used in the timer view
    '''
    class Meta:
        model = WorkoutSession
        widgets = {'time_start': widgets.HiddenInput(),
                   'time_end': widgets.HiddenInput(),
                   'user': widgets.HiddenInput()}
