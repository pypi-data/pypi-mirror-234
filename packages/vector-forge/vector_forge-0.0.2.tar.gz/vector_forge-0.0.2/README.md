<p align="center">
  <img src="assets/logo.png" alt="Vector Forge Logo" width="110">
</p>
<p align="center">
  <a href="https://www.python.org/downloads/release/python-3110/" target="_blank">
      <img src="https://img.shields.io/badge/Python->3.10-blue?logo=python" alt="Python > 3.11">
  </a>
</p>
<p align="center">
  <i>🐍 Vector Forge is a Python package designed for easy transformation of various data types into feature vectors.</i>
</p>

---

<p align="center">
  <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"
      alt="Python">
  </a>
  <a href="https://pytorch.org/">
      <img src="https://img.shields.io/badge/PyTorch-orange.svg?&style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch"/>
  </a>
  <a href="https://keras.io/">
      <img src="https://img.shields.io/badge/Keras-005571?style=for-the-badge&logo=keras" alt="Keras">
  </a>
</p>

---

## 💡Core ideas

🌄 For image embeddings, Vector Forge uses pre-trained networks, which means the models have already learned features
from
a large set of images called [ImageNet](https://www.image-net.org/). When we use these models in Vector Forge, we skip
the part that
identifies objects, and instead, we use
the part that understands the image features. This way, we get a bunch of numbers (a vector) representing the image,
which can be used
in many different tasks like finding similar images, clustering, classification and many more.

📄 Text embeddings are a way to convert words or sentences into numbers, making it possible for computers to understand
and
process them. In Vector Forge, the [CLIP ViT-B/32](https://huggingface.co/openai/clip-vit-base-patch32) model is
utilized to generate these embeddings. When you provide any text, be it
a single word or a sentence, to CLIP, it transforms this text into a fixed-size vector. Each vector has a consistent
length, no matter how long or short the original text is. This consistency in size is valuable, especially when
comparing different pieces of text or measuring how similar a piece of text is to an image.

## 🧩 Features

- **Image to Vector conversion**: Easily convert individual images into feature vectors by specifying your desired model
  to extract meaningful representations.
- **Batch processing**: Provide a folder path to process multiple images in bulk. Select your preferred model and let
  Vector Forge swiftly handle all the images in the specified directory.
- **Text to Vector transformation**: Effortlessly convert textual data into vectors. Choose your model, and Vector Forge
  will transform your text input into a high-dimensional vector representation.
- **Support for multiple models**: Vector Forge supports various models for vectorization, including CLIP, Xception, and
  VGG16, to provide flexibility in handling different data types.

## ⚙️ Requirements

- [Python >= 3.10](https://www.python.org/downloads/release/python-31012/)

## 📦 Supported models

|                              Model Name                              |         Implementation          |   Parameter Value    | Supports Image | Supports Text | Embedding Size |
|:--------------------------------------------------------------------:|:-------------------------------:|:--------------------:|:--------------:|:-------------:|:--------------:|
| [CLIP ViT-B/32](https://huggingface.co/openai/clip-vit-base-patch32) | [PyTorch](https://pytorch.org/) |   `vf.Models.CLIP`   |       ✅        |       ✅       |     (512,)     |
|               [VGG16](https://arxiv.org/abs/1409.1556)               |   [Keras](https://keras.io/)    |  `vf.Models.VGG16`   |       ✅        |       ❌       |    (2048,)     |
|       [Xception](https://keras.io/api/applications/xception/)        |   [Keras](https://keras.io/)    | `vf.Models.XCEPTION` |       ✅        |       ❌       |    (2048,)     |

## 🎛️ Usage

You can work on many pictures at once or just one piece of text with simple commands, making it a breeze to get your
data ready for further use or analysis

### 🔧 Installation

```shell
pip install vector_forge
```

### 🔌 Create a vectorizer

#### Import the library

```python
import vector_forge as vf
```

#### Default vectorizer

By default, the vectorizer is [CLIP ViT-B/32](https://huggingface.co/openai/clip-vit-base-patch32), as it works for text
and images.

```python
vectorizer = vf.Vectorizer()  
```

#### Text to Vector

Example how to convert a text prompt to a vector.

```python
text_embedding = vectorizer.text_to_vector("Nice text!")
```

#### Image to Vector

Example how to convert to convert image from path to vector.

```python
image_embedding = vectorizer.image_to_vector("/path/to/image.jpg")
```

#### Change the vectorizer to use a different model

Example how to change the vectorizer model, in this example
to [Xception](https://keras.io/api/applications/xception/).  
Keep in mind, that not all models work for for text prompts. If you want to compare image and texts, I recommend
using [CLIP ViT-B/32](https://huggingface.co/openai/clip-vit-base-patch32).

```python
vectorizer = vf.Vectorizer(model=vf.Models.XCEPTION)
```

#### Return types

In Vector Forge, you have the flexibility to choose the format in which the vectors are returned. This is controlled by
the `return_type` parameter available in the `image_to_vector` and `text_to_vector` methods of the Vectorizer
class. Here are
the available return types along with examples:

a) **return_type="numpy"**

This is the default return type. Vectors are returned as [NumPy](https://numpy.org/doc/stable/index.html) arrays.

```python
image_embedding = vectorizer.image_to_vector("/path/to/image.jpg", return_type="numpy")
# Output: array([0.0234, 0.0345, ..., 0.0456])
# Shape: (2048,)  # for Xception and VGG16, (512,) for CLIP
```

b) **return_type="str"**

Vectors are returned as a string representation of the NumPy array.

```python
image_embedding = vectorizer.image_to_vector("/path/to/image.jpg", return_type="str")
# Output: "[0.0234, 0.0345, ..., 0.0456]"
```

c) **return_type="list"**

Vectors are returned as a list of values.

```python
image_embedding = vectorizer.image_to_vector("/path/to/image.jpg", return_type="list")
# Output: [0.0234, 0.0345, ..., 0.0456]
```

d) **return_type="2darray"**

Vectors are returned as a 2-dimensional NumPy array, where each vector is a row in the array. This format is especially
useful when you want to compute similarities or perform other vectorized operations.

```python
image_embedding = vectorizer.image_to_vector("/path/to/image.jpg", return_type="2darray")
# Output: array([[0.0234, 0.0345, ..., 0.0456]])
# Shape: (1, 2048)  # for Xception and VGG16, (1, 512) for CLIP
```

#### Batch Processing for images

Vector Forge can process multiple images in a folder in one go. Just provide the folder path, and the `load_from_folder`
method will handle the rest.

```python
# Convert all valid images in a folder to vectors
for vector in vectorizer.load_from_folder("/path/to/folder"):
    print(vector.shape)
```

You can specify the return_type and width parameters to control the output format and the width to which images should
be resized, respectively.

```python
# Example with return_type and width parameters
for vector in vectorizer.load_from_folder("/path/to/folder", return_type="str", width=300):
    print(vector)  # Each vector is now a string and images are resized to a width of 300 pixels.
```

### 🧪 A complete example

```python
import vector_forge as vf
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity(vectorizer, text, image_path):
    # Convert text and image to vectors with return type '2darray'
    text_embedding = vectorizer.text_to_vector(text, return_type="2darray")
    image_embedding = vectorizer.image_to_vector(image_path, return_type="2darray")

    # Compute cosine similarity
    similarity = cosine_similarity(text_embedding, image_embedding)[0][0]
    return similarity


# Create a vectorizer with the default CLIP model
vectorizer = vf.Vectorizer()

# Define text and image paths
text = "A couple of birds"
image_path_1 = "vector_forge/test_data/birds.jpg"
image_path_2 = "vector_forge/test_data/sample.jpg"

# Compute and print similarity scores
similarity_1 = compute_similarity(vectorizer, text, image_path_1)
similarity_2 = compute_similarity(vectorizer, text, image_path_2)

print(f"Similarity between text and first image: {similarity_1}")
print(f"Similarity between text and second image: {similarity_2}")
```

## 🔮 Future features

### New image models

[ ] Add support for VGG19

### New text models

[ ] Add support for GloVe
