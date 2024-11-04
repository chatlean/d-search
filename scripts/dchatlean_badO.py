import json
import time
import openai
import argparse

import ray
from ray.util.actor_pool import ActorPool
from loguru import logger

from lean_dojo import *
import utils

#======================================================================================================================================
parser = argparse.ArgumentParser(description='Solve mathematical problems in Lean by ChatGPT with d-search and Bad(O) feedback algorithm')
parser.add_argument('--API_key', default=None, help='Openai API key')
parser.add_argument('--model', default='gpt-4', help='GPT model version')
parser.add_argument('--temperature', default=0, type=float, help='Model Temperature')
parser.add_argument('--req_try', default=10, type=int, help='Number of retry for request of chatgpt')
parser.add_argument('--req_to', default=60, type=int, help='Time out for request of chatgpt')
parser.add_argument('--sleep_time', default=90, type=int, help='Time for intermediate sleep')

parser.add_argument('--data_path', default=None, help='Path for dataset')
parser.add_argument('--split', default='test', help='Name of test JSON file')
parser.add_argument('--ex_data', default=None, help='File path for example in prompt')

parser.add_argument('--file_path', default=None, help='File path containing theorem')
parser.add_argument('--full_name', default=None, help='Full name of theorem')
parser.add_argument('--name_filter', default=None, help='Name for filtering theorem')
parser.add_argument('--num_theorems', default=None, type=int, help='The number of theorems to load')
parser.add_argument('--timeout', default=600, type=int, help='Timeout for proof search')
parser.add_argument('--passn', default=10, type=int, help='Number of thoerem proving trial')

parser.add_argument('--result_dir', default="results/dfs", help='Directory for searching result')
parser.add_argument('--result_fname', default='result_dchatlean_badO', help='Name of result file')
parser.add_argument('--print_iter', default=10, type=int, help='Iteration number for print')
parser.add_argument('--ncpu', default=1, type=int, help='Number of CPU for parallel computing')

args = parser.parse_args()
logger.info(args)

#======================================================================================================================================
def preparation(args):

    examples = []
    with open(args.ex_data, 'r', encoding="utf-8") as f:
        for line in f:
            examples.append(json.loads(line))
        
    msg_dict = {}
    msg_dict['sys_message'] = 'You are an expert in Lean3 theorem prover.'
    msg_dict['prompt'] = """Make a proof statement in Lean3 to prove theorem using the following guidelines:

- Generate only the single line of proof that immediately follows.
- Do not use `sorry`.
        
Here are some examples you may refer to:
    
=========
    
"""
    
    for ex in examples:
        msg_dict['prompt'] += """Lean3 tactic state : 
{}
    
Next tactic:

%%%%%
{}
%%%%%

=========

""".format(ex['statement'], ex['tactic'])

    repo, theorems, positions = utils._get_theorems(args.data_path, args.split, args.file_path, args.full_name, args.name_filter, args.num_theorems)
    logger.info('The repository to test : {}'.format(repo))
    
    return msg_dict, repo, theorems, positions

