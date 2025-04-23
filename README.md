## File descriptions

- `export_stat.py`goes through the train files extracts them into `stats.csv` in the same directory.
- `classifier.py` goes through the test files and references `stats.csv` to guess based on the distance, using KNN.

## Requirements

- Includes external libraries like scikit-learn, pandas, scapy, and statistics.

## Running code

- Create venv with `python3 -m venv venv` then run `run.sh`
- Or install directly with `pip install -r requirements.txt` then run `classifier.py`
