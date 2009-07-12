import hashlib
import base64
import hmac
import urllib
import urlparse
import copy

default_entry_point = 'http://webservices.amazon.co.jp/onca/xml'

def encode(params, seckey, entry_point=default_entry_point):
    newparams = sorted(params)
    param = urllib.urlencode(newparams)

    (_, host, path, _, _, _) = urlparse.urlparse(entry_point)
    message = "\n".join(('GET', host, path, param))

    hmac_digest = hmac.new(seckey, message, hashlib.sha256).digest()
    sig = base64.b64encode(hmac_digest)

    #sig = hmac_sha256(seckey, message)
    newparams.append(('Signature', sig))

    return entry_point + "?" + urllib.urlencode(newparams)

