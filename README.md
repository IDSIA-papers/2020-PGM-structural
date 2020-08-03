# Structural Causal Models Are (Solvable by) Credal Networks

Here we provide the relevant code for the manuscript entitled 
"Structural Causal Models Are (Solvable by) Credal Networks" and accepted in 
the PGM 2020. The code is organised as follows.

- [./examples](examples) contains java files with the examples
shown in the paper.

- [./experiments](experiments) contains the jupyter notebooks for reproducing
the numerical tests given.


## Run code examples

First, run the following  command in a terminal:

```bash
mvn clean package
```

This should create the file target/experiments.jar containing all the dependencies.
Then for running any of the examples, let's say ./examples/Example9.java, run:

```
java -cp target/experiments.jar ./examples/Example9.java
```


## Run experiments


python -m jupyter notebook .

## Requirements