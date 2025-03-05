from django.conf import settings
from service.models import Service, Tariff
User = settings.AUTH_USER_MODEL
from django.db import models
from django.urls import reverse
import os
from ckeditor.fields import RichTextField
from django.core.validators import (FileExtensionValidator)


def blog_cover_upload_to(instance, filename):
    subfolder = instance.slug or 'default'
    return os.path.join('generalsettings', subfolder, filename)


class BlogCategory(models.Model):
    name = models.CharField("Название", max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Категория блога"
        verbose_name_plural = "Категории блогов"

class Blog(models.Model):
    name = models.CharField("Название", max_length=255, null=True, blank=True)
    description = RichTextField("Описание", null=True, blank=True)
    title = models.CharField("Заголовок", max_length=255, null=True, blank=True)
    content = models.TextField("Содержимое", null=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, verbose_name="Категория", null=True, blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True, null=True, blank=True)
    image = models.ImageField("Изображение", upload_to='blogs/', null=True, blank=True)
    preview = models.ImageField("Превью", upload_to='blogs/previews/', null=True, blank=True)
    slug = models.SlugField("Слаг", unique=True,)
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"

class Contact(models.Model):
    address = models.CharField("Адрес", max_length=255)
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Электронная почта")
    latitude = models.FloatField("Широта", blank=True, null=True)
    longitude = models.FloatField("Долгота", blank=True, null=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    departaments = models.TextField("Департаменты")
    social_links = models.ManyToManyField('SocialLink', verbose_name="Социальные ссылки", null=True, blank=True)

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

class SocialLink(models.Model):
    link = models.URLField("Ссылка")
    icon = models.ImageField("Иконка", upload_to='social_links/')

    class Meta:
        verbose_name = "Социальная ссылка"
        verbose_name_plural = "Социальные ссылки"

class Pages(models.Model):
    """"СТРАНИЦЫ"""""

    TYPES = [
        (1, 'Подвал'),
        (2, 'Документация'),
        (3, 'FAQ'),
    ]
    name = models.CharField("Название", max_length=250)
    description = RichTextField("Описание",db_index=True)
    title = models.CharField("Заголовок", max_length=260)
    meta_description = models.TextField("Мета описание")
    thumbnail = models.FileField("Изображение", upload_to="product/%Y/%m/%d/", blank=True, null=True, default='default/blogs/cover.png', validators=[FileExtensionValidator(allowed_extensions=['png', 'webp', 'jpeg', 'jpg', 'svg'])],)
    slug = models.SlugField(max_length=140)
    viewtype = models.PositiveSmallIntegerField("Где показывать СТРАНИЦЫ", default=1, choices=TYPES, blank=False)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pages', kwargs={"slug": self.slug})

class Seo(models.Model):
    PAGE_CHOICE = [
        (1, 'Главная страница'),
        (2, 'Новости'),
        (3, 'Галерея'),
        (4, 'О нас'),
        (5, 'Тарифы'),
        (6, 'Контакты'),
        (7, 'ЧаВо'),
        (8, 'Ресгистрации'),
        (9, 'Авторизация'),
        (10, 'Сбросить пароль'),
        (11, 'Контакты'),
        (12, 'Сотрудничество'),
        (13, 'Контакты'),
    ]
    pagetype = models.PositiveSmallIntegerField('Странца', unique=True, choices=PAGE_CHOICE, blank=False, default=1)
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    title = models.CharField("Заголовок", max_length=255)
    content = models.TextField("Содержимое")
    preview = models.ImageField("Превью", upload_to='seo/previews/')
    propertytitle = models.CharField("Заголовок свойства", max_length=255)
    propertydescription = models.CharField("Описание свойства", max_length=255)
    slug = models.SlugField("Слаг", unique=True)
    setting = models.ForeignKey('SettingGlobal', on_delete=models.CASCADE, verbose_name="Настройка")

    class Meta:
        verbose_name = "SEO"
        verbose_name_plural = "SEO"

class SettingGlobal(models.Model):
    logo = models.ImageField("Логотип", upload_to='settings/')
    doplogo = models.ImageField("Дополнительный логотип", upload_to='settings/')
    doplogolight = models.ImageField("Дополнительный логотип", upload_to='settings/')
    favicon = models.ImageField("Фавикон", upload_to='settings/')
    paymentmethod = models.FileField("Метод оплаты", upload_to='settings/')
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    copyright = models.TextField("Копирайт")
    message_header = models.TextField("Заголовок сообщения")
    message_footer = models.TextField("Подвал сообщения")
    yandex_metrica = models.TextField("Яндекс Метрика")
    google_analytics = models.TextField("Google Аналитика")

    class Meta:
        verbose_name = "Глобальная настройка"
        verbose_name_plural = "Глобальные настройки"

class SMTPPage(models.Model):
    """Настройки сайта"""
    email_host = models.TextField("Email Site HOST")
    default_from_email = models.TextField("Email Site HOST")
    email_port = models.TextField("Email Site PORT")
    email_host_user = models.TextField("Email Site User")
    email_host_password = models.TextField("Email Site Password")
    email_use_tls = models.BooleanField("Use TLS", default=False)
    email_use_ssl = models.BooleanField("Use SSL", default=False)
    setting = models.ForeignKey(SettingGlobal, verbose_name='Настройки', on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Сначала сохраняем модель
        super().save(*args, **kwargs)

        # Путь к файлу, куда будем сохранять данные
        file_path = os.path.join(settings.BASE_DIR, '_media/smtp.py')

        # Сохраняем данные в текстовый файл
        with open(file_path, 'w') as f:
            f.write(f"EMAIL_HOST = '{self.email_host}'\n")
            f.write(f"EMAIL_PORT = '{self.email_port}'\n")
            f.write(f"EMAIL_USE_TLS = {self.email_use_tls}\n")
            f.write(f"EMAIL_USE_SSL = {self.email_use_ssl}\n")
            f.write(f"EMAIL_HOST_USER = '{self.email_host_user}'\n")
            f.write(f"EMAIL_HOST_PASSWORD = '{self.email_host_password}'\n")
            f.write(f"DEFAULT_FROM_EMAIL = '{self.default_from_email}'\n")

    class Meta:
        verbose_name = "Настройка SMTP"
        verbose_name_plural = "Настройки SMTP"

class Gallery(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    items = models.ManyToManyField('GalleryItem', verbose_name="Элементы галереи", related_name='galleries')

    class Meta:
        verbose_name = "Галерея"
        verbose_name_plural = "Галереи"

class GalleryItem(models.Model):
    item_type = models.CharField("Тип элемента", max_length=255)
    photo = models.ImageField("Фото", upload_to='gallery_photos/')
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Элемент галереи"
        verbose_name_plural = "Элементы галереи"



class Review(models.Model):
    name = models.CharField("Название", max_length=255)
    avatar = models.ImageField("Аватарка",upload_to='reviews/')
    description = models.TextField("Описание")
    stars = models.IntegerField("Оценка")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

class Faq(models.Model):
    question = models.TextField("Вопрос")
    answer = models.TextField("Ответ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Часто задаваемый вопрос"
        verbose_name_plural = "Часто задаваемые вопросы"


class HomePage(models.Model):
    first_banner = models.ImageField("Первый баннер", upload_to='home/', null=True, blank=True)
    first_banner_title = models.TextField("Первый баннер Заголовок", null=True, blank=True)
    first_banner_title_1 = models.TextField("Первый баннер Заголовок 1", null=True, blank=True)
    first_banner_description = models.TextField("Первый баннер описание", null=True, blank=True)
    first_banner_sociallinks = models.ManyToManyField(SocialLink, related_name='first_banner_sociallinks', blank=True)
    first_banner_1btn_name = models.CharField("Первый баннер 1 кнопка название", max_length=255, null=True, blank=True)
    first_banner_1btn_link = models.URLField("Первый баннер 1 ссылка кнопки", null=True, blank=True)
    first_banner_2btn_name = models.CharField("Первый баннер 2 кнопка название", max_length=255, null=True, blank=True)
    first_banner_2btn_link = models.URLField("Первый баннер 2 ссылка кнопки", null=True, blank=True)
    home_slides_name = models.CharField("", max_length=255, null=True, blank=True)
    choose_us_main_title = models.TextField("Выбирайте нас заголовок", null=True, blank=True)
    choose_us_main_description = models.TextField("Выбирайте нас описание", null=True, blank=True)
    choose_us_main_image = models.ImageField("Выбирайте нас изображение", upload_to='home/', null=True, blank=True)
    choose_us_services = models.ManyToManyField(Service, verbose_name="Выбирайте нас Сервисы", blank=True)
    gallery_main_title = models.TextField("Галерея гл заголовок", null=True, blank=True)
    gallery_main_description = models.TextField("Галерея гл описание", null=True, blank=True)
    gallery_main_image = models.ImageField("Галерея гл изображения", upload_to='home/', null=True, blank=True)
    gallery = models.ManyToManyField(Gallery,  verbose_name="Галерея", null=True, blank=True)
    tariff_main_title = models.TextField("Тариф гл заголовок", null=True, blank=True)
    tariff_main_description = models.TextField("Тариф гл описание", null=True, blank=True)
    tariff_main_image = models.ImageField("Тариф гл изображения", upload_to='home/', null=True, blank=True)
    tariff = models.ManyToManyField(Tariff,  verbose_name="Тариф", null=True, blank=True)
    reviews_main_title = models.TextField("Отзывы гл заголовок", null=True, blank=True)
    reviews_main_description = models.TextField("Отзывы гл описание", null=True, blank=True)
    reviews_main_image = models.ImageField("Отзывы гл изображение", upload_to='home/', null=True, blank=True)
    reviews = models.ManyToManyField(Review, verbose_name="Отзывы", null=True, blank=True)
    second_banner = models.ImageField("Второй баннер главная", upload_to='home/', null=True, blank=True)
    second_banner_first_stat_count = models.TextField("Второй баннер статистика количество 1", null=True, blank=True)
    second_banner_first_stat_title = models.TextField("Второй баннер статистика заголовок 1", null=True, blank=True)
    second_banner_first_stat_descr = models.TextField("Второй баннер статистика описание 1", null=True, blank=True)
    second_banner_first_stat_image = models.FileField("Второй баннер статистика изображение 1", upload_to='home/', null=True, blank=True)
    second_banner_sec_stat_count = models.TextField("Второй баннер статистика количество 2", null=True, blank=True)
    second_banner_sec_stat_title = models.TextField("Второй баннер статистика заголовок 2", null=True, blank=True)
    second_banner_sec_stat_descr = models.TextField("Второй баннер статистика описание 2", null=True, blank=True)
    second_banner_sec_stat_image = models.FileField("Второй баннер статистика изображение 2", upload_to='home/', null=True, blank=True)
    second_banner_thi_stat_count = models.TextField("Второй баннер статистика количество 3", null=True, blank=True)
    second_banner_thi_stat_title = models.TextField("Второй баннер статистика заголовок 3", null=True, blank=True)
    second_banner_thi_stat_descr = models.TextField("Второй баннер статистика описание 3", null=True, blank=True)
    second_banner_thi_stat_image = models.FileField("Второй баннер статистика изображение 3", upload_to='home/', null=True, blank=True)
    faqs_main_title = models.TextField("FAQ гл заголовок", null=True, blank=True)
    faqs_main_description = models.TextField("FAQ гл описание", null=True, blank=True)
    faqs_main_image = models.ImageField("FAQ гл изображение", upload_to='home/', null=True, blank=True)
    faqs = models.ManyToManyField(Faq, blank=True)
    blogs_main_title = models.TextField("Статьи гл заголовок", null=True, blank=True)
    blogs_main_description = models.TextField("Статьи гл описание", null=True, blank=True)
    blogs_main_image = models.ImageField("Статьи гл изображение", upload_to='home/', null=True, blank=True)
    blogs = models.ManyToManyField(Blog, null=True, blank=True)
    def __str__(self):
        return f"HomePage {self.pk}"

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главные страницы"


class About(models.Model):
    image = models.ImageField("Выбирайте нас гл изображение",upload_to='about/')
    services = models.ManyToManyField(Service)
    description = RichTextField("Описание")
    title = models.CharField("Заголовок", max_length=255)
    content = models.TextField("Содержимое")
    preview = models.ImageField("Превью", upload_to='seo/previews/')
    propertytitle = models.CharField("Заголовок свойства", max_length=255)
    propertydescription = models.CharField("Описание свойства", max_length=255)

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"

