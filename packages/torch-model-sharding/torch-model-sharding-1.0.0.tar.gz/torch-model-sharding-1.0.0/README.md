# torch-model-sharding

## install

```bash
pip install torch-model-sharding==1.0.0
```

## how to use

```bash
torch-model-sharding --source_file=/path/to/torch/pt/file --sharding_factor=3 --target_dir=/path/to/target/directory
```

## dev

```bash
## build
python3 setup.py sdist

## publish
twine upload dist/*

```

```

```
