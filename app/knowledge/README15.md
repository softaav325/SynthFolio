Project Instance JTI
==============
This is project Instance JTI with functionality.

***Содержание:***
- [Введение](#Introduction)
- [Подготовка Подготовка JTI Instance](#Preparing)  
- [Запуск и публикация кода](#Deploy)
- [Описание Helm чарта](#Helm)
- [Заключение](#Сonclusion)

# Введение <a name="Introduction"></a>

**Project JTI Instance** — это описание проекта с базовой функциональностью. Проект имеет типовую структуру и сборку в Azure. 
JTI разработан с использованием Next.js, React и TypeScript. Приложение позволяет пользователям инвестировать в произведения искусства.
Проект состоит из нескольких частей, описанных на схеме ниже:

# Подготовка JTI Instance <a name="Preparing"></a>

1. Запуск и публикация кода описана тут [Запуск и публикация кода](#Deploy)

2. Код values.yaml:
```YML
replicaCount: 1                  # число копий приложения
migration: false                 # отключение миграции баз данных
image:
  pullPolicy: IfNotPresent       # используется локальное иззображение, если его нет то будет загружено
volume:
  enabled: false                 # отключаем создание постоянных томов
containerName: art-invest-admin  # имя контейнера
containerPort: 3000              # порт контейнера
nameOverride: ""
fullnameOverride: "art-invest-admin" # переопределяем полное имя диаграммы в Helm
env:                                 # определяем переменные окружения в контейнере
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
  type: ClusterIP    # устанавливаем тип внутрикластерного взаимодействия 
  port: 80           # только внутри кластера по 80 порту
ingress:             # описываем правила для ingress controllera
  enabled: true      # включаем ingress
  annotations:
    nginx.ingress.kubernetes.io/use-regex: "true" # включаем регулярные выражения в пути
    nginx.ingress.kubernetes.io/proxy-body-size: 25m # максимальный размер запроса 25
  hosts:
    - host: artinvestadmin.app # указываем полное внешнее DNS-имя 
      paths:
        - /                    # определяем путь к корню по этому DNS имени 
    - host: art-invest-admin.k8s.i.self.team  # указываем полное внешнее DNS-имя
      paths:
        - /                     # определяем путь к корню по этому DNS имени
resources:
nodeSelector: {}
tolerations: []
affinity: {}
```

# Запуск и публикация кода <a name="Deploy"></a> 

1. Запуск для всех частей репозиториев для **staging** проводится в кастомном docker image ***helm_kubectl*** реджистри проекта: ***helm_kubectl:latest***

Код создания docker image образа (в Alpine устанавливаются helm и kubectl):
```dockerfile
ARG BASE_IMAGE
FROM ${BASE_IMAGE:-node:22-alpine} 

# Image Labels
LABEL org.opencontainers.image.vendor="self.team"
LABEL org.opencontainers.image.authors="Alexey Andreychenko <andreychenko@self.team>"
LABEL org.opencontainers.image.title="Docker"
LABEL "com.azure.dev.pipelines.agent.handler.node.path"="/usr/local/bin/node"

# YQ процессор командной строки YAML, JSON, INI и XML 
ENV KUBE_VERSION=1.31.0
ENV HELM_VERSION=3.19.0
ENV YQ_VERSION=4.47.2   

#ARG KUBE_VERSION
#ARG HELM_VERSION
# ARG YQ_VERSION
ARG TARGETOS
ARG TARGETARCH

RUN apk -U upgrade \
    && apk add --no-cache ca-certificates bash shadow sudo git openssh curl gettext jq \
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
CMD [ "node" ]
```

* helm repo add "stable" "https://charts.helm.sh/stable" --force-update - добавляется и принудительно обновляется официальный репозиторий хранилище чартов stable Helm 
* утилита jq нужна для потоковой обработки JSON-файлов

2. Код запуска кластера **Kubernetes**
```bash
    yc config profile create jti
    yc config set service-account-key $(authkey.secureFilePath)  
    export KUBE_TOKEN=$(yc iam create-token) 
    kubectl config set-cluster k8s --server=$(IpK8s) --insecure-skip-tls-verify=true
    kubectl config set-credentials sa-k8s-jti --token="$KUBE_TOKEN"
    kubectl config set-context default --cluster=k8s --user=sa-k8s-jti
    kubectl config use-context default
    

    kubectl create namespace $(Namespace) -o yaml --dry-run=client | kubectl apply -f - || /bin/true
    kubectl create -n $(Namespace) secret docker-registry $(NameSecretDockerRegistry) --docker-server=$(REGISTRY) --docker-username=$(DockerUser) --docker-password=$(DockerPass) --docker-email=admin@self.team -o yaml --dry-run=client | kubectl apply -f - || /bin/true
    kubectl create -n $(Namespace) secret generic $(NameSecret) --from-literal=minio_key=$(MinioKey) --from-literal=minio_secret=$(MinioSecret) -o yaml --dry-run=client | kubectl apply -f - || /bin/true
    kubectl create -n $(Namespace) secret tls tls-secret --cert=$(cert.secureFilePath) --key=$(key.secureFilePath)  

```

* настроиваем подключение к кластеру Kubernetes с пропуском TLS-верификации *—insecure-skip-tls-verify=true*  используется, если используется HTTP поверх HTTPS
* *kubectl config set-credentials admin —token=* - Команда для добавления информации о токене для пользователя *admin* в файл конфигурации kubectl. 
* *kubectl config set-context default --cluster=k8s --user=admin* — установка контекста в конфигурацию Kubernetes. Контекст — это комбинация кластера, пользователя и необязательного пространства имён, которая определяет, как нужно взаимодействовать с кластером. 
* *kubectl config use-context default* - переключение на контекст default. Делаем его текущим, все последующие команды kubectl будут использовать его параметры. 
* *kubectl create namespace ${NAMESPACE} -o yaml --dry-run=client | kubectl apply -f - || /bin/true* - создание неймспейса с выводом в фрмаие yml. Выполняется сухой прогон на стороне клиента, то есть локальная проверка запроса без отправки запросов на сервер. Это помогает быстро проверить корректность команды и убедиться, что она не вызовет ошибок. В случае ошибки терминал вернет нулевой код выхода */bin/true*. 
* *kubectl create -n ${NAMESPACE} ... -o yaml --dry-run=client | kubectl apply -f - || /bin/true* - создание секретов в неймспесе для подключения к реджистри, для подключения к Минио, и сертификат сайта TLS

3. Код запуска приложений:
```bash
helm upgrade --install --wait --timeout 3m ${{ parameters.NAME_HELM }} $(HelmChartPath) -n $(Namespace) -f ${{ parameters.VALUE_FILE }} --set "image.repository=${{ parameters.IMAGE_FULL_PATH }}"
```

ожидаемые переменные:
* ***NAME_HELM*** - имя Helm Charta:
     * ***admin-ui*** - для запуска сервиса *admin-ui*
     * ***admin-api*** - для запуска сервиса *admin-api*     
     * ***portal-ui*** - для запуска сервиса *portal-ui*
     * ***portal-api*** - для запуска сервиса *portal-api*
     * ***magic*** - для запуска сервиса *magic* 
     * ***cache*** - для запуска сервиса *cache* 
     * ***preview*** - для запуска сервиса *preview*
     * ***scheduler*** - для запуска сервиса *scheduler*     
     * ***mongo*** - для запуска БД *Mongo*
     * ***redis*** - для запуска БД *Redis*
* ***NAMESPACE*** - неймспейс кубернетис, может принимать значения в зависимости от ветки:
     * ***test*** - ветка staging
* ***HelmChartPath***  -  - репозиторий helm чарта. 

[Описание Helm чарта тут](#Helm)  
* ***IMAGE_FULL_PATH*** - репозиторий изображения для использования, может принимать значения в зависимости от сервиса или БД
* --set "image.repository=${IMAGE_FULL_PATH}" - указывается образ контейнера
* -f - YML файл для helm для каждого Helm Charta.
* helm upgrade --install - установка (если не установлен) и обновление helm чарта с новыми значениями

# Описание Helm чарта <a name="Helm"></a> 

Структура папок:
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
    ├── pv.yaml
    ├── service.yaml
    ├── _helpers.tpl
    ├── service.yaml
    ├── configmap.yaml
    └── database/
        └── statefulset.yaml
```

Описание:

* Chart.yaml - это основной обязательный файл манифеста чарта. Имя начинается с заглавной буквы.
```YML
apiVersion: v2                             # версия
name: self                                 # имя
description: A Helm chart for Kubernetes   # описание
type: application
version: 1.1.14                            # Версия чарта, соответствует стандарту SemVer2.
appVersion: latest                         # Версия приложения, которое используется в чарте. 
```

* values.yaml - содержит переменные по умолчанию, а также список и описание переменных, которые чарт может ожидать.
```YML
# Количество ReplicaSet
replicaCount: 1
# Какое количество ревизий ReplicaSet хранить от предыдущих деплоев
revisionHistory: 0
# pullPolicy: Always используется в случае тегирования один и тем же тегом, например image:latest
# Значение по-умолчанию: IfNotPresent
image:
  pullPolicy: IfNotPresent
#  repository: registry.self.team
# Имя секрета с настроенным pull-доступом в docker-регистри
imagePullSecrets:
  - name: regcred
# Переменная должна быть установлена в значение true, если приложение
# работает с серверами очередей, наподобие Nats-Streaming-Server или RabbitMQ
# Это определяет стратегию обновления релиза, т.к сервера очередей
# могут отвергнуть соединения от приложения из создаваемого пода, пока работает старый под.
# Эта переменная позволит оборвать соединения старого пода, и только после этого запустит новый под
useQueueServers: false
# Использование файлов конфигураций из configMap
configMap:  # true - если монтируем внешний конфиг приложения, false - если используем конфиг по-умолчанию, или планируем заполнять переменными окружения
  enabled: false
  # имя конфигмапы (уходит в deployment: spec.volumes.name, spec.volumes.name.configMap.name)
command: []
imagePullSecrets: 
  - name: regcred
nameOverride: ""
fullnameOverride: ""
health: false
serviceAccount:  # Specifies whether a service account should be created
  create: true  # The name of the service account to use.
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
  requests:    # задется мин ресурсов, которое гарантировано будет выделено 
    memory: 128Mi
    cpu: 150m  # 150миллиядер процессорного времени (1000 соответствуют одному vCPU).
  limits:
    memory: 256Mi
    cpu: 250m
nodeSelector: {}
tolerations: []
affinity: {}
``` 

Каталог templates/ - обязательный каталог, содержит шаблоны Kubernetes-манифестов — YAML-файлы, которые Helm рендерит с использованием значений из values.yaml и переданных параметров. Здесь находиться манифесты объектов Kubernetes, которые требуются для запуска и работы приложения в кластере.

* NOTES.txt содержит дополнительные инструкции и сообщения, которые воводятся после установки чарта и при просмотре статуса релиза.

Код:
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
  kubectl --namespace {{ .Release.Namespace }} port-forward $POD_NAME 8080:80
{{- end }}
```

* deployment.yaml - развертываются приложения с необходимым количеством реплик

Код:
```YML
{{- if (ne .Values.mode "database") }}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "jti.fullname" . }}
  labels:
    {{- include "jti.labels" . | nindent 4 }}
spec:
  {{- if .Values.strategy }}
  strategy:
    type: {{ .Values.strategy.type }}
  {{- end }}
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "jti.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "jti.selectorLabels" . | nindent 8 }}
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }} # обновление deployment про изменениях в configmap
        rollme: {{ randAlphaNum 5 | quote }}  # автоматическое обновление развертывания при каждом выпуске, генерирует строку 5 символов. При каждом вызове шаблона будет генерироваться строка. 
    spec:
      containers:
        - name: {{ .Values.containerName }}
          image: {{ .Values.image.repository }}
          imagePullPolicy: {{ .Values.image.pullPolicy }}  
          {{- if .Values.command }}
          command: 
            {{- toYaml .Values.command | nindent 12 }}
          {{- end }}
          {{- if .Values.env }}
          env:
            {{- toYaml .Values.env | nindent 12 }}
          {{- end }}
          {{- if .Values.envFrom }}
          envFrom:
          - configMapRef: 
              name: {{ .Values.envFrom.name  }}
          {{- end }}
          {{- if .Values.containerPort }}
          ports:
            {{- toYaml .Values.containerPort | nindent 12 }}
          {{- end }}
          {{- if .Values.volumeMounts }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          {{- end }}
          {{- if .Values.volumeMounts }}
          volumeMounts:
              {{- toYaml .Values.volumeMounts | nindent 12 }}
          {{- end }}
      imagePullSecrets:
        - name: {{ .Values.imagePullSecrets.name }} 
      {{- if .Values.volumes }}  
      volumes:
        {{- toYaml .Values.volumes | nindent 8 }}
        {{- if .Values.configMap.name }}  
        - name: {{ .Values.configMap.name }}
          configMap:
            name: {{ .Values.configMap.name }} 
        {{- end }}  
      {{- end }}
{{- end }}
```

* statefulset.yaml - используется для запуска БД Redis, Mongo

Код:
```YML
{{- if (eq .Values.mode "database") }}
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: {{ include "jti.fullname" . }}
  labels:
    {{- include "jti.labels" . | nindent 4 }}
spec:
  selector:
    matchLabels:
      {{- include "jti.labels" . | nindent 6 }}
  replicas: {{ .Values.replicaCount }}
  {{- if .Values.serviceName }}
  serviceName: {{ .Values.serviceName }}
  {{- end }}
  template:
    metadata:
      labels:
        {{- include "jti.labels" . | nindent 8 }}
    spec:
      {{- if .Values.terminationGracePeriodSeconds }}
      terminationGracePeriodSeconds: {{ .Values.terminationGracePeriodSeconds }}
      {{- end }}
      containers:
        - name: {{ .Values.containerName }}
          image: {{ .Values.image.repository }}
          imagePullPolicy: {{ .Values.image.pullPolicy }}  
          {{- if .Values.command }}
          command: 
            {{- toYaml .Values.command | nindent 12 }}
          {{- end }}
          {{- if .Values.args }}
          args: 
            {{- toYaml .Values.args | nindent 12 }}
          {{- end }}
          {{- if .Values.env }}
          env:
            {{- toYaml .Values.env | nindent 12 }}
          {{- end }}
          {{- if .Values.envFrom }}
          envFrom:
          - configMapRef: 
              name: {{ .Values.envFrom.name  }}
          {{- end }}
          {{- if .Values.containerPort }}
          ports:
            {{- toYaml .Values.containerPort | nindent 12 }}
          {{- end }}
          {{- if .Values.resources }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          {{- end }}
          {{- if .Values.volumeMounts }}
          volumeMounts:
              {{- toYaml .Values.volumeMounts | nindent 12 }}
          {{- end }}
      imagePullSecrets:
        - name:  {{ .Values.imagePullSecrets.name }} 
      {{- if .Values.volume.enabled }}
      volumes:
        {{- if .Values.volumes }}
        - name: {{ .Values.volumes.name }} 
          persistentVolumeClaim:
            claimName: {{ .Values.volumes.claimName }}
            readOnly: {{ .Values.volumes.readOnly }}
        {{- end }}
        {{- if .Values.volumesConfigmaps }}
          {{- toYaml .Values.volumesConfigmaps | nindent 8 }}
        {{- end }}
      {{- end }}
{{- end }}
```

* pvc.yaml - создается ресурс, который представляет запрос на хранилище от модуля. Он  указывает требования к хранилищу, такие как размер, режим доступа и класс хранения. Kubernetes использует PVC, чтобы найти доступный PersistentVolume (PV), который удовлетворяет требованиям PVC. После создания PVC его можно монтировать как том в модуле, и тогда модуль может использовать смонтированный том для хранения и получения данных.

Код:
```YML
{{- if .Values.persistence }}  # значение не определено 
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: {{ .Values.persistence.name }}
  labels:
    {{- include "jti.labels" . | nindent 4 }}
spec:
  {{- if .Values.persistence.accessModes }}
  accessModes: 
    {{- toYaml .Values.persistence.accessModes | nindent 4 }} 
  {{- end }}
  {{- if .Values.persistence.storageClassName }}
  storageClassName: {{ .Values.persistence.storageClassName }}
  {{- end }}
  {{- if .Values.persistence.volumeName }}
  volumeName: {{ .Values.persistence.volumeName }}
  {{- end }}
  resources:
    requests:
      storage: {{ .Values.persistence.size }}     
 {{- end }}
```

* service.yaml - определяется логический набор подов и политика доступа к ним. Набор подов определяется на основе меток (присваиваются в момент создания подов) и селекторов

Код:
```YML
{{- if .Values.service }}
apiVersion: v1
kind: Service
metadata:
  name: {{ include "jti.fullname" . }}
  labels:
    {{- include "jti.labels" . | nindent 4 }}
spec:
  {{- if .Values.service.type }}
  type: {{ .Values.service.type }}
  {{- end }}  
  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.targetPort }}
      protocol: TCP
      name: {{ .Values.service.name }}
  {{- if .Values.clusterIP }}  
  clusterIP: {{ .Values.clusterIP }}  
  {{- end }}    
  selector:
    {{- include "jti.selectorLabels" . | nindent 4 }}
{{- end }}
```

* pv.yaml -  используется для создания статических томов.

Код:
```YML
{{- if .Values.pv }}
apiVersion: v1
kind: PersistentVolume
metadata:
  name: {{ .Values.pv.name }}
  labels:
    {{- include "jti.labels" . | nindent 4 }}
spec:
  {{- if .Values.pv.storageClassName }}
  storageClassName: {{ .Values.pv.storageClassName }}
  {{- end }}
  capacity:
    storage:  {{ .Values.pv.capacity.storage }}
  {{- if .Values.pv.accessModes }}
  accessModes: 
    {{- toYaml .Values.pv.accessModes | nindent 4 }} 
  {{- end }}
  {{- if .Values.pv.claimRef }}
  claimRef: 
    namespace: {{ .Values.pv.claimRef.namespace }}
    name: {{ .Values.pv.claimRef.name }}
  {{- end }}
  csi:
    driver: ru.yandex.s3.csi
    volumeHandle: {{ .Values.pv.volumeHandle }}
    {{- if .Values.pv.controllerPublishSecretRef }}
    controllerPublishSecretRef:
      name: {{ .Values.pv.controllerPublishSecretRef.name }}
      namespace: {{ .Values.pv.controllerPublishSecretRef.namespace }}
    nodePublishSecretRef:
      name: {{ .Values.pv.controllerPublishSecretRef.name }}
      namespace: {{ .Values.pv.controllerPublishSecretRef.namespace }}
    nodeStageSecretRef:
      name: {{ .Values.pv.controllerPublishSecretRef.name }}
      namespace: {{ .Values.pv.controllerPublishSecretRef.namespace }}
    volumeAttributes:
      capacity: {{ .Values.pv.controllerPublishSecretRef.capacity }}
      mounter: geesefs
      options: {{ .Values.pv.controllerPublishSecretRef.options }}
  {{- end }}
{{- end }}
```

* configmap.yaml -  используется для описания данных.

Код:
```YML
{{- if .Values.cm }}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Values.cm.name }}
  labels:
    app.kubernetes.io/name: {{ .Values.cm.name }}
{{- if .Values.cm.data }}
data:
  {{- toYaml .Values.cm.data | nindent 4 }}
{{- end }}
{{- end }}
```

*  _helpers.tpl — утилита для повторного использования кода (для использования применяется **{{-include <имя шаблона> }}**) и управления конфигурацией. Cодержит повторно используемые шаблоны (начинаются с **{{- define <имя шаблона> }}** и заканчивается **{{- end -}}**), вспомогательные функции и общие значения. Для упрощения и повторного использования код в шаблонах чарта, делая их более читаемыми и поддерживаемыми. 
Код:
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

# Заключение <a name="Сonclusion"></a> 

Данное описание написано на языке Markdown.
[Markdown](https://ru.wikipedia.org/wiki/Markdown) (маркдаун) — облегченный язык разметки, созданный с целью написания максимально читаемого и удобного для правки текста, но пригодного для преобразования в языки для продвинутых публикаций (HTML, Rich Text и др.).

Для работы с ним есть множество онлайн-инструментов, в том числе с инструкцией по правильной разметке текста, например: 
* [Dillinger](http://dillinger.io/) — в этом онлайн-редакторе можно на лету форматировать markdown-файлы и смотреть результат визуализации разметки.
                 
Также и GitHub поддерживает автоматическое отображение README.md файлов в формате markdown.

В маркдаун-документацию можно добавлять индекс (оглавление) на внутренние якоря в документе. При этом ссылки в таком оглавлении будут кликабельными, как в обычном html-документе. Это полезно для больших markdown-документов.