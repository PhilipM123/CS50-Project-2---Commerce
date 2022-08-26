from xml.etree.ElementTree import Comment
from django.contrib import admin

from .models import Auction_Listing, Bids, Comments, Category
# Register your models here.
admin.site.register(Auction_Listing)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Category)