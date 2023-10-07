from furl import furl
from kafka import KafkaConsumer


def check(url):
    parsedUrL = furl(url)
    bootstrap_hosts = parsedUrL.host.split(",")
    bootstrap_nodes = []
    if parsedUrL.port:
        port = parsedUrL.port
    else:
        port = 9092
    for u in bootstrap_hosts:
        bootstrap_nodes.append(f"{u}:{port}")

    try:
        connection = KafkaConsumer(bootstrap_servers=bootstrap_nodes)
        if parsedUrL.path not in ("", None, "/"):
            if parsedUrL.path in connection.topics:
                return True
            else:
                return False

        return True
    except Exception:
        return False
