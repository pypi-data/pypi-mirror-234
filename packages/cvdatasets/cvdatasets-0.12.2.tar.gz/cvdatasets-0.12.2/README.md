# CV Datasets Wrapper

## Installation
```bash
pip install cvdatasets
```

Small addition: you can use this package to resize images in a fast way:
```bash
python -m cvdatasets.resize <src folder> <dest folder> --size 600
python -m cvdatasets.resize <src folder> <dest folder> --size 600 --fit_short
```
The first line resizes all images in `<src folder>` so that the larger size is `600px` and stores them to `<dest folder>`.
The second line does the same, except that the smaller size is `600px`.


## Motivation
We want to follow the interface of custom [PyTorch datasets](https://pytorch.org/tutorials/beginner/basics/data_tutorial.html#creating-a-custom-dataset-for-your-files) (originally presented by [Chainer](https://docs.chainer.org/en/latest/reference/generated/chainer.dataset.DatasetMixin.html#chainer.dataset.DatasetMixin)):

```python
class OurDataset(DatasetInterface):
    def __init__(self, *args, **kwargs):
        super().__init__()
        # read the data annotations, select proper split, etc.

    def __len__(self) -> int:
        return len(self.images)

    def __getitem__(self, index):
        # read the image and the according label
        # transform the image (e.g. with augmentations)
        return img, label
```

Additionally, we would like to add support for reading of part annotations (or bounding boxes, hierarchies, etc.) and select the correct dataset annotations based on command-line arguments.
The straight-forward way is to create a look-up file (we call it **data config file**) and store all required information there, e.g.:

```yaml
# data config file
BASE_DIR: /data/your_data_folder/

DATA_DIR: datasets

DATASETS:
    # each dataset is found as
    # <BASE_DIR>/<DATA_DIR>/<DATASET.folder>/<DATASET.annotation>
    CUB200:
        folder: birds
        annotations: cub200/ORIGINAL

    CUB200_2fold:
        folder: birds
        annotations: cub200/2fold

    NAB:
        folder: birds
        annotations: NAB/2fold

```

```python
# your data initialization code
data_config = "path/to/data/config_file.yml"
annot = Annnotation.load(data_config, dataset="CUB200")
train, test = annot.new_train_test_datasets()

# now we can create any data loader that supports the before-mentioned dataset API:
train_loader = DataLoader(train, batch_size=32)
test_loader = DataLoader(test, batch_size=32)
```

The advantage of this approach is that you can have different data config files for different environments, but your data initialization code remains the same.


## Basic usage
Now we dive a bit deeper into the actual usage examples:

### 1. Load annotations from a data config file
The example in the motivation section is already almost a working example.
We just need to modify the code a bit:

```python
from cvdatasets import AnnotationType
from munch import munchify

# this args can also be result of argparse's parse_args or any other data class
args = munchify(dict(data="path/to/data/config_file.yml", dataset="CUB200"))

annot = AnnotationType.new_annotation(args)
train, test = annot.new_train_test_datasets()
```

### 2. Load annotations without a data config file
Alternatively, you can create an annotation instance directly by pointing to a directory.
Hereby, we implemented *file list*, *folder*, and *JSON* annotations:

```python
from cvdatasets import FileListAnnotations
from cvdatasets import FolderAnnotations
from cvdatasets import JSONAnnotations

annot = FileListAnnotations(
    root_or_infofile="path/to/eg/CUB200",
    # this indicates which ID in the "tr_ID.txt" file is used for validation;
    # all other ids in this file will be assigned to the training split
    test_fold_id=0
)

annot = FolderAnnotations(
    root_or_infofile="ImageNet/has/folder/annotations",
    folders=dict( # < these are the default folders, where the different splits are selected on
        train_images="train",
        val_images="val",
        test_images=("test", True) # < "True" indicates that the test folder is optional
    )
)

annot = JSONAnnotations(root_or_infofile="iNaturalist/datasets/have/this")

# afterwards proceed as usual:
train, test = annot.new_train_test_datasets()
```

### 3. Load datasets based on a custom datasets class
Per default, the resulting dataset instances (`cvdatasets.dataset.Dataset`) will return a tuple of a numpy-array, parts (if present, otherwise `None`), and a label:
```python
im_array, parts, label = train[0]
```

There is a possibility to return an object (`cvdatasets.dataset.image.ImageWrapper`) holding a bunch of interesting information about the loaded image (e.g., a PIL instance of the image or the numpy representation):
```python
from cvdatasets.dataset import ImageWrapperDataset

train, test = annot.new_train_test_datasets(dataset_cls=ImageWrapperDataset)
im_obj = train[0]

pil_image = im_obj.im
numpy_array = im_obj.im_array

# there is a shortcut to get the same output as the default Dataset class
im_array, parts, label = im_obj.as_tuple()
```

Using the same idea, you can also define your own dataset class and perform everything you want with these outputs (including applying augmentations):

```python

from torch.utils.data import Dataset as BaseDataset
from torch.utils.data import DataLoader

from cvdatasets import FileListAnnotations
from cvdatasets import ImageWrapperDataset

class Dataset(ImageWrapperDataset, BaseDataset):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # inialize training and validation augmentations

    def __getitem__(self, i):
        im_obj = super().__getitem__(i)

        pil_im = im_obj.im
        label = im_obj.label

        aug_im = self.augment(pil_im)

        return aug_im, label

annot = FileListAnnotations(root_or_infofile="path/to/CUB200")
train, test = annot.new_train_test_datasets(dataset_cls=Dataset)

train_loader = DataLoader(train, batch_size=32)
test_loader = DataLoader(test, batch_size=32)
```

## Working with Part Annotations
Both datasets (NAB and CUB) have part annotations. Each annotation has for each of the predefined parts the location of this part and a boolean (`0` or `1`) value whether this part is visible. A [`Dataset`](cvdatasets/dataset/__init__.py) instance returns besides the image and the class label this information:

```python

im, parts, label = train_data[100]

print(parts)
# array([[  0, 529, 304,   1],
#        [  1, 427, 277,   1],
#        [  2, 368, 323,   1],
#        [  3,   0,   0,   0],
#        [  4, 449, 292,   1],
#        [  5, 398, 502,   1],
#        [  6, 430, 398,   1],
#        [  7,   0,   0,   0],
#        [  8, 365, 751,   1],
#        [  9,   0,   0,   0],
#        [ 10,   0,   0,   0]])
...
```



### Visible Parts

In order to filter by only visible parts use the [`visible_locs`](cvdatasets/dataset/part.py#L46) method. It returns the indices and the x-y positions of the visible parts:

```python
...

idxs, xy = parts.visible_locs()

print(idxs)
# array([0, 1, 2, 4, 5, 6, 8])
print(xy)
# array([[529, 427, 368, 449, 398, 430, 365],
#        [304, 277, 323, 292, 502, 398, 751]])

x, y = xy
plt.imshow(im)
plt.scatter(x,y, marker="x", c=idxs)
plt.show()
```

### Uniform Parts
In case you don't want to use the ground truth parts, you can generate parts uniformly distributed over the image. Here you need to pass the image as well as the ratio, which tells how many parts will be extracted (ratio of `1/5` extracts 5 by 5 parts, resulting in 25 parts). In case of uniform parts all of them are visible.


```python
...
from cvdatasets.dataset.part import UniformParts

parts = UniformParts(im, ratio=1/3)
idxs, xy = parts.visible_locs()

print(idxs)
# array([0, 1, 2, 3, 4, 5, 6, 7, 8])
print(xy)
# array([[140, 420, 700, 140, 420, 700, 140, 420, 700],
#        [166, 166, 166, 499, 499, 499, 832, 832, 832]])

x, y = xy
plt.imshow(im)
plt.scatter(x,y, marker="x", c=idxs)
plt.show()
...
```

### Crop Extraction
From the locations we can also extract some crops. Same as in [`UniformParts`](cvdatasets/dataset/part.py#L76) you have to give a ratio with which the crops around the locations are created:

```python
...

part_crops = parts.visible_crops(im, ratio=0.2)

fig = plt.figure(figsize=(16,9))
n_crops = part_crops.shape[0]
rows = int(np.ceil(np.sqrt(n_crops)))
cols = int(np.ceil(n_crops / rows))

for j, crop in enumerate(part_crops, 1):
    ax = fig.add_subplot(rows, cols, j)
    ax.imshow(crop)
    ax.axis("off")

plt.show()
...
```


### Random Crops
In some cases randomly selected crops are desired. Here you can use the [`utils.random_index`](cvdatasets/utils/__init__.py#L3) function. As optional argument you can also pass a `rnd` argument, that can be an integer (indicating a random seed) or a `numpy.random.RandomState` instance. Additionally, you can also determine the number of crops that will be selected (default is to select random number of crops).

```python
...
from cvdatasets import utils
import copy

part_crops = parts.visible_crops(im, ratio=0.2)
idxs, xy = parts.visible_locs()

rnd_parts = copy.deepcopy(parts)
rnd_idxs = utils.random_idxs(idxs, rnd=rnd, n_parts=n_parts)
rnd_parts.select(rnd_idxs)
# now only selected parts are visible
rnd_part_crops = rnd_parts.visible_crops(im, ratio=0.2)

fig = plt.figure(figsize=(16,9))

n_crops = part_crops.shape[0]
rows = int(np.ceil(np.sqrt(n_crops)))
cols = int(np.ceil(n_crops / rows))

for j, crop in zip(rnd_idxs, rnd_part_crops):
    ax = fig.add_subplot(rows, cols, j + 1)
    ax.imshow(crop)
    ax.axis("off")

plt.show()
...
```


### Revealing of the Parts
In order to create a single image, that consist of the given parts on their correct location use [`reveal`](cvdatasets/dataset/part.py#L58) function. It requires again besides the original image and the locations the ratio with which the parts around the locations should be revealed:

```python

plt.imshow(parts.reveal(im, ratio=0.2))
plt.show()

plt.imshow(rnd_parts.reveal(im, ratio=0.2))
plt.show()
```


## Hierarchies
Hierachy file is currently only loaded. Code for proper processing is needed!
