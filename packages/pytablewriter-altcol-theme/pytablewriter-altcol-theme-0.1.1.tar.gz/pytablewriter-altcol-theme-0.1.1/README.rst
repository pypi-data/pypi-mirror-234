.. contents:: **pytablewriter-altcol-theme**
   :backlinks: top
   :depth: 2


Summary
============================================

.. image:: https://github.com/thombashi/pytablewriter-altcol-theme/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/thombashi/pytablewriter-altcol-theme/actions/workflows/ci.yml
    :alt: CI status of Linux/macOS/Windows

.. image:: https://coveralls.io/repos/github/thombashi/pytablewriter-altcol-theme/badge.svg?branch=master
    :target: https://coveralls.io/github/thombashi/pytablewriter-altcol-theme?branch=master
    :alt: Test coverage: coveralls

.. image:: https://github.com/thombashi/pytablewriter-altcol-theme/actions/workflows/github-code-scanning/codeql/badge.svg
    :target: https://github.com/thombashi/pytablewriter-altcol-theme/actions/workflows/github-code-scanning/codeql
    :alt: CodeQL

``pytablewriter-altcol-theme`` is a `pytablewriter <https://github.com/thombashi/pytablewriter>`__ plugin to provide a terminal theme.


Installation
============================================
::

    pip install pytablewriter-altcol-theme

Usage
============================================

:Sample Code:
    .. code-block:: python

        import pytablewriter as ptw

        writer = ptw.TableWriterFactory.create_from_format_name(
            "markdown",
            headers=["INT", "STR"],
            value_matrix=[
                [1, "hoge"],
                [2, "foo"],
                [3, "bar"],
            ],
            margin=1,
            theme="altcol",
        )
        writer.write_table()

You can change the color of the theme by using the ``color`` parameter:

:Sample Code:
    .. code-block:: python

        import pytablewriter as ptw

        writer = ptw.TableWriterFactory.create_from_format_name(
            "markdown",
            headers=["INT", "STR"],
            value_matrix=[
                [1, "hoge"],
                [2, "foo"],
                [3, "bar"],
            ],
            margin=1,
        )

        writer.set_theme("altcol", color="yellow")

        writer.write_table()


Other Examples
--------------------------------------------
- Generate HTML example: `source file <https://github.com/thombashi/pytablewriter-altcol-theme/blob/master/examples/write_html.py>`__ and `the output <https://thombashi.github.io/pytablewriter-altcol-theme/example.html>`__


Dependencies
============================================
- Python 3.7+
- `Python package dependencies (automatically installed) <https://github.com/thombashi/pytablewriter-altcol-theme/network/dependencies>`__


Related Projects
============================================
- `pytablewriter <https://github.com/thombashi/pytablewriter>`__
- `pytablewriter-altrow-theme <https://github.com/thombashi/pytablewriter-altrow-theme>`__
