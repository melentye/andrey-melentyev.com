Title: Model interchange formats
Tags: machine learning, interoperability
Modified: 2017-10-10 22:06
Status: draft
Summary: Current state of the model interchange formats including PMML and ONNX

Unless you are using the same language and framework for both training and prediction, you will normally have to adopt a
model interchange format: the trained model will be exported to a format which is also supported by the prediction
component. There are multiple cases when this may be required, for example when there are strict requirements to the
prediction latency and the language used for modelling is not performant enough, when the machine learning process in
the company is organized in a way such that the features and the model are developed by one team and deployed by
another team, or when the model needs to be executed in environments completely different from the training one, such
as edge devices or client-side in a browser.

In this articles we will explore various types of model interchange formats, including those provided by machine learning
frameworks, natively in programming languages and designated interchange formats. I'll briefly touch upon
Apple CoreML, Baidu MDL and NNVM and the kinds of model formats they support.

[TOC]

## Modelling frameworks and their supported formats

### scikit-learn

[scikit-learn](http://scikit-learn.org/)'s recommended way of model persistence is to use
[Pickle]({filename}/2017-09-27_model-interchange-formats.md#python). The alternative is the `sklearn.externals.joblib`
module with `dump` and `load` functions which may be more efficient. Refer to
[the documentation](http://scikit-learn.org/stable/modules/model_persistence.html) for code example.

There's a [sklearn2pmml](https://github.com/jpmml/sklearn2pmml) library by Openscoring.io team that allows exporting
scikit-learn models to PMML. It is implemented as a Python wrapper around
[a Java library](https://github.com/jpmml/jpmml-sklearn) and it is somewhat unclear which types of sklearn models are supported.
It is also worth noting that these Openscoring.io software is distributed under a viral
[GNU Affero General Public License](https://tldrlegal.com/license/gnu-affero-general-public-license-v3-(agpl-3.0)).

[sklearn-porter](https://github.com/nok/sklearn-porter) allows transpiling trained scikit-learn models into C, Java, JavaScript
and other languages. [Scikit-Learn Compiled Trees](https://github.com/ajtulloch/sklearn-compiledtrees/) creates C++ code
for sklearn decision trees and ensembles, but hasn't been updated for 11 months at the time of writing.

### XGBoost

[XGBoost](https://xgboost.readthedocs.io/en/latest/) gradient boosted decision trees library core is written in C++
with APIs available for Python, R, Java and Scala. Model saving and loading is done into an framework-specific format
and is offered via a pair of methods, there are examples
[in Python](http://xgboost.readthedocs.io/en/latest/python/python_intro.html#training) and
[in R](http://xgboost.readthedocs.io/en/latest/R-package/xgboostPresentation.html#save-and-load-models).
Because the model persistence logic is delegated to the library core, an XGB model trained in R or Python can then be exported
and loaded into a prediction module written in a different, possibly more performant langugage such as C++.

XGBoost models can be converted to PMML using [jpmml-xgboost](https://github.com/jpmml/jpmml-xgboost) by Openscoring.io.

Models can also be converted to Apple CoreML using [coremltools](https://github.com/apple/coremltools).

### LightGBM

[LightGBM](https://github.com/Microsoft/LightGBM) is another popular decision tree gradient boosting library, created
by Microsoft. Just like XGBoost its core is written in C++ with APIs in R and Python. Code examples
[in R](https://github.com/Microsoft/LightGBM/blob/master/R-package/demo/basic_walkthrough.R) and
[Python](https://github.com/Microsoft/LightGBM/blob/master/tests/python_package_test/test_basic.py) show how to save and
load models into LightGBM internal format.

LightGBM models can be converted to PMML using [jpmml-lightgbm](https://github.com/jpmml/jpmml-lightgbm) by Openscoring.io.

### CatBoost

[CatBoost](https://tech.yandex.com/catboost/doc/dg/concepts/about-docpage/) is a library by
[Yandex](https://en.wikipedia.org/wiki/Yandex) implementing gradient boosting on decision trees. It features C++ core, Python,
R and command-line interfaces.

In R, built-in serialization in RDS [won't work](https://github.com/catboost/catboost/issues/91) for CatBoost models but
there are [save_model](https://tech.yandex.com/catboost/doc/dg/concepts/r-reference_catboost-save_model-docpage/)
and [load_model](https://tech.yandex.com/catboost/doc/dg/concepts/r-reference_catboost-load_model-docpage/) methods covers
the have you covered.

CatBoost Python package has familiar pair of methods
[to save](https://tech.yandex.com/catboost/doc/dg/concepts/python-reference_catboost-docpage/#save_model)
the model and to [load it back](https://tech.yandex.com/catboost/doc/dg/concepts/python-reference_catboost-docpage/#load_model).
Python API also supports saving trained CatBoost models to Apple CoreML format:

    :::python
    import catboost
    from sklearn import datasets

    wine = datasets.load_wine()
    cls = catboost.CatBoostClassifier(loss_function='MultiClass')

    cls.fit(wine.data, wine.target)
    cls.save_model("wine.mlmodel", format="coreml", export_parameters={'prediction_type': 'probability'})

Produces a CoreML model

    :::shell
    $ file wine.mlmodel
    wine.mlmodel: PDP-11 pure executable not stripped - version 101

Which can later be imported into a macOS or iOS app, see [CoreML]({filename}/2017-09-27_model-interchange-formats.md#apple-coreml)

### Spark MLLib

Starting from Spark 1.6, MLLib transformers and models can be persisted and later loaded.

MLLib Pipeline API also has
[export/import functionality](https://docs.cloud.databricks.com/docs/spark/1.6/examples/ML%20Pipeline%20Persistence.html)
which requires every component of the pipeline to implement the save/load methods.

Spark has [PMML export feature](https://spark.apache.org/docs/latest/mllib-pmml-model-export.html) for linear, ridge and
lasso regression models, k-means clustering, SVM and binary logistic regression models.

### Theano

Theano recommends [Pickle]({filename}/2017-09-27_model-interchange-formats.md#python) model serialization for short-term storage and
[offers advice](http://deeplearning.net/software/theano/tutorial/loading_and_saving.html) on long-term storage.

### Tensorflow

Offers a language-agnostic [SavedModel](https://www.tensorflow.org/programmers_guide/saved_model) format, meaning that
you can store a model trained with Tensorflow Python package and then load it from the C++ API. The format uses
[Google Protocol Buffers](https://developers.google.com/protocol-buffers/) for schema definition, kind of a logical
step for Tensorflow being a Google product.

[Tensorflow Serving](https://www.tensorflow.org/serving/) is a product whose purpuse is, unsurprisingly, to serve
Tensorflow models. It exposes a [gRPC](https://grpc.io/) endpoint that can be deployed into production infrastructure
and be called by other components that need to run machine learning models. Tensorflow Serving is not limited to
Tensorflow models and can be tailored to execute arbitrary model code while providing nice abstractions around it.
It is a viable alternative for production deployments of any machine learning models, especially if your organization
is service-oriented and has experience integrating gRPC endpoints.

### Keras

[Keras](https://keras.io/) is a deep learning library written by [François Chollet](https://twitter.com/fchollet) in
Python, it providies high-level abstractions for building neural network models. It allows defining the network
architecture  in clean and human-readable code and it delegates the actual training to Theano, Tensorflow or CNTK.

Keras documentation [recommends using framework-specific method of model persistence](https://keras.io/getting-started/faq/#how-can-i-save-a-keras-model)
which gives the user a choice of storing both the nueral network architecture and the trained weights, or just one of
the two components. Keras uses [HDF5](https://hdfgroup.org/HDF5/) format popular in the scientific applications.

[Here's a good guide](https://tensorflow.rstudio.com/keras/articles/faq.html#how-can-i-save-a-keras-model) on how to do
it for Keras in R.

### PyTorch

Like Keras, supports exporting the entire model or just the parameters as documented [here](http://pytorch.org/docs/master/notes/serialization.html).
The implementation uses [Python Pickle]({filename}/2017-09-27_model-interchange-formats.md#python) under the hood.

### Deeplearning4j

[Deeplearning4j](https://deeplearning4j.org/), as the name suggests, is a deep learning library for Java. The underlying
computation is not done in JVM but rather written in C and C++. It has an additional Keras API and
[can import](https://deeplearning4j.org/model-import-keras) trained Keras models allowing to chose between
importing just the model architecture from `.json` file and importing a model together with weights from the `.h5`.
Once loaded into DL4J, a model can be further trained or deployed into a production environment for predictions.

DL4J also has its own [model persistence format](https://deeplearning4j.org/modelpersistence). Later in 2017 a direct
import of Tensorflow models is planned (right now it is only possible to import a Tensorflow model if it is created in
Keras).

## Other frameworks and their supported formats

### Apple CoreML

Apple has recently released [CoreML](https://developer.apple.com/documentation/coreml) - a library for *running* trained
machine learning models on iOS and macOS. In contrast to the rest of the frameworks mention above, CoreML itself can't
be used for training models. It is shipped with a set of pre-trained models for computer vision and natural language
processing tasks. Models trained using other frameworks can be converted into CoreML `.mlmodel` format. It
is a binary format using [Google Protocol Buffers](https://developers.google.com/protocol-buffers/) to
describe the schema and with a [publicly available specification](https://apple.github.io/coremltools/coremlspecification/index.html).
A great thing about building on top of Protocol Buffers is that they have support for virtually all major programming
languages.

The introductory [WWDC 2017 presentation on CoreML](https://developer.apple.com/videos/play/wwdc2017/703/) lists the supported
by CoreML conversion tool modelling frameworks. The following frameworks are supported: Caffe and Keras for neural nets
(only outdated major versions at the time of announcement), scikit-learn and XGBoost for tree ensembles,
[LIBSVM](http://www.csie.ntu.edu.tw/~cjlin/libsvm/) and scikit-learn for SVM and some more models from scikit-learn.

![CoreML supported model formats]({attach}static/images/coreml-formats.png)

There's a page explaining
[how to convert a model into CoreML format](https://developer.apple.com/documentation/coreml/converting_trained_models_to_core_ml)
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

[Clipper](http://clipper.ai/) is another product for *running* trained models. It allows deploying models as microservices
that can be invoked by other services within the IT landscape of the company, for example a rules engine may call out to
a feature service to fetch the variables and then call Clipper to make the predictions. Trained Python models
[can be deployed directly](http://clipper.ai/documentation/python_model_deployment/) into Clipper, a prediction serving
service by UC Berkeley [RISE Lab](https://rise.cs.berkeley.edu/).

### NNVM

While this article was being written, AWS
[announced NNVM](https://aws.amazon.com/blogs/ai/introducing-nnvm-compiler-a-new-open-end-to-end-compiler-for-ai-frameworks/),
a framework for compiling models created in deep learning frameworks into optimized machine codes (LLVM Intermediate Representation
for CPUs, CUDA and other for GPUs). The process consists of two stages:

1. NNVM compiler, based on the model from a deep learning framework such as Keras or MXNet, creates and
   optimizes a computational graph.
1. [TVM](http://tvmlang.org/2017/08/17/tvm-release-announcement.html) takes the computational graph intermediate representation
   as an input, implements and optimizes it to be executed on a target platform (CPU, GPU or mobile).

NNVM is still on early stages and currently supports MXNet and CoreML models. Caffe and Keras are supported indirectly
via conversion to CoreML and explicit support for Keras is planned.

![NNVM supported frameworks and targets]({attach}static/images/nnvm-formats.png)

Note that in the referenced above announcement, a special terminology is employed where the modelling framework is
referred to as the *frontend* and the piece that will execute the model is called the *backend*. However such
terminology can be slightly confusing for two reasons:

* *Frontend* is often associated with the user-facing part while *backend* is something that is hidden. If we treat the
  algorithm developer as the user here, such terminology makes sense.
* When using Keras, the word *backend* already has a different meaning, it is the choice between Theano, Tensorflow and CNTK.

## Model persistence using programming language standard libraries

### R

For those R frameworks that don't offer their own way of saving and loading models, R offers object
serialization/deserialization using
[saveRDS/readRDS](https://stat.ethz.ch/R-manual/R-devel/library/base/html/readRDS.html)
or [save](https://stat.ethz.ch/R-manual/R-devel/library/base/html/save.html)/
[load](https://stat.ethz.ch/R-manual/R-devel/library/base/html/load.html).
The resulting format while being available to all R users is not scoring too high on the interoperability scale.

Framework-specific save/load feature should normally be preferred since the serialized R object might not have all
the necessary data or may have some extra data that is not necessary for storing a trained model.

### Python

Python's built-in persistence model, an alternative to R object serialization, is called
[Pickle](https://docs.python.org/3/library/pickle.html).
And, similarly to R object serialization, it lacks interoperability. Framework-specific model persistence functionality
is preferrable when exist. scikit-learn has a
[concise code snippet](http://scikit-learn.org/stable/modules/model_persistence.html#persistence-example)
showing the usage of Pickle to save and load the model.

Note that pickling might not be a suitable approach for long-term model storage, due to the fact that it doesn't store
classes, only their instances. Therefore it may not be possible to deserialize a model trained by an older version of
a library using a newer one.

## Designated model interchange formats

### Open Neural Network Exchange (ONNX)

A neural network model interchange format with the goal of enabling interoperability between across deep learning frameworks.
Like CoreML, uses Google Protocol Buffers for the schema definition. Announced in September 2017
[by Microsoft](https://www.microsoft.com/en-us/cognitive-toolkit/blog/2017/09/microsoft-facebook-create-open-ecosystem-ai-model-interoperability/)
and [Facebook](https://research.fb.com/facebook-and-microsoft-introduce-new-open-ecosystem-for-interchangeable-ai-frameworks/),
it is on the early stages. Support for PyTorch, Caffe2 and CNTK is planned.

> ONNX provides an open source format for AI models. It defines an extensible computation graph model, as well
> as definitions of built-in operators and standard data types. Initially we focus on the capabilities needed for
> inferencing (evaluation).

### Predictive Model Markup Language (PMML)

Some types of models that PMML supports are neural networks, SVM, Naive Bayes classifiers and other.

PMML has third-party support, most often implemented by Openscoring.io, for many machine and deep learning frameworks.
It is sometimes referred to as the "de facto standard" for model interoperability and cannot be ignored.
That being said, Apple in their CoreML went for a custom model exchange format, Facebook and Microsoft teamed up
to create ONNX; the position of PMML in the area of deep learning is not as strong.

## Last words

In classical *shallow* machine learning area, PMML seems to be the only independent standard. In some cases it is possible
to use one framework for training and then transpile the model for predictions without using an intermediate format,
like we saw for XGBoost.

The world of deep learning is changing fast and just over the last few months a number of new and promising projects
were announced, including ONNX, NNVM and CoreML. I can only speculate but CoreML model format is likely there to stay
and perhaps soon there will be tools supporting conversion in both directions. What is even more interesting to see is
if ONNX and NNVM will be widely accepted by the community. A mature combination of the two could possibly lead to
a situation where the user's choice of the *frontend* framework will not limit the target *backends*. 

For those who got 
