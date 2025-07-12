#!/bin/bash

# Output CSV header
echo "filename,ra,dec,PD,PD_err,PA,PA_err,MDP" > results.csv

# Loop through all IXPE event2 FITS files in current directory
for file in *_evt2_*.fits; do
    [ -e "$file" ] || continue

    echo "Processing $file..."

    # Use Python & Astropy to get RA and DEC
    read ra dec < <(
        python3 -c "
from astropy.io import fits
with fits.open('$file') as hdul:
    hdr = hdul[0].header
    print(hdr.get('RA_OBJ', 'nan'), hdr.get('DEC_OBJ', 'nan'))
"
    )

    # Run xpselect
    xpselect "$file" --ra "$ra" --dec "$dec" --rad 1.0

    # Construct output filenames
    base="${file%.fits}"
    select_file="${base}_select.fits"
    pcube_file="${base}_select_pcube.fits"

    # Run xpbin
    xpbin "$select_file" --algorithm PCUBE --irfname ixpe:obssim20240101:v13 --ebins 1 --emax 8.0 --emin 2.0

    # Extract polarization values
    PD=$(ftlist "$pcube_file"[1] R col=PD | awk 'NR==3 {print $1}')
    PD_ERR=$(ftlist "$pcube_file"[1] R col=PD_ERR | awk 'NR==3 {print $1}')
    PA=$(ftlist "$pcube_file"[1] R col=PA | awk 'NR==3 {print $1}')
    PA_ERR=$(ftlist "$pcube_file"[1] R col=PA_ERR | awk 'NR==3 {print $1}')
    MDP=$(ftlist "$pcube_file"[1] R col=MDP | awk 'NR==3 {print $1}')

    # Append to results.csv
    echo "$file,$ra,$dec,$PD,$PD_ERR,$PA,$PA_ERR,$MDP" >> results.csv
done

echo "✅ Done. Results saved to results.csv"

