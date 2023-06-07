from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account, Interest_Junction_c,Product,Opportunity,Interest
from .documents import AccountDocument, Interest_Junction_cDocument


@receiver(post_save, sender=Account)
def update_interest_junction_c(sender, instance, **kwargs):
    # Get the related Interest_Junction_c records for the updated Account
    interest_junction_records = Interest_Junction_c.objects.filter(Account=instance)

    # Update the related Interest_Junction_c records based on the changes in Account
    for record in interest_junction_records:
        record.AccountName = instance.AccountName
        record.State = instance.State
        record.LastPurchasedDate = instance.LastPurchasedDate
        record.TotalPurchase = instance.TotalPurchase
        record.PersonHasOptedOutOfEmail = instance.PersonHasOptedOutOfEmail
        record.CategoryOfInterest = instance.CategoryOfInterest
        record.PeriodOfInterest = instance.PeriodOfInterest
        record.TypeOfInterest = instance.TypeOfInterest
        record.YoungerAudience = instance.YoungerAudience
        record.Star5 = instance.Star5
        record.AccountLastPurchaseDate = instance.AccountLastPurchaseDate
        record.HolidayCelebrated = instance.HolidayCelebrated
        record.Email = instance.Email
        record.ShippingCity = instance.ShippingCity
        record.BouncedEmail = instance.BouncedEmail
        record.OwnerId = instance.OwnerId
        record.save()




@receiver(post_save, sender=Account)
def update_opportunities(sender, instance, **kwargs):
    # Get the related Opportunity records for the updated Account
    opportunities = Opportunity.objects.filter(AccountId=instance)

    # Update the related Opportunity records based on the changes in Account
    for opportunity in opportunities:
        opportunity.AccountName = instance.AccountName
        opportunity.State = instance.State
        opportunity.LastPurchasedDate = instance.LastPurchasedDate
        opportunity.TotalPurchase = instance.TotalPurchase
        opportunity.PersonHasOptedOutOfEmail = instance.PersonHasOptedOutOfEmail
        opportunity.CategoryOfInterest = instance.CategoryOfInterest
        opportunity.PeriodOfInterest = instance.PeriodOfInterest
        opportunity.TypeOfInterest = instance.TypeOfInterest
        opportunity.YoungerAudience = instance.YoungerAudience
        opportunity.Star5 = instance.Star5
        opportunity.AccountLastPurchaseDate = instance.AccountLastPurchaseDate
        opportunity.HolidayCelebrated = instance.HolidayCelebrated
        opportunity.Email = instance.Email
        opportunity.ShippingCity = instance.ShippingCity
        opportunity.BouncedEmail = instance.BouncedEmail
        opportunity.OwnerId = instance.OwnerId
        opportunity.save()

@receiver(post_save, sender=Product)
def update_interest_junction_c_product(sender, instance, **kwargs):
    # Get the related Interest_Junction_c records for the updated Product
    interest_junction_records = Interest_Junction_c.objects.filter(Product=instance)

    # Update the related Interest_Junction_c records based on the changes in Product
    for record in interest_junction_records:
        record.Product.ProductName = instance.ProductName
        # Update other fields accordingly
        record.save()



@receiver(post_save, sender=Interest)
def update_interest_junction_c_interest(sender, instance, **kwargs):
    # Get the related Interest_Junction_c records for the updated Interest
    interest_junction_records = Interest_Junction_c.objects.filter(Interest=instance)

    # Update the related Interest_Junction_c records based on the changes in Interest
    for record in interest_junction_records:
        record.Interest.InterestName = instance.InterestName
        # Update other fields accordingly
        record.save()        