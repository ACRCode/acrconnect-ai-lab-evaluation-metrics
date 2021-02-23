import argparse
import sys
import os
import json
import traceback 

from evaluationFactory import EvaluationFactory

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AI Lab Evaluation Metrics')
    parser.add_argument("--dataset_file_path",nargs="?", default=None, help="string, the path to the ground truth json file", type=str)
    parser.add_argument("--output_file_path",nargs="?", default=None, help="string, the path to the prediction json file", type=str)
    parser.add_argument("--evaluation_file_path",nargs="?", default=None, help="string, the path to the resulting results for the evaluation", type=str)
    parser.add_argument("--threshold", nargs="?", default=0.5, help="float, the threshold of the evaluation for binary classification", type=float)
    parser.add_argument("--binary_maps", nargs="?", default=None, help="string, the serialized json object of the binary maps for evaluations", type=str)
    
    args=parser.parse_args()
    
    if(args.binary_maps != None):
        args.binary_maps = json.loads(args.binary_maps)

    try:
        print("Building evaluation with args: ", args)
        factory = EvaluationFactory(args)
        output = factory.Create()
        print("Evaluation complete")
        if args.evaluation_file_path is not None and len(args.evaluation_file_path) > 0:
            print("Writing results to output json....")
            with open(args.evaluation_file_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=4)
            print("Writing results to json completed....")
        else:
            print('OUTPUT', json.dumps(output, indent=4, sort_keys=True))
        
    except Exception as err:
        print(err, file=sys.stderr)
        traceback.print_exc() 
        sys.exit(1)
