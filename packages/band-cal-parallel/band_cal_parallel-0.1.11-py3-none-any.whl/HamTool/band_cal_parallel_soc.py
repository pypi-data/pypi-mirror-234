'''
Descripttion: 
version: 
Author: Yang Zhong
Date: 2023-05-02 16:06:52
LastEditors: Yang Zhong
LastEditTime: 2023-07-02 11:55:01
'''

from ctypes import Union
import numpy as np
import sympy as sym
from tqdm import tqdm
from typing import Tuple, Union, Optional, List, Set, Dict, Any
import matplotlib.pyplot as plt
from pymatgen.core.structure import Structure
from pymatgen.symmetry.kpath import KPathSeek
from pymatgen.core.periodic_table import Element
import os
from easydict import EasyDict as edict
from mpi4py import MPI
import opt_einsum as oe
import mpitool
import yaml
import argparse

def suggest_blocking(N: int, ncpus: int) -> tuple[int, int, int]:
    """Suggest blocking of ``NxN`` matrix.

    Returns rows, columns, blocksize tuple.

    >>> suggest_blocking(10, 6)
    (3, 2, 2)
    """

    nprow = ncpus
    npcol = 1

    # Make npcol and nprow as close to each other as possible
    npcol_try = npcol
    while npcol_try < nprow:
        if ncpus % npcol_try == 0:
            npcol = npcol_try
            nprow = ncpus // npcol
        npcol_try += 1

    assert npcol * nprow == ncpus

    # ScaLAPACK creates trouble if there aren't at least a few whole blocks.
    # Choose block size so that there will always be at least one whole block
    # and at least two blocks in total.
    blocksize = max((N - 2) // max(nprow, npcol), 1)
    # The next commented line would give more whole blocks.
    # blocksize = max(N // max(nprow, npcol) - 2, 1)

    # Use block size that is a power of 2 and at most 64
    blocksize = 2**int(np.log2(blocksize))
    blocksize = max(min(blocksize, 64), 1)

    return nprow, npcol, blocksize

def _nice_float(x,just,rnd):
    return str(round(x,rnd)).rjust(just)

class kpoints_generator:
    """
    Used to generate K point path
    """
    def __init__(self, dim_k: int=3, lat: Union[np.array, list]=None, per: Union[List, Tuple] = None):
        self._dim_k = dim_k
        self._lat = lat
        # choose which self._dim_k out of self._dim_r dimensions are
        # to be considered periodic.        
        if per==None:
            # by default first _dim_k dimensions are periodic
            self._per=list(range(self._dim_k))
        else:
            if len(per)!=self._dim_k:
                raise Exception("\n\nWrong choice of periodic/infinite direction!")
            # store which directions are the periodic ones
            self._per=per
        
    def k_path(self,kpts,nk,report=True):
        r"""
    
        Interpolates a path in reciprocal space between specified
        k-points.  In 2D or 3D the k-path can consist of several
        straight segments connecting high-symmetry points ("nodes"),
        and the results can be used to plot the bands along this path.
        
        The interpolated path that is returned contains as
        equidistant k-points as possible.
    
        :param kpts: Array of k-vectors in reciprocal space between
          which interpolated path should be constructed. These
          k-vectors must be given in reduced coordinates.  As a
          special case, in 1D k-space kpts may be a string:
    
          * *"full"*  -- Implies  *[ 0.0, 0.5, 1.0]*  (full BZ)
          * *"fullc"* -- Implies  *[-0.5, 0.0, 0.5]*  (full BZ, centered)
          * *"half"*  -- Implies  *[ 0.0, 0.5]*  (half BZ)
    
        :param nk: Total number of k-points to be used in making the plot.
        
        :param report: Optional parameter specifying whether printout
          is desired (default is True).

        :returns:

          * **k_vec** -- Array of (nearly) equidistant interpolated
            k-points. The distance between the points is calculated in
            the Cartesian frame, however coordinates themselves are
            given in dimensionless reduced coordinates!  This is done
            so that this array can be directly passed to function
            :func:`pythtb.tb_model.solve_all`.

          * **k_dist** -- Array giving accumulated k-distance to each
            k-point in the path.  Unlike array *k_vec* this one has
            dimensions! (Units are defined here so that for an
            one-dimensional crystal with lattice constant equal to for
            example *10* the length of the Brillouin zone would equal
            *1/10=0.1*.  In other words factors of :math:`2\pi` are
            absorbed into *k*.) This array can be used to plot path in
            the k-space so that the distances between the k-points in
            the plot are exact.

          * **k_node** -- Array giving accumulated k-distance to each
            node on the path in Cartesian coordinates.  This array is
            typically used to plot nodes (typically special points) on
            the path in k-space.
    
        Example usage::
    
          # Construct a path connecting four nodal points in k-space
          # Path will contain 401 k-points, roughly equally spaced
          path = [[0.0, 0.0], [0.0, 0.5], [0.5, 0.5], [0.0, 0.0]]
          (k_vec,k_dist,k_node) = my_model.k_path(path,401)
          # solve for eigenvalues on that path
          evals = tb.solve_all(k_vec)
          # then use evals, k_dist, and k_node to plot bandstructure
          # (see examples)
        
        """
    
        # processing of special cases for kpts
        if kpts=='full':
            # full Brillouin zone for 1D case
            k_list=np.array([[0.],[0.5],[1.]])
        elif kpts=='fullc':
            # centered full Brillouin zone for 1D case
            k_list=np.array([[-0.5],[0.],[0.5]])
        elif kpts=='half':
            # half Brillouin zone for 1D case
            k_list=np.array([[0.],[0.5]])
        else:
            k_list=np.array(kpts)
    
        # in 1D case if path is specified as a vector, convert it to an (n,1) array
        if len(k_list.shape)==1 and self._dim_k==1:
            k_list=np.array([k_list]).T

        # make sure that k-points in the path have correct dimension
        if k_list.shape[1]!=self._dim_k:
            print('input k-space dimension is',k_list.shape[1])
            print('k-space dimension taken from model is',self._dim_k)
            raise Exception("\n\nk-space dimensions do not match")

        # must have more k-points in the path than number of nodes
        if nk<k_list.shape[0]:
            raise Exception("\n\nMust have more points in the path than number of nodes.")

        # number of nodes
        n_nodes=k_list.shape[0]
    
        # extract the lattice vectors from the TB model
        lat_per=np.copy(self._lat)
        # choose only those that correspond to periodic directions
        lat_per=lat_per[self._per]    
        # compute k_space metric tensor
        k_metric = np.linalg.inv(np.dot(lat_per,lat_per.T))

        # Find distances between nodes and set k_node, which is
        # accumulated distance since the start of the path
        #  initialize array k_node
        k_node=np.zeros(n_nodes,dtype=float)
        for n in range(1,n_nodes):
            dk = k_list[n]-k_list[n-1]
            dklen = np.sqrt(np.dot(dk,np.dot(k_metric,dk)))
            k_node[n]=k_node[n-1]+dklen
    
        # Find indices of nodes in interpolated list
        node_index=[0]
        for n in range(1,n_nodes-1):
            frac=k_node[n]/k_node[-1]
            node_index.append(int(round(frac*(nk-1))))
        node_index.append(nk-1)
    
        # initialize two arrays temporarily with zeros
        #   array giving accumulated k-distance to each k-point
        k_dist=np.zeros(nk,dtype=float)
        #   array listing the interpolated k-points    
        k_vec=np.zeros((nk,self._dim_k),dtype=float)
    
        # go over all kpoints
        k_vec[0]=k_list[0]
        for n in range(1,n_nodes):
            n_i=node_index[n-1]
            n_f=node_index[n]
            kd_i=k_node[n-1]
            kd_f=k_node[n]
            k_i=k_list[n-1]
            k_f=k_list[n]
            for j in range(n_i,n_f+1):
                frac=float(j-n_i)/float(n_f-n_i)
                k_dist[j]=kd_i+frac*(kd_f-kd_i)
                k_vec[j]=k_i+frac*(k_f-k_i)
    
        if report==True:
            if self._dim_k==1:
                print(' Path in 1D BZ defined by nodes at '+str(k_list.flatten()))
            else:
                print('----- k_path report begin ----------')
                original=np.get_printoptions()
                np.set_printoptions(precision=5)
                print('real-space lattice vectors\n', lat_per)
                print('k-space metric tensor\n', k_metric)
                print('internal coordinates of nodes\n', k_list)
                if (lat_per.shape[0]==lat_per.shape[1]):
                    # lat_per is invertible
                    lat_per_inv=np.linalg.inv(lat_per).T
                    print('reciprocal-space lattice vectors\n', lat_per_inv)
                    # cartesian coordinates of nodes
                    kpts_cart=np.tensordot(k_list,lat_per_inv,axes=1)
                    print('cartesian coordinates of nodes\n',kpts_cart)
                print('list of segments:')
                for n in range(1,n_nodes):
                    dk=k_node[n]-k_node[n-1]
                    dk_str=_nice_float(dk,7,5)
                    print('  length = '+dk_str+'  from ',k_list[n-1],' to ',k_list[n])
                print('node distance list:', k_node)
                print('node index list:   ', np.array(node_index))
                np.set_printoptions(precision=original["precision"])
                print('----- k_path report end ------------')
            print()

        return (k_vec,k_dist,k_node,lat_per_inv,node_index)

au2ang = 0.5291772083
au2ev = 27.213

# 计算每个结构的norbs
basis_def_19 = {1:np.array([0,1,3,4,5], dtype=int), # H
             2:np.array([0,1,3,4,5], dtype=int), # He
             3:np.array([0,1,2,3,4,5,6,7,8], dtype=int), # Li
             4:np.array([0,1,3,4,5,6,7,8], dtype=int), # Be
             5:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # B
             6:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # C
             7:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # N
             8:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # O
             9:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # F
             10:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Ne
             11:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Na
             12:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Mg
             13:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Al
             14:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Si
             15:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # p
             16:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # S
             17:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Cl
             18:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Ar
             19:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # K
             20:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Ca 
             42:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int), # Mo  
             83:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int), # Bi  
             34:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int), # Se 
             24:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Cr 
             53:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int), # I   
             82:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int), # pb
             55:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int), # Cs
             28:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Ni
             35:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int), # Br 
             26:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Fe
             77:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=int) # Ir
             }

