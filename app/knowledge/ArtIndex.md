Sure — here is the English version of your text, rewritten in Markdown and keeping the original structure.

```markdown
Project ART Index
=================
This is the ART Index project with its core functionality.

***Table of Contents:***
- 
- 
- 
     - 
     -     
     -    
- 
-   
- 
- 
- 

# Introduction <a name="Introduction"></a>

**Project ART Index** is a project description with basic functionality. The project has a standard structure and is built using GitLab CI.  
Invest Art is developed using Next.js, React, and TypeScript. The application allows users to invest in works of art.  
The project consists of several parts shown in the diagram below:

!

Art Estimate Backend (hereinafter referred to as **Backend**) contains the code responsible for data storage and request processing.  
The execution process consists of the stages shown in the diagram below:

!

Art Estimate Frontend (hereinafter referred to as **Frontend**) contains the code for the external interface of the website and applications.  
The execution process consists of the stages shown in the diagram below:

!

Art Estimate Invest Admin (hereinafter referred to as **Admin**) contains the code for the administrative panel used to manage the InvestArt platform.  
The execution process consists of the stages shown in the diagram below:

!

* Project information in Jira: 
* Project information in Confluence: 

# Build Process Optimization <a name="Build"></a> 

1. Builds for all repository parts — **Backend**, **Frontend**, and **Admin** — are performed using the ***Kaniko*** Docker image from the Google Cloud registry:  
   ***gcr.io/kaniko-project/executor:v1.9.2-debug***

2. ***Kaniko*** expects:
* `--dockerfile` — the file containing all commands for building the image
* `--destination` — the repository registry path where the image will be pushed
* `--context` — the directory whose files Kaniko uses to build the image
* `--build-arg` — ARG values passed during the build

To speed up builds, the following ***Kaniko*** parameters are used:
* `--cache` — enables caching
* `--snapshot-mode=redo` — when creating a filesystem snapshot, Kaniko takes into account the file modification time, size, mode, uid, and gid. This can be up to 50% faster than a full snapshot, especially in projects with a large number of files

Build command:
```bash
/kaniko/executor --cache --snapshot-mode=redo --force --context $CI_PROJECT_DIR/${CONTEXT} ${BUILD_ARGS} --build-arg=K8S_ENVIRONMENT --dockerfile ${DOCKERFILE_PATH} --destination ${IMAGE_FULL_PATH}
```

# Preparing Art Estimate Backend <a name="Preparing-repo-Backend"></a>

1. Project documentation must be maintained in the **README.md** file in **Markdown** format, located in the root of the repository in every branch. Versioning and documentation changes should be committed in the same way as regular code, with separate commits to the corresponding branch.

## Code Quality Check with a Sniffer <a name="Quality_phpcs"></a>

1. The code is checked inside the built container from the previous step:
```
 ${CI_REGISTRY_IMAGE}/${IMAGE_NAME}:${CI_COMMIT_REF_SLUG}-${CI_COMMIT_SHORT_SHA}
``` 

2. The code quality check command using PHP_CodeSniffer looks like this:
```bash
php ${APP_DIR}/vendor/bin/phpcs -p -w --colors --standard=${APP_DIR}/phpcs.xml ./src
```

* `-p` — shows execution progress
* `-w` — outputs warnings and errors
* `--colors` — enables colored output
* `--standard` — specifies the coding standard file
* `./src` — the directory to check

## PHP Code Validation and Analysis <a name="Quality_psalm"></a>

1. The code is checked in the same container described above.

2. Psalm is a static analysis tool for detecting errors in PHP applications. It performs advanced type inference and checks for various kinds of issues, including type errors, undefined variables, incorrect function calls, and more.

The code analysis command using Psalm looks like this:
```bash
php ${APP_DIR}/vendor/bin/psalm --root=${APP_DIR} --config=${APP_DIR}/psalm.xml
```

* `--config` — configuration file
* `--root` — project root

## Publishing the Backend Repository <a name="Public_Backend"></a>

1. Code deployment and publishing are described here: 

2. `values.yaml` code:
```YML
replicaCount: 1            # number of application replicas
migration: false           # disable database migrations
image:
  pullPolicy: IfNotPresent # the image will be pulled only if it does not exist locally
