from subprocess import check_call

def test_run_unit_tests_in_vagrant():
    '''This just runs the unit-tests on-box'''
    check_call(['vagrant', 'ssh', '-c', 'python /home/weather/opt/current/weather/manage.py test'])
