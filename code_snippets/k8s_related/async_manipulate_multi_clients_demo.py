import asyncio

from kubernetes_asyncio import client, config
from kubernetes_asyncio.client.api_client import ApiClient
from kubernetes_asyncio.client.configuration import Configuration


async def main():
    # You can load multi cluster config by different client_config
    client_config = Configuration()
    # load kube config into client_config instance
    await config.load_kube_config(config_file='~/.kube/config', client_configuration=client_config)
    async with ApiClient(configuration=client_config) as api:
        v1 = client.CoreV1Api(api_client=api)
        # get namespaces
        res = await v1.list_namespace(timeout_seconds=3)
        # print namespaces
        print(len(res.items))


if __name__ == '__main__':
    asyncio.run(main())
