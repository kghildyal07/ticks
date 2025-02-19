# Ticks Service

## How to run the project?
This project was developed on python 3.12 and Windows

```
git clone https://github.com/kghildyal07/ticks.git
cd ticks
py -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Set pythonpath to make sure that pytest can be executed (in powershell):
```
$env:PYTHONPATH = $PWD;
pytest
python .\run.py
```

There are also simulations in the following directory:
```
cd ./simulations
python all_simulations.py
python current_ticks.py
python past_ticks.py
```

Finally, to run the load test, ensure locust in installed
```
cd tests
python load_locust.py
```

## Artifacts
There are coverage and locust test reports in the `./reports` directory.

## Assumptions:
- timestamp is unix timestamp and it is not in the future w.r.t current timestamp
- Non - blocking lock was implemented assuming that APIs' performance is more important than the data integrity. Threading library could have been used as well for a blocking lock.

## Improvements:
- More unit tests
- More stress test and on a better system. I had limited resource on my laptop.
- better doctstring in the codebase.
- run with gunicorn for better process management.
- Probably have just one deque cache instead of two. I had to go with two for simplicity.
- Persist the populated cache is parquet/arrow file before it is destroyed.
- Add GHA and run unit tests in the CI pipeline.

## Challenge:
I aboslutely loved it. I had not worked on a concurrency problem statements a lot. So it was a great learning experience for me altogether. 
