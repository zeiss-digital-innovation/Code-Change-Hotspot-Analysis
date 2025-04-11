# Project Overview

### Main Features
`createHotspots.py` is a small tool that automatically generates an interactive treemap in the web browser functioning as a tool for Hot- and Coldspotanalysis using the [plotly](https://plotly.com/python/treemaps/) framework. It generates data using the [git log](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History) history from a local git repository given by the user.  

A file is regarded as a cold- or hotspot, depending on the date the change on the file has been commited. To differentiate between cold- and hotspots, the tool uses a **reference date** (i.e. 2024-02-22) given by the user.   
**Hotspots** are files that have recently been changed, meaning changes on the file that have been commited after the refernce date.   
**Coldspots** are files that have not been changed recently, meaning there are no changes commited after the reference date.  
**Note:** If you hover over a file regarded as a coldspot it will still have *one* change. This is the initial commit and has to be added in order for the file to be shown on the treemap.  
A **node** is an individual rectangle schown on the treemap. They are nested, since a common folder structure of a repository is also nested. The bigger a node the more changes it has. For example: In *Picture 1* the `readme.md` file in the `doc` directory has 11 changes while the `api_reference.md` has only 8 changes and thus is smaller. 

Example on how a treemap might look like using pseudo data: 

![treemap_example_1_png](images/treemap_example_1.png)  
*Picture 1* 
The nodes with a red color represent hotspots, while the nodes with a blue represent coldspots.  
The grey nodes are usally directories that contain hot- and coldspots. Directories that have one or more files in only one state take the color of the file(s) (i.e. the Config directory which only contains a hotspot and thus is read).

![treemap_example_2_png](images/treemap_example_2.png)  
*Picture 2* 
Here is an example to show the interactivity of the treemap. The user can click on one node to "drill-down" and see the individual nodes in more detail. 
### Target Audience 
(also refer to scenarios and personas)

# Installation Guide
### Requirements
### Installation Steps

# User Manual
### Step by Step Guide
with screenshots and code snippets