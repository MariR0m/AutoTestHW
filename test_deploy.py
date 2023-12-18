from sshcheckers import ssh_checkout, upload_files
import yaml
import pytest

with open('config.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)


def test_deploy():
    res = []
    upload_files(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                 f'{data.get("folder_in")}{data.get("file")}.deb', f'{data.get("folder_user")}{data.get("file")}.deb')
    res.append(ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                            f'echo {data.get("passwd")} | sudo -S dpkg -i {data.get("folder_user")}{data.get("file")}.deb',
                            "Настраивается пакет"))
    res.append(ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                            f'echo {data.get("passwd")} | sudo -S dpkg -s {data.get("file")}',
                            "Status: install ok installed"))
    assert all(res)


def test_make_folders():
    assert ssh_checkout(f"{data.get('host')}", f"{data.get('user')}", f"{data.get('passwd')}", f"mkdir -p {data.get('folder_in2')}{data.get('folder_out2')}{data.get('folder_ex2')}", "")


def test_make_file():
    assert ssh_checkout(f"{data.get('host')}", f"{data.get('user')}", f"{data.get('passwd')}", f"cd {data.get('folder_in2')}; touch file_1", "")


def test_make_arh():
    assert ssh_checkout(f"{data.get('host')}", f"{data.get('user')}", f"{data.get('passwd')}", f"cd {data.get('folder_in2')}; 7z a {data.get('folder_out2')}/arh_1", "")


def test_del_fol():
    assert ssh_checkout(f"{data.get('host')}", f"{data.get('user')}", f"{data.get('passwd')}",f"rm -rf {data.get('folder_in2')}{data.get('folder_out2')}{data.get('folder_ex2')}", "")


def test_delete():
    assert ssh_checkout(data.get('host'), data.get('user'), data.get('passwd'), f"echo {data.get('passwd')} | sudo -S dpkg -r {data.get('file')}",
    "Удаляется")


if __name__ == '__main__':
    pytest.main(['-vv'])