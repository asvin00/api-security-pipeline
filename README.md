# DevSecOps CI/CD Pipeline on AWS (Python App)

## Project Overview

This project demonstrates an end-to-end DevSecOps pipeline using AWS and Kubernetes.  
It automates build, test, security scanning, containerization, and deployment of a Python application.

---

## Architecture
<img width="1130" height="450" alt="image" src="https://github.com/user-attachments/assets/03bfb35c-9512-4dc3-b824-8a4782d69781" />

---

## Tech Stack

- AWS CodePipeline (CI/CD)
- AWS CodeBuild (Build & Test)
- AWS ECR (Container Registry)
- AWS EKS (Kubernetes)
- Docker
- Python (Flask)
- pytest
- Trivy and Bandit
- SNS (Notifications)

---

## Project Structure

```bash
python-devsecops/
│── app/
│   └── app.py
│── tests/
│   └── test_app.py
│── Dockerfile
│── requirements.txt
│── deployment.yaml
│── service.yaml
│── buildspec.yml
│── architecture.png
│── README.md
```
Setup Instructions:

1. Clone Repository
```bash
git clone https://github.com/asvin00/python-devsecops.git
cd python-devsecops
```
2. Run Application Locally
```bash
pip install -r requirements.txt
python run.py
```
Open in browser:
```
http://localhost:5000
```

3. Run Tests
```
pytest
```
4. Build Docker Image
```
docker build -t python-devsecops .
```
5. Configure AWS
```
aws configure
```
6. Push Image to ECR
```
docker tag python-devsecops:latest <account-id>.dkr.ecr.ap-south-1.amazonaws.com/python-devsecops:latest
```
```
docker push <account-id>.dkr.ecr.ap-south-1.amazonaws.com/python-devsecops:latest
```
7. Create EKS Cluster
```
eksctl create cluster \
  --name devsecops-cluster \
  --region ap-south-1 \
  --node-type t3.medium \
  --nodes 2
```
- wait for nearly 45 minutes.

8. Configure Kubernetes
```
aws eks update-kubeconfig --region ap-south-1 --name devsecops-cluster
```
9. Deploy Application
```
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```
10. Verify Deployment
```
kubectl get pods
kubectl get svc
```
<img width="1685" height="84" alt="image" src="https://github.com/user-attachments/assets/11ef4280-e110-4a92-8ebc-8c735a357366" />

- Open the EXTERNAL-IP in browser.

11. Setup CodeBuild

- Go to AWS Console → CodeBuild → Create Project

- Configure Source:
```
- Source provider: GitHub
- Repository: Select your repository
- Branch: main
```
- Environment Configuration:
```
- Environment image: Managed image
- OS: Amazon Linux 2
- Runtime: Standard
- Image: aws/codebuild/amazonlinux2-x86_64-standard:5.0
- Privileged mode: Enabled (required for Docker)
```
- Service Role:
```
- Create new role or use existing with:
  - ECR access
  - EKS access
  - S3 access
```
- Buildspec:
```
- Use `buildspec.yml` from repository
```
- Logs:
```
- Enable CloudWatch logs
```
- Create Build Project

12. Setup CodePipeline

- Go to AWS Console → CodePipeline → Create Pipeline

- Pipeline Settings:
```
- Pipeline name: devsecops-pipeline
- Service role: Create new role
- Artifact store: Default S3
```
- Add Source Stage:
```
- Source provider: GitHub
- Connect your GitHub account
- Repository: Select your repo
- Branch: main
```
- Add Build Stage:
```
- Build provider: CodeBuild
- Select previously created CodeBuild project
```
- Add Deploy Stage (Optional if handled in buildspec):
```
- You can skip this if deployment is done via `kubectl` in buildspec.yml
```

- Review and Create Pipeline


13. Trigger Pipeline

```bash
git add .
git commit -m "Trigger pipeline"
git push origin main
```
