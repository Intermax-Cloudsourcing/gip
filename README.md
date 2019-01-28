# Gip

## Usage
```bash
gip --gitlab-token=<token> requirements.yml
```

## Requirements.yml

```yaml
- name: ansible-role-plex  # directory name in destination directory
  repo: https://github.com/wilmardo/ansible-role-plex  # repository url
  type: github  # type: gitlab or github allowed
  version: 2.1.0  # version: tag, branch name or commit sha defaults to master
  dest: lib/  # destination directory, defaults to current directory
```
