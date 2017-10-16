Title: Model interoperability
Tags: machine learning, interoperability, keras, xgboost, sklearn, lightgbm, catboost, spark, theano, tensorflow, pytorth, dl4j, coreml, nnvm, onnx, pmml
Modified: 2017-10-14 17:54
Status: draft
Summary: How the trained models can be persisted and reused across libraries and environments.

The post will describe how the **trained models** can be persisted and reused across machine learning **libraries**
and **environments**, i.e. how they can *interoperate*.
To be more specific, let's first introduce some definitions: a *trained model* is an artefact produced by the machine
learning algorithm as part of training which can be used for inference. *Library* refers to a software package like
scikit-learn or Tensorflow. An *environment* is roughly speaking a combination of hardware and operating system. We
will distinguish between training and inference environments. An example of a training environment is a data
scientist's MacBook running macOS, and an inference environment could be a production server in the cloud.

There are multiple cases when model interoperability is important:

* The *training environment* is different from the *inference environment*, and the library used for modelling is
  not available in the latter. For example, the model is trained with distributed Tensorflow on a cluster with a
  hundred GPUs then needs to be executed on an iPhone.
* There are strict requirements to the inference latency, and the language or library used for training is not
  performant enough.
* The company is organized in such a way that the features and the model are developed by one team, and deployed by
  another team which prefers another language or library.

In this article, we will explore various options of model interoperability, look at the model interchange formats,
including those provided by machine learning libraries, natively in programming languages and designated interchange
formats. We'll briefly touch upon Apple CoreML, Baidu MDL, NNVM and the kinds of models they support.

[TOC]

## Machine learning libraries

This section gives an overview of the ML library interoperability features.

### scikit-learn

