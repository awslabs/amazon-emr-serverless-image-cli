# Amazon EMR Serverless Image CLI

## Introduction

[Amazon EMR Serverless](https://aws.amazon.com/emr/serverless/) provides support for
Custom Images, a capability that enables you to customize the Docker container images used for running
Apache Spark and Apache Hive applications on [Amazon EMR Serverless](https://aws.amazon.com/emr/serverless/).
Custom images enables you to install and configure packages specific to your workload that are not available
in the public distribution of EMR’s runtimes into a single immutable container. An immutable container
promotes portability and simplifies dependency management for each workload and enables you to integrate
developing applications for EMR Serverless with your own continuous integration (CI) pipeline.

To test the compatibility of the modifications made to your EMR base image, we are providing a utility to validate 
the image’s file structure. The utility will examine basic required arguments and ensure that the modifications work as 
expected and prevent job failures due to common misconfigurations. This tool can be integrated into your Continuous 
Integration (CI) pipeline when you are building your image.

## For Developers

Developers who wish to develop on or contribute to the source code, please refer to [Contribution Guide](CONTRIBUTING.md) and [Development Guide](DEVELOPMENT_GUIDE.md).

## Getting Started

### Prerequisite

Before running this tool, please make sure you have Docker CLI installed.

#### Install Docker CLI (Optional).

This tool utilizes [Docker CLI](https://docs.docker.com/get-docker/) to help validate custom images.
Please make sure you have Docker CLI installed prior to using the tool.

### Installation

#### Option 1 - Python

If you have python, you can get the wheel file from our Releases and install using Python3.

```
pip3 install <location-of-wheel-file>
```

The command is available as `amazon-emr-serverless-image`.

#### Option 2 - PyInstaller

PyInstaller creates an executable. See instructions [here](installer/pyinstaller/INSTRUCTION.md).

### Usage

#### Validate Custom Image

Use command:

```
amazon-emr-serverless-image validate-image -i <image_name> -r <release_name> [-t <image_type>]
```

-i specifies the local image URI that needs to be validated, this can be the image URI or any name/tag you defined for your image.

-r specifies the exact release version of the EMR base image used to generate the customized image. It supports `emr-6.9.0` and newer releases.

-t specifies the image type. The default value is `spark`. It also accepts `hive`.

After successfully running the tool, the log info will show test results. If the image doesn't meet necessary configuration requirements, you will see error messages that inform the missing part.

##### Basic Test

The [basic test](amazon_emr_serverless_image_cli/validation_tool/validation_tests/check_manifest.py) ensures the image contains expected configuration. The following parameters are verified in this test:

* `UserName`
* `WorkingDir`
* `EntryPoint`

##### Environment Test

The [environment test](amazon_emr_serverless_image_cli/validation_tool/validation_tests/check_envs.py) ensures the required environment variables are set to the expected paths.

Examples:

* `SPARK_HOME=/usr/lib/spark`
* `JAVA_HOME=/etc/alternatives/jre`

##### File Structure Test

The [file structure test](amazon_emr_serverless_image_cli/validation_tool/validation_tests/check_files.py) ensures the required files exist in expected locations. For different
types of images, the required dependencies are different. You should make sure those files are in the correct
location.

##### Local Job Run Test

The [local job run test](amazon_emr_serverless_image_cli/validation_tool/validation_tests/check_local_job_run.py) ensures that the custom image is valid and can pass basic job run. We will run a sample local spark job with following configuration:

```
docker run -it --rm <image-uri> spark-submit 
--deploy-mode client 
--master local 
--class org.apache.spark.examples.SparkPi local:///usr/lib/spark/examples/jars/spark-examples.jar
```

### Output Results

Examples:

```
Amazon EMR Serverless - Image CLI
Version: 0.0.1
... Checking if docker cli is installed
... Checking Image Manifest
[INFO] Image ID: 4c43e76fe820dc0df0fefe31f5307bd0d4da25f9ab606fea8cbdf0cc3a01b9ae
[INFO] Created On: 2022-12-02T07:39:13.100828697Z
[INFO] Default User Set to hadoop:hadoop : PASS
[INFO] Working Directory Set to /home/hadoop : PASS
[INFO] Entrypoint Set to /usr/bin/entrypoint.sh : PASS
[INFO] JAVA_HOME is set with value: /etc/alternatives/jre : PASS
[INFO] SPARK_HOME is set with value: /usr/lib/spark : PASS
[INFO] File Structure Test for bin-files in /usr/bin: PASS
[INFO] File Structure Test for hadoop-files in /usr/lib/hadoop: PASS
[INFO] File Structure Test for hadoop-jars in /usr/lib/hadoop/lib: PASS
[INFO] File Structure Test for spark-jars in /usr/lib/spark/jars: PASS
[INFO] File Structure Test for spark-bin in /usr/lib/spark/bin: PASS
[INFO] File Structure Test for java-bin in /etc/alternatives/jre/bin: PASS
... Start Running Sample Spark Job
[INFO] Sample Spark Job Test with local:///usr/lib/spark/examples/jars/spark-examples.jar : PASS
-----------------------------------------------------------------
Overall Custom Image Validation Succeeded.
-----------------------------------------------------------------
```

Error Message:

```
Amazon EMR Serverless - Image CLI
Version: 0.0.1
... Checking if docker cli is installed
... Checking Image Manifest
[INFO] Image ID: 3f061067cacfb69cbf76f233fea73d01ab464a0de748fdba18addce0fe1cfd7b
[INFO] Created On: 2022-12-08T22:45:38.767201727Z
[INFO] Default User Set to hadoop:hadoop : PASS
[INFO] Working Directory Set to /home/hadoop : PASS
[INFO] Entrypoint Set to /usr/bin/entrypoint.sh : PASS
[INFO] JAVA_HOME is set with value: /etc/alternatives/jre : PASS
[INFO] SPARK_HOME is set with value: /usr/lib/spark : PASS
[INFO] File Structure Test for bin-files in /usr/bin: PASS
[INFO] File Structure Test for hadoop-files in /usr/lib/hadoop: PASS
[ERROR] avro MUST be in /usr/lib/hadoop/lib : FAIL
[INFO] File Structure Test for spark-jars in /usr/lib/spark/jars: PASS
[INFO] File Structure Test for spark-bin in /usr/lib/spark/bin: PASS
[INFO] File Structure Test for java-bin in /etc/alternatives/jre/bin: PASS
... Start Running Sample Spark Job
[INFO] Sample Spark Job Test with local:///usr/lib/spark/examples/jars/spark-examples.jar : PASS
-----------------------------------------------------------------
Custom Image Validation Failed. Please see individual test results above for detailed information.
-----------------------------------------------------------------
```

## Support

This tool is only supported for the following EMR Serverless releases:

- `6.9.0`
- `6.10.0`
- `6.11.0`
- `6.12.0`

Future releases will be supported. Usage of the validation tool does not guarantee your image or job will run in EMR Serverless, but is meant to help validate common configuration issues.

## Security

If you discover a potential security issue in this project, or think you may have discovered a security issue, we request you to notify AWS Security via our vulnerability [reporting page](http://aws.amazon.com/security/vulnerability-reporting/). Please do not create a public GitHub issue.