configMap:                 # use configuration files from configMap
  enabled: true            # mount external application config
  name: art-app-files      # configMap name
volumeMounts:              # define mount paths
  - name: art-app-files
    mountPath: /app/src/resources/alfa/self-lab.cer    # certificate
    subPath: self-lab.cer        # will not be updated until pod restart
  - name: art-app-files
    mountPath: /app/src/resources/alfa/self-lab.key     # key
    subPath: self-lab.key        # will not be updated until pod restart
containerName: art-api-back      # container name
containerPort: 80                # port exposed by the container
nameOverride: ""
fullnameOverride: "art-api-back" # override the full chart name in Helm
env:                             # environment variables
serviceAccount:                  # service account parameters
  create: true                   # create a service account
  name:
podSecurityContext: {}           # pod-level security parameters
securityContext: {}              # container-level security parameters
service:
  type: ClusterIP                # internal cluster communication type
  port: 80                       # accessible only inside the cluster on port 80
ingress:                         # ingress controller rules
  enabled: true                  # enable ingress
  annotations:
     nginx.ingress.kubernetes.io/proxy-body-size: 256m # maximum request size 256 MB
  hosts:
    - host: art-api-back.k8s.i.self.team  # full external DNS name of the container
      paths:
        - /                   # root path for this DNS name
resources:                    # container resources
  limits:                     # resource limits
    cpu: 4000m                # maximum 4 vCPU
    memory: 4Gi               # maximum memory 4 GB
  requests:                   # requested resources
    cpu: 250m                 # 250 millicores (1000 = 1 vCPU)
    memory: 256Mi             # 256 MB memory
nodeSelector: {}              # for all nodes
tolerations: []
affinity: {}
```  

# Preparing Art Estimate Frontend <a name="Preparing-repo-Frontend"></a>

## Frontend Launch Conditions <a name="Launch_conditions_Frontend"></a>

Below are the service launch tables for **Frontend** for different branches, with external addresses available via a web browser:

**front**
| branch | host address | api address |
|:-------|:-------------|:------------|
| develop | www.art.test.self.team | www.art.test.self.team/api/v1 |
| preprod | www.art.preprod.self.team | www.art.preprod.self.team/api/v1 |
| master | www.myinvest.art | www.myinvest.art/api/v1 |

**tech-work**
| branch | host address | api address |
|:-------|:-------------|:------------|
| develop | www.art.test.self.team | www.art.test.self.team/api/v1 |
| preprod | www.art.preprod.self.team | www.art.preprod.self.team/api/v1 |
| master | www.myinvest.art | www.myinvest.art/api/v1 |

**Ingosinvest**
| branch | host address | api address |
|:-------|:-------------|:------------|
| develop | www.art-ingosinvest.test.self.team | www.art-ingosinvest.test.self.team/api/v1 |
| preprod | www.art-ingosinvest.preprod.self.team | www.art-ingosinvest.preprod.self.team/api/v1 |
| master | www.ingosinvest.myinvest.art | www.ingosinvest.myinvest.art/api/v1 |

**Alfacapital**
| branch | host address | api address |
|:-------|:-------------|:------------|
| develop | www.art-alfacapital.test.self.team | www.art-alfacapital.test.self.team/api/v1 |
| preprod | www.art-alfacapital.preprod.self.team | www.art-alfacapital.preprod.self.team/api/v1 |
| master | www.alfacapital.myinvest.art | www.alfacapital.myinvest.art/api/v1 |

## Publishing the Frontend Repository <a name="Public_Frontend"></a>

1. Code deployment and publishing are described here: 

2. `values.yaml` code:
```YML
replicaCount: 1             # number of application replicas
migration: false            # disable database migrations
image:
  pullPolicy: IfNotPresent  # image will be pulled only if it is not available locally
