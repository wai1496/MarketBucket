from market_bucket import sg, User
from sendgrid.helpers.mail import Email, Content, Mail
import time
import datetime


# def send_product_email(to, bid_id):
#     bid = Bid.query.get(bid_id)
#     billboard = Billboard.query.get(bid.billboard_id)
#     from_email = Email("bids@bidboard.com")
#     to_email = Email(to)
#     subject = f"Thank You For Placing Your Bid {User.query.get((bid.user_id)).first_name}!"
#     content = Content(
#         "text/html", f"<html><table><tr><td align='center'><img src='https://s3.amazonaws.com/bidboard/11.31851.logo.jpg' height='200px'></td></tr><tr><td>Dear {User.query.get((bid.user_id)).first_name} {User.query.get((bid.user_id)).last_name},<br><br>You have just placed a {bid.amount} MYR bid on BidBoard. The details of your booking are as follows: <br> <br>Billboard size: {billboard.size} <br>Billboard location: {billboard.location} <br>Booking Date and time: {bid.booking_at_readable}<br> <br> This is <b>NOT</b> a confirmed booking. You will recieve another email when the bidding closes to confirm your booking if you are the highest bidder. You will also recieve an email to notify you if someone has outbidded you. <br> Happy Advertising! <br><br>Kind regards, <br> Bidboard Team </td></tr><tr><td align='center'>This is a no-reply address. If you have any questions, please email us <a href='mailto:ahmed160ramzi@gmail.com'>here.</a></td></tr></table>"
#     )

#     mail = Mail(from_email, subject, to_email, content)
#     response = sg.client.mail.send.post(request_body=mail.get())
# print(response.status_code)
# print(response.body)
# print(response.headers)

def send_signup_email(to, user_id):
    from_email = Email("signup@marketbucket.com")
    to_email = Email(to)
    subject = f"Welcome to MarketBucket {User.query.get(user_id).first_name}!"
    content = Content(
        "text/html", f"<html><table><tr><td align='center'><img src='https://s3.amazonaws.com/market.bucket/1.11556.Screenshot_2019-01-08_at_21.01.12.jpg' height='200px'></td></tr><tr><td>Dear {User.query.get((user_id)).first_name} {User.query.get((user_id)).last_name},<br><br>You have just signed up on MarketBucket! <br>We encourage you to connect all of your online stores through MarketBucket to start enjoying the convenience of our services and save your time to use it on what really matters. We look forward to working with you on maximising your returns and improving your brand growth. <br> We wish you the most successful of experiences with MarketBucket! <br> <br> Kind regards, <br> MarketBucket Team </td></tr><tr><td align='center'>This is a no-reply address. If you have any questions, please email us <a href='mailto:ahmed160ramzi@gmail.com'>here.</a></td></tr></table>"
    )

    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())


def send_new_marketplace_email(to, user_id, marketplace):
    from_email = Email(f"{marketplace}@marketbucket.com")
    to_email = Email(to)
    subject = f"{marketplace} added to MarketBucket {User.query.get(user_id).first_name}!"
    content = Content(
        "text/html", f"<html><table><tr><td align='center'><img src='https://s3.amazonaws.com/market.bucket/1.11556.Screenshot_2019-01-08_at_21.01.12.jpg' height='200px'></td></tr><tr><td>Dear {User.query.get((user_id)).first_name} {User.query.get((user_id)).last_name},<br><br>You have just added {marketplace} to your MarketBucket! <br>You can now add products to all your online stores through MarketBucket and relax while we take care of your stocks and products for you. We encourage you to add your other marketplaces with us if you haven't already in order to maximise the potential of what we can do for you. <br> We wish you the most successful of experiences with MarketBucket! <br> <br> Kind regards, <br> MarketBucket Team </td></tr><tr><td align='center'>This is a no-reply address. If you have any questions, please email us <a href='mailto:ahmed160ramzi@gmail.com'>here.</a></td></tr></table>"
    )

    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
