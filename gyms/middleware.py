from django.shortcuts import redirect

class HttpsRedirectMiddleware(object):

    def process_request(self, request):
        if request.META.get("HTTP_X_FORWARDED_PROTO", "") == "http":
            return redirect("https://%s/%s" % (request.get_host(), request.get_full_path()))