volume:
  enabled: false            # disable persistent volume creation
containerName: art-front      # container name
containerPort: 3000           # container port
nameOverride: ""
fullnameOverride: "art-front" # override the full chart name in Helm
env:                          # define environment variables in the container
  - name: APP_NAME
    value: "art-front"
  - name: NEXT_PUBLIC_API_URL
    value: "https://myinvest.art/api/v1"
  - name: NEXT_STAGE_NAME
    value: "prod"
  - name: APP_ENV
    value: "master"
serviceAccount:              # service account parameters
  create: true               # create a service account
  name:
podSecurityContext: {}       # pod-level security parameters
securityContext: {}          # container-level security parameters
service:
  type: ClusterIP            # internal cluster communication type
  port: 80                   # accessible only inside the cluster on port 80
ingress:                     # ingress controller rules
  enabled: true              # enable ingress
  hosts:
    - host: art-front.k8s.i.self.team  # full external DNS name
      paths:
        - /                             # root path for this DNS name
resources:                              # define container resources
  limits:                               # limits
    cpu: 2000m                          # 2 vCPU
    memory: 1Gi                         # maximum memory 1 GB
  requests:                             # minimum guaranteed resources
    cpu: 250m                           # 250 millicores (1000 = 1 vCPU)
    memory: 256Mi                       # 256 MB memory
nodeSelector: {}                        # for all nodes
tolerations: []
affinity: {}
```

# Preparing Art Estimate Invest Admin <a name="Preparing-repo-Admin"></a>

1. Code deployment and publishing are described here: 

2. `values.yaml` code:
```YML
replicaCount: 1                      # number of application replicas
migration: false                     # disable database migrations
image:
  pullPolicy: IfNotPresent           # use the local image; if unavailable, it will be pulled
volume:
  enabled: false                     # disable persistent volume creation
containerName: art-invest-admin      # container name
containerPort: 3000                  # container port
nameOverride: ""
fullnameOverride: "art-invest-admin" # override the full chart name in Helm
env:                                 # define environment variables in the container
  - name: APP_NAME
    value: "art-invest-admin"
  - name: APP_ENV  
    value: "master"
  - name: NEXT_STAGE_NAME
    value: "prod"
  - name: NEXT_PUBLIC_API_URL
    value: "https://myinvest.art/api/v1"
  - name: NEXT_PUBLIC_HOST_URL
    value: "https://admin-invest.myinvest.art"
service:
  type: ClusterIP    # internal cluster communication type
  port: 80           # accessible only inside the cluster on port 80
ingress:             # ingress controller rules
  enabled: true      # enable ingress
  annotations:
    nginx.ingress.kubernetes.io/use-regex: "true" # enable regex in path definitions
    nginx.ingress.kubernetes.io/proxy-body-size: 25m # maximum request size 25 MB
  hosts:
    - host: artinvestadmin.app # full external DNS name
      paths:
        - /                    # root path for this DNS name
    - host: art-invest-admin.k8s.i.self.team  # full external DNS name
      paths:
        - /                     # root path for this DNS name
resources:
nodeSelector: {}
tolerations: []
affinity: {}
```

# Code Deployment and Publishing <a name="Deploy"></a> 

1. Deployment for all repository parts — **Backend**, **Frontend**, and **Admin** — is performed in a custom Docker image ***helm_kubectl*** from the project registry:  
   ***selfteam/k8s-deploy/deploy/helm_kubectl:latest***

Docker image build code (Helm and kubectl are installed in Alpine):
```dockerfile
FROM alpine:3.19
ENV KUBE_VERSION=1.28.9
ENV HELM_VERSION=3.14.4
ENV YQ_VERSION=4.43.1
ARG TARGETOS
ARG TARGETARCH
ARG YQ_VERSION

