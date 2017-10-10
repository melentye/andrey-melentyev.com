Title: Model interchange formats
Tags: machine learning, interoperability
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
frameworks, natively in programming languages and designated interchange formats. We'll briefly touch
Apple CoreML, Baidu MDL and NNVM and the kinds of model formats they support.

[TOC]

## Modelling frameworks and their supported formats

### scikit-learn

[scikit-learn](http://scikit-learn.org/)'s recommended way of model persistence is to use Pickle which we will cover in
the Python chapter of the article. The alternative is the `sklearn.externals.joblib` module with `dump` and `load`
functions which may be more efficient. Refer to [the documentation](http://scikit-learn.org/stable/modules/model_persistence.html)
for code example.

There's a [sklearn2pmml](https://github.com/jpmml/sklearn2pmml) library by Openscoring.io team that allows exporting
scikit-learn models to PMML. It is implemented as a Python wrapper around
[a Java library](https://github.com/jpmml/jpmml-sklearn) and it is somewhat unclear what types of sklearn models are supported.
It is also worth noting that these Openscoring.io software is distributed under a viral
[GNU Affero General Public License](https://tldrlegal.com/license/gnu-affero-general-public-license-v3-(agpl-3.0)).

[sklearn-porter](https://github.com/nok/sklearn-porter) allows transpiling trained scikit-learn models into C, Java, JavaScript
and other languages. [Scikit-Learn Compiled Trees](https://github.com/ajtulloch/sklearn-compiledtrees/) creates C++ code
for sklearn decision trees and ensembles, but hasn't been updated for 11 months at the time of writing.

### XGBoost

[XGBoost](https://xgboost.readthedocs.io/en/latest/) gradient boosting library core is written in C++ with APIs available
for Python, R, Java and Scala. Model saving and loading is done into an framework-specific format and is offered via a
pair of methods, there are examples
[in Python](http://xgboost.readthedocs.io/en/latest/python/python_intro.html#training) and
[in R](http://xgboost.readthedocs.io/en/latest/R-package/xgboostPresentation.html#save-and-load-models).
Because the model persistence logic is delegated to the library core, an XGB model trained in R or Python can then be exported
and loaded into a prediction module written in a different, possibly more performant langugage such as C++.

XGBoost models can be converted to PMML using [jpmml-xgboost](https://github.com/jpmml/jpmml-xgboost) by Openscoring.io.

Models can also be converted to Apple CoreML using [coremltools](https://github.com/apple/coremltools).

### LightGBM

[LightGBM](https://github.com/Microsoft/LightGBM) is another popular gradient boosting library, created by Microsoft. Just
like XGBoost it's core is written in C++ with APIs in R and Python. Code examples
[in R](https://github.com/Microsoft/LightGBM/blob/master/R-package/demo/basic_walkthrough.R) and
[Python](https://github.com/Microsoft/LightGBM/blob/master/tests/python_package_test/test_basic.py) show how to save and
load models into LightGBM internal format.

LightGBM models can be converted to PMML using [jpmml-lightgbm](https://github.com/jpmml/jpmml-lightgbm) by Openscoring.io.

### CatBoost

[CatBoost](https://tech.yandex.com/catboost/doc/dg/concepts/about-docpage/) is a library by
[Yandex](https://en.wikipedia.org/wiki/Yandex) implementing gradient boosting on decision trees. It features C++ core, Python,
R and command-line interfaces.

In R built-in serialization in RDS [won't work](https://github.com/catboost/catboost/issues/91) for CatBoost models but
there are [save_model](https://tech.yandex.com/catboost/doc/dg/concepts/r-reference_catboost-save_model-docpage/)
and [load_model](https://tech.yandex.com/catboost/doc/dg/concepts/r-reference_catboost-load_model-docpage/) methods covers
the have you covered.

CatBoost Python package has familiar pair of methods
[to save](https://tech.yandex.com/catboost/doc/dg/concepts/python-reference_catboost-docpage/#save_model)
the model and to [load it back](https://tech.yandex.com/catboost/doc/dg/concepts/python-reference_catboost-docpage/#load_model).
Python API also supports saving trained CatBoost models to Apple CoreML format:

    :::python
    # TODO
    print("The path-less shebang syntax *will* show line numbers.")

### Spark MLLib

Starting from Spark 1.6, MLLib transformers and models can be persisted and later loaded.

MLLib Pipeline API also has
[export/import functionality](https://docs.cloud.databricks.com/docs/spark/1.6/examples/ML%20Pipeline%20Persistence.html)
which requires every component of the pipeline to implement the save/load methods.

Spark has [PMML export feature](https://spark.apache.org/docs/latest/mllib-pmml-model-export.html) for linear, ridge and
lasso regression models, k-means clustering, SVM and binary logistic regression models.

### Theano

http://deeplearning.net/software/theano/tutorial/loading_and_saving.html

### Tensorflow

[Tensorflow Serving](https://www.tensorflow.org/serving/)

### Keras

[Keras](https://keras.io/) is a deep learning library written by [François Chollet](https://twitter.com/fchollet) in
Python, it providies high-level abstractions for building neural network models. It allows you to use clean and
human-readable code to define the network architecture and it delegates the actual training to Theano, Tensorflow or CNTK.

For Python
[Here's a good guide](https://tensorflow.rstudio.com/keras/articles/faq.html#how-can-i-save-a-keras-model) on how to do
it for Keras in R.

### PyTorch

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

The introductory [WWDC 2017 presentation on CoreML](https://developer.apple.com/videos/play/wwdc2017/703/) lists the supported
by CoreML conversion tool modelling frameworks. The following frameworks are supported: Caffe and Keras for neural nets
(only outdated major versions at the time of announcement), scikit-learn and XGBoost for tree ensembles,
[LIBSVM](http://www.csie.ntu.edu.tw/~cjlin/libsvm/) and scikit-learn for SVM and some more models from scikit-learn.

![CoreML supported model formats]({attach}static/images/coreml-formats.png)

There's a page explaining
[how to convert a model into CoreML format](https://developer.apple.com/documentation/coreml/converting_trained_models_to_core_ml)
and the conversion [coremltools](https://github.com/apple/coremltools) themselves are open source.

Interesting to see that Apple decided not to support PMML as one of the import formats.

### Baidu Mobile Deep Learning

Baidu's [MDL](https://github.com/baidu/mobile-deep-learning) is a new kid on the block, similar to Apple CoreML,
it's a library for deploying deep learning models to mobile devices with support for iOS and Android. Models trained in
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
   optimizes a computation graph.
1. TVM implements and optimizes the output of NNVM to be executed on a target platform (CPU, GPU or mobile).

NNVM is still on early stages and currently supports MXNet and CoreML models. Caffe and Keras are supported indirectly
via conversion to CoreML and explicit support for Keras is planned.

![NNVM supported frameworks and targets]({attach}static/images/nnvm-formats.png)

Note that in the referenced above announcement, a special terminology is employed where the modelling framework is
referred to as the *frontend* and the piece that will execute the model is called the *backend*. However such
terminology can be slightly confusing for two reasons:

* *Frontend* is often associated with the user-facing part while *backend* is something that is hidden. If we treat the
  algorithm developer as the user here, such terminology makes sense.
* When using Keras, the word *backend* already has a different meaning, it's the choice between Theano, Tensorflow and CNTK.

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

### Predictive Model Markup Language (PMML)

Some types of models that PMML supports are neural networks, SVM, Naive Bayes classifiers and other.

### Open Neural Network Exchange (ONNX)

### Custom model interchange formats

The article merely gives an overview of what's already available, I will not rule out that in some cases implementing
your own custom format may be worthwhile.

Let me know if your favorite language/framework/format missing in the article, I will try to include it.
