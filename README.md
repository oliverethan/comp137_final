Excerpts from final report about the project:

# COMP137 Report: Neuron Activation Pattern Monitoring on DenseNet
### Ethan Oliver


## Introduction

Currently most machine learning models are black boxes. A typical image classifier network takes in an input image and outputs a set of probabilities for what class that image falls into. Over the years these computer vision models have gotten more accurate but they have also gotten more complex. A human user can no longer tell how the network makes decisions and whether or not they are trustworthy decisions. These complex architectures make it easy for bias to enter the model and make it more difficult to fix errors. As machine learning models move outside the laboratory and into the real world these problems only become more pressing.

When a classification network makes a decision, an important question to ask is whether that decision was made based on information it learned from the training set about that class or if it is attempting to classify something outside the bounds of the training data. If the network is classifying something novel it is more likely to make a problematic or incorrect decision so catching these occurrences is important in safety critical systems such as self-driving cars. One way to do this is through neuron activation pattern (NAP) monitoring. The details behind the monitors architecture will be discussed later. During training the monitor learns all the activation patterns of a given layer for each class. When the network is then deployed and classifies an image, the monitor can then test whether the activations for that image fit within the activation patterns of the chosen class. This new information can be used to decide whether to accept or reject the decision made by the network.

The goal of this project is to design a NAP monitor in python and then implement this NAP monitor on an image classification network trained on Tiny Imagenet. Performance of a NAP can be measured with three metrics: trigger rate, sensitivity, and pattern probability. Trigger rate is the rate the NAP finds an image out of pattern from its class. Sensitivity is how well the NAP detects a misclassification. Pattern probability is the probability that an out of pattern image indicates that the image is misclassified. These metrics will be used to evaluate the performance of the system.

There are many hyperparameters that can affect the performance of a NAP monitor: # of neurons, negative positive split, hamming distance, thresholding. The hypotheses and results for varying these parameters can be found below. By careful tuning of these hyperparameters we hypothesize that we can create two high performance monitors. A silent monitor that triggers at less than 5% but has a sensitivity of 10% and loud monitor that triggers less than 10% but has a sensitivity of 25%. We were able to create a monitor that triggers 5.04 % with a sensitivity of 10.8%. However we were not able to find suitable hyperparameters to design a lous monitor the best result for this task was found to be a monitor with a trigger rate of 17.61% and a sensitivity of 27.97%


## Method
### Data
The dataset used in this project was Tiny Imagenet. The dataset contains 100,000 training images, 10,000 validation images, and 10,000 test images. As the test images are not labeled we will use the validation dataset as the test and sample the training data for validation in this experiment. The data contains no overlap between classes.  Each image is 64x64 pixels and contains three channels for RGB with values ranging from 0-255. 

### Transfer Learning
A DenseNet model pretrained on the larger imagenet was modified by removing its head and adding a fully connected 200 neuron layer to serve as the classifier for the smaller dataset. A dropout of 0.5 was used and a scaled 224x224 version of the images was used as the input. No data augmentation was performed as the training set would need to be reused when training the NAP monitor. 

### NAP Monitor architecture
After model training the construction of the NAP monitor could begin. Due to computing restraints of Google Colab it was only possible to construct monitors and run experiments for the first 50 classes of the dataset out of 200 total classes. With more computing power this concept could easily be expanded to encompass all 200 classes.

In constructing this Monitor the last feature layer with shape 1024x1 was chosen. This layer contains high level features of the image and less spatial information so it is ideal for a NAP monitor.

Each monitor had the following components associated with it:

selected_indices:
This array contained the indices to select for monitoring from the larger 1024 array of activations. It is unique to each class.

bdd_patterns:
This is a bdd that stores all the different activation patterns associated with the class.


### Initialization
During initialization each class monitor is created and it's bdd_pattern set to empty. It is here that the indices are selected based on the hyperparameters. The weights between the 1024 layer and selected class are passed in during initialization. The weights are then sorted. The absolute value of the weight is an indicator for how much impact the activation has on deciding if the image is in the selected class. The number of indices selected is based on the hyperparameter # of neurons. The split hyper parameter decides how many of the neurons with the largest negative weight to select and how many of the neurons with the largest positive weight to select. Once initialized the indices remain constant throughout the training process.

### Training
We only train the NAP monitor on images that are correctly classified. During training the 1024 activations are calculated using a partial model that ends at the specified layer. The activations have already passed through a ReLU function so they are either positive or zero. These activations are then converted into a binary array. The threshold hyperparameter decides how large the activation needs to be to be considered a “1” in the binary array. The array is then passed into the class monitor which selects the specified indices and encodes it into the bdd.

After training if the hamming distance hyper parameter is specified. Then the monitor's patterns are looped through and extended by adding a new case where a selected variable can be true or false and still match a pattern. This is done efficiently using the architecture of the bdd.

### Testing
During runtime the 1024 activations are calculated using a partial model that ends at the specified layer. The activation is converted to a binary array and then is checked against the bdd of its predicted class. If a pattern match is found then the NAP returns true otherwise false.


## References

[1] Chih-Hong Cheng, Georg Nuhrenberg, and Hirotoshi Yasuoka. Runtime Monitoring Neuron Activation Patterns. CoRR https://arxiv.org/abs/1809.06573 

[2] K. S. Brace, R. L. Rudell and R. E. Bryant, Efficient implementation of a BDD package, 27th ACM/IEEE Design Automation Conference https://ieeexplore.ieee.org/abstract/document/114826/ 

[3] Gao Huang, Zhuang Liu, and Kilian Q. Weinberger. Densely Connected Convolutional Networks. CoRR https://arxiv.org/abs/1608.06993 

[4] Jiayu Wu, Qixiang Zhang, and Guoxi Xu. Tiny ImageNet Challenge.  http://cs231n.stanford.edu/reports/2017/pdfs/930.pdf 

