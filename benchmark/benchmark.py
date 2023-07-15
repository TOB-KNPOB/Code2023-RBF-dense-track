# include .. to the system path
from inspect import getsourcefile
import os.path
import sys

current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)

import time
import argparse
from mesh4d import kps, obj3d, utils
from mesh4d.analyse import crave
from regist import reg_rbf, reg_ecpd, reg_cpd, reg_bcpd

def parse_sys_args():
    """parse system arguments"""
    parser = argparse.ArgumentParser(description='Benchmarking 4D dense tracking performance')

    parser.add_argument("--approach", default="rbf")
    parser.add_argument("--plot", default=True, action=argparse.BooleanOptionalAction)
    parser.add_argument("--export", default=True, action=argparse.BooleanOptionalAction)
    parser.add_argument("--export-folder", default='../output/12fps/rbf')
    parser.add_argument("--mesh-path", default='/Users/knpob/Territory/2-Kolmo/4-Dataset/20230715-DynaBreastLite/mesh/')
    parser.add_argument("--landmark-path", default='/Users/knpob/Territory/2-Kolmo/4-Dataset/20230715-DynaBreastLite/landmark/landmark.pkl')
    parser.add_argument("--test-landmark-path", default='/Users/knpob/Territory/2-Kolmo/4-Dataset/20230715-DynaBreastLite/test/random_landmark.pkl')
    parser.add_argument("--start", default=0)
    parser.add_argument("--end", default=120)
    parser.add_argument("--stride", default=12)

    return parser.parse_args()


class Benchmarker:
    def __init__(self, args, obj4d_class):
        self.args = args
        self.obj4d_class = obj4d_class
        self.origin_fps = 120
        self.fps = self.origin_fps / self.args.stride

        self.load_data()
        self.implement()
        self.eval_control_landmark()
        self.eval_noncontrol_landmark()
        self.eval_virtual_landmark()
        self.eval_deformation_intensity()

    def load_data(self):
        """load data"""
        # load mesh from paths
        mesh_ls, texture_ls = obj3d.load_mesh_series(
            folder = self.args.mesh_path,
            start = self.args.start,
            stride = self.args.stride,
            end = self.args.end,
        )
        mesh_ls = [crave.fix_pvmesh_disconnect(mesh) for mesh in mesh_ls]

        # load landmarks from paths
        landmarks = utils.load_pkl_object(self.args.landmark_path)
        landmarks.interp_field()
        landmarks = landmarks.reslice(self.fps)
        landmarks.interp_field()

        # automatic breast crop
        contour = landmarks.extract(('marker 0', 'marker 2', 'marker 3', 'marker 14', 'marker 15', 'marker 17'))
        mesh_clip_ls = crave.clip_with_contour(mesh_ls, start_time=0, fps=self.origin_fps / self.args.stride, contour=contour, clip_bound='xy', margin=30)

        # create obj3d object lists for cropped breast
        self.breast_ls = obj3d.init_obj_series(
            mesh_clip_ls,
            obj_type=obj3d.Obj3d_Deform
            )
        
    def implement(self):
        pass

    def eval_control_landmark(self):
        pass

    def eval_noncontrol_landmark(self):
        pass

    def eval_virtual_landmark(self):
        pass

    def eval_deformation_intensity(self):
        pass


class Bemchmarker_marker_guided(Benchmarker):
    pass


class Bemchmarker_marker_less(Benchmarker):
    pass


if __name__ == "__main__":
    args = parse_sys_args()
    Benchmarker(args, "")