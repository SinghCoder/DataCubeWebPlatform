# Metadata Add

Add default metadata like earth observatory and telemetry data by running 

```
datacube metadata add default_metadata_types.yaml
```

# Metadata file to YAML format

Datacube recognises metadata files in yaml format/ json format only.
So if the file is in MTL.txt format run

```
MTL_MetadataTo_YAML.py --output <destination path with a file name> <path to mtl file>
```

E.g. if MTL file is in previous directory and yaml to be created in current directory named abc.yaml

Run

```
MTL_MetadataTo_YAML.py --output ./abc.yaml ../
```

## If metadata is in XML format

```python
python xmlToYaml.py <path to xml> 
```
It creates corresponding yaml file in this folder

e.g.

To convert try.xml currently in this folder run,

```python
python xmlToYaml.py try.xml
```
