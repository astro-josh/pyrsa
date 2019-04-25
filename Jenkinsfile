

// Obtain files from source control system.
if (utils.scm_checkout()) return
utils.installConda()


// Define each build configuration, copying and overriding values as necessary.
bc0 = new BuildConfig()
bc0.nodetype = "master"
bc0.name = "debug"
bc0.build_cmds = []
bc0.test_cmds = ["ls"]


utils.run([bc0])
