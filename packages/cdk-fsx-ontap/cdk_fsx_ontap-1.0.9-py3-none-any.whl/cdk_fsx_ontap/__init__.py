'''
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
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import constructs as _constructs_77d1e7e8


class FsxOntap(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-fsx-ontap.FsxOntap",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        security_group_source: _aws_cdk_aws_ec2_ceddda9d.SecurityGroup,
        vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
        mount_name: typing.Optional[builtins.str] = None,
        mount_path: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param security_group_source: 
        :param vpc: VPC in which the FSx for NetApp ONTAP instance will be created.
        :param mount_name: Name of the mount point. Default: '/datavol'
        :param mount_path: Path to mount the FSx for NetApp ONTAP instance. Default: '/mnt/fsx'
        :param name: Name of the FSx for NetApp ONTAP Storage Virtual Machine (SVM). Also used in resource ID creation, e.g. ``${name}-resource-type``. Default: 'fsx-ontap'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba67456b85be074102a517564724acdd0eab73e9ea51879efb03ef517f3c1da)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FsxOntapProps(
            security_group_source=security_group_source,
            vpc=vpc,
            mount_name=mount_name,
            mount_path=mount_path,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="mountName")
    def mount_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountName"))

    @builtins.property
    @jsii.member(jsii_name="mountPath")
    def mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountPath"))

    @builtins.property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsName"))


@jsii.data_type(
    jsii_type="cdk-fsx-ontap.FsxOntapProps",
    jsii_struct_bases=[],
    name_mapping={
        "security_group_source": "securityGroupSource",
        "vpc": "vpc",
        "mount_name": "mountName",
        "mount_path": "mountPath",
        "name": "name",
    },
)
class FsxOntapProps:
    def __init__(
        self,
        *,
        security_group_source: _aws_cdk_aws_ec2_ceddda9d.SecurityGroup,
        vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
        mount_name: typing.Optional[builtins.str] = None,
        mount_path: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param security_group_source: 
        :param vpc: VPC in which the FSx for NetApp ONTAP instance will be created.
        :param mount_name: Name of the mount point. Default: '/datavol'
        :param mount_path: Path to mount the FSx for NetApp ONTAP instance. Default: '/mnt/fsx'
        :param name: Name of the FSx for NetApp ONTAP Storage Virtual Machine (SVM). Also used in resource ID creation, e.g. ``${name}-resource-type``. Default: 'fsx-ontap'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75aa5b1b8039ecada0199cda77aa6f599f3191468015efca2e0a9689ccb40927)
            check_type(argname="argument security_group_source", value=security_group_source, expected_type=type_hints["security_group_source"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument mount_name", value=mount_name, expected_type=type_hints["mount_name"])
            check_type(argname="argument mount_path", value=mount_path, expected_type=type_hints["mount_path"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "security_group_source": security_group_source,
            "vpc": vpc,
        }
        if mount_name is not None:
            self._values["mount_name"] = mount_name
        if mount_path is not None:
            self._values["mount_path"] = mount_path
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def security_group_source(self) -> _aws_cdk_aws_ec2_ceddda9d.SecurityGroup:
        result = self._values.get("security_group_source")
        assert result is not None, "Required property 'security_group_source' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SecurityGroup, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.Vpc:
        '''VPC in which the FSx for NetApp ONTAP instance will be created.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Vpc, result)

    @builtins.property
    def mount_name(self) -> typing.Optional[builtins.str]:
        '''Name of the mount point.

        :default: '/datavol'
        '''
        result = self._values.get("mount_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mount_path(self) -> typing.Optional[builtins.str]:
        '''Path to mount the FSx for NetApp ONTAP instance.

        :default: '/mnt/fsx'
        '''
        result = self._values.get("mount_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the FSx for NetApp ONTAP Storage Virtual Machine (SVM).

        Also used in resource ID creation, e.g. ``${name}-resource-type``.

        :default: 'fsx-ontap'
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FsxOntapProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "FsxOntap",
    "FsxOntapProps",
]

publication.publish()

def _typecheckingstub__8ba67456b85be074102a517564724acdd0eab73e9ea51879efb03ef517f3c1da(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    security_group_source: _aws_cdk_aws_ec2_ceddda9d.SecurityGroup,
    vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
    mount_name: typing.Optional[builtins.str] = None,
    mount_path: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75aa5b1b8039ecada0199cda77aa6f599f3191468015efca2e0a9689ccb40927(
    *,
    security_group_source: _aws_cdk_aws_ec2_ceddda9d.SecurityGroup,
    vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
    mount_name: typing.Optional[builtins.str] = None,
    mount_path: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
