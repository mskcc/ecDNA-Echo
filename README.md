# ecDNA-Echo
Pipeline to Analyze ecDNA in collaboration with BoundlessBio

## Version 2

### Dependencies

The environment yml file may be found in ```/scripts/envs/echo.yml```

You can get all the dependencies with 

```
conda env create --name ecDNA --file=/scripts/envs/echo.yml
conda activate ecDNA
```

Note: You may need to ask for permission to get facetsAPI access. Please visit https://github.com/mskcc/facetsAPI and contact Adam Price if you need access.

### Step 0: Configure Config File

The default config file is scripts/global_config_bash.rc.
Edit ```projectName``` to the desired project name, ```dataDir``` to the desired data directory, and place a list of the sampleIds to run (separated by newlines) in the manifest folder (by default it is ```[dataDir]/input/manifest/[projectName]```). Edit ```sampleFull``` to this path. All other paths and configurations can be changed for further customization, such as choosing to use the FACETS called tumor purity.

### Step 1: Run the Parallelized ECHO Caller

```
cd scripts
sh generateECHOResults.sh ./global_config_bash.rc
```

### Step 2: Merge ECHO Results

Please ensure that all jobs have concluded. You can check statuses in ```[dataDir]/flag/flag_[projectName]/echoCalls```. Ensure that no samples are still running.

```
sh merge_echo_results.sh ./global_config_bash.rc
```

### Step 3 (Optional, for FACETS Report): Run the Parallelized FACETS Caller

```
sh submit_facets_on_cluster.sh ./global_config_bash.rc
```

### Step 4 (Optional, for FACETS REport): Merge FACETS Results

Please ensure that all jobs have concluded. You can check statuses in ```[dataDir]/flag/flag_[projectName]/facetsCalls```.

```
sh merge_facets_results.sh ./global_config_bash.rc
```