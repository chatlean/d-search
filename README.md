# dChatLean
# Proof Search
The project focuses on generating mathematical proofs by employing two proof search algorithms. The proof search algorithms we propose are simple yet effective, based on the principles of Breadth-First Search (BFS) and Depth-First Search (DFS). 

We utilize chatGPT and Lean3 to support the mathematical proof. This initiative provides the means to explore the mathematical proofs and equips with the necessary resources to address complex mathematical challenges.

## Requirements
- 3.9 <= python <= 3.10
- Set the environment variables below:
    ```
    export CONTAINER="native"
    export GITHUB_ACCESS_TOKEN="[Your GitHub access token]"
    ```

### Installation
- Install the packages with the following command to run our project:
    ```
    pip install -r requirements.txt
    ```

## Project Structure
Below is an outline of the main directories and files included in this project:
- `datasets/`: : Contains the datasets used by the project.
    - `prompt_examples/` : Includes the examples used in prompt.
    - `small_minif2f/` : A smaller version of our dataset for quick tests. 
- `log/`: Stores log files for different search algorithms.
    - `dfs/`: Logs for the Depth-First Search algorithm.
- `results/`: Contains the output from the search algorithms.
  - `bfs/`: Results of a proof-generating with the BFS algorithm.
  - `dfs/`: Results of a proof-generating with the DFS algorithm.
- `scripts/`: Includes Python files to run for a proof-generating with BFS and DFS.

### BFS
`chatlean_bfs.py` is to search for a mathematical proofs using BFS. To run the code, use the following command:
```
python scripts/chatlean_bfs.py --API_key [OpenAI API key] --minif2f [Path for minif2f dataset] --model [Model name] --temperature [Temperature] --ex_data datasets/prompt_examples/examples.json --num_sample [Number of Samples] --result_fname [Name of result file]
```

### DFS
`chatlean_dfs.py` and `chatlean_dfs_badO.py` are to search for a mathematical proofs with DFS. To run this scripts, use the following command lines:
```
python scripts/chatlean_dfs.py --API_key [OpenAI API key] --minif2f [Path for minif2f dataset] --model [model name] --temperature [Temperature] --ex_data datasets/prompt_examples/examples.json --passn [Number of repetition for theorem] --result_fname [Name of result file] --ncpu [Number of CPU cores for parallel computing]

python scripts/chatlean_dfs_badO.py --API_key [OpenAI API key] --minif2f [Path for minif2f dataset] --model [model name] --temperature [Temperature] --ex_data datasets/prompt_examples/examples.json --passn [Number of repetition for theorem] --result_fname [Name of result file] --ncpu [Number of CPU cores for parallel computing]
```

## Citations
