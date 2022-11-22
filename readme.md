# LineBOforNishinaExperiment


The repository is based on https://github.com/kirschnj/LineBO of the ICML 2019 Paper
"Adaptive and Safe Bayesian Optimization in High Dimensions via One-Dimensional Subspaces", but modified specifically with the aim to apply for the accelerator systems at Nishina Center.

The above paper can be found here: https://arxiv.org/abs/1902.03229

The code can be excecuted by the following procedure

1. Install a Python 3.7 environment
* conda create -n py37 python=3.7
* conda activate py37
2. Install the package with "pip install -e ."
3. pip install git+https://github.com/automl/HPOlib1.5
4. pip install git+https://github.com/befelix/SafeOpt.git

In case for newly set python3.7 environment, following error occurs
"AttributeError: 'EntryPoints' object has no attribute 'get'C"
Try installing older version of importlib-metadata
pip install importlib-metadata==4.13.0

If the system require numpy version greater than 1.20.0. specify `pip install numpy==1.20.0`.

To run the canonical problems, replace "{experiment_name}" in the instructions below by any of:

* camelback
* camelback_sub10
* hartmann6
* hartmann6_sub14
* gaussian10
* camelback_constraint
* hartmann6_constraint
* camelback_sub10_constraint

Instructions to run experiments and create plots:

1. febo create {user_specified_experiment_name} --config config/{experiment_name}.yaml
2. febo run {user_specified_experiment_name}
                (this will take a while, you can set the number of repetitions in the yaml file)
3. febo plot {user_specified_experiment_name} --plots febo.plots.InferenceRegret

Experimental results will be generated under `runs/{user_specified_experiment_name}`. 

# Run for Mocadi simulation
For trying out safety-aware LineBO, opt for the `gicosy_interface.yaml` as the template YAML file. 

The default system is composed of $X \in \mathbb{R}^{17}$ inputs, and transmission ratio 
$y=(\mathrm {Transmitted\ particles })/(\mathrm{Total \ particles})$, and 30+1 constraints (30 read from the output table, and one as the lower bound of the transmisstion ratio).
These values are computed or just fetched from the ouput result of Mocadi. 

```
$ cat gicosy/T_Cource_Transmission/MonteCarlo_Result__environment.txt
Dipole#0  in:     0,     0,     0,     0,     0
Dipole#0 out:     1,     1,     7,     2,    11
Dipole#1  in:     0,     0,     0,     0,     0
Dipole#1 out:     0,     0,     0,     0,     0
Dipole#2  in:     0,     0,     0,     0,     0
Dipole#2 out:     0,     0,     0,     0,     0
3.707068, 0.451586, 3.474535, 0.383571, 0.034785,  3.595134, 5.482656, 10000, 8219
```


# Objective Function
This template file specifies `febo.environment.benchmarks.functions.MocadiSimulation` as the benchmark environment to extract objective function. 
The implementation of this class is under `febo/environment/benchmarks/functions.py`, 

```
class MocadiSimulation(BenchmarkEnvironment):
    """
    Mocadi simulation interface.
    """
    def __init__(self, path=None):
        super().__init__(path)
        # self.config.dimension = 17 wrote in ymal
        ones = np.ones(self.config.dimension)
        self._domain = ContinuousDomain(-ones, ones)

        # determine x0 based on the initial value of BQ 
        self.emconfig = ElectroMagnetClass() 
        #self._x0 = 0.0*ones/np.sqrt(self.config.dimension) # initially all 0
        self._x0 = self.emconfig.getX0().flatten() # relative to the domain range
        self._x = self._x0
        self._max_value = 1.0
        # specify to the path where simulation located
        self.mocadi = MocadiInterface('__environment', 'gicosy/T_Cource_Transmission/', self.emconfig) # base is the repository's home directory

    def f(self, X):
        X = np.atleast_2d(X)
        self.mocadi.RunMocadi(X)
        # Y = 2*np.sum(np.square(X), axis=1)
        Y = self.mocadi.LoadMocadiResults() # Y \in [0,1]
        return Y
```

which reads out the numerical evaluation of the system via Mocadi simulation wrapper class under `gicosy/simulation_wrapper.py`.

The function `f(self, X)` is to be ***maximized*** in thie context, which is the transmission ratio of the beamline.

# Evaluation function implementation

Initial state value is normalized to be $x_i \in [-1,1] \ (i \in R)$

Constraints $g_i(x)$ will be described later in `simulation_wrapper.py`.


# Constraints and observable value implementation. 
Two major source codes are newly introduced to wrap the simulation under `gicosy/` directory.

* gicosy/simulation_wrapper.py 
* gicosy/ElectroMagnetClass.py 

For the future experimental implementation, these read out values must be hardcoded according to the system in its implementation.

The initial input value `x0` is normalized relative to the maximum plausible input setup $x_{max}$ and the minimum plausible input setup $x_{min}$.

## Constraints for the objective
Upper bound to the objective function is added as the constraints under 

## Explicit constraints

## User input deck

