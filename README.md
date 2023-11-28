# Recipe searching
Credit to Ryan Lee [Eigth Box. _"Recipe Box"_. 2022](https://eightportions.com/datasets/Recipes/) for scraped recipes that is used in the application database.

I used the best ranked model in [Sentence Transformers (sBERT)](https://huggingface.co/sentence-transformers/multi-qa-mpnet-base-dot-v1) for semantic search.

## Questions
### Your software application idea
### The architecture design decisions in your application
### The business implications of these architecture decisions
### Interaction between different microservices
### Details of your deployment
### Security issues identified and/or mitigated

the frontend and worker(s) will be in python flask and python fastapi. Which ports should be set in these applications to make this work? Im most uncertain for the workers with fastapi as there are multiple workers.