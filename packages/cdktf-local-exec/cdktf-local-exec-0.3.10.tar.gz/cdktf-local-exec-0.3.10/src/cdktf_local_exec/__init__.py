'''
# CDKTF Local Exec Construct

A simple construct that executes a command locally. This is useful to run build steps within your CDKTF Program or to run a post action after a resource is created.

The construct uses the null provider to achieve this so it can be trusted to only run after all dependencies are met.

## Usage

```python
import { Provider, LocalExec } from "cdktf-local-exec";

// LocalExec extends from the null provider,
// so if you already have the provider initialized you can skip this step
new Provider(this, "local-exec");

const frontend = new LocalExec(this, "frontend-build", {
  // Will copy this into an asset directory
  cwd: "/path/to/project/frontend",
  command: "npm install && npm build",
});

const pathToUpload = `${frontend.path}/dist`;

new LocalExec(this, "frontend-upload", {
  cwd: pathToUpload,
  command: `aws s3 cp --recursive ${pathToUpload} s3://${bucket.name}/frontend`,
});

new LocalExec(this, "backend-build", {
  cwd: "/path/to/project/backend",
  copyBeforeRun: false, // can not run remotely since the runner has no docker access
  command: "docker build -t foo . && docker push foo",
});
```

### Options

* `cwd`: The working directory to run the command in. It will be copied before execution to ensure the asset can be used in a remote execution environment.
* `command`: The command to execute.
* `copyBeforeRun`: If true, the command will copy the `cwd` directory into a tmp dir and run there. If false, the command will be executed in the `cwd` directory.
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
import cdktf_cdktf_provider_null.provider as _cdktf_cdktf_provider_null_provider_dc159705
import cdktf_cdktf_provider_null.resource as _cdktf_cdktf_provider_null_resource_dc159705
import constructs as _constructs_77d1e7e8


class LocalExec(
    _cdktf_cdktf_provider_null_resource_dc159705.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-local-exec.LocalExec",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        command: builtins.str,
        cwd: builtins.str,
        copy_before_run: typing.Optional[builtins.bool] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param command: The command to run.
        :param cwd: The working directory to run the command in. Defaults to process.pwd(). If copyBeforeRun is set to true it will copy the working directory to an asset directory and take that as the base to run.
        :param copy_before_run: If set to true, the working directory will be copied to an asset directory. Default: true
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param triggers: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ee226ecef9bc421745f4fb7a77da107a3128108799414818045cf62f04f035)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = LocalExecConfig(
            command=command,
            cwd=cwd,
            copy_before_run=copy_before_run,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
            triggers=triggers,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "command"))

    @command.setter
    def command(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b75c4edb6570a6af04e2652c642969f6ab144fdff697afc2b078e6c018680a58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value)

    @builtins.property
    @jsii.member(jsii_name="cwd")
    def cwd(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cwd"))

    @cwd.setter
    def cwd(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e53fe62d184119bcca645c7ccd97945acfcac4e9ac849689309f9c9543ef957)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cwd", value)


@jsii.data_type(
    jsii_type="cdktf-local-exec.LocalExecConfig",
    jsii_struct_bases=[],
    name_mapping={
        "command": "command",
        "cwd": "cwd",
        "copy_before_run": "copyBeforeRun",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "triggers": "triggers",
    },
)
class LocalExecConfig:
    def __init__(
        self,
        *,
        command: builtins.str,
        cwd: builtins.str,
        copy_before_run: typing.Optional[builtins.bool] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param command: The command to run.
        :param cwd: The working directory to run the command in. Defaults to process.pwd(). If copyBeforeRun is set to true it will copy the working directory to an asset directory and take that as the base to run.
        :param copy_before_run: If set to true, the working directory will be copied to an asset directory. Default: true
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param triggers: 
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e2cb82b5f3da5691cde851cb84a07444c060fe1756d8620ef9c9138e4e7589)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument cwd", value=cwd, expected_type=type_hints["cwd"])
            check_type(argname="argument copy_before_run", value=copy_before_run, expected_type=type_hints["copy_before_run"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument triggers", value=triggers, expected_type=type_hints["triggers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "command": command,
            "cwd": cwd,
        }
        if copy_before_run is not None:
            self._values["copy_before_run"] = copy_before_run
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if triggers is not None:
            self._values["triggers"] = triggers

    @builtins.property
    def command(self) -> builtins.str:
        '''The command to run.'''
        result = self._values.get("command")
        assert result is not None, "Required property 'command' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cwd(self) -> builtins.str:
        '''The working directory to run the command in.

        Defaults to process.pwd().
        If copyBeforeRun is set to true it will copy the working directory to an asset directory and take that as the base to run.
        '''
        result = self._values.get("cwd")
        assert result is not None, "Required property 'cwd' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def copy_before_run(self) -> typing.Optional[builtins.bool]:
        '''If set to true, the working directory will be copied to an asset directory.

        :default: true
        '''
        result = self._values.get("copy_before_run")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def triggers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("triggers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LocalExecConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NullProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-local-exec.NullProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/null/3.2.1/docs null}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/null/3.2.1/docs null} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/null/3.2.1/docs#alias NullProvider#alias}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b2def60d733396ff0f8fd3fc7a53bffd7225075875c28a2ad30bfc636484530)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = _cdktf_cdktf_provider_null_provider_dc159705.NullProviderConfig(
            alias=alias
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30bf38e7c1e5c971979b47196909bb7a08c305a26e62f5688542d5554b6e1283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value)


__all__ = [
    "LocalExec",
    "LocalExecConfig",
    "NullProvider",
]

publication.publish()

def _typecheckingstub__d4ee226ecef9bc421745f4fb7a77da107a3128108799414818045cf62f04f035(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    command: builtins.str,
    cwd: builtins.str,
    copy_before_run: typing.Optional[builtins.bool] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b75c4edb6570a6af04e2652c642969f6ab144fdff697afc2b078e6c018680a58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e53fe62d184119bcca645c7ccd97945acfcac4e9ac849689309f9c9543ef957(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e2cb82b5f3da5691cde851cb84a07444c060fe1756d8620ef9c9138e4e7589(
    *,
    command: builtins.str,
    cwd: builtins.str,
    copy_before_run: typing.Optional[builtins.bool] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2def60d733396ff0f8fd3fc7a53bffd7225075875c28a2ad30bfc636484530(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30bf38e7c1e5c971979b47196909bb7a08c305a26e62f5688542d5554b6e1283(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass
