# Wildflower FastAPI/Auth0 integration

Basic token verification for FastAPI and Auth0.  Also includes support for the Wildflower Permissions API, which provides centralized Role/Domain based access control.

## Environment Configuration

`AUTH0_DOMAIN` Domain to auth against within Auth0

`API_AUDIENCE` Audience the tokens should target

`CLIENT_ID` Client ID for machine-to-machine authenticatio for checking user Profiles

`CLIENT_SECRET` Client Secret for machine-to-machine authenticatio for checking user Profiles


### For permissions-api integration (optional)

`TOKEN_EMAIL_DOMAIN` Domain to add to client_credentials for email address for `wf_permissions` integration

`TOKEN_DOMAIN` Domain to add to client_credentials for `wf_permissions` integration

`PERMS_API_URI` URI for permissions API

`PERMS_API_AUD` Audience to auth against with machine-to-machine tokens
