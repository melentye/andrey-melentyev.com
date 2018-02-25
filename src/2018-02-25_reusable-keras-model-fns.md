Title: Reusable Keras model definitions
Tags: deep learning, keras
Modified: 2018-02-25 14:02
Summary: How to define your Keras models in code to allow reuse.

Models in Keras inherit from the `keras.engine.training.Model` class. It is a container for layers but it may also
include other models as building blocks. Before being trained or used for prediction, a Keras model needs to be
"compiled". I have found that in order to improve reusability of the model code, there are some basic principles
I need to follow:

* Keep model definition separate from compilation and training steps.
* Implement models as methods taking hyper-parameters as input and returning `Model` objects.
* Consider making top level layers optional.

I would not expect anyone to take this advice for granted, therefore let's proceed to the rationale behind every point.

## Separate model definition from compilation and training

The argument goes as follows: having model defined separately, one can later decide to train it with one optimizer
or another.

Let's consider an example of a basic convolution neural network for multi-label sentence classification:

```python
from keras import Sequential, Model
from keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense

def simple_cnn_pretrained_vectors(embedding_matrix, max_words_in_sample,
                                  num_feature_maps=10, kernel_size=5,
                                  num_classes=6) -> Model:
    model = Sequential()
    model.add(Embedding(input_dim=embedding_matrix.shape[0],
                        input_length=max_words_in_sample,
                        weights=[embedding_matrix],
                        output_dim=embedding_matrix.shape[1]))
    model.add(Conv1D(filters=num_feature_maps, 
                     kernel_size=kernel_size,
                     activation='relu'))
    model.add(GlobalMaxPooling1D())
    model.add(Dense(units=num_classes, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='sgd')
    return model

 # Load pre-trained word vectors
embedding_matrix = ...
# Load, tokenize, vectorize the sentences
X_train, X_val, y_train, y_val = ...
# Trim/pad sentences to a fixed length
max_seq_len = ...
model = simple_cnn_pretrained_vectors(embedding_matrix, max_seq_len)
model.fit(X_train, y_train,
          epochs=20,
          validation_data=(X_val, y_val),
          verbose=1)
```

This is nice, now what if we want to [freeze](https://keras.io/getting-started/faq/#how-can-i-freeze-keras-layers)
the embedding layer and use a more advanced optimizer with an aggressive learning rate? One way is to create new method
like `simple_cnn_pretrained_vectors_adam_big_lr` - that'd work but would lead to copy-paste of the model definition.
The second option could be to pass the optimizer as an input parameter to our model producing method, that'd work too
but what if we have a dozen of such methods with different model architectures?
Another straightforward way to make it work is to postpone model compilation until we actually know how we want to
train the model:

```python
from keras import Sequential, Model
from keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense
from keras.optimizers import Adam

def simple_cnn_pretrained_vectors(embedding_matrix, max_words_in_sample,
                                  num_feature_maps=10, kernel_size=5,
                                  num_classes=6) -> Model:
    model = Sequential()
    model.add(Embedding(input_dim=embedding_matrix.shape[0],
                        input_length=max_words_in_sample,
                        weights=[embedding_matrix],
                        output_dim=embedding_matrix.shape[1]))
    model.add(Conv1D(filters=num_feature_maps, 
                     kernel_size=kernel_size, 
                     activation='relu'))
    model.add(GlobalMaxPooling1D())
    model.add(Dense(units=num_classes, activation='sigmoid'))
    # notice how the model isn't compiled here anymore
    return model

# Load pre-trained word vectors
embedding_matrix = ...
# Load, tokenize, vectorize the sentences
X_train, X_val, y_train, y_val = ...
# Trim/pad sentences to a fixed length
max_seq_len = ...
model = simple_cnn_pretrained_vectors(embedding_matrix, max_seq_len)
# Freeze the embedding layer
for layer in model.layers:
    if isinstance(layer, Embedding):
        layer.trainable = False
# instead we delay the compilation until training time 
# where we have more information on which layers we want to train
# and how the model should be optimized
model.compile(loss='binary_crossentropy', 
              optimizer=Adam(lr=0.01, amsgrad=True))
model.fit(X_train, y_train,
          epochs=20,
          validation_data=(X_val, y_val),
          verbose=1)
```

## Model definitions as functions taking hyper-parameters as arguments

This is how `keras.applications` module

## Compatibility of with scikit-learn wrappers

It is disappointing but the suggested approach with methods returning models without compiling them first won't work
with [Keras scikit-learn wrappers](https://keras.io/scikit-learn-api/) such as
`keras.wrappers.scikit_learn.KerasClassifier` and `keras.wrappers.scikit_learn.KerasRegressor`. The documentation
clearly states:

> `build_fn` should construct, *compile* and return a Keras model, which will then be used to fit/predict.

And the error message that you'll get if you try is `AttributeError: 'Sequential' object has no attribute 'loss'`.
Let's cast some higher-order function magic to fix it:

```python
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.wrappers.scikit_learn import KerasClassifier

def binary_logistic_regression(input_dim=10):
    model = Sequential()
    model.add(Dense(1, input_dim=input_dim, activation='sigmoid'))
    return model

def compiled(model_fn, loss, optimizer, metrics=None):
    def compiled_model_fn():
        model = model_fn()
        model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
        return model

    return compiled_model_fn

build_fn = compiled(binary_logistic_regression, 
                    loss='binary_crossentropy',
                    optimizer=Adam(lr=0.01, amsgrad=True))
# at this point build_fn is a function that produces compiled models
sklearn_clf = KerasClassifier(build_fn=build_fn)
sklearn_clf.fit(...)
```

we introduce a function `compiled` which takes our model-producing function as input, as well as the loss function
and the optimizer and returns another function which produces compiled models. This is a step forward, now the `fit`
method is less unhappy. There's still a small problem - you can't pass arguments to the `build_fn`, because the 
function `compiled_model_fn` doesn't take any. Python's functools module comes to rescue with it's [wraps](https://docs.python.org/3/library/functools.html#functools.wraps) method:

```python
from functools import wraps

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.wrappers.scikit_learn import KerasClassifier

def compiled(model_fn, loss, optimizer, metrics=None):
    @wraps(model_fn)
    def compiled_model_fn(*args, **kwargs):
        model = model_fn(*args, **kwargs)
        model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
        return model

    return compiled_model_fn

build_fn = compiled(simple_cnn_pretrained_vectors,
                    loss='binary_crossentropy',
                    optimizer=Adam(lr=0.01, amsgrad=True))
# at this point build_fn is a function that produces compiled models,
# it also takes the same arguments as simple_cnn_pretrained_vectors
sklearn_clf = KerasClassifier(build_fn=build_fn, 
                              embedding_matrix=...,
                              max_words_in_sample=140)
sklearn_clf.fit(...)
```

our `compiled` higher-order function became a little smarter, now it knows to produce a function that takes
the same arguments as the input argument `model_fn`.
