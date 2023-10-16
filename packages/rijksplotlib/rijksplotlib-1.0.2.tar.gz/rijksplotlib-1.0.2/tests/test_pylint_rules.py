"""Test the pylint rules for the rws_dataviz package."""
import astroid
import pylint.testutils
from rijksplotlib import pylint_rules


class TestUseRWSDatavizChecker(pylint.testutils.CheckerTestCase):
    """Test the UseRWSDatavizChecker class.

    Parameters
    ----------
    pylint
        A reference to the PyLint linter being used.
    """

    CHECKER_CLASS = pylint_rules.UseRijksplotlibChecker

    def test_report_error_for_plt_usage(self):
        """Validate that the visit_call adds a pylint message.

        This test validates that the visit_call function adds a pylint message
        when a plt.show() or plt.savefig() call is found.
        """
        func_node, call = astroid.extract_node(
            """
        import matplotlib.pyplot as plt

        def show_graph(): #@
            plt.show() #@
        """
        )

        self.checker.visit_call(call)
        self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="use-rijksplotlib-library",
                node=func_node,
            )
        )

    # def test_no_error_if_disabled(self):
    #     """Validate that the visit_call doesn't add a pylint message if disabled.

    #     This test validates that the visit_call function doesn't add a pylint message
    #     when the E0042 message is disabled.
    #     """
    #     func_node = astroid.extract_node("""
    #     import matplotlib.pyplot as plt
    #     # pylint: disable=use-rws-dataviz-library
    #     plt.show() #@
    #     """)

    #     # Disable the E0042 message
    #     # self.checker.linter.disable("use-rws-dataviz-libary")
    #     # print(dir(self.checker.linter))
    #     # Assert that no messages are logged when the message is disabled
    #     self.checker.visit_call(func_node)
    #     self.assertNoMessages()

    def test_no_error_if_not_desired_astroid_node(self):
        """Validate that the initial if statement is executed if no astroid func is seen."""
        node = astroid.extract_node(
            """
        import matplotlib.pyplot as plt
        def x():
            pass

        x() #@
        """
        )

        # Assert that no messages are logged when the astroid node
        # is not a function called by attribute (e.g x() instead of mymodule.x())
        self.checker.visit_call(node)
        self.assertNoMessages()

        node2 = astroid.extract_node(
            """
        import matplotlib.pyplot as plt
        plt.title() #@
        """
        )

        # Assert that no messages are logged when the astroid node
        # is not a plt.show or plt.savefig function call
        self.checker.visit_call(node2)
        self.assertNoMessages()

    def test_register_function(self):
        """Validate that the checker is registered with pylint."""
        linter = pylint.lint.PyLinter()
        pylint_rules.register(linter)
        assert "rijksplotlib-pylint-checker" in linter._checkers
