def write_10x_h5(adata, path, name):
    filepath = (path + "/" + name)
    with h5py.File(filepath, 'w', locking=False) as f:
        # Check if 'matrix' group already exists
        matrix_group = f.create_group('matrix') if 'matrix' not in f else f['matrix']
        
        # Convert pandas indices to byte strings for barcodes
        barcodes = adata.obs.index.to_numpy().astype('S')
        matrix_group.create_dataset(
            'barcodes', data=barcodes,
            chunks=(540,), compression='gzip', compression_opts=4
        )

        # Create features subgroup within matrix
        features_group = matrix_group.create_group('features') if 'features' not in matrix_group else matrix_group['features']

        features_group.create_dataset('_all_tag_keys', data=np.array(['genome']).astype('S'))
        
        common_settings = {'chunks': (980,), 'compression': 'gzip', 'compression_opts': 4}
        
        features_group.create_dataset('id', data=adata.var["gene_ids"].to_numpy().astype('S'), **common_settings)
        features_group.create_dataset('name', data=adata.var.index.to_numpy().astype('S'), **common_settings)
        features_group.create_dataset('feature_type', data=np.array(["Gene Expression"] * len(adata.var.index)).astype('S'), **common_settings)
        features_group.create_dataset('genome', data=np.array(["cr_index_hs"] * len(adata.var.index)).astype('S'), chunks=(1960,), **common_settings)

        # Add shape
        matrix_group.create_dataset(
            'shape', data=np.array(adata.X.shape)[::-1], dtype='int32', maxshape=(None,),
            chunks=(80000,), compression='gzip', compression_opts=4, shuffle=True
        )

        if isinstance(adata.X, scipy.sparse.csr.csr_matrix):
            sparse_settings = {'dtype': 'int32', 'maxshape': (None,), 'chunks': (80000,), 'compression': 'gzip', 'compression_opts': 4, 'shuffle': True}

            matrix_group.create_dataset('data', data=adata.X.data, **sparse_settings)
            matrix_group.create_dataset('indptr', data=adata.X.indptr, dtype='int64', **sparse_settings)
            matrix_group.create_dataset('indices', data=adata.X.indices, dtype='int64', **sparse_settings)
        else:
            matrix_group.create_dataset('data', data=adata.X)
