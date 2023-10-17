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
