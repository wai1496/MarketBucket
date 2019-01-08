import re
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from market_bucket import db
from market_bucket.helpers.helpers import validation_preparation
import re


class Marketplace(db.Model):
    __tablename__ = 'marketplaces'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # the name of the marketplace
    marketplace_name = db.Column(db.String(64), nullable=False)
    # the seller id on the marketplace
    shop_id = db.Column(db.Integer, nullable=False)
    # the sellers name or code on the marketplace
    shop_name = db.Column(db.String(64), nullable=False)
    access_token = db.Column(db.String(64), nullable=False)
    refresh_token = db.Column(db.String(64))
    shop_description = db.Column(db.Text)
    shop_logo = db.Column(db.String())

    def __init__(self, user_id, marketplace_name, shop_id, shop_name, access_token, refresh_token=None):
        self.user_id = user_id
        self.marketplace_name = marketplace_name
        self.shop_id = shop_id
        self.shop_name = shop_name
        self.access_token = access_token
        self.refresh_token = refresh_token

    def __repr__(self):
        return f"{self.shop_name} with id {self.shop_id} belonging to user {self.user_id} saved to database!"
