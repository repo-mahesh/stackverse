from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get("credential")  # Google OAuth token
        print(token)

        if not token:
            return Response({"error": "Access token is required"}, status=400)

        try:
            # Verify the Google ID token
            print("try google")
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request())
            print("idinfo")
            print(idinfo)

            if "email" not in idinfo:
                return Response({"error": "Invalid Google token"}, status=400)

            email = idinfo["email"]
            name = idinfo.get("name", "")
            first_name = idinfo.get("given_name", "")
            last_name = idinfo.get("family_name", "")
            picture = idinfo.get("picture", "")

            # Get or create the user
            User.objects.all().delete()
            user, created = User.objects.get_or_create(
                email=email,
                defaults={"username": email, "first_name": first_name, "last_name": last_name, "name": name, "profile_picture": picture}
            )
            if not created:
                user.first_name = first_name
                user.last_name = last_name
                user.name = name
                user.profile_picture = picture
                user.save()


            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = Response({
                "message": "Login successful",
                "is_new_user": created,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "is_premium": user.is_premium,
                    "picture": user.profile_picture,
                    "first_name": user.first_name,
                }
            })
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,  # Enable in production
                samesite="Lax",
                path="/",  # Ensure cookies are accessible site-wide
            )
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite="Lax",
                path="/",  # Ensure cookies are accessible site-wide
            )

            return response

        except ValueError:
            return Response({"error": "Invalid token"}, status=400)
