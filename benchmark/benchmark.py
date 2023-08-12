# include .. to the system path
import sys
import os.path
from inspect import getsourcefile

current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)

import time
import argparse
import pyvista as pv
import mesh4d
from mesh4d import kps, obj3d, utils
from mesh4d.analyse import crave, visual, measure

from regist import reg_rbf, reg_ecpd, reg_cpd, reg_bcpd

def sys_args_parser() -> argparse.ArgumentParser:
    """parse system arguments"""
    parser = argparse.ArgumentParser(description='Benchmarking 4D dense tracking performance')

    parser.add_argument("--approach", default="rbf", type=str)
    parser.add_argument("--plot", default=True, type=bool, action=argparse.BooleanOptionalAction)
    parser.add_argument("--export", default=True, type=bool, action=argparse.BooleanOptionalAction)
    parser.add_argument("--keep-plot-win", default=True, type=bool, action=argparse.BooleanOptionalAction)
    parser.add_argument("--export-folder", default='../output/10fps/rbf', type=str)
    parser.add_argument("--mesh-path", default='/Users/knpob/Territory/2-Kolmo/4-Dataset/20230715-DynaBreastLite/mesh/', type=str)
    parser.add_argument("--landmark-path", default='/Users/knpob/Territory/2-Kolmo/4-Dataset/20230715-DynaBreastLite/landmark/landmark.pkl', type=str)
    parser.add_argument("--test-landmark-path", default='/Users/knpob/Territory/2-Kolmo/4-Dataset/20230715-DynaBreastLite/test/random_landmark.pkl', type=str)
    parser.add_argument("--start", default=0, type=int)
    parser.add_argument("--end", default=120, type=int)
    parser.add_argument("--stride", default=12, type=int)

    return parser


class Benchmarker:
    def __init__(self, args: argparse.Namespace, meta: dict):
        self.args = args
        self.meta = meta
        self.origin_fps = 120
        self.fps = self.origin_fps / self.args.stride

        print('=' * 50)
        print(f'benchmarking {self.args.approach} on {self.fps}fps')

        if not os.path.exists(self.args.export_folder):
            os.makedirs(self.args.export_folder)
            print(f'created export folder: {self.args.export_folder}')

    def load_data(self):
        """load data"""
        print('-' * 50)
        print('data loading')

        # load mesh from paths
        mesh_ls, texture_ls = obj3d.load_mesh_series(
            folder = self.args.mesh_path,
            start = self.args.start,
            stride = self.args.stride,
            end = self.args.end,
        )
        mesh_ls = [crave.fix_pvmesh_disconnect(mesh) for mesh in mesh_ls]

        # load landmarks from paths
        self.landmarks = utils.load_pkl_object(self.args.landmark_path)

        # automatic breast crop
        contour = self.landmarks.extract(('marker 0', 'marker 2', 'marker 3', 'marker 14', 'marker 15', 'marker 17'))
        mesh_clip_ls = crave.clip_with_contour(mesh_ls, start_time=0, fps=self.fps, contour=contour, clip_bound='xy', margin=30)

        # create obj3d object lists for cropped breast
        self.breast_ls = obj3d.init_obj_series(
            mesh_clip_ls,
            obj_type=obj3d.Obj3d_Deform
            )
        
    def implement(self):
        print('-' * 50)
        print('implement 4d registration approach')
        pass

    def eval_control_landmark(self):
        print('-' * 50)
        print('evaluate alignment on control landmarks')
        pass

    def eval_noncontrol_landmark(self):
        print('-' * 50)
        print('evaluate alignment on non-control landmarks')
        pass

    def eval_virtual_landmark(self):
        print('-' * 50)
        print('evaluate virtual landmarks tracking performance')

        random_landmarks = utils.load_pkl_object(self.args.test_landmark_path)
        random_kps = random_landmarks.get_frame_coord(0)

        self.o4.vkps_track(random_kps, start_id=0, name='vkps_random')
        vkps_random = self.o4.assemble_markerset(name='vkps_random')
        vkps_random.interp_field()

        # animation
        if self.args.plot and self.args.export:
            self.o4.animate(output_folder=self.args.export_folder, filename='vkps_random', kps_names=('vkps_random',), m_props={'opacity': 0.5}, k_props={'color': 'royalblue'})

        # stack plot
        if self.args.plot:
            scene = self.o4.show(elements='pk', stack_dist=500, kps_names=('vkps_random',), window_size=[2000, 500],  zoom_rate=5, skip=round(len(self.breast_ls) / 10), p_props={'color': 'gray'}, k_props={'color': 'royalblue'}, is_save=self.args.export, export_folder=self.args.export_folder, export_name='vkps_random_stack')

            if not self.args.keep_plot_win:
                scene.close()

        # trace plot
        if self.args.plot:
            scene = pv.Plotter()
            vkps_random.add_to_scene(scene)
            self.breast_ls[0].add_mesh_to_scene(scene, opacity=0.1)
            scene.camera_position = 'xy'

            if self.args.export:
                export_path = os.path.join(self.args.export_folder, 'vkps_random_trace.png')
                scene.show(screenshot=export_path, interactive_update=True)

                if mesh4d.output_msg:
                    print("export image: {}".format(export_path))

            else:
                scene.show(interactive_update=True)

            if not self.args.keep_plot_win:
                scene.close()
            
    def eval_deformation_intensity(self):
        print('-' * 50)
        print('evaluate deformation intensity analysis performance')

        breast_kps = self.breast_ls[1].get_sample_kps(100)
        self.o4.vkps_track(breast_kps, start_id=1, name='vkps_breast_full')

        vkps_breast_full = self.o4.assemble_markerset(name='vkps_breast_full', start_id=1)
        vkps_breast_full.interp_field()

        _, starts, traces = measure.markerset_trace_length(vkps_breast_full, start_frame=0)

        # deformation intensity plot
        if self.args.plot:
            scene = visual.show_mesh_value_mask(
                self.breast_ls[1].mesh, starts, traces,
                is_save=self.args.export, export_folder=self.args.export_folder, export_name='breast_disp',
                show_edges=True, scalar_bar_args={'title': "tragcctory lenght (mm)"})
            
            if not self.args.keep_plot_win:
                scene.close()

    def export(self):
        """export benchmarker obj to disk with evaluated metrics"""
        print('-' * 50)
        print('export benchmark results')

        self.meta = None
        self.landmarks = None
        self.breast_ls = None
        self.o4 = None

        utils.save_pkl_object(self, self.args.export_folder, 'benchmark')
        

