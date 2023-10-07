
class KubefacetsFEException(Exception):
    msg = "Unexpected Error"
    status_code = 500
    redirect_url = "/"

    def __init__(self, msg, code, redirectUrl):
        self.msg = msg
        self.status_code = code
        self.redirect_url = redirectUrl
