# Recipe Finder
## What's your next meal?

Recipe Finder helps user to find cooking insperation by using AI to search for relevant recipes in the database, based on the users input.
The user can also add their own recipes to the database.

Credit to Ryan Lee [Eigth Box. _"Recipe Box"_. 2022](https://eightportions.com/datasets/Recipes/) for scraped recipes that is used in the application database.

I used the best ranked model in [Sentence Transformers (sBERT)](https://huggingface.co/sentence-transformers/multi-qa-mpnet-base-dot-v1) for semantic search.

## Questions
### 1. Your software application idea
The Idea is to enable users to search recipes based on plain text that doesn't neccerely need to contain words in the recipies but rather ask for it by desribing high or low level wants/ingredients/cuisine etc.

This is enables by using a simple front-end with 2 user inputs, 1 for searching recipes and one for adding a recipe of their own.

### 2. The architecture design decisions in your application
The application is built as a client-server architecture where the server is resposible for fetching/adding recipes whilst the client is resposible for requesting and displaying the content from the server. The server is a collection of workers that embeds the incoming content and either stores it or uses it to search the stored recipes. The recipes and corresponing vectors are stored in a shared database that the workers share. The frontend has no direct access to the database.

### 3. The business implications of these architecture decisions
As the services (client(s) & server(s)) are decoupled, they can be scaled independently of each-other.

### 4. Interaction between different microservices
### 5. Details of your deployment
### 6. Security issues identified and/or mitigated
As there are no real sensitive information, and the recipes are meant to be publically available I think there is no security issues. They would in that case lie in the content displayed as there is no filters for adding recipes and it could be used store any kind of content.

1. A description of the software you have built and what it does.
2. A software architecture design of your application, describing the role of each component in your system, their responsibilities, and the architecture principles (e.g. cloud architecture patterns) that are used to connect them to a functioning system. This also includes a mapping between software components and the microservices designed and built to implement the components.
3. A discussion of the benefits and challenges with your architecture design. This must include a discussion about security. It must also include a discussion of what you have done or what can be done to mitigate the identified challenges.
4. A link to a configuration management repository (e.g. git) where the source code of the application can be viewed. This must also include the code for your Kubernetes deployment.
