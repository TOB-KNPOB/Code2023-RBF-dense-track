export digits=%04d
export frame_size=300
export file_name=vkps_random

for fps in 10 60 120
do
    mkdir ./$(echo $fps)fps/

    for approach in rbf ecpd cpd bcpd
    do
        export source=../output/$(echo $fps)fps/$approach
        export destination=./$(echo $fps)fps/$approach
        mkdir $destination
        cp $source/$file_name.mp4 $destination

        magick convert -coalesce $destination/*.mp4 $destination/temp$digits.png
        magick mogrify -resize $frame_size $destination/*.png
        magick convert -coalesce $destination/*.png $destination/$file_name.gif

        rm $destination/*.mp4 $destination/*.png
    done
done