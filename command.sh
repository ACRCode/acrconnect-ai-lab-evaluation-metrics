
MODULE="BreastDensity"

python src/main.py \
    --dataset_file_path="C:\Users\ramaya\Projects\acrconnect-ai-lab-evaluation-metrics\ExampleJsons\\$MODULE\dataset.json" \
    --output_file_path="C:\Users\ramaya\Projects\acrconnect-ai-lab-evaluation-metrics\ExampleJsons\\$MODULE\modelOutput.json" \
    --evaluation_file_path="C:\Users\ramaya\Projects\acrconnect-ai-lab-evaluation-metrics\bin\\$MODULE.json" \
    --binary_maps="{\"breast-density-classification\": {\"presentLabels\":[\"1\", \"2\"], \"absentLabels\":[\"3\", \"4\"]}}"
