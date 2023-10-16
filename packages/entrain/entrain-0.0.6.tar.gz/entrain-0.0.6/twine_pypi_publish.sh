mamba activate pypi-test-entrain

python3 -m build

python3 -m twine upload dist/*

# mamba install squidpy anndata scvelo scanpy rpy2
# python3 -m pip install --no-deps entrain