[scikit-learn](http://scikit-learn.org/)'s recommended way of model persistence is to use
[Pickle]({filename}/2017-10-14_model-interoperability.md#other-python-libraries). The alternative is the `sklearn.externals.joblib`
module with `dump` and `load` functions which may be more efficient. Refer to
[the documentation](http://scikit-learn.org/stable/modules/model_persistence.html) for a code example.
Such a persisted model cannot be directly used by other libraries but can be deployed to an inference environment
if it happens to be able to run Python.

Linear and logistic regression, SVM, tree models and some of the preprocessing transformers can be converted to the
[CoreML]({filename}/2017-10-14_model-interoperability.md#apple-coreml) format.

[sklearn-porter](https://github.com/nok/sklearn-porter) allows transpiling trained scikit-learn models into C, Java, JavaScript
and other languages. [Scikit-Learn Compiled Trees](https://github.com/ajtulloch/sklearn-compiledtrees/) creates C++ code
for sklearn decision trees and ensembles but hasn't been updated for 11 months at the time of writing.

There's a [sklearn2pmml](https://github.com/jpmml/sklearn2pmml) library by Openscoring.io team that allows exporting
scikit-learn models to [PMML]({filename}/2017-10-14_model-interoperability.md#predictive-model-markup-language-pmml).
It is implemented as a Python wrapper around
[a Java library](https://github.com/jpmml/jpmml-sklearn) and it is somewhat unclear which types of sklearn models are supported.
It is also worth noting that Openscoring.io software is distributed under a viral
[GNU Affero General Public License](https://tldrlegal.com/license/gnu-affero-general-public-license-v3-(agpl-3.0)).

### XGBoost

[XGBoost](https://xgboost.readthedocs.io/en/latest/) gradient boosted decision trees library core is written in C++
with APIs available for Python, R, Java and Scala. Model saving and loading is done into a library-specific format
and is offered via a pair of methods, there are examples
[in Python](http://xgboost.readthedocs.io/en/latest/python/python_intro.html#training) and
[in R](http://xgboost.readthedocs.io/en/latest/R-package/xgboostPresentation.html#save-and-load-models).
Because the model persistence logic is delegated to the library core, an XGB model trained in R or Python can then be exported
and loaded into an XGB inference module written in a different, possibly more performant language such as C++:

![XGBoost language interoperability]({attach}static/images/xgboost-languages.png)

XGBoost models can be converted to [Apple CoreML]({filename}/2017-10-14_model-interoperability.md#apple-coreml)
using [coremltools](https://github.com/apple/coremltools).

Models can also be converted to [PMML]({filename}/2017-10-14_model-interoperability.md#predictive-model-markup-language-pmml)
using [jpmml-xgboost](https://github.com/jpmml/jpmml-xgboost) by Openscoring.io.

### LightGBM

[LightGBM](https://github.com/Microsoft/LightGBM) is another popular decision tree gradient boosting library, created
by Microsoft. Just like XGBoost, its core is written in C++ with APIs in R and Python. Code examples
[in R](https://github.com/Microsoft/LightGBM/blob/master/R-package/demo/basic_walkthrough.R) and
[Python](https://github.com/Microsoft/LightGBM/blob/master/tests/python_package_test/test_basic.py) show how to save and
load models into the LightGBM internal format.

LightGBM models can be converted to [PMML]({filename}/2017-10-14_model-interoperability.md#predictive-model-markup-language-pmml)
using [jpmml-lightgbm](https://github.com/jpmml/jpmml-lightgbm) by Openscoring.io.

### CatBoost

[CatBoost](https://tech.yandex.com/catboost/doc/dg/concepts/about-docpage/) is a library by
[Yandex](https://en.wikipedia.org/wiki/Yandex) implementing gradient boosting on decision trees. It features C++ core, Python,
R and command-line interfaces.

In R, built-in serialization in RDS [won't work](https://github.com/catboost/catboost/issues/91) for CatBoost models but
there are [save_model](https://tech.yandex.com/catboost/doc/dg/concepts/r-reference_catboost-save_model-docpage/)
and [load_model](https://tech.yandex.com/catboost/doc/dg/concepts/r-reference_catboost-load_model-docpage/) methods cover
the have you covered.

CatBoost Python package has a familiar pair of methods
[to save](https://tech.yandex.com/catboost/doc/dg/concepts/python-reference_catboost-docpage/#save_model)
the model and to [load it back](https://tech.yandex.com/catboost/doc/dg/concepts/python-reference_catboost-docpage/#load_model).
Python API also supports saving trained CatBoost models to 
[Apple CoreML]({filename}/2017-10-14_model-interoperability.md#apple-coreml) format:

    :::python
    import catboost
    from sklearn import datasets

    wine = datasets.load_wine()
    cls = catboost.CatBoostClassifier(loss_function='MultiClass')

    cls.fit(wine.data, wine.target)
    cls.save_model("wine.mlmodel",
                   format='coreml',
                   export_parameters={'prediction_type': 'probability'})

produces a CoreML model

    :::shell
    $ file wine.mlmodel
    wine.mlmodel: PDP-11 pure executable not stripped - version 101

that can later be imported into a macOS or iOS app.

### Spark MLLib

Starting from Spark 1.6, MLLib transformers and models can be persisted and later loaded.

MLLib Pipeline API also has
[export/import functionality](https://docs.cloud.databricks.com/docs/spark/1.6/examples/ML%20Pipeline%20Persistence.html)
which requires every component of the pipeline to implement the save/load methods.

Spark has [PMML export feature](https://spark.apache.org/docs/latest/mllib-pmml-model-export.html) for linear, ridge and
lasso regression models, k-means clustering, SVM and binary logistic regression models.

### Theano

Theano recommends [Pickle]({filename}/2017-10-14_model-interoperability.md#other-python-libraries) model serialization for short-term
storage and [offers advice](http://deeplearning.net/software/theano/tutorial/loading_and_saving.html) on long-term
storage.

As for the production deployments, a custom solution with Theano packaged in a Docker container is possible, although
that would still require having a C++ compiler in the container. There are some more
[bits of advice](https://github.com/Theano/Theano/issues/2271) on Theano issue tracker but it's unlikely we will see
more on this now that the library's development is discontinued.

### Tensorflow

Offers a language-agnostic [SavedModel](https://www.tensorflow.org/programmers_guide/saved_model) format, meaning that
you can store a model trained with Tensorflow Python package and then load it from the C++ API. The format uses
[Google Protocol Buffers](https://developers.google.com/protocol-buffers/) for schema definition, kind of a logical
step for Tensorflow being a Google product.

The logical choice for serving Tensorflow models server-side would be
[Tensorflow Serving]({filename}/2017-10-14_model-interoperability.md#tensorflow-serving). For edge devices, trained
model can be converted to the CoreML format and deployed as part of a macOS or iOS app.

### Keras

[Keras](https://keras.io/) is a deep learning library written by [François Chollet](https://twitter.com/fchollet) in
Python, it provides high-level abstractions for building neural network models. It allows defining the network
architecture in clean and human-readable code and it delegates the actual training to Theano, Tensorflow or CNTK.

Keras documentation [recommends using its built-in method of model persistence](https://keras.io/getting-started/faq/#how-can-i-save-a-keras-model)
which gives the user a choice of storing both the neural network architecture and the trained weights, or just one of
the two components. Keras uses [HDF5](https://hdfgroup.org/HDF5/) format popular in the scientific applications.

[Here's a good guide](https://tensorflow.rstudio.com/keras/articles/faq.html#how-can-i-save-a-keras-model) on how to
persist Keras models in R.

From interoperability viewpoint, Keras takes a special place because it allows using the same model training code and
architecture across Theano, Tensorflow and CNTK. That works as long as the user does not utilize the underlying
framework’s API directly, which is also a valid Keras use case! As for the trained weights, they can also be saved
and loaded across Keras backends,
[some restrictions apply](https://github.com/fchollet/keras/wiki/Converting-convolution-kernels-from-Theano-to-TensorFlow-and-vice-versa)

### PyTorch

Like Keras supports exporting the entire model or just the parameters as documented [here](http://pytorch.org/docs/master/notes/serialization.html).
The implementation uses [Python Pickle]({filename}/2017-10-14_model-interoperability.md#other-python-libraries) under
the hood.

### Deeplearning4j

[Deeplearning4j](https://deeplearning4j.org/), as the name suggests, is a deep learning library for Java. The underlying
computation is not done in JVM but rather written in C and C++. It has an additional Keras API and
[can import](https://deeplearning4j.org/model-import-keras) trained Keras models allowing to chose between
importing just the model architecture from `.json` file and importing a model together with weights from the `.h5`.
Once loaded into DL4J, a model can be further trained or deployed into an inference environment for predictions.

DL4J also has its own [model persistence format](https://deeplearning4j.org/modelpersistence). Later in 2017, a direct
import of Tensorflow models is planned (right now it is only possible to import a Tensorflow model if it is created in
Keras).

### Other R libraries

For those R libraries that don't offer their own way of saving and loading models, R offers object
serialization/deserialization using
[saveRDS/readRDS](https://stat.ethz.ch/R-manual/R-devel/library/base/html/readRDS.html)
or [save](https://stat.ethz.ch/R-manual/R-devel/library/base/html/save.html)/
[load](https://stat.ethz.ch/R-manual/R-devel/library/base/html/load.html).
The resulting format while being available to all R users is not scoring too high on the interoperability scale.

R models can nevertheless be deployed server-side by utilizing [Rserve](https://www.rforge.net/Rserve/). A setup with
a thin web service on top of Rserve is known to work well in practice, web service and Rserve can be optionally
containerized. A REST interface for the model is then exposed from the web service which can be implemented in Java,
C, C++ or another language supporting Rserve.

![Exposing R model with Rserve]({attach}static/images/rserve-deployment.png)

Library-specific save/load feature should normally be preferred since the serialized R object might not have all
the necessary data or may have some extra data that is not necessary for storing a trained model.

### Other Python libraries

Python's built-in persistence model, an analogue of the R object serialization, is called
[Pickle](https://docs.python.org/3/library/pickle.html). scikit-learn has a
[concise code snippet](http://scikit-learn.org/stable/modules/model_persistence.html#persistence-example)
showing the usage of Pickle to save and load the model.

Pickled models can be easily served by a Python-based web app.
Here's a [guide on how to do it with Flask](https://medium.com/towards-data-science/a-flask-api-for-serving-scikit-learn-models-c8bcdaa41daa),
a lightweight web application framework for Python.

![Exposing sklearn model with Flask]({attach}static/images/sklearn-flask-deployment.png)

Note that pickling might not be a suitable approach for long-term model storage, due to the fact that it doesn't store
classes, only their instances. Therefore it may not be possible to deserialize a model trained by an older version of
a library using a newer one. Model persistence functionality provided by the machine learning library is preferable
when exists.

## Inference time software packages

### Tensorflow Serving

[Tensorflow Serving](https://www.tensorflow.org/serving/) is a product whose purpose is, unsurprisingly, to serve
Tensorflow models. It exposes a [gRPC](https://grpc.io/) endpoint that can be deployed into production infrastructure
and be called by other components that need to run machine learning models.

It also supports model versioning,

Tensorflow Serving is not limited to Tensorflow models and can be tailored to execute arbitrary model code while
providing nice abstractions around it. Such a custom model needs to have a wrapper written in C++ called
[Servable](https://www.tensorflow.org/serving/custom_servable).
It is a viable alternative for production deployments of any machine learning models, especially if your organization
is service-oriented and has experience integrating gRPC endpoints. A possible usage scenario could be a low latency
deployment of a trained XGB model where Tensorflow Serving uses a custom servable:

![Tensorflow Serving XGB model]({attach}static/images/xgb-tf-serving.png)

On the figure above, XGBoost Servable is something that the developer will have to come up with - Tensorflow Serving
allows that and XGBoost offers a C++ API.

### Apple CoreML

Apple has recently released [CoreML](https://developer.apple.com/documentation/coreml) - a framework for *running*
trained machine learning models on iOS and macOS. In contrast to the libraries mention above, CoreML
itself can't be used for training models. It is shipped with a set of pre-trained models for computer vision and
natural language processing tasks. Models trained using other libraries can be converted into the CoreML `.mlmodel`
format. It is a binary format using [Google Protocol Buffers](https://developers.google.com/protocol-buffers/) to
describe the schema and with a [publicly available specification](https://apple.github.io/coremltools/coremlspecification/index.html).
A great thing about building on top of Protocol Buffers is that they have support for virtually all major programming
languages.

The introductory [WWDC 2017 presentation on CoreML](https://developer.apple.com/videos/play/wwdc2017/703/) lists the supported
by CoreML conversion tool ML libraries. The following libraries are supported: Caffe and Keras for neural nets
(only outdated major versions at the time of announcement), scikit-learn and XGBoost for tree ensembles,
[LIBSVM](http://www.csie.ntu.edu.tw/~cjlin/libsvm/) and scikit-learn for SVM and some more models from scikit-learn.

![CoreML supported model formats]({attach}static/images/coreml-formats.png)

There's a page explaining
[how to convert a model into the CoreML format](https://developer.apple.com/documentation/coreml/converting_trained_models_to_core_ml)
and the conversion [coremltools](https://github.com/apple/coremltools) themselves are open source.

Unofficial [MXNet to Core ML converter tool](https://github.com/apache/incubator-mxnet/tree/master/tools/coreml) is available,
refer to [Bring Machine Learning to iOS apps using Apache MXNet and Apple Core ML](https://aws.amazon.com/blogs/ai/bring-machine-learning-to-ios-apps-using-apache-mxnet-and-apple-core-ml/?sc_channel=sm&sc_campaign=AI_Blog&sc_publisher=TWITTER&sc_country=Global&sc_geo=GLOBAL&sc_outcome=awareness&trk=_TWITTER&sc_content=MXNet&sc_category=MXNet&linkId=42887519)
to get started.

Interesting to see that Apple decided not to support PMML as one of the import formats.

### Baidu Mobile Deep Learning

Baidu's [MDL](https://github.com/baidu/mobile-deep-learning) is a new kid on the block, similar to Apple CoreML,
it is a library for deploying deep learning models to mobile devices with support for iOS and Android. Models trained in
[PaddlePaddle](https://github.com/PaddlePaddle/Paddle) and Caffe can be converted into MDL format.

### Clipper

[Clipper](http://clipper.ai/) is a prediction serving system by UC Berkeley
[RISE Lab](https://rise.cs.berkeley.edu/). It allows deploying models as microservices with
[REST](https://en.wikipedia.org/wiki/Representational_state_transfer) interfaces that can be invoked by other systems
within the IT landscape of the organization. For example, a rules engine may call out to a feature service to fetch the
variables and then call Clipper for inference. Clipper's is similar to Tensorflow Serving:

* Have the same purpose.
* Both offer model versioning.
* Both written in C++.
* Both offer containerized deployments with Docker.

with some differences:

* TF Serving only serves TF models by default, other models need custom support. Clipper supports Python functions,
  R models, PySpark models and users can add custom support for other models as well.
* Clipper exposes REST API while TF Serving has gRPC. That matters if there are strict requirements for low latency,
  in this case gRPC will likely
  [perform](https://blog.gopheracademy.com/advent-2015/etcd-distributed-key-value-store-with-grpc-http2/)
  [better](https://cloud.google.com/blog/big-data/2016/03/announcing-grpc-alpha-for-google-cloud-pubsub).
* Clipper offers model selection and ensembling.
* TF Serving supports batching of predictions for better throughput.

### NNVM

While this post was being written, AWS
[announced NNVM](https://aws.amazon.com/blogs/ai/introducing-nnvm-compiler-a-new-open-end-to-end-compiler-for-ai-frameworks/),
a software package for compiling models created in deep learning libraries into optimized machine codes (LLVM
Intermediate Representation for CPUs, CUDA and other for GPUs). The process consists of two stages:

1. NNVM compiler, based on a trained model from a deep learning library such as Keras or MXNet, creates and
   optimizes a computational graph.
1. [TVM](http://tvmlang.org/2017/08/17/tvm-release-announcement.html) takes the computational graph intermediate representation
   as an input, implements and optimizes it to be executed on a target platform (CPU, GPU or mobile).

NNVM is still in early stages and currently supports MXNet and CoreML models. Caffe and Keras are supported indirectly
via conversion to CoreML and explicit support for Keras is planned.

![NNVM supported libraries and targets]({attach}static/images/nnvm-formats.png)

Note that in the referenced above announcement, a special terminology is employed where the ML library used for
modelling is referred to as the *frontend* and the piece that will execute the model is called the *backend*. However
such terminology can be slightly confusing for two reasons:

* *Frontend* is often associated with the user-facing part while *backend* is something that is hidden. If we treat the
  algorithm developer as the user here, such terminology makes sense.
* When using Keras, the word *backend* already has a different meaning, it is the choice between Theano, Tensorflow and CNTK.

It is not exactly correct to list NNVM in the inference software packages, but at the moment it seems to be targeting
this segment while relying on the other *frontend* frameworks for the model design and training.

## Designated model interchange formats

### Open Neural Network Exchange (ONNX)

[ONNX](https://github.com/onnx/onnx) is a neural network model interchange format with the goal of enabling
interoperability between across deep learning libraries. Like CoreML uses Google Protocol Buffers for the schema
definition. Announced in September 2017
[by Microsoft](https://www.microsoft.com/en-us/cognitive-toolkit/blog/2017/09/microsoft-facebook-create-open-ecosystem-ai-model-interoperability/)
and [Facebook](https://research.fb.com/facebook-and-microsoft-introduce-new-open-ecosystem-for-interchangeable-ai-frameworks/),
it is in the early stages. Support for PyTorch, Caffe2 and CNTK is planned.

> ONNX provides an open source format for AI models. It defines an extensible computation graph model, as well
> as definitions of built-in operators and standard data types. Initially we focus on the capabilities needed for
> inferencing (evaluation).

Soon after the initial announcement, IBM
[joined the initiative](https://www.ibm.com/blogs/research/2017/10/open-standards-deep-learning-simplify-development-neural-networks/).

### Predictive Model Markup Language (PMML)

PMML is a model exchange format developed and maintained by the Data Mining Group.

Some types of models that PMML supports are neural networks, SVM, Naive Bayes classifiers and other. Data Mining Group
website features a list of [supported products and models](http://dmg.org/pmml/products.html).

PMML has third-party support, most often implemented by Openscoring.io, for many opensource machine and deep learning
libraries. It is sometimes referred to as the "de facto standard" for model interoperability.
That being said, Apple in their CoreML went for a custom model exchange format, Facebook and Microsoft teamed up
to create ONNX; the position of PMML in the area of deep learning is not as strong. XML is no longer the engineers'
favourite format for exchanging data.

### Portable Format for Analytics (PFA)

PMML's successor [PFA](http://dmg.org/pfa/index.html) is developed by the same organization, the Data Mining Group.
It uses [Avro](https://avro.apache.org/docs/current/) which is in many ways similar to Google Protocol Buffers.
It is unclear if PFA is currently supported by any software package.

## Last words

In classical "shallow" machine learning area, PMML seems to be the only independent standard with noticable degree of
adoption. In some cases, it is possible to use one library for training and then transpile the model for inference
without using an intermediate format like we saw for XGBoost. Some products specialize in serving predictions.

The world of deep learning is changing fast, just over the last few months a number of new and promising projects
were announced, including ONNX and NNVM. It is interesting to see if ONNX and NNVM will be widely accepted by the
community. A mature combination of the two could possibly lead to a situation where the user's choice of the deep
learning library for training will not limit the target inference environment. I can only speculate but CoreML model
format is likely there to stay, and it will benefit from ONNX and NNVM support.
