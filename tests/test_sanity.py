from openrouter_observer import main

def test_argparse_runs():
    assert callable(main.main)
