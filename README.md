# dChatLean
The project focuses on generating mathematical proofs by employing our two proof search algorithms, b-search and d-search. The proof search algorithms we propose are simple yet effective, based on the principles of breadth-first search and depth-first search. 

In this repository, we contain all codes and some results for dChatLean and dChatLean+, which are based on d-search.

## Requirements
First of all, we utilize ChatGPT and Lean 3 to support the mathematical proof.
To interact with Lean, we utilize LeanDojo (https://github.com/lean-dojo/LeanDojo), which allows parallel implementation, easily checks time limits, and is well-organized.
Using LeanDojo requires several environment settings to facilitate the tracing and extraction of data.
We only document our specific settings; additional settings can be confirmed in the original LeanDojo repository.

- 3.9 <= python <= 3.10
- Set the environment variables below:
    ```
    export CONTAINER=native
    export GITHUB_ACCESS_TOKEN=[Your GitHub access token]
    export CACHE_DIR=[Directory for cache files]
    ```

### Installation
- Install the packages with the following command to run our project:
    ```
    pip install -r requirements.txt
    ```
    
### Data Preparation
TODO

## Structure
Below is an outline of the main directories and files included in this project:
- `datasets/`: The directory for the datasets used in experiments.
    - `prompt_examples/`: Examples for a prompt. We contain a file, `examples.json`, used in our experiments.
    - `small_minif2f/`: A small part of MiniF2F for quick tests. 
- `log/`: The directory for log files for experiments. We contain our logs for dChatLean and dChatLean+.
- `results/`: The directory for the experiment results.
- `scripts/`: The directory for Python files to run dChatLean and dChatLean+.

### Run
`dchatlean.py` and `dchatlean_badO.py` are to search for a mathematical proofs with DFS. To run this scripts, use the following command lines:
```
python scripts/dchatlean.py --API_key [OpenAI API key] --minif2f [Path for minif2f dataset] --model [model name] --temperature [Temperature] --ex_data datasets/prompt_examples/examples.json --passn [Number of repetition for theorem] --result_fname [Name of result file] --ncpu [Number of CPU cores for parallel computing]

python scripts/dchatlean_badO.py --API_key [OpenAI API key] --minif2f [Path for minif2f dataset] --model [model name] --temperature [Temperature] --ex_data datasets/prompt_examples/examples.json --passn [Number of repetition for theorem] --result_fname [Name of result file] --ncpu [Number of CPU cores for parallel computing]
```

For example :
```
python scripts/dchatlean_badO.py --API_key YOUR_API_KEY --minif2f datasets/small_minif2f/default --model gpt-4o --temperature 1.4 --ex_data datasets/prompt_examples/examples.json --passn 50 --result_fname small_minif2f_test --ncpu 1 1> log/small_test.out 2> log/small_test.err
```

## Citations
