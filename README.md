## File descriptions

- `export_stat.py`goes through the train files extracts them into `stats.csv` in the same directory.
- `classifier.py` goes through the test files and references `stats.csv` to guess based on the distance, using KNN.

## Requirements

- Includes external libraries like scikit-learn, pandas, scapy, and statistics.

## Running code

- In `app/` directory, create venv with `python3 -m venv venv` then run `run.sh`
  - `run.sh` includes venv start, requirements install, and running two python files.
- Or install directly with `pip install -r requirements.txt` then run `export_stats.py` and `classifier.py` sequentially.
- Or (preferably on PC) install Docker GUI and run `docker-compose up -d --build` then `docker exec -it app /bin/bash`. Now you can run the python files.
