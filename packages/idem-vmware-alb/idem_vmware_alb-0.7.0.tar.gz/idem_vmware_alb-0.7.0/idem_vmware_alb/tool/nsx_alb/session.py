import json
from typing import Any
from typing import Dict

import aiohttp


async def request(
    hub,
    ctx,
    method: str,
    path: str,
    query_params: Dict[str, str] = {},
    data: Dict[str, Any] = {},
    headers: Dict[str, Any] = {},
):
    # Enable trace logging listener for the http client
    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(hub.tool.nsx_alb.session.on_request_start)
    trace_config.on_request_end.append(hub.tool.nsx_alb.session.on_request_end)

    # path usually starts with "/" in openapi spec
    # To handle the case for basic auth to do a "get" for controller version , acct will not be present
    if ctx.get("acct"):
        url = "".join((ctx.acct.endpoint_url.rstrip("/"), path))
    else:
        url = "".join((ctx.get("endpoint_url").rstrip("/"), path))
    async with aiohttp.ClientSession(
        loop=hub.pop.Loop,
        trace_configs=[trace_config],
    ) as session:
        result = dict(ret=None, result=True, status=200, comment=[], headers={})
        if not headers.get("content-type"):
            headers["content-type"] = "application/json"
            headers["accept"] = "application/json"

        if ctx.get("acct") and "headers" in ctx.acct:
            # The acct login could set authorization and other headers
            headers.update(ctx.acct.headers)

        data = await hub.tool.nsx_alb.utils.get_appended_prefix(ctx, data=data)

        if data:
            if not data.get("tenant_ref"):
                tenant_ref_acct = ctx.acct.get("tenant_ref")
                if tenant_ref_acct:
                    data.update({"tenant_ref": "/api/tenant/?name=" + tenant_ref_acct})

            if not data.get("cloud_ref"):
                cloud_ref_acct = ctx.acct.get("cloud_ref")
                if cloud_ref_acct:
                    data.update({"cloud_ref": "/api/cloud/?name=" + cloud_ref_acct})

        if "tenant_ref" in data:
            if "name" in data["tenant_ref"]:
                tenant = data["tenant_ref"].split("=")[1]
            else:
                tenant = data["tenant_ref"].split("#")[-1]
            headers.update({"X-Avi-Tenant": tenant})
        if "X-Avi-Tenant" not in headers:
            headers.update({"X-Avi-Tenant": "admin"})

        query_params_sanitized = {
            k: v for k, v in query_params.items() if v is not None
        }

        async with session.request(
            url=url,
            method=method.lower(),
            ssl=False,
            allow_redirects=True,
            params=query_params_sanitized,
            data=json.dumps(data),
            headers=headers,
        ) as response:
            result["status"] = response.status
            result["result"] = 200 <= response.status <= 204
            result["comment"].append(response.reason)
            result["headers"].update(response.headers)
            try:
                result["ret"] = hub.tool.type.dict.namespaced(await response.json())
                response.raise_for_status()
            except Exception as err:
                result["comment"].append(result["ret"])
                result["comment"].append(f"{err.__class__.__name__}: {err}")
                result["result"] = False
                if response.status != 404:
                    try:
                        ret = await response.read()
                        result["ret"] = ret.decode() if hasattr(ret, "decode") else ret
                    except Exception as ex_read_err:
                        result["comment"].append(
                            f"Failed to read response: {ex_read_err.__class__.__name__}: {ex_read_err}"
                        )

            return result


async def append_prefix(
    hub,
    ctx,
    value: str = None,
    obj_prefix: str = None,
) -> Dict[str, Any]:
    if "_" in obj_prefix:
        obj_prefix = obj_prefix.replace("_", "")
    k = "/api/" + obj_prefix + "?name=" + value
    return k


async def on_request_start(hub, session, trace_config_ctx, params):
    hub.log.debug("Starting %s" % params)


async def on_request_end(hub, session, trace_config_ctx, params):
    hub.log.debug("Ending %s" % params)
