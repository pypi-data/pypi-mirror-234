# cvmodelz

*"Why is it written with 'z'? Because 'cvmodels' already exists ¯\\\_(ツ)\_/¯"*

This is a package for fast and easy loading of `chainer` models.
It also supports chainercv and chainercv2 models.

## Installation
```bash
pip install cvmodelz
```

## Built-in scripts

```bash
python -m cvmodelz.model_info cvmodelz.InceptionV3
python -m cvmodelz.model_info cvmodelz.InceptionV3 -size 427 --device 0
python -m cvmodelz.model_info cvmodelz.ResNet50 -size 448 --device 0
```

## Basic Usage
```python
from cvmodelz.models import ModelFactory

model = ModelFactory.new("cvmodelz.ResNet50", input_size=224)
print(model.meta)
# ModelInfo:
#   name: ResNet50
#   input_size: 224
#   feature_size: 2048
#   n_conv_maps: 2048
#   conv_map_layer: res5
#   feature_layer: pool5
#   classifier_layers:
#     - fc6
#   prepare_func: '<bound method BaseResNet.prepare of <cvmodelz.models.pretrained.resnet.ResNet50
#     object at 0x7fa037f13f70>>'
print(model.clf_layer)
# Linear(in_size=2048, out_size=1000, nobias=False)

```

You can also easily use the class methods `ModelFactory.get_all_models` and `ModelFactory.get_models` to restrict the options in argparse:

```python
from cvmodelz.models import ModelFactory

print("\n".join(ModelFactory.get_all_models()))
# chainer.ResNet50Layers
# chainer.ResNet101Layers
# chainer.ResNet152Layers
# chainercv.SSD300
# chainercv.FasterRCNNVGG16
# chainercv2.resnet50
# chainercv2.resnet18
# chainercv2.inceptionv3
# chainercv2.inceptionresnetv1
# chainercv2.resnext50_32x4d
# cvmodelz.VGG16
# cvmodelz.VGG19
# cvmodelz.ResNet35
# cvmodelz.ResNet35HD
# cvmodelz.ResNet50
# cvmodelz.ResNet50HD
# cvmodelz.ResNet101
# cvmodelz.ResNet152
# cvmodelz.InceptionV3
# cvmodelz.InceptionV3HD


import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--model_type", choices=ModelFactory.get_models())
# or restrict it to particular modules:
parser.add_argument("--model_type", choices=ModelFactory.get_models(["chainercv2", "cvmodelz"]))

args = parser.parse_args()

model = ModelFactory.new(args.model_type)
```

Models from the `cvmodelz` package have a method to preprocess an input so it fits the pixel values:

```python
import numpy as np

from cvmodelz.models import ModelFactory

incv3 = ModelFactory.new("cvmodelz.InceptionV3")

array = np.random.randint(0, 255, size=(1080, 1920, 3)).astype(np.uint8)

print(incv3.prepare(array).shape)
# (3, 299, 299)
print(incv3.prepare(array, keep_ratio=True).shape)
# (3, 299, 531)
print(incv3.prepare(array, size=427, keep_ratio=True).shape)
# (3, 427, 759)

x = incv3.prepare(array, keep_ratio=True)
print(x.min(), x.max(), x.dtype)
# 0.00030062173 0.9944885 float32
print(array.min(), array.max(), array.dtype)
# 0 225 uint8
```

## Classifiers
The model objects returned by the `ModelFactory` are "just" backbones that can be used in a classifier object:
```python
from cvmodelz.models import ModelFactory
from cvmodelz.classifiers import Classifier

model = ModelFactory.new("cvmodelz.InceptionV3")

clf = Classifier(model=model)
```

The main ideas behind this separation are the following:
* In the forward pass, the classifier object is responsible for (1) calling the model, (2) computing the evaluation metrics, and (3) computing the loss and returning it, so it can be minimized by an updater.
* `cvmodelz.classifiers.SeparateClassifier` can be used instead of the default classifier class, which then creates a duplicate of the given model. By overriding the `forward` method, one can for example easily implement a global- and part-based classification.
* The loading of the weights is abstracted away in the different implementations but also gives the possibility to override this behavior (see `cvmodelz.classifiers.base.Classifier.load` method for further information).

