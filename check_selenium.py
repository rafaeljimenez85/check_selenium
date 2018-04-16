#!/usr/bin/python
#
# check_selenium.py
# part of nagdog
#
# (c) copyright 2008,2009,2010 mm/mare-system.de
#     dogtown@mare-system.de
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#
# v 0.2.1 - AALPHAA - 2010-11-04
# 
# 

import os, posix, string, sys, time, getopt

# where the testcases are stored, must be python_exports from selenium ide 
test_dir="/srv/data/selenium_tests"

# defaults
warning_t="15"
critical_t="30"
test_count="none"
debug = "no"

return_status="UNKNOWN"
return_exit=3
return_text="no return (default)"
return_perfdata="none"

def check_selenium_help():
    print """

check_selenium 
    nagios_plugin to check selenium_tests and display results / perfdata
    
    USAGE
     check_selenium [otions]
     
    OPTIONS
      -s [scriptname] 
            test_script to execute
            must be located in $test_dir 
      -t [count] 
            number of test that must be executed; if number
            differs, status==WARNING
            default: off 
      -w [seconds]
            threshold in seconds for the test to pass
            to change status to WARNING
            default: 15 sek
      -c [seconds] 
            threshold in seconds for the test to pass
            to change status to CRITICAL
            default: 30sek
      -d    turn debug on
      
    
    """

def return_result():
    print "SELENIUM %s %s | %s " % (return_status, return_text, return_perfdata)
    sys.exit(return_exit)

def print_debug(debug_output):
    if debug == "yes":
        print "d:: %s " % debug_output
    return()
        

try:
    opts, args = getopt.getopt(sys.argv[1:], "s:c:w:t:hdz", 
        ["help", "script", "debug" ])
except getopt.GetoptError, err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    check_selenium_help()
    sys.exit(2)


for o, a in opts:
    #print "o :: " + o + "   <-->  a: " + a
    if o in ("-s", "--script"):
        test_script = a
        test_script_path = "%s/%s" % (test_dir, test_script)
    elif o in ("-h", "--help"):
        check_selenium_help()
        sys.exit()
        

    elif o in ("-w", "--warning"):
        warning_t = a
    elif o in ("-c", "--critical"):
        critical_t = a
        
    elif o == "-t":
       test_count = a
    
    elif o == "-d":
       debug = "yes"
    
    else:
        check_selenium_help()
        sys.exit(2)        

if len(sys.argv) == 1:
    check_selenium_help()
    sys.exit(0)

if not test_script:
    return_text = "no testscript given"
    return_status="CRITICAL"
    return_exit = 2
    return_result()

if not os.path.exists(test_script_path):
    return_text = "no testscript found in %s " % test_script_path
    return_status="CRITICAL"
    return_exit = 2
    return_result()

print_debug("excuting %s in %s " % (test_script, test_dir))

test_output = os.popen("cd %s && python %s 2>&1 " % (test_dir, test_script)).readlines()

print_debug(test_output)

test_out_compiled = string.join(test_output, "")


# return if test failed 
if test_out_compiled.find("FAIL") > -1:
    return_exit = 2
    return_status == "CRITICAL"
    return_text = "FAIL: not all tests passed -> %s " % (test_script) 
    return_perfdata = test_out_compiled
    return_result()
    sys.exit(2)

out_string = string.strip(test_output[2])
out_status = string.strip(test_output[4])

out_time = float((string.split(out_string, "test in")[1]).replace("s", ""))

print_debug(out_time)
return_perfdata = "checktime=%ss" % out_time

if out_status == "OK":
    try:
        wt = float(warning_t)
    except:
        return_text = "Warning-Time (-w) must be a number"
        return_result()

    try:
        ct = float(critical_t)
    except:
        return_text = "Critical-Time (-c) must be a number"
        return_result()

    if out_time > ct:
        return_status = "CRTITICAL"
        return_exit = 2
        return_text = "all tests passed, but time exceeds > %s s (%s)" % (ct,return_perfdata)
        return_result()
    elif out_time > wt:
        return_status = "WARNING"
        return_exit = 1
        return_text = "all tests passed, but time exceeds > %s s (%s)" % (wt,return_perfdata)
        return_result()

         
    return_exit = 0
    return_status = "OK"
    return_text = "all tests passed from %s (%s) " % (test_script, return_perfdata)
else:
    return_exit = 2
    return_status == "CRITICAL"
    return_text = "not all tests passed :: %s -> %s " % (out_status, test_script) 

return_result()
