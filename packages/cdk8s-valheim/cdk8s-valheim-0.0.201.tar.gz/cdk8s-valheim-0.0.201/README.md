# CDK8s Valheim

This is a [CDK8s](https://cdk8s.io/) project that defines a Kubernetes deployment for [Valheim](https://www.valheimgame.com/) using the [lloesche/valheim-server](https://github.com/lloesche/valheim-server-docker) image.

## Use

A default deployment can be created with:

```python
new ValheimChart(app, 'valheim')
```

Default deployment will produce a server configured with all default [environment variables](https://github.com/lloesche/valheim-server-docker#environment-variables). The container will request resources for the games minimum recommended specs of 2 CPU and 4GB of memory.

Settings can be customized by passing in a `ValheimChartProps` object. This will allow you to configure all supported environment customizations and container configurations

```python
new ValheimChart(app, 'valheim', {
  server: {
    name: 'K8S Valheim',
    worldName: 'K8S',
    password: {
      raw: 'password',
    },
  },
})
```

## Persistence

By default, the server will store its data on a host path. This is not recommended as your world data can easily be lost.

This chart allows for storing the data on a PersistentVolumeClaim. Two pvcs can be created, one for the world data and one for the configuration. The world data is mounted at `/opt/valheim/data` directory and the configuration is mounted at `/config` directory.

To create these, the PVCs can be configured as follows:

```python
new ValheimChart(app, 'valheim'. {
    persistence: {
    server: {
      storageClass: "my-class",
    },
    config: {
      storageClass: "my-class",
    },
  },
})
```
