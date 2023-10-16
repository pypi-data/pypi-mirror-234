'''
# Terraform CDK spotinst Provider ~> 1.0

This repo builds and publishes the Terraform spotinst Provider bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-spotinst](https://www.npmjs.com/package/@cdktf/provider-spotinst).

`npm install @cdktf/provider-spotinst`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-spotinst](https://pypi.org/project/cdktf-cdktf-provider-spotinst).

`pipenv install cdktf-cdktf-provider-spotinst`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Spotinst](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Spotinst).

`dotnet add package HashiCorp.Cdktf.Providers.Spotinst`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-spotinst](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-spotinst).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-spotinst</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-spotinst-go`](https://github.com/cdktf/cdktf-provider-spotinst-go) package.

`go get github.com/cdktf/cdktf-provider-spotinst-go/spotinst`

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-spotinst).

## Versioning

This project is explicitly not tracking the Terraform spotinst Provider version 1:1. In fact, it always tracks `latest` of `~> 1.0` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by generating the [provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [Terraform CDK](https://cdk.tf)
* [Terraform spotinst Provider](https://registry.terraform.io/providers/spotinst/spotinst/1.0.0)

  * This links to the minimum version being tracked, you can find the latest released version [in our releases](https://github.com/cdktf/cdktf-provider-spotinst/releases)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped.

## Features / Issues / Bugs

Please report bugs and issues to the [terraform cdk](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

### projen

This is mostly based on [projen](https://github.com/eladb/projen), which takes care of generating the entire repository.

### cdktf-provider-project based on projen

There's a custom [project builder](https://github.com/hashicorp/cdktf-provider-project) which encapsulate the common settings for all `cdktf` providers.

### Provider Version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).

### Repository Management

The repository is managed by [Repository Manager](https://github.com/hashicorp/cdktf-repository-manager/)
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

__all__ = [
    "account_aws",
    "credentials_aws",
    "data_integration",
    "elastigroup_aws",
    "elastigroup_aws_beanstalk",
    "elastigroup_aws_suspension",
    "elastigroup_azure",
    "elastigroup_azure_v3",
    "elastigroup_gcp",
    "elastigroup_gke",
    "health_check",
    "managed_instance_aws",
    "mrscaler_aws",
    "multai_balancer",
    "multai_deployment",
    "multai_listener",
    "multai_routing_rule",
    "multai_target",
    "multai_target_set",
    "ocean_aks",
    "ocean_aks_np",
    "ocean_aks_np_virtual_node_group",
    "ocean_aks_virtual_node_group",
    "ocean_aws",
    "ocean_aws_extended_resource_definition",
    "ocean_aws_launch_spec",
    "ocean_ecs",
    "ocean_ecs_launch_spec",
    "ocean_gke_import",
    "ocean_gke_launch_spec",
    "ocean_gke_launch_spec_import",
    "ocean_spark",
    "ocean_spark_virtual_node_group",
    "organization_policy",
    "organization_programmatic_user",
    "organization_user",
    "organization_user_group",
    "provider",
    "stateful_node_azure",
    "subscription",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import account_aws
from . import credentials_aws
from . import data_integration
from . import elastigroup_aws
from . import elastigroup_aws_beanstalk
from . import elastigroup_aws_suspension
from . import elastigroup_azure
from . import elastigroup_azure_v3
from . import elastigroup_gcp
from . import elastigroup_gke
from . import health_check
from . import managed_instance_aws
from . import mrscaler_aws
from . import multai_balancer
from . import multai_deployment
from . import multai_listener
from . import multai_routing_rule
from . import multai_target
from . import multai_target_set
from . import ocean_aks
from . import ocean_aks_np
from . import ocean_aks_np_virtual_node_group
from . import ocean_aks_virtual_node_group
from . import ocean_aws
from . import ocean_aws_extended_resource_definition
from . import ocean_aws_launch_spec
from . import ocean_ecs
from . import ocean_ecs_launch_spec
from . import ocean_gke_import
from . import ocean_gke_launch_spec
from . import ocean_gke_launch_spec_import
from . import ocean_spark
from . import ocean_spark_virtual_node_group
from . import organization_policy
from . import organization_programmatic_user
from . import organization_user
from . import organization_user_group
from . import provider
from . import stateful_node_azure
from . import subscription
