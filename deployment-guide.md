1. Test django (0. login )

```
python manage.py test
```

2. Build container

```
docker build -f Dockerfile -t registry.digitalocean.com/rso-vaje/service-user:latest .
docker build -f Dockerfile -t registry.digitalocean.com/rso-vaje/service-user:v1 .
```

3. Push Container with 2 tags: latest and random

```
docker push registry.digitalocean.com/rso-vaje/service-user --all-tags
```

4. Update secrets (if needed)

```
kubectl delete secret django-k8s-user-prod-env
kubectl create secret generic django-k8s-user-prod-env --from-env-file=.env.prod
```

5. Update Deployment `k8s/apps/django-k8s-user.yaml`:

Add in a rollout strategy:


`imagePullPolicy: Always`

Change 
```
image: registry.digitalocean.com/rso-vaje/service-user:latest
```
to

```
image: registry.digitalocean.com/rso-vaje/service-user:v1 
```
Notice that we need `v1` to change over time.


```
kubectl apply -f k8s/apps/django-k8s-user.yaml
```

6. Roll Update:

Wait for rollout to finish
```
kubectl rollout status deployment/service-user-deployment
```
7. Migrate database

Get a single pod (either method works)

```
export SINGLE_POD_NAME=$(kubectl get pod -l app=service-user-deployment -o jsonpath="{.items[0].metadata.name}")
```
or 
```
export SINGLE_POD_NAME=$(kubectl get pod -l=app=service-user-deployment -o NAME | tail -n 1)
```

Then run `migrate.sh` 

```
kubectl exec -it $SINGLE_POD_NAME -- bash /app/migrate.sh