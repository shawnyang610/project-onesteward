from rest_api import db
from rest_api.models.order import OrderModel # noqa
from datetime import datetime
from flask_login import UserMixin

# UserMixin adds implementations to the model for flask_login
class UserModel(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(256))
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    orders = db.relationship("OrderModel", lazy="dynamic")

    is_deleted = db.Column(db.Integer)

    def __init__(self, hashed_password, name, email, phone):
        self.password_hash=hashed_password
        self.name = name
        self. email = email
        self. phone = phone
        self.is_deleted = 0

    def json(self):
        return {
            "id":self.id,
            "name":self.name,
            "email":self.email,
            "phone":self.phone,
            "orders": [order.json() for order in self.orders.all()],
            "is_deleted":self.is_deleted
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=0).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name, is_deleted=0).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email, is_deleted=0).first()

    @classmethod
    def find_all(cls):
        return cls.query.filter_by(is_deleted=0).order_by(cls.name)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        self.is_deleted=1
        db.session.add(self)
        db.session.commit()


    ######################################################################
    #### overrides UserMixin. adding "user_" identifier to distinguish
    #### from staffs during @flask_login.user_loader callback. ###########
    def get_id(self):
        try:
            return "user_"+str(self.id)

        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')