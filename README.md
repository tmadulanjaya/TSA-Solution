# Travelling Salesman Problem using Genetic Algorithm

---

## 📁 Project Structure

| File           | Description                                         |
| -------------- | --------------------------------------------------- |
| `main.py`      | Entry point of the program                          |
| `algorithm.py` | Core GA loop, 2-opt local search, and random search |
| `operators.py` | Genetic operators (selection, crossover, mutation)  |
| `analyze.py`   | Parameter tuning and statistical evaluation         |
| `visual.py`    | Visualization of convergence and tours              |
| `dataload.py`  | Loads the CSV distance matrix                       |
| `utils.py`     | Helper functions (saving results, summaries)        |

---

## ⚙️ Installation

Make sure you have Python 3.9 or later installed.

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

Run with default settings:

```bash
python main.py
```

Run with custom parameters:

```bash
python main.py --pop 400 --gens 2000 --mut 0.03 --elite 10 --tourn 5 --patience 300 --runs 10
```

---

## 🔧 Parameters

| Argument     | Default | Description                             |
| ------------ | ------- | --------------------------------------- |
| `--file`     | auto    | Path to CSV distance matrix             |
| `--pop`      | 400     | Population size                         |
| `--gens`     | 2000    | Maximum generations                     |
| `--mut`      | 0.03    | Mutation rate (inversion)               |
| `--elite`    | 10      | Number of elite individuals             |
| `--tourn`    | 5       | Tournament size                         |
| `--patience` | 300     | Early stopping threshold                |
| `--runs`     | 10      | Number of runs for statistical analysis |

---

## 🧠 Methodology

### Representation

Each solution is represented as a permutation of city indices, ensuring all cities are visited exactly once.

### Fitness Function

The objective is to minimize the total tour distance, including the return to the starting city.

### Selection

Tournament selection is used by choosing the best individual from a random subset of the population.

### Crossover

Order Crossover (OX) is applied to preserve valid routes while combining parent solutions.

### Mutation

Two mutation strategies are used:

* Swap mutation (rate = 0.01)
* Inversion mutation (rate = 0.03)

### Elitism

Top-performing individuals are carried forward unchanged to the next generation.

### Local Search (2-opt)

A 2-opt optimization is applied after the GA to further improve the final route.

### Early Stopping

The algorithm stops if no improvement is observed for a defined number of generations.

---

## 📥 Input Format

CSV distance matrix with city names:

```
,CityA,CityB,CityC
CityA,0,120,340
CityB,120,0,210
CityC,340,210,0
```

---

## 📤 Output

All results are saved in the `results/` directory:

* `solution.txt` – Best route and distance
* `convergence.png` – Best vs average fitness per generation
* `best_tour.png` – Visualized tour (2D projection)
* `parameter_tuning.png` – Parameter comparison results
* `multi_run_stats.png` – Statistical analysis across runs
* `multi_run_stats.txt` – Mean, standard deviation, confidence intervals
* `comparison_random.txt` – GA vs random search comparison

---

## 📊 Complexity

* Genetic Algorithm: **O(population × generations × n)**
* 2-opt Local Search: **O(n²)** per iteration

---

## ⚠️ Limitations

* Does not guarantee a globally optimal solution
* Performance depends on parameter tuning
* 2-opt can be computationally expensive for large datasets

---

## 📌 Summary

This project demonstrates how Genetic Algorithms can effectively approximate solutions to NP-hard problems like the Travelling Salesman Problem, especially when combined with local search techniques and statistical evaluation.