class Bemchmarker_marker_guided(Benchmarker):
    def implement(self):
        super().implement()
        start_time = time.time()

        self.o4 = self.meta['obj4d_class'](
            fps=self.fps,
            enable_rigid=False,
            enable_nonrigid=True,
        )
        self.o4.add_obj(*self.breast_ls)
        self.o4.load_markerset('landmarks', self.landmarks)
        self.o4.regist('landmarks', **self.meta['regist_props'])

        self.duration = time.time() - start_time
        print(f'4d registrtion time: {self.duration:.2f} (s)')

    def eval_control_landmark(self):
        super().eval_control_landmark()

        kps_source = self.landmarks.get_time_coord(0)
        self.o4.vkps_track(kps_source, start_id=0, name='vkps_control')
        vkps_control = self.o4.assemble_markerset(name='vkps_control')
        self.diff_control = kps.MarkerSet.diff(vkps_control, self.landmarks)

        # control landmarks plot
        if self.args.plot and self.args.export:
            self.o4.animate(self.args.export_folder, filename='vkps_control', kps_names=('landmarks', 'vkps_control'), m_props={'opacity': 0.5})

    def eval_noncontrol_landmark(self):
        super().eval_noncontrol_landmark()
        import time
        mesh4d.output_msg = False

        self.diff_noncontrol = {}
        self.diff_noncontrol_brief = []

        for name in self.landmarks.markers.keys():
            # split dataset
            landmarks_test, landmarks_train = self.landmarks.split((name, ))

            # registration
            start_time = time.time()

            self.o4 = self.meta['obj4d_class'](
                fps=self.fps,
                enable_rigid=False,
                enable_nonrigid=True,
            )
            self.o4.add_obj(*self.breast_ls)
            self.o4.load_markerset('landmarks_train', landmarks_train)
            self.o4.load_markerset('landmarks_test', landmarks_test)
            self.o4.regist('landmarks_train', **self.meta['regist_props'])

            # computation time
            duration = time.time() - start_time
            print(f"computation time: {duration:.2f} (s)")

            # virtual key points tracking
            kps_source = landmarks_test.get_time_coord(0)
            self.o4.vkps_track(kps_source, start_id=0, name='vkps')
            
            # quantitative estimation
            vkps = self.o4.assemble_markerset(name='vkps')
            diff = kps.MarkerSet.diff(vkps, landmarks_test)

            # store result
            self.diff_noncontrol[name] = diff
            brief_str = f"{name}: test error: {diff['diff_str']}"
            self.diff_noncontrol_brief.append(brief_str)
            print(brief_str)

        mesh4d.output_msg = True

        
class Bemchmarker_marker_less(Benchmarker):
    def implement(self):
        super().implement()
        start_time = time.time()
    
        self.o4 = self.meta['obj4d_class'](
            fps=self.fps,
            enable_rigid=False,
            enable_nonrigid=True,
        )
        self.o4.add_obj(*self.breast_ls)
        self.o4.load_markerset('landmarks', self.landmarks)
        self.o4.regist(**self.meta['regist_props'])

        self.duration = time.time() - start_time
        print(f'4d registrtion time: {self.duration:.2f} (s)')

    def eval_control_landmark(self):
        super().eval_control_landmark()
        print("n/a")
        self.diff_control = None

    def eval_noncontrol_landmark(self):
        super().eval_noncontrol_landmark()

        kps_source = self.landmarks.get_time_coord(0)
        self.o4.vkps_track(kps_source, start_id=0, name='vkps_noncontrol')
        vkps_noncontrol = self.o4.assemble_markerset(name='vkps_noncontrol')
        self.diff_noncontrol = kps.MarkerSet.diff(vkps_noncontrol, self.landmarks)


if __name__ == "__main__":
    parser = sys_args_parser()
    args = parser.parse_args()

    approach_dict = {
        'rbf': {'benchmarker': Bemchmarker_marker_guided, 'obj4d_class': reg_rbf.Obj4d_RBF, 'regist_props': {}},
        'ecpd': {'benchmarker': Bemchmarker_marker_guided, 'obj4d_class': reg_ecpd.Obj4d_ECPD, 'regist_props': {}},
        'cpd': {'benchmarker': Bemchmarker_marker_less, 'obj4d_class': reg_cpd.Obj4d_CPD, 'regist_props': {}},
        'bcpd': {'benchmarker': Bemchmarker_marker_less, 'obj4d_class': reg_bcpd.Obj4d_BCPD, 'regist_props': {}},
    }

    meta= approach_dict[args.approach]
    benchmarker_class = meta['benchmarker']
    benchmarker = benchmarker_class(args, meta)

    benchmarker.load_data()
    benchmarker.implement()
    benchmarker.eval_control_landmark()
    # benchmarker.eval_noncontrol_landmark()
    benchmarker.eval_virtual_landmark()
    benchmarker.eval_deformation_intensity()

    # if args.export:
    #     benchmarker.export()