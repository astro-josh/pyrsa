
// Obtain files from source control system.
if (utils.scm_checkout()) return



// Define each build configuration, copying and overriding values as necessary.
bc0 = new BuildConfig()
bc0.nodetype = "linux-stable"
bc0.name = "debug"
bc0.build_cmds = [
    "conda env update --file=environment.yml",
    "pip install codecov pytest-cov",
    "with_env -n jwql python setup.py install"]
bc0.test_cmds = [
    "with_env -n jwql pytest -s --junitxml=results.xml --cov=./jwql/ --cov-report xml",
    "codecov --token=${codecov_token}"]


utils.run([bc0])
