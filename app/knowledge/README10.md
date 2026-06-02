Project ART Index 
==============
This is project ART Index with functionality.

***Содержание:***
- [Введение](#Introduction)
- [Оптимизация процесса сборки](#Build)
- [Подготовка Art Estimate Backend](#Preparing-repo-Backend)
     - [Проверка кода сниффором](#Quality_phpcs)
     - [Проверка и анализ кода PHP](#Quality_psalm)    
     - [Публикация репозитория Backend](#Public_Backend)   
- [Подготовка Art Estimate Frontend](#Preparing-repo-Frontend)
- [Подготовка Art Estimate Invest Admin](#Preparing-repo-Admin)  
- [Запуск и публикация кода](#Deploy)
- [Описание Helm чарта](#Helm)
- [Заключение](#Сonclusion)

# Введение <a name="Introduction"></a>

**Project ART Index** — это описание проекта с базовой функциональностью. Проект имеет типовую структуру и сборку в GitlabCI. 
Invest Art разработан с использованием Next.js, React и TypeScript. Приложение позволяет пользователям инвестировать в произведения искусства.
Проект состоит из нескольких частей, описанных на схеме ниже:

!["Общая схема репозиториев"](General_scheme.png "Общая схема репозиториев")

Art Estimate Backend (далее Backend) - содержит код, отвечающий за хранение данных и обработку запросов.
Запуск состоит из этапов, описанных на схеме ниже:

!["Cхема запуска Backend"](BackendPipeline.png "Cхема запуска Backend")

Art Estimate Frontend (далее Frontend) - содержит код внешнего интерфейса веб-сайта и приложений.
Запуск состоит из этапов, описанных на схеме ниже:

!["Cхема запуска Frontend"](FrontendPipeline.png "Cхема запуска Frontend")

Art Estimate Invest Admin (далее Admin) - содержит код Административной панели для управления платформой InvestArt.
Запуск состоит из этапов, описанных на схеме ниже:

!["Cхема запуска Admin"](AdminPipeline.png "Cхема запуска Admin")

* Информация по проекту в jire [ART_Index](https://jira.self.team/browse/AI)
* Информация по проекту в confluence [ART_Index](https://confluence.self.team/display/AI/Art+Index+Home)

# Оптимизация процесса сборки <a name="Build"></a> 

1. Сборка для всех частей репозиториев для **Backend**, **Frontend**, **Admin** проводится в docker image ***Kaniko*** реджистри Google Cloud:  ***gcr.io/kaniko-project/executor:v1.9.2-debug***

2. Сборщик ***Kaniko*** ожидает:
* --dockerfile — файл, содержащий все команды для сборки образа 
* --destination — путь к реестру репозитория, куда будет выгружаться образ
* --context — директорию, в которой Kaniko использует файлы для сборки образа. 
* --build-arg - значения ARG во время сборки

Для ускорения сборки используются параметры ***Kaniko***:
* --cache — активирует кэширование
* --snapshot-mode=redo — при создании снимка файловой системы будут учитываться время последнего изменения файла, его размер, режим, uid и gid владельца. Это может быть на 50% быстрее, чем полный снимок, особенно если в проекте большое количество файлов

Код сборки:
```bash
/kaniko/executor --cache --snapshot-mode=redo --force --context $CI_PROJECT_DIR/${CONTEXT} ${BUILD_ARGS} --build-arg=K8S_ENVIRONMENT --dockerfile ${DOCKERFILE_PATH} --destination ${IMAGE_FULL_PATH}
```

# Подготовка Art Estimate Backend <a name="Preparing-repo-Backend"></a>

1. Документация к проекту должна вестись в файле **README.md** формата **markdown**, который должен располагаться в корне репозитория в каждой ветке. Версионирование и изменения в документацию вносятся как в обычный код, вместе с отдельными комитами в соответствующую ветку. 

## Проверка кода сниффером <a name="Quality_phpcs"></a>

1. Проверка кода осуществляется в собранном контейнере (предыдущий шаг):
```
 ${CI_REGISTRY_IMAGE}/${IMAGE_NAME}:${CI_COMMIT_REF_SLUG}-${CI_COMMIT_SHORT_SHA}
``` 

2. Команда проверки кода с помощью PHP_CodeSniffer выглядит так: 
```bash
php ${APP_DIR}/vendor/bin/phpcs -p -w --colors --standard=${APP_DIR}/phpcs.xml ./src
```

* -p — показывает прогресс выполнения 
* -w — выводит предупреждения и ошибки (по умолчанию)
* --colors — использует цвета в выводе
* --standard — указывается файл со стандартом кодирования
* ./src - директория проверки

## Проверка и анализ кода PHP <a name="Quality_psalm"></a>

1. Проверка кода осуществляется в том же контейнере, описанном выше:

2. Psalm — это инструмент статического анализа для поиска ошибок в PHP-приложениях. Он выполняет продвинутый вывод типов и проверяет различные виды ошибок, включая ошибки типов, неопределённые переменные, некорректные вызовы функций и многое другое. 

Команда проверки кода с помощью PHP_CodeSniffer выглядит так: 
```bash
  php ${APP_DIR}/vendor/bin/psalm  --root=${APP_DIR} --config=${APP_DIR}/psalm.xml
```

* --config - конфигурациооный файл
* --root - корень проекта 

## Публикация репозитория Backend<a name="Public_Backend"></a>

1. Запуск и публикация кода описана тут [Запуск и публикация кода](#Deploy)

2. Код values.yaml:
```YML
replicaCount: 1            # число копий приложения
migration: false           # отключение миграции баз данных
image:
  pullPolicy: IfNotPresent # изображение будет загружено, если оно не существует 
configMap:                 # использование файлов конфигураций из configMap
  enabled: true            # монтируем внешний конфиг приложения
  name: art-app-files      # имя конфигмапы
volumeMounts:              # Определяем пути монтирования  
  - name: art-app-files
    mountPath: /app/src/resources/alfa/self-lab.cer    # сертификат
    subPath: self-lab.cer        # не обновится до перезапуска пода
  - name: art-app-files
    mountPath: /app/src/resources/alfa/self-lab.key     # ключ
    subPath: self-lab.key        # не обновится до перезапуска пода
containerName: art-api-back      # имя контейнера
containerPort: 80                # порт на котором будет доступен контейнер
nameOverride: ""
fullnameOverride: "art-api-back" # переопределяем полное имя диаграммы в Helm
env:                             # тут заданы переменные окружения
serviceAccount:                  # параметры учетной записи сервиса
  create: true                   # создание учетной записи сервиса
  name:
podSecurityContext: {}           # параметры безопасности на уровне пода
securityContext: {}              # параметры безопасности контейнера
service:
  type: ClusterIP                # устанавливаем тип внутрикластерного взаимодействия
  port: 80                       # только внутри кластера по 80 порту
ingress:                         # описываем правила для ingress controllera
  enabled: true                  # включаем ingress
  annotations:
     nginx.ingress.kubernetes.io/proxy-body-size: 256m # максимальный размер запроса 256Мб
  hosts:
    - host: art-api-back.k8s.i.self.team  # указываем полное внешнее DNS-имя контейнера
      paths:
        - /                   # определяем путь к корню по этому DNS имени 
resources:                    # определяем ресурсы для контейнера
  limits:                     # ограничиваем лимит ресурсов
    cpu: 4000m                # максимальная 4 vCPU
    memory: 4Gi               # задаем максимальный объем памяти 1 Гб
  requests:                   # рекомендуемое значение
    cpu: 250m                 # 250 миллиядер процессорного времени (1000 соответствуют одному vCPU)
    memory: 256Mi             # объем памяти 256 Мб
nodeSelector: {}              # для всех node
tolerations: []
affinity: {}
```  

# Подготовка Art Estimate Frontend <a name="Preparing-repo-Frontend"></a>

## Условия запуска Frontend <a name="Launch_conditions_Frontend"></a>

Ниже приведены таблицы запуска сервисов **Frontend** для различных веток с внешними адресами, доступными через web-браузер: 

**front**
|branch ветка            | host адрес                 | api адрес                        |
|:-----------------------|:-------------------------- |--------------------------------- |
|- develop               | www.art.test.self.team     | www.art.test.self.team/api/v1    |
|- preprod               | www.art.preprod.self.team  | www.art.preprod.self.team/api/v1 |
|- master                | www.myinvest.art           | www.myinvest.art/api/v1          |

**tech-work**
|branch ветка            | host адрес                 | api адрес                        |
|:-----------------------|:-------------------------- |--------------------------------- |
|- develop               | www.art.test.self.team     | www.art.test.self.team/api/v1    |
|- preprod               | www.art.preprod.self.team  | www.art.preprod.self.team/api/v1 |
|- master                | www.myinvest.art           | www.myinvest.art/api/v1          |

**Ingosinvest**
|branch ветка | host адрес                             | api адрес                                    |
|:------------|:-------------------------------------- |--------------------------------------------- |
|- develop    | www.art-ingosinvest.test.self.team     | www.art-ingosinvest.test.self.team/api/v1    |
|- preprod    | www.art-ingosinvest.preprod.self.team  | www.art-ingosinvest.preprod.self.team/api/v1 |
|- master     | www.ingosinvest.myinvest.art           | www.ingosinvest.myinvest.art/api/v1          |

**Alfacapital**
|branch ветка | host адрес                            | api адрес                                    |
|:------------|:------------------------------------- |--------------------------------------------- |
|- develop    | www.art-alfacapital.test.self.team    |www.art-alfacapital.test.self.team/api/v1     |
|- preprod    | www.art-alfacapital.preprod.self.team |www.art-alfacapital.preprod.self.team/api/v1  |
|- master     | www.alfacapital.myinvest.art          |www.alfacapital.myinvest.art/api/v1           |

## Публикация репозитория Frontend<a name="Public_Frontend"></a>

1. Запуск и публикация кода описана тут [Запуск и публикация кода](#Deploy)

2. Код values.yaml:
```YML
replicaCount: 1             # число копий приложения
migration: false            # отключение миграции баз данных
image:
  pullPolicy: IfNotPresent  # изображение будет загружено, если оно не существует локально
volume:
  enabled: false              # отключаем создание постоянных томов
containerName: art-front      # имя контейнера
containerPort: 3000           # порт контейнера
nameOverride: ""
fullnameOverride: "art-front" # переопределяем полное имя диаграммы в Helm
env:                          # определяем переменные окружения в контейнере
  - name: APP_NAME
    value: "art-front"
  - name: NEXT_PUBLIC_API_URL
    value: "https://myinvest.art/api/v1"
  - name: NEXT_STAGE_NAME
    value: "prod"
  - name: APP_ENV
    value: "master"
serviceAccount:              # параметры учетной записи сервиса
  create: true               # создание учетной записи сервиса
  name:
podSecurityContext: {}       # параметры безопасности на уровне пода
securityContext: {}          # параметры безопасности контейнера
service:
  type: ClusterIP            # устанавливаем тип внутрикластерного взаимодействия 
  port: 80                   # только внутри кластера по 80 порту
ingress:                     # описываем правила для ingress controllera
  enabled: true              # включаем ingress
  hosts:
    - host: art-front.k8s.i.self.team  # указываем полное внешнее DNS-имя
      paths:
        - /                             # определяем путь к корню по этому DNS имени
resources:                              # определяем ресурсы для контейнера
  limits:                               # определяем лимт     
    cpu: 2000m                          # 2 vCPU
    memory: 1Gi                         # максимальный объем памяти 1 Гб
  requests:        # задется мин ресурсов, которое гарантировано будет выделено
    cpu: 250m      # 250 миллиядер процессорного времени (1000 соответствуют одному vCPU)
    memory: 256Mi  # объем памяти 256 Мб 
nodeSelector: {}   # для всех node
tolerations: []
affinity: {}
```

# Подготовка Art Estimate Invest Admin <a name="Preparing-repo-Admin"></a>

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

1. Запуск для всех частей репозиториев для **Backend**, **Frontend**, **Admin** проводится в кастомном docker image ***helm_kubectl*** реджистри проекта: ***selfteam/k8s-deploy/deploy/helm_kubectl:latest***

Код создания docker image образа (в Alpine устанавливаются helm и kubectl):
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

* helm repo add "stable" "https://charts.helm.sh/stable" --force-update - добавляется и принудительно обновляется официальный репозиторий хранилище чартов stable Helm 
* утилита jq нужна для потоковой обработки JSON-файлов

2. Код запуска кластера **Kubernetes**
```bash
kubectl config set-cluster k8s --server="$KUBE_URL" --insecure-skip-tls-verify=true
kubectl config set-credentials admin --token="$KUBE_TOKEN"
kubectl config set-context default --cluster=k8s --user=admin
kubectl config use-context default
kubectl create namespace ${NAMESPACE} -o yaml --dry-run=client | kubectl apply -f - || /bin/true
kubectl create -n ${NAMESPACE} secret docker-registry regcred --docker-server=registry.self.team --docker-username=k8s-selfteam --docker-password=${K8S_SELFTEAM_PASSWORD} --docker-email=admin@self.team -o yaml --dry-run=client | kubectl apply -f - || /bin/true
kubectl delete -n ${NAMESPACE} jobs.batch app-migrate || true
```

* настроиваем подключение к кластеру Kubernetes с пропуском TLS-верификации *—insecure-skip-tls-verify=true*  используется, если используется HTTP поверх HTTPS
* *kubectl config set-credentials admin —token=* - Команда для добавления информации о токене для пользователя *admin* в файл конфигурации kubectl. 
* *kubectl config set-context default --cluster=k8s --user=admin* — установка контекста в конфигурацию Kubernetes. Контекст — это комбинация кластера, пользователя и необязательного пространства имён, которая определяет, как нужно взаимодействовать с кластером. 
* *kubectl config use-context default* - переключение на контекст default. Делаем его текущим, все последующие команды kubectl будут использовать его параметры. 
* *kubectl create namespace ${NAMESPACE} -o yaml --dry-run=client | kubectl apply -f - || /bin/true* - создание неймспейса с выводом в фрмаие yml. Выполняется сухой прогон на стороне клиента, то есть локальная проверка запроса без отправки запросов на сервер. Это помогает быстро проверить корректность команды и убедиться, что она не вызовет ошибок. В случае ошибки терминал вернет нулевой код выхода */bin/true*. 
* *kubectl create -n ${NAMESPACE} secret docker-registry regcred --docker-server=registry.self.team --docker-username=k8s-selfteam --docker-password=${K8S_SELFTEAM_PASSWORD} --docker-email=admin@self.team -o yaml --dry-run=client | kubectl apply -f - || /bin/true* - создание секрета в неймспесе для подключения к реджистри.
* *kubectl delete -n ${NAMESPACE} jobs.batch app-migrate || true* - удаление ресурсов из неймспейса jobs.batch app-migrate.

3. Код запуска приложений:
```bash
helm upgrade --install --wait --timeout 10m ${APP}${WORKER}-${CI_COMMIT_REF_SLUG} -n ${NAMESPACE} ${HELM_CHART_URL} -f k8s/values.yaml --set "image.repository=${IMAGE_FULL_PATH}"
```

ожидаемые переменные:
* ***APP*** - может принимать значения в зависимости от репозитория:
     * ***art-api-back*** - для репозитория *backend*
     * ***art-investadmin*** - для репозитория *admin*     
     * ***art-front*** - для репозитория *frontend*
     * ***art-front-tech-work*** - для репозитория *frontend*
     * ***art-front-ingosinvest*** - для репозитория *frontend* 
     * ***art-front-alfacapital*** - для репозитория *frontend* 
* ***WORKER*** - принимает значение ***-cron*** в репозитории *backend* для **deploy:worker:cron:**
* ***CI_COMMIT_REF_SLUG*** - уникальный идентификатор ветки 
* ***NAMESPACE*** - неймспейс кубернетис, может принимать три значения в зависимости от ветки:
     * ***art-estimate-preprod*** - ветка preprod
     * ***art-estimate-test*** - ветка test
     * ***art-estimate*** - ветка master
* ***HELM_CHART_URL***  - *https://${CI_SERVER_HOST}/api/v4/projects/78/repository/archive.tar.gz?private_token=${K8S_SELFTEAM_HELM_TOKEN}* - репозиторий helm чарта. 
[Описание Helm чарта тут](#Helm)  
* ***IMAGE_FULL_PATH*** - репозиторий изображения для использования, может принимать значения в зависимости от текущего репозитория:
Для **Backend**: 
  * ***art-api-back-cron:tag***
  * ***art-api-back:tag***
Для **Admin**:
  * ***art-investadmin:tag***
Для **Frontend**:
  * ***art-front-tech-work:tag***
  * ***art-front-alfacapital:tag***
  * ***art-front-ingosinvest:tag***
  * ***art-front:tag***
* --set "image.repository=${IMAGE_FULL_PATH}" - указывается образ контейнера, перечислены выше 
* -f - YML файл для helm для каждого репозиторя [Backend](#Public_Backend), [Frontend](#Preparing-repo-Frontend), [Admin](#Preparing-repo-Admin) описаны выше.
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
    ├── service.yaml
    ├── _helpers.tpl
    ├── serviceaccount.yaml
    └── tests/
        └── test-connection.yaml
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
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace {{ .Release.Namespace }} port-forward $POD_NAME 8080:80
{{- end }}
```

Например вывод для **Admin** (ветка ***develop***) выглядить так:
```
1. Get the application URL by running these commands:
  http://dev.artinvestadmin.app/
  http://art-invest-admin-dev.k8s.i.self.team/
```

* deployment.yaml - развертываются приложения с необходимым количеством реплик

Код:
```YML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "self.fullname" . }}  
  labels:
    {{- include "self.labels" . | nindent 4 }}
spec:
  {{- if .Values.useQueueServers }} # по умолчанию задано значение false так как сервер очередей не используется
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

* ingress.yaml - описываем объект, который управляет внешним доступом к службам, запущенным в кластере. Он действует как обратный прокси и балансировщик нагрузки, направляя внешний HTTP- и HTTPS-трафик к различным службам внутри кластера.

Код:
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
  ingressClassName: nginx # указываем класс используемого ingress-контроллера nginx. 
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

* pvc.yaml - создается ресурс, который представляет запрос на хранилище от модуля. Он  указывает требования к хранилищу, такие как размер, режим доступа и класс хранения. Kubernetes использует PVC, чтобы найти доступный PersistentVolume (PV), который удовлетворяет требованиям PVC. После создания PVC его можно монтировать как том в модуле, и тогда модуль может использовать смонтированный том для хранения и получения данных.

Код:
```YML
{{- if .Values.pvc }} # значение не определено 
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: {{ .Values.pvc.name }}
  labels:
    {{- include "self.labels" . | nindent 4 }}
spec:
  accessModes:
  - ReadWriteMany  # режим чтения/записи в одно хранилище для совместной работы подов
  resources:
    requests:
      storage: {{ .Values.pvc.storage }} 
  storageClassName: nfs
{{- end }}
```

* service.yaml - определяется логический набор подов и политика доступа к ним. Набор подов определяется на основе меток (присваиваются в момент создания подов) и селекторов

Код:
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

* serviceaccount.yaml -  всё общение между компонентами кластера идёт через запросы к API-серверу, и каждый такой запрос авторизуется токеном. Этот токен автоматически генерируется при создании объекта типа **ServiceAccount** и кладётся в secret. Чтобы дать больше разрешений приложению или настроить индивидуальный контроль, создается сервис аккаунт для приложения. При запуске контейнеров пода в них будет смонтирован секрет с токеном от этого сервис аккаунта.

Код:
```YML
{{- if .Values.serviceAccount.create -}}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{ include "self.serviceAccountName" . }}  # указываем имя сервис аккаунта 
  labels:
{{ include "self.labels" . | nindent 4 }}
{{- end -}}
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