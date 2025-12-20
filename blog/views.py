from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import BlogPost
from mailer import send_mail

class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        # Проверяем, достигнет ли после увеличения 100 просмотров
        if obj.views_count == 99:  # перед увеличением на 1 будет ровно 99
            send_mail(
                subject='Поздравляем! Статья набрала 100 просмотров!',
                message=f'Статья "{obj.title}" достигла 100 просмотров!\n\n'
                        f'Ссылка: https://your-site.com/blogs/{obj.pk}/',
                from_email='no-reply@skystore.com',
                recipient_list=['Couguar72@gmail.com'],
                priority="now",
            )
            messages.info(self.request, "Поздравительное письмо отправлено на email!")

        # Увеличиваем счётчик
        obj.views_count += 1
        obj.save(update_fields=['views_count'])

        return obj

class BlogCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/create.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        messages.success(self.request, "Статья успешно создана!")
        return super().form_valid(form)

class BlogUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/update.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:list')  # будет переопределено ниже

    def get_success_url(self):
        messages.success(self.request, "Статья успешно обновлена!")
        return reverse_lazy('blog:detail', kwargs={'pk': self.object.pk})

class BlogDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/delete.html'
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        messages.success(self.request, "Статья удалена.")
        return super().form_valid(form)