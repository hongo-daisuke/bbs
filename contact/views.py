from django.shortcuts import render
from django.views.generic import FormView, CreateView
from .forms import ContactForm
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

class ContactHomeView(FormView):
    template_name = 'contact/contact_home.html'
    form_class = ContactForm
    def form_valid(self, form):
        return render(self.request, 'contact/contact_home.html', {'form': form})


class ContactConfirmView(FormView):
    form_class = ContactForm

    def form_valid(self, form):
        return render(self.request, 'contact/contact_confirm.html', {'form': form})

    def form_invalid(self, form):
        return render(self.request, 'contact/contact_home.html', {'form': form})
    
class ContactCompleteView(CreateView):
    template_name = 'contact/contact_complete.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:complete')
    def form_valid(self, form):
        subject = 'お問合せ完了しました'
        html_message = render_to_string('mail/contact_complete.html')
        text_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['test@test']
        send_mail(subject, text_message, from_email, recipient_list, html_message=html_message)
        return super().form_valid(form)