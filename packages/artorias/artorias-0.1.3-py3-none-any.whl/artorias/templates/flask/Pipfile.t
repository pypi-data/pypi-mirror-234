[[source]]
url = "https://pypi.python.org/simple/"
verify_ssl = true
name = "pypi"

[packages]
artorias = "*"

[dev-packages]
pre-commit = "*"

[scripts]
dev = "flask run"
serve = "gunicorn -c gunicorn.conf.py wsgi:app"

[requires]
python_version = "$python_version"
