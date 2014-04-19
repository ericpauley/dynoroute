import json
import base64
import hashlib
import hmac
import time

from django.conf import settings

def disqus_sso(request):
    if settings.DISQUS_SECRET_KEY and request.user.is_authenticated():
        user = request.user
        data = json.dumps({
            'id': user.id,
            'username': user.get_full_name(),
            'email': user.email,
        })

        # encode the data to base64
        message = base64.b64encode(data)
        # generate a timestamp for signing the message
        timestamp = int(time.time())
        # generate our hmac signature
        sig = hmac.HMAC(settings.DISQUS_SECRET_KEY, '%s %s' % (message, timestamp), hashlib.sha1).hexdigest()

        return {
            "disqus_sso": "%s %s %s" % (message, sig, timestamp),
            "disqus_pubkey": settings.DISQUS_PUBLIC_KEY,
        }
    else:
        return {}
