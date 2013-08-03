import subprocess



try:
    print subprocess.check_output(["make", "clean"])
    print subprocess.check_output(["make", "all"])
    print subprocess.check_output(["make", "alla"])
except Exception, e:
    print "something failed: %s" % e

