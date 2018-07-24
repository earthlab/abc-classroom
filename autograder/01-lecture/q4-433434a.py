# Test Suite for Plot 1
# currently i want more verbose but also cleaner feedback.
# note that above i commented out the legend. and the legend tests thus failed.
# i'd like a very user friendly feedback block with the tests that passed vs failed.
# below is ugly and scary but it does work!

# this test has to be private as it depends on code from `earthanalytics`
# which is a private package
from earthanalytics.hw4_tests import homework4_tests
hw4t = homework4_tests()
results = unittest.TextTestRunner().run(hw4t.p1_tests(q4_ax1))
