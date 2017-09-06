Title: On the importance of software engineering in machine learning
Tags: machine learning, software engineering
Summary: Machine learning is a software-heavy area where software development know-how is useful in a number of cases. Let's take a look at how applying engineering practices can help build ML products faster, make them more reliable and keep data scientists happy.  

With the recent advances in areas of machine and deep learning, availability of large data sets and inexpensive compute 
power, engineering aspects of ML-heavy products are becoming increasingly important. There's a number of stages 
in a typical ML project:

* Data collection, where the data of interest (or not!) is collected and made available for future analysis.
* Exploratory analysis, when data scientists explore the data and make sense of it.
* Modelling, development and application of ML algorithms in order to solve the problem at hand.
* Deployment of the resulting models into production and scaling them to support the load.
* Monitoring the ML systems in production, including the features and predictions.

On each step, applying engineering practices such as [version control for source code](https://martinfowler.com/bliki/VersionControlTools.html), 
[unit testing](https://www.martinfowler.com/bliki/UnitTest.html), [continuous integration](https://martinfowler.com/articles/continuousIntegration.html)
 and [delivery](https://www.martinfowler.com/bliki/ContinuousDelivery.html), [infrastructure as code](https://www.martinfowler.com/bliki/InfrastructureAsCode.html), 
 [agile principles](http://agilemanifesto.org/) can help improve the quality and reduce lead time. A simplified way of 
thinking about it is to automate as much routine as possible in order to allow data scientists to focus on modelling.

For example, a mature data-driven company will likely create and support infrastructure for data ingestion, some kind of 
data lake to store what's been collected, and necessary tooling for analysis and modelling using the resulting data sets.
Depending on the needs and constraints the collection of data can be batch or (near)realtime but first and foremost 
it should be automated. 

Collecting the data is not enough, imagine there are terabytes of relevant data but not enough infrastructure to query it.
Yet again, an engineering effort needs to be taken to create or provision the necessary tools. Luckily these days there 
are plenty of open source products which should cover all the basic needs. Compute is cheap and quick to scale with cloud
providers like AWS or Azure: an instance with Tesla K80 GPU costs as little as [$0.21 per hour](https://aws.amazon.com/ec2/spot/pricing/). 
Depending on the size of the data sets and ML algorithms, modelling can happen anywhere from laptops to clusters of 
GPU-enabled instances in the cloud.

Production deployment of models and feature extraction pipelines is perhaps one of the steps where the role of engineering
has always been appreciated and the role of the data scientist ends. However there's a middle ground with yet another win:
software engineering can be used to build a framework allowing data scientists to deploy models to production. Feature 
pipelines can be developed in a way that is suitable for both analysis and production use cases. Sounds scary, but with 
a certain amount of automated testing on top, it is known to work very well.

Now that we have the newly produced model making decisions live, we are still not done. Monitoring, logging and audit are
some of the capabilities that can be developed: values of input variables or features for the model, as well as model 
decisions can be logged and made available in form of dashboards. Depending on business needs, alerts can be set up to 
notify on-call staff of deviations from the expected value distributions. Model results can be fed back to the data lake 
for further analysis. [What's your ML test score?](https://research.google.com/pubs/pub45742.html) paper by Google Research
covers questions of testing monitoring ML production systems.

In this blog I will do my best to collect and summarize my personal experience and best practices in the field. 

_Geronimo!_
    