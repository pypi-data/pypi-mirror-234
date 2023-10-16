# IDEA DINO and Grounding-DINO

## VENV

### "SAM"

dino/notebooks/zero_shot_object_detection_with_grounding_dino.ipynb


### "gdino"

All works under `gdino` shall use this environment.


### "samlabel"

`samlabel` environment contains PYPI wheels for `groundingDINO-py` and `hqsam`. My notebook `gdino/notebooks/text_annotate_02.ipynb` used this environment and this notebook provided good example how to do grounded-segment-anything.

2023.10.09 uninstalled `groundingdino-py` to use standalone module.

Under `/gdino`, to run my standalone groundingDINO inference, do

```bash
cd gdino
python infer.py
```

## Building `gddet` wheel

```bash
cd gdino
python setup.py sdist bdist_wheel
```

After that, deactive `samlabel` environment and activate `serve` environment to test pip installed module.


```bash
deactivate
source /home/hai/vv/serve/bin/activate
cd gdino/dist
pip install gddet-0.1.0-py3-none-any.whl
pip install addict yapf transformers timm

cd ../../gdino_wheel_test
python infer.py
```

### Upload

Refer to my stackedit note on 20200202

Under ENV `samlabel`,

```bash
pip install twine
cd gdino
twine check dist/*
twine upload dist/*
```

>Enter your username: H-AI
>Enter your password: X98
