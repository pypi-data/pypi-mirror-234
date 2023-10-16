    
import anndata as ad
import scvelo as scv
import scanpy as sc
import squidpy as sq
import numpy as np
import pandas as pd
import tangram as tg
import matplotlib.pyplot as plt
import math, sys, os
from .entrain_spatial import *

def plot_ligand_spatial_expression(
        adata,
        adata_st,
        velocity_clusters,
        top_n_ligands = 5,
        tangram_result_column = "velocity_label_transfer",
        figsize = None,
        nrows=2,
        save = "ligand_spatial_influence.png",
        dpi=300):

    entrain_result = adata.uns["entrain_velocity_ligands"]
    ligand_df = entrain_result["vclust_ligand_importances"]
    var_exp_df = entrain_result["variance_explained"]

    if velocity_clusters is None:
        # get default positive v.e. clusters
        velocity_clusters = var_exp_df.loc[var_exp_df.var_exp > 0, "velocity_clusters"].to_list()
    else:
        if np.all(np.isin(velocity_clusters, adata_st.obs[tangram_result_column].unique())):
            clusters = velocity_clusters
        else:
            raise ValueError(velocity_clusters + "not found in values of column: " + tangram_result_column)
        # set up matplotlib plots

    fig = plt.figure()
    ax = []
    n_clusters = len(velocity_clusters)
    nrows = 1 if n_clusters < 5 else 1 + (math.floor(n_clusters / 4) )
    ncols = n_clusters if n_clusters < 4 else 4
    ax = []
        
    figsize = figsize if figsize is not None else (8*ncols, 8*nrows)
    gs = plt.GridSpec(nrows,
                      ncols,
                      plt.figure(figsize=figsize)
                      ) 
    
    for i,vcluster in enumerate(velocity_clusters):
        vcluster_result = ligand_df.loc[:,["ligand",vcluster]].sort_values(by = vcluster, ascending=False)
        lig_names = vcluster_result.head(top_n_ligands)["ligand"].to_list()
        lig_weights = vcluster_result.head(top_n_ligands)[vcluster].to_numpy()
        
        lig_expr = adata_st[:, lig_names].X.toarray()

        # weighted average expression, weighted by entrain importance.
        if not np.isclose(np.sum(lig_weights), 1):
            lig_weights = lig_weights / np.sum(lig_weights)
        weighted_avg = np.einsum('ij,j->i', lig_expr, lig_weights)
                
        # get cells adjacent to vcluster cells.
        cell_names = adata_st.obs[np.isin(adata_st.obs[tangram_result_column], vcluster)].index.values
        if adata_st.obsp["spatial_connectivities"] is not None:
            adj_cell_idx = get_adjacent_cells(adata_st, cell_names_oi=cell_names)
        else:
            raise ValueError("Please run `squidpy.gr.spatial_neighbors(adata_st)` to calculate spatial connectivities")
        
        weighted_avg[~adj_cell_idx] = 0
        col_name = "ligand_average_expression_" + vcluster
        adata_st.obs[col_name] = weighted_avg
        
        gs_row = math.floor(i/4)
        gs_col = i % 4
        ax.append(
            sc.pl.spatial(adata_st,
                      color = col_name,
                      ax=plt.subplot(gs[gs_row,gs_col]),
                      show=False)[0]
            )

    ax[0].figure.savefig(save, dpi=dpi)
    
    print("Saved at "+ os.getcwd() + "/" + save)
    return ax


