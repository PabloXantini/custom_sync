# Using Python Implementation

Check the file example.json for setup a whislist of directories for load/download files between OneDrive and your local disk.
In this file you will encounter with these parameters:
- __disk_root__: This is your local disk where you put your files
- __onedrive_destiny__: Could it there different OneDrive folder names, so you can put the OneDrive folder of your organization. For more organization, I recommend create a dedicated folder.
- __whitelist__: The list of directories which will be synced, in the OneDrive must appear with the same name.

### Run the script for loading (PC to OneDrive)
```python
python sync.py --mode load
```

### Run the script for downloading (OneDrive to PC)
```python
python sync.py --mode download
```