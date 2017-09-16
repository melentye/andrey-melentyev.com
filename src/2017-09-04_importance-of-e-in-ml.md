Title: On the importance of software engineering in machine learning
Tags: machine learning, software engineering
Summary: Machine learning is a software-heavy area where software development know-how is useful in a number of cases.
Let's take a look at how applying engineering practices can help build ML products faster, make them more reliable and
keep data scientists happy.

With the recent advances in areas of machine and deep learning, availability of large data sets and inexpensive compute
power, engineering aspects of ML-heavy products such as maintainability, testability, scalability are becoming
increasingly important. In real life products, even the most advanced and well-tuned model is worth very little until it
is deployed. Being able to test and deploy new features and models quickly is a much-desired capability.

A typical ML project will have a number of stages similar to the ones below with some feedback
loops between them:

* Data collection, where the data of interest is collected (or not!) and made available for future analysis.
* Exploratory analysis, when data scientists explore the data and make sense of it.
* Modelling, development of a model to solve the problem at hand.
* Deployment of the resulting models into production and scaling them to support the load.
* Monitoring the ML systems in production, including the features and predictions.

At each step, applying engineering practices such as
[version control for source code](https://martinfowler.com/bliki/VersionControlTools.html),
[unit testing](https://www.martinfowler.com/bliki/UnitTest.html),
[continuous integration](https://martinfowler.com/articles/continuousIntegration.html)
and [delivery](https://www.martinfowler.com/bliki/ContinuousDelivery.html),
[infrastructure as code](https://www.martinfowler.com/bliki/InfrastructureAsCode.html),
[agile principles](http://agilemanifesto.org/) can help improve the quality and reduce lead time. A simplified way of
thinking about it is to automate as much routine as possible in order to allow data scientists to focus on modelling and
have a shorter feedback loop between having a new idea and seeing it work live.

For example, a mature data-intensive company will likely create and support infrastructure for **data collection**, some
kind of data lake to store what's been collected. Depending on the needs and constraints, the collection of data can be
batch or (near)real-time, but first and foremost it should be automated. It allows data scientist to easily find what 
data is available and how to access it.

Collecting the data is not enough, imagine there are terabytes of relevant data but not enough **infrastructure for
analysis and modelling**. Yet again, an engineering effort needs to be taken to create or provision the necessary tools.
Luckily these days there are plenty of open source products covering all the basic needs. Compute is cheap and quick to
scale with cloud providers like AWS or Azure: an instance with Tesla K80 GPU costs as little as [$0.21 per hour](https://aws.amazon.com/ec2/spot/pricing/).
Depending on the size of the data sets and ML algorithms, modelling can happen anywhere from laptops to clusters of 
GPU-powered instances in the cloud. Feature engineering, model training and validation are some of the activities that
we associate with the data scientist role but it doesn't mean no engineering work is required to make them efficient
and painless.

**Production deployment** of models and **feature extraction pipelines** are perhaps some of the steps where the role of
engineering has always been appreciated and the role of the data scientist ceases. However there's yet another possible
win: instead of the popular approach where data scientists hand over documentation and ask the engineers to implement the
features and models once again, this time using a production-worthy framework, engineering can be used to build a
framework allowing data scientists to deploy models directly to production. Feature pipelines can be developed in a way
that is suitable for both analysis and production use cases. It may sound scary, but with a certain amount of automated
testing, it is known to work well.

Now that we have the newly produced model making decisions live, we are still not done.
**Monitoring, logging and audit** are some of the capabilities that can be developed: values of input variables
or features for the model, as well as model decisions, can be logged and made available in form of dashboards.
Depending on business needs, alerts can be set up to notify on-call staff of deviations from the expected value
distributions. Model results can be fed back to the data lake for further analysis.
[What's your ML test score?](https://research.google.com/pubs/pub45742.html) - a paper by Google Research
covers questions of testing monitoring ML production systems.

One other place where software engineering practices are useful is the development of the **machine learning frameworks**,
[Scikit-learn](http://scikit-learn.org/), [TensorFlow](https://www.tensorflow.org/), [Theano](http://deeplearning.net/software/theano/),
[Keras](keras.io), [Gensim](https://radimrehurek.com/gensim/) just to name a few, all use version control systems,
reproducible builds, and continuous integration pipelines with automated testing.

Another interesting topic is team organization, how does one structure the teams so that data scientists get the best of
engineering? What is the best way to **collaborate**? What is the role of ML engineer?

In this blog, I will do my best to collect best practices and summarize my personal experience in the area of production
ML systems.

_Geronimo!_
