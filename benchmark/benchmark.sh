export fps_origin=120

for fps_test in 10 60 120
do
    for approach in udmc ecpd cpd bcpd
    do
        python benchmark.py --approach $approach --stride $(expr $fps_origin / $fps_test) --export-folder output/$(echo $fps_test)fps/$approach --no-keep-plot-win
    done
done