# The influence of cell types positioned next to a given velocity cluster, where influence
# is the summed expression of the top n ligands weighted by their variable_importance
# to that velocity cluster.
def plot_influence_proportions(
	adata,
	adata_st,
    tangram_celltype_column,
    tangram_result_column  = 'velocity_label_transfer',
	celltype_key = "broadlabel",
	velocity_cluster_key = "velocity_clusters",
    top_n_ligands=5,
    positive_ve_only=True,
	color = None,
    colormap=None,
    save = "cell_influence_proportions.png",
    dpi=300,

  ):
    if celltype_key not in adata.obs.columns:
        raise ValueError("cluster_key not found in adata.obs.columns")
    if velocity_cluster_key not in adata.obs.columns:
        raise ValueError("velocity_cluster_key not found in adata.obs.columns")
    
    if tangram_celltype_column not in adata_st.obs.columns:
        adata_st = velocity_label_transfer(adata,
                                                       adata_st,
                                                       tangram_result_column = tangram_celltype_column,
                                                       velocity_cluster_key=celltype_key)
    
    if tangram_result_column not in adata_st.obs.columns:
        adata_st = velocity_label_transfer(adata,
                                                       adata_st,
                                                       tangram_result_column = tangram_result_column,
                                                       velocity_cluster_key = velocity_cluster_key)
    
    entrain_result = adata.uns["entrain_velocity_ligands"]
    ve_df = entrain_result["variance_explained"]
    imps_df = entrain_result["vclust_ligand_importances"]
    
    if positive_ve_only:
        vclusters = ve_df.loc[ve_df["var_exp"] > 0, velocity_cluster_key]
    else:
        vclusters = np.sort(adata_st.obs[tangram_result_column].unique())
    
    result = pd.DataFrame(columns = [tangram_celltype_column, "weighted_sum", velocity_cluster_key])
    for vc in vclusters:
        vc_spots = adata_st.obs_names[adata_st.obs[tangram_result_column] == vc]
        adata_vc = adata_st[vc_spots,:]
        
        
        # ligands to consider
        top_ligand_df = imps_df.loc[:,["ligand", vc]].sort_values(vc, ascending=False).head(top_n_ligands)
        top_ligands = top_ligand_df["ligand"]
        top_imps = top_ligand_df[vc].values
        # cells in proximity: 
        if "spatial_connectivities" not in adata_st.obsp.keys():
            try:
                sq.gr.spatial_neighbors(adata_st)
            except:
                raise KeyError("spatial_connectivities not found in adata_st.obsp. Please run squidpy.gr.spatial_neighbors() on adata_st")          
                
        adj_cells_bool = get_adjacent_cells(adata_st, vc_spots)
        adj_cells_names = adata_st.obs_names[adj_cells_bool]
        adj_ligand_mtrx = adata_st[adj_cells_names, top_ligands].X.todense()
        summed_avg_expr = np.multiply(adj_ligand_mtrx, top_imps).sum(axis=1)
        
        summed_avg_expr_df = pd.DataFrame(summed_avg_expr)
        summed_avg_expr_df.index = adj_cells_names
        summed_avg_expr_df.columns = [vc]
        
        df = pd.merge(summed_avg_expr_df, adata_st.obs[tangram_celltype_column],
                 how="left",
                 left_index=True, right_index=True)
        
        df_wsum = df.groupby(tangram_celltype_column)[vc].sum().reset_index()
        df_wsum.columns = [tangram_celltype_column, 'weighted_sum']
        df_wsum["weighted_sum"] = df_wsum["weighted_sum"]/np.sum(df_wsum["weighted_sum"])
        df_wsum[velocity_cluster_key] = vc
        
        result = pd.concat([result, df_wsum])
        
    pivot_df = result.pivot_table(values='weighted_sum', index=velocity_cluster_key, columns=tangram_celltype_column, aggfunc='sum')
    pivot_df = pivot_df.fillna(0)
    ax=pivot_df.plot(kind='barh',
                  stacked=True,
                  figsize=(10,7),
                  width = 0.8,
                  color=color,
                  colormap=colormap)
    plt.title('Cell Type Influence on Velocities')
    plt.xlabel('Velocity Clusters')
    plt.ylabel('Cell Type Contributions')
    ax.figure.savefig(save, dpi=dpi)
    print("Saved at "+ os.getcwd() + "/" + save)
    
    return ax

