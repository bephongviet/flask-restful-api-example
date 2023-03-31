from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from kernelapp.models.user import User
from kernelapp.models.social_profile import SocialProfile
from kernelapp.extensions import db

class AuthenticateResource(Resource):
    def post(self):
        data = request.get_json(force=True)
        provider = data.get('provider')
        social_id = data.get('id')

        if not provider or not social_id:
            return {"error": "Invalid data. Provider and providerAccountId are required."}, 400

        social_profile = SocialProfile.query.filter_by(provider=provider, social_id=social_id).first()

        if social_profile:
            # User with this social profile exists, return JWT token
            user = social_profile.user
        else:
            # Create new user and social profile
            user = User(username=data.get('email'),password=User.generate_secure_password())
            db.session.add(user)
            db.session.commit()

            social_profile = SocialProfile(provider=provider, social_id=social_id, user_id=user.id)
            db.session.add(social_profile)
            db.session.commit()

        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, 200