RUN apk -U upgrade \
    && apk add --no-cache ca-certificates bash git openssh curl gettext jq \
    && wget -q https://storage.googleapis.com/kubernetes-release/release/v${KUBE_VERSION}/bin/${TARGETOS}/${TARGETARCH}/kubectl -O /usr/local/bin/kubectl \
    && wget -q https://get.helm.sh/helm-v${HELM_VERSION}-${TARGETOS}-${TARGETARCH}.tar.gz -O - | tar -xzO ${TARGETOS}-${TARGETARCH}/helm > /usr/local/bin/helm \
    && wget -q https://github.com/mikefarah/yq/releases/download/v${YQ_VERSION}/yq_${TARGETOS}_${TARGETARCH} -O /usr/local/bin/yq \
    && chmod +x /usr/local/bin/helm /usr/local/bin/kubectl /usr/local/bin/yq \
    && mkdir /config \
    && chmod g+rwx /config /root \
    && helm repo add "stable" "https://charts.helm.sh/stable" --force-update \
    && kubectl version --client \
    && helm version
WORKDIR /config
```

* `helm repo add "stable" "https://charts.helm.sh/stable" --force-update` — adds and force-updates the official stable Helm chart repository
* `jq` is required for stream processing of JSON files

2. Kubernetes cluster launch code:
```bash
kubectl config set-cluster k8s --server="$KUBE_URL" --insecure-skip-tls-verify=true
kubectl config set-credentials admin --token="$KUBE_TOKEN"
kubectl config set-context default --cluster=k8s --user=admin
kubectl config use-context default
kubectl create namespace ${NAMESPACE} -o yaml --dry-run=client | kubectl apply -f - || /bin/true
kubectl create -n ${NAMESPACE} secret docker-registry regcred --docker-server=registry.self.team --docker-username=k8s-selfteam --docker-password=${K8S_SELFTEAM_PASSWORD} --docker-email=admin@self.team -o yaml --dry-run=client | kubectl apply -f - || /bin/true
kubectl delete -n ${NAMESPACE} jobs.batch app-migrate || true
```

* configure the connection to the Kubernetes cluster with TLS verification skipped; `--insecure-skip-tls-verify=true` is used when HTTPS/TLS verification is not required
* `kubectl config set-credentials admin --token=` — adds token information for the `admin` user to the kubectl configuration file
* `kubectl config set-context default --cluster=k8s --user=admin` — creates a Kubernetes context in the config. A context is a combination of cluster, user, and optional namespace that defines how to interact with the cluster
* `kubectl config use-context default` — switches to the `default` context so all subsequent kubectl commands use its parameters
* `kubectl create namespace ${NAMESPACE} -o yaml --dry-run=client | kubectl apply -f - || /bin/true` — creates a namespace and outputs YAML. The command performs a client-side dry run, which allows checking correctness without sending the request to the server. In case of an error, `/bin/true` returns a zero exit code
* `kubectl create -n ${NAMESPACE} secret docker-registry regcred --docker-server=registry.self.team --docker-username=k8s-selfteam --docker-password=${K8S_SELFTEAM_PASSWORD} --docker-email=admin@self.team -o yaml --dry-run=client | kubectl apply -f - || /bin/true` — creates a secret in the namespace for connecting to the registry
* `kubectl delete -n ${NAMESPACE} jobs.batch app-migrate || true` — deletes the `app-migrate` batch job from the namespace

3. Application deployment code:
```bash
helm upgrade --install --wait --timeout 10m ${APP}${WORKER}-${CI_COMMIT_REF_SLUG} -n ${NAMESPACE} ${HELM_CHART_URL} -f k8s/values.yaml --set "image.repository=${IMAGE_FULL_PATH}"
```

Expected variables:
* ***APP*** — possible values depending on the repository:
     * ***art-api-back*** — for the *backend* repository
     * ***art-investadmin*** — for the *admin* repository     
     * ***art-front*** — for the *frontend* repository
     * ***art-front-tech-work*** — for the *frontend* repository
     * ***art-front-ingosinvest*** — for the *frontend* repository 
     * ***art-front-alfacapital*** — for the *frontend* repository
* ***WORKER*** — takes the value ***-cron*** in the *backend* repository for **deploy:worker:cron:**
* ***CI_COMMIT_REF_SLUG*** — unique branch identifier
* ***NAMESPACE*** — Kubernetes namespace; may take three values depending on the branch:
     * ***art-estimate-preprod*** — `preprod` branch
     * ***art-estimate-test*** — `test` branch
     * ***art-estimate*** — `master` branch
* ***HELM_CHART_URL*** — `https://${CI_SERVER_HOST}/api/v4/projects/78/repository/archive.tar.gz?private_token=${K8S_SELFTEAM_HELM_TOKEN}` — Helm chart repository  
  
