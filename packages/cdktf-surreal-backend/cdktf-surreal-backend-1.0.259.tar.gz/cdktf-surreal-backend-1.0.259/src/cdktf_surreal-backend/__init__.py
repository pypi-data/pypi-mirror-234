'''
# cdktf-surreal-backend

This is library to create a CDKTF construct for [terraform-backend-surreal](https://github.com/awlsring/terraform-backend-surreal). This library vends a single construct, `SurrealBackend`, which extends the default `HttpBackend` construct to make instantiation of this easier.

## Usage

### Example

```python
import { TerraformStack } from "cdktf";
import { SurrealBackend } from '@awlsring/cdktf-surreal-backend';

export class MyStack extends TerraformStack {
  constructor(scope: Construct, name: string, props: MyStackProps) {
    super(scope, name);

    const backend = new SurrealBackend(this, 'Backend', {
      address: 'https://localhost:8032',
      project: "homelab",
      stack: "infra",
      username: "terraform",
      password: "alligator3",
    });

    ... // other stuff

  }
}
```

### Construct Properties:

* address: The address your backend sever is reachable at.
* project: The project name to use for this stack.
* stack: The stack name to use for this stack. stacks names must be unique across a project.
* username: The username to use for authentication, configured in the server's config.yaml file
* password: The password to use for authentication, configured in the server's config.yaml file
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

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class SurrealBackend(
    _cdktf_9a9027ec.HttpBackend,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-surreal-backend.SurrealBackend",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        address: builtins.str,
        password: builtins.str,
        project: builtins.str,
        stack: builtins.str,
        username: builtins.str,
        skip_cert_verification: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param address: 
        :param password: 
        :param project: 
        :param stack: 
        :param username: 
        :param skip_cert_verification: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13bb76e59bb29b13dba15ab0a9815fe8a06403fb63c4a5f580f98d32d453727a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = SurrealBackendProps(
            address=address,
            password=password,
            project=project,
            stack=stack,
            username=username,
            skip_cert_verification=skip_cert_verification,
        )

        jsii.create(self.__class__, self, [scope, props])


@jsii.data_type(
    jsii_type="@awlsring/cdktf-surreal-backend.SurrealBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "password": "password",
        "project": "project",
        "stack": "stack",
        "username": "username",
        "skip_cert_verification": "skipCertVerification",
    },
)
class SurrealBackendProps:
    def __init__(
        self,
        *,
        address: builtins.str,
        password: builtins.str,
        project: builtins.str,
        stack: builtins.str,
        username: builtins.str,
        skip_cert_verification: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param address: 
        :param password: 
        :param project: 
        :param stack: 
        :param username: 
        :param skip_cert_verification: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95edd12545333394817e862899c7fb3eeb63a129a08e853d65adb2399094b87d)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument skip_cert_verification", value=skip_cert_verification, expected_type=type_hints["skip_cert_verification"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address": address,
            "password": password,
            "project": project,
            "stack": stack,
            "username": username,
        }
        if skip_cert_verification is not None:
            self._values["skip_cert_verification"] = skip_cert_verification

    @builtins.property
    def address(self) -> builtins.str:
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stack(self) -> builtins.str:
        result = self._values.get("stack")
        assert result is not None, "Required property 'stack' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def skip_cert_verification(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("skip_cert_verification")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SurrealBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SurrealBackend",
    "SurrealBackendProps",
]

publication.publish()

def _typecheckingstub__13bb76e59bb29b13dba15ab0a9815fe8a06403fb63c4a5f580f98d32d453727a(
    scope: _constructs_77d1e7e8.Construct,
    *,
    address: builtins.str,
    password: builtins.str,
    project: builtins.str,
    stack: builtins.str,
    username: builtins.str,
    skip_cert_verification: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95edd12545333394817e862899c7fb3eeb63a129a08e853d65adb2399094b87d(
    *,
    address: builtins.str,
    password: builtins.str,
    project: builtins.str,
    stack: builtins.str,
    username: builtins.str,
    skip_cert_verification: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
