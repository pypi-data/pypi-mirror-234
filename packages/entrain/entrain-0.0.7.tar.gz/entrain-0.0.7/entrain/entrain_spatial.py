
import anndata as ad
import scvelo as scv
import scanpy as sc
import squidpy as sq
import numpy as np
import pandas as pd
import tangram as tg
import matplotlib.pyplot as plt
from pypath.utils import homology
from omnipath.interactions import import_intercell_network
from pypath.utils import mapping
import math, sys, os
import rpy2.robjects as robjects
from rpy2.robjects import numpy2ri
from rpy2.robjects import pandas2ri
from rpy2.robjects import default_converter
from .entrain_scvelo import cluster_velocities
from .entrain_scvelo import recover_dynamics_clusters
from sklearn.preprocessing import MinMaxScaler


def get_velocity_ligands_spatial(
        adata,
        adata_st,
        velocity_cluster_key = "velocity_clusters",
        n_top_genes = 500,
        adata_env=None,
        vclusters = None,
        ligand_target_matrix = None,
        lr_network = None,
        tangram_result_column = "velocity_label_transfer",
        expression_proportion_cutoff=0.05,
        organism="human",
        n_jobs = 4,

):

    adata=ad.read_h5ad(adata) if type(adata) == str else adata
    adata_st=ad.read_h5ad(adata_st) if type(adata_st) == str else adata_st

        # step1 cluster velocities.
    
    if velocity_cluster_key not in adata.obs.columns.values:
        adata = cluster_velocities(adata, cluster_key = velocity_cluster_key)
    
        #step 2 get dynamics
    if "velocity_cluster_likelihoods" not in adata.uns.keys():
        adata = recover_dynamics_clusters(adata, 
                                     return_adata=True,
                                     cluster_key=velocity_cluster_key,
                                     n_jobs = n_jobs,
                                     n_top_genes = n_top_genes)

        # step 3 transfer velocity labels to spatial.
    if tangram_result_column not in adata_st.obs.columns.values:
        adata_st = velocity_label_transfer(adata,
                                    adata_st,
                                    velocity_cluster_key = velocity_cluster_key,
                                    tangram_result_column = tangram_result_column)
    
    if vclusters is None:
        vclusters = adata_st.obs[tangram_result_column].unique()
        
        # get lr pairs expressed with spatial data.
    spatially_interacting_ligands = get_spatially_interacting_ligands(
                                                    adata_st,
                                                    organism=organism,
                                                    vclusters_of_interest=vclusters,
                                                    cluster_key=tangram_result_column,
                                                    expression_proportion_cutoff = expression_proportion_cutoff)
    
    adata.uns["entrain"] = {}
    adata.uns["entrain"]["spatially_interacting_ligands"] = spatially_interacting_ligands
    
    if ligand_target_matrix is None:
        raise(ValueError("Please supply a ligand target matrix"))
    elif type(ligand_target_matrix) == str:
            ligand_target_matrix = pd.read_csv(ligand_target_matrix, index_col=0)
    result_ligands = velocity_ligands(adata,
                                              vclusters_of_interest = vclusters,
                                              ligand_target_matrix = ligand_target_matrix,
                                              ligands_key = "spatially_interacting_ligands")
    adata.uns["entrain_velocity_ligands"] = result_ligands
    return(adata)

def get_velocity_ligands(
        adata,
        velocity_cluster_key = "velocity_clusters",
        n_top_genes = 500,
        vclusters = None,
        sender_clusters = None,
        sender_cluster_key = None,
        ligand_target_matrix = None,
        expression_proportion_cutoff=0.05,
        organism="human",
        n_jobs = 4,
):

    adata=ad.read_h5ad(adata) if type(adata) == str else adata

        # step1 cluster velocities.
    
    if velocity_cluster_key not in adata.obs.columns.values:
        adata = cluster_velocities(adata, cluster_key = velocity_cluster_key)
    
        #step 2 get dynamics
    if "velocity_cluster_likelihoods" not in adata.uns.keys():
        adata = recover_dynamics_clusters(adata, 
                                     return_adata=True,
                                     cluster_key=velocity_cluster_key,
                                     n_jobs = n_jobs,
                                     n_top_genes = n_top_genes)

    if vclusters is None:
        vclusters = adata.obs[velocity_cluster_key].unique()
    
    # get lr pairs expressed without spatial data.

    interacting_ligands = get_interacting_ligands(adata,
                                                    organism=organism,
                                                    vclusters_of_interest=vclusters,
                                                    velocity_cluster_key=velocity_cluster_key,
                                                    sender_clusters = sender_clusters,
                                                    sender_cluster_key = sender_cluster_key,
                                                    expression_proportion_cutoff = expression_proportion_cutoff)
    
    adata.uns["entrain"] = {}
    adata.uns["entrain"]["interacting_ligands"] = interacting_ligands
    
    if ligand_target_matrix is None:
        raise(ValueError("Please supply a ligand target matrix"))
    elif type(ligand_target_matrix) == str:
            ligand_target_matrix = pd.read_csv(ligand_target_matrix, index_col=0)

    result_ligands = velocity_ligands(adata,
                                              vclusters_of_interest = vclusters,
                                              ligand_target_matrix = ligand_target_matrix,
                                              ligands_key = "interacting_ligands")
    adata.uns["entrain_velocity_ligands"] = result_ligands
    return(adata)

