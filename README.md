# Ultra-dense Motion Capture: An exploratory full-automatic approach for dense tracking of breast motion in 4D

For demo videos, please visit our [paper page](https://liu-qilong.github.io/udmc/).

## Setup

First install [mesh4d](https://github.com/liu-qilong/mesh4d) package and create a virtual environment:

```
git clone https://github.com/liu-qilong/mesh4d.git
cd mesh4d
conda create -n mesh4d
conda activate mesh4d
pip install -r requirements.txt
python -m pip install --editable .
```

Clone this repository:

```
cd ..
git clone https://github.com/liu-qilong/udmc
cd udmc
conda activate mesh4d
```

### Compatibility

[mesh4d](https://github.com/liu-qilong/mesh4d) package is under active development and breaking changes may be introduced. If you encounter any issues, please try to roll-back to a compatible version of `mesh4d` by running this command under the `mesh4d/` folder:

```
git reset --hard c3ee229da0660c1f32dd005a11ea93c6a704e231
```

## Run

### Get data

Download the [dyna-breast-lite](https://huggingface.co/datasets/liu-qilong/dyna-breast-lite/tree/main) dataset.

### Vicon to 3dMD alignment

Please refer to python script & jupyter notebooks in `autolabel/` folder:

- Spatial alignment
    - `kps_extract.py`
    Used for extracting corresponding key points to the Vicon keypoints from 3dMD 4D scanning sequences scanned under static posture.
    - `align_space.ipynb`
    Estimate the transformation matrix between Vicon and 3dMD coordinate systems.
- Temporal alignment
    - `texture_extract.ipynb`
    Used for extracting texture information from 3dMD 4D scanning sequences, i.e. RGB values of all vertices.
    - `marker_extract.ipynb`
    Extract a set of potential marker points from the 3dMD 4D scanning sequences with pre-set rules and thresholds.
    - `align_time.ipynb`
    Estimate the temporal offset between Vicon and 3dMD sequences.

_P.S. Due to privacy constraint, the texture of all 3dMD sequences has been removed. Therefore you can't directly run these scripts with our data. You can however adapted them for your own data._

### Run the experiments

To replicate the experiments, fill the dataset folder path to the first line of `benchmark/benchmark.sh`, e.g.

```
export data_folder=../../../data/DynaBreastLite
```

And then simply run:

```
conda activate mesh4d
cd benchmark
./benchmark.sh
```

### Workflow details

`benchmark.sh` is a shell script that called `benchmark.py` with different arguments to benchmark performance of our methods as well as the baseline methods.

If you are interested in the detail, please refer to the implementation of the `Bemchmarker_marker_guided` and `Bemchmarker_marker_less` classes, which mainly includes:

- `load_data()`: Load the data from the dataset and automatically crop out the breast region.
- `implement()`: Run the shape-correspondence estimation method to track the breast motion.
- `eval_control_landmark()`: Evaluate the tracking accuracy of the control landmarks.
- `eval_noncontrol_landmark()`: Evaluate the tracking accuracy of the arbitrary landmarks.
- `eval_virtual_landmark()`: Output the tracking trajectories of a set of arbitrarily selected landmarks from the surface.
- `eval_deformation_intensity()`: Estimate the deformation intensity of the breast throughout the movement.
- `export()`: Save the benchmark results.

## Citation

```
@article{LiuQilong2024,
	title = {Ultra-dense Motion Capture{:} An exploratory full-automatic approach for dense tracking of breast motion in 4D},
	volume = {19},
	issn = {1932-6203},
	url = {http://dx.doi.org/10.1371/journal.pone.0299040},
	doi = {10.1371/journal.pone.0299040},
	number = {2},
	journal = {PLoS One},
	publisher = {Public Library of Science (PLoS)},
	author = {Liu,  Qi-Long and Yick,  Kit-Lun and Sun,  Yue and Yip,  Joanne},
	editor = {Lu,  Yawen},
	year = {2024},
	month = {2},
	pages = {e0299040},
}

```