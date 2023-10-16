import numpy as np
import torch
from PIL import Image
from collections import OrderedDict
from .slconfig import SLConfig
from .groundingdino import MODULE_BUILD_FUNCS
from .transforms import Compose, ToTensor, Normalize, RandomResize


def build_model(args):

    assert args.modelname in MODULE_BUILD_FUNCS._module_dict
    build_func = MODULE_BUILD_FUNCS.get(args.modelname)
    model = build_func(args)
    return model


def clean_state_dict(state_dict):
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        if k[:7] == "module.":
            k = k[7:]  # remove `module.`
        new_state_dict[k] = v
    return new_state_dict


def load_model(model_config_path: str, model_checkpoint_path: str):
    args = SLConfig.fromfile(model_config_path)
    model = build_model(args)
    checkpoint = torch.load(model_checkpoint_path, map_location="cpu")
    model.load_state_dict(clean_state_dict(checkpoint["model"]), strict=False)
    model.eval().cuda()
    return model


def pp_image(image: np.ndarray) -> torch.Tensor:
    transform = Compose(
        [
            RandomResize([800], max_size=1333),
            ToTensor(),
            Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    image_transformed, _ = transform(Image.fromarray(image), None)
    return image_transformed
