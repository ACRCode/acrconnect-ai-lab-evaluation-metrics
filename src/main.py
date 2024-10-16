import argparse
import sys
import os
import json
import traceback 

from evaluationFactory import EvaluationFactory

def securePath(path):
    """
    secures paths for path transversal vulnerabilities. Throws security exception if path is insecure
    """
    examplesFolderPath = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../examples')
    aiLabFolderPath = '/volumes/acrconnect-ai-lab-service'

    if ".." in path:
        raise Exception('Security Error: Invalid path: ' + realPath + '. File paths must not have back tracking dots in them')

    #on windows machines we do not have a reliable way of knowing where connect will be installed as we can't control the path through a mount 
    if os.name == 'nt':
        return

    realPath = os.path.realpath(path)
    if not realPath.startswith(examplesFolderPath) and not realPath.startswith(aiLabFolderPath):
        raise Exception('Security Error: Invalid path: ' + realPath + '. Filepaths must reside within the examples folder if run locally or within the /app/Data folder if run from AI Lab')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AI Lab Evaluation Metrics')
    parser.add_argument("--dataset_file_path",nargs="?", default=None, help="string, the path to the ground truth json file", type=str)
    parser.add_argument("--output_file_path",nargs="?", default=None, help="string, the path to the prediction json file", type=str)
    parser.add_argument("--evaluation_file_path",nargs="?", default=None, help="string, the path to the resulting results for the evaluation", type=str)
    parser.add_argument("--threshold", nargs="?", default=0.5, help="float, the threshold of the evaluation for binary classification", type=float)
    parser.add_argument("--binary_maps", nargs="?", default=None, help="string, the serialized json object of the binary maps for evaluations", type=str)
    
    parser.add_argument('--cache', dest='use_cache', action='store_true')
    parser.add_argument('--no_cache', dest='use_cache', action='store_false')
    parser.set_defaults(use_cache=True)
    
    args=parser.parse_args()
    #path transversal mitigation
    securePath(args.dataset_file_path)
    securePath(args.output_file_path)
    securePath(args.evaluation_file_path)
    
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

