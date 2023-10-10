from .models import AUCTION, BID
from products.models import CATEGORY, PRODUCT
from datetime import date


class AuctionService:
    
    def find_auction_winner(request, product_id=None):
        today = date.today()
        if product_id is not None:
            win = False
            auction = AUCTION.objects.get(product_id=product_id)
            
            def set_auction_winner(auction):
                if BID.objects.filter(auction_id=auction.id).exists():
                    highest_bid = BID.objects.filter(auction_id=auction.id).order_by('-price').first()
                    auction.update(auction_winner=highest_bid.bider_id.email)
                    win = True
                else:
                    auction.update(auction_winner="No bid available!")
                    
            if auction.auction_end_date <= today:
                set_auction_winner(auction)
        else:
            auctions = AUCTION.objects.filter(auction_end_date__lte=today)
            for auction in auctions:
                set_auction_winner(auction)
                