export fps_test=10
export fps_origin=120

for approach in rbf ecpd cpd bcpd
do
    python benchmark.py --approach $approach --stride $(expr $fps_origin / $fps_test) --export-folder ../output/$(echo $fps_test)fps/$approach # --no-plot
done