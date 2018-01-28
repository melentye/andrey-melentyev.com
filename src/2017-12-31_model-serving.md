Title: Model serving
Tags: software engineering, machine learning, interoperability
Modified: 2017-12-31 13:55
Status: draft
Summary: After a model is trained, it often needs to be deployed to a different environment than the one used for training. What are some ways of doing that?

Three main types of environments for predictions:

* Offline, batch predictions
* Near real-time, server-side
* Near real-time, client-side

## Scope

In this post, we will consider querying the data sources and feature extraction to be out of scope. That is not how it
works in the real life where before calling a model, additional features may need to be collected. However in practice
those features are usually provided by other systems.

## Functional requirements

* Model serving, i.e. using a trained model for making predictions.
* Model lifecycle management (optional), allowing to deploy multiple versions of the model.
* Advanced features: ensembles, A/B testing and experimentation.

## Non-functional considerations

The task of using a trained model for predictions has a nice property: it doesn't require keeping state, apart from
the model itself which is unlikely to be large (VGG16 is about 540MB big). For the server-side and batch serving use
cases, such a proprty allows designing a horizontally scalable system that supports arbitrary large volumes of
requests per unit of time.

*Latency* of a single prediction may or may not be critical, depending on the use case. Latency should be considered in
the context of the rest of the prediction pipeline, for instance if feature extraction / enrichment takes 10 seconds,
it might not matter if the model execution time is 10ms or 100ms.

Support for all the necessary model formats or *interoperability*.

*Monitoring* of the deployed model is important, from both technical perspective (performance KPIs, error rates,
missing values) and from the model perspective (whether input value and prediction result distributions match the
expectations).

*Deployment* of new models should be a routine task and not different from deploying a change to the source code.
Practices like automated testing and continous delivery are applicable.

Regulatory, fairness, privacy and security requirements go without saying and will heavily depend on the use case.

## Deployment options

* Near real-time predictions
  * Server-side
    * Tensorflow serving. Also [Kubernetes Tensorflow Model Server](https://github.com/google/kubeflow/tree/master/components/k8s-model-server)
    * [MXNet Model Server](https://github.com/awslabs/mxnet-model-server)
    * Clipper
    * H2O REST API
    * Openscoring
    * Spark Streaming
    * Flink
    * Custom web server
      * Wrapping the modelling framework
        * [A flask API for serving scikit-learn models](https://towardsdatascience.com/a-flask-api-for-serving-scikit-learn-models-c8bcdaa41daa)
        * Rserve
      * Transpiling the trained model
    * Deployment infrastructure: containers, clouds, AWS lambda
  * Mobile, client-side
    * Apple CoreML
    * Baidu MDL
    * Google
  * Web, client-side
    * WebAssembly
* Batch predictions
  * Spark

References:

* https://ucbrise.github.io/cs294-rise-fa16/prediction_serving.html
* https://eng.uber.com/michelangelo/