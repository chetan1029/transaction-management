from django.contrib import admin

from app.account.models import Account, Transaction

admin.site.register(Account)
admin.site.register(Transaction)
