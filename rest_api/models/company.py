from rest_api import db
from rest_api.models.address import AddressModel # noqa


class CompanyModel(db.Model):

    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    phone = db.Column(db.String(20))
    password_hash = db.Column (db.String(256))
    is_deleted =db.Column(db.Integer)

    addresses = db.relationship ("AddressModel", lazy="dynamic")

    def __init__(self, name, password_hash, email, phone):
        self.name = name
        self.password_hash = password_hash
        self.email = email
        self.phone = phone
        self.is_deleted=0

    def json(self):
        return {
            "id":self.id,
            "name":self.name,
            "email":self.email,
            "phone":self.phone,
            "is_deleted": self.is_deleted,
            "addresses": [address.json() for address in self.addresses.all()]
        }

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name, is_deleted=0).first()

    @classmethod
    def find_all(cls):
        return cls.query.filter_by(is_deleted=0)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        self.is_deleted=1
        db.session.add(self)
        db.session.commit()
