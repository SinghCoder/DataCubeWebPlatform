@echo off
for %%i in (c:\batch_files\dataset_doc\*.yaml) do datacube product add --auto-match %%i 
