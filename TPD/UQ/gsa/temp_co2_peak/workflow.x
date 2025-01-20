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

head -n17476 input.txt > ptrain.dat
tail -n1941 input.txt > pval.dat
awk 'NR<=17476{print log($1)}' output_temp_co2_max.txt > ytrain.dat
awk 'NR>17476{print log($1)}' output_temp_co2_max.txt > yval.dat


# Scale the inputs
${UQPC}/scale.x ptrain.dat from parameter_range.txt qtrain.dat
${UQPC}/scale.x pval.dat from parameter_range.txt qval.dat

# Get the number of training samples and validation samples
NSAM=`echo | awk 'END{print NR}' ptrain.dat`
NVAL=`echo | awk 'END{print NR}' pval.dat`


# Build surrogates
${UQPC}/uq_pc.py -r offline_post -p parameter_range.txt -m bcs -s rand -n $NSAM -v $NVAL -t 3 -e 1.e-7


# Plot model-vs-surrogate
${UQPC}/plot.py dm training validation
# Plot total sensitivities
cp parameter_names.txt pnames.txt
${UQPC}/plot.py sens total

# Enjoy the .eps files!

