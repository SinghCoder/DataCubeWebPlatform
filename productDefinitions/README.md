#Product Definition
The first step in indexing process is to describe the source of the imagery. We include basic details
about which sensor the data comes from, what format to expect the data in, as well as its measurements, e.g. bands.
This is done by drafting a document called a product definition for each data type. This product definition is then added to the system. Adding a product definition enables the system to accept that product. 

## Add product definitions in datacube 

```python
datacube product add <path to product definition .yaml>
```

e.g.

```python
datacube product add ls_usgs.yaml
```