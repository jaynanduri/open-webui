#!/bin/bash

gcloud container clusters get-credentials linkedlens-cluster --region us-east1 --project linkedlens-452503 

docker build . --file ./Dockerfile --tag us-east1-docker.pkg.dev/linkedlens-452503/linkedlens-repo/open-webui:latest

docker push us-east1-docker.pkg.dev/linkedlens-452503/linkedlens-repo/open-webui:latest

kubectl apply -f ./kubernetes/open-webui.yaml

kubectl create serviceaccount openwebui-ksa -n open-webui

kubectl annotate serviceaccount linkedlens-ksa --namespace app iam.gke.io/gcp-service-account=firestoreserviceaccount@linkedlens.iam.gserviceaccount.com

kubectl apply -f ./kubernetes/frontend/deployment.yaml

kubectl apply -f ./kubernetes/frontend/service.yaml

kubectl set serviceaccount deployments open-webui-deployment openwebui-ksa  -n open-webui