#!/usr/bin/python3

import sys,boto3
from kubernetes.client.rest import ApiException
from kubernetes import client, config


def main():

    if len(sys.argv) == 4:
        kube_config = sys.argv[1]
        app_name    = sys.argv[2]
        namespace   = sys.argv[3]
        get_pod_logs(kube_config, app_name, namespace)

    else:
        print(
            """ Usage:    get_k8s_pod_logs [kube_config]       [app_name]  [namespace]
                Example:  get_k8s_pod_logs ${HOME}/kubeconfig  hello-world technical-operations
            """
            )

def get_pod_name(kube_config, namespace, app_name):
    try:
        config.load_kube_config(config_file=kube_config)
        instance = client.CoreV1Api()
        response = instance.list_namespaced_pod(namespace, label_selector="app=" + app_name)
        msg = {}
        pod_name = ""
        for i in response.items:
            msg = i.metadata.labels
            msg['pod_name'] = i.metadata.name
            pod_name = (msg['pod_name'])
        return pod_name
    except ApiException as e:
        print('Found exception in getting the pod name: \n %s', e)

def get_pod_logs(kube_config, app_name, namespace):
    pod_name = get_pod_name(kube_config, namespace, app_name)
    try:
        config.load_kube_config(config_file=kube_config)
        instance = client.CoreV1Api()
        response = instance.read_namespaced_pod_log(name=pod_name, namespace=namespace)
        print(response)
    except ApiException as e:
        print('Found exception in reading the pod logs: \n %s', e)

if __name__ == '__main__':
    main()