* ***IMAGE_FULL_PATH*** — image repository to use, with values depending on the current repository:

For **Backend**: 
  * ***art-api-back-cron:tag***
  * ***art-api-back:tag***

For **Admin**:
  * ***art-investadmin:tag***

For **Frontend**:
  * ***art-front-tech-work:tag***
  * ***art-front-alfacapital:tag***
  * ***art-front-ingosinvest:tag***
  * ***art-front:tag***

* `--set "image.repository=${IMAGE_FULL_PATH}"` — specifies the container image listed above
* `-f` — YAML file for Helm for each repository; , , and  are described above
* `helm upgrade --install` — installs the Helm chart if not installed, or upgrades it with new values

# Helm Chart Description <a name="Helm"></a> 

Folder structure:
```
chart/
├── Chart.yaml  
├── values.yaml
└── templates/
    ├── _helpers.tpl
    ├── deployment.yaml
    ├── ingress.yaml
    ├── NOTES.txt
    ├── pvc.yaml
    ├── service.yaml
    ├── _helpers.tpl
    ├── serviceaccount.yaml
    └── tests/
        └── test-connection.yaml
```

Description:

* `Chart.yaml` is the main required chart manifest file. Its name starts with a capital letter.
```YML
apiVersion: v2                             # version
name: self                                 # name
description: A Helm chart for Kubernetes   # description
type: application
version: 1.1.14                            # chart version, follows the SemVer2 standard
appVersion: latest                         # application version used in the chart
```

* `values.yaml` contains default variables, as well as the list and description of variables the chart expects.
```YML
# Number of ReplicaSet replicas
replicaCount: 1
# Number of ReplicaSet revisions to keep from previous deployments
revisionHistory: 0
# pullPolicy: Always is used when tagging with the same tag, for example image:latest
# Default value: IfNotPresent
image:
  pullPolicy: IfNotPresent
#  repository: registry.self.team
# Name of the secret with configured pull access to the Docker registry
imagePullSecrets:
  - name: regcred
# This variable should be set to true if the application
# works with queue servers such as Nats-Streaming-Server or RabbitMQ
# This determines the release update strategy, because queue servers
# may reject connections from the newly created pod while the old pod is still running
# This variable allows terminating connections from the old pod first,
# and only then starting a new one
useQueueServers: false
# Use configuration files from configMap
configMap:  # true - if an external app config is mounted, false - if using the default config or filling values via environment variables
  enabled: false
  # configMap name (used in deployment: spec.volumes.name, spec.volumes.name.configMap.name)
command: []
imagePullSecrets: 
  - name: regcred
nameOverride: ""
fullnameOverride: ""
health: false
serviceAccount:  # Specifies whether a service account should be created
  create: true   # The name of the service account to use
  # If not set and create is true, a name is generated using the fullname template
  name:
podSecurityContext: {}
securityContext: {}
service:
  type: ClusterIP
  port: 80
ingress:
  enabled: false
resources:
  requests:    # minimum guaranteed resources
    memory: 128Mi
    cpu: 150m  # 150 millicores (1000 = 1 vCPU)
  limits:
    memory: 256Mi
    cpu: 250m
nodeSelector: {}
tolerations: []
affinity: {}
``` 

The `templates/` directory is a required directory containing Kubernetes manifest templates — YAML files that Helm renders using values from `values.yaml` and passed parameters. It contains Kubernetes object manifests required to run and operate the application in the cluster.

