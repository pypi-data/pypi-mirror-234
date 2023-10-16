import operator, time
from requests import Session
from zeep import Client
from zeep.transports import Transport

proxies = {"http": "165.225.76.32:80", "https": "165.225.76.32:80"}

cert_path = "merged-CA.pem"
import operator
import time

from requests import Session
from zeep import Client
from zeep.transports import Transport


def get_wsdl_response(
    base: str,
    wsdl: str,
    method: str,
    parameters: dict[str, str],
    use_cert: bool | None = False,
    cert_path: str | None = None,
    use_proxy: bool | None = False,
    proxies: dict[str, str] | None = None,
    log: object | None = None,
) -> str | int | float | None:
    """
    Call a SOAP method and return the response.

    Args:
        base: The base URL for the SOAP service.
        wsdl: The path to the WSDL file.
        method: The name of the SOAP method to call.
        parameters: The parameters to pass to the SOAP method.
        use_cert: Whether to use a client certificate for HTTPS.
        cert_path: The path to the client certificate file.
        use_proxy: Whether to use a proxy server for the connection.
        proxies: A dictionary of proxy servers to use for the connection.
        log: A logger object for writing log messages.

    Returns:
        The response from the SOAP method, or None if an exception is raised.
    """
    wsdl_url = f"{base}/{wsdl}"
    if log is not None:
        log.info(f"Request url {wsdl_url=}, {method=} with parameters {parameters=}")

    transport = None
    session = None
    if use_cert:
        session = Session()
        session.verify = cert_path
        transport = Transport(session=session)

    client = Client(wsdl_url, transport=transport)
    if use_proxy:
        client.transport.session.proxies = proxies

    # methods
    services_names = []
    methods = {}
    for service in client.wsdl.services.values():
        services_names.append(service.name)

        for port in service.ports.values():
            operations = sorted(
                port.binding._operations.values(), key=operator.attrgetter("name")
            )

            for operation in operations:
                methods[operation.name] = {}
                if type(operation.input.body) != list:
                    methods[operation.name] = [operation.input.body.__dict__]

    client.service._binding_options["address"] = f"{base}/{method}/"

    m = [x["name"] for x in methods[method]]

    values = []
    for parameter in [x["name"] for x in methods[method]]:
        if parameter in parameters:
            values.append(parameters[parameter])

    retries = 4
    while retries > 0:
        try:
            response = client.service._operations[method](*values)
            break
        except Exception as ex:
            if log is not None:
                log.error(ex=ex)
            time.sleep(10)
            response = None
            retries -= 1
    return response
