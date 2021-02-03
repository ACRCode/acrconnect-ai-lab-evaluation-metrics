python src/main.py \
    --dataset_file_path=".\examples\breastDensity\dataset.json" \
    --output_file_path=".\examples\breastDensity\modelOutput.json" \
    --evaluation_file_path=".\examples\breastDensity\evaluation.json" \
    --binary_maps="{\"breast-density-classification\": {\"presentLabels\":[\"1\", \"2\"], \"absentLabels\":[\"3\", \"4\"]}}"
