# Argo MLOps: Model Training Demonstration Pipeline

This project provides an example implementation of an MLOps pipeline using **Argo Workflows** and **Argo CD** within a Kubernetes cluster. The project automates the process of synthetic data generation, machine learning model training, and result validation.

## 🚀 Architecture Overview

The project is built according to GitOps principles and is divided into the following stages:

1.  **Data Preparation**: Generation of a synthetic set of logs (information messages vs. errors).
2.  **Training**: Training a logistic regression model using TF-IDF vectorization.
3.  **Orchestration**: Managing steps via a DAG (Directed Acyclic Graph) in Argo Workflows.
4.  **Storage**: Using Persistent Volume Claims (PVC) to pass data and models between pipeline steps.

## 🛠 Technology Stack

- **Language**: Python 3
- **ML Libraries**: `scikit-learn`, `pandas`, `joblib`
- **Orchestration**: Argo Workflows
- **CD**: Argo CD
- **Infrastructure**: Kubernetes, Docker, Helm


## 📁 Project Structure
- `src/`: Source code (generation, training, UI).
- `k8s/`: Kubernetes values. Helm Charts and Workflow definitions.
- `data/`: Local data storage (used during local execution).
- `docker/Dockerfile.train`: Build recipe for the runtime environment.

## 📋 Component Description

### 1. Processing Pipeline
The pipeline is defined in `k8s/argo-pipeline.yaml` and consists of three sequential steps:
- `generate-data`: Runs `generate_data.py`, creating the `dataset.csv` file.
- `train-model`: Runs `train.py`, which reads the data, trains the model, and saves `model.joblib`.
- `validate-metrics`: Checks the contents of the working directory (in this demo version, it executes the `ls -R` command).

### 2. ML Model
- **Task**: Binary classification of text logs (INFO vs ERROR).
- **Method**: TF-IDF Vectorizer $\rightarrow$ Logistic Regression.
- **Result**: Saved model artifact in `.joblib` format.

### 3. Infrastructure Layer
- **Dockerfile.train**: An image containing all necessary dependencies to execute all pipeline stages.
- **PVC (Persistent Volume Claim)**: Provides a shared file system (`/app/data`) for all containers within a single Workflow.
- **Argo App**: Configuration for automatic resource deployment via Argo CD.

## ⚙️ Running Instructions

# Install Argo CD with Helm:
```
helm repo add argo https://argoproj.github.io/argo-helm; helm repo update; helm install argocd argo/argo-cd --create-namespace --namespace argocd --set controller.metrics.enabled=true
```

Patch redis image if unavalible 
```
helm upgrade argocd argo/argo-cd -n argocd --set redis.image.repository=redis --set redis.image.tag=8.2.3-alpine

# after delete pod argo-controller
kubectl delete pod -n argocd -l app.kubernetes.io/name=argocd-application-controller
```

After reaching the UI the first time you can login with username: admin and the random password generated during the installation. You can find the password by running:
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```
Then run kubectl port-forward service/argocd-server -n argocd 8080:443
and then open the browser on http://localhost:8080 and accept the certificate

# Install Argo Workflows with Helm:
curl -L -o argo-workflows.tgz https://github.com/argoproj/argo-helm/releases/download/argo-workflows-1.0.13/argo-workflows-1.0.13.tgz
helm install argo argo-workflows.tgz --namespace argo-workflows --create-namespace --set server.authMode=server

kubectl -n argo port-forward svc/argo-argo-workflows-server 8082:2746 
and then open the browser on http://localhost:8082 and accept the certificate

# RUN Project: 
```bash
curl -L -o root-app.yaml   https://github.com/softaav325/argo-mlops/blob/main/k8s/root-app.yaml
kubectl apply -f root-app.yaml
```
<kbd><img src="images/ArgoCD.jpg" /></kbd>

You can run app in any port 8081 or another:
kubectl port-forward service/ai-service-ui -n ai-service 8081:8080
<kbd><img src="images/App.jpg" /></kbd>

Also you can trane model locally:
<kbd><img src="images/ArgoWorkflowes.jpg" /></kbd>