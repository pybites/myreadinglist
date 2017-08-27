from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    bookid = models.CharField(max_length=20)  # google bookid
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    publisher = models.CharField(max_length=100)
    published = models.CharField(max_length=20)
    isbn = models.CharField(max_length=15)
    pages = models.CharField(max_length=5)
    language = models.CharField(max_length=2)
    description = models.TextField()
    inserted = models.DateTimeField('inserted', auto_now_add=True)
    edited = models.DateTimeField('last modified', auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.bookid, self.title)


class Search(models.Model):
    book = models.ForeignKey(Book, related_name='book_search_set')
    user = models.ForeignKey(User, related_name='user_search_set')
    inserted = models.DateTimeField('inserted', auto_now_add=True)
    edited = models.DateTimeField('last modified', auto_now=True)

    class Meta:
        verbose_name_plural = 'searches'


class Like(models.Model):
    book = models.ForeignKey(Book, related_name='book_like_set')
    user = models.ForeignKey(User, related_name='user_like_set')
    comment = models.TextField(null=True)
    deleted = models.BooleanField(default=False)
    inserted = models.DateTimeField('inserted', auto_now_add=True)
    edited = models.DateTimeField('last modified', auto_now=True)


class Status(models.Model):
    ACTIONS = (
        ('HR', 'Have Read'),
        ('AR', 'Am Reading'),
        ('WR', 'Want to Read'),
    )
    DEFAULT_ACTION = 'AR'

    book = models.ForeignKey(Book, related_name='book_status_set')
    user = models.ForeignKey(User, related_name='user_status_set')
    action = models.CharField(
        max_length=2,
        choices=ACTIONS,
        default=DEFAULT_ACTION,
    )

    inserted = models.DateTimeField('inserted', auto_now_add=True)
    edited = models.DateTimeField('last modified', auto_now=True)

    class Meta:
        verbose_name_plural = 'statuses'
