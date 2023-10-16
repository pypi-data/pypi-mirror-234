# A. To-do list
- pack data information
- Image correlation
- Image contrast adjust
- thickness recognition
- Add labels to multiple lines
- Complete linescan for SEM
- Add information for saved data

# B. Completed task
- Merge individual curves from multiple files
- Add shaded regions for peak range
- SEM - remove data zone
- image data structure created
- xyplot data structure created
- restructure - abstract a base class for plotting/updating data (figProc)
- Add save/load to
    - Output individual maps/2d plots so that they can be plotted in a subfigure
    - Output images

# 1. Data structure
## 1.0 imgData

## 1.1 lineData

## 1.1 figProc
### 1.2 hyperImg
## 1.2 spcMap
## 1.3 imgMap
### 1.3.1. SEM
- `remove_data_zone(kept = 0.85)` :*kept*: the portion (from top) remains; returns a new instance.