def get_adjacent_cells(adata, cell_names_oi):
    connectivities = adata.obsp["spatial_connectivities"]

    neighbouring_cells_idx = np.isin(adata.obs_names, cell_names_oi)
    adjacent_edges = connectivities[neighbouring_cells_idx, :]
    cells_interacting_with_clusters_oi_bool = np.array(
        (adjacent_edges).sum(axis=0) > 0)[0]
    return(cells_interacting_with_clusters_oi_bool)


def get_possible_ligrec(adata, organism, intercell_network, ligand_or_receptor):
    
    if ligand_or_receptor == "ligand":
        intercell_column = "source"
        intercell_symbol_column = "genesymbol_intercell_source"
    elif ligand_or_receptor == "receptor":
        intercell_column = "target"
        intercell_symbol_column = "genesymbol_intercell_target"
    else:
        raise(ValueError("ligand_or_receptor must be one of 'ligand' or 'receptor'"))
            
    
    all_possible_ligrec = intercell_network.loc[:, [
        intercell_column, intercell_symbol_column]].drop_duplicates()

    if organism == "mouse":
        ncbi_tax_id = 10090

        possible_ids = homology.translate(
            all_possible_ligrec[intercell_column], ncbi_tax_id)
        
        all_possible_ligrec_array = np.array(list(
            mapping.map_names(possible_ids,
                              id_type="uniprot",
                              target_id_type="genesymbol",
                              ncbi_tax_id=ncbi_tax_id)
        ))
        common_idx = np.isin(all_possible_ligrec_array, adata.var_names)

        all_possible_ligrec_common = all_possible_ligrec_array[common_idx]
        
    elif organism == "human":
        common_idx = np.isin(all_possible_ligrec, adata.var_names)
        all_possible_ligrec_common = all_possible_ligrec[common_idx].iloc[:, 1].values
        
    else:
        raise(ValueError("organism must be one of 'human' or 'mouse'"))
    
    return(all_possible_ligrec_common)


def subset_adata_to_expressed_genes(adata, expression_proportion_cutoff):
    min_cells = int(np.floor(adata.n_obs * expression_proportion_cutoff))
    sc.pp.filter_genes(adata, min_cells=min_cells)
    return adata

def velocity_label_transfer(adata,
                            adata_st,
                            velocity_cluster_key = "velocity_clusters",
                            tangram_result_column = "velocity_label_transfer",
                            plot = None
                            ):
    
        # tg annoyingly sets names to lowercase. Saving here to restore later. 
    adata_st.var["original_name"] = adata_st.var_names.values
    adata.var["original_name"] = adata.var_names.values

    sc.tl.rank_genes_groups(adata,
                            groupby=velocity_cluster_key,
                            use_raw=False)
    
    markers_df = pd.DataFrame(adata.uns["rank_genes_groups"]["names"]).iloc[0:100, :]
    markers = list(np.unique(markers_df.melt().value.values))
    
    tg.pp_adatas(adata, adata_st, genes=markers)

    ad_map = tg.map_cells_to_space(adata, adata_st,
        mode="clusters", cluster_label = velocity_cluster_key,
        density_prior='rna_count_based',
        num_epochs=500,
        # device="cuda:0",
        device='cpu')
    
    tg.project_cell_annotations(ad_map, adata_st, annotation = velocity_cluster_key)
    
    tg_result = adata_st.obsm["tangram_ct_pred"]
    adata_st.obs[tangram_result_column] = tg_result.idxmax(axis=1)
    
    if type(plot) == str: 
        annotation_list = list(adata_st.obsm["tangram_ct_pred"].columns.unique())
        tg.plot_cell_annotation_sc(adata_st, annotation_list,perc=0.02)
        
            # Restore gene names from lowercase.
    adata_st.var.set_index("original_name", drop=True, inplace=True) 
    adata.var.set_index("original_name", drop=True, inplace=True) 

    return(adata_st)