#======================================================================================================================================
# TODO: check timeout, all_path and break check
@ray.remote
class psearch():
    def __init__(self, args):
        openai.api_key = args.API_key
        
    def run(self, args, theorem, msg_dict):

        status = 'Init'
        proving_try = 0
        tot_req_no = 0
        badO = []
        all_path = []
        for j in range(args.passn):
            proving_try += 1
            logger.info('For thm {} : {} proving try'.format(theorem.full_name, proving_try))
            try:
                with Dojo(theorem, hard_timeout=60 + args.timeout) as (dojo, init_state):
                    start_time = time.monotonic()   
                    state = init_state

                    proof = []
                    while True:
                        tot_req_no += 1
                        chat_res = self.generate(args, state, msg_dict, badO)
                        proof.append(chat_res)

                        next_state = dojo.run_tac(state, chat_res)

                        if isinstance(next_state, ProofFinished):
                            logger.info('Theorem is proved')
                            status = 'Proved'
                            break
                        elif isinstance(next_state, LeanError):
                            logger.info('Error in Lean is raised')
                            status = 'Failed'
                            break
                        elif isinstance(next_state, TimeoutError):
                            logger.info('Timed out')
                            status = 'TimeOut'
                            break
                        elif isinstance(next_state, ProofGivenUp): 
                            logger.info('Proving is given up')
                            status = 'GiveUp'
                            break
                        else:
                            state = next_state
                            status = 'Open'

                    searching_time = time.monotonic() - start_time      
            except DojoHardTimeoutError:
                if proving_try == args.passn:
                    status = 'HardTimeOut'
                    break
                else:
                    pass
            except DojoCrashError:
                if proving_try == args.passn:
                    status = 'DojoCrashError'
                    break
                else:
                    pass
                
            if status == 'Proved':
                all_path.append({'status':status, 'path': proof})
                logger.info(f"all_path: 'status':{status}, 'path': {proof}")
                break
            else:
                badO.append({'state':state, 'failed_tac':proof[-1]})
                all_path.append({'status':status, 'path': proof})
                logger.info(f"all_path: 'status':{status}, 'path': {proof}")
        if status in ['HardTimeOut', 'DojoCrashError']:
            all_path.append({'status':status, 'path': proof})
            logger.info(f"all_path: 'status':{status}, 'path': {proof}")

        return theorem, init_state.pp, status, proof, searching_time, proving_try, tot_req_no, all_path
        
    def generate(self, args, state, msg_dict, badO):
    
        tac_for_fail = []
        for case in badO:
            if case['state'] == state:
                tac_for_fail.append(case['failed_tac'])
        
        if len(tac_for_fail) > 0:
            full_message = msg_dict['prompt'] + """Then the next line is what we need to prove:
        
Lean3 tactic state : 
{}

When you tried to make tactic before, you made like these:""".format(state.pp)
            for k in range(len(tac_for_fail)):
                full_message += """
%%%%%
{}
%%%%%
""".format(tac_for_fail[k])

            full_message += """
But these failed, so Make something else.

Next tactic:

"""
        else:
            full_message = msg_dict['prompt'] + """Then the next line is what we need to prove:
        
Lean3 tactic state : 
{}

Next tactic:

""".format(state.pp)

        message = [
            {'role': 'system', 'content': msg_dict['sys_message']},
            {'role': 'user', 'content': full_message}
            ]

        retries = args.req_try
        while retries > 0:
            try:
                response = openai.ChatCompletion.create(
                            model=args.model,
                            messages=message,
                            temperature=args.temperature,
                            request_timeout=args.req_to
                        )
                res = response["choices"][0]["message"]["content"]
                out_tac = res[res.find('%%%%%')+6 : res.find('%%%%%', res.find('%%%%%')+1)-1]
                return out_tac
            except Exception as e:    
                if e: 
                    logger.info(e)   
                    logger.info('Timeout error, retrying...')    
                    retries -= 1    
                    time.sleep(args.sleep_time)    
                else:    
                    raise e

#======================================================================================================================================

ray.init(num_cpus = args.ncpu)
msg_dict, repo, theorems, positions = preparation(args) 

search_obj = [psearch.remote(args) for _ in range(args.ncpu)]
logger.info(len(search_obj))
pool = ActorPool(search_obj)

msg_dict_lst = [msg_dict]*len(theorems)
unordered_results = list(pool.map_unordered(
        lambda p, x: p.run.remote(args, x[0], x[1]),            
        zip(theorems, msg_dict_lst)))
    
results = {}
with open('/'.join([args.result_dir, args.result_fname + '_pass{}rate.jsonl'.format(args.passn)]), 'w') as h:
    for i in range(len(theorems)):
        results['repo'] = '/'.join([repo.url, repo.commit])
        results['theorem_path'] = unordered_results[i][0].file_path.__str__()
        results['theorem_name'] = unordered_results[i][0].full_name
        results['init_state'] = unordered_results[i][1]
        results['status'] = unordered_results[i][2]
        results['proof'] = unordered_results[i][3]
        results['searching_time'] = unordered_results[i][4]
        results['proving_try_num'] = unordered_results[i][5]
        results['total_req_num'] = unordered_results[i][6]
        results['all_path'] = unordered_results[i][7]
        json.dump(results, h)
        h.write('\n')
        
logger.info('Result file is saved')
    
logger.info('Test over')
    