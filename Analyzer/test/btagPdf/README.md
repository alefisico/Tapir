# To calculate the btag pdfs

For the BLR computation, we need a map of the btag discriminators as a function of pt and eta. The file `calculateBtagPdfs.py` does that. 

In short, it opens a nanoAOD file for semileptonic ttbar, applies a loose selection, and creates 3D maps for jets identified as `l` (uds), `c` or `b` from the generator information (variable already included in nanoAOD).

To run:
```python
python calculateBtagPdfs.py -v 2017
```
where -v corresponds to the dataset to calculate. There is a small condor script to submit jobs to the condor batch:
```bash
condor_submit condorJob.sub
```
