.. _eherkenning_oidc:

================================================
Configuration for eHerkenning via OpenID Connect
================================================

Settings Overview
=================


Enable/Disable configuration:
"""""""""""""""""""""""""""""

::

    EHERKENNING_OIDC_CONFIG_ENABLE



Required:
"""""""""

::

    EHERKENNING_OIDC_OIDC_RP_CLIENT_ID
    EHERKENNING_OIDC_OIDC_RP_CLIENT_SECRET


All settings:
"""""""""""""

::

    EHERKENNING_OIDC_ENABLED
    EHERKENNING_OIDC_ERROR_MESSAGE_MAPPING
    EHERKENNING_OIDC_IDENTIFIER_CLAIM_NAME
    EHERKENNING_OIDC_OIDC_EXEMPT_URLS
    EHERKENNING_OIDC_OIDC_KEYCLOAK_IDP_HINT
    EHERKENNING_OIDC_OIDC_NONCE_SIZE
    EHERKENNING_OIDC_OIDC_OP_AUTHORIZATION_ENDPOINT
    EHERKENNING_OIDC_OIDC_OP_DISCOVERY_ENDPOINT
    EHERKENNING_OIDC_OIDC_OP_JWKS_ENDPOINT
    EHERKENNING_OIDC_OIDC_OP_LOGOUT_ENDPOINT
    EHERKENNING_OIDC_OIDC_OP_TOKEN_ENDPOINT
    EHERKENNING_OIDC_OIDC_OP_USER_ENDPOINT
    EHERKENNING_OIDC_OIDC_RP_CLIENT_ID
    EHERKENNING_OIDC_OIDC_RP_CLIENT_SECRET
    EHERKENNING_OIDC_OIDC_RP_IDP_SIGN_KEY
    EHERKENNING_OIDC_OIDC_RP_SCOPES_LIST
    EHERKENNING_OIDC_OIDC_RP_SIGN_ALGO
    EHERKENNING_OIDC_OIDC_STATE_SIZE
    EHERKENNING_OIDC_OIDC_USE_NONCE
    EHERKENNING_OIDC_USERINFO_CLAIMS_SOURCE

Detailed Information
====================