def get_interacting_ligands(adata,
                         organism,
                         vclusters_of_interest=None,
                         velocity_cluster_key=None,
                         sender_cluster_key = None,
                         sender_clusters = None,
                         expression_proportion_cutoff=0.05
                         ):

    sc.set_figure_params(dpi=300, dpi_save=300,
                         format='.svg', figsize=(16, 16))

    transmitter_params = {"categories": "ligand"}
    receiver_params = {"categories": "receptor"}
    
    intercell_network = import_intercell_network(
        transmitter_params=transmitter_params,
        receiver_params=receiver_params)
    
    if type(adata) == str:
        adata = ad.read_h5ad(adata)

    if vclusters_of_interest is None:
        vclusters_of_interest = adata.obs[velocity_cluster_key].unique().astype(str)
    
    ligands_dict = {}
    for vcluster in vclusters_of_interest:
        ligands = interacting_ligands(adata,
                             velocity_cluster_key = velocity_cluster_key,
                             vclusters_of_interest = vcluster,
                             intercell_network = intercell_network,
                             expression_proportion_cutoff = expression_proportion_cutoff,
                             organism = organism)
        ligands_dict[vcluster] = ligands
    return(ligands_dict)

def interacting_ligands(adata,
                         organism,
                         vclusters_of_interest=None,
                         velocity_cluster_key=None,
                         sender_cluster_key = None,
                         sender_clusters = None,
                         expression_proportion_cutoff=None,
                         intercell_network = None,
                         ):

    human_tax_id = 9606
    mouse_tax_id = 10090

    duplicated_vars = adata.var_names.duplicated().sum()
    duplicated_obs = adata.obs_names.duplicated().sum()
    if (duplicated_vars > 0):
        print("Found " + str(duplicated_vars) + "duplicated gene names.")
        adata.var_names_make_unique()
    if duplicated_obs > 0:
        print("Found " + str(duplicated_obs) + "duplicated cell barcodes.")
        adata.obs_names_make_unique()
    # get active ligands that are expressed in the clusters of interest.
    all_possible_ligands_common = get_possible_ligrec(adata=adata,
                                                      organism=organism,
                                                      intercell_network=intercell_network,
                                                      ligand_or_receptor="ligand")

    if len(all_possible_ligands_common) < 5:
        RuntimeWarning("There are less than 5 common ligand genes between the AnnData object and the intercell network. Are your gene names formatted correctly and have you chosen the right organism?")

    if sender_clusters:
        if sender_cluster_key:
            sender_cell_names_oi = adata.obs[np.isin(
                    adata.obs[sender_cluster_key], sender_clusters)].index.values
        else:
            raise(ValueError("If you're suppling sender_clusters, please supply a sender_cluster_key as well."))
    else:
        sender_cell_names_oi = adata.obs_names.values

    adata_senders = adata[sender_cell_names_oi, all_possible_ligands_common]

    adata_senders = subset_adata_to_expressed_genes(
        adata_senders, expression_proportion_cutoff)
    expressed_ligands = adata_senders.var_names

    # get only those active receptors that are expressed in the velocity clusters.
    all_possible_receptors_common = get_possible_ligrec(adata=adata,
                                                      organism=organism,
                                                      intercell_network=intercell_network,
                                                      ligand_or_receptor="receptor")
    if len(all_possible_receptors_common) < 5:
        RuntimeWarning("There are less than 5 common receptor genes between the AnnData object and the intercell network. Are your gene names formatted correctly and have you chosen the right organism?")

    receiver_cell_names_oi = adata.obs[np.isin(
            adata.obs[velocity_cluster_key], vclusters_of_interest)].index.values
    adata_receptors_present_in_traj = adata[receiver_cell_names_oi,
                                            all_possible_receptors_common]
    adata_receptors_present_in_traj = subset_adata_to_expressed_genes(
        adata_receptors_present_in_traj, expression_proportion_cutoff)
    expressed_receptors = adata_receptors_present_in_traj.var_names
    
    if organism == "mouse": # translate to human genes for lr mapping.
        expressed_receptors = homology.translate(
            expressed_receptors, source=mouse_tax_id, target=human_tax_id, id_type="genesymbol")
        expressed_ligands = homology.translate(
            expressed_ligands, source=mouse_tax_id, target=human_tax_id, id_type="genesymbol")

        # subset interaction network to ligands that have their
        # corresponding receptor expressed in the trajectory.

    if len(expressed_receptors) < 5 or len(expressed_ligands) < 5:
        RuntimeWarning("There are less than 5 expressed ligand or receptor genes found. Are your gene names formatted correctly and have you chosen the right organism?")

    subset_receptors_idx = np.isin(
        intercell_network["genesymbol_intercell_target"].values, list(expressed_receptors))
    intercell_network_subset = intercell_network.iloc[subset_receptors_idx, :]
    subset_ligands_idx = np.isin(
        intercell_network["genesymbol_intercell_source"].values, list(expressed_ligands))
    intercell_network_subset = intercell_network.iloc[subset_ligands_idx, :]

    if organism == "mouse": # translate back to mouse.
        interacting_ligands = list(
            homology.translate(
                intercell_network_subset["genesymbol_intercell_source"],
                 source=human_tax_id,
                 target=mouse_tax_id,
                 id_type="genesymbol")
        )
    elif organism == "human":
        interacting_ligands = list(
            intercell_network_subset["genesymbol_intercell_source"]
        )

    return(interacting_ligands)

