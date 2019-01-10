# Gip

## Usage
```bash
gip --gitlab-token=<token> --github-token=<token> requirements.yml
```

## Requirements.yml

```yaml
- name: ansible-role-plex  # directory name in destination directory
  repo: https://github.com/wilmardo/ansible-role-plex  # repository url
  type: github  # type: gitlab or github allowed
  version: 2.1.0  # version: tag, branch name or commit sha
  dest: lib/  # destination directory
```

## Visual Studio Code Setup
```json
///.vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File (Integrated Terminal)",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/gip/main.py",
            "args" : ["--gitlab-token=-hBtB7xJ3msiRtsHBFrQ", "--github-token=c58e0b2750301008b0051a4b9275a9aad687c9df", "tests/requirements.yml"],
            "console": "integratedTerminal"
        }
    ]
}
```


## Draft release
```bash
python setup.py sdist
```