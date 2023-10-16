{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "f713491a",
   "metadata": {},
   "source": [
    "conda install squidpy scanpy rpy2 scvelo adjusttext r-randomforest\n",
    "conda install entrain-spatial\n",
    "pip install tangram-sc\n",
    "pip install pypath-omnipath"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "4369048d",
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "import entrain as en\n",
    "import anndata as ad\n",
    "import scanpy as sc\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "feac8bf2",
   "metadata": {},
   "source": [
    "Load Data and Visualize"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "45452fe3",
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "# Zenodo Links\n",
    "velocity_adata_file = \"/Users/wk/Github/entrain_vignette_data/ratz_atlas_velocities_sparse.h5ad\"\n",
    "spatial_adata_file = \"/Users/wk/Github/entrain_vignette_data/v11_vis.h5ad\"\n",
    "ligand_target_matrix_file = \"/Users/wk/Github/entrain_vignette_data/ligand_target_matrix_mm.csv\"\n",
    "# velocity_adata_file = \"ratz_atlas_velocities_sparse.h5ad\"\n",
    "# spatial_adata_file = \"v11_vis.h5ad\"\n",
    "# ligand_target_matrix_file = \"/Users/wk/Github/entrain_vignette_data/ligand_target_matrix_mm.csv\"\n",
    "\n",
    "adata = ad.read_h5ad(velocity_adata_file)\n",
    "adata_st = ad.read_h5ad(spatial_adata_file)\n",
    "ligand_target_matrix = pd.read_csv(ligand_target_matrix_file, index_col=0)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c15e6567",
   "metadata": {},
   "source": [
    "Cluster Velocities"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "efc6c18b",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "adata = en.cluster_velocities(adata)\n",
    "en.plot_velocity_clusters_python(adata,\n",
    "                                 plot_file = \"velocity_clusters.png\",\n",
    "                                velocity_cluster_key = \"velocity_clusters\")\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "dded7234",
   "metadata": {
    "tags": []
   },
   "source": [
    "Recover Dynamics: Calculate velocity likelihoods via scvelo.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0c1f28c3",
   "metadata": {
    "scrolled": true,
    "tags": []
   },
   "outputs": [],
   "source": [
    "adata = en.recover_dynamics_clusters(adata, \n",
    "                              n_jobs = 10,\n",
    "                              return_adata = True, n_top_genes=None)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "48da8c8e",
   "metadata": {},
   "source": [
    "Run Entrain: The following function performs two steps: performs label transfer (via tangram) on the velocity clusters, followed by fitting a random forest model to the velocity likelihoods and ligand-target network,"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "eab667fb",
   "metadata": {
    "scrolled": true,
    "tags": []
   },
   "outputs": [],
   "source": [
    "adata_result=en.get_velocity_ligands_spatial(adata,\n",
    "                                             adata_st,\n",
    "                                             organism=\"mouse\",\n",
    "                                             annotation_key = \"velocity_clusters\",\n",
    "                                             ligand_target_matrix=ligand_target_matrix)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "de2dada9",
   "metadata": {},
   "source": [
    "Plot"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3b04930a",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "en.plot_velocity_ligands_python(adata_result,\n",
    "                                cell_palette=\"plasma\",\n",
    "                                velocity_cluster_palette = \"black\",\n",
    "                                color=\"velocity_clusters\",\n",
    "                                plot_output_path = \"plot_result1.png\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "debe513a",
   "metadata": {},
   "source": [
    "Step-by-step analysis: You may wish to perform label transfer separately from the ligand inference. For example if you would like to manually inspect the transferred labels before continuing."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "dc526710",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "adata_st_transfer = en.velocity_label_transfer(adata,\n",
    "                                               adata_st,\n",
    "                                               plot=\"label_transfer_plot.png\",\n",
    "                                               organism=\"mouse\",\n",
    "                                               tangram_result_column = \"velocity_label_transfer\",\n",
    "                                              velocity_cluster_key=\"velocity_clusters\")\n",
    "\n",
    "sc.pl.spatial(adata_st_transfer,\n",
    "              color=\"velocity_label_transfer\",\n",
    "              save = \"plot_labels.png\")\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "29e484fa-abf1-403a-b888-849b55a5c474",
   "metadata": {},
   "source": [
    "Here, we are happy with these transferred velocity clusters. You can now feed these labels back into `en.get_velocity_ligands_spatial()`. Make sure to specify `tangram_result_column =` and `adata_st =` to prevent redundant analysis."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "e4cf88d5",
   "metadata": {
    "scrolled": true,
    "tags": []
   },
   "outputs": [],
   "source": [
    "adata_result = en.get_velocity_ligands_spatial(adata,\n",
    "                                               adata_st = adata_st_transfer,\n",
    "                                               tangram_result_column = \"velocity_label_transfer\",\n",
    "                                               annotation_key = \"annot\",\n",
    "                                               ligand_target_matrix = ligand_target_matrix,\n",
    "                                               plot_output_path = \"plot_result2.png\")\n",
    "                                               \n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:anaconda3-pypi-test-entrain] *",
   "language": "python",
   "name": "conda-env-anaconda3-pypi-test-entrain-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
