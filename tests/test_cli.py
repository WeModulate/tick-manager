from click.testing import CliRunner

from tick_manager.cli.main import cli


def test_greet():
    runner = CliRunner()
    result = runner.invoke(cli, ["greet"])
    assert result.exit_code == 0
    assert "Hello, Tick Manager!" in result.output


def test_add_cmd():
    runner = CliRunner()
    result = runner.invoke(cli, ["add-cmd", "2", "3"])
    assert result.exit_code == 0
    assert "Result: 5.0" in result.output


def test_divide_cmd_by_zero():
    runner = CliRunner()
    result = runner.invoke(cli, ["divide-cmd", "10", "0"])
    assert result.exit_code != 0
    assert "Error: division by zero" in result.output
