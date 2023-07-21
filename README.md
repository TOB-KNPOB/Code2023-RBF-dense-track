# An exploratory semi-automatic approach for dense tracking of breast motion in 4D

## Graphical abstract

![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/workflow.png?raw=true)

## `DynaBreastLite` dataset

A lightweight dynamic 4D human breast anthropometric dataset constructed in this study. Data will be released after acceptance of the manuscript.

## Virtual landmarks tracking

Tracking arbitrary landmarks' trajectories. Noted that the selection of virtual landmarks are merely for visual clarity. Under the hood, every point on the breast surface can be densely tracked based on the continues fullfield dense correspondence mapping described in subsection 3.3

### 10 fps

| Ours | ECPD [^ecpd] | CPD [^cpd] | BCPD [^bcpd] |
| :---: | :---: | :---: | :--: |
| ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/rbf/vkps_random.gif?raw=ture) | ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/ecpd/vkps_random.gif?raw=ture) | ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/cpd/vkps_random.gif?raw=ture) | ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/bcpd/vkps_random.gif?raw=ture) |
| ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/rbf/vkps_random_trace.png?raw=ture) | ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/ecpd/vkps_random_trace.png?raw=ture) | ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/cpd/vkps_random_trace.png?raw=ture) | ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/bcpd/vkps_random_trace.png?raw=ture) |


### 60 fps

| Ours | ECPD [^ecpd] | CPD [^cpd] | BCPD [^bcpd] |
| :---: | :---: | :---: | :--: |
| ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/rbf/vkps_random.gif?raw=ture) | ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/ecpd/vkps_random.gif?raw=ture) | ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/cpd/vkps_random.gif?raw=ture) | ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/bcpd/vkps_random.gif?raw=ture) |
| ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/rbf/vkps_random_trace.png?raw=ture) | ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/ecpd/vkps_random_trace.png?raw=ture) | ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/cpd/vkps_random_trace.png?raw=ture) | ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/bcpd/vkps_random_trace.png?raw=ture) |


### 120 fps

| Ours | ECPD [^ecpd] | CPD [^cpd] | BCPD [^bcpd] |
| :---: | :---: | :---: | :--: |
| ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/rbf/vkps_random.gif?raw=ture) | ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/ecpd/vkps_random.gif?raw=ture) | ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/cpd/vkps_random.gif?raw=ture) | ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/bcpd/vkps_random.gif?raw=ture) |
| ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/rbf/vkps_random_trace.png?raw=ture) | ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/ecpd/vkps_random_trace.png?raw=ture) | ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/cpd/vkps_random_trace.png?raw=ture) | ![img](https://github.com/TOB-KNPOB/code2023-rbf-dense-track/blob/main/graphic/10fps/bcpd/vkps_random_trace.png?raw=ture) |

[^ecpd]: Golyanik, Vladislav, et al. "Extended coherent point drift algorithm with correspondence priors and optimal subsampling." 2016 IEEE winter conference on applications of computer vision (WACV). IEEE, 2016.
[^cpd]: Myronenko, Andriy, and Xubo Song. "Point set registration: Coherent point drift." IEEE transactions on pattern analysis and machine intelligence 32.12 (2010): 2262-2275.
[^bcpd]: Hirose, Osamu. "A Bayesian formulation of coherent point drift." IEEE transactions on pattern analysis and machine intelligence 43.7 (2020): 2269-2286.