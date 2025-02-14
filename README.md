# dChatLean
The project focuses on generating mathematical proofs by employing our two proof search algorithms, b-search and d-search. The proof search algorithms we propose are simple yet effective, based on the principles of breadth-first search and depth-first search. 

In this repository, we contain all codes and some results for dChatLean and dChatLean+, which are based on d-search.

## Requirements
First of all, we utilize ChatGPT as a model and Lean 3 to support the mathematical proof. In our experiments, we used Lean version 3.42.1, the same version used in [miniF2F](https://github.com/openai/miniF2F).

To interact with Lean, we utilize [LeanDojo](https://github.com/lean-dojo/LeanDojo), which allows parallel implementation, easily checks time limits, and is well-organized.
Using LeanDojo requires several environment settings to facilitate the tracing and extraction of data.
We only document our specific settings; additional available settings can be found in the original LeanDojo repository.

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
We use LeanDojo to interact with Lean. Employing LeanDojo requires a data extraction process. For more information and a detailed example, refer to the [LeanDojo](https://github.com/lean-dojo/LeanDojo).

## Structure
Below is an outline of the main directories and files included in this project:
- `datasets/`: The directory for the datasets used in experiments.
    - `prompt_examples/`: Examples for a prompt. We contain a file, `examples.json`, used in our experiments.
    - `small_minif2f/`: A small part of MiniF2F for quick tests.
- `log/`: The directory for log files.
- `results/`: The directory for the experiment results.
    - `AMC12_2023/`: Our experiment results for the 2023 AMC12 problems, which we newly formalized.
    - `Llemma/`: Our experiment results using [Llemma](https://arxiv.org/abs/2310.10631) as the base model instead of ChatGPT, with miniF2F as the problem set.
    - `miniF2F/`: Our main results in the paper.
    - `ProofNet/`: Our experiment results for the [ProofNet](https://github.com/zhangir-azerbayev/ProofNet) dataset.
- `scripts/`: The directory for Python files to run dChatLean and dChatLean+.

### Run
`dchatlean.py` and `dchatlean_badO.py` are to search for a mathematical proof with d-search. To run these scripts, use the following command lines:
```
python scripts/dchatlean.py --API_key [OpenAI API key] --model [ChatGPT model name] --temperature [Temperature] --data_path [Directory for test dataset] --split [Name of json file for test] --ex_data [File path for example in prompt] --passn [Number of repetition for a theorem] --result_dir [Directory to save result] --result_fname [Name of result file] --ncpu [Number of CPU cores for parallel computing]

python scripts/dchatlean_badO.py --API_key [OpenAI API key] --model [ChatGPT model name] --temperature [Temperature] --data_path [Directory for test dataset] --split [Name of json file for test] --ex_data [File path for example in prompt] --passn [Number of repetition for a theorem] --result_dir [Directory to save result] --result_fname [Name of result file] --ncpu [Number of CPU cores for parallel computing]
```

For example :
```
python scripts/dchatlean_badO.py --API_key YOUR_API_KEY --model gpt-4o --temperature 1.4 --data_path datasets/small_minif2f/default --split test --ex_data datasets/prompt_examples/examples.json --passn 50 --result_dir results --result_fname small_minif2f_test --ncpu 1 1> log/small_test.out 2> log/small_test.err
```

## Results in Paper
Here, we present experimental results from our paper for d-search.
For a detailed analysis, please refer to our paper.

<details>
  <summary> Ablation study for the number of attempts </summary>
    
  |Model|Baseline|Temperature|Number of attempts|Pass rate
  |:---:|:---:|:---:|:---:|:---:
  |dChatLean|GPT-4 Turbo|0.7|<p>10 <p>50|<p>13.93 \% <p>20.90 \%
  |dChatLean|GPT-4 Turbo|1.4|<p>10 <p>50|<p>15.16 \% <p>23.77 \%
  
</details>

<details>
  <summary> Ablation study for the temperature </summary>
    
  |Model|Baseline|Number of attempts|Temperature|Pass rate
  |:---:|:---:|:---:|:---:|:---:
  |dChatLean|GPT-4|10|<p>0.7 <p>1.4|<p>14.75 \% <p>15.98 \%
  |dChatLean|GPT-4 Turbo|10|<p>0.7 <p>1.4|<p>13.93 \% <p>15.16 \%
  |dChatLean|GPT-4 Turbo|50|<p>0.7 <p>1.4|<p>20.90 \% <p>23.77 \%
  
</details>

<details>
  <summary> Ablation study for the feedback algorithm by Bad(O) </summary>
    
  |Model|Baseline|Temperature|Number of attempts|Pass rate
  |:---:|:---:|:---:|:---:|:---:
  |<p>dChatLean <p>dChatLean+|GPT-4 Turbo|1.4|10|<p>15.16 \% <p>18.85 \%
  |<p>dChatLean <p>dChatLean+|GPT-4 Turbo|1.4|50|<p>23.77 \% <p>25.00 \%
  
</details>

## Citations
