from market_bucket import db, S3_LOCATION


class Image(db.Model):

    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_name = db.Column(db.Text, nullable=False)
    image_caption = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.Text, nullable=False)

    def __init__(self, user_id, image_name, image_caption=None, image_url=None):
        self.user_id = user_id
        self.image_name = image_name
        self.image_caption = image_caption
        self.image_url = f'{S3_LOCATION}{self.image_name}'
