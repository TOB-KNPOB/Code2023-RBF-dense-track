# retrieve quantitative plots
mkdir graph
cp -r ../benchmark/output/graph/ .

# retrieve qualitative plots
export scale=0.5

for fps in 10 60 120
do
    mkdir ./$(echo $fps)fps/

    for approach in udmc ecpd cpd bcpd
    do
        export source=../../benchmark/output/$(echo $fps)fps/$approach
        export destination=./$(echo $fps)fps/$approach
        mkdir $destination
        
        # retrieve mp4 and resize it
        # the ffmpeg package is needed:
        # $ sudo apt update
        # $ sudo apt install ffmpeg
        cp $source/vkps_random.mp4 $destination/original.mp4
        ffmpeg -i $destination/original.mp4 -vf scale="iw*$scale:ih*$scale" -y $destination/vkps_random.mp4
        rm $destination/original.mp4

        # retrieve trace image
        cp $source/vkps_random_trace.png $destination
    done
done