basis_def_14 = {1:np.array([0,1,3,4,5], dtype=int), # H
                 2:np.array([0,1,3,4,5], dtype=int), # He
                 3:np.array([0,1,2,3,4,5,6,7,8], dtype=int), # Li
                 4:np.array([0,1,3,4,5,6,7,8], dtype=int), # Be
                 5:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # B
                 6:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # C
                 7:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # N
                 8:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # O
                 9:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # F
                 10:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Ne
                 11:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Na
                 12:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Mg
                 13:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Al
                 14:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Si
                 15:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # p
                 16:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # S
                 17:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Cl
                 18:np.array([0,1,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Ar
                 19:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # K
                 20:np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=int), # Ca 
                 }

def main():
    parser = argparse.ArgumentParser(description='SOC band calculation')
    parser.add_argument('--config', default='band_cal.yaml', type=str, metavar='N')
    args = parser.parse_args()
    
    with open(args.config, encoding='utf-8') as rstream:
        input = yaml.load(rstream, yaml.SafeLoader)
    
    nao_max = input['nao_max']    
    save_dir = input['save_dir'] 
    filename = input['filename'] 
    graph_data_path = input['graph_data_path'] 
    hamiltonian_path = input['hamiltonian_path'] 
    num_wfns = input['num_wfns'] 
    k_path=input['k_path'] 
    label=input['label'] 
    nk = input['nk'] 
    
    comm = MPI.COMM_WORLD
    rank_size = comm.Get_size()
    rank = comm.Get_rank()
    
    if nao_max == 14:
        basis_def = basis_def_14
    else:
        basis_def = basis_def_19
    
    num_valence = {1:1,2:2,3:3,4:2,5:3,6:4,7:5,8:6,9:7,10:8,11:9,12:8,13:3,14:4,
                   15:5,16:6,17:7,18:8,19:9,20:10,42:14,83:15,34:6,53:7,82:14,55:9,28:18,35:7,26:14,77:15}
    
    # 设置价电子数
    num_val = np.zeros((99,), dtype=int)
    for k in num_valence.keys():
        num_val[k] = num_valence[k]
    
    # build crystal structure
    if rank == 0:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        graph_data_path = graph_data_path
        graph_data = np.load(graph_data_path, allow_pickle=True)
        graph_data = graph_data['graph'].item()
        graph_data = list(graph_data.values())[0]
        Hsoc = np.load(hamiltonian_path).reshape(-1, 2*nao_max, 2*nao_max)
        
        # 删除一些不需要的键
        data = edict()
        data.edge_index = graph_data['edge_index']
        data.nbr_shift = graph_data['nbr_shift']
        data.cell_shift = graph_data['cell_shift']
        data.z = graph_data['z']
        data.pos = graph_data['pos']
        data.cell = graph_data['cell']
        data.Son = graph_data['Son']
        data.Soff = graph_data['Soff']
        del graph_data
        
        Son = data.Son.numpy().reshape(-1, nao_max*nao_max)
        Soff = data.Soff.numpy().reshape(-1, nao_max*nao_max) 
        
        Hsoc_real, Hsoc_imag = np.split(Hsoc, 2, axis=0)
        Hsoc = [Hsoc_real[:, :nao_max, :nao_max]+1.0j*Hsoc_imag[:, :nao_max, :nao_max], 
                Hsoc_real[:, :nao_max, nao_max:]+1.0j*Hsoc_imag[:, :nao_max, nao_max:], 
                Hsoc_real[:, nao_max:, :nao_max]+1.0j*Hsoc_imag[:, nao_max:, :nao_max],
                Hsoc_real[:, nao_max:, nao_max:]+1.0j*Hsoc_imag[:, nao_max:, nao_max:]]
        del Hsoc_real, Hsoc_imag
        
        latt = data.cell.numpy().reshape(3,3)
        pos = data.pos.numpy()*au2ang
        nbr_shift = data.nbr_shift.numpy()
        edge_index = data.edge_index.numpy()
        cell_shift = data.cell_shift.numpy()
        species = data.z.numpy()
        struct = Structure(lattice=latt*au2ang, species=[Element.from_Z(k).symbol for k in species], coords=pos, coords_are_cartesian=True)
        struct.to(filename=os.path.join(save_dir, filename+'.cif'))
        del data
        
        # 初始化k_path和lable
        if k_path is None:
            kpath_seek = KPathSeek(structure = struct)
            klabels = []
            for lbs in kpath_seek.kpath['path']:
                klabels += lbs
            # remove adjacent duplicates   
            res = [klabels[0]]
            [res.append(x) for x in klabels[1:] if x != res[-1]]
            klabels = res
            k_path = [kpath_seek.kpath['kpoints'][k] for k in klabels]
            label = [rf'${lb}$' for lb in klabels]
        
        kpts=kpoints_generator(dim_k=3, lat=latt)
        k_vec, k_dist, k_node, lat_per_inv, node_index = kpts.k_path(k_path, nk)
        np.save(file=os.path.join(save_dir, 'k_vecs.npy'), arr=k_vec)
        print(k_vec)
        k_vec = k_vec.dot(lat_per_inv[np.newaxis,:,:]) # shape (nk,1,3)
        k_vec = k_vec.reshape(-1,3) # shape (nk, 3)
        print('OK!')
    # Prepare some necessary variables
    if rank == 0:
        natoms = len(species)
        Son = Son.reshape(-1, nao_max*nao_max).astype(np.float32).copy(order='F')
        Soff = Soff.reshape(-1, nao_max*nao_max).astype(np.float32).copy(order='F')   
        Hsoc_on = [H_tmp[:natoms].reshape(-1, nao_max**2).astype(np.complex64).copy(order='F') for H_tmp in Hsoc]
        Hsoc_off = [H_tmp[natoms:].reshape(-1, nao_max**2).astype(np.complex64).copy(order='F') for H_tmp in Hsoc]
        del Hsoc    
        natoms = len(species)
        nedges = len(edge_index[0])
        basis_milestones = np.array([len(basis_def[z]) for z in species], dtype=np.int64)
        norbs = basis_milestones.sum()
        basis_milestones = np.cumsum(basis_milestones)-basis_milestones
        basis_milestones = basis_milestones.copy(order='F')
        basis_def_dict = dict()
        for z in species:
            basis_def_dict[z] = basis_def[z].astype(np.int64)
        i_idx = edge_index[0].astype(np.int64).copy(order='F')
        j_idx = edge_index[1].astype(np.int64).copy(order='F')
        species = species.astype(np.int64).copy(order='F')
        k_vec = k_vec.astype(np.float32)
        k_vec = k_vec.copy(order='F')
        nbr_shift = nbr_shift.astype(np.float32).copy(order='F')
    else:
        nk = species = nedges = norbs = natoms = None
        basis_def_dict = basis_milestones = None
        i_idx = j_idx = k_vec = None
        Hsoc_on = [np.empty((0,), dtype=np.complex64, order='F') for i in range(4)]
        Hsoc_off = [np.empty((0,), dtype=np.complex64, order='F') for i in range(4)]
        Son = np.empty((0,), dtype=np.float32, order='F')
        Soff = np.empty((0,), dtype=np.float32, order='F')
        nbr_shift = np.empty((0,), dtype=np.float32, order='F')
    
    # Broadcast some auxiliary parameters
    nk = MPI.COMM_WORLD.bcast(nk, 0)
    species = MPI.COMM_WORLD.bcast(species, 0)
    nedges = MPI.COMM_WORLD.bcast(nedges, 0)
    natoms = MPI.COMM_WORLD.bcast(natoms, 0)
    basis_def_dict = MPI.COMM_WORLD.bcast(basis_def_dict, 0)
    basis_milestones = MPI.COMM_WORLD.bcast(basis_milestones, 0)
    i_idx = MPI.COMM_WORLD.bcast(i_idx, 0)
    j_idx = MPI.COMM_WORLD.bcast(j_idx, 0)
    k_vec = MPI.COMM_WORLD.bcast(k_vec, 0)
    norbs = MPI.COMM_WORLD.bcast(norbs, 0)
    
    # Creating process grids
    nprow, npcol, blocksize = suggest_blocking(2*norbs, rank_size)
    ictxt_col = mpitool.BLACS_grid_create(rank_size, 1)
    ictxt = mpitool.BLACS_grid_create(nprow, npcol)
    
    # Creates the descriptors of distributed arrays
    dist_on = np.empty((9,), dtype=np.int64)
    m_loc_on, n_loc_on = mpitool.matrix_desc_create(ictxt_col, natoms, nao_max**2, blocksize, nao_max**2, dist_on)
    
    dist_off = np.empty((9,), dtype=np.int64)
    m_loc_off, n_loc_off = mpitool.matrix_desc_create(ictxt_col, nedges, nao_max**2, blocksize, nao_max**2, dist_off)
    
    dist_nbr = np.empty((9,), dtype=np.int64)
    m_loc_nbr, n_loc_nbr = mpitool.matrix_desc_create(ictxt_col, nedges, 3, blocksize, 3, dist_nbr)
    
    glob_on = np.empty((9,), dtype=np.int64)    
    _, _ = mpitool.matrix_desc_create(ictxt_col, natoms, nao_max**2, natoms, nao_max**2, glob_on)
    
    glob_off = np.empty((9,), dtype=np.int64)    
    _, _ = mpitool.matrix_desc_create(ictxt_col, nedges, nao_max**2, nedges, nao_max**2, glob_off)
    
    glob_nbr = np.empty((9,), dtype=np.int64)    
    _, _ = mpitool.matrix_desc_create(ictxt_col, nedges, 3, nedges, 3, glob_nbr)
    
    dist_k_tmp = np.empty((9,), dtype=np.int64)
    m_loc_k_tmp, n_loc_k_tmp = mpitool.matrix_desc_create(ictxt_col, 2*norbs, 2*norbs, blocksize, 2*norbs, dist_k_tmp)
    
    dist_k = np.empty((9,), dtype=np.int64)
    m_loc_k, n_loc_k = mpitool.matrix_desc_create(ictxt, 2*norbs, 2*norbs, blocksize, blocksize, dist_k)
    
    glob_wfn = np.empty((9,), dtype=np.int64)    
    m_loc_wfn, n_loc_wfn = mpitool.matrix_desc_create(ictxt, 2*norbs, int(2*num_wfns+1), 2*norbs, int(2*num_wfns+1), glob_wfn)
    
    glob_SK = np.empty((9,), dtype=np.int64)    
    m_loc_SK, n_loc_SK = mpitool.matrix_desc_create(ictxt, 2*norbs, 2*norbs, 2*norbs, 2*norbs, glob_SK)
    
    # Creates the distributed arrays
    Son_d = np.empty((m_loc_on, n_loc_on), dtype=np.float32, order='F')
    mpitool.matrix_redist(glob_on, dist_on, Son, Son_d, 0, 0, 0, 0, 'g')
    del Son
    
    Soff_d = np.empty((m_loc_off, n_loc_off), dtype=np.float32, order='F')
    mpitool.matrix_redist(glob_off, dist_off, Soff, Soff_d, 0, 0, 0, 0,'g')
    del Soff
    
    Hsoc_on_d = []
    for i in range(4):
        Hon_d = np.empty((m_loc_on, n_loc_on), dtype=np.complex64, order='F')
        mpitool.matrix_redist(glob_on, dist_on, Hsoc_on[i], Hon_d, 0, 0, 0, 0,'g')
        Hsoc_on_d.append(Hon_d)
    del Hsoc_on, Hon_d
    
    Hsoc_off_d = []
    for i in range(4):
        Hoff_d = np.empty((m_loc_off, n_loc_off), dtype=np.complex64, order='F')
        mpitool.matrix_redist(glob_off, dist_off, Hsoc_off[i], Hoff_d, 0, 0, 0, 0,'g')
        Hsoc_off_d.append(Hoff_d)
    del Hsoc_off, Hoff_d
    
    nbr_shift_d = np.empty((m_loc_nbr, n_loc_nbr), dtype=np.float32, order='F')
    mpitool.matrix_redist(glob_nbr, dist_nbr, nbr_shift, nbr_shift_d, 0, 0, 0, 0,'g')
    del nbr_shift
    
    HK_d = np.empty((m_loc_k, n_loc_k), dtype=np.complex64, order='F')
    SK_d = np.empty((m_loc_k, n_loc_k), dtype=np.complex64, order='F')
    SK0 = np.empty((m_loc_SK, n_loc_SK), dtype=np.complex64, order='F')
    
    # diagonalization
    if rank == 0:
        eigen = []
        eigen_vecs = []
        spin_projection = []
        
    eigenvec0 = np.zeros((m_loc_wfn, n_loc_wfn), dtype=np.complex64, order='F')    
    eigenval = np.empty((2*norbs,), dtype=np.float32, order='F')
    
    for ik in range(nk):
        # SK
        SK_d_tmp = np.zeros((m_loc_k_tmp, n_loc_k_tmp), dtype=np.complex64, order='F')
        for ispin in range(2):
            mpitool.build_HK_on(ictxt_col, nao_max, int(norbs*ispin), int(norbs*ispin), dist_on, dist_k_tmp, Son_d, SK_d_tmp, basis_def_dict, basis_milestones, species)
        
            mpitool.build_HK_off(ictxt_col, nao_max, int(norbs*ispin), int(norbs*ispin), dist_off, dist_k_tmp, Soff_d, SK_d_tmp, basis_def_dict, basis_milestones, i_idx, j_idx,
                                species, k_vec[ik].copy(), nbr_shift_d)
        mpitool.matrix_redist(dist_k_tmp, dist_k, SK_d_tmp, SK_d, 0, 0, 0, 0, 'g')
        del SK_d_tmp
        
        # HK
        HK_d_tmp = np.zeros((m_loc_k_tmp, n_loc_k_tmp), dtype=np.complex64, order='F')
        for ispin in range(2):    
            for jspin in range(2):
                index = int(2*ispin+jspin)
                Hon_d = Hsoc_on_d[index]
                Hoff_d = Hsoc_off_d[index]            
                # HK
                mpitool.build_HK_on_soc(ictxt_col, nao_max, int(norbs*ispin), int(norbs*jspin), dist_on, dist_k_tmp, Hsoc_on_d[index], HK_d_tmp, basis_def_dict, basis_milestones, species)
    
                mpitool.build_HK_off_soc(ictxt_col, nao_max, int(norbs*ispin), int(norbs*jspin), dist_off, dist_k_tmp, Hsoc_off_d[index], HK_d_tmp, basis_def_dict, basis_milestones, i_idx, j_idx,
                                    species, k_vec[ik].copy(), nbr_shift_d)
    
        mpitool.matrix_redist(dist_k_tmp, dist_k, HK_d_tmp, HK_d, 0, 0, 0, 0, 'l')
        del HK_d_tmp
        
        # diagonalization
        num_electrons = np.sum(num_val[species])
        mpitool.general_matrix_solve(1, num_electrons-num_wfns, num_electrons+num_wfns, glob_wfn, dist_k, HK_d, SK_d, eigenvec0, eigenval)
        
        mpitool.matrix_redist(dist_k, glob_SK, SK_d, SK0, 0, 0, 0, 0, 'g')
        
        if rank == 0:
            eigen.append(eigenval.copy())
            
            # wavefunction
            wfn = eigenvec0.copy().T # (nb_pick, 2*norbs)
            lamda = oe.contract('ai, ij, aj -> a', np.conj(wfn), SK0, wfn).real
            lamda = 1/np.sqrt(lamda) # shape: (nb_pick,)
            wfn = wfn*lamda[:,None]
            
            eigen_vecs.append(wfn) # (nk, nb_pick, 2*norbs)
            
            spin_up = oe.contract('mi,ij,mj -> m', np.conj(wfn[:,:norbs]), SK0[:norbs,:norbs], wfn[:,:norbs]).real
            spin_down = oe.contract('mi,ij,mj -> m', np.conj(wfn[:,norbs:]), SK0[:norbs,:norbs], wfn[:,norbs:]).real
            spin_z = (spin_up - spin_down)/2.0 # shape: (nb_pick,)
            
            spin_up = oe.contract('mi,ij,mj -> m', np.conj(wfn[:,norbs:]), SK0[:norbs,:norbs], wfn[:,:norbs]).real
            spin_down = oe.contract('mi,ij,mj -> m', np.conj(wfn[:,:norbs]), SK0[:norbs,:norbs], wfn[:,norbs:]).real
            spin_x = (spin_up + spin_down)/2.0 # shape: (nb_pick,)
            
            spin_up = 1.0j*oe.contract('mi,ij,mj -> m', np.conj(wfn[:,norbs:]), SK0[:norbs,:norbs], wfn[:,:norbs])
            spin_down = 1.0j*oe.contract('mi,ij,mj -> m', np.conj(wfn[:,:norbs]), SK0[:norbs,:norbs], wfn[:,norbs:])
            spin_y = (spin_up - spin_down).real/2.0 # shape: (nb_pick,)
            
            spin_projection.append(np.stack([spin_x, spin_y, spin_z], axis=1)) # shape: (nb_pick,3)      
    
    if rank == 0:
        eigen = np.swapaxes(np.array(eigen), 0, 1)*au2ev # (nbands, nk)   
        eigen_vecs = np.stack(eigen_vecs, axis=0)
        np.save(file=os.path.join(save_dir, 'eigen_vecs.npy'), arr=eigen_vecs)
        # plot fermi line    
        num_electrons = np.sum(num_val[species])
        print(num_electrons)
        max_val = np.max(eigen[num_electrons-1])
        min_con = np.min(eigen[num_electrons])
        eigen = eigen - max_val
        print(f"max_val = {max_val} eV")
        print(f"band gap = {min_con - max_val} eV")
        
        # plotting of band structure
        print('Plotting bandstructure...')
    
        # First make a figure object
        fig, ax = plt.subplots()
    
        # specify horizontal axis details
        ax.set_xlim(k_node[0],k_node[-1])
        ax.set_xticks(k_node)
        ax.set_xticklabels(label)
        for n in range(len(k_node)):
            ax.axvline(x=k_node[n], linewidth=0.5, color='k')
    
        # plot bands
        for n in range(norbs):
            ax.plot(k_dist, eigen[n])
        ax.plot(k_dist, nk*[0.0], linestyle='--')
    
        # put title
        ax.set_title("Band structure")
        ax.set_xlabel("Path in k-space")
        ax.set_ylabel("Band energy (eV)")
        ax.set_ylim(-2, 2)
        # make an PDF figure of a plot
        fig.tight_layout()
        plt.savefig(os.path.join(save_dir, 'Band.png'))#保存图片
        print('Done.\n')
        
        # 导出能带数据
        text_file = open(os.path.join(save_dir, 'Band.dat'), "w")
    
        text_file.write("# k_lable: ")
        for ik in range(len(label)):
            text_file.write("%s " % label[ik])
        text_file.write("\n")
    
        text_file.write("# k_node: ")
        for ik in range(len(k_node)):
            text_file.write("%f  " % k_node[ik])
        text_file.write("\n")
        
        node_index_band = node_index[1:]
        for nb in range(len(eigen)):
            for ik in range(nk):
                text_file.write("%f    %f\n" % (k_dist[ik], eigen[nb,ik]))
                if ik in node_index_band[:-1]:
                    text_file.write('\n')
                    text_file.write("%f    %f\n" % (k_dist[ik], eigen[nb,ik]))       
            text_file.write('\n')
        text_file.close()
        
        # 导出自旋数据
        spin_projection = np.swapaxes(np.array(spin_projection), 0, 1) # (nb_pick, nk, 3)
        text_file = open(os.path.join(save_dir, 'Spin.dat'), "w")
    
        text_file.write("# k_lable: ")
        for ik in range(len(label)):
            text_file.write("%s " % label[ik])
        text_file.write("\n")
    
        text_file.write("# k_node: ")
        for ik in range(len(k_node)):
            text_file.write("%f  " % k_node[ik])
        text_file.write("\n")
    
        node_index_spin = node_index[1:]
        for nb in range(len(spin_projection)):
            for ik in range(nk):
                text_file.write("%f    %f    %f    %f\n" % (k_dist[ik], *spin_projection[nb,ik]))
                if ik in node_index_spin[:-1]:
                    text_file.write('\n')
                    text_file.write("%f    %f    %f    %f\n" % (k_dist[ik], *spin_projection[nb,ik]))       
            text_file.write('\n')
        text_file.close()

if __name__ == '__main__':
    main()