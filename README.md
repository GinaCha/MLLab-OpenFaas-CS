# MLLab-OpenFaaS

# Prerequisites
1. Git Bash for Windows (recommended by OpenFaaS instead of WSL)
2. A kubernetes cluster (we'll use minikube for ease)
3. [Helm3](https://github.com/helm/helm/releases/latest) to deploy the OpenFaaS chart to the cluster.
   * Get the latest release from the link and unzip to a folder in your path (for example ```C:\Windows```)
    
   * Or using Git Bash for windows run:

    ```bash 
    curl -sSLf https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
    ```



# 1. Depoloyment

## Step 1

---

### Start a k8s cluster using `Minikube`

First set the cluster settings (adjust accordingly):

```bash 
minikube config set driver hyperv
minikube config set cpus 4
minikube config set memory 10G
minikube config set disk-size 20G 
minikube config set EmbedCerts true
minikube config set insecure-registry true
minikube config set kubernetes-version 1.21.2
minikube config set profile minikube-openfaas
```

Then just run:

```bash
minikube start
```

## Step 2

---

### Deploy OpenFaaS through `helm3`

First create 2 namespaces in your cluster:
- `openfaas` -> where the core openfaas pods are located (Gateway, Prometheus ...)
- `openfaas-fn` -> where function pods will be executed
 
 You can create those 2 namespaces using the following command:

 ```bash
kubectl apply -f https://raw.githubusercontent.com/openfaas/faas-netes/master/namespaces.yml
```

Add the OpenFaaS `helm` chart & get repository:

```bash
helm repo add openfaas https://openfaas.github.io/faas-netes/
helm repo update
```

 **IMPORTANT:** 

Create the basic authentication secrets using the provided yaml file in this repository **before** you install the helm chart, so that the gateway authentication uses your provided credentials. You can change the default username & password in the [basic-auth-secret.yaml](helm/basic-auth-secret.yaml) file before applying with:

```bash
kubectl apply -f helm/basic-auth-secret.yaml
``` 

Then finally you can install openfaas in your cluster, using our desired [values](helm\values.yaml) with `helm` by running:

```bash
helm upgrade openfaas --install openfaas/openfaas --namespace openfaas --values helm/values.yaml
```

## Step 3

---

### Access the OpenFaaS `gateway`

In order to access the OpenFaaS gateway either through the web-UI or using the faas-cli we need to be able to connect to the cluster service.

* First check that the gateway is ready

```bash
kubectl rollout status -n openfaas deploy/gateway
```

In order to be able to connect to the `gateway` service through `localhost` we have to port-forward that service.
* Start a <u>**new terminal**</u> and run:

```bash
kubectl port-forward svc/gateway -n openfaas 8090:8080
```

This command will open a tunnel from your Kubernetes cluster to your local computer so that you can access the OpenFaaS gateway. There are other ways to access OpenFaaS, but that is beyond the scope of this workshop.

Your gateway URL is: 

`http://127.0.0.1:8090`  ([link](http://127.0.0.1:8090))

* Another way to access the gateway is through it's NodePort. You can get the gateway url running the following:
  
    ```bash
    echo "OpenFaaS Gateway listening in: http://$(minikube ip):$(kubectl -n openfaas get svc gateway-external -o jsonpath="{.spec.ports[0].nodePort}")"
    ```


---

**IMPORTANT:** If you're using bash you should set the environment variable for the CLI using:

```bash
export -- OPENFAAS_URL="http://127.0.0.1:8090"
# export -- OPENFAAS_URL="http://172.28.0.196:31112"
```

## Step 4

---

### Logging into the gateway using the CLI

<u>AFTER you have set</u> the `OPENFAAS_URL` environment variable to the up and port your gateway server is running, you can login to the gateway using the faas-cli by running:

```bash
faas-cli login --username admin --password pass
```

In the above commands admin username is `admin` and admin password is `pass`.

## Grafana

---

You can apply the provided YAML files to your cluster in the openfaas namespace in order to deploy a sample Grafana dashboard for OpenFaaS

```bash
kubectl apply -f grafana/
``` 

Then you can access Grafana by the URL obtained by running the command below:

```bash
echo "Grafana Dashboard listening in: http://$(minikube ip):$(kubectl -n openfaas get svc grafana -o jsonpath="{.spec.ports[0].nodePort}")"
```

Default admin credentials are:

- username: `admin`
- pass: `1qa2ws!@`


## MinIO

---

You can deploy a `MinIO` container & persistent volume using helm, and the provided values file as follows

First add the helm chart to your repos and download it:

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

Then create a `minio` namespace and apply the [minio-keys](minio/minio-keys.yaml) file to generate the initial administrator user credentials (modify according to your preferences).

```bash
kubectl create namespace minio
kubectl apply -n minio -f minio/minio-keys.yaml
```

Then you can take a look at the [helm chart values](minio/values.yaml), modify anything you want and finally install the helm chart using:

```bash
helm upgrade minio bitnami/minio --install --namespace minio --values minio/values.yaml --wait
```

After the deployment is complete you can access the MinIO browser using the url obtained by:

```bash
echo "MinIO browser listening in: http://$(minikube ip):$(kubectl -n minio get svc minio -o jsonpath="{.spec.ports[0].nodePort}")"
```

And <u>pods **within** the cluster</u> can access the MinIO API using

```
http://minio.minio.svc.cluster.local:9000
```

## Node-RED

---

You can deploy a `node-RED` container & persistent volume using the provided kubernetes specification yaml files in the [node-red](./node-red) directory

First, create a `namespace` for the node-red deployment:

```bash
kubectl create ns node-red
```

Then you can apply the provided yaml files using:

```bash
kubectl apply -n node-red -f node-red/cm.yaml -f node-red/pvc.yaml -f node-red/deployment.yaml -f node-red/service.yaml
```

Wait until the rollout is finished:
```bash
kubectl rollout status -n node-red deployment node-red
```

And after it's done you can access the dashboard at:

```bash
echo "Node-RED dashboard at: http://$(minikube ip):$(kubectl -n node-red get svc node-red -o jsonpath="{.spec.ports[0].nodePort}")"
```

---

<br>

## Authors

* **<a href="https://github.com/GinaCha" target="_blank">`Gina Chatzimarkaki`</a>.** - *Initial work* 

---

<br>

## License

This project is licensed under the Apache License  - see the [LICENSE](LICENSE) file for details
