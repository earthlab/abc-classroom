import doctest
import inspect
import io
import json
import glob
import os
from contextlib import redirect_stderr, redirect_stdout
from jinja2 import Template
from textwrap import dedent

from .notebook import execute_notebook, _global_anywhere
from .utils import hide_outputs
from pygments import highlight
from pygments.lexers import PythonConsoleLexer
from pygments.formatters import HtmlFormatter


def run_doctest(name, doctest_string, global_environment):
    """
    Run a single test with given global_environment.
    Returns (True, '') if the doctest passes.
    Returns (False, failure_message) if the doctest fails.
    """
    examples = doctest.DocTestParser().parse(
        doctest_string,
        name
    )
    test = doctest.DocTest(
        [e for e in examples if isinstance(e, doctest.Example)],
        global_environment,
        name,
        None,
        None,
        doctest_string
    )

    doctestrunner = doctest.DocTestRunner(verbose=True)

    runresults = io.StringIO()
    with redirect_stdout(runresults), redirect_stderr(runresults), hide_outputs():
        doctestrunner.run(test, clear_globs=False)
    with open('/dev/null', 'w') as f, redirect_stderr(f), redirect_stdout(f):
        result = doctestrunner.summarize(verbose=True)
    # An individual test can only pass or fail
    if result.failed == 0:
        return (True, '')
    else:
        return False, runresults.getvalue()


class OKTest:
    """
    A single DocTest defined by OKPy.
    Instances of this class are callable. When called, it takes
    a global_environment dict, and returns a TestResult object.
    We only take a global_environment, *not* a local_environment.
    This makes tests not useful inside functions, methods or
    other scopes with local variables. This is a limitation of
    doctest, so we roll with it.
    """
    result_pass_template = Template("""
    <p><strong>{{ name }}</strong> passed!</p>
    """)

    result_fail_template = Template("""
    <p><strong style='color: red;'>{{ name }}</strong></p>
    <p><strong>Test code:</strong><pre>{{test_code}}</pre></p>
    <p><strong>Test result:</strong><pre>{{test_result}}</pre></p>
    """)

    def __init__(self, name, tests):
        """
        tests is list of doctests that should be run.
        """
        self.name = name
        self.tests = tests

    def run(self, global_environment):
        for i, t in enumerate(self.tests):
            passed, result = run_doctest(self.name + ' ' + str(i), t, global_environment)
            if not passed:
                return False, OKTest.result_fail_template.render(
                    name=self.name,
                    test_code=highlight(t, PythonConsoleLexer(), HtmlFormatter(noclasses=True)),
                    test_result=result
                )
        return True, OKTest.result_pass_template.render(name=self.name)

    @classmethod
    def from_file(cls, path):
        """
            Parse a ok test file & return an OKTest
        """
        # ok test files are python files, with a global 'test' defined
        test_globals = {}
        with open(path) as f:
            exec(f.read(), test_globals)

        test_spec = test_globals['test']

        # We only support a subset of these tests, so let's validate!

        # Make sure there is a name
        assert 'name' in test_spec

        # Do not support multiple suites in the same file
        assert len(test_spec['suites']) == 1

        # Do not support point values other than 1
        assert test_spec.get('points', 1) == 1

        test_suite = test_spec['suites'][0]

        # Only support doctest. I am unsure if other tests are implemented
        assert test_suite.get('type', 'doctest') == 'doctest'

        # Not setup and teardown supported
        assert not bool(test_suite.get('setup'))
        assert not bool(test_suite.get('teardown'))

        tests = []

        for i, test_case in enumerate(test_spec['suites'][0]['cases']):
            tests.append(dedent(test_case['code']))

        return cls(path, tests)


class OKTests:
    def __init__(self, test_paths):
        self.tests = [OKTest.from_file(path) for path in test_paths]

    def run(self, global_environment, include_grade=True):
        passed_tests = []
        failed_tests = []
        for t in self.tests:
            passed, hint = t.run(global_environment)
            if passed:
                passed_tests.append(t)
            else:
                failed_tests.append((t, hint))

        grade = len(passed_tests) / len(self.tests)
        return OKTestsResult(grade, self.tests, passed_tests, failed_tests, include_grade)


class OKTestsResult:
    """
    Displayable result from running OKTests
    """
    result_template = Template("""
    {% if include_grade %}
    <strong>Grade: {{ grade }}</strong>
    {% endif %}
    {% if grade == 1.0 %}
        <p>All {{ tests|length }} tests passed! Full grade.</p>
    {% else %}
        <p>{{ passed_tests|length }} of {{ tests|length }} tests passed</p>
        {% if passed_tests %}
        <p> <strong>Tests passed:</strong>
            {% for passed_test in passed_tests %} {{ passed_test.name }} {% endfor %}
        </p>
        {% endif %}
        {% if failed_tests %}
        <p> <strong>Tests failed: </strong>
            <ul>
            {% for failed_test, failed_test_hint in failed_tests %}
                <li> {{ failed_test_hint }} </li>
            {% endfor %}
            </ul>
        {% endif %}
    {% endif %}
    """)


    def __init__(self, grade, tests, passed_tests, failed_tests, include_grade=True):
        self.grade = grade
        self.tests = tests
        self.passed_tests = passed_tests
        self.failed_tests = failed_tests
        self.include_grade = include_grade

    def _repr_html_(self):
        return OKTestsResult.result_template.render(
            grade=self.grade,
            passed_tests=self.passed_tests,
            failed_tests=self.failed_tests,
            tests=self.tests,
            include_grade=self.include_grade
        )


def grade_notebook(notebook_path, tests_glob):
    """
    Grade a notebook file & return grade
    """
    try:
        # Lots of notebooks call grade_notebook in them. These notebooks are then
        # executed by gradememaybe - which will in-turn execute grade_notebook again!
        # This puts us in an infinite loop.
        # We use this sentinel to detect and break out of that loop.
        _global_anywhere('__OKGRADE__')
        # FIXME: Do something else here?
        return None
    except NameError:
        pass

    with open(notebook_path) as f:
        nb = json.load(f)

    initial_env = {
        # Set this to prevent recursive executions!
        '__OKGRADE__': True
    }

    global_env = execute_notebook(nb, initial_env, ignore_errors=True)

    tests = OKTests(glob.glob(tests_glob))

    return tests.run(global_env, include_grade=True)


def check(test_file_path, global_env=None):
    """
    check global_env against given test_file in oktest format
    If global_env is none, the global environment of the calling
    function is used. The following two calls are equivalent:
    check('tests/q1.py')
    check('tests/q1.py', globals())
    Returns a TestResult object.
    """
    # It isn't an error to call this with a non-existant file
    # students don't have access to all tests
    if not os.path.exists(test_file_path):
        return None

    tests = OKTests([test_file_path])

    if global_env is None:
        # Get the global env of our callers - one level below us in the stack
        # The grade method should only be called directly from user / notebook
        # code. If some other method is calling it, it should also use the
        # inspect trick to pass in its parents' global env.
        global_env = inspect.currentframe().f_back.f_globals
    return tests.run(global_env, include_grade=False)
