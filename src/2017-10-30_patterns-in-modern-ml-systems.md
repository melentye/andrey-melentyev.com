Title: Patterns in modern ML systems
Tags: machine learning, deployment, monitoring, infrastructure, google, uber, klarna
Modified: 2017-10-30 15:57
Status: draft
Summary: Analysis of modern machine learning deployments by Google, Uber and Klarna.

## Main parts

* Data ingestion. Data quality issues can be caused for a number of reasons, including but not limited to code defects, human error or system failures. When it comes to data quality, Spotify Engineering shares their experience in [Data Quality By Engineers, For Engineers]((https://labs.spotify.com/2017/10/17/tc4d-data-quality-by-engineers-for-engineers/) blog post.
* Data analysis. Have a good pre-defined set of statistics calculate for different types of features. Allow defining custom statistics. Visualization matters - https://blog.acolyer.org/2017/10/31/same-stats-different-graphs-generating-datasets-with-varied-appearance-and-identical-statistics-through-simulated-annealing/ 
* Data transformation, aka feature extraction. Feature-to-integer mapping, etc. Important to have the same logic in training and serving time, for example to package it in the trained model.
* Data validation. Use schema to verify that feature matches the necessary data type, fits into min-max values interval or is from a pre-defined set. Provide actionably options to the user: exclude feature, update schema. Can include more specific requirements like a distribution of values. Make sure feature is present in a certain fraction of examples (or in all of them if mandatory). Integrate data validation with bug tracking so that data defects can be treated accordingly.
* Training. Performance improvements: warm start. Usability: high level Feature and Estimator API.
* Model evaluation and validation.

Evaluation (think if model is good from user perspective)

valuate prediction quality on a hold-out dataset.
* Experimentation. Models that show promising performance on the offline A/B test during the evaluation, get to be deployed to production. The purpose of the online A/B test is to tell
how the model is actually performing on relevant business metrics in real life.

Validation (think if model is good from computer perspective)
Canary deployments, validating model's health, i.e. lack of crashes.

Configuration-free validation is nice - teams don't have to set it up.

Slicing is useful - can help detect both validation and evaluation issues which are not significant enough to be noticed on the whole population.

* Model serving. 
* Monitoring, logging, audit


### Sources

1. [TFX: A TensorFlow-Based Production-Scale Machine Learning Platform](http://www.kdd.org/kdd2017/papers/view/tfx-a-tensorflow-based-production-scale-machine-learning-platform)
1. [Meet Michelangelo: Uber’s Machine Learning Platform](https://eng.uber.com/michelangelo/)
1. [Turbocharging Analytics at Uber with our Data Science Workbench](https://eng.uber.com/dsw/)
