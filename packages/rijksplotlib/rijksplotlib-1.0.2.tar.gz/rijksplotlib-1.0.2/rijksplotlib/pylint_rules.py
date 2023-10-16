"""Custom pylint rules for rijksplotlib.

These rules are used to check that the rijksplotlib library is used correctly and
enforce the use of :func:`rijksplotlib.pyplot.show` and
:func:`rijksplotlib.pyplot.savefig` over ``matplotlib.pyplot.show()``
and ``matplotlib.pyplot.savefig()``.
"""
import astroid
from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.lint import PyLinter


class UseRijksplotlibChecker(BaseChecker):
    """A PyLint linting rule that prevents a user from using ``plt.show`` and ``plt.savefig``.

    This linter informs the user that plt.show and plt.savefig should be avoided
    in favor of :func:`rijksplotlib.pyplot.show` and :func:`rijksplotlib.pyplot.savefig`
    as these functions provide safeguards against incorrect usage of matplotlib graphs.
    The import for these functions is ``import rijksplotlib.pyplot as rlt``.

    Example
    -------

    .. code-block:: python

        import matplotlib.pyplot as plt
        import rijksplotlib.pyplot as rlt

        plt.plot([1, 2, 3])
        plt.show()  # This will raise an error
        rlt.show()  # This will not raise an error
    """  # noqa: D412

    __implements__ = IAstroidChecker

    name = "rijksplotlib-pylint-checker"
    _symbol = "use-rijksplotlib-library"
    msg = (
        "plt.show and plt.savefig should not be used directly!"
        " Use rijksplotlib.pyplot.show() or rijksplotlib.pyplot.savefig() instead."
    )
    priority = -1
    msgs = {
        "E0042": (
            msg,
            _symbol,
            msg,
        ),
    }

    def visit_call(self, node: nodes.Call) -> None:
        """Raise an error if an AST node contains ``plt.show`` or ``plt.savefig``.

        Parameters
        ----------
        node
            The AST node being evaluated by Pylint.
        """
        if isinstance(node.func, astroid.Attribute):
            if (
                node.func.attrname in ["show", "savefig"]
                and node.func.expr.as_string() == "plt"
            ):
                if self.linter.is_message_enabled(self._symbol):
                    self.add_message(self._symbol, node=node)


def register(linter: PyLinter) -> None:
    """Register the PyLint checker in the pylint extension list.

    Parameters
    ----------
    linter
        A reference to the PyLint linter being used.
        In our case this is the BaseChecker.
    """
    linter.register_checker(UseRijksplotlibChecker(linter))