def get_adjacent_ligands(adata,
                         organism,
                         intercell_network,
                         cell_names_oi=None,
                         clusters_oi=None,
                         cluster_key=None,
                         expression_proportion_cutoff=0.05
                         ):

    mouse_tax_id = 9606
    human_tax_id = 10090

    sc.set_figure_params(dpi=300, dpi_save=300,
                         format='.svg', figsize=(16, 16))


    if type(adata) == str:
        adata = ad.read_h5ad(adata)

    sq.gr.spatial_neighbors(adata)

    duplicated_vars = adata.var_names.duplicated().sum()
    duplicated_obs = adata.obs_names.duplicated().sum()
    if (duplicated_vars > 0):
        print("Found " + str(duplicated_vars) + "duplicated gene names.")
        adata.var_names_make_unique()
    if duplicated_obs > 0:
        print("Found " + str(duplicated_obs) + "duplicated cell barcodes.")
        adata.obs_names_make_unique()
    # get active ligands that are expressed proximal to the trajectory.
    if cell_names_oi is None:
        cell_names_oi = adata.obs[np.isin(
            adata.obs[cluster_key], clusters_oi)].index.values

    all_possible_ligands_common = get_possible_ligrec(adata=adata,
                                                      organism=organism,
                                                      intercell_network=intercell_network,
                                                      ligand_or_receptor="ligand")
    
    cells_interacting_with_traj_idx = get_adjacent_cells(
        adata, cell_names_oi=cell_names_oi)
    adata_ligands_interacting_with_traj = adata[cells_interacting_with_traj_idx,
                                                all_possible_ligands_common]
    adata_ligands_interacting_with_traj = subset_adata_to_expressed_genes(
        adata_ligands_interacting_with_traj, expression_proportion_cutoff)
    expressed_ligands = adata_ligands_interacting_with_traj.var_names

    # get active receptors rhat are expressed within the trajectory
    all_possible_receptors_common = get_possible_ligrec(adata=adata,
                                                      organism=organism,
                                                      intercell_network=intercell_network,
                                                      ligand_or_receptor="receptor")
    if len(all_possible_receptors_common) < 5:
        RuntimeWarning("There are less than 5 common receptor genes between the AnnData object and the intercell network. Are your gene names formatted correctly and have you chosen the right organism?")

    adata_receptors_present_in_traj = adata[cell_names_oi,
                                            all_possible_receptors_common]
    adata_receptors_present_in_traj = subset_adata_to_expressed_genes(
        adata_receptors_present_in_traj, expression_proportion_cutoff)
    expressed_receptors = adata_receptors_present_in_traj.var_names
    
    if organism == "mouse":
        expressed_receptors = homology.translate(
            expressed_receptors, mouse_tax_id, id_type="genesymbol")
        expressed_ligands = homology.translate(
            expressed_ligands, mouse_tax_id, id_type="genesymbol")

        # subset interaction network to ligands that are both
        # expressed proximal to the trajectory and have their
        # corresponding receptor expressed in the trajectory.
    subset_receptors_idx = np.isin(
        intercell_network["genesymbol_intercell_target"].values, list(expressed_receptors))
    intercell_network_subset = intercell_network.iloc[subset_receptors_idx, :]
    subset_ligands_idx = np.isin(
        intercell_network["genesymbol_intercell_source"].values, list(expressed_ligands))
    intercell_network_subset = intercell_network.iloc[subset_ligands_idx, :]

    if organism == "mouse":
        adjacent_ligands = list(
            homology.translate(
                intercell_network_subset["genesymbol_intercell_source"], human_tax_id, id_type="genesymbol")
        )
    elif organism == "human":
        adjacent_ligands = list(
            intercell_network_subset["genesymbol_intercell_source"]
        )

    return(adjacent_ligands)

