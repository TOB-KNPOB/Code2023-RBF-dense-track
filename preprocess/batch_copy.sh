export start=1
export end=120
export source_path="/mnt/d/knpob/4-data/20211229-DynaBreast4D/3dmd/6kmh_27marker_2/meshes/speed_6km_h_26_marker_set_2."
export target_path="/mnt/d/knpob/4-data/20231110-DynaBreastLite/mesh/"

for i in $(seq -f "%06g" $start $end)
do
  cp ${source_path}${i}.obj ${target_path}${i}.obj
done