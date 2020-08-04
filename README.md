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


_Requirements_: java 12, maven

## Run experiments

Results in the paper can be reproduced by means of the jupyter notebooks in experiements
folder. For running them, start a jupyter server with the command below and then open the corresponding notebooks.

```
python -m jupyter notebook .
```



_Requirements_: python3 and packages in requirements.txt (pip install -r requirements.txt)


## Citation

```
@misc{zaffalon2020structural,
    title={Structural Causal Models Are (Solvable by) Credal Networks},
    author={Marco Zaffalon and Alessandro Antonucci and Rafael Caba\~{n}as},
    year={2020},
    eprint={2008.00463},
    archivePrefix={arXiv},
    primaryClass={cs.AI}
}


```