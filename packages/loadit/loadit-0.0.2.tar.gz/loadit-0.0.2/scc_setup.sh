
module load python3/3.10.12 git/2.31.1 gcc/12.2.0

if [ ! -d "env" ]; then
  python -m venv "env"
fi

source env/bin/activate

