from market_bucket import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    marketplace_id = db.Column(db.Integer, db.ForeignKey('marketplaces.id'), nullable=False)
    product_name = db.Column(db.String(64),unique=True, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(), nullable=False)
    description = db.Column(db.Text)
    images = db.relationship("Image", backref="products", lazy=True,
                             order_by="desc(Image.id)", cascade="delete, delete-orphan")

    def __init__(self, user_id, marketplace_id, product_name, stock, price, description=None):
        self.user_id = user_id
        self.marketplace_id = marketplace_id
        self.product_name = product_name
        self.stock = stock
        self.price = price
        self.description = description

    def __repr__(self):
        return f"{self.user_id} added {self.product_name} to marketplace {self.marketplace_id} priced at {self.price} with a stock of {self.stock}!"
