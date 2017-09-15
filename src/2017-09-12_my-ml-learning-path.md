Title: My ML learning path
Tags: machine learning, education
Summary: A story on how I learned myself some machine learning and an advice to fellow engineers

My colleague, [Mariana Bocoi](https://twitter.com/MarianaBocoi) was so kind as to invite me to the dry-run of her 
presentation on _Machine Learning for the masses_ where she speaks about her experience getting to know machine learning,
goes into the basics of what ML is and how can one get started. Not only the presentation is well made and has gotten 
a feedback of being "the least hostile presentation on machine learning" but it also pushed me to finally share my own path.

As many other ML enthusiasts over the last few years, I started with an amazing course on machine learning by 
[Andrew Ng](http://www.andrewng.org/)'s, available [for free on Coursera](https://www.coursera.org/learn/machine-learning). 
I took the course in early 2016 and have very positive recollections of the material and exercises. Being excited after 
the course I joined [one of](https://www.kaggle.com/c/santander-customer-satisfaction) the Kaggle competitions to practice
the new skills, unsurprisingly I didn't make it anywhere close to the top of the leaderboard but I learn a lot and 
strengthened the material.

The next big thing for me was the _Neural Networks for Machine Learning_ by [Geoffrey Hinton](http://www.cs.toronto.edu/~hinton/)
which is also [available on Coursera](https://www.coursera.org/learn/neural-networks/). Tons of material squeezed into the 
15 weeks of videos and assignments. A lot of fun, quite time-consuming, and sometimes a little challenging. 

In case your calculus or probability theory are rusty, it could be worth refreshing them before taking Hinton's course,
for example, [MITx 6.041x](https://www.edx.org/course/introduction-probability-science-mitx-6-041x-2) works really well 
and has incredible structure, content and just the right balance between dry theory and intuition.

It is absolutely brilliant that machine learning courses from the top universities and researchers like the ones mentioned 
above are available for free these days.

[Python Machine Learning](https://www.amazon.com/Python-Machine-Learning-Sebastian-Raschka/dp/1783555130/ref=sr_1_1?ie=UTF8&qid=1470882464&sr=8-1&keywords=python+machine+learning)
by [Sebastian Raschka](http://sebastianraschka.com/) is very hands-on and detailed description on how to solve the most
common machine learning tasks in Python. It is about to get the [second revision](https://github.com/rasbt/python-machine-learning-book-2nd-edition#whats-new-in-the-second-edition-from-the-first-edition) 
published; until that check out the great collection of notebooks with code examples from the [first](https://github.com/rasbt/python-machine-learning-book) 
and [second](https://github.com/rasbt/python-machine-learning-book-2nd-edition) editions.

To familiarize myself with NLP I used one of the Kaggle competitions where the main task was to extract signal from a text.
I tried both more classical approaches like TF-IDF followed by a random forest classifier as well as a convolutional neural net
on top of a word2vec representation of the texts. Using [t-SNE](https://distill.pub/2016/misread-tsne/) for word2vec 
visualization turned out to be a lot of fun, thanks to my colleague Damien Lejeune for guiding me. I used [this](https://www.kaggle.com/c/msk-redefining-cancer-treatment)
competition's dataset but I'm sure any good text corpus will do.

Russian-speaking readers should consider following [Machine Learning course](https://yandexdataschool.ru/edu-process/courses/machine-learning)
by [Yandex](https://en.wikipedia.org/wiki/Yandex) [Data School](https://yandexdataschool.com/) where the first part goes 
deeply into classic ML algorithms while the second part focuses more on neural networks, reinforcement learning and 
unsupervised learning. There also seem to be a [Coursera specialization](https://www.coursera.org/specializations/machine-learning-data-analysis)
by the same team and also in Russian.

There is also a number of resources I have on my to-do list but haven't yet had a chance to explore:
* [fast.ai](http://www.fast.ai/) offers [Practical Deep Learning for Coders](http://course.fast.ai/) and 
[Cutting Edge Deep Learning for Coders](http://course.fast.ai/part2.html), both sound amazing.
* [Deep Learning Specialization on Coursera](https://www.coursera.org/specializations/deep-learning) by Andrew Ng.
* [DataCamp](https://www.datacamp.com/) offers a lot of courses and tracks for everything data science and ML.
* [Stanford's CS231n](https://www.youtube.com/playlist?list=PL3FW7Lu3i5JvHM8ljYj-zLfQRF3EO8sYv) by Fei-Fei Li if I will
become interested in computer vision.

To summarize, I don't think my learning path was the most optimal one. What would I do differently if I were to start over?
Well, for one thing, I'd mix in more practice and real-life projects in between the online courses and books. And make sure
to apply all the [best practices for learning](https://www.coursera.org/learn/learning-how-to-learn?utm_source=blog). 
I also recommend checking [The Open Source Data Science Masters](http://datasciencemasters.org/) 
and [Will Wolf's somewhat unorthodox approach](http://willwolf.io/2016/07/29/my-open-source-machine-learning-masters-in-casablanca-morocco/)
to finding time to learn. Have an advice for fellow machine learning learners? Drop me an email and I will make sure to 
incorporate it.