* `NOTES.txt` contains additional instructions and messages displayed after chart installation and when viewing the release status.

Code:
```
1. Get the application URL by running these commands:
{{- if .Values.ingress.enabled }}
{{- range $host := .Values.ingress.hosts }}
  {{- range .paths }}
  http{{ if $.Values.ingress.tls }}s{{ end }}://{{ $host.host }}{{ . }}
  {{- end }}
{{- end }}
{{- else if contains "NodePort" .Values.service.type }}
  export NODE_PORT=$(kubectl get --namespace {{ .Release.Namespace }} -o jsonpath="{.spec.ports[0].nodePort}" services {{ include "self.fullname" . }})
  export NODE_IP=$(kubectl get nodes --namespace {{ .Release.Namespace }} -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT
{{- else if contains "LoadBalancer" .Values.service.type }}
     NOTE: It may take a few minutes for the LoadBalancer IP to be available.
           You can watch the status of by running 'kubectl get --namespace {{ .Release.Namespace }} svc -w {{ include "self.fullname" . }}'
  export SERVICE_IP=$(kubectl get svc --namespace {{ .Release.Namespace }} {{ include "self.fullname" . }} --template "{{"{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}"}}")
  echo http://$SERVICE_IP:{{ .Values.service.port }}
{{- else if contains "ClusterIP" .Values.service.type }}
  export POD_NAME=$(kubectl get pods --namespace {{ .Release.Namespace }} -l "app.kubernetes.io/name={{ include "self.name" . }},app.kubernetes.io/instance={{ .Release.Name }}" -o jsonpath="{.items[0].metadata.name}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace {{ .Release.Namespace }} port-forward $POD_NAME 8080:80
{{- end }}
```

For example, the output for **Admin** (`develop` branch) looks like this:
```
1. Get the application URL by running these commands:
  http://dev.artinvestadmin.app/
  http://art-invest-admin-dev.k8s.i.self.team/
```

* `deployment.yaml` — deploys applications with the required number of replicas

Code:
```YML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "self.fullname" . }}  
  labels:
    {{- include "self.labels" . | nindent 4 }}
spec:
  {{- if .Values.useQueueServers }} # default value is false because queue servers are not used
  strategy:
    type: Recreate
  {{- end }}
  replicas: {{ .Values.replicaCount }}
  revisionHistoryLimit: {{ .Values.revisionHistory }}
  selector:
    matchLabels:
      {{- include "self.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        rollme: {{ randAlphaNum 5 | quote }}
      labels:
        {{- include "self.selectorLabels" . | nindent 8 }}
    spec:
    {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
    {{- end }}
      serviceAccountName: {{ include "self.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      {{- if .Values.configMap.enabled }}
      volumes:
        - name: "{{ .Values.configMap.name }}"
          configMap:
            name: "{{ .Values.configMap.name }}"
      {{- end }}
      containers:
        - name: {{ .Values.containerName }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.image.repository }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          {{- if .Values.command }}
          command: 
            {{- toYaml .Values.command | nindent 12 }}
          {{- end }}
          env:
          {{- if .Values.env }}
            {{- toYaml .Values.env | nindent 12 }}
          {{- end }}
          ports:
            - name: http
              containerPort: {{ .Values.containerPort }}
              protocol: TCP
          {{- if .Values.health }}
          livenessProbe:
            httpGet:
              path: /health
              port: http
            periodSeconds: 10
            timeoutSeconds: 30
          readinessProbe:
            httpGet:
              path: /readiness
              port: http
            periodSeconds: 10
            timeoutSeconds: 30
          {{- end }}
          {{- if .Values.configMap.enabled }}
          volumeMounts:
            {{- if .Values.volumeMounts }}
              {{- toYaml .Values.volumeMounts | nindent 12 }}
            {{- end }}
          {{- end }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
    {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
    {{- end }}
    {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
    {{- end }}
```

* `ingress.yaml` — describes the object that manages external access to services running in the cluster. It acts as a reverse proxy and load balancer, routing external HTTP and HTTPS traffic to different services inside the cluster.