::

    Variable            EHERKENNING_OIDC_ENABLED
    Setting             inschakelen
    Description         Geeft aan of OpenID Connect voor authenticatie/autorisatie is ingeschakeld. Deze heeft voorrang op het gebruik van SAML voor eHerkenning-authenticatie.
    Possible values     True, False
    Default value       False
    
    Variable            EHERKENNING_OIDC_ERROR_MESSAGE_MAPPING
    Setting             Foutmelding mapping
    Description         Mapping die de door de identiteitsprovider geretourneerde foutmeldingen, omzet in leesbare meldingen die aan de gebruiker worden getoond
    Possible values     Mapping: {'some_key': 'Some value'}
    Default value       {}
    
    Variable            EHERKENNING_OIDC_IDENTIFIER_CLAIM_NAME
    Setting             KVK claim naam
    Description         De naam van de claim waarin het KVK nummer van de gebruiker is opgeslagen
    Possible values     string
    Default value       kvk
    
    Variable            EHERKENNING_OIDC_OIDC_EXEMPT_URLS
    Setting             URLs exempt from session renewal
    Description         This is a list of absolute url paths, regular expressions for url paths, or Django view names. This plus the mozilla-django-oidc urls are exempted from the session renewal by the SessionRefresh middleware.
    Possible values     string, comma-delimited ('foo,bar,baz')
    Default value       
    
    Variable            EHERKENNING_OIDC_OIDC_KEYCLOAK_IDP_HINT
    Setting             Keycloak-identiteitsprovider hint
    Description         Specifiek voor Keycloak: parameter die aangeeft welke identiteitsprovider gebruikt moet worden (inlogscherm van Keycloak overslaan).
    Possible values     string
    Default value       No default
    
    Variable            EHERKENNING_OIDC_OIDC_NONCE_SIZE
    Setting             Nonce size
    Description         Sets the length of the random string used for OpenID Connect nonce verification
    Possible values     string representing a positive integer
    Default value       32
    
    Variable            EHERKENNING_OIDC_OIDC_OP_AUTHORIZATION_ENDPOINT
    Setting             Authorization endpoint
    Description         URL of your OpenID Connect provider authorization endpoint
    Possible values     string (URL)
    Default value       No default
    
    Variable            EHERKENNING_OIDC_OIDC_OP_DISCOVERY_ENDPOINT
    Setting             Discovery endpoint
    Description         URL of your OpenID Connect provider discovery endpoint ending with a slash (`.well-known/...` will be added automatically). If this is provided, the remaining endpoints can be omitted, as they will be derived from this endpoint.
    Possible values     string (URL)
    Default value       No default
    
    Variable            EHERKENNING_OIDC_OIDC_OP_JWKS_ENDPOINT
    Setting             JSON Web Key Set endpoint
    Description         URL of your OpenID Connect provider JSON Web Key Set endpoint. Required if `RS256` is used as signing algorithm.
    Possible values     string (URL)
    Default value       No default
    
    Variable            EHERKENNING_OIDC_OIDC_OP_LOGOUT_ENDPOINT
    Setting             Endpoint uitlog
    Description         URL van het uitlog-endpoint van uw OpenID Connect Connect-provider
    Possible values     string (URL)
    Default value       No default
    
    Variable            EHERKENNING_OIDC_OIDC_OP_TOKEN_ENDPOINT
    Setting             Token endpoint
    Description         URL of your OpenID Connect provider token endpoint
    Possible values     string (URL)
    Default value       No default
    
    Variable            EHERKENNING_OIDC_OIDC_OP_USER_ENDPOINT
    Setting             User endpoint
    Description         URL of your OpenID Connect provider userinfo endpoint
    Possible values     string (URL)
    Default value       No default
    
    Variable            EHERKENNING_OIDC_OIDC_RP_CLIENT_ID
    Setting             OpenID Connect client ID
    Description         OpenID Connect client ID provided by the OIDC Provider
    Possible values     string
    Default value       No default
    
    Variable            EHERKENNING_OIDC_OIDC_RP_CLIENT_SECRET
    Setting             OpenID Connect secret
    Description         OpenID Connect secret provided by the OIDC Provider
    Possible values     string
    Default value       No default
    
    Variable            EHERKENNING_OIDC_OIDC_RP_IDP_SIGN_KEY
    Setting             Sign key
    Description         Key the Identity Provider uses to sign ID tokens in the case of an RSA sign algorithm. Should be the signing key in PEM or DER format.
    Possible values     string
    Default value       No default
    
    Variable            EHERKENNING_OIDC_OIDC_RP_SCOPES_LIST
    Setting             OpenID Connect scopes
    Description         OpenID Connect-scopes die worden bevraagd tijdens het inloggen. Deze zijn hardcoded en moeten worden ondersteund door de identiteitsprovider.
    Possible values     string, comma-delimited ('foo,bar,baz')
    Default value       openid, kvk
    
    Variable            EHERKENNING_OIDC_OIDC_RP_SIGN_ALGO
    Setting             OpenID sign algorithm
    Description         Algorithm the Identity Provider uses to sign ID tokens
    Possible values     string
    Default value       HS256
    
    Variable            EHERKENNING_OIDC_OIDC_STATE_SIZE
    Setting             State size
    Description         Sets the length of the random string used for OpenID Connect state verification
    Possible values     string representing a positive integer
    Default value       32
    
    Variable            EHERKENNING_OIDC_OIDC_USE_NONCE
    Setting             Use nonce
    Description         Controls whether the OpenID Connect client uses nonce verification
    Possible values     True, False
    Default value       True
    
    Variable            EHERKENNING_OIDC_USERINFO_CLAIMS_SOURCE
    Setting             user information claims extracted from
    Description         Indicates the source from which the user information claims should be extracted.
    Possible values     userinfo_endpoint, id_token
    Default value       userinfo_endpoint
