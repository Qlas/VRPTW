from collections import Counter

import jwt
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import (OutstandingToken, RefreshToken,
                                             SlidingToken, TokenError)
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(("POST",))
@permission_classes((IsAuthenticated,))
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
    except KeyError:
        return Response("You need to include you refresh token", status=400)

    try:
        token = RefreshToken(refresh_token)
    except TokenError:
        return Response("You have provided an invalid token", status=400)

    token.blacklist()
    logout(request)

    return Response("Successful logout", status=200)


@api_view()
@permission_classes((IsAuthenticated,))
def obtain_ci_token(request):
    user_outstanding_tokens = OutstandingToken.objects.filter(user=request.user, blacklistedtoken__isnull=True)
    user_outstanding_tokens_decoded = [
        jwt.decode(token.token, options={"verify_signature": False}) for token in user_outstanding_tokens
    ]
    if Counter(tok["token_type"] for tok in user_outstanding_tokens_decoded)["sliding"] > 0:
        return Response({"error": "Given user can only have up to 1 CI token"}, status=400)

    token = SlidingToken.for_user(request.user)

    return Response({"token": str(token)}, status=200)


@api_view()
@permission_classes((IsAuthenticated,))
def get_ci_token(request):
    user_outstanding_tokens = OutstandingToken.objects.filter(user=request.user, blacklistedtoken__isnull=True)
    ci_token = next(
        (
            token
            for token in user_outstanding_tokens
            if jwt.decode(token.token, options={"verify_signature": False})["token_type"] == "sliding"
        ),
        None,
    )

    return Response({"token": ci_token.token if ci_token else None}, status=200)
