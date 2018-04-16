# check_selenium
## Requirements

make sure to have a selenium-server.jar running an accessible from your testscripts (server/port etc), for setting up headless selenium-server see below create an nagios-accessible directory (check_dir) for your sel_check_scripts.py get selenium-python-clientdrivers (see seleniumhq for an actual version place `selenium*.py` and `test_*.py` from  python-clientdrivers into $check_dir create some tests from Selenium IDE, export Test-cases as python_tests upload your sel_check_scripts to $check_dir copy the nagios_plugin check_selenium.py to your $USER1$ / nagios_plugins_dir run some tests as user nagios create a check_command and service_definition (see below)

## Bugs / Addidtional Notes
    
Please note, this plugin was created for a customer and works superb in our environment (test-cases, not suites, python-checks, firefox) if you have commnets/suggestions or find bugs please report them to dogtown@mare-system.de

## Sample nagios_command and service_def

```
define command{
    command_name    check_selenium
    command_line    $USER1$/check_selenium.py  -s $ARG1$ -w $ARG2$  -c $ARG3$ 
    }
```
```
define  service {
        host_name               check_host
        service_description     check_selenium
        check_command           check_selenium!check_script!20!33
        use                     custom-service

}
```
    
    

## Selenium-Server headless
+ install java aptitude install sun-java6-bin  sun-java6-jre    
+ install a simple windowmanager aptitude install gdm icewm-lite 
+ install firefox
+ install xvfb aptitude install xfvb
+ add a xfvb_display to some startup-script Xvfb :99 -ac -noreset &
+ execute selenium-server with the correct display export DISPLAY=:99 && java -jar /path/to/selenium-server-1.0.1/selenium-server.jar &
+ check your tests now
