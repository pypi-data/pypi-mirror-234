import base64
import re
from typing import Any
from typing import Dict


BASE_URL = "/api"


async def gather(hub, profiles) -> Dict[str, Any]:
    """
    Generate token with basic auth

    Example:
    .. code-block:: yaml

        nsx_alb.alb:
          profile_name:
            username: "admin"
            password: "password"
            endpoint_url: 'https://10.65.11.14/'
            tenant: "admin"

    """

    sub_profiles = {}
    for (
        profile,
        ctx,
    ) in profiles.get("nsx_alb", {}).items():
        endpoint_url = ctx.get("endpoint_url")

        if not re.search(BASE_URL, endpoint_url):
            endpoint_url = "".join((endpoint_url.rstrip("/"), BASE_URL))
        ctx["endpoint_url"] = endpoint_url
        creds = f"{ctx.get('username')}:{ctx.get('password')}"
        # The plugin_version is hardcoded for now , but will change once the autogeneration sync gets done
        plugin_version = "30.2.1"
        initial_data_url = "/initial-data"
        headers_ctrl = {
            "Authorization": f"Basic {base64.b64encode(creds.encode('utf-8')).decode('ascii')}",
        }
        controller_initial_data = await hub.tool.nsx_alb.session.request(
            ctx,
            method="get",
            path=initial_data_url,
            headers=headers_ctrl,
        )
        if controller_initial_data["result"]:
            api_version = controller_initial_data["ret"]["version"]["Version"]
            if api_version > plugin_version:
                api_version = plugin_version
            sub_profiles[profile] = dict(
                endpoint_url=endpoint_url,
                headers={
                    "X-Avi-Version": api_version,
                    "Authorization": f"Basic {base64.b64encode(creds.encode('utf-8')).decode('ascii')}",
                },
            )
    return sub_profiles
