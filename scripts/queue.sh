#!/bin/bash 

# sbatch mdconvert.sh ../md_out/water/0M-4.0-c

#----------------------------------------------------------------#
# MDCOPY1

# Run water EF simulations

# foo='abc'

# mol=0

# for (( i=0; i<${#foo}; i++ )); do


# for x in {0..9}; do
#        x=$((x*2))
#      y=`bc <<< "scale=1; $x/10"`
#      temp="sbatch cpu-small.sh md-Copy1.py -mol ${mol} -ef 0${y} -box 150 -ptime 5 -o water/150A -desc ${foo:$i:1} -temperature 291.15"
#      $temp
# done

# for x in {10..24}; do
#        x=$((x*2))
#      y=`bc <<< "scale=1; $x/10"`
#      temp="sbatch cpu-small.sh md-Copy1.py -mol ${mol} -ef ${y} -box 150 -ptime 5 -o water/150A -desc ${foo:$i:1} -temperature 291.15"
#      $temp
# done

# for x in {1..10}; do
#     x=$((x*50))
#      y=`bc <<< "scale=1; $x/10"`
#      temp="sbatch cpu-small.sh md-Copy1.py -mol ${mol} -ef ${y} -box 150 -ptime 5 -o water/150A -desc ${foo:$i:1} -temperature 291.15"
#      $temp
# done


# done



# Run ionbox EF simulations

# file=../md_out/ions/MD_$(date +"%b%d_%I_%M%p").txt

# foo='abc'

# temp=293.15

# # mol=0.172
# mol=0.346

# box=30

# for (( i=0; i<${#foo}; i++ )); do


# for x in {1..9}; do
#      y=`bc <<< "scale=2; $x/100"`
#      cmd="sbatch gpu.sh md-Copy1.py -mol ${mol} -ef 0${y} -box ${box} -ptime 5 -o ions/temp -desc ${foo:$i:1} -temperature ${temp} -subset True"
#       $cmd
# done

# for x in {1..9}; do
#      y=`bc <<< "scale=1; $x/10"`
#      cmd="sbatch gpu.sh md-Copy1.py -mol ${mol} -ef 0${y} -box ${box} -ptime 5 -o ions/temp -desc ${foo:$i:1} -temperature ${temp} -subset True"
#      $cmd
# done

# for x in {10..12}; do
#      y=`bc <<< "scale=1; $x/10"`
#      cmd="sbatch gpu.sh md-Copy1.py -mol ${mol} -ef ${y} -box ${box} -ptime 5 -o ions/temp -desc ${foo:$i:1} -temperature ${temp} -subset True"
#      $cmd
# done

# for ((j=1; j<6; j++)); do
#     x=$((j*50))
#     y=`bc <<< "scale=1; $x/10"`
#          cmd="sbatch gpu.sh md-Copy1.py -mol ${mol} -ef ${y} -box ${box} -ptime 5 -o ions/temp -desc ${foo:$i:1} -temperature ${temp} -subset True"
#       $cmd
# done


# done
# sbatch gpu.sh md-Copy1.py -mol ${mol} -ef 0 -box ${box} -ptime 5 -o ions/temp -desc ${foo:$i:1} -temperature ${temp} -subset True

#----------------------------------------------------------------#
# CONDUCT
# Group queue HEWL/ion conductivity


# HEWL
# foo='abc'
# run='run3'

# for (( i=0; i<${#foo}; i++ )); do

# for x in {1..9}; do
#      y=`bc <<< "scale=2; $x/100"`
#       sbatch cpu-small.sh conduct.py -f NVT-0$y-${foo:$i:1}.h5 -o HEWLmd/$run -axis 2
# done

# for x in {1..9}; do
#      y=`bc <<< "scale=1; $x/10"`
#       sbatch cpu-small.sh conduct.py -f NVT-0$y-${foo:$i:1}.h5 -o HEWLmd/$run -axis 2
# done

# for x in {10..12}; do
#      y=`bc <<< "scale=1; $x/10"`
#       sbatch cpu-small.sh conduct.py -f NVT-$y-${foo:$i:1}.h5 -o HEWLmd/$run -axis 2
# done


# done

# IONS

# foo='abc'
# mol=0.172
# for (( i=0; i<${#foo}; i++ )); do


