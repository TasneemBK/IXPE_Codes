#!/bin/bash

# === CONFIGURATION ===
OUTPUT_CSV="net_count_rates_2-4keV.csv"
XSPEC_SCRIPT="temp_xspec_commands.xcm"
TEMP_OUTPUT="xspec_temp_output.txt"

# Response files (modify these paths if needed)
RMF_FILE="/home/seps/anaconda3/envs/xspec_pyenv/lib/python3.10/site-packages/ixpeobssim/caldb/ixpe/gpd/cpf/rmf/ixpe_d3_obssim20240101_v013.rmf"
ARF_FILE="/home/seps/anaconda3/envs/xspec_pyenv/lib/python3.10/site-packages/ixpeobssim/caldb/ixpe/gpd/cpf/arf/ixpe_d3_obssim20240101_v013.arf"

# === CREATE CSV HEADER ===
echo "PHA_Filename,Net_Count_Rate_4-8keV(cts/s),Uncertainty,Full_Range_Rate(cts/s),Full_Range_Uncertainty,Ignored_Channels" > "$OUTPUT_CSV"

# === PROCESS EACH PHA FILE ===
for pha_file in *.pha; do
    echo "Processing $pha_file..."
    
    # Create XSPEC commands
    cat > "$XSPEC_SCRIPT" <<EOF
data $pha_file
response $RMF_FILE
arf $ARF_FILE
setplot energy
ignore **-2.0 4.0-**
show rates
exit
EOF

    # Run XSPEC
    xspec - "$XSPEC_SCRIPT" > "$TEMP_OUTPUT" 2>&1

    # Extract full range rate (before filtering)
    full_rate_line=$(grep "Net count rate (cts/s) for Spectrum:1" "$TEMP_OUTPUT" | head -n 1)
    full_rate=$(echo "$full_rate_line" | awk '{print $(NF-2)}')
    full_error=$(echo "$full_rate_line" | awk '{print $NF}')

    # Extract 4-8 keV rate
    filtered_rate_line=$(grep "Net count rate (cts/s) for Spectrum:1" "$TEMP_OUTPUT" | tail -n 1)
    filtered_rate=$(echo "$filtered_rate_line" | awk '{print $(NF-2)}')
    filtered_error=$(echo "$filtered_rate_line" | awk '{print $NF}')

    # Get ignored channels info
    ignored_info=$(grep "channels.*ignored in spectrum" "$TEMP_OUTPUT" | tr -d '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

    # Write to CSV
    echo "\"$pha_file\",$filtered_rate,$filtered_error,$full_rate,$full_error,\"$ignored_info\"" >> "$OUTPUT_CSV"

    echo "  -> 4-8 keV rate: $filtered_rate ± $filtered_error cts/s"
done

# === CLEAN UP ===
rm -f "$XSPEC_SCRIPT" "$TEMP_OUTPUT"

echo "Processing complete. Results saved to $OUTPUT_CSV"can