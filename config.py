# config.py

from authomatic.providers import oauth2, oauth1, openid, gaeopenid

CONFIG = {

    'tw': { # Your internal provider name

        # Provider class
        'class_': oauth1.Twitter,

        # Twitter is an AuthorizationProvider so we need to set several other properties too:
        'consumer_key': '########################',
        'consumer_secret': '########################',
    },

    'fb': {

        'class_': oauth2.Facebook,

        # Facebook is an AuthorizationProvider too.
        'consumer_key': '########################',
        'consumer_secret': '########################',

        # But it is also an OAuth 2.0 provider and it needs scope.
        'scope': ['user_about_me', 'email', 'publish_stream', 'read_stream'],
    },

    'google': {
        'class_': oauth2.Google,
        'consumer_key': '765649350281-ub33kfhbhorslq5a99f4p2umo1lv8t6v.apps.googleusercontent.com',
        'consumer_secret': 'cwv0Zc5K8K_FNENWl6gU2bDd'
    }

    'gae_oi': {

        # OpenID provider based on Google App Engine Users API.
        # Works only on GAE and returns only the id and email of a user.
        # Moreover, the id is not available in the development environment!
        'class_': gaeopenid.GAEOpenID,
    },

    'oi': {

        # OpenID provider based on the python-openid library.
        # Works everywhere, is flexible, but requires more resources.
        'class_': openid.OpenID,
    }
}
