import os

import cv2
import numpy as np
import torch

from .constants import Models

# Check if GPU available
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class Vectorizer:
    """
    Vectorizer class for converting images and text into vector representations
    using specified models like CLIP, Xception, and VGG16.

    Attributes:
        model (Models): The model to be used for vectorization.
        model_instance (Model): The instance of the specified model.
        processor (CLIPProcessor, optional): Processor for CLIP model, if applicable.
    """

    def __init__(self, model: Models = Models.CLIP):
        """
        Initializes the Vectorizer with the specified model.

        Args:
            model (Models, optional): The model to be used for vectorization.
                                      Defaults to Models.CLIP.
        """
        self.model = model
        if model == Models.CLIP:
            from transformers import CLIPProcessor, CLIPTokenizerFast, CLIPModel

            self.processor = CLIPProcessor.from_pretrained(model.value)
            self.model_instance = CLIPModel.from_pretrained(model.value).to(DEVICE)
        elif model == Models.XCEPTION:
            from tensorflow.keras.applications import Xception  # lazy loading

            self.model_instance = Xception(
                weights="imagenet", include_top=False, pooling="avg"
            )
        elif model == Models.VGG16:
            from tensorflow.keras.applications import VGG16  # lazy loading

            self.model_instance = VGG16(
                weights="imagenet", include_top=False, pooling="avg"
            )
        else:
            raise ValueError(f"Unsupported model: {model}")

    def image_to_vector(
        self,
        input_image: str | np.ndarray,
        return_type: str = "numpy",
        width: int = 600,
    ) -> np.ndarray | str | list:
        """
        Converts an image to a vector representation using the specified model.

        Args:
            input_image (str | np.ndarray): Path to the image or a NumPy array of the image.
            return_type (str, optional): The format in which to return the vector.
                                          Options are "numpy", "str", "list", or "2darray".
                                          Defaults to "numpy".
            width (int, optional): The width to which the image should be resized.
                                    Defaults to 600.

        Returns:
            np.ndarray | str | list: The vector representation of the image.
        """
        if self.model == Models.CLIP:
            # Convert to NumPy if image path
            input_image = self._prepare_image(input_image, width)
            image_tensor = self.processor(
                text=None, images=input_image, return_tensors="pt"
            )["pixel_values"]
            img_emb = self.model_instance.get_image_features(image_tensor)
        elif self.model == Models.XCEPTION:
            input_image = self._prepare_image_xception(input_image, width)
            img_emb = self.model_instance.predict(input_image)
        elif self.model == Models.VGG16:
            input_image = self._prepare_image_vgg16(input_image, width)
            img_emb = self.model_instance.predict(input_image)
        else:
            raise ValueError(f"Unsupported model: {self.model}")

        result = self._process_result(img_emb, return_type)
        return result

    def text_to_vector(
        self, input_text: str, return_type: str = "numpy"
    ) -> np.ndarray | str | list:
        """
        Converts a given text to a vector representation using the specified model.

        Args:
            input_text (str): The text to be vectorized.
            return_type (str, optional): The format in which to return the vector.
                                          Options are "numpy", "str", "list", or "2darray".
                                          Defaults to "numpy".

        Returns:
            np.ndarray | str | list: The vector representation of the text.
        """
        if self.model == Models.CLIP:
            from transformers import CLIPTokenizerFast

            tokenizer = CLIPTokenizerFast.from_pretrained(self.model.value)
            inputs = tokenizer(input_text, return_tensors="pt")
            text_emb = self.model_instance.get_text_features(**inputs)
            result = text_emb[0].cpu().detach().numpy()
        else:
            raise ValueError(f"Unsupported model for text: {self.model}")

        result /= np.linalg.norm(result, axis=0)
        if return_type == "numpy":
            return result
        elif return_type == "2darray":
            return result[np.newaxis, :]
        elif return_type == "list":
            return result.tolist()
        elif return_type == "str":
            return np.array2string(result, separator=", ").replace("\n", "")
        else:
            raise ValueError(f"Unsupported return type: {return_type}")

    @staticmethod
    def _prepare_image(input_image: str | np.ndarray, width: int) -> np.ndarray:
        """
        Prepares the input image for vectorization by resizing it to the specified width
        while maintaining the aspect ratio.

        Args:
            input_image (str | np.ndarray): Path to the image or a NumPy array of the image.
            width (int): The width to which the image should be resized.

        Returns:
            np.ndarray: The resized image.
        """
        if isinstance(input_image, str):
            if not os.path.exists(input_image):
                raise FileNotFoundError(f"File {input_image} does not exist!")
            input_image = cv2.imread(input_image)
        r = width / input_image.shape[1]
        dim = (width, int(input_image.shape[0] * r))
        return cv2.resize(
            input_image,
            dim,
            interpolation=cv2.INTER_AREA
            if width < input_image.shape[1]
            else cv2.INTER_LANCZOS4,
        )

    def _prepare_image_xception(
        self, input_image: str | np.ndarray, width: int
    ) -> np.ndarray:
        """
        Prepares the input image for vectorization using the Xception model
        by resizing and preprocessing it.

        Args:
            input_image (str | np.ndarray): Path to the image or a NumPy array of the image.
            width (int): The width to which the image should be resized.

        Returns:
            np.ndarray: The preprocessed image ready for vectorization with Xception.
        """
        from tensorflow.keras.applications.xception import (
            preprocess_input,
        )  # Lazy import
        from tensorflow.keras.preprocessing import image as keras_image

        input_image = self._prepare_image(input_image, width)
        input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
        input_image = keras_image.array_to_img(input_image)
        input_image = keras_image.img_to_array(input_image)
        input_image = np.expand_dims(input_image, axis=0)
        input_image = preprocess_input(
            input_image
        )  # This is where preprocess_input is used
        return input_image

    def _prepare_image_vgg16(
        self, input_image: str | np.ndarray, width: int
    ) -> np.ndarray:
        """
        Prepares the input image for vectorization using the VGG16 model
        by resizing and preprocessing it.

        Args:
            input_image (str | np.ndarray): Path to the image or a NumPy array of the image.
            width (int): The width to which the image should be resized.

        Returns:
            np.ndarray: The preprocessed image ready for vectorization with VGG16.
        """
        from tensorflow.keras.applications.vgg16 import (
            preprocess_input as vgg16_preprocess_input,
        )
        from tensorflow.keras.preprocessing import image as keras_image

        input_image = self._prepare_image(input_image, width)
        input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
        input_image = keras_image.array_to_img(input_image)
        input_image = keras_image.img_to_array(input_image)
        input_image = np.expand_dims(input_image, axis=0)
        input_image = vgg16_preprocess_input(input_image)
        return input_image

    def _process_result(self, result, return_type: str) -> np.ndarray | str | list:
        """
        Processes the result vector based on the specified return type.

        Args:
            result (np.ndarray): The vector to be processed.
            return_type (str): The format in which to return the vector.
                               Options are "numpy", "str", "list", or "2darray".

        Returns:
            np.ndarray | str | list: The processed vector.
        """
        result = (
            result[0].cpu().detach().numpy() if self.model == Models.CLIP else result[0]
        )
        result /= np.linalg.norm(result, axis=0)
        if return_type == "str":
            return np.array2string(result, separator=", ")
        elif return_type == "list":
            return result.tolist()
        elif return_type == "numpy":
            return result
        elif return_type == "2darray":
            return result[np.newaxis, :]
        else:
            raise ValueError(f"Unsupported return type: {return_type}")

    def load_from_folder(
        self, folder: str, return_type: str = "numpy", width: int = 600
    ):
        """
        Loads images from a specified folder, converts them to vectors,
        and yields the vectors one by one.

        Args:
            folder (str): Path to the folder containing images.
            return_type (str, optional): The format in which to return the vectors.
                                          Options are "numpy", "str", "list", or "2darray".
                                          Defaults to "numpy".
            width (int, optional): The width to which images should be resized.
                                    Defaults to 600.

        Yields:
            np.ndarray | str | list: The vector representation of each image.
        """
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                # Attempt to read the file as an image
                img = cv2.imread(file_path)
                if img is not None:
                    vector = self.image_to_vector(
                        file_path, return_type=return_type, width=width
                    )
                    yield vector
