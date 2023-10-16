import subprocess


def test_git_no_config(tmp_home_dir):
    """
    Ensure git finds config in tmp_home_dir.
    """
    tmp_home_dir.joinpath('.gitconfig').write_text(
        '[user]\nemail="joe@pie.com"', encoding='utf-8'
    )
    out = subprocess.check_output(['git', 'config', 'user.email'])
    out == 'joe@pie.com'