# for x in {1..9}; do
#      y=`bc <<< "scale=2; $x/100"`
#      sbatch cpu-small.sh conduct.py -f ${mol}M-0$y-${foo:$i:1}.h5 -o md_out/ions/150A_293.15 -axis 0
# done

# for x in {1..9}; do
#      y=`bc <<< "scale=1; $x/10"`
#      sbatch cpu-small.sh conduct.py -f ${mol}M-0$y-${foo:$i:1}.h5 -o md_out/ions/150A_293.15 -axis 0
# done

# for x in {10..12}; do
#      y=`bc <<< "scale=1; $x/10"`
#      sbatch cpu-small.sh conduct.py -f ${mol}M-$y-${foo:$i:1}.h5 -o md_out/ions/150A_293.15 -axis 0
# done

# for ((j=1; j<6; j++)); do
#     x=$((j*50))
#     y=`bc <<< "scale=1; $x/10"`
#     sbatch cpu-small.sh conduct.py -f ${mol}M-$y-${foo:$i:1}.h5 -o md_out/ions/150A_293.15 -axis 0
# done


# done




# for x in {1..9}; do
#      y=`bc <<< "scale=2; $x/100"`
#       sbatch cpu-small.sh conduct.py -f 0.346M-0$y-${foo:$i:1}.h5 -o md_out/ions/291.15 -axis 0
# done

# for x in {1..9}; do
#      y=`bc <<< "scale=2; $x/100"`
#       sbatch cpu-small.sh conduct.py -f 0.172M-0$y-${foo:$i:1}.h5 -o md_out/ions/291.15 -axis 0
# done




# for x in {1..9}; do
#      y=`bc <<< "scale=1; $x/10"`
#       sbatch cpu-small.sh conduct.py -f 0.346M-0$y-${foo:$i:1}.h5 -o md_out/ions/291.15 -axis 0
# done

# for x in {10..12}; do
#      y=`bc <<< "scale=1; $x/10"`
#       sbatch cpu-small.sh conduct.py -f 0.346M-$y-${foo:$i:1}.h5 -o md_out/ions/291.15 -axis 0
# done

# for x in {1..9}; do
#      y=`bc <<< "scale=1; $x/10"`
#       sbatch cpu-small.sh conduct.py -f 0.346M-0$y-${foo:$i:1}.h5 -o md_out/ions/60A_293.15 -axis 0
# done

# for x in {10..12}; do
#      y=`bc <<< "scale=1; $x/10"`
#       sbatch cpu-small.sh conduct.py -f 0.346M-$y-${foo:$i:1}.h5 -o md_out/ions/60A_293.15 -axis 0
# done

# for x in {3..10}; do
#     x=$((x*5))
#      y=`bc <<< "scale=1; $x/10"`
#      sbatch cpu-small.sh conduct.py -f 0.346M-$y-${foo:$i:1}.h5 -o md_out/ions/60A_293.15 -axis 0
# done

# mol=0.346
# for ((j=1; j<6; j++)); do
#     x=$((j*50))
#     y=`bc <<< "scale=1; $x/10"`
#      sbatch cpu-small.sh conduct.py -f ${mol}M-$y-${foo:$i:1}.h5 -o md_out/ions/60A_293.15
# done
# for ((j=1; j<6; j++)); do
#     x=$((j*50))
#     y=`bc <<< "scale=1; $x/10"`
#      sbatch cpu-small.sh conduct.py -f ${mol}M-$y-${foo:$i:1}.h5 -o md_out/ions/291.15
# done

# done




# 291.15 IONS

# file=../md_out/ions/CONDUCT_$(date +"%b%m_%I_%M%p").txt

# foo='abc'

# mol=0.172
# mol=0.346

# for (( i=0; i<${#foo}; i++ )); do


# for x in {1..9}; do
#      y=`bc <<< "scale=1; $x/10"`
#      temp="sbatch cpu-small.sh conduct.py -f ${mol}M-0${y}-${foo:$i:1}.h5 -o md_out/ions/60A_293.15"
#      echo $temp >> $file
#      $temp
# done

# for x in {10..12}; do
#      y=`bc <<< "scale=1; $x/10"`
#      temp="sbatch cpu-small.sh conduct.py -f ${mol}M-${y}-${foo:$i:1}.h5 -o md_out/ions/60A_293.15"
#      echo $temp >> $file
#      $temp
# done

