import entrain as en
import anndata as ad
import scanpy as sc
import pandas as pd
import scvelo as scv

# Zenodo Links
velocity_adata_file = "/Users/wk/Github/entrain_vignette_data/ratz_atlas_velocities_sparse.h5ad"
spatial_adata_file = "/Users/wk/Github/entrain_vignette_data/v11_vis.h5ad"
ligand_target_matrix_file = "/Users/wk/Github/entrain_vignette_data/ligand_target_matrix_mm.csv"
# velocity_adata_file = "ratz_atlas_velocities_sparse.h5ad"
# spatial_adata_file = "v11_vis.h5ad"
# ligand_target_matrix_file = "ligand_target_matrix_mm.csv"

adata = ad.read_h5ad(velocity_adata_file)
adata_st = ad.read_h5ad(spatial_adata_file)
ligand_target_matrix = pd.read_csv(ligand_target_matrix_file, index_col=0)

d = pd.read_csv("ratz_broadlabel_colors.csv", index_col=0)
broadlabel_palette = d.to_dict()['broad_label_color']
adata.uns["broad_label_palette"] = broadlabel_palette

scv.tl.recover_dynamics(adata, n_jobs=4)

'''

adata = en.cluster_velocities(adata, resolution=0.02)
en.plot_velocity_clusters_python(adata,
                                plot_file = "plot_velocity_clusters.png",
                                velocity_cluster_key = "velocity_clusters")

adata = en.recover_dynamics_clusters(adata, 
                              n_jobs = 10,
                              return_adata = True, n_top_genes=None)
adata_result=en.get_velocity_ligands_spatial(adata,
                                             adata_st,
                                             organism="mouse",
                                             velocity_cluster_key = "velocity_clusters",
                                             ligand_target_matrix=ligand_target_matrix)
en.plot_velocity_ligands_python(adata_result,
                                cell_palette="plasma",
                                velocity_cluster_palette = "black",
                                color="velocity_clusters",
                                plot_output_path = "plot_result1.png")
adata_result.write("ratz_entrain.h5ad")
'''
adata = ad.read_h5ad("ratz_entrain.h5ad")

adata_st_transfer = en.velocity_label_transfer(adata,
                                               adata_st,
                                               plot="label_transfer_plot.png",
                                               tangram_result_column = "velocity_label_transfer_1",
                                              velocity_cluster_key="velocity_clusters")

sc.pl.spatial(adata_st_transfer,
              color="velocity_label_transfer_1",
              save = "plot_labels.png")

adata_result = en.get_velocity_ligands_spatial(adata,
                                               adata_st = adata_st_transfer,
                                               tangram_result_column = "velocity_label_transfer_1",
                                               organism = "mouse",
                                               ligand_target_matrix = ligand_target_matrix)
en.plot_velocity_ligands_python(adata_result,
                                cell_palette="plasma",
                                velocity_cluster_palette = "black",
                                color="velocity_clusters",
                                plot_output_path = "plot_result2.png")
# plot

annotation_key = "broadlabel"
adata = en.recover_dynamics_clusters(adata,
                                     n_jobs = 10,
                                     cluster_key = annotation_key,
                                     return_adata = True)

adata_result=en.get_velocity_ligands_spatial(adata,
                                             adata_st,
                                             organism="mouse",
                                             velocity_cluster_key = annotation_key,
                                             tangram_result_column = "velocity_label_transfer_2",
                                             ligand_target_matrix=ligand_target_matrix)

en.plot_velocity_ligands_python(adata_result,
                                cell_palette="Set1",
                                tangram_result_column = "velocity_label_transfer_2",
                                velocity_cluster_palette = "black",
                                color = annotation_key,
                                plot_output_path = "plot_result3.png")
adata_result.write("ratz_entrain_broadlabel_clusters.h5ad")

adata = ad.read_h5ad("ratz_entrain_broadlabel_clusters.h5ad")
sc.set_figure_params(dpi=300, dpi_save=300, format="png")
sc.pl.umap(adata, color = annotation_key, palette = adata.uns["broad_label_palette"])

### draft
# plot the locations of the spots where the ligand is 1. expressed and 2. spatially proximal
# to the differentiating vcluster.

## testing
adata = ad.read_h5ad("/Users/wk/Github/entrain_draft/R/ratz/ratz_entrain_diet.h5ad")
adata_st = ad.read_h5ad("/Users/wk/Github/entrain_vignette_data/v11_vis.h5ad")
adata_st = en.velocity_label_transfer(adata,
                            adata_st,
                            velocity_cluster_key = "velocity_clusters",
                            tangram_result_column = "velocity_label_transfer")

top_n_ligands = 5
tangram_result_column = "velocity_label_transfer"
dpi=300
figsize = None
nrows=2
save = "ligand_spatial_influence.png"

##


