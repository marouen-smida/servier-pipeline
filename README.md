# Servier Pipeline — Local Setup (Astro CLI + Airflow)

This guide explains how to get the project running locally with the **Astro CLI** and **Apache Airflow**, where to place input files, how to trigger the DAG(s), and where to find outputs.

> **Prereqs**
> - Docker Desktop (or Docker Engine) installed and running
> - Git
> - ~6–8 GB free RAM for the Airflow stack
>
> Optional but recommended:
> - Python 3.10+ (via [pyenv](https://github.com/pyenv/pyenv)) for tooling/scripts if present.

---

## 1) (Optional) Install `pyenv` and create a Python 3.10 virtualenv

If you want a clean local Python environment (useful for running helper scripts or tests outside Airflow):

### Install pyenv

#### macOS (Homebrew)
```bash
brew install pyenv
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y build-essential curl git libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev \
  libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl
curl https://pyenv.run | bash
```
Add to your `~/.bashrc` or `~/.zshrc`:
```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
```
Restart your shell.

### Install Python 3.10
```bash
pyenv install 3.10.18
pyenv virtualenv 3.10.18 servier-pipeline-3.10
pyenv activate servier-pipeline-3.10
```

### Install dependencies (if any scripts need them)
```bash
pip install -r requirements.txt
```

Now you have a dedicated environment for this repo outside of Docker.

---

## 2) Install the Astro CLI

Install the `astro` command-line tool from Astronomer.

### macOS (Homebrew)
```bash
brew install astro
```

### Linux (curl script)
```bash
curl -sSL https://install.astronomer.io | sudo bash
```

> After install, verify:
```bash
astro version
```

If the command prints a version, you’re good to go.

---

## 3) Clone and initialize the project

```bash
git clone https://github.com/marouen-smida/servier-pipeline.git
cd servier-pipeline
# if this repo uses branches, switch to the develop branch
git checkout develop
```


---

## 4) Project structure (what goes where)

```
servier-pipeline/

├─ dags/                  # Airflow DAGs

├─ include/               # Put the csv and json files here

├─ data/processed         # The output result here (json)

├─ Other_questions        # Answers to other questions
```



## 5) Build and run Airflow locally

CD into the repo folder and start the full Airflow stack (webserver, scheduler, triggerer, Postgres):
```bash
astro dev start
```
This will:
- Build the Docker image with your requirements and configurations
- Spin up the Airflow services
- Mount your project code into the containers for live reloads

**Open the Airflow UI**: http://localhost:8080


## 6) Place input files & get outputs

- **Put your input files here (host):**
  - `./include`
- **They are visible in containers at:**
  - `/usr/local/airflow/include/`
- **Pipeline results will appear here (host):**
  - `./data/processed/`
- **Inside containers:**
  - `/usr/local/airflow/include/data/`

## 7) Enable and trigger the DAG

You can trigger DAGs via the **UI** or the **CLI**.

From the Airflow UI
1. Go to http://localhost:8080
2. Find your DAG ( `servier_pipeline`)
3. Toggle it **On**
4. Click **Play ▶** → **Trigger DAG**




## 8) Where to find result files

Results are written to `./data/processed/` on your machine.
