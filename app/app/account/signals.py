# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from app.account.models import Transaction
#
#
# @receiver(post_save, sender=Transaction)
# def update_account_balance_on_new_transaction(sender, instance, created, **kwargs):
#     """
#         Signal handler to update account balance when a new Transaction is saved.
#     """
#     if created:
#         account = instance.account
#
#         account.balance += instance.amount
#         account.save()
#
#         print("account balance is updated")
