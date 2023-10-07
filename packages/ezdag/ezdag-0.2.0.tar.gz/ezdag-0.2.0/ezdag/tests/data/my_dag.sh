# Job process_bins:00000
/path/to/process_bins 0 --verbose --bins 0 --bins 3 --bins 6 --input data.txt output_0.txt

# Job process_bins:00001
/path/to/process_bins 1 --verbose --bins 1 --bins 4 --bins 7 --input data.txt output_1.txt

# Job process_bins:00002
/path/to/process_bins 2 --verbose --bins 2 --bins 5 --bins 8 --input data.txt output_2.txt

# Job combine_bins:00000
/path/to/combine_bins --verbose output_0.txt output_1.txt output_2.txt combined.txt

