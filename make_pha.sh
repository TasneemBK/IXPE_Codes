#!/bin/bash

# === CONFIGURATION ===
INPUT_DIR="/home/seps/Downloads/heasoft/data"    # <-- CHANGE THIS
IRF="ixpe:obssim20240101:v13"
EMIN=2.0
EMAX=8.0
EBINS=1
OUTPUT_CSV="net_count_rates.csv"

# === CSV HEADER ===
echo "Filename,PHA_File,Net_Count_Rate_cts_per_s" > "$OUTPUT_CSV"

# === LOOP OVER SELECT FILES ===
for file in "$INPUT_DIR"/*_select.fits; do
    full_base=$(basename "$file" .fits)                  # e.g., obs001_select
    base=${full_base%_select}                            # strip "_select" → obs001
    original_output="${full_base}_pha1.fits"             # xpbin output → obs001_select_pha1.fits
    renamed_output="${base}.pha"                         # desired output → obs001.pha

    echo "Processing $file → $renamed_output"

    # Step 1: Run xpbin (default output name will be auto-generated)
    xpbin "$file" \
        --algorithm PHA1 \
        --irfname "$IRF" \
        --emin "$EMIN" \
        --emax "$EMAX" \
        --ebins "$EBINS" \
        

    # Step 2: Rename xpbin output to .pha
    if [[ -f "$original_output" ]]; then
        mv "$original_output" "$renamed_output"
    else
        echo "❌ Error: Expected output file $original_output not found"
        continue
    fi

    # Step 3: Extract COUNTS and EXPOSURE using ftlist
    counts=$(ftlist "$renamed_output"[1] X columns=RATE rows=1 | awk '/RATE/ {getline; print $1}')
   
    # Step 4: Compute net count rate
    
    net_rate=$(echo "$counts " | bc -l)
    printf "%s,%s,%.5e\n" "$file" "$renamed_output" "$net_rate" >> "$OUTPUT_CSV"
    
done

echo "✅ All done! Results saved to $OUTPUT_CSV"

