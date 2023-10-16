mamba create -n pypi-test-entrain
mamba activate pypi-test-entrain

mamba install squidpy scanpy rpy2 scvelo adjusttext r-randomforest pytorch
# mamba install entrain-spatial

pip install tangram-sc
pip install pypath-omnipath
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps entrain_spatial_test18
