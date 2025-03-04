# Analyzer 

### Recommended Git Log commands
```
git log --before="2024-01-01" --pretty=format:"" --name-only`

git log --since="2024-01-01" --pretty=format:"" --name-only
```

## treemap.py
The script adds one "change" towards the changes of a file, counting it as the "initial commit", which are not represented in the data seen in the treemap because file names from the older data set that are not in the newer data set will be added with a weight of "zero". Since "plotly.express" does not show paths with a value of zero, a "initial commit" has to be added.