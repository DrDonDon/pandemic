mkdir pandemic_tmp
cd pandemic_tmp
python3 -m venv pandemic
pip install pandemic
python3 -c "import pandemic; pandemic.run()"