# for x in {3..10}; do
#     x=$((x*5))
#      y=`bc <<< "scale=1; $x/10"`
#      temp="sbatch cpu-small.sh conduct.py -f 0.172M-${y}-${foo:$i:1}.h5 -o md_out/ions/60A_293.15"
# #       $temp >> $file
#       $temp
# done

# for x in {3..10}; do
#     x=$((x*5))
#      y=`bc <<< "scale=1; $x/10"`
#      temp="sbatch cpu-small.sh conduct.py -f 0.346M-${y}-${foo:$i:1}.h5 -o md_out/ions/60A_293.15"
# #       $temp >> $file
#       $temp
# done

# done






# 5E21

# foo='abc'
# run='run2'

# for (( i=0; i<${#foo}; i++ )); do

# for x in {1..9}; do
#      y=`bc <<< "scale=1; $x/10"`
#       sbatch gpu.sh conduct.py -f NVT-0$y-${foo:$i:1}.h5 -o 5E21/$run -axis 1
# done

# # for x in {10..12}; do
# #      y=`bc <<< "scale=1; $x/10"`
# #       sbatch gpu.sh conduct.py -f NVT-$y-${foo:$i:1}.h5 -o 5E21/$run -axis 1
# # done

# # for x in {1..9}; do
# #      y=`bc <<< "scale=2; $x/100"`
# #       sbatch gpu.sh conduct.py -f NVT-0$y-${foo:$i:1}.h5 -o 5E21/$run -axis 1
# # done

# done

#----------------------------------------------------------------#


# ALIGN

# file=../md_out/water/ALIGN_$(date +"%b%m_%I_%M%p").txt
# foo='abc'

# mol=0

# for (( i=0; i<${#foo}; i++ )); do


# for x in {0..9}; do
#        x=$((x*2))
#      y=`bc <<< "scale=1; $x/10"`
#      temp="sbatch cpu-small.sh align.py -file 0M-0${y}-${foo:$i:1}.h5"
#      echo $temp >> $file
#      $temp
# done

# for x in {10..24}; do
#        x=$((x*2))
#      y=`bc <<< "scale=1; $x/10"`
#      temp="sbatch cpu-small.sh align.py -file 0M-${y}-${foo:$i:1}.h5"
#      echo $temp >> $file
#      $temp
# done

# for x in {1..10}; do
#     x=$((x*50))
#      y=`bc <<< "scale=1; $x/10"`
#      temp="sbatch cpu-small.sh align.py -file 0M-${y}-${foo:$i:1}.h5"
#      echo $temp >> $file
#      $temp
# done


# done





#----------------------------------------------------------------#
# LOADIN
# Run proteinbox simulations

# 5E21

# foo='abc'
# for (( i=0; i<${#foo}; i++ )); do

# for x in {1..9}; do
#      y=`bc <<< "scale=1; $x/10"`
#       sbatch gpu.sh loadin.py -ef 0$y -desc ${foo:$i:1} -path 5E21/irun1
# done

# # for x in {1..9}; do
# #     y=`bc <<< "scale=2; $x/100"`
# #      sbatch gpu.sh loadin.py -ef 0$y -desc ${foo:$i:1} -path 5E21/irun1
# # done

# # for x in {10..12}; do
# #     y=`bc <<< "scale=1; $x/10"`
# #      sbatch gpu.sh loadin.py -ef $y -desc ${foo:$i:1} -path 5E21/irun1
# # done

# done


# Run proteinbox simulations
# foo='abc'
# for (( i=0; i<${#foo}; i++ )); do

# for x in {1..9}; do
#     y=`bc <<< "scale=2; $x/100"`
#      sbatch gpu.sh loadin.py -ef 0$y -desc ${foo:$i:1} -path HEWLmd/irun2 -slant False
# done

# for x in {10..12}; do
#     y=`bc <<< "scale=1; $x/10"`
#      sbatch gpu.sh loadin.py -ef $y -desc ${foo:$i:1} -path HEWLmd/irun2 -slant False
# done

# done




#----------------------------------------------------------------#

# foo='abc'

# for x in {1..9}; do
# for (( i=0; i<${#foo}; i++ )); do
#     y=`bc <<< "scale=1; $x/10"`
#     sbatch cpu-small.sh conduct.py NVT_run-0.05.h5 0.05
# done
# done


