import uuid

from kernelapp.extensions import db

class SocialProfile(db.Model):
    __tablename__ = "social_profiles"

    id = db.Column(db.String(50), primary_key=True, default=str(uuid.uuid1()))
    provider = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False)
    social_id = db.Column(db.String(50), nullable=False)

    def __init__(self, provider, user_id, social_id):
        self.provider = provider
        self.user_id = user_id
        self.social_id = social_id
