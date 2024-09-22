from click.testing import CliRunner
from tick_manager.cli.main import cli

def test_greet():
    runner = CliRunner()
    result = runner.invoke(cli, ['greet'])
    assert result.exit_code == 0
    assert 'Hello, Tick Manager!' in result.output

