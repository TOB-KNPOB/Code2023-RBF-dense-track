"""Replace the simple nearest point alignment displacement field estimation workflow with Coherent Point Drift (CPD) based approach."""
from __future__ import annotations
from typing import Type, Union, Iterable

import copy
import numpy as np
import open3d as o3d
import pyvista as pv
from probreg import cpd
from scipy.interpolate import RBFInterpolator

import mesh4d
import mesh4d.config.param
from mesh4d import obj3d, obj4d, field

class Trans_Nonrigid_CPD(field.Trans_Nonrigid):
    """Derived from :class:`mesh4d.field.Trans_Nonrigid` and replace the displacement field estimation as Coherent Point Drift (CPD) based approach.
    """
    def regist(self, sample_num: int = 1000, field_nbr: int = 100, scale_rate: float = 100, **kwargs):
        """The registration method.

        Parameters
        ---
        sample_num
            the number of the points sampled from the mesh to construct the point cloud.
            
            Attention
            ---
            Since the Coherent Point Drift (CPD) is not very efficient, the number of the sampling points used to estimate the displacement field should relatively small. The default value is :code:`1000`.
        field_nbr
            tbf
        scale_rate
            scale the point cloud to guarantee convergence within limits of iteration.
        **kwargs
            Configurations parameters of the registration.
            
        See Also
        --------
        `probreg.cpd.registration_cpd <https://probreg.readthedocs.io/en/latest/probreg.html?highlight=registration_cpd#probreg.cpd.registration_cpd>`_
        """
        # registration
        source_pcd = obj3d.np2pcd(self.source.get_sample_points(sample_num) / scale_rate)
        target_pcd = obj3d.np2pcd(self.target.get_sample_points(sample_num) / scale_rate)

        tf_param, _, _ = cpd.registration_cpd(
            source=source_pcd, 
            target=target_pcd, 
            tf_type_name='nonrigid',
            **kwargs
            )
        
        # parse
        deform = copy.deepcopy(source_pcd)
        deform.points = tf_param.transform(deform.points)
        self.deform_points = obj3d.pcd2np(deform) * scale_rate

        self.source_points = self.source.get_sample_points(sample_num)
        self.field = RBFInterpolator(self.source_points, self.deform_points, neighbors=field_nbr)


class Obj4d_CPD(obj4d.Obj4d_Deform):
    """Derived from :class:`mesh4d.obj4d.Obj4d_Deform` and replace the displacement field estimation as Coherent Point Drift (CPD) based approach.

    Parameters
    ---
    regist_points_num
        the number of the points sampled from the mesh for registration.
            
            Attention
            ---
            Since the Coherent Point Drift (CPD) is not very efficient, the number of the sampling points used to estimate the displacement field should relatively small. The default value is :code:`3000`.
    """
    def __init__(self, regist_points_num: int = 1000, **kwargs):
        obj4d.Obj4d_Deform.__init__(self, **kwargs)
        self.regist_points_num = regist_points_num

    def process_nonrigid_dynamic(self, idx_source: int, idx_target: int, **kwargs):
        trans = Trans_Nonrigid_CPD(
            source_obj=self.obj_ls[idx_source],
            target_obj=self.obj_ls[idx_target],
        )
        trans.regist(sample_num=self.regist_points_num, **kwargs)
        self.obj_ls[idx_source].set_trans_nonrigid(trans)