# `pycloud`

### Introduction

`pycloud` is codebase that provides an user-friendly interface around using `gsutil` and `gcloud` in interactive `Python` environemnts such as `Jupyter`.

#### Information on `gcloud` and `gsutil`

##### Command-line references

[gcloud Overview](https://cloud.google.com/sdk/gcloud/reference/)

[gsutil Overview](https://cloud.google.com/storage/docs/gsutil)

##### Regions and zones

[Google regions and zones](https://cloud.google.com/compute/docs/regions-zones/regions-zones)

Regions are collections of zones. In order to deploy fault-tolerant applications that have high availability, Google recommends deploying applications across multiple zones and multiple regions.

If you have specific needs that require your data to live in the US, it makes sense to store your resources in zones in the us-central1 region or zones in the us-east1 region.

A zone is an isolated location within a region. 

Stick with Eastern US, us-east1-b, us-east1-c, us-east1-d

##### Permissions

[Project permission](https://cloud.google.com/iam/docs/understanding-roles) (IAM)

- Owner  

- Editor  

- Viewer

- Browser 

Ch roles:

R: READ  
W: WRITE  
O: OWNER  


### `GCloud` class

To sign into Google Cloud, 

```
gc = GCloud(account = 'tsingh@broadinstitute.org', 
            project = 'daly-neale-sczmeta', 
            local = True)
```

To logout of Google Cloud,

`gc.logout()`

#### Common functions

`ls`:

`gc.ls('gs://sczmeta_genomes/test/*')`

`rm`:

`gc.rm('gs://test/', recursive=True)`

`cp`:

`gc.cpi(glob.glob('test/*'), 'gs://test/')`

### `ComputeEngine` class

The `ComputeEngine` class is used to monitor ComputeEngine virtual machines currently running in Google Cloud.

Create a ComputeEngine object:

`ce = gc.ComputeEngine()` or 
`ce = ComputeEngine(account = 'tsingh@broadinstitute.org', project = 'daly-neale-sczmeta')`

Get all running VM instances:

`ce.get_instances()`

Load a running instance:

`cei = ce.ComputeEngineInstance('vm01')`

### `ComputeEngineInstance` class

The `ComputeEngineInstance` class is used to create, modify, and delete a single virtual machine running in Google Cloud.

To load a running instance:

`cei = ce.ComputeEngineInstance('vm01')`

or 

`cei = ComputeEngineInstance(instance_name, project_name)`

### `DataProc` class

The `ComputeEngine` class is used to monitor DataProc clusters currently running in Google Cloud.

To create a `DataProc` object:

```
dp = DataProc(account='tsingh@broadinstitute.org', 
              project='daly-neale-sczmeta')
```

### `DataProcInstance` class

The `DataProcInstance` class is used to create, modify, and delete a DataProc cluster running in Google Cloud.


```
dpi = DataProcInstance('cluster01', 'tsingh@broadinstitute.org', 'daly-neale-sczmeta', 
                       zone = 'us-central1-b',
                       master_machine_type = 'n1-highmem-4', 
                       master_boot_disk_size = 50, 
                       n_workers = 2, 
                       worker_machine_type = 'n1-highmem-4', 
                       worker_boot_disk_size = 50,
                       n_pre_workers = 2, create = False)
```

To change the number of preemptible workers:

`dpi.update(n_pre_workers = 20)`

To delete a cluster,

`dpi.delete()`

### `HailRunner` class

The `HailRunner` class provides a user-friendly interface to submitting sequential Hail jobs to the Spark cluster. `HailRunner` can be inherited into downstream classes to be adapted into different Cloud infrastructure. 

```
outdir = 'outdir'

runner = HailRunner(outdir = outdir, 
                    input_file = "/Users/tsingh/1000Genomes_248samples_coreExome10K.vcf.bgz",
                    hail_jar_path = "/Users/tsingh/repos/hail/build/libs/hail-all-spark.jar", 
                    pyhail_zip = "/Users/tsingh/repos/hail/python/")

runner.add_batch(""" 
vds = hc.import_vcf('{}')
vds = vds.split_multi()
vds.write('{}')""", os.path.join(outdir, '1kg.vds'))

runner.submit('save_vds')
```

```
runner.quick_submit("""
vds = hc.read('{}')

print(vds.count(genotypes=True))
""".format(runner.f))
```

### `HailRunnerGC` class

The `HailRunner` class adapted for use with Google Cloud and DataProc.


```
outdir = 'test/'
bucket_dir = 'gs://test/'
```

```
runner = HailRunnerGC('vm01',
                      outdir = outdir, 
                      input_file = "gs://data/exomes.vcf.bgz")

runner.add_batch(""" 
vds = hc.import_vcf('{}')

vds = vds.split_multi()

vds.write('{}')""", change_ext(runner.f, '.vds', '.vcf.bgz', bucket_dir))

runner.submit('save_vds')
```

```
runner.quick_submit("""

vds = hc.read('{}')

print(vds.count())
print(vds.variant_schema)
print(vds.sample_schema)
print(vds.global_schema)

""".format(runner.f))
```

### Installing Hail on Broad prem

Add `SPARK_HOME`, `HAIL_HOME`, and add Hail and Spark bins to `PATH`.

On Broad cluster, get the version of Spark correct. `./gradlew -Dspark.version=2.1.0.cloudera shadowJar`

```
use CMake
use GCC-5.2
use Java-1.8
```

before running gradlew