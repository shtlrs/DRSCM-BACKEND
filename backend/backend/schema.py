from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object
from django.utils.translation import gettext_lazy as _


class JWTAuthenticationSchema(OpenApiAuthenticationExtension):

    target_class = "rest_framework_simplejwt.authentication.JWTAuthentication"
    name = "JWT Authentication"

    def get_security_definition(self, auto_schema):

        security_schema = build_bearer_security_scheme_object(
            header_name="Authorization", token_prefix="Bearer", bearer_format="JWT"
        )

        security_schema["description"] = _(
            r"Our api uses JSON Web Tokens for authentication purposes.<br>"
            "In order to obtain a token, you need to be registered by an admin first.<br>"
            "Then you would need to refer to the [token](#tag/token) section below"
            "in order to follow the details on how to obtain one. <br>"
            '`Example` : "Authorization": "JWT {{ token }}"'
        )

        return security_schema
