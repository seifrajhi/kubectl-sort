#!/usr/bin/env python

import sys
import subprocess

# Creator and Maintainer: Saifeddine RAJHI
# Project: https://github.com/
# version: 1.0.0

cmd = sys.argv[4] if len(sys.argv) >= 5 else "help"
option3 = sys.argv[5] if len(sys.argv) >= 6 else None
option1 = ""



def pod():
    global option1
    global option2


    arg = {
        "name": ".metadata.name",
        "status": ".status.phase",
        "restarts": ".status.containerStatuses[0].restartCount",
        "age": ".status.startTime",
        "ip": ".status.podIP",
        "node": ".spec.nodeName"
    }
    
    option1 = "pod"
    option2 = arg.get(cmd)
def deployment():
    global option1
    global option2
    

    arg = {
        "name": ".metadata.name",
        "uptodate": ".status.updatedReplicas",
        "available": ".metadata.availableReplicas",
        "age": ".metadata.creationTimestamp",
        "containers": ".spec.template.spec.containers[*].name",
        "images": ".spec.template.spec.containers[*].image"
    }
    option1 = "deployment"
    option2 = arg.get(cmd)

def service():
    global option1
    global option2
    arg = {
        "name": ".metadata.name",
        "type": ".spec.type",
        "clusterip": ".spec.clusterIP",
        "port": ".spec.ports[*].port",
        "age": ".metadata.creationTimestamp"
    }
    option1 = "service"
    option2 = arg.get(cmd)

def help():
    print("""
   Missing something? need Help?
   kubectl sort  option1 option2 option3

   Available options are
        option1:
        (po/pod/pods), (deployments/deployment/deploy), (svc/service/services)

                option2(po/pod/pods):
                name, status, restarts, age, ip, node

                option2(deployments/deployment/deploy):
                name, uptodate, available, age, containers, images

                option2(svc/service/services):
                name, type, clusterIP, externalIP, ports, age

                        option3: namespace-name or all
    """)
    sys.exit()
if len(sys.argv) >= 3 and sys.argv[1] == "kubectl" and sys.argv[2] == "sort":
    arg = sys.argv[3]
    if arg in ["pod", "pods", "po"]:
        pod()
    elif arg in ["deploy", "deployments", "deployment"]:
        deployment()
    elif arg in ["svc", "service", "services"]:
        service()
    else:
        help()


    if len(sys.argv) >= 4:
        if len(sys.argv) == 5:
            option3 = "default" 
        elif len(sys.argv) == 6 and sys.argv[5] == "all":
            option3 = "--all-namespaces"
        elif len(sys.argv) == 6:
            option3 = sys.argv[5]
        else:
            help()

        if option3:
            if sys.argv[4] != "all":
                command = f"kubectl get {option1} --sort-by='{option2}' -n {option3}"
            else:
                command = f"kubectl get {option1} --sort-by='{option2}'  {option3} "
        else:
            command = f"kubectl get {option1} --sort-by='{option2}'"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        print(result.stdout)
else:
    help()


