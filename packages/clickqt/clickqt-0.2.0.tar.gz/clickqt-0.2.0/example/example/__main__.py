import os
from typing import TYPE_CHECKING

import click
from click_option_group import optgroup
from PySide6.QtWidgets import QSpinBox

import clickqt
from clickqt.basedint import BasedIntParamType

if TYPE_CHECKING:
    from clickqt.widgets.customwidget import CustomWidget


@click.group()
def utilgroup():
    pass


@utilgroup.command()
@click.option("--optional", type=str, required=False)
@click.option("--required", type=str, required=True)
def optreq(**kwargs):
    """
    Blah blah i
    am a long
    text
    """
    print(kwargs)


@utilgroup.command()
@click.option(
    "--someflag",
    "-sf",
    type=bool,
    is_flag=True,
)
@click.option("--foo", multiple=True, type=(click.Path(), int))
@click.option("--someint", multiple=True, type=click.File())
def foobar(someint, someflag, foo):
    click.echo(f"{someflag} {someint} {foo}")


@utilgroup.command()
@click.argument("username", default=lambda: os.environ.get("USERNAME", ""))
@click.option(
    "--verbose",
    type=bool,
    is_flag=True,
    default=True,
    required=True,
    help="Verbosity of the output",
)
@click.option("-c", "--count", count=True, default=3, help="Repetition of the option")
@click.option(
    "--hash-type-single", confirmation_prompt=True, type=click.Choice(["MD5", "SHA1"])
)
@click.option(
    "--hash-type-multiple",
    required=True,
    type=click.Choice(["MD5", "SHA1"]),
    multiple=True,
)
@click.option(
    "-r",
    "--range",
    confirmation_prompt=True,
    type=click.FloatRange(max=20.23, clamp=True),
)
@click.password_option()
@click.confirmation_option(
    expose_value=False,
    prompt="Are you sure you want to run the application with these options?",
)
@click.argument("filename", type=click.Path(exists=True))
@click.argument("input", type=click.File("rb"))
@click.argument("output", type=click.File("wb"))
def test(
    verbose,
    username,
    count,
    hash_type_single,
    hash_type_multiple,
    range,
    password,
    filename,
    input,
    output,
):
    click.echo(
        f"verbose: '{verbose}'\n"
        + f"username: '{username}'\n"
        + f"count: '{count}'\n"
        + f"hash_type_single: '{hash_type_single}'\n"
        + f"hash_type_multiple: '{hash_type_multiple}'\n"
        + f"range: '{range}'\n"
        + f"password: '{password}'\n"
        + f"filename: '{filename}'"
    )
    click.echo("input: ", nl=False)
    while True:
        chunk = input.read(1024)
        if not chunk:
            break
        output.write(chunk)
    click.echo()  # New line


@utilgroup.command()
@click.option(
    "--userinfo",
    type=(str, int, click.types.DateTime()),
    default=["test", 1, "2023-06-14 15:20:25"],
)
def greet(userinfo):
    fname, no, date = userinfo
    date = date.strftime("%Y-%m-%d")
    click.echo(f"Hello, {fname}! Int, Date: {no, date}.")


@utilgroup.command()
@click.option("--pos", type=int, nargs=2, default=[1, 2])
@click.option("--custom", type=BasedIntParamType())
def position(pos, custom):
    a, b = pos
    c = custom
    click.echo(f"{a}/{b} + {c}")


@click.group()
def hello():
    print("Hello group")


@hello.command()
@click.option("--n", type=int, default=3)
def test(n):
    for i in range(n):
        click.echo(i)


def test_callback(ctx, param, value):
    if value == "2":
        return "123"
    else:
        raise click.BadParameter(f"Wrong value")


@hello.command()
@click.option("-t", type=str, callback=test_callback)
def test_with_callback(t):
    click.echo(t)


@hello.command()
@click.option(
    "-ns", type=(int, str), multiple=True, required=True, default=[(1, "a"), (2, "b")]
)
def hello_ns(ns):
    for i, s in ns:
        for _ in range(i):
            click.echo(f"{s}{i}")


@hello.command()
@click.option(
    "paths",
    "--path",
    multiple=True,
    envvar="PATH",
    default=[".", "tests"],
    type=click.Path(exists=True),
)
def hellp_path(paths):
    for path in paths:
        click.echo(path)


@click.group()
def hello2():
    print("Hello2 group")


@hello2.command()
@click.option("-ns", type=(int, str), multiple=True)
def hello_ns2(ns):
    print(ns)
    for i, s in ns:
        for _ in range(i):
            click.echo(f"{s}{i}")


@utilgroup.command()
@click.option("--test", type=int)
@optgroup.group(
    "Server configuration", help="The configuration of some server connection"
)
@optgroup.option("-h", "--host", default="localhost", help="Server host name")
@optgroup.option("-p", "--port", type=int, default=8888, help="Server port")
@click.option("--debug/--no-debug", default=False, help="Debug flag")
@optgroup.group("Test configuration", help="The configuration of some test suite.")
@optgroup.option("--n", default=5, help="Number of test rounds")
def cli(test, host, port, debug, n):
    params = test, host, port, debug
    print(params)
    print(n)


utilgroup.add_command(hello)
hello.add_command(hello2)


def custom_getter(widget: "CustomWidget"):
    assert isinstance(widget.widget, QSpinBox)
    return widget.widget.value()


def custom_setter(widget: "CustomWidget", val):
    widget.widget.setValue(val)


gui = clickqt.qtgui_from_click(
    utilgroup,
    {BasedIntParamType: (QSpinBox, custom_getter, custom_setter)},
    "custom entrypoint name",
)

if __name__ == "__main__":
    utilgroup()
