from typing import Any
from typing import Dict


async def get_appended_prefix(
    hub,
    ctx,
    data: dict = None,
) -> Dict[str, Any]:
    if data:
        for k, v in data.items():
            if ("_ref" in k and isinstance(v, str)) and (
                ("name=" not in v) and ("/api" not in v)
            ):
                obj_prefix = k.split("_ref")[0]
                if obj_prefix == "vrf":
                    obj_prefix = "vrfcontext"
                new_value = await hub.tool.nsx_alb.session.append_prefix(
                    ctx, obj_prefix=obj_prefix, value=v
                )
                data.update({k: new_value})
            if "_ref" in k and isinstance(v, list):
                new_value_list = []
                for index in range(len(data[k])):
                    if ("name=" not in data[k][index]) and (
                        "/api" not in data[k][index]
                    ):
                        obj_prefix = k.split("_refs")[0]
                        new_value = await hub.tool.nsx_alb.session.append_prefix(
                            ctx, obj_prefix=obj_prefix, value=data[k][index]
                        )
                        new_value_list.append(new_value)
                data.update({k: new_value_list})
    return data
