def run_repl_and_send_input(commands):
    import subprocess

    proc = subprocess.Popen(
        ['python3', '-m', 'promptshell.main'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    input_str = '\n'.join(commands) + '\n'
    try:
        stdout, stderr = proc.communicate(input=input_str, timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()
    print("STDOUT:", stdout)
    print("STDERR:", stderr)
    return stdout, stderr, proc.returncode

def test_quit_command():
    out, err, code = run_repl_and_send_input(["quit"])
    assert "Terminating" in out or "Terminating" in err

def test_exit_command():
    out, err, code = run_repl_and_send_input(["exit"])
    assert "Terminating" in out or "Terminating" in err