def get_spatially_interacting_ligands(adata_st,
                         organism,
                         vclusters_of_interest,
                         cluster_key=None,
                         expression_proportion_cutoff = None):
    
    transmitter_params = {"categories": "ligand"}
    receiver_params = {"categories": "receptor"}
    
    intercell_network = import_intercell_network(
        transmitter_params=transmitter_params,
        receiver_params=receiver_params)
    
    if vclusters_of_interest is None:
        vclusters_of_interest = adata_st.obs[cluster_key].unique().str()
    
    ligands_dict = {}
    for vcluster in vclusters_of_interest:
        adjacent_ligands = get_adjacent_ligands(adata_st,
                             cluster_key = cluster_key,
                             clusters_oi = vcluster,
                             intercell_network = intercell_network,
                             expression_proportion_cutoff = expression_proportion_cutoff,
                             cell_names_oi = None,
                             organism = organism)
        ligands_dict[vcluster] = adjacent_ligands
    return(ligands_dict)

def velocity_ligands(adata,
                             vclusters_of_interest,
                             ligand_target_matrix,
                             ligands_key = "spatially_interacting_ligands"):
    
    ##### R Function importing
    np_cv_rules = default_converter + pandas2ri.converter
    
    rf_regression_str = """
    library("randomForest")
    get_ligand_trajectory_scores_regression <- function(pseudotime_genes, active_ligand_potentials){

    intersection_genes <- base::intersect(rownames(active_ligand_potentials), rownames(pseudotime_genes))
    potentials_intersection <- active_ligand_potentials[intersection_genes,]

    pseudotime_genes_intersection <- pseudotime_genes[intersection_genes,]
    rf <- randomForest::randomForest(x=potentials_intersection, y=pseudotime_genes_intersection, importance=TRUE)

    gene_names = rownames(rf$importance)
    list(genes_input=pseudotime_genes_intersection, gene_names = gene_names, model=rf)
    }
    """
    rf_regression = robjects.r(rf_regression_str)
    #####

    interacting_ligands = adata.uns["entrain"][ligands_key]
    likelihoods_df = adata.uns["velocity_cluster_likelihoods"]
    
    var_exp_df = pd.DataFrame(columns=["vcluster", "var_exp"])
    importance_df = pd.DataFrame(columns=["ligand"]) # coumns = vcluster
    for i, vcluster in enumerate(vclusters_of_interest):
        test_ligands = interacting_ligands[vcluster]
        test_ligands_common = ligand_target_matrix.columns.intersection(test_ligands)
        if len(test_ligands_common) < 10:
            RuntimeWarning("There are less than 10 ligands found in the ligand_target_matrix. Have you supplied the mouse ortholog-converted ligand_target_matrix to human data or vice versa?")

        active_ligand_target = ligand_target_matrix.loc[:, test_ligands_common]
        likelihoods = likelihoods_df[vcluster].dropna()
            
        with (robjects.default_converter + pandas2ri.converter).context():
            rf = rf_regression(pd.DataFrame(likelihoods), active_ligand_target)
        
        var_exp = rf["model"]["rsq"][-1]
        importances_data =  rf["model"]["importance"][:,1] # Column 0 is %IncMSE, Col1 is IncNodePurity
        gene_names = rf["gene_names"]
        importances = pd.DataFrame({"ligand" : gene_names, 
                                    vcluster : importances_data})
        
        var_exp_df.loc[i] = [vcluster, var_exp] 
        importance_df = pd.merge(importance_df, importances, how="outer", left_on="ligand", right_on = "ligand")

    result = {"variance_explained" : var_exp_df,
              "vclust_ligand_importances" : importance_df,
              "vclust_gene_likelihoods" : likelihoods_df
              }  
    
    return(result)


