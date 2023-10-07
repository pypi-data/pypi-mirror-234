# AWS CDK Discord Notifier Constructs

This is a CDK construct library the vends constructs used to notify via discord about various resources and services.

## Constructs

The following constructs are available:

`MonthlyCostNotifier` - This construct will notify a discord webhook with a formatted embed of the monthly billing for the account.
`TrueNasAlertNotifier` - Creates resources to ingest a TrueNAS SNS alert by sending it to a lambda where it is parsed and sent to a discord webhook.

## Available Packages

This provider is built for the following languages:

* Javascript/Typescript
* Python
* C#

Details on how to find these packages are below and on [ConstructHub](https://constructs.dev/packages/@awlsring/cdk-aws-discord-notifiers)

### NPM

Javascript/Typescript package is available on NPM.

The npm package is viewable at https://www.npmjs.com/package/@awlsring/cdk-aws-discord-notifiers

```bash
npm install @awlsring/cdk-aws-discord-notifiers
```

### PyPi

Python package is available on PyPi.

The pypi package is viewable at https://pypi.org/project/cdk-aws-discord-notifiers/

```bash
pip install cdk-aws-discord-notifiers
```

### Nuget

C# package is available on Nuget.

The nuget package is viewable at https://www.nuget.org/packages/awlsring.CdkAwsDiscordNotifiers/

```bash
dotnet add package awlsring.CdkAwsDiscordNotifiers
```
