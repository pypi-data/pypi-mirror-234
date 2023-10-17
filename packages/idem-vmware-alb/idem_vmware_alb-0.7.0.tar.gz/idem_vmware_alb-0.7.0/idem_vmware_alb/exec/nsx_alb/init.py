def __init__(hub):
    hub.exec.nsx_alb.ENDPOINT_URLS = ["/api"]
    # The default is the first in the list
    hub.exec.nsx_alb.DEFAULT_ENDPOINT_URL = "/api"

    # This enables acct profiles that begin with "nsx_alb.alb" for nsx_alb modules
    hub.exec.nsx_alb.ACCT = ["nsx_alb"]
