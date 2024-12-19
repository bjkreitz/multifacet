#!/bin/bash -e


#=====================================================================================
# Need to have UQTK_INS defined and bin added to the path.
export UQTK_INS=/Users/bjkreitz/work/UQTk-software/installdir
export PATH=${UQTK_INS}/bin:$PATH
#=====================================================================================

# Script location
export UQPC=${UQTK_INS}/examples/uqpc


# Use all inputs as training, and no validation
# cp Input.txt ptrain.dat
# #cp output_CH4.txt ytrain.dat # Or better work with the logarithms
# awk '{print log($1), log($2), log($3)}' output_CH4.txt > ytrain.dat

head -n16000 input_nodiff.txt > ptrain.dat
tail -n1146 input_nodiff.txt > pval.dat
awk 'NR<=16000{print log($1)}' output_temp_co_max_nodiff.txt > ytrain.dat
awk 'NR>16000{print log($1)}' output_temp_co_max_nodiff.txt > yval.dat


# Scale the inputs
${UQPC}/scale.x ptrain.dat from parameter_range_nodiff.txt qtrain.dat
${UQPC}/scale.x pval.dat from parameter_range_nodiff.txt qval.dat

# Get the number of training samples and validation samples
NSAM=`echo | awk 'END{print NR}' ptrain.dat`
NVAL=`echo | awk 'END{print NR}' pval.dat`


# Build surrogates
${UQPC}/uq_pc.py -r offline_post -p parameter_range_nodiff.txt -m bcs -s rand -n $NSAM -v $NVAL -t 3 -e 1.e-7


# Plot model-vs-surrogate
${UQPC}/plot.py dm training validation
# Plot total sensitivities
cp parameter_names_nodiff.txt pnames.txt
${UQPC}/plot.py sens total

# Enjoy the .eps files!

