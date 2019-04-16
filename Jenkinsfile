// Obtain files from source control system.
if (utils.scm_checkout()) return



// Define each build configuration, copying and overriding values as necessary.
bc0 = new BuildConfig()
bc0.nodetype = "linux"
bc0.name = "debug"
bc0.build_cmds = [
'export PATH="/var/jenkins_home/miniconda3/bin:$PATH"',
    "conda env update --file=environment.yml",
    "pip install codecov pytest-cov",
    "with_env -n pyrsa python setup.py install"]
bc0.test_cmds = [
    "with_env -n pyrsa pytest -s --junitxml=results.xml --cov=./pyrsa --cov-report xml",
    ]

// bc1 = utils.copy(bc0)
// bc1.build_cmds[0] = "conda install -q -y python=3.5"

// Iterate over configurations that define the (distibuted) build matrix.
// Spawn a host of the given nodetype for each combination and run in parallel.
utils.run([bc0])
