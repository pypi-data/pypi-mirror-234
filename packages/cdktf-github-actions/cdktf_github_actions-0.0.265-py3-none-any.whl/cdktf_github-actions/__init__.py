'''
# cdktf-github-actions

This is a library to help define GitHub Actions workflows using CDKTF. This package vends constructs for defining a workflow that will be synthesized to a workflow yaml file in your repos `.github/workflows` directory.

## Development

This project is in early development. The constructs are likely to change as the needs of the project evolve.

A few items I'm currently working towards:

* [ ] More github resource synthesis
* [ ] Higher test coverage
* [ ] More indepth documentation

## Usage

### Example

```python
import { Construct } from 'constructs';
import { App, TerraformStack } from 'cdktf';
import { Workflow, Job } from 'cdktf-github-actions';

const app = new App();

class MyWorkflowStack executes TerraformStack {
  constructor(scope: Construct, name: string) {
    super(scope, name);

    let echoJob = new Job(this, 'build-job', {
      steps: [
        {
          name: 'echo',
          run: 'echo "Hello World"',
        },
      ],
    });

    const wf = new Workflow(this, 'workflow', {
      repoName: 'my-repo',
      jobs: [echoJob],
    });
  }
}

const stack = new MyWorkflowStack(app, 'test');
app.synth();
```

The constructs support the ability to define github resources and create them using the github terrafrom provider. The following example shows how to create a create a workflow with secrets that will be stored in the repository.

```python
import { Construct } from 'constructs';
import { App, TerraformStack } from 'cdktf';
import { Workflow, Job } from 'cdktf-github-actions';

const app = new App();

class MyWorkflowStack executes TerraformStack {
  constructor(scope: Construct, name: string) {
    super(scope, name);

    let echoJob = new Job(this, 'build-job', {
      steps: [
        {
          name: 'echo',
          run: 'echo "Hello World"',
          withSecrets: [
            {
              referencedName: 'token',
              secretName: 'MY_SECRET',
              secretValue: '123',
            },
          ],
        },
      ],
    });

    const wf = new Workflow(this, 'workflow', {
      repoName: 'my-repo',
      jobs: [echoJob],
    });
  }
}

const stack = new MyWorkflowStack(app, 'test');
app.synth();
```

The example above will create a secret with the name `MY_SECRET` and the value `123` in the repository. The secret will be referenced in the workflow using the name `token`.
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

import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.CheckRunOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class CheckRunOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Check run options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a782937bdfd03983584e034e91a80976debda0e536104d007aa603f963deff6)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckRunOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.CheckSuiteOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class CheckSuiteOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Check suite options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fe01942fe47c9f0a94235d83068102bc515d036b148677788d732f4a804c275)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckSuiteOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.ContainerCredentials",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class ContainerCredentials:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''Credentials to use to authenticate to Docker registries.

        :param password: The password.
        :param username: The username.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80112d00c9e6ad87669cddb60f24db7f28616ab8f6e5a592e0566dc4604e2004)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''The password.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''The username.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.ContainerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "credentials": "credentials",
        "env": "env",
        "options": "options",
        "ports": "ports",
        "volumes": "volumes",
    },
)
class ContainerOptions:
    def __init__(
        self,
        *,
        image: builtins.str,
        credentials: typing.Optional[typing.Union[ContainerCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        options: typing.Optional[typing.Sequence[builtins.str]] = None,
        ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
        volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Options petaining to container environments.

        :param image: The Docker image to use as the container to run the action. The value can be the Docker Hub image name or a registry name.
        :param credentials: f the image's container registry requires authentication to pull the image, you can use credentials to set a map of the username and password. The credentials are the same values that you would provide to the docker login command.
        :param env: Sets a map of environment variables in the container.
        :param options: Additional Docker container resource options.
        :param ports: Sets an array of ports to expose on the container.
        :param volumes: Sets an array of volumes for the container to use. You can use volumes to share data between services or other steps in a job. You can specify named Docker volumes, anonymous Docker volumes, or bind mounts on the host. To specify a volume, you specify the source and destination path: ``<source>:<destinationPath>``.
        '''
        if isinstance(credentials, dict):
            credentials = ContainerCredentials(**credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d6461d95341b2a11e0667c65e2f7ecb33f23ba2487725caf3fd46e5e5fd3095)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if credentials is not None:
            self._values["credentials"] = credentials
        if env is not None:
            self._values["env"] = env
        if options is not None:
            self._values["options"] = options
        if ports is not None:
            self._values["ports"] = ports
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def image(self) -> builtins.str:
        '''The Docker image to use as the container to run the action.

        The value can
        be the Docker Hub image name or a registry name.
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def credentials(self) -> typing.Optional[ContainerCredentials]:
        '''f the image's container registry requires authentication to pull the image, you can use credentials to set a map of the username and password.

        The credentials are the same values that you would provide to the docker
        login command.
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[ContainerCredentials], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Sets a map of environment variables in the container.'''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional Docker container resource options.

        :see: https://docs.docker.com/engine/reference/commandline/create/#options
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Sets an array of ports to expose on the container.'''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Sets an array of volumes for the container to use.

        You can use volumes to
        share data between services or other steps in a job. You can specify
        named Docker volumes, anonymous Docker volumes, or bind mounts on the
        host.

        To specify a volume, you specify the source and destination path:
        ``<source>:<destinationPath>``.
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.CreateOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class CreateOptions:
    def __init__(self) -> None:
        '''The Create event accepts no options.'''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CreateOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.CronScheduleOptions",
    jsii_struct_bases=[],
    name_mapping={"cron": "cron"},
)
class CronScheduleOptions:
    def __init__(self, *, cron: builtins.str) -> None:
        '''CRON schedule options.

        :param cron: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05e75a13596a5b83e96255c41ac6916da833bb277e30081dbebc4e9454e2d744)
            check_type(argname="argument cron", value=cron, expected_type=type_hints["cron"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cron": cron,
        }

    @builtins.property
    def cron(self) -> builtins.str:
        '''
        :see: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html#tag_20_25_07
        '''
        result = self._values.get("cron")
        assert result is not None, "Required property 'cron' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronScheduleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.DeleteOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DeleteOptions:
    def __init__(self) -> None:
        '''The Delete event accepts no options.'''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeleteOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.DeploymentOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DeploymentOptions:
    def __init__(self) -> None:
        '''The Deployment event accepts no options.'''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeploymentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.DeploymentStatusOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DeploymentStatusOptions:
    def __init__(self) -> None:
        '''The Deployment status event accepts no options.'''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeploymentStatusOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.ForkOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class ForkOptions:
    def __init__(self) -> None:
        '''The Fork event accepts no options.'''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ForkOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.GollumOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GollumOptions:
    def __init__(self) -> None:
        '''The Gollum event accepts no options.'''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GollumOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.IssueCommentOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class IssueCommentOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Issue comment options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d46103d6dcd8cc3a19adacec36642c7fb86439c841bcde588fb00068801b38)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IssueCommentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.IssuesOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class IssuesOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Issues options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4be6353a13832066a3671838515ee8b07932d4f07cf3006569cb73149a65186)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IssuesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Job(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-github-actions.Job",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        steps: typing.Sequence[typing.Union["JobStep", typing.Dict[builtins.str, typing.Any]]],
        concurrency: typing.Any = None,
        container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union["JobDefaults", typing.Dict[builtins.str, typing.Any]]] = None,
        depends_on: typing.Optional[typing.Sequence["Job"]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Any = None,
        job_referene_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        permissions: typing.Optional[typing.Union["JobPermissions", typing.Dict[builtins.str, typing.Any]]] = None,
        run_if: typing.Optional[builtins.str] = None,
        runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        strategy: typing.Optional[typing.Union["JobStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param steps: 
        :param concurrency: 
        :param container: 
        :param continue_on_error: 
        :param defaults: 
        :param depends_on: 
        :param env: 
        :param environment: 
        :param job_referene_name: 
        :param name: 
        :param outputs: 
        :param permissions: 
        :param run_if: 
        :param runs_on: 
        :param services: 
        :param strategy: 
        :param timeout_minutes: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be21f04638b9906cec654e3f713ef2d8f7e5c2e530067c866cf02adf881e55f2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = JobProps(
            steps=steps,
            concurrency=concurrency,
            container=container,
            continue_on_error=continue_on_error,
            defaults=defaults,
            depends_on=depends_on,
            env=env,
            environment=environment,
            job_referene_name=job_referene_name,
            name=name,
            outputs=outputs,
            permissions=permissions,
            run_if=run_if,
            runs_on=runs_on,
            services=services,
            strategy=strategy,
            timeout_minutes=timeout_minutes,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, job: "Job") -> None:
        '''
        :param job: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e057c955095553b0383af68f3b57537ad24cf6a41453497377a1d37c59e357d)
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
        return typing.cast(None, jsii.invoke(self, "addDependency", [job]))

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> "JobData":
        return typing.cast("JobData", jsii.invoke(self, "toObject", []))

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dependsOn"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> "JobPermissions":
        return typing.cast("JobPermissions", jsii.get(self, "permissions"))

    @builtins.property
    @jsii.member(jsii_name="runsOn")
    def runs_on(self) -> typing.Union[builtins.str, typing.List[builtins.str]]:
        return typing.cast(typing.Union[builtins.str, typing.List[builtins.str]], jsii.get(self, "runsOn"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> typing.List["SecretsOptions"]:
        return typing.cast(typing.List["SecretsOptions"], jsii.get(self, "secrets"))

    @builtins.property
    @jsii.member(jsii_name="steps")
    def steps(self) -> typing.List["JobStep"]:
        return typing.cast(typing.List["JobStep"], jsii.get(self, "steps"))

    @builtins.property
    @jsii.member(jsii_name="timeoutMinutes")
    def timeout_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutMinutes"))

    @builtins.property
    @jsii.member(jsii_name="concurrency")
    def concurrency(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "concurrency"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> typing.Optional[ContainerOptions]:
        return typing.cast(typing.Optional[ContainerOptions], jsii.get(self, "container"))

    @builtins.property
    @jsii.member(jsii_name="continueOnError")
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "continueOnError"))

    @builtins.property
    @jsii.member(jsii_name="defaults")
    def defaults(self) -> typing.Optional["JobDefaults"]:
        return typing.cast(typing.Optional["JobDefaults"], jsii.get(self, "defaults"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="runIf")
    def run_if(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runIf"))

    @builtins.property
    @jsii.member(jsii_name="services")
    def services(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ContainerOptions]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, ContainerOptions]], jsii.get(self, "services"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def strategy(self) -> typing.Optional["JobStrategy"]:
        return typing.cast(typing.Optional["JobStrategy"], jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.JobData",
    jsii_struct_bases=[],
    name_mapping={
        "permissions": "permissions",
        "runs_on": "runsOn",
        "steps": "steps",
        "concurrency": "concurrency",
        "container": "container",
        "continue_on_error": "continueOnError",
        "defaults": "defaults",
        "env": "env",
        "environment": "environment",
        "if_": "if",
        "name": "name",
        "needs": "needs",
        "outputs": "outputs",
        "services": "services",
        "strategy": "strategy",
        "timeout_minutes": "timeoutMinutes",
    },
)
class JobData:
    def __init__(
        self,
        *,
        permissions: typing.Union["JobPermissions", typing.Dict[builtins.str, typing.Any]],
        runs_on: typing.Union[builtins.str, typing.Sequence[builtins.str]],
        steps: typing.Sequence[typing.Union["JobStepData", typing.Dict[builtins.str, typing.Any]]],
        concurrency: typing.Any = None,
        container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union["JobDefaults", typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Any = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        strategy: typing.Optional[typing.Union["JobStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''A GitHub Workflow job definition.

        :param permissions: You can modify the default permissions granted to the GITHUB_TOKEN, adding or removing access as required, so that you only allow the minimum required access. Use ``{ contents: READ }`` if your job only needs to clone code. This is intentionally a required field since it is required in order to allow workflows to run in GitHub repositories with restricted default access.
        :param runs_on: The type of machine to run the job on. The machine can be either a GitHub-hosted runner or a self-hosted runner.
        :param steps: A job contains a sequence of tasks called steps. Steps can run commands, run setup tasks, or run an action in your repository, a public repository, or an action published in a Docker registry. Not all steps run actions, but all actions run as a step. Each step runs in its own process in the runner environment and has access to the workspace and filesystem. Because steps run in their own process, changes to environment variables are not preserved between steps. GitHub provides built-in steps to set up and complete a job.
        :param concurrency: (experimental) Concurrency ensures that only a single job or workflow using the same concurrency group will run at a time. A concurrency group can be any string or expression. The expression can use any context except for the secrets context.
        :param container: A container to run any steps in a job that don't already specify a container. If you have steps that use both script and container actions, the container actions will run as sibling containers on the same network with the same volume mounts.
        :param continue_on_error: Prevents a workflow run from failing when a job fails. Set to true to allow a workflow run to pass when this job fails.
        :param defaults: A map of default settings that will apply to all steps in the job. You can also set default settings for the entire workflow.
        :param env: A map of environment variables that are available to all steps in the job. You can also set environment variables for the entire workflow or an individual step.
        :param environment: The environment that the job references. All environment protection rules must pass before a job referencing the environment is sent to a runner.
        :param if_: You can use the if conditional to prevent a job from running unless a condition is met. You can use any supported context and expression to create a conditional.
        :param name: The name of the job displayed on GitHub.
        :param needs: Identifies any jobs that must complete successfully before this job will run. It can be a string or array of strings. If a job fails, all jobs that need it are skipped unless the jobs use a conditional expression that causes the job to continue.
        :param outputs: A map of outputs for a job. Job outputs are available to all downstream jobs that depend on this job.
        :param services: Used to host service containers for a job in a workflow. Service containers are useful for creating databases or cache services like Redis. The runner automatically creates a Docker network and manages the life cycle of the service containers.
        :param strategy: A strategy creates a build matrix for your jobs. You can define different variations to run each job in.
        :param timeout_minutes: The maximum number of minutes to let a job run before GitHub automatically cancels it. Default: 360
        '''
        if isinstance(permissions, dict):
            permissions = JobPermissions(**permissions)
        if isinstance(container, dict):
            container = ContainerOptions(**container)
        if isinstance(defaults, dict):
            defaults = JobDefaults(**defaults)
        if isinstance(strategy, dict):
            strategy = JobStrategy(**strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb4186255cabb20b2161c41788f309a468babdf2e0c103969ab7f287ffcc2c0d)
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument runs_on", value=runs_on, expected_type=type_hints["runs_on"])
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
            check_type(argname="argument concurrency", value=concurrency, expected_type=type_hints["concurrency"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument continue_on_error", value=continue_on_error, expected_type=type_hints["continue_on_error"])
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
            check_type(argname="argument outputs", value=outputs, expected_type=type_hints["outputs"])
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "permissions": permissions,
            "runs_on": runs_on,
            "steps": steps,
        }
        if concurrency is not None:
            self._values["concurrency"] = concurrency
        if container is not None:
            self._values["container"] = container
        if continue_on_error is not None:
            self._values["continue_on_error"] = continue_on_error
        if defaults is not None:
            self._values["defaults"] = defaults
        if env is not None:
            self._values["env"] = env
        if environment is not None:
            self._values["environment"] = environment
        if if_ is not None:
            self._values["if_"] = if_
        if name is not None:
            self._values["name"] = name
        if needs is not None:
            self._values["needs"] = needs
        if outputs is not None:
            self._values["outputs"] = outputs
        if services is not None:
            self._values["services"] = services
        if strategy is not None:
            self._values["strategy"] = strategy
        if timeout_minutes is not None:
            self._values["timeout_minutes"] = timeout_minutes

    @builtins.property
    def permissions(self) -> "JobPermissions":
        '''You can modify the default permissions granted to the GITHUB_TOKEN, adding or removing access as required, so that you only allow the minimum required access.

        Use ``{ contents: READ }`` if your job only needs to clone code.

        This is intentionally a required field since it is required in order to
        allow workflows to run in GitHub repositories with restricted default
        access.

        :see: https://docs.github.com/en/actions/reference/authentication-in-a-workflow#permissions-for-the-github_token
        '''
        result = self._values.get("permissions")
        assert result is not None, "Required property 'permissions' is missing"
        return typing.cast("JobPermissions", result)

    @builtins.property
    def runs_on(self) -> typing.Union[builtins.str, typing.List[builtins.str]]:
        '''The type of machine to run the job on.

        The machine can be either a
        GitHub-hosted runner or a self-hosted runner.

        Example::

            ["ubuntu-latest"]
        '''
        result = self._values.get("runs_on")
        assert result is not None, "Required property 'runs_on' is missing"
        return typing.cast(typing.Union[builtins.str, typing.List[builtins.str]], result)

    @builtins.property
    def steps(self) -> typing.List["JobStepData"]:
        '''A job contains a sequence of tasks called steps.

        Steps can run commands,
        run setup tasks, or run an action in your repository, a public repository,
        or an action published in a Docker registry. Not all steps run actions,
        but all actions run as a step. Each step runs in its own process in the
        runner environment and has access to the workspace and filesystem.
        Because steps run in their own process, changes to environment variables
        are not preserved between steps. GitHub provides built-in steps to set up
        and complete a job.
        '''
        result = self._values.get("steps")
        assert result is not None, "Required property 'steps' is missing"
        return typing.cast(typing.List["JobStepData"], result)

    @builtins.property
    def concurrency(self) -> typing.Any:
        '''(experimental) Concurrency ensures that only a single job or workflow using the same concurrency group will run at a time.

        A concurrency group can be any
        string or expression. The expression can use any context except for the
        secrets context.

        :stability: experimental
        '''
        result = self._values.get("concurrency")
        return typing.cast(typing.Any, result)

    @builtins.property
    def container(self) -> typing.Optional[ContainerOptions]:
        '''A container to run any steps in a job that don't already specify a container.

        If you have steps that use both script and container actions,
        the container actions will run as sibling containers on the same network
        with the same volume mounts.
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[ContainerOptions], result)

    @builtins.property
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        '''Prevents a workflow run from failing when a job fails.

        Set to true to
        allow a workflow run to pass when this job fails.
        '''
        result = self._values.get("continue_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def defaults(self) -> typing.Optional["JobDefaults"]:
        '''A map of default settings that will apply to all steps in the job.

        You
        can also set default settings for the entire workflow.
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional["JobDefaults"], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of environment variables that are available to all steps in the job.

        You can also set environment variables for the entire workflow or an
        individual step.
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Any:
        '''The environment that the job references.

        All environment protection rules
        must pass before a job referencing the environment is sent to a runner.

        :see: https://docs.github.com/en/actions/reference/environments
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Any, result)

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        '''You can use the if conditional to prevent a job from running unless a condition is met.

        You can use any supported context and expression to
        create a conditional.
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the job displayed on GitHub.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def needs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Identifies any jobs that must complete successfully before this job will run.

        It can be a string or array of strings. If a job fails, all jobs
        that need it are skipped unless the jobs use a conditional expression
        that causes the job to continue.
        '''
        result = self._values.get("needs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def outputs(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of outputs for a job.

        Job outputs are available to all downstream
        jobs that depend on this job.
        '''
        result = self._values.get("outputs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def services(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ContainerOptions]]:
        '''Used to host service containers for a job in a workflow.

        Service
        containers are useful for creating databases or cache services like Redis.
        The runner automatically creates a Docker network and manages the life
        cycle of the service containers.
        '''
        result = self._values.get("services")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, ContainerOptions]], result)

    @builtins.property
    def strategy(self) -> typing.Optional["JobStrategy"]:
        '''A strategy creates a build matrix for your jobs.

        You can define different
        variations to run each job in.
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional["JobStrategy"], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of minutes to let a job run before GitHub automatically cancels it.

        :default: 360
        '''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.JobDefaults",
    jsii_struct_bases=[],
    name_mapping={"run": "run"},
)
class JobDefaults:
    def __init__(
        self,
        *,
        run: typing.Optional[typing.Union["RunSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Default settings for all steps in the job.

        :param run: Default run settings.
        '''
        if isinstance(run, dict):
            run = RunSettings(**run)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__602b6d9483733a9a57aade72d7cc2dee06cf9a12317aae233cd4090b4c915627)
            check_type(argname="argument run", value=run, expected_type=type_hints["run"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if run is not None:
            self._values["run"] = run

    @builtins.property
    def run(self) -> typing.Optional["RunSettings"]:
        '''Default run settings.'''
        result = self._values.get("run")
        return typing.cast(typing.Optional["RunSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobDefaults(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.JobMatrix",
    jsii_struct_bases=[],
    name_mapping={"domain": "domain", "exclude": "exclude", "include": "include"},
)
class JobMatrix:
    def __init__(
        self,
        *,
        domain: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
        exclude: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, builtins.str]]] = None,
        include: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        '''A job matrix.

        :param domain: Each option you define in the matrix has a key and value. The keys you define become properties in the matrix context and you can reference the property in other areas of your workflow file. For example, if you define the key os that contains an array of operating systems, you can use the matrix.os property as the value of the runs-on keyword to create a job for each operating system.
        :param exclude: You can remove a specific configurations defined in the build matrix using the exclude option. Using exclude removes a job defined by the build matrix.
        :param include: You can add additional configuration options to a build matrix job that already exists. For example, if you want to use a specific version of npm when the job that uses windows-latest and version 8 of node runs, you can use include to specify that additional option.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e75f9de38d013acb438dd6100f3e72a51ecfda4438e6eb335d21dde85a48e6a)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain is not None:
            self._values["domain"] = domain
        if exclude is not None:
            self._values["exclude"] = exclude
        if include is not None:
            self._values["include"] = include

    @builtins.property
    def domain(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]]:
        '''Each option you define in the matrix has a key and value.

        The keys you
        define become properties in the matrix context and you can reference the
        property in other areas of your workflow file. For example, if you define
        the key os that contains an array of operating systems, you can use the
        matrix.os property as the value of the runs-on keyword to create a job
        for each operating system.
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]], result)

    @builtins.property
    def exclude(
        self,
    ) -> typing.Optional[typing.List[typing.Mapping[builtins.str, builtins.str]]]:
        '''You can remove a specific configurations defined in the build matrix using the exclude option.

        Using exclude removes a job defined by the
        build matrix.
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def include(
        self,
    ) -> typing.Optional[typing.List[typing.Mapping[builtins.str, builtins.str]]]:
        '''You can add additional configuration options to a build matrix job that already exists.

        For example, if you want to use a specific version of npm
        when the job that uses windows-latest and version 8 of node runs, you can
        use include to specify that additional option.
        '''
        result = self._values.get("include")
        return typing.cast(typing.Optional[typing.List[typing.Mapping[builtins.str, builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobMatrix(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@awlsring/cdktf-github-actions.JobPermission")
class JobPermission(enum.Enum):
    '''Access level for workflow permission scopes.'''

    READ = "READ"
    '''Read-only access.'''
    WRITE = "WRITE"
    '''Read-write access.'''
    NONE = "NONE"
    '''No access at all.'''


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.JobPermissions",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "checks": "checks",
        "contents": "contents",
        "deployments": "deployments",
        "discussions": "discussions",
        "id_token": "idToken",
        "issues": "issues",
        "packages": "packages",
        "pull_requests": "pullRequests",
        "repository_projects": "repositoryProjects",
        "security_events": "securityEvents",
        "statuses": "statuses",
    },
)
class JobPermissions:
    def __init__(
        self,
        *,
        actions: typing.Optional[JobPermission] = None,
        checks: typing.Optional[JobPermission] = None,
        contents: typing.Optional[JobPermission] = None,
        deployments: typing.Optional[JobPermission] = None,
        discussions: typing.Optional[JobPermission] = None,
        id_token: typing.Optional[JobPermission] = None,
        issues: typing.Optional[JobPermission] = None,
        packages: typing.Optional[JobPermission] = None,
        pull_requests: typing.Optional[JobPermission] = None,
        repository_projects: typing.Optional[JobPermission] = None,
        security_events: typing.Optional[JobPermission] = None,
        statuses: typing.Optional[JobPermission] = None,
    ) -> None:
        '''The available scopes and access values for workflow permissions.

        If you
        specify the access for any of these scopes, all those that are not
        specified are set to ``JobPermission.NONE``, instead of the default behavior
        when none is specified.

        :param actions: 
        :param checks: 
        :param contents: 
        :param deployments: 
        :param discussions: 
        :param id_token: 
        :param issues: 
        :param packages: 
        :param pull_requests: 
        :param repository_projects: 
        :param security_events: 
        :param statuses: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4570cf024ce9e959d0e6f37e592a91aad5b667f49707c3623b2aabdad9e6b2a3)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument checks", value=checks, expected_type=type_hints["checks"])
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument deployments", value=deployments, expected_type=type_hints["deployments"])
            check_type(argname="argument discussions", value=discussions, expected_type=type_hints["discussions"])
            check_type(argname="argument id_token", value=id_token, expected_type=type_hints["id_token"])
            check_type(argname="argument issues", value=issues, expected_type=type_hints["issues"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument pull_requests", value=pull_requests, expected_type=type_hints["pull_requests"])
            check_type(argname="argument repository_projects", value=repository_projects, expected_type=type_hints["repository_projects"])
            check_type(argname="argument security_events", value=security_events, expected_type=type_hints["security_events"])
            check_type(argname="argument statuses", value=statuses, expected_type=type_hints["statuses"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if checks is not None:
            self._values["checks"] = checks
        if contents is not None:
            self._values["contents"] = contents
        if deployments is not None:
            self._values["deployments"] = deployments
        if discussions is not None:
            self._values["discussions"] = discussions
        if id_token is not None:
            self._values["id_token"] = id_token
        if issues is not None:
            self._values["issues"] = issues
        if packages is not None:
            self._values["packages"] = packages
        if pull_requests is not None:
            self._values["pull_requests"] = pull_requests
        if repository_projects is not None:
            self._values["repository_projects"] = repository_projects
        if security_events is not None:
            self._values["security_events"] = security_events
        if statuses is not None:
            self._values["statuses"] = statuses

    @builtins.property
    def actions(self) -> typing.Optional[JobPermission]:
        result = self._values.get("actions")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def checks(self) -> typing.Optional[JobPermission]:
        result = self._values.get("checks")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def contents(self) -> typing.Optional[JobPermission]:
        result = self._values.get("contents")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def deployments(self) -> typing.Optional[JobPermission]:
        result = self._values.get("deployments")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def discussions(self) -> typing.Optional[JobPermission]:
        result = self._values.get("discussions")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def id_token(self) -> typing.Optional[JobPermission]:
        result = self._values.get("id_token")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def issues(self) -> typing.Optional[JobPermission]:
        result = self._values.get("issues")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def packages(self) -> typing.Optional[JobPermission]:
        result = self._values.get("packages")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def pull_requests(self) -> typing.Optional[JobPermission]:
        result = self._values.get("pull_requests")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def repository_projects(self) -> typing.Optional[JobPermission]:
        result = self._values.get("repository_projects")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def security_events(self) -> typing.Optional[JobPermission]:
        result = self._values.get("security_events")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def statuses(self) -> typing.Optional[JobPermission]:
        result = self._values.get("statuses")
        return typing.cast(typing.Optional[JobPermission], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobPermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.JobProps",
    jsii_struct_bases=[],
    name_mapping={
        "steps": "steps",
        "concurrency": "concurrency",
        "container": "container",
        "continue_on_error": "continueOnError",
        "defaults": "defaults",
        "depends_on": "dependsOn",
        "env": "env",
        "environment": "environment",
        "job_referene_name": "jobRefereneName",
        "name": "name",
        "outputs": "outputs",
        "permissions": "permissions",
        "run_if": "runIf",
        "runs_on": "runsOn",
        "services": "services",
        "strategy": "strategy",
        "timeout_minutes": "timeoutMinutes",
    },
)
class JobProps:
    def __init__(
        self,
        *,
        steps: typing.Sequence[typing.Union["JobStep", typing.Dict[builtins.str, typing.Any]]],
        concurrency: typing.Any = None,
        container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union[JobDefaults, typing.Dict[builtins.str, typing.Any]]] = None,
        depends_on: typing.Optional[typing.Sequence[Job]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Any = None,
        job_referene_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        permissions: typing.Optional[typing.Union[JobPermissions, typing.Dict[builtins.str, typing.Any]]] = None,
        run_if: typing.Optional[builtins.str] = None,
        runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        strategy: typing.Optional[typing.Union["JobStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param steps: 
        :param concurrency: 
        :param container: 
        :param continue_on_error: 
        :param defaults: 
        :param depends_on: 
        :param env: 
        :param environment: 
        :param job_referene_name: 
        :param name: 
        :param outputs: 
        :param permissions: 
        :param run_if: 
        :param runs_on: 
        :param services: 
        :param strategy: 
        :param timeout_minutes: 
        '''
        if isinstance(container, dict):
            container = ContainerOptions(**container)
        if isinstance(defaults, dict):
            defaults = JobDefaults(**defaults)
        if isinstance(permissions, dict):
            permissions = JobPermissions(**permissions)
        if isinstance(strategy, dict):
            strategy = JobStrategy(**strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea95168c7557d23f4c6321ca3edaecafcbec637a3d6a88bc857045eff5b16581)
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
            check_type(argname="argument concurrency", value=concurrency, expected_type=type_hints["concurrency"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument continue_on_error", value=continue_on_error, expected_type=type_hints["continue_on_error"])
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument job_referene_name", value=job_referene_name, expected_type=type_hints["job_referene_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument outputs", value=outputs, expected_type=type_hints["outputs"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument run_if", value=run_if, expected_type=type_hints["run_if"])
            check_type(argname="argument runs_on", value=runs_on, expected_type=type_hints["runs_on"])
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "steps": steps,
        }
        if concurrency is not None:
            self._values["concurrency"] = concurrency
        if container is not None:
            self._values["container"] = container
        if continue_on_error is not None:
            self._values["continue_on_error"] = continue_on_error
        if defaults is not None:
            self._values["defaults"] = defaults
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if env is not None:
            self._values["env"] = env
        if environment is not None:
            self._values["environment"] = environment
        if job_referene_name is not None:
            self._values["job_referene_name"] = job_referene_name
        if name is not None:
            self._values["name"] = name
        if outputs is not None:
            self._values["outputs"] = outputs
        if permissions is not None:
            self._values["permissions"] = permissions
        if run_if is not None:
            self._values["run_if"] = run_if
        if runs_on is not None:
            self._values["runs_on"] = runs_on
        if services is not None:
            self._values["services"] = services
        if strategy is not None:
            self._values["strategy"] = strategy
        if timeout_minutes is not None:
            self._values["timeout_minutes"] = timeout_minutes

    @builtins.property
    def steps(self) -> typing.List["JobStep"]:
        result = self._values.get("steps")
        assert result is not None, "Required property 'steps' is missing"
        return typing.cast(typing.List["JobStep"], result)

    @builtins.property
    def concurrency(self) -> typing.Any:
        result = self._values.get("concurrency")
        return typing.cast(typing.Any, result)

    @builtins.property
    def container(self) -> typing.Optional[ContainerOptions]:
        result = self._values.get("container")
        return typing.cast(typing.Optional[ContainerOptions], result)

    @builtins.property
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("continue_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def defaults(self) -> typing.Optional[JobDefaults]:
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[JobDefaults], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[Job]]:
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[Job]], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Any:
        result = self._values.get("environment")
        return typing.cast(typing.Any, result)

    @builtins.property
    def job_referene_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("job_referene_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outputs(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("outputs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def permissions(self) -> typing.Optional[JobPermissions]:
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[JobPermissions], result)

    @builtins.property
    def run_if(self) -> typing.Optional[builtins.str]:
        result = self._values.get("run_if")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runs_on(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]]:
        result = self._values.get("runs_on")
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]], result)

    @builtins.property
    def services(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ContainerOptions]]:
        result = self._values.get("services")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, ContainerOptions]], result)

    @builtins.property
    def strategy(self) -> typing.Optional["JobStrategy"]:
        result = self._values.get("strategy")
        return typing.cast(typing.Optional["JobStrategy"], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.JobStepData",
    jsii_struct_bases=[],
    name_mapping={
        "continue_on_error": "continueOnError",
        "env": "env",
        "id": "id",
        "if_": "if",
        "name": "name",
        "run": "run",
        "timeout_minutes": "timeoutMinutes",
        "uses": "uses",
        "with_": "with",
    },
)
class JobStepData:
    def __init__(
        self,
        *,
        continue_on_error: typing.Optional[builtins.bool] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        run: typing.Optional[builtins.str] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
        uses: typing.Optional[builtins.str] = None,
        with_: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''A job step.

        :param continue_on_error: Prevents a job from failing when a step fails. Set to true to allow a job to pass when this step fails.
        :param env: Sets environment variables for steps to use in the runner environment. You can also set environment variables for the entire workflow or a job.
        :param id: A unique identifier for the step. You can use the id to reference the step in contexts.
        :param if_: You can use the if conditional to prevent a job from running unless a condition is met. You can use any supported context and expression to create a conditional.
        :param name: A name for your step to display on GitHub.
        :param run: Runs command-line programs using the operating system's shell. If you do not provide a name, the step name will default to the text specified in the run command.
        :param timeout_minutes: The maximum number of minutes to run the step before killing the process.
        :param uses: Selects an action to run as part of a step in your job. An action is a reusable unit of code. You can use an action defined in the same repository as the workflow, a public repository, or in a published Docker container image.
        :param with_: A map of the input parameters defined by the action. Each input parameter is a key/value pair. Input parameters are set as environment variables. The variable is prefixed with INPUT_ and converted to upper case.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__376a7046dcae820e8505bb15110e912cd78ebac8f065da00158a60c775d0ddf0)
            check_type(argname="argument continue_on_error", value=continue_on_error, expected_type=type_hints["continue_on_error"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument run", value=run, expected_type=type_hints["run"])
            check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
            check_type(argname="argument uses", value=uses, expected_type=type_hints["uses"])
            check_type(argname="argument with_", value=with_, expected_type=type_hints["with_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if continue_on_error is not None:
            self._values["continue_on_error"] = continue_on_error
        if env is not None:
            self._values["env"] = env
        if id is not None:
            self._values["id"] = id
        if if_ is not None:
            self._values["if_"] = if_
        if name is not None:
            self._values["name"] = name
        if run is not None:
            self._values["run"] = run
        if timeout_minutes is not None:
            self._values["timeout_minutes"] = timeout_minutes
        if uses is not None:
            self._values["uses"] = uses
        if with_ is not None:
            self._values["with_"] = with_

    @builtins.property
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        '''Prevents a job from failing when a step fails.

        Set to true to allow a job
        to pass when this step fails.
        '''
        result = self._values.get("continue_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Sets environment variables for steps to use in the runner environment.

        You can also set environment variables for the entire workflow or a job.
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''A unique identifier for the step.

        You can use the id to reference the
        step in contexts.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        '''You can use the if conditional to prevent a job from running unless a condition is met.

        You can use any supported context and expression to
        create a conditional.
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for your step to display on GitHub.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run(self) -> typing.Optional[builtins.str]:
        '''Runs command-line programs using the operating system's shell.

        If you do
        not provide a name, the step name will default to the text specified in
        the run command.
        '''
        result = self._values.get("run")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of minutes to run the step before killing the process.'''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def uses(self) -> typing.Optional[builtins.str]:
        '''Selects an action to run as part of a step in your job.

        An action is a
        reusable unit of code. You can use an action defined in the same
        repository as the workflow, a public repository, or in a published Docker
        container image.
        '''
        result = self._values.get("uses")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def with_(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''A map of the input parameters defined by the action.

        Each input parameter
        is a key/value pair. Input parameters are set as environment variables.
        The variable is prefixed with INPUT_ and converted to upper case.
        '''
        result = self._values.get("with_")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobStepData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.JobStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "fail_fast": "failFast",
        "matrix": "matrix",
        "max_parallel": "maxParallel",
    },
)
class JobStrategy:
    def __init__(
        self,
        *,
        fail_fast: typing.Optional[builtins.bool] = None,
        matrix: typing.Optional[typing.Union[JobMatrix, typing.Dict[builtins.str, typing.Any]]] = None,
        max_parallel: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''A strategy creates a build matrix for your jobs.

        You can define different
        variations to run each job in.

        :param fail_fast: When set to true, GitHub cancels all in-progress jobs if any matrix job fails. Default: true
        :param matrix: You can define a matrix of different job configurations. A matrix allows you to create multiple jobs by performing variable substitution in a single job definition. For example, you can use a matrix to create jobs for more than one supported version of a programming language, operating system, or tool. A matrix reuses the job's configuration and creates a job for each matrix you configure. A job matrix can generate a maximum of 256 jobs per workflow run. This limit also applies to self-hosted runners.
        :param max_parallel: The maximum number of jobs that can run simultaneously when using a matrix job strategy. By default, GitHub will maximize the number of jobs run in parallel depending on the available runners on GitHub-hosted virtual machines.
        '''
        if isinstance(matrix, dict):
            matrix = JobMatrix(**matrix)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b46814aa85f4de17fbf6baa60460dccf6c2f97ae9d81a682b1f8159d4faee394)
            check_type(argname="argument fail_fast", value=fail_fast, expected_type=type_hints["fail_fast"])
            check_type(argname="argument matrix", value=matrix, expected_type=type_hints["matrix"])
            check_type(argname="argument max_parallel", value=max_parallel, expected_type=type_hints["max_parallel"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fail_fast is not None:
            self._values["fail_fast"] = fail_fast
        if matrix is not None:
            self._values["matrix"] = matrix
        if max_parallel is not None:
            self._values["max_parallel"] = max_parallel

    @builtins.property
    def fail_fast(self) -> typing.Optional[builtins.bool]:
        '''When set to true, GitHub cancels all in-progress jobs if any matrix job fails.

        Default: true
        '''
        result = self._values.get("fail_fast")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def matrix(self) -> typing.Optional[JobMatrix]:
        '''You can define a matrix of different job configurations.

        A matrix allows
        you to create multiple jobs by performing variable substitution in a
        single job definition. For example, you can use a matrix to create jobs
        for more than one supported version of a programming language, operating
        system, or tool. A matrix reuses the job's configuration and creates a
        job for each matrix you configure.

        A job matrix can generate a maximum of 256 jobs per workflow run. This
        limit also applies to self-hosted runners.
        '''
        result = self._values.get("matrix")
        return typing.cast(typing.Optional[JobMatrix], result)

    @builtins.property
    def max_parallel(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of jobs that can run simultaneously when using a matrix job strategy.

        By default, GitHub will maximize the number of jobs
        run in parallel depending on the available runners on GitHub-hosted
        virtual machines.
        '''
        result = self._values.get("max_parallel")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.LabelOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class LabelOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''label options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68eb496b82123f6e76f7d92b069e479d6fe2656dca162406a682bc24a486e7db)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabelOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.MilestoneOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class MilestoneOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Milestone options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6a48efaec3c02845f60a6993db7229c6a8c06976d1e70a29eec2a1d864d2fd2)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MilestoneOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.PageBuildOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class PageBuildOptions:
    def __init__(self) -> None:
        '''The Page build event accepts no options.'''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PageBuildOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.ProjectCardOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ProjectCardOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Project card options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47d152a7e54ef0be8ca6245b12f99b7c066028481063992853e5c56a5ac2eea5)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectCardOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.ProjectColumnOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ProjectColumnOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Probject column options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8b188e11df5621066b88f269e802d0f1cafcd2782e126886d8efbda337aa7d7)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectColumnOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.ProjectOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ProjectOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Project options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae6c711eb2c7f80b18642b4265808197268855c9553e73591e1d303bfa5e946b)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.PublicOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class PublicOptions:
    def __init__(self) -> None:
        '''The Public event accepts no options.'''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PublicOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.PullRequestOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class PullRequestOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Pull request options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2f1598ec4a615f2949befbc5a21abef68b4e9356692c70399a735ae5bfc902)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.PullRequestReviewCommentOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class PullRequestReviewCommentOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Pull request review comment options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ddcf952a6e512a3215c2dd60c2298e08b425a12f11b25f08a117e5a710a97ea)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestReviewCommentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.PullRequestReviewOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class PullRequestReviewOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Pull request review options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a60939c966ca1d7686c883fb70fa90ad963fb49908e9e6c90cfd6e63b0f9b4ed)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestReviewOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.PushOptions",
    jsii_struct_bases=[],
    name_mapping={"branches": "branches", "paths": "paths", "tags": "tags"},
)
class PushOptions:
    def __init__(
        self,
        *,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Options for push-like events.

        :param branches: When using the push and pull_request events, you can configure a workflow to run on specific branches or tags. For a pull_request event, only branches and tags on the base are evaluated. If you define only tags or only branches, the workflow won't run for events affecting the undefined Git ref.
        :param paths: When using the push and pull_request events, you can configure a workflow to run when at least one file does not match paths-ignore or at least one modified file matches the configured paths. Path filters are not evaluated for pushes to tags.
        :param tags: When using the push and pull_request events, you can configure a workflow to run on specific branches or tags. For a pull_request event, only branches and tags on the base are evaluated. If you define only tags or only branches, the workflow won't run for events affecting the undefined Git ref.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d726a3a5c42f73ca8f44dd1e5df516be286ce800935e40254a63a91d26659bc9)
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches
        if paths is not None:
            self._values["paths"] = paths
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''When using the push and pull_request events, you can configure a workflow to run on specific branches or tags.

        For a pull_request event, only
        branches and tags on the base are evaluated. If you define only tags or
        only branches, the workflow won't run for events affecting the undefined
        Git ref.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''When using the push and pull_request events, you can configure a workflow to run when at least one file does not match paths-ignore or at least one modified file matches the configured paths.

        Path filters are not
        evaluated for pushes to tags.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''When using the push and pull_request events, you can configure a workflow to run on specific branches or tags.

        For a pull_request event, only
        branches and tags on the base are evaluated. If you define only tags or
        only branches, the workflow won't run for events affecting the undefined
        Git ref.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PushOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.RegistryPackageOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class RegistryPackageOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Registry package options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2be95501fe49c6b6398781eb68cd6972627987fb8175dfc4dbf3bfc58eb87904)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RegistryPackageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.ReleaseOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ReleaseOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Release options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ba52f61d222ed0bbeefb8506346838919fd8fb81e32d506b342ff0d3bc8dcb6)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.RepositoryDispatchOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class RepositoryDispatchOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Repository dispatch options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a371d09a416a6caffde792ea61901bcc664182e6734e337922993c2de75071a)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryDispatchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.RunSettings",
    jsii_struct_bases=[],
    name_mapping={"shell": "shell", "working_directory": "workingDirectory"},
)
class RunSettings:
    def __init__(
        self,
        *,
        shell: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Run settings for a job.

        :param shell: Which shell to use for running the step.
        :param working_directory: Working directory to use when running the step.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91d0b884bc01533998bc1d20f06f8815e76bcebff37f924aaaefedfdd29ceacb)
            check_type(argname="argument shell", value=shell, expected_type=type_hints["shell"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if shell is not None:
            self._values["shell"] = shell
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def shell(self) -> typing.Optional[builtins.str]:
        '''Which shell to use for running the step.

        Example::

            "bash"
        '''
        result = self._values.get("shell")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''Working directory to use when running the step.'''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.SecretsOptions",
    jsii_struct_bases=[],
    name_mapping={
        "referenced_name": "referencedName",
        "secret_name": "secretName",
        "secret_value": "secretValue",
    },
)
class SecretsOptions:
    def __init__(
        self,
        *,
        referenced_name: builtins.str,
        secret_name: builtins.str,
        secret_value: builtins.str,
    ) -> None:
        '''
        :param referenced_name: 
        :param secret_name: 
        :param secret_value: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f57dc86f81d3c3e3aad5080c1adfebd7d73ea6864baa1fba16a515cfa3d7629c)
            check_type(argname="argument referenced_name", value=referenced_name, expected_type=type_hints["referenced_name"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            check_type(argname="argument secret_value", value=secret_value, expected_type=type_hints["secret_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "referenced_name": referenced_name,
            "secret_name": secret_name,
            "secret_value": secret_value,
        }

    @builtins.property
    def referenced_name(self) -> builtins.str:
        result = self._values.get("referenced_name")
        assert result is not None, "Required property 'referenced_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_name(self) -> builtins.str:
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_value(self) -> builtins.str:
        result = self._values.get("secret_value")
        assert result is not None, "Required property 'secret_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.StatusOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class StatusOptions:
    def __init__(self) -> None:
        '''The Status event accepts no options.'''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StatusOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.WatchOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class WatchOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Watch options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dc9f250cf90631093741133f9e562f42e8db4a43a40bd815f7689c8412e4f8e)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Workflow(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-github-actions.Workflow",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        repo_name: builtins.str,
        jobs: typing.Optional[typing.Sequence[Job]] = None,
        workflow_name: typing.Optional[builtins.str] = None,
        workflow_path: typing.Optional[builtins.str] = None,
        workflow_triggers: typing.Optional[typing.Union["WorkflowTriggers", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param repo_name: 
        :param jobs: 
        :param workflow_name: Name of the workflow file. Default: "deploy"
        :param workflow_path: File path where the workflow should be synthesized. Default: ".github/workflows/deploy.yml"
        :param workflow_triggers: GitHub workflow triggers. Default: - By default, workflow is triggered on push to the ``main`` branch and can also be triggered manually (``workflow_dispatch``).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32433a930bc5c211005975ca56778a7bf9629f48745f12756bad3652d095a038)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WorkflowProps(
            repo_name=repo_name,
            jobs=jobs,
            workflow_name=workflow_name,
            workflow_path=workflow_path,
            workflow_triggers=workflow_triggers,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addJob")
    def add_job(self, job: Job) -> None:
        '''
        :param job: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9383b4468f880ecdda624b93b0bfaa3cee789b2554b3e38f5d61a626ed5027e5)
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
        return typing.cast(None, jsii.invoke(self, "addJob", [job]))

    @builtins.property
    @jsii.member(jsii_name="jobs")
    def jobs(self) -> typing.List[Job]:
        return typing.cast(typing.List[Job], jsii.get(self, "jobs"))

    @builtins.property
    @jsii.member(jsii_name="repoName")
    def repo_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoName"))

    @builtins.property
    @jsii.member(jsii_name="workflowFile")
    def workflow_file(self) -> "YamlFile":
        return typing.cast("YamlFile", jsii.get(self, "workflowFile"))

    @builtins.property
    @jsii.member(jsii_name="workflowName")
    def workflow_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workflowName"))

    @builtins.property
    @jsii.member(jsii_name="workflowPath")
    def workflow_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workflowPath"))

    @builtins.property
    @jsii.member(jsii_name="workflowTriggers")
    def workflow_triggers(self) -> "WorkflowTriggers":
        return typing.cast("WorkflowTriggers", jsii.get(self, "workflowTriggers"))


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.WorkflowDispatchOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class WorkflowDispatchOptions:
    def __init__(self) -> None:
        '''The Workflow dispatch event accepts no options.'''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowDispatchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.WorkflowProps",
    jsii_struct_bases=[],
    name_mapping={
        "repo_name": "repoName",
        "jobs": "jobs",
        "workflow_name": "workflowName",
        "workflow_path": "workflowPath",
        "workflow_triggers": "workflowTriggers",
    },
)
class WorkflowProps:
    def __init__(
        self,
        *,
        repo_name: builtins.str,
        jobs: typing.Optional[typing.Sequence[Job]] = None,
        workflow_name: typing.Optional[builtins.str] = None,
        workflow_path: typing.Optional[builtins.str] = None,
        workflow_triggers: typing.Optional[typing.Union["WorkflowTriggers", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param repo_name: 
        :param jobs: 
        :param workflow_name: Name of the workflow file. Default: "deploy"
        :param workflow_path: File path where the workflow should be synthesized. Default: ".github/workflows/deploy.yml"
        :param workflow_triggers: GitHub workflow triggers. Default: - By default, workflow is triggered on push to the ``main`` branch and can also be triggered manually (``workflow_dispatch``).
        '''
        if isinstance(workflow_triggers, dict):
            workflow_triggers = WorkflowTriggers(**workflow_triggers)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41e5e096eecff8f705c220786e8fa5d6ac7d573f7a278d8e863d0b1585ac3433)
            check_type(argname="argument repo_name", value=repo_name, expected_type=type_hints["repo_name"])
            check_type(argname="argument jobs", value=jobs, expected_type=type_hints["jobs"])
            check_type(argname="argument workflow_name", value=workflow_name, expected_type=type_hints["workflow_name"])
            check_type(argname="argument workflow_path", value=workflow_path, expected_type=type_hints["workflow_path"])
            check_type(argname="argument workflow_triggers", value=workflow_triggers, expected_type=type_hints["workflow_triggers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repo_name": repo_name,
        }
        if jobs is not None:
            self._values["jobs"] = jobs
        if workflow_name is not None:
            self._values["workflow_name"] = workflow_name
        if workflow_path is not None:
            self._values["workflow_path"] = workflow_path
        if workflow_triggers is not None:
            self._values["workflow_triggers"] = workflow_triggers

    @builtins.property
    def repo_name(self) -> builtins.str:
        result = self._values.get("repo_name")
        assert result is not None, "Required property 'repo_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def jobs(self) -> typing.Optional[typing.List[Job]]:
        result = self._values.get("jobs")
        return typing.cast(typing.Optional[typing.List[Job]], result)

    @builtins.property
    def workflow_name(self) -> typing.Optional[builtins.str]:
        '''Name of the workflow file.

        :default: "deploy"
        '''
        result = self._values.get("workflow_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_path(self) -> typing.Optional[builtins.str]:
        '''File path where the workflow should be synthesized.

        :default: ".github/workflows/deploy.yml"
        '''
        result = self._values.get("workflow_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_triggers(self) -> typing.Optional["WorkflowTriggers"]:
        '''GitHub workflow triggers.

        :default:

        - By default, workflow is triggered on push to the ``main`` branch
        and can also be triggered manually (``workflow_dispatch``).
        '''
        result = self._values.get("workflow_triggers")
        return typing.cast(typing.Optional["WorkflowTriggers"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.WorkflowRunOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class WorkflowRunOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Workflow run options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77e79ed0a6983c58278f82bfa82a680d322eae83961f769dac078fbe1169d55c)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowRunOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.WorkflowTriggers",
    jsii_struct_bases=[],
    name_mapping={
        "check_run": "checkRun",
        "check_suite": "checkSuite",
        "create": "create",
        "delete": "delete",
        "deployment": "deployment",
        "deployment_status": "deploymentStatus",
        "fork": "fork",
        "gollum": "gollum",
        "issue_comment": "issueComment",
        "issues": "issues",
        "label": "label",
        "milestone": "milestone",
        "page_build": "pageBuild",
        "project": "project",
        "project_card": "projectCard",
        "project_column": "projectColumn",
        "public": "public",
        "pull_request": "pullRequest",
        "pull_request_review": "pullRequestReview",
        "pull_request_review_comment": "pullRequestReviewComment",
        "pull_request_target": "pullRequestTarget",
        "push": "push",
        "registry_package": "registryPackage",
        "release": "release",
        "repository_dispatch": "repositoryDispatch",
        "schedule": "schedule",
        "status": "status",
        "watch": "watch",
        "workflow_dispatch": "workflowDispatch",
        "workflow_run": "workflowRun",
    },
)
class WorkflowTriggers:
    def __init__(
        self,
        *,
        check_run: typing.Optional[typing.Union[CheckRunOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        check_suite: typing.Optional[typing.Union[CheckSuiteOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        create: typing.Optional[typing.Union[CreateOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        delete: typing.Optional[typing.Union[DeleteOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deployment: typing.Optional[typing.Union[DeploymentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_status: typing.Optional[typing.Union[DeploymentStatusOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        fork: typing.Optional[typing.Union[ForkOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gollum: typing.Optional[typing.Union[GollumOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        issue_comment: typing.Optional[typing.Union[IssueCommentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        issues: typing.Optional[typing.Union[IssuesOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        label: typing.Optional[typing.Union[LabelOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        milestone: typing.Optional[typing.Union[MilestoneOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        page_build: typing.Optional[typing.Union[PageBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[typing.Union[ProjectOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        project_card: typing.Optional[typing.Union[ProjectCardOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        project_column: typing.Optional[typing.Union[ProjectColumnOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        public: typing.Optional[typing.Union[PublicOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        pull_request: typing.Optional[typing.Union[PullRequestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        pull_request_review: typing.Optional[typing.Union[PullRequestReviewOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        pull_request_review_comment: typing.Optional[typing.Union[PullRequestReviewCommentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        pull_request_target: typing.Optional[typing.Union["PullRequestTargetOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        push: typing.Optional[typing.Union[PushOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        registry_package: typing.Optional[typing.Union[RegistryPackageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        release: typing.Optional[typing.Union[ReleaseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        repository_dispatch: typing.Optional[typing.Union[RepositoryDispatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[typing.Sequence[typing.Union[CronScheduleOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        status: typing.Optional[typing.Union[StatusOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        watch: typing.Optional[typing.Union[WatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_dispatch: typing.Optional[typing.Union[WorkflowDispatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_run: typing.Optional[typing.Union[WorkflowRunOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''The set of available triggers for GitHub Workflows.

        :param check_run: Runs your workflow anytime the check_run event occurs.
        :param check_suite: Runs your workflow anytime the check_suite event occurs.
        :param create: Runs your workflow anytime someone creates a branch or tag, which triggers the create event.
        :param delete: Runs your workflow anytime someone deletes a branch or tag, which triggers the delete event.
        :param deployment: Runs your workflow anytime someone creates a deployment, which triggers the deployment event. Deployments created with a commit SHA may not have a Git ref.
        :param deployment_status: Runs your workflow anytime a third party provides a deployment status, which triggers the deployment_status event. Deployments created with a commit SHA may not have a Git ref.
        :param fork: Runs your workflow anytime when someone forks a repository, which triggers the fork event.
        :param gollum: Runs your workflow when someone creates or updates a Wiki page, which triggers the gollum event.
        :param issue_comment: Runs your workflow anytime the issue_comment event occurs.
        :param issues: Runs your workflow anytime the issues event occurs.
        :param label: Runs your workflow anytime the label event occurs.
        :param milestone: Runs your workflow anytime the milestone event occurs.
        :param page_build: Runs your workflow anytime someone pushes to a GitHub Pages-enabled branch, which triggers the page_build event.
        :param project: Runs your workflow anytime the project event occurs.
        :param project_card: Runs your workflow anytime the project_card event occurs.
        :param project_column: Runs your workflow anytime the project_column event occurs.
        :param public: Runs your workflow anytime someone makes a private repository public, which triggers the public event.
        :param pull_request: Runs your workflow anytime the pull_request event occurs.
        :param pull_request_review: Runs your workflow anytime the pull_request_review event occurs.
        :param pull_request_review_comment: Runs your workflow anytime a comment on a pull request's unified diff is modified, which triggers the pull_request_review_comment event.
        :param pull_request_target: This event runs in the context of the base of the pull request, rather than in the merge commit as the pull_request event does. This prevents executing unsafe workflow code from the head of the pull request that could alter your repository or steal any secrets you use in your workflow. This event allows you to do things like create workflows that label and comment on pull requests based on the contents of the event payload. WARNING: The ``pull_request_target`` event is granted read/write repository token and can access secrets, even when it is triggered from a fork. Although the workflow runs in the context of the base of the pull request, you should make sure that you do not check out, build, or run untrusted code from the pull request with this event. Additionally, any caches share the same scope as the base branch, and to help prevent cache poisoning, you should not save the cache if there is a possibility that the cache contents were altered.
        :param push: Runs your workflow when someone pushes to a repository branch, which triggers the push event.
        :param registry_package: Runs your workflow anytime a package is published or updated.
        :param release: Runs your workflow anytime the release event occurs.
        :param repository_dispatch: You can use the GitHub API to trigger a webhook event called repository_dispatch when you want to trigger a workflow for activity that happens outside of GitHub.
        :param schedule: You can schedule a workflow to run at specific UTC times using POSIX cron syntax. Scheduled workflows run on the latest commit on the default or base branch. The shortest interval you can run scheduled workflows is once every 5 minutes.
        :param status: Runs your workflow anytime the status of a Git commit changes, which triggers the status event.
        :param watch: Runs your workflow anytime the watch event occurs.
        :param workflow_dispatch: You can configure custom-defined input properties, default input values, and required inputs for the event directly in your workflow. When the workflow runs, you can access the input values in the github.event.inputs context.
        :param workflow_run: This event occurs when a workflow run is requested or completed, and allows you to execute a workflow based on the finished result of another workflow. A workflow run is triggered regardless of the result of the previous workflow.

        :see: https://docs.github.com/en/actions/reference/events-that-trigger-workflows
        '''
        if isinstance(check_run, dict):
            check_run = CheckRunOptions(**check_run)
        if isinstance(check_suite, dict):
            check_suite = CheckSuiteOptions(**check_suite)
        if isinstance(create, dict):
            create = CreateOptions(**create)
        if isinstance(delete, dict):
            delete = DeleteOptions(**delete)
        if isinstance(deployment, dict):
            deployment = DeploymentOptions(**deployment)
        if isinstance(deployment_status, dict):
            deployment_status = DeploymentStatusOptions(**deployment_status)
        if isinstance(fork, dict):
            fork = ForkOptions(**fork)
        if isinstance(gollum, dict):
            gollum = GollumOptions(**gollum)
        if isinstance(issue_comment, dict):
            issue_comment = IssueCommentOptions(**issue_comment)
        if isinstance(issues, dict):
            issues = IssuesOptions(**issues)
        if isinstance(label, dict):
            label = LabelOptions(**label)
        if isinstance(milestone, dict):
            milestone = MilestoneOptions(**milestone)
        if isinstance(page_build, dict):
            page_build = PageBuildOptions(**page_build)
        if isinstance(project, dict):
            project = ProjectOptions(**project)
        if isinstance(project_card, dict):
            project_card = ProjectCardOptions(**project_card)
        if isinstance(project_column, dict):
            project_column = ProjectColumnOptions(**project_column)
        if isinstance(public, dict):
            public = PublicOptions(**public)
        if isinstance(pull_request, dict):
            pull_request = PullRequestOptions(**pull_request)
        if isinstance(pull_request_review, dict):
            pull_request_review = PullRequestReviewOptions(**pull_request_review)
        if isinstance(pull_request_review_comment, dict):
            pull_request_review_comment = PullRequestReviewCommentOptions(**pull_request_review_comment)
        if isinstance(pull_request_target, dict):
            pull_request_target = PullRequestTargetOptions(**pull_request_target)
        if isinstance(push, dict):
            push = PushOptions(**push)
        if isinstance(registry_package, dict):
            registry_package = RegistryPackageOptions(**registry_package)
        if isinstance(release, dict):
            release = ReleaseOptions(**release)
        if isinstance(repository_dispatch, dict):
            repository_dispatch = RepositoryDispatchOptions(**repository_dispatch)
        if isinstance(status, dict):
            status = StatusOptions(**status)
        if isinstance(watch, dict):
            watch = WatchOptions(**watch)
        if isinstance(workflow_dispatch, dict):
            workflow_dispatch = WorkflowDispatchOptions(**workflow_dispatch)
        if isinstance(workflow_run, dict):
            workflow_run = WorkflowRunOptions(**workflow_run)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0387f7b34704bec5f4f1b919355816eec318416e07cebd87ece23421ba7d6bc9)
            check_type(argname="argument check_run", value=check_run, expected_type=type_hints["check_run"])
            check_type(argname="argument check_suite", value=check_suite, expected_type=type_hints["check_suite"])
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument deployment", value=deployment, expected_type=type_hints["deployment"])
            check_type(argname="argument deployment_status", value=deployment_status, expected_type=type_hints["deployment_status"])
            check_type(argname="argument fork", value=fork, expected_type=type_hints["fork"])
            check_type(argname="argument gollum", value=gollum, expected_type=type_hints["gollum"])
            check_type(argname="argument issue_comment", value=issue_comment, expected_type=type_hints["issue_comment"])
            check_type(argname="argument issues", value=issues, expected_type=type_hints["issues"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument milestone", value=milestone, expected_type=type_hints["milestone"])
            check_type(argname="argument page_build", value=page_build, expected_type=type_hints["page_build"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument project_card", value=project_card, expected_type=type_hints["project_card"])
            check_type(argname="argument project_column", value=project_column, expected_type=type_hints["project_column"])
            check_type(argname="argument public", value=public, expected_type=type_hints["public"])
            check_type(argname="argument pull_request", value=pull_request, expected_type=type_hints["pull_request"])
            check_type(argname="argument pull_request_review", value=pull_request_review, expected_type=type_hints["pull_request_review"])
            check_type(argname="argument pull_request_review_comment", value=pull_request_review_comment, expected_type=type_hints["pull_request_review_comment"])
            check_type(argname="argument pull_request_target", value=pull_request_target, expected_type=type_hints["pull_request_target"])
            check_type(argname="argument push", value=push, expected_type=type_hints["push"])
            check_type(argname="argument registry_package", value=registry_package, expected_type=type_hints["registry_package"])
            check_type(argname="argument release", value=release, expected_type=type_hints["release"])
            check_type(argname="argument repository_dispatch", value=repository_dispatch, expected_type=type_hints["repository_dispatch"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument watch", value=watch, expected_type=type_hints["watch"])
            check_type(argname="argument workflow_dispatch", value=workflow_dispatch, expected_type=type_hints["workflow_dispatch"])
            check_type(argname="argument workflow_run", value=workflow_run, expected_type=type_hints["workflow_run"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if check_run is not None:
            self._values["check_run"] = check_run
        if check_suite is not None:
            self._values["check_suite"] = check_suite
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if deployment is not None:
            self._values["deployment"] = deployment
        if deployment_status is not None:
            self._values["deployment_status"] = deployment_status
        if fork is not None:
            self._values["fork"] = fork
        if gollum is not None:
            self._values["gollum"] = gollum
        if issue_comment is not None:
            self._values["issue_comment"] = issue_comment
        if issues is not None:
            self._values["issues"] = issues
        if label is not None:
            self._values["label"] = label
        if milestone is not None:
            self._values["milestone"] = milestone
        if page_build is not None:
            self._values["page_build"] = page_build
        if project is not None:
            self._values["project"] = project
        if project_card is not None:
            self._values["project_card"] = project_card
        if project_column is not None:
            self._values["project_column"] = project_column
        if public is not None:
            self._values["public"] = public
        if pull_request is not None:
            self._values["pull_request"] = pull_request
        if pull_request_review is not None:
            self._values["pull_request_review"] = pull_request_review
        if pull_request_review_comment is not None:
            self._values["pull_request_review_comment"] = pull_request_review_comment
        if pull_request_target is not None:
            self._values["pull_request_target"] = pull_request_target
        if push is not None:
            self._values["push"] = push
        if registry_package is not None:
            self._values["registry_package"] = registry_package
        if release is not None:
            self._values["release"] = release
        if repository_dispatch is not None:
            self._values["repository_dispatch"] = repository_dispatch
        if schedule is not None:
            self._values["schedule"] = schedule
        if status is not None:
            self._values["status"] = status
        if watch is not None:
            self._values["watch"] = watch
        if workflow_dispatch is not None:
            self._values["workflow_dispatch"] = workflow_dispatch
        if workflow_run is not None:
            self._values["workflow_run"] = workflow_run

    @builtins.property
    def check_run(self) -> typing.Optional[CheckRunOptions]:
        '''Runs your workflow anytime the check_run event occurs.'''
        result = self._values.get("check_run")
        return typing.cast(typing.Optional[CheckRunOptions], result)

    @builtins.property
    def check_suite(self) -> typing.Optional[CheckSuiteOptions]:
        '''Runs your workflow anytime the check_suite event occurs.'''
        result = self._values.get("check_suite")
        return typing.cast(typing.Optional[CheckSuiteOptions], result)

    @builtins.property
    def create(self) -> typing.Optional[CreateOptions]:
        '''Runs your workflow anytime someone creates a branch or tag, which triggers the create event.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[CreateOptions], result)

    @builtins.property
    def delete(self) -> typing.Optional[DeleteOptions]:
        '''Runs your workflow anytime someone deletes a branch or tag, which triggers the delete event.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[DeleteOptions], result)

    @builtins.property
    def deployment(self) -> typing.Optional[DeploymentOptions]:
        '''Runs your workflow anytime someone creates a deployment, which triggers the deployment event.

        Deployments created with a commit SHA may not have
        a Git ref.
        '''
        result = self._values.get("deployment")
        return typing.cast(typing.Optional[DeploymentOptions], result)

    @builtins.property
    def deployment_status(self) -> typing.Optional[DeploymentStatusOptions]:
        '''Runs your workflow anytime a third party provides a deployment status, which triggers the deployment_status event.

        Deployments created with a
        commit SHA may not have a Git ref.
        '''
        result = self._values.get("deployment_status")
        return typing.cast(typing.Optional[DeploymentStatusOptions], result)

    @builtins.property
    def fork(self) -> typing.Optional[ForkOptions]:
        '''Runs your workflow anytime when someone forks a repository, which triggers the fork event.'''
        result = self._values.get("fork")
        return typing.cast(typing.Optional[ForkOptions], result)

    @builtins.property
    def gollum(self) -> typing.Optional[GollumOptions]:
        '''Runs your workflow when someone creates or updates a Wiki page, which triggers the gollum event.'''
        result = self._values.get("gollum")
        return typing.cast(typing.Optional[GollumOptions], result)

    @builtins.property
    def issue_comment(self) -> typing.Optional[IssueCommentOptions]:
        '''Runs your workflow anytime the issue_comment event occurs.'''
        result = self._values.get("issue_comment")
        return typing.cast(typing.Optional[IssueCommentOptions], result)

    @builtins.property
    def issues(self) -> typing.Optional[IssuesOptions]:
        '''Runs your workflow anytime the issues event occurs.'''
        result = self._values.get("issues")
        return typing.cast(typing.Optional[IssuesOptions], result)

    @builtins.property
    def label(self) -> typing.Optional[LabelOptions]:
        '''Runs your workflow anytime the label event occurs.'''
        result = self._values.get("label")
        return typing.cast(typing.Optional[LabelOptions], result)

    @builtins.property
    def milestone(self) -> typing.Optional[MilestoneOptions]:
        '''Runs your workflow anytime the milestone event occurs.'''
        result = self._values.get("milestone")
        return typing.cast(typing.Optional[MilestoneOptions], result)

    @builtins.property
    def page_build(self) -> typing.Optional[PageBuildOptions]:
        '''Runs your workflow anytime someone pushes to a GitHub Pages-enabled branch, which triggers the page_build event.'''
        result = self._values.get("page_build")
        return typing.cast(typing.Optional[PageBuildOptions], result)

    @builtins.property
    def project(self) -> typing.Optional[ProjectOptions]:
        '''Runs your workflow anytime the project event occurs.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[ProjectOptions], result)

    @builtins.property
    def project_card(self) -> typing.Optional[ProjectCardOptions]:
        '''Runs your workflow anytime the project_card event occurs.'''
        result = self._values.get("project_card")
        return typing.cast(typing.Optional[ProjectCardOptions], result)

    @builtins.property
    def project_column(self) -> typing.Optional[ProjectColumnOptions]:
        '''Runs your workflow anytime the project_column event occurs.'''
        result = self._values.get("project_column")
        return typing.cast(typing.Optional[ProjectColumnOptions], result)

    @builtins.property
    def public(self) -> typing.Optional[PublicOptions]:
        '''Runs your workflow anytime someone makes a private repository public, which triggers the public event.'''
        result = self._values.get("public")
        return typing.cast(typing.Optional[PublicOptions], result)

    @builtins.property
    def pull_request(self) -> typing.Optional[PullRequestOptions]:
        '''Runs your workflow anytime the pull_request event occurs.'''
        result = self._values.get("pull_request")
        return typing.cast(typing.Optional[PullRequestOptions], result)

    @builtins.property
    def pull_request_review(self) -> typing.Optional[PullRequestReviewOptions]:
        '''Runs your workflow anytime the pull_request_review event occurs.'''
        result = self._values.get("pull_request_review")
        return typing.cast(typing.Optional[PullRequestReviewOptions], result)

    @builtins.property
    def pull_request_review_comment(
        self,
    ) -> typing.Optional[PullRequestReviewCommentOptions]:
        '''Runs your workflow anytime a comment on a pull request's unified diff is modified, which triggers the pull_request_review_comment event.'''
        result = self._values.get("pull_request_review_comment")
        return typing.cast(typing.Optional[PullRequestReviewCommentOptions], result)

    @builtins.property
    def pull_request_target(self) -> typing.Optional["PullRequestTargetOptions"]:
        '''This event runs in the context of the base of the pull request, rather than in the merge commit as the pull_request event does.

        This prevents
        executing unsafe workflow code from the head of the pull request that
        could alter your repository or steal any secrets you use in your workflow.
        This event allows you to do things like create workflows that label and
        comment on pull requests based on the contents of the event payload.

        WARNING: The ``pull_request_target`` event is granted read/write repository
        token and can access secrets, even when it is triggered from a fork.
        Although the workflow runs in the context of the base of the pull request,
        you should make sure that you do not check out, build, or run untrusted
        code from the pull request with this event. Additionally, any caches
        share the same scope as the base branch, and to help prevent cache
        poisoning, you should not save the cache if there is a possibility that
        the cache contents were altered.

        :see: https://securitylab.github.com/research/github-actions-preventing-pwn-requests
        '''
        result = self._values.get("pull_request_target")
        return typing.cast(typing.Optional["PullRequestTargetOptions"], result)

    @builtins.property
    def push(self) -> typing.Optional[PushOptions]:
        '''Runs your workflow when someone pushes to a repository branch, which triggers the push event.'''
        result = self._values.get("push")
        return typing.cast(typing.Optional[PushOptions], result)

    @builtins.property
    def registry_package(self) -> typing.Optional[RegistryPackageOptions]:
        '''Runs your workflow anytime a package is published or updated.'''
        result = self._values.get("registry_package")
        return typing.cast(typing.Optional[RegistryPackageOptions], result)

    @builtins.property
    def release(self) -> typing.Optional[ReleaseOptions]:
        '''Runs your workflow anytime the release event occurs.'''
        result = self._values.get("release")
        return typing.cast(typing.Optional[ReleaseOptions], result)

    @builtins.property
    def repository_dispatch(self) -> typing.Optional[RepositoryDispatchOptions]:
        '''You can use the GitHub API to trigger a webhook event called repository_dispatch when you want to trigger a workflow for activity that happens outside of GitHub.'''
        result = self._values.get("repository_dispatch")
        return typing.cast(typing.Optional[RepositoryDispatchOptions], result)

    @builtins.property
    def schedule(self) -> typing.Optional[typing.List[CronScheduleOptions]]:
        '''You can schedule a workflow to run at specific UTC times using POSIX cron syntax.

        Scheduled workflows run on the latest commit on the default or
        base branch. The shortest interval you can run scheduled workflows is
        once every 5 minutes.

        :see: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html#tag_20_25_07
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[typing.List[CronScheduleOptions]], result)

    @builtins.property
    def status(self) -> typing.Optional[StatusOptions]:
        '''Runs your workflow anytime the status of a Git commit changes, which triggers the status event.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[StatusOptions], result)

    @builtins.property
    def watch(self) -> typing.Optional[WatchOptions]:
        '''Runs your workflow anytime the watch event occurs.'''
        result = self._values.get("watch")
        return typing.cast(typing.Optional[WatchOptions], result)

    @builtins.property
    def workflow_dispatch(self) -> typing.Optional[WorkflowDispatchOptions]:
        '''You can configure custom-defined input properties, default input values, and required inputs for the event directly in your workflow.

        When the
        workflow runs, you can access the input values in the github.event.inputs
        context.
        '''
        result = self._values.get("workflow_dispatch")
        return typing.cast(typing.Optional[WorkflowDispatchOptions], result)

    @builtins.property
    def workflow_run(self) -> typing.Optional[WorkflowRunOptions]:
        '''This event occurs when a workflow run is requested or completed, and allows you to execute a workflow based on the finished result of another workflow.

        A workflow run is triggered regardless of the result of the
        previous workflow.
        '''
        result = self._values.get("workflow_run")
        return typing.cast(typing.Optional[WorkflowRunOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowTriggers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class YamlFile(
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-github-actions.YamlFile",
):
    def __init__(self, file_path: builtins.str, *, obj: typing.Any = None) -> None:
        '''
        :param file_path: -
        :param obj: The object that will be serialized. You can modify the object's contents before synthesis. Default: {} an empty object
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f7f49f93fdb8bb2ff9840c13716b8b6bb007510136e6189fa564ee4e6fa509d)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        options = YamlFileOptions(obj=obj)

        jsii.create(self.__class__, self, [file_path, options])

    @jsii.member(jsii_name="toYaml")
    def to_yaml(self) -> builtins.str:
        '''Returns the patched yaml file.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toYaml", []))

    @jsii.member(jsii_name="update")
    def update(self, obj: typing.Any) -> None:
        '''Update the output object.

        :param obj: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79fddbb66dfb63556728574cf989f64cc6eb8611fa794432f9778bd5a03f9fdc)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        return typing.cast(None, jsii.invoke(self, "update", [obj]))

    @jsii.member(jsii_name="writeFile")
    def write_file(self) -> None:
        '''Write the patched yaml file to the specified location.'''
        return typing.cast(None, jsii.invoke(self, "writeFile", []))

    @builtins.property
    @jsii.member(jsii_name="commentAtTop")
    def comment_at_top(self) -> typing.Optional[builtins.str]:
        '''A comment to be added to the top of the YAML file.

        Can be multiline. All non-empty line are pefixed with '# '. Empty lines are kept, but not
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentAtTop"))

    @comment_at_top.setter
    def comment_at_top(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dcdb88b1cf90860bcd41d29610e5ee644c6dd3814cbe75f15887b9449a92b77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commentAtTop", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.YamlFileOptions",
    jsii_struct_bases=[],
    name_mapping={"obj": "obj"},
)
class YamlFileOptions:
    def __init__(self, *, obj: typing.Any = None) -> None:
        '''Options for ``YamlFile``.

        :param obj: The object that will be serialized. You can modify the object's contents before synthesis. Default: {} an empty object
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c841f2c573d826862c90fc32dd4c4473708774058a00b5e0005e69f873d1349c)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if obj is not None:
            self._values["obj"] = obj

    @builtins.property
    def obj(self) -> typing.Any:
        '''The object that will be serialized.

        You can modify the object's contents
        before synthesis.

        :default: {} an empty object
        '''
        result = self._values.get("obj")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "YamlFileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.JobStep",
    jsii_struct_bases=[JobStepData],
    name_mapping={
        "continue_on_error": "continueOnError",
        "env": "env",
        "id": "id",
        "if_": "if",
        "name": "name",
        "run": "run",
        "timeout_minutes": "timeoutMinutes",
        "uses": "uses",
        "with_": "with",
        "with_secrets": "withSecrets",
    },
)
class JobStep(JobStepData):
    def __init__(
        self,
        *,
        continue_on_error: typing.Optional[builtins.bool] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        run: typing.Optional[builtins.str] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
        uses: typing.Optional[builtins.str] = None,
        with_: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        with_secrets: typing.Optional[typing.Sequence[typing.Union[SecretsOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param continue_on_error: Prevents a job from failing when a step fails. Set to true to allow a job to pass when this step fails.
        :param env: Sets environment variables for steps to use in the runner environment. You can also set environment variables for the entire workflow or a job.
        :param id: A unique identifier for the step. You can use the id to reference the step in contexts.
        :param if_: You can use the if conditional to prevent a job from running unless a condition is met. You can use any supported context and expression to create a conditional.
        :param name: A name for your step to display on GitHub.
        :param run: Runs command-line programs using the operating system's shell. If you do not provide a name, the step name will default to the text specified in the run command.
        :param timeout_minutes: The maximum number of minutes to run the step before killing the process.
        :param uses: Selects an action to run as part of a step in your job. An action is a reusable unit of code. You can use an action defined in the same repository as the workflow, a public repository, or in a published Docker container image.
        :param with_: A map of the input parameters defined by the action. Each input parameter is a key/value pair. Input parameters are set as environment variables. The variable is prefixed with INPUT_ and converted to upper case.
        :param with_secrets: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90fd62dfa4da7f32e261f2dcbf958695d5193af329b94943843cba688a126dc7)
            check_type(argname="argument continue_on_error", value=continue_on_error, expected_type=type_hints["continue_on_error"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument run", value=run, expected_type=type_hints["run"])
            check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
            check_type(argname="argument uses", value=uses, expected_type=type_hints["uses"])
            check_type(argname="argument with_", value=with_, expected_type=type_hints["with_"])
            check_type(argname="argument with_secrets", value=with_secrets, expected_type=type_hints["with_secrets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if continue_on_error is not None:
            self._values["continue_on_error"] = continue_on_error
        if env is not None:
            self._values["env"] = env
        if id is not None:
            self._values["id"] = id
        if if_ is not None:
            self._values["if_"] = if_
        if name is not None:
            self._values["name"] = name
        if run is not None:
            self._values["run"] = run
        if timeout_minutes is not None:
            self._values["timeout_minutes"] = timeout_minutes
        if uses is not None:
            self._values["uses"] = uses
        if with_ is not None:
            self._values["with_"] = with_
        if with_secrets is not None:
            self._values["with_secrets"] = with_secrets

    @builtins.property
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        '''Prevents a job from failing when a step fails.

        Set to true to allow a job
        to pass when this step fails.
        '''
        result = self._values.get("continue_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Sets environment variables for steps to use in the runner environment.

        You can also set environment variables for the entire workflow or a job.
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''A unique identifier for the step.

        You can use the id to reference the
        step in contexts.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        '''You can use the if conditional to prevent a job from running unless a condition is met.

        You can use any supported context and expression to
        create a conditional.
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for your step to display on GitHub.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run(self) -> typing.Optional[builtins.str]:
        '''Runs command-line programs using the operating system's shell.

        If you do
        not provide a name, the step name will default to the text specified in
        the run command.
        '''
        result = self._values.get("run")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of minutes to run the step before killing the process.'''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def uses(self) -> typing.Optional[builtins.str]:
        '''Selects an action to run as part of a step in your job.

        An action is a
        reusable unit of code. You can use an action defined in the same
        repository as the workflow, a public repository, or in a published Docker
        container image.
        '''
        result = self._values.get("uses")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def with_(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''A map of the input parameters defined by the action.

        Each input parameter
        is a key/value pair. Input parameters are set as environment variables.
        The variable is prefixed with INPUT_ and converted to upper case.
        '''
        result = self._values.get("with_")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def with_secrets(self) -> typing.Optional[typing.List[SecretsOptions]]:
        result = self._values.get("with_secrets")
        return typing.cast(typing.Optional[typing.List[SecretsOptions]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-github-actions.PullRequestTargetOptions",
    jsii_struct_bases=[PushOptions],
    name_mapping={
        "branches": "branches",
        "paths": "paths",
        "tags": "tags",
        "types": "types",
    },
)
class PullRequestTargetOptions(PushOptions):
    def __init__(
        self,
        *,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Pull request target options.

        :param branches: When using the push and pull_request events, you can configure a workflow to run on specific branches or tags. For a pull_request event, only branches and tags on the base are evaluated. If you define only tags or only branches, the workflow won't run for events affecting the undefined Git ref.
        :param paths: When using the push and pull_request events, you can configure a workflow to run when at least one file does not match paths-ignore or at least one modified file matches the configured paths. Path filters are not evaluated for pushes to tags.
        :param tags: When using the push and pull_request events, you can configure a workflow to run on specific branches or tags. For a pull_request event, only branches and tags on the base are evaluated. If you define only tags or only branches, the workflow won't run for events affecting the undefined Git ref.
        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d28c195fbfe2acaaf2e14c0c828f64fde9aaa1a083487aa09f4a566a3995be67)
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches
        if paths is not None:
            self._values["paths"] = paths
        if tags is not None:
            self._values["tags"] = tags
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''When using the push and pull_request events, you can configure a workflow to run on specific branches or tags.

        For a pull_request event, only
        branches and tags on the base are evaluated. If you define only tags or
        only branches, the workflow won't run for events affecting the undefined
        Git ref.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''When using the push and pull_request events, you can configure a workflow to run when at least one file does not match paths-ignore or at least one modified file matches the configured paths.

        Path filters are not
        evaluated for pushes to tags.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''When using the push and pull_request events, you can configure a workflow to run on specific branches or tags.

        For a pull_request event, only
        branches and tags on the base are evaluated. If you define only tags or
        only branches, the workflow won't run for events affecting the undefined
        Git ref.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestTargetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CheckRunOptions",
    "CheckSuiteOptions",
    "ContainerCredentials",
    "ContainerOptions",
    "CreateOptions",
    "CronScheduleOptions",
    "DeleteOptions",
    "DeploymentOptions",
    "DeploymentStatusOptions",
    "ForkOptions",
    "GollumOptions",
    "IssueCommentOptions",
    "IssuesOptions",
    "Job",
    "JobData",
    "JobDefaults",
    "JobMatrix",
    "JobPermission",
    "JobPermissions",
    "JobProps",
    "JobStep",
    "JobStepData",
    "JobStrategy",
    "LabelOptions",
    "MilestoneOptions",
    "PageBuildOptions",
    "ProjectCardOptions",
    "ProjectColumnOptions",
    "ProjectOptions",
    "PublicOptions",
    "PullRequestOptions",
    "PullRequestReviewCommentOptions",
    "PullRequestReviewOptions",
    "PullRequestTargetOptions",
    "PushOptions",
    "RegistryPackageOptions",
    "ReleaseOptions",
    "RepositoryDispatchOptions",
    "RunSettings",
    "SecretsOptions",
    "StatusOptions",
    "WatchOptions",
    "Workflow",
    "WorkflowDispatchOptions",
    "WorkflowProps",
    "WorkflowRunOptions",
    "WorkflowTriggers",
    "YamlFile",
    "YamlFileOptions",
]

publication.publish()

def _typecheckingstub__7a782937bdfd03983584e034e91a80976debda0e536104d007aa603f963deff6(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe01942fe47c9f0a94235d83068102bc515d036b148677788d732f4a804c275(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80112d00c9e6ad87669cddb60f24db7f28616ab8f6e5a592e0566dc4604e2004(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d6461d95341b2a11e0667c65e2f7ecb33f23ba2487725caf3fd46e5e5fd3095(
    *,
    image: builtins.str,
    credentials: typing.Optional[typing.Union[ContainerCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    options: typing.Optional[typing.Sequence[builtins.str]] = None,
    ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
    volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e75a13596a5b83e96255c41ac6916da833bb277e30081dbebc4e9454e2d744(
    *,
    cron: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d46103d6dcd8cc3a19adacec36642c7fb86439c841bcde588fb00068801b38(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4be6353a13832066a3671838515ee8b07932d4f07cf3006569cb73149a65186(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be21f04638b9906cec654e3f713ef2d8f7e5c2e530067c866cf02adf881e55f2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    steps: typing.Sequence[typing.Union[JobStep, typing.Dict[builtins.str, typing.Any]]],
    concurrency: typing.Any = None,
    container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[JobDefaults, typing.Dict[builtins.str, typing.Any]]] = None,
    depends_on: typing.Optional[typing.Sequence[Job]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Any = None,
    job_referene_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    permissions: typing.Optional[typing.Union[JobPermissions, typing.Dict[builtins.str, typing.Any]]] = None,
    run_if: typing.Optional[builtins.str] = None,
    runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    strategy: typing.Optional[typing.Union[JobStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e057c955095553b0383af68f3b57537ad24cf6a41453497377a1d37c59e357d(
    job: Job,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb4186255cabb20b2161c41788f309a468babdf2e0c103969ab7f287ffcc2c0d(
    *,
    permissions: typing.Union[JobPermissions, typing.Dict[builtins.str, typing.Any]],
    runs_on: typing.Union[builtins.str, typing.Sequence[builtins.str]],
    steps: typing.Sequence[typing.Union[JobStepData, typing.Dict[builtins.str, typing.Any]]],
    concurrency: typing.Any = None,
    container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[JobDefaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Any = None,
    if_: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    strategy: typing.Optional[typing.Union[JobStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602b6d9483733a9a57aade72d7cc2dee06cf9a12317aae233cd4090b4c915627(
    *,
    run: typing.Optional[typing.Union[RunSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e75f9de38d013acb438dd6100f3e72a51ecfda4438e6eb335d21dde85a48e6a(
    *,
    domain: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
    exclude: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, builtins.str]]] = None,
    include: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4570cf024ce9e959d0e6f37e592a91aad5b667f49707c3623b2aabdad9e6b2a3(
    *,
    actions: typing.Optional[JobPermission] = None,
    checks: typing.Optional[JobPermission] = None,
    contents: typing.Optional[JobPermission] = None,
    deployments: typing.Optional[JobPermission] = None,
    discussions: typing.Optional[JobPermission] = None,
    id_token: typing.Optional[JobPermission] = None,
    issues: typing.Optional[JobPermission] = None,
    packages: typing.Optional[JobPermission] = None,
    pull_requests: typing.Optional[JobPermission] = None,
    repository_projects: typing.Optional[JobPermission] = None,
    security_events: typing.Optional[JobPermission] = None,
    statuses: typing.Optional[JobPermission] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea95168c7557d23f4c6321ca3edaecafcbec637a3d6a88bc857045eff5b16581(
    *,
    steps: typing.Sequence[typing.Union[JobStep, typing.Dict[builtins.str, typing.Any]]],
    concurrency: typing.Any = None,
    container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[JobDefaults, typing.Dict[builtins.str, typing.Any]]] = None,
    depends_on: typing.Optional[typing.Sequence[Job]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Any = None,
    job_referene_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    permissions: typing.Optional[typing.Union[JobPermissions, typing.Dict[builtins.str, typing.Any]]] = None,
    run_if: typing.Optional[builtins.str] = None,
    runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    strategy: typing.Optional[typing.Union[JobStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__376a7046dcae820e8505bb15110e912cd78ebac8f065da00158a60c775d0ddf0(
    *,
    continue_on_error: typing.Optional[builtins.bool] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    if_: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    run: typing.Optional[builtins.str] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
    uses: typing.Optional[builtins.str] = None,
    with_: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46814aa85f4de17fbf6baa60460dccf6c2f97ae9d81a682b1f8159d4faee394(
    *,
    fail_fast: typing.Optional[builtins.bool] = None,
    matrix: typing.Optional[typing.Union[JobMatrix, typing.Dict[builtins.str, typing.Any]]] = None,
    max_parallel: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68eb496b82123f6e76f7d92b069e479d6fe2656dca162406a682bc24a486e7db(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6a48efaec3c02845f60a6993db7229c6a8c06976d1e70a29eec2a1d864d2fd2(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d152a7e54ef0be8ca6245b12f99b7c066028481063992853e5c56a5ac2eea5(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b188e11df5621066b88f269e802d0f1cafcd2782e126886d8efbda337aa7d7(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6c711eb2c7f80b18642b4265808197268855c9553e73591e1d303bfa5e946b(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2f1598ec4a615f2949befbc5a21abef68b4e9356692c70399a735ae5bfc902(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ddcf952a6e512a3215c2dd60c2298e08b425a12f11b25f08a117e5a710a97ea(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a60939c966ca1d7686c883fb70fa90ad963fb49908e9e6c90cfd6e63b0f9b4ed(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d726a3a5c42f73ca8f44dd1e5df516be286ce800935e40254a63a91d26659bc9(
    *,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2be95501fe49c6b6398781eb68cd6972627987fb8175dfc4dbf3bfc58eb87904(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba52f61d222ed0bbeefb8506346838919fd8fb81e32d506b342ff0d3bc8dcb6(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a371d09a416a6caffde792ea61901bcc664182e6734e337922993c2de75071a(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d0b884bc01533998bc1d20f06f8815e76bcebff37f924aaaefedfdd29ceacb(
    *,
    shell: typing.Optional[builtins.str] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f57dc86f81d3c3e3aad5080c1adfebd7d73ea6864baa1fba16a515cfa3d7629c(
    *,
    referenced_name: builtins.str,
    secret_name: builtins.str,
    secret_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc9f250cf90631093741133f9e562f42e8db4a43a40bd815f7689c8412e4f8e(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32433a930bc5c211005975ca56778a7bf9629f48745f12756bad3652d095a038(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    repo_name: builtins.str,
    jobs: typing.Optional[typing.Sequence[Job]] = None,
    workflow_name: typing.Optional[builtins.str] = None,
    workflow_path: typing.Optional[builtins.str] = None,
    workflow_triggers: typing.Optional[typing.Union[WorkflowTriggers, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9383b4468f880ecdda624b93b0bfaa3cee789b2554b3e38f5d61a626ed5027e5(
    job: Job,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e5e096eecff8f705c220786e8fa5d6ac7d573f7a278d8e863d0b1585ac3433(
    *,
    repo_name: builtins.str,
    jobs: typing.Optional[typing.Sequence[Job]] = None,
    workflow_name: typing.Optional[builtins.str] = None,
    workflow_path: typing.Optional[builtins.str] = None,
    workflow_triggers: typing.Optional[typing.Union[WorkflowTriggers, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e79ed0a6983c58278f82bfa82a680d322eae83961f769dac078fbe1169d55c(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0387f7b34704bec5f4f1b919355816eec318416e07cebd87ece23421ba7d6bc9(
    *,
    check_run: typing.Optional[typing.Union[CheckRunOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    check_suite: typing.Optional[typing.Union[CheckSuiteOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    create: typing.Optional[typing.Union[CreateOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    delete: typing.Optional[typing.Union[DeleteOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment: typing.Optional[typing.Union[DeploymentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_status: typing.Optional[typing.Union[DeploymentStatusOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    fork: typing.Optional[typing.Union[ForkOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gollum: typing.Optional[typing.Union[GollumOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    issue_comment: typing.Optional[typing.Union[IssueCommentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    issues: typing.Optional[typing.Union[IssuesOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    label: typing.Optional[typing.Union[LabelOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    milestone: typing.Optional[typing.Union[MilestoneOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    page_build: typing.Optional[typing.Union[PageBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[typing.Union[ProjectOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    project_card: typing.Optional[typing.Union[ProjectCardOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    project_column: typing.Optional[typing.Union[ProjectColumnOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    public: typing.Optional[typing.Union[PublicOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pull_request: typing.Optional[typing.Union[PullRequestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pull_request_review: typing.Optional[typing.Union[PullRequestReviewOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pull_request_review_comment: typing.Optional[typing.Union[PullRequestReviewCommentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pull_request_target: typing.Optional[typing.Union[PullRequestTargetOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    push: typing.Optional[typing.Union[PushOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    registry_package: typing.Optional[typing.Union[RegistryPackageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    release: typing.Optional[typing.Union[ReleaseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    repository_dispatch: typing.Optional[typing.Union[RepositoryDispatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: typing.Optional[typing.Sequence[typing.Union[CronScheduleOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    status: typing.Optional[typing.Union[StatusOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    watch: typing.Optional[typing.Union[WatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    workflow_dispatch: typing.Optional[typing.Union[WorkflowDispatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    workflow_run: typing.Optional[typing.Union[WorkflowRunOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7f49f93fdb8bb2ff9840c13716b8b6bb007510136e6189fa564ee4e6fa509d(
    file_path: builtins.str,
    *,
    obj: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79fddbb66dfb63556728574cf989f64cc6eb8611fa794432f9778bd5a03f9fdc(
    obj: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dcdb88b1cf90860bcd41d29610e5ee644c6dd3814cbe75f15887b9449a92b77(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c841f2c573d826862c90fc32dd4c4473708774058a00b5e0005e69f873d1349c(
    *,
    obj: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90fd62dfa4da7f32e261f2dcbf958695d5193af329b94943843cba688a126dc7(
    *,
    continue_on_error: typing.Optional[builtins.bool] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    if_: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    run: typing.Optional[builtins.str] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
    uses: typing.Optional[builtins.str] = None,
    with_: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    with_secrets: typing.Optional[typing.Sequence[typing.Union[SecretsOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28c195fbfe2acaaf2e14c0c828f64fde9aaa1a083487aa09f4a566a3995be67(
    *,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
