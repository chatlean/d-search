# dChatLean
The project focuses on generating mathematical proofs by employing two proof search algorithms. The proof search algorithms we propose are simple yet effective, based on the principles of Breadth-First Search (BFS) and Depth-First Search (DFS). In this repository, we contain all codes for dChatLean and dChatLean+, which are based on DFS.

We utilize chatGPT and Lean3 to support the mathematical proof. This initiative provides the means to explore the mathematical proofs and equips with the necessary resources to address complex mathematical challenges.

## Requirements
- 3.9 <= python <= 3.10
- Set the environment variables below:
    ```
    export CONTAINER=native
    export GITHUB_ACCESS_TOKEN=[Your GitHub access token]
    ```

### Installation
- Install the packages with the following command to run our project:
    ```
    pip install -r requirements.txt
    ```

## Structure
Below is an outline of the main directories and files included in this project:
- `datasets/`: The directory for the datasets used in experiments.
    - `prompt_examples/`: Examples for a prompt. We contain a file, `examples.json`, used in our experiments.
    - `small_minif2f/`: A small part of MiniF2F for quick tests. 
- `log/`: The directory for log files for experiments. We contain our logs for dChatLean and dChatLean+.
- `results/`: The directory for the experiment results.
- `scripts/`: The directory for Python files to run dChatLean and dChatLean+.

### DFS
`chatlean_dfs.py` and `chatlean_dfs_badO.py` are to search for a mathematical proofs with DFS. To run this scripts, use the following command lines:
```
python scripts/chatlean_dfs.py --API_key [OpenAI API key] --minif2f [Path for minif2f dataset] --model [model name] --temperature [Temperature] --ex_data datasets/prompt_examples/examples.json --passn [Number of repetition for theorem] --result_fname [Name of result file] --ncpu [Number of CPU cores for parallel computing]

python scripts/chatlean_dfs_badO.py --API_key [OpenAI API key] --minif2f [Path for minif2f dataset] --model [model name] --temperature [Temperature] --ex_data datasets/prompt_examples/examples.json --passn [Number of repetition for theorem] --result_fname [Name of result file] --ncpu [Number of CPU cores for parallel computing]
```

## Citations