Code:
```YML
{{- if .Values.ingress.enabled -}}
{{- $fullName := include "self.fullname" . -}}
{{- $svcPort := .Values.service.port -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ $fullName }}
  labels:
    {{- include "self.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  ingressClassName: nginx # specify the ingress controller class: nginx
{{- if .Values.ingress.tls }}
  tls:
  {{- range .Values.ingress.tls }}
    - hosts:
      {{- range .hosts }}
        - {{ . | quote }}
      {{- end }}
      secretName: {{ .secretName }}
  {{- end }}
{{- end }}
  rules:
  {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
        {{- range .paths }}
          - path: {{ . }}
            pathType: Prefix
            backend:
              service:
                name: {{ $fullName }}
                port:
                  number: {{ $svcPort }}
        {{- end }}
  {{- end }}
{{- end }}
```

* `pvc.yaml` — creates a resource that represents a storage request from a pod. It specifies storage requirements such as size, access mode, and storage class. Kubernetes uses the PVC to find an available PersistentVolume (PV) that satisfies the PVC requirements. After the PVC is created, it can be mounted as a volume in a pod so the pod can store and retrieve data.

Code:
```YML
{{- if .Values.pvc }} # value is not defined
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: {{ .Values.pvc.name }}
  labels:
    {{- include "self.labels" . | nindent 4 }}
spec:
  accessModes:
  - ReadWriteMany  # read/write access to the same storage for multiple pods
  resources:
    requests:
      storage: {{ .Values.pvc.storage }} 
  storageClassName: nfs
{{- end }}
```

* `service.yaml` — defines a logical set of pods and a policy for accessing them. The set of pods is determined based on labels assigned at pod creation time and selectors.

Code:
```YML
apiVersion: v1
kind: Service
metadata:
  name: {{ include "self.fullname" . }}
  labels:
    {{- include "self.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http
      protocol: TCP
      name: http
  selector:
    {{- include "self.selectorLabels" . | nindent 4 }}
```

* `serviceaccount.yaml` — all communication between cluster components goes through requests to the API server, and each such request is authorized with a token. This token is automatically generated when a **ServiceAccount** object is created and stored in a secret. To grant more permissions to the application or configure custom access control, a service account is created for the application. When pod containers are started, the secret with the token for that service account is mounted into them.

Code:
```YML
{{- if .Values.serviceAccount.create -}}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{ include "self.serviceAccountName" . }}  # specify the service account name
  labels:
{{ include "self.labels" . | nindent 4 }}
{{- end -}}
```

* `_helpers.tpl` — a utility for code reuse (used via **{{-include <template name> }}**) and configuration management. It contains reusable templates (starting with **{{- define <template name> }}** and ending with **{{- end -}}**), helper functions, and common values. This simplifies chart templates and makes them more readable and maintainable.

Code:
```
{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "self.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "self.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "self.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "self.labels" -}}
helm.sh/chart: {{ include "self.chart" . }}
{{ include "self.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "self.selectorLabels" -}}
app.kubernetes.io/name: {{ include "self.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "self.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{ default (include "self.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}
```

# Conclusion <a name="Conclusion"></a> 

This description is written in Markdown.  
 is a lightweight markup language created to make text as readable and easy to edit as possible, while still being suitable for conversion into more advanced publishing formats such as HTML, Rich Text, and others.

There are many online tools available for working with it, including tools with guides for proper text formatting, for example:
*  — an online editor where you can format Markdown files on the fly and view the rendered output.

GitHub also supports automatic rendering of `README.md` files in Markdown format.

You can add an index (table of contents) with internal anchors to Markdown documentation. Links in such a table of contents are clickable, just like in a regular HTML document. This is especially useful for large Markdown documents.
```

If you want, I can also do one of these next:
1. **make the English version more formal and technical**,  
2. **rewrite it as a polished README for GitHub/GitLab**,  
3. **fix style issues and grammar in both Russian and English versions**.