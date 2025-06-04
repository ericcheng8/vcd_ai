Run in same directory as this file (README.md).

1. `Set-ExecutionPolicy Bypass -Scope Process`
2. `.\env_setup.ps1`

If using CLI version:

3. `.\training/train.ps1`
4. `python py/cli.py src/waves.vcd "What changed at time 382000?"`

Else:

3. `streamlit run py/app.py`

If any "training material" in `training/` is updated, make sure to delete the corresponding .txt files (including `train.txt`). Training material is extra background/relevant information provided during prompting.
