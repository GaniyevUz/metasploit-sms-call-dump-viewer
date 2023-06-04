from json import dumps, loads
from time import time

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView

from sms.forms import FileForm


class IndexPageView(FormView):
    template_name = 'index.html'
    form_class = FileForm

    def form_valid(self, form):
        file = form.cleaned_data.get('file')
        if not file:
            return self.form_invalid(form)
        file_contents = file.read().decode('utf-8')
        lines = file_contents.strip().split('\n')
        sms_data = {}
        device = {}
        message = {}
        for line in lines:
            if line.startswith('=') or line.strip() == '' or line.startswith('[+') or line.startswith('#'):
                continue
            else:
                key, value = line.split(':', 1)
                message[key.strip()] = value.strip()
                if key.strip() == 'Remote Port':
                    device = message
                    message = {}
                elif key.strip() == 'Message':
                    person = message['Address']
                    if not sms_data.get(person):
                        sms_data[person] = []
                    sms_data[person].append(message)
                    message = {}
            sms_data = {key: list(reversed(value)) for key, value in sms_data.items()}
        with open(f'media/sms.json', 'w') as f:
            f.write(dumps({'device': device, 'sms_data': sms_data}, indent=4))
        response = render(self.request, 'chat.html', {'people': sms_data.keys(), 'messages': ''})
        return response

    def form_invalid(self, form):
        text_errors = [error for field_errors in form.errors.values() for error in field_errors]
        return render(self.request, 'index.html', {'errors': text_errors})


class SMSView(View):
    def get(self, request, key, *args, **kwargs):
        with open(f'media/sms.json', 'r') as f:
            data = f.read()
            if not data:
                return redirect('sms-view')
            sms_data = loads(data)

        if sms_data['sms_data'].get(key):
            messages = sms_data['sms_data'][key]
            del sms_data['sms_data'][key]
        return render(request, 'chat.html', {'people': sms_data['sms_data'].keys(), 'messages': messages, 'current': key})
