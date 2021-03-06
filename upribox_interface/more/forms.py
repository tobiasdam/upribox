# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy
from lib import utils, passwd
from django.contrib.auth import authenticate


class AdminForm(forms.Form):

    username = forms.CharField(
        required=True,
        label=ugettext_lazy("Benutzername"),
        max_length=20,
    )
    oldpassword = forms.CharField(
        required=True,
        label=ugettext_lazy("Altes Passwort"),
        widget=forms.PasswordInput(attrs={'placeholder': '*' * 10})
    )
    password1 = forms.CharField(
        required=True,
        label=ugettext_lazy("Neues Passwort"),
        widget=forms.PasswordInput(attrs={'placeholder': '*' * 10})
    )
    password2 = forms.CharField(
        required=True,
        label=ugettext_lazy("Neues Passwort erneut eingeben"),
        widget=forms.PasswordInput(attrs={'placeholder': '*' * 10})
    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(AdminForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['value'] = request.user.username

    def clean_oldpassword(self):
        oldpassword = self.cleaned_data.get('oldpassword')
        username = self.request.user.username

        if not authenticate(username=username, password=oldpassword):
            raise forms.ValidationError(ugettext_lazy("Das alte Passwort ist inkorrekt"))

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        return utils.check_passwords(password1, password2)