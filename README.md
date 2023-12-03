# Recipe Finder
## What's your next meal?

Recipe Finder helps user to find cooking insperation by using AI to search for relevant recipes in the database, based on the users input.
The user can also add their own recipes to the database.

Credit to Ryan Lee [Eigth Box. _"Recipe Box"_. 2022](https://eightportions.com/datasets/Recipes/) for scraped recipes that is used in the application database.

I used the best ranked model in [Sentence Transformers (sBERT)](https://huggingface.co/sentence-transformers/multi-qa-mpnet-base-dot-v1) for semantic search.

## Deployment
### [OPTIONAL] Populate database
* this requires some packages to be installed.
```bash
$ docker run -d -p 6379:6379 -p 8001:8001 -v $(pwd)/data/redis:/data redis/redis-stack:latest
$ cd shared_database/
$ python redis_populate.py
```

### Configuration
Start by changing the `recipe-deployment.yaml` volumes' hostPaths to where you store your redis `dump.rdb` for `data-pv` and `sentence-transformers_multi-qa-mpnet-base-dot-v1` for `model-pv`.

### Deploy
Start the local-registry:
```bash
$ docker run -d -p 5000:5000 --name local-registry registry:2
```
Build the images:
```bash
$ docker compose build
```
Push the images to the local-registry:
```bash
$ docker compose push
```
Deploy the application:
```bash
$ kubectl apply -f recipe-deployment.yaml
```

or alternative:
```bash
$ docker compose up
```

### Delete
To delete the deployment:
```bash
$ kubectl delete --cascade='foreground' -f recipe-deployment.yaml
```

## Questions
### 1. Your software application idea
The Idea is to enable users to search recipes based on plain text that doesn't neccerely need to contain words in the recipies but rather ask for it by desribing high or low level wants/ingredients/cuisine etc.

This is enables by using a simple front-end with 2 user inputs, 1 for searching recipes and one for adding a recipe of their own.

### 2. The architecture design decisions in your application
__Horizontally Scaling Compute Pattern__

The application is built as a client-server architecture where the server is resposible for fetching/adding recipes whilst the client is resposible for requesting and displaying the content from the server. The server is a collection of workers that embeds the incoming content and either stores it or uses it to search the stored recipes. The recipes and corresponing vectors are stored in a shared database that the workers share. The frontend has no direct access to the database.

### 3. The business implications of these architecture decisions
As the services (client(s) & server(s)) are decoupled, they can be scaled independently of each-other. As the server(s) / workers are doing somewhat heavy computing compared to the client / frontend, this scalability enables higher troughput / faster response times for the end-user.

### 4. Interaction between different microservices
#### 4.1 Searching recipes
The frontend-service, takes the user input and makes a get request to the worker-service where one worker container uses its AI model to embed the user-input and search the redis database that the worker is connected to.

#### 4.2 Posting new recipe
The frontend-service takes the new-recipe form and makes a post request to the worker-service where one worker container embedds it and adds it to the redis database.

### 5. Details of your deployment
My kubernetes deployment contain this data:
* 1 config-map that contains a json file object containing the urls for the services.
* 2 persistentVolume(Claim) pairs that contain the database data and the AI models for the workers.
    * The models are in a volume because 1. the models dont have to be downloaded twice, 2. the worker-services share the volume so no extra space for multiple models instances occour.

These services:
* frontend-service : LoadBalancer exposing the frontend-deployments
* worker-service : ClusterIP for internal routing to worker-deployments
* database-service : ClusterIP for internal routing to database-deployments

These deployments:
* frontend-deployments : exposes the container for frontend-image and mounts the config-map to that container.
* worker-deployments : sets 3 replicas for workers and mounting the config-map and model-pvc to each.
* database-deployments : exposes the container for redis/redis-stack and mounts the data-pvc containing the database content to that container.

These images:
* frontend-image : python flask running with gunicorn for a frontend webGUI.
* worker-image : pytorch (python) restAPI with python fastAPI that runs the AI model and handles the database.
* redis/redis-stack : the redis database.


### 6. Security issues identified and/or mitigated
As there are no real sensitive information, and the recipes are meant to be publically available I think there is no security issues. They would in that case lie in the content displayed as there is no filters for adding recipes and it could be used store any kind of content. This is also the case for bing volumes with hostPath, which I have done so that the models / data can be re-used and/or transfered to another host. Binding a volume to hostPath makes the host vurnable to data being injected to the host aswell as the containers that mounts the volume. In a real setting, you wouldn't bind the hostPath to the volumes but rather let those spin. The are mainly done as is now because of the long download time for the models and the example data I obtained (credit to _Ryan Lee_)