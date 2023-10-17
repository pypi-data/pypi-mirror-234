from enum import Enum

DEVICE = "cpu"


class Models(str, Enum):
    CLIP = "openai/clip-vit-base-patch32"
    XCEPTION = "keras.applications.xception"
    VGG16 = "keras.application.vgg16"
