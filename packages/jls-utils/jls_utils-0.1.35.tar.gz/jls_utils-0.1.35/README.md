# julius-utils

## Before start

To work, you need to create **gitlab** [`TOKEN`](https://gitlab.com/-/profile/personal_access_tokens) and `USERNAME`. Add appropriate `GITLAB_ACCESS_TOKEN` and `GITLAB_USERNAME` in **~/.bashrc** and run **source ~/.bashrc**:

```bash
export GITLAB_USERNAME=<your gitlab>
export GITLAB_ACCESS_TOKEN=<your gitlab token>
```

After it you can install package 

```commandline
pip install -U jls_utils --extra-index-url https://$GITLAB_USERNAME:$GITLAB_ACCESS_TOKEN@gitlab.com/api/v4/projects/38063738/packages/pypi/simple
```

## Main

It is a library with helper functions
