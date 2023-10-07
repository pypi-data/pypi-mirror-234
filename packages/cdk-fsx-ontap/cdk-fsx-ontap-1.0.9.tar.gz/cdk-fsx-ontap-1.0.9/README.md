# CDK FSx ONTAP

![AWS CDK Version](https://img.shields.io/badge/AWS%20CDK-v2-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

## Overview

[An AWS Cloud Development Kit (CDK) construct](https://docs.aws.amazon.com/cdk/v2/guide/constructs.html)
for deploying shared file storage using
[Amazon FSx for Netapp ONTAP](https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/what-is-fsx-ontap.html).

## Installation

* TypeScript

  ```bash
  yarn add cdk-fsx-ontap
  ```
* Python

  ```bash
  pip install cdk-fsx-ontap
  ```

## Usage

**a)** basic - going with all of the defaults

NB, check the full example in [src/examples/basic.ts](src/examples/basic.ts)

```python
declare const vpc: ec2.Vpc;
declare const securityGroupSource: ec2.SecurityGroup;

new FsxOntap(this, 'FsxOntap', {
  vpc,
  ec2SecurityGroup,
});
```

## Acknowledgements

This project utilizes [projen](https://github.com/projen/projen) (*star it on GitHub*)
and was created by following [this guide by hayao-k](https://dev.to/aws-builders/a-beginner-s-guide-to-create-aws-cdk-construct-library-with-projen-5eh4)
(*like it on Dev.to*).
