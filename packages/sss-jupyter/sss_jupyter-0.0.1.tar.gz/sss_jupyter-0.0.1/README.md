# sss-jupyter

A package to launch a JupyterLab server with a self-signed SSL certificate.

## Install

```sh
pip install sss-jupyter
```

## Usage

The following command launches a JupyterLab sesrver with HTTPS.

```sh
python3 -m sss_jupyter
```

Output:
```
generate ssh key in ~/.jupyterkey...
JupyterLab server is runnning at:
    https://xx.xx.xx.xx:8888/?token=9a935b2658685774fe07c3bca01e8eb4d23aa52472eb263ab1

JupyterLab logs are stored in ~/.jupyter.log
```

Option:
```
-p, --port: int (default: 8888)
     The port the server will listen on.
-l, --token_length: int (default: 50)
    The character length of a secret token.
```
