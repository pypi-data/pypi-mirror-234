from starlette.datastructures import MutableHeaders, Headers, MultiDict


def inheritance_service_headers(
    gateway_headers: MutableHeaders,
    service_headers: MutableHeaders,
) -> MutableHeaders:
    forced_gateway_headers = [
        "server",
        "date",
        "content-encoding",
        "content-type",
        "content-length",
    ]
    headers = MutableHeaders()
    for key, value in service_headers.items():
        if key not in gateway_headers and key.lower() not in forced_gateway_headers:
            headers.append(key, value)
    return headers


def generate_headers_for_microservice(headers: Headers) -> MutableHeaders:
    new_headers = headers.mutablecopy()
    gateway_host = headers.get("host")
    new_headers.append("gateway_host", gateway_host)

    forced_gateway_headers = [
        "host",
        "content-type",
        "accept-encoding",
        "content-length",
    ]
    [new_headers.__delitem__(key_header) for key_header in forced_gateway_headers]

    return new_headers
