"""Replace the simple nearest point alignment displacement field estimation workflow with Extend Coherent Point Drift (ECPD) based approach. Comparing with basic CPD, ECPD considers prior correspondence to improve the registration quality."""
from __future__ import annotations
from typing import Type, Union, Iterable

import copy
import open3d as o3d
import pyvista as pv
from probreg import cpd
from scipy.spatial import KDTree
from scipy.interpolate import RBFInterpolator

import mesh4d
import mesh4d.config.param
from mesh4d import obj3d, obj4d, field, utils

class Trans_Nonrigid_ECPD(field.Trans_Nonrigid):
    """Derived from :class:`mesh4d.field.Trans_Nonrigid` and replace the displacement field estimation as Coherent Point Drift (CPD) based approach.
    """
    def regist(self, landmark_name: str, sample_num = 1000, field_nbr: int = 100, scale_rate: float = 100, **kwargs):
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
        # sampling source & target mesh
        source_points = self.source.get_sample_points(sample_num)
        target_points = self.target.get_sample_points(sample_num)

        # get source & target correspondence
        def get_landmarks_idx(mesh_points, landmarks_points):
            tree = KDTree(mesh_points)
            _, idx = tree.query(landmarks_points)
            return idx

        landmarks_source = self.source.kps_group[landmark_name].get_points_coord()
        landmarks_target = self.target.kps_group[landmark_name].get_points_coord()

        idx_source = get_landmarks_idx(source_points, landmarks_source)
        idx_target = get_landmarks_idx(target_points, landmarks_target)

        # registration
        source_pcd = obj3d.np2pcd(source_points / scale_rate)
        target_pcd = obj3d.np2pcd(target_points /scale_rate)
        
        tf_param, _, _ = cpd.registration_cpd(
            source=source_pcd, 
            target=target_pcd, 
            tf_type_name='nonrigid_constrained',
            idx_source=idx_source,
            idx_target=idx_target,
            **kwargs
            )

        # parse
        deform = copy.deepcopy(source_pcd)
        deform.points = tf_param.transform(deform.points)
        self.deform_points = obj3d.pcd2np(deform) * scale_rate
        
        self.source_points = source_points
        self.field = RBFInterpolator(self.source_points, self.deform_points, neighbors=field_nbr)


class Obj4d_ECPD(obj4d.Obj4d_Deform):
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

    def regist(self, landmark_name: str, **kwargs):
        """Implement registration among 3D objects in :attr:`self.obj_ls`.

        Parameters
        ---
        landmarks
            the control landmarks to guide the registration.
        
        **kwargs
            configuration parameters for the registration and the configuration parameters of the base classes (:class:`Obj3d` and :class:`Obj3d_Kps`)'s :meth:`add_obj` method can be passed in via :code:`**kwargs`.
        """        
        reg_num = len(self.obj_ls)
        
        for idx in range(reg_num):
            if idx == 0:
                self.process_first_obj()
                continue

            if self.enable_rigid:
                self.process_rigid_dynamic(idx - 1, idx, **kwargs)  # aligned to the previous one

            if self.enable_nonrigid:
                self.process_nonrigid_dynamic(idx - 1, idx, landmark_name, **kwargs)  # aligned to the later one
            
            if mesh4d.output_msg:
                percent = (idx + 1) / reg_num
                utils.progress_bar(percent, back_str=" registered the {}-th frame".format(idx))


    def process_nonrigid_dynamic(self, idx_source: int, idx_target: int, landmark_name: str, **kwargs):
        trans = Trans_Nonrigid_ECPD(
            source_obj=self.obj_ls[idx_source],
            target_obj=self.obj_ls[idx_target],
        )
        trans.regist(landmark_name, sample_num=self.regist_points_num, **kwargs)
        self.obj_ls[idx_source].set_trans_nonrigid(trans)