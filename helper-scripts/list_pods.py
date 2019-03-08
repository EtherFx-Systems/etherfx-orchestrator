from kubernetes import client, config
from kubernetes.client.rest import ApiException
from pprint import pprint

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()


def update_deployment(api_instance, deployment):
    # Update container image
    # Update the deployment
    api_response = api_instance.patch_namespaced_deployment(
        name="orchestrator-logic",
        namespace="default",
        body=deployment)
    print("Deployment updated. status='%s'" % str(api_response.status))


def list_pods(api_instance, namespace):
    try: 
        api_response = api_instance.list_namespaced_pod(namespace, pretty="true")
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)


#v1 = client.CoreV1Api()
v1 = client.ExtensionsV1beta1Api()
print("Listing pods with their IPs:")


container = client.V1Container(
        name="etherfx-orchestrator",
        image="gcr.io/groupify-201122/etherfx-orchestrator:v2",
        ports=[client.V1ContainerPort(container_port=50051)])


template = client.V1PodTemplateSpec(
    metadata=client.V1ObjectMeta(labels={"app": "etherfx"}),
    spec=client.V1PodSpec(containers=[container]))


spec = client.ExtensionsV1beta1DeploymentSpec(
        replicas=3,
        template=template)


deployment = client.ExtensionsV1beta1Deployment(
    api_version="extensions/v1beta1",
    kind="Deployment",
    metadata=client.V1ObjectMeta(name="orchestrator-logic"),
    spec=spec)

#update_deployment(v1,deployment)
list_pods(v1, "default")

# for i in ret.items:
#     print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
