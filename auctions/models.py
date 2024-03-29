from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    category = models.CharField('Category',max_length=60)

    def __str__(self):
        return f"{self.category}"

class Listings(models.Model):
    title = models.CharField('Title', max_length=60)
    description = models.CharField('Description', null=True, max_length=300)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="creator_listing")
    startingBid = models.FloatField('Starting bid')
    currentBid = models.FloatField('Current bid', null=True, blank=True)
    createdDate = models.DateTimeField('Created date', auto_now_add=True)
    isActive = models.BooleanField('Active',default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="similar_listing")
    watchers = models.ManyToManyField(User, blank=True, related_name="watched_listing")
    buyer = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    img = models.URLField(null=True, blank=True)


    def __str__(self):
        return f"Auction #{self.id}: {self.title} ({self.user.username})"

    @property
    def image_url(self):
        if self.img:
            return self.img
        else:
            return "/auctions/media/images/default_img.png"

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auctions = models.ForeignKey(Listings, on_delete=models.CASCADE)
    offers = models.FloatField('Offer')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid #{self.id}: {self.offers} on ({self.auctions.title} by {self.user.username})"

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField('Comments', max_length=300)
    createdDate = models.DateTimeField('Created at', auto_now_add=True)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="get_comments")

    def __str__(self):
        return f"Comment #{self.id}: {self.user.username} on {self.listing.title}: {self.content}"