def plot_ligand_importance_heatmap(adata,
                n_top_ligands = 5,
                colorscale = "inferno",
                velocity_clusters = None,
                filename = "velocity_importances.png",
                figsize = (10, 8),
                rescale_columns = True,
                return_plot = True):
    import seaborn as sns

    df = adata.uns["entrain_velocity_ligands"]["vclust_ligand_importances"].set_index("ligand")
    
    # Subset to velocity_clusters
    if velocity_clusters:
        df = df[velocity_clusters]
    
    # Subset to top n_top_ligands for each column
    df = df.apply(lambda x: x.nlargest(n_top_ligands))
    
    if rescale_columns:
        from sklearn.preprocessing import MinMaxScaler
        # Rescale columns to be between 0 and 1
        scaler = MinMaxScaler()
        df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)
    df=df.fillna(0)

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df, cmap=colorscale, ax=ax)
    
    # Save the plot
    plt.savefig(filename)
    print("Saving under filename: "+ filename)
    if return_plot:
        return plt

def plot_likelihoods_heatmap(adata,
                n_top_genes = 10,
                colorscale = "viridis",
                velocity_clusters = None,
                filename = "velocity_likelihoods.png",
                figsize = (10, 8),
                rescale_columns = True,
                return_plot = True):
    from sklearn.preprocessing import MinMaxScaler
    import seaborn as sns

    df = adata.uns["entrain_velocity_ligands"]["vclust_gene_likelihoods"]
    
    # Subset to velocity_clusters
    if velocity_clusters:
        df = df[velocity_clusters]
    
    # Subset to top n_top_ligands for each column
    df = df.apply(lambda x: x.nlargest(n_top_genes))
    
    if rescale_columns:
        # Rescale columns to be between 0 and 1
        scaler = MinMaxScaler()
        df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)
    df=df.fillna(0)

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df, cmap=colorscale, ax=ax)
    
    # Save the plot
    plt.savefig(filename)
    print("Saving under filename: "+ filename)
    if return_plot:
        return plt        

def plot_ligand_targets_heatmap(
    adata,
    ligand_target_matrix,
    velocity_cluster,
    colorscale = "cividis",
    n_top_ligands = 5,
    n_top_genes = 10,
    filename = "ligand_target_heatmap.png",
    figsize = (10, 4),
    return_plot=True,
    rescale = False,
    coord_flip = True):
    from sklearn.preprocessing import MinMaxScaler
    import seaborn as sns
    df = pd.DataFrame(adata.uns["entrain_velocity_ligands"]["vclust_ligand_importances"].set_index("ligand"))
            
    df = df[velocity_cluster]

    # Get top n largest ligands
    top_ligands = df.nlargest(n_top_ligands).index

    #Get top genes for each ligand
    top_genes = ligand_target_matrix.loc[top_ligands].apply(lambda x: x.nlargest(n_top_genes).index, axis=1)
    top_genes = pd.unique(top_genes.explode())

    # Subset the ligand_target_matrix to the top ligands and top genes
    ligand_target_df = ligand_target_matrix.loc[top_genes, top_ligands]

    # Replace NaN values with 0
    ligand_target_df = ligand_target_df.fillna(0)

    # Rescale to be between 0 and 1. Default False because it is usually useful to compare gene regulatory potentials across different ligands.
    if rescale:
        scaler = MinMaxScaler()
        ligand_target_df = pd.DataFrame(scaler.fit_transform(ligand_target_df), columns=ligand_target_df.columns, index=ligand_target_df.index)
        
    if coord_flip: 
        ligand_target_df = ligand_target_df.transpose() # usually more genes than ligands, so landscape orientation suits.
    # Create a new figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot heatmap
    sns.heatmap(ligand_target_df, cmap=colorscale, ax=ax)
    
    # Save the plot
    fig.savefig(filename)

    if return_plot:
        return plt       
