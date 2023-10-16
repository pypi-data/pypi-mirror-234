'''
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

import cdk8s as _cdk8s_d3d9af27
import cdk8s_plus_26 as _cdk8s_plus_26_f7eb4715
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@awlsring/cdk8s-valheim.BackupProps",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "directory": "directory",
        "idle_grace_period": "idleGracePeriod",
        "max_backups": "maxBackups",
        "perform_if_idle": "performIfIdle",
        "permission_umask": "permissionUmask",
        "retention_age": "retentionAge",
        "schedule_cron": "scheduleCron",
        "zip": "zip",
    },
)
class BackupProps:
    def __init__(
        self,
        *,
        enabled: builtins.bool,
        directory: typing.Optional[builtins.str] = None,
        idle_grace_period: typing.Optional[jsii.Number] = None,
        max_backups: typing.Optional[jsii.Number] = None,
        perform_if_idle: typing.Optional[builtins.bool] = None,
        permission_umask: typing.Optional[builtins.str] = None,
        retention_age: typing.Optional[jsii.Number] = None,
        schedule_cron: typing.Optional[builtins.str] = None,
        zip: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Props for configuring the valheim server backups.

        :param enabled: Should backups be enabled. Default: true
        :param directory: The directory to store backups. Default: /config/backups
        :param idle_grace_period: The grace period for the server to be idle. Default: 3600s
        :param max_backups: The retention count for backups. Default: unlimited
        :param perform_if_idle: Only backup if server idle. Default: true
        :param permission_umask: Permission mask for the backup directory.
        :param retention_age: The retention age for backups. Default: 3
        :param schedule_cron: The cron schedule for the backup job. Default: 0 * * * *
        :param zip: Should the backups be zipped. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c264ff7780c484f1a5326cdabaacaaff929f5acdf98711fd644b912afa8c927e)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument directory", value=directory, expected_type=type_hints["directory"])
            check_type(argname="argument idle_grace_period", value=idle_grace_period, expected_type=type_hints["idle_grace_period"])
            check_type(argname="argument max_backups", value=max_backups, expected_type=type_hints["max_backups"])
            check_type(argname="argument perform_if_idle", value=perform_if_idle, expected_type=type_hints["perform_if_idle"])
            check_type(argname="argument permission_umask", value=permission_umask, expected_type=type_hints["permission_umask"])
            check_type(argname="argument retention_age", value=retention_age, expected_type=type_hints["retention_age"])
            check_type(argname="argument schedule_cron", value=schedule_cron, expected_type=type_hints["schedule_cron"])
            check_type(argname="argument zip", value=zip, expected_type=type_hints["zip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if directory is not None:
            self._values["directory"] = directory
        if idle_grace_period is not None:
            self._values["idle_grace_period"] = idle_grace_period
        if max_backups is not None:
            self._values["max_backups"] = max_backups
        if perform_if_idle is not None:
            self._values["perform_if_idle"] = perform_if_idle
        if permission_umask is not None:
            self._values["permission_umask"] = permission_umask
        if retention_age is not None:
            self._values["retention_age"] = retention_age
        if schedule_cron is not None:
            self._values["schedule_cron"] = schedule_cron
        if zip is not None:
            self._values["zip"] = zip

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''Should backups be enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def directory(self) -> typing.Optional[builtins.str]:
        '''The directory to store backups.

        :default: /config/backups
        '''
        result = self._values.get("directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_grace_period(self) -> typing.Optional[jsii.Number]:
        '''The grace period for the server to be idle.

        :default: 3600s
        '''
        result = self._values.get("idle_grace_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_backups(self) -> typing.Optional[jsii.Number]:
        '''The retention count for backups.

        :default: unlimited
        '''
        result = self._values.get("max_backups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def perform_if_idle(self) -> typing.Optional[builtins.bool]:
        '''Only backup if server idle.

        :default: true
        '''
        result = self._values.get("perform_if_idle")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def permission_umask(self) -> typing.Optional[builtins.str]:
        '''Permission mask for the backup directory.'''
        result = self._values.get("permission_umask")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_age(self) -> typing.Optional[jsii.Number]:
        '''The retention age for backups.

        :default: 3
        '''
        result = self._values.get("retention_age")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def schedule_cron(self) -> typing.Optional[builtins.str]:
        '''The cron schedule for the backup job.

        :default: 0 * * * *
        '''
        result = self._values.get("schedule_cron")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zip(self) -> typing.Optional[builtins.bool]:
        '''Should the backups be zipped.

        :default: true
        '''
        result = self._values.get("zip")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdk8s-valheim.PasswordProps",
    jsii_struct_bases=[],
    name_mapping={"raw": "raw", "secret": "secret"},
)
class PasswordProps:
    def __init__(
        self,
        *,
        raw: typing.Optional[builtins.str] = None,
        secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Password properties.

        Used to determine if the password should be a raw string in manifest or retrieved from an existing secret

        :param raw: The raw password string. Will be visible in manifest. Should not use.
        :param secret: The name of the secret to retrieve the password from. The secret should be stored in a key named "password"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b10a2ff508053e2f157bc94c5c8692cee63656a8c44910b9294f6a733044fa85)
            check_type(argname="argument raw", value=raw, expected_type=type_hints["raw"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if raw is not None:
            self._values["raw"] = raw
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def raw(self) -> typing.Optional[builtins.str]:
        '''The raw password string.

        Will be visible in manifest. Should not use.
        '''
        result = self._values.get("raw")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret(self) -> typing.Optional[builtins.str]:
        '''The name of the secret to retrieve the password from.

        The secret should be stored in a key named "password"
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PasswordProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdk8s-valheim.PersistanceProps",
    jsii_struct_bases=[],
    name_mapping={"config": "config", "server": "server"},
)
class PersistanceProps:
    def __init__(
        self,
        *,
        config: typing.Optional[typing.Union["PersistentVolumeClaimConfigProps", typing.Dict[builtins.str, typing.Any]]] = None,
        server: typing.Optional[typing.Union["PersistentVolumeClaimConfigProps", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param config: PVC configuration for data specific files.
        :param server: PVC configuration for server specific files.
        '''
        if isinstance(config, dict):
            config = PersistentVolumeClaimConfigProps(**config)
        if isinstance(server, dict):
            server = PersistentVolumeClaimConfigProps(**server)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f45d8688f22acbc5d39a51fb5f6cf60015ad619af12f37ebd195a5f74b9560e5)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config is not None:
            self._values["config"] = config
        if server is not None:
            self._values["server"] = server

    @builtins.property
    def config(self) -> typing.Optional["PersistentVolumeClaimConfigProps"]:
        '''PVC configuration for data specific files.'''
        result = self._values.get("config")
        return typing.cast(typing.Optional["PersistentVolumeClaimConfigProps"], result)

    @builtins.property
    def server(self) -> typing.Optional["PersistentVolumeClaimConfigProps"]:
        '''PVC configuration for server specific files.'''
        result = self._values.get("server")
        return typing.cast(typing.Optional["PersistentVolumeClaimConfigProps"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PersistanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdk8s-valheim.PersistentVolumeClaimConfigProps",
    jsii_struct_bases=[],
    name_mapping={
        "storage_class": "storageClass",
        "access_modes": "accessModes",
        "storage": "storage",
    },
)
class PersistentVolumeClaimConfigProps:
    def __init__(
        self,
        *,
        storage_class: builtins.str,
        access_modes: typing.Optional[typing.Sequence[_cdk8s_plus_26_f7eb4715.PersistentVolumeAccessMode]] = None,
        storage: typing.Optional[_cdk8s_d3d9af27.Size] = None,
    ) -> None:
        '''Props for configuring a persistent volume claim.

        :param storage_class: The name of the storage class.
        :param access_modes: The access mode from the volume. Default: = [READ_WRITE_ONCE]
        :param storage: The size of the volume.

        :see: https://kubernetes.io/docs/concepts/storage/persistent-volumes/
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84056e1fc7ec6d02a5e23b88e7f61a58bf2f75fdebdb1db5fd7044fa84813949)
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
            check_type(argname="argument access_modes", value=access_modes, expected_type=type_hints["access_modes"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "storage_class": storage_class,
        }
        if access_modes is not None:
            self._values["access_modes"] = access_modes
        if storage is not None:
            self._values["storage"] = storage

    @builtins.property
    def storage_class(self) -> builtins.str:
        '''The name of the storage class.'''
        result = self._values.get("storage_class")
        assert result is not None, "Required property 'storage_class' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_modes(
        self,
    ) -> typing.Optional[typing.List[_cdk8s_plus_26_f7eb4715.PersistentVolumeAccessMode]]:
        '''The access mode from the volume.

        :default: = [READ_WRITE_ONCE]

        :see: https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes
        '''
        result = self._values.get("access_modes")
        return typing.cast(typing.Optional[typing.List[_cdk8s_plus_26_f7eb4715.PersistentVolumeAccessMode]], result)

    @builtins.property
    def storage(self) -> typing.Optional[_cdk8s_d3d9af27.Size]:
        '''The size of the volume.

        :see: https://kubernetes.io/docs/concepts/storage/persistent-volumes/#capacity
        '''
        result = self._values.get("storage")
        return typing.cast(typing.Optional[_cdk8s_d3d9af27.Size], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PersistentVolumeClaimConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdk8s-valheim.ResourceLimitsProps",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory": "memory"},
)
class ResourceLimitsProps:
    def __init__(
        self,
        *,
        cpu: typing.Optional[typing.Union[_cdk8s_plus_26_f7eb4715.CpuResources, typing.Dict[builtins.str, typing.Any]]] = None,
        memory: typing.Optional[typing.Union[_cdk8s_plus_26_f7eb4715.MemoryResources, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Props for configuring resource limits.

        :param cpu: The CPU resources to allocate to the container. Default: = 2000m
        :param memory: The memory resources to allocate to the container. Default: = 4Gi

        :see: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
        '''
        if isinstance(cpu, dict):
            cpu = _cdk8s_plus_26_f7eb4715.CpuResources(**cpu)
        if isinstance(memory, dict):
            memory = _cdk8s_plus_26_f7eb4715.MemoryResources(**memory)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a3967a9651a36d81448049048c76b15c3087cdaa87bb61be6eb9a639f185d1)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory is not None:
            self._values["memory"] = memory

    @builtins.property
    def cpu(self) -> typing.Optional[_cdk8s_plus_26_f7eb4715.CpuResources]:
        '''The CPU resources to allocate to the container.

        :default: = 2000m

        :see: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#meaning-of-cpu
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[_cdk8s_plus_26_f7eb4715.CpuResources], result)

    @builtins.property
    def memory(self) -> typing.Optional[_cdk8s_plus_26_f7eb4715.MemoryResources]:
        '''The memory resources to allocate to the container.

        :default: = 4Gi

        :see: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#meaning-of-memory
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[_cdk8s_plus_26_f7eb4715.MemoryResources], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceLimitsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdk8s-valheim.SecurityProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_privilege_escalation": "allowPrivilegeEscalation",
        "group": "group",
        "privileged": "privileged",
        "read_only_root_filesystem": "readOnlyRootFilesystem",
        "user": "user",
    },
)
class SecurityProps:
    def __init__(
        self,
        *,
        allow_privilege_escalation: typing.Optional[builtins.bool] = None,
        group: typing.Optional[jsii.Number] = None,
        privileged: typing.Optional[builtins.bool] = None,
        read_only_root_filesystem: typing.Optional[builtins.bool] = None,
        user: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Props for configuring security aspects of the container.

        :param allow_privilege_escalation: 
        :param group: 
        :param privileged: 
        :param read_only_root_filesystem: 
        :param user: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a25616d80468fd1cf5132ae0ac4ef2b0c47a415e36f603f9deac6e3322d30521)
            check_type(argname="argument allow_privilege_escalation", value=allow_privilege_escalation, expected_type=type_hints["allow_privilege_escalation"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument privileged", value=privileged, expected_type=type_hints["privileged"])
            check_type(argname="argument read_only_root_filesystem", value=read_only_root_filesystem, expected_type=type_hints["read_only_root_filesystem"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_privilege_escalation is not None:
            self._values["allow_privilege_escalation"] = allow_privilege_escalation
        if group is not None:
            self._values["group"] = group
        if privileged is not None:
            self._values["privileged"] = privileged
        if read_only_root_filesystem is not None:
            self._values["read_only_root_filesystem"] = read_only_root_filesystem
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def allow_privilege_escalation(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("allow_privilege_escalation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def group(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("group")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def privileged(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("privileged")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def read_only_root_filesystem(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("read_only_root_filesystem")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def user(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("user")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdk8s-valheim.ServerProps",
    jsii_struct_bases=[],
    name_mapping={
        "admin_list": "adminList",
        "allow_list": "allowList",
        "block_list": "blockList",
        "crossplay": "crossplay",
        "idle_datagram_max_count": "idleDatagramMaxCount",
        "idle_datagram_window": "idleDatagramWindow",
        "launch_args": "launchArgs",
        "name": "name",
        "password": "password",
        "port": "port",
        "public": "public",
        "public_beta": "publicBeta",
        "restart_cron": "restartCron",
        "restart_if_idle": "restartIfIdle",
        "service_type": "serviceType",
        "steam_cmd_args": "steamCmdArgs",
        "timezone": "timezone",
        "update_cron": "updateCron",
        "update_when_idle": "updateWhenIdle",
        "valheim_plus": "valheimPlus",
        "world_name": "worldName",
    },
)
class ServerProps:
    def __init__(
        self,
        *,
        admin_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        block_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        crossplay: typing.Optional[builtins.bool] = None,
        idle_datagram_max_count: typing.Optional[jsii.Number] = None,
        idle_datagram_window: typing.Optional[jsii.Number] = None,
        launch_args: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        password: typing.Optional[typing.Union[PasswordProps, typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        public: typing.Optional[builtins.bool] = None,
        public_beta: typing.Optional[builtins.bool] = None,
        restart_cron: typing.Optional[builtins.str] = None,
        restart_if_idle: typing.Optional[builtins.bool] = None,
        service_type: typing.Optional[_cdk8s_plus_26_f7eb4715.ServiceType] = None,
        steam_cmd_args: typing.Optional[builtins.str] = None,
        timezone: typing.Optional[builtins.str] = None,
        update_cron: typing.Optional[builtins.str] = None,
        update_when_idle: typing.Optional[builtins.bool] = None,
        valheim_plus: typing.Optional[typing.Union["ValheimPlusProps", typing.Dict[builtins.str, typing.Any]]] = None,
        world_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Props for configuring a Valheim server.

        :param admin_list: Space separated list of admin SteamIDs in SteamID64 format. Overrides any existing adminlist.txt entries!
        :param allow_list: Space separated list of allowed SteamIDs in SteamID64 format. Overrides any existing permittedlist.txt entries!
        :param block_list: Space separated list of banned SteamIDs in SteamID64 format. Overrides any existing banlist.txt entries!
        :param crossplay: Should enable crossplay.
        :param idle_datagram_max_count: The number of incoming UDP datagrams the container should tolerate (including useless datagrams such as mDNS, as well as useful datagrams like queries against the UDP query port and active connections by players) on non-public servers before deciding that the server is not idle.
        :param idle_datagram_window: The time window, in seconds, to wait for incoming UDP datagrams on non-public servers before determining if the server is idle.
        :param launch_args: Arguments to pass to the server on start.
        :param name: The name of the server. Default: "My Server"
        :param password: The server password.
        :param port: The port the server runs on. This and the port + 1 must be open on the host The specified port is used for game conncections, and the increment port is used for the server query Default: 2456
        :param public: If the server is public. Default: true
        :param public_beta: If the beta server branch should be used.
        :param restart_cron: The server restart schedule. Default: "0 5 * * *"
        :param restart_if_idle: Only restart the server if no players are connected to the server (true or false). Default: true
        :param service_type: The service type in the cluster to expose the server on. Default: ServiceType.LOAD_BALANCER
        :param steam_cmd_args: The arguments to pass to the steamcmd command.
        :param timezone: The container timezone. Default: "Etc/UTC
        :param update_cron: The server update schedule. Default: "*/15 * * * *"
        :param update_when_idle: Only run update check if no players are connected to the server (true or false). Default: true
        :param valheim_plus: Properties for ValheimPlus.
        :param world_name: The world name. Default: "Dedicated"
        '''
        if isinstance(password, dict):
            password = PasswordProps(**password)
        if isinstance(valheim_plus, dict):
            valheim_plus = ValheimPlusProps(**valheim_plus)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__151b650527fa4a60446e13898faf6e68c9e95ee12094894aeea8910627a0a555)
            check_type(argname="argument admin_list", value=admin_list, expected_type=type_hints["admin_list"])
            check_type(argname="argument allow_list", value=allow_list, expected_type=type_hints["allow_list"])
            check_type(argname="argument block_list", value=block_list, expected_type=type_hints["block_list"])
            check_type(argname="argument crossplay", value=crossplay, expected_type=type_hints["crossplay"])
            check_type(argname="argument idle_datagram_max_count", value=idle_datagram_max_count, expected_type=type_hints["idle_datagram_max_count"])
            check_type(argname="argument idle_datagram_window", value=idle_datagram_window, expected_type=type_hints["idle_datagram_window"])
            check_type(argname="argument launch_args", value=launch_args, expected_type=type_hints["launch_args"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument public", value=public, expected_type=type_hints["public"])
            check_type(argname="argument public_beta", value=public_beta, expected_type=type_hints["public_beta"])
            check_type(argname="argument restart_cron", value=restart_cron, expected_type=type_hints["restart_cron"])
            check_type(argname="argument restart_if_idle", value=restart_if_idle, expected_type=type_hints["restart_if_idle"])
            check_type(argname="argument service_type", value=service_type, expected_type=type_hints["service_type"])
            check_type(argname="argument steam_cmd_args", value=steam_cmd_args, expected_type=type_hints["steam_cmd_args"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
            check_type(argname="argument update_cron", value=update_cron, expected_type=type_hints["update_cron"])
            check_type(argname="argument update_when_idle", value=update_when_idle, expected_type=type_hints["update_when_idle"])
            check_type(argname="argument valheim_plus", value=valheim_plus, expected_type=type_hints["valheim_plus"])
            check_type(argname="argument world_name", value=world_name, expected_type=type_hints["world_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admin_list is not None:
            self._values["admin_list"] = admin_list
        if allow_list is not None:
            self._values["allow_list"] = allow_list
        if block_list is not None:
            self._values["block_list"] = block_list
        if crossplay is not None:
            self._values["crossplay"] = crossplay
        if idle_datagram_max_count is not None:
            self._values["idle_datagram_max_count"] = idle_datagram_max_count
        if idle_datagram_window is not None:
            self._values["idle_datagram_window"] = idle_datagram_window
        if launch_args is not None:
            self._values["launch_args"] = launch_args
        if name is not None:
            self._values["name"] = name
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if public is not None:
            self._values["public"] = public
        if public_beta is not None:
            self._values["public_beta"] = public_beta
        if restart_cron is not None:
            self._values["restart_cron"] = restart_cron
        if restart_if_idle is not None:
            self._values["restart_if_idle"] = restart_if_idle
        if service_type is not None:
            self._values["service_type"] = service_type
        if steam_cmd_args is not None:
            self._values["steam_cmd_args"] = steam_cmd_args
        if timezone is not None:
            self._values["timezone"] = timezone
        if update_cron is not None:
            self._values["update_cron"] = update_cron
        if update_when_idle is not None:
            self._values["update_when_idle"] = update_when_idle
        if valheim_plus is not None:
            self._values["valheim_plus"] = valheim_plus
        if world_name is not None:
            self._values["world_name"] = world_name

    @builtins.property
    def admin_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Space separated list of admin SteamIDs in SteamID64 format.

        Overrides any existing adminlist.txt entries!
        '''
        result = self._values.get("admin_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Space separated list of allowed SteamIDs in SteamID64 format.

        Overrides any existing permittedlist.txt entries!
        '''
        result = self._values.get("allow_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def block_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Space separated list of banned SteamIDs in SteamID64 format.

        Overrides any existing banlist.txt entries!
        '''
        result = self._values.get("block_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def crossplay(self) -> typing.Optional[builtins.bool]:
        '''Should enable crossplay.'''
        result = self._values.get("crossplay")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def idle_datagram_max_count(self) -> typing.Optional[jsii.Number]:
        '''The number of incoming UDP datagrams the container should tolerate (including useless datagrams such as mDNS, as well as useful datagrams like queries against the UDP query port and active connections by players) on non-public servers before deciding that the server is not idle.'''
        result = self._values.get("idle_datagram_max_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def idle_datagram_window(self) -> typing.Optional[jsii.Number]:
        '''The time window, in seconds, to wait for incoming UDP datagrams on non-public servers before determining if the server is idle.'''
        result = self._values.get("idle_datagram_window")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def launch_args(self) -> typing.Optional[builtins.str]:
        '''Arguments to pass to the server on start.'''
        result = self._values.get("launch_args")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the server.

        :default: "My Server"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[PasswordProps]:
        '''The server password.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[PasswordProps], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port the server runs on.

        This and the port + 1 must be open on the host
        The specified port is used for game conncections, and the increment port is
        used for the server query

        :default: 2456
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def public(self) -> typing.Optional[builtins.bool]:
        '''If the server is public.

        :default: true
        '''
        result = self._values.get("public")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def public_beta(self) -> typing.Optional[builtins.bool]:
        '''If the beta server branch should be used.'''
        result = self._values.get("public_beta")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def restart_cron(self) -> typing.Optional[builtins.str]:
        '''The server restart schedule.

        :default: "0 5 * * *"
        '''
        result = self._values.get("restart_cron")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restart_if_idle(self) -> typing.Optional[builtins.bool]:
        '''Only restart the server if no players are connected to the server (true or false).

        :default: true
        '''
        result = self._values.get("restart_if_idle")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def service_type(self) -> typing.Optional[_cdk8s_plus_26_f7eb4715.ServiceType]:
        '''The service type in the cluster to expose the server on.

        :default: ServiceType.LOAD_BALANCER
        '''
        result = self._values.get("service_type")
        return typing.cast(typing.Optional[_cdk8s_plus_26_f7eb4715.ServiceType], result)

    @builtins.property
    def steam_cmd_args(self) -> typing.Optional[builtins.str]:
        '''The arguments to pass to the steamcmd command.'''
        result = self._values.get("steam_cmd_args")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''The container timezone.

        :default: "Etc/UTC
        '''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update_cron(self) -> typing.Optional[builtins.str]:
        '''The server update schedule.

        :default: "*/15 * * * *"
        '''
        result = self._values.get("update_cron")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update_when_idle(self) -> typing.Optional[builtins.bool]:
        '''Only run update check if no players are connected to the server (true or false).

        :default: true
        '''
        result = self._values.get("update_when_idle")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def valheim_plus(self) -> typing.Optional["ValheimPlusProps"]:
        '''Properties for ValheimPlus.'''
        result = self._values.get("valheim_plus")
        return typing.cast(typing.Optional["ValheimPlusProps"], result)

    @builtins.property
    def world_name(self) -> typing.Optional[builtins.str]:
        '''The world name.

        :default: "Dedicated"
        '''
        result = self._values.get("world_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdk8s-valheim.StatusHttpProps",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "config_path": "configPath",
        "htdoc_location": "htdocLocation",
        "port": "port",
        "service_type": "serviceType",
    },
)
class StatusHttpProps:
    def __init__(
        self,
        *,
        enabled: builtins.bool,
        config_path: typing.Optional[builtins.str] = None,
        htdoc_location: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        service_type: typing.Optional[_cdk8s_plus_26_f7eb4715.ServiceType] = None,
    ) -> None:
        '''Props for configuring the status http server.

        :param enabled: Should the status http server be enabled. Default: false
        :param config_path: Path to the busybox httpd config.
        :param htdoc_location: Path to the status httpd htdocs where status.json is written.
        :param port: The port the status http server runs on. Default: 80
        :param service_type: The service type for the status http server. Default: ServiceType.CLUSTER_IP
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f27ddd642c99404f3afb6fb613c058236203c662f2b47f1d9dc98e0632edffdc)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument config_path", value=config_path, expected_type=type_hints["config_path"])
            check_type(argname="argument htdoc_location", value=htdoc_location, expected_type=type_hints["htdoc_location"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument service_type", value=service_type, expected_type=type_hints["service_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if config_path is not None:
            self._values["config_path"] = config_path
        if htdoc_location is not None:
            self._values["htdoc_location"] = htdoc_location
        if port is not None:
            self._values["port"] = port
        if service_type is not None:
            self._values["service_type"] = service_type

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''Should the status http server be enabled.

        :default: false
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def config_path(self) -> typing.Optional[builtins.str]:
        '''Path to the busybox httpd config.

        :deafult: /config/httpd.conf
        '''
        result = self._values.get("config_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def htdoc_location(self) -> typing.Optional[builtins.str]:
        '''Path to the status httpd htdocs where status.json is written.

        :deafult: /opt/valheim/htdocs
        '''
        result = self._values.get("htdoc_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port the status http server runs on.

        :default: 80
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_type(self) -> typing.Optional[_cdk8s_plus_26_f7eb4715.ServiceType]:
        '''The service type for the status http server.

        :default: ServiceType.CLUSTER_IP
        '''
        result = self._values.get("service_type")
        return typing.cast(typing.Optional[_cdk8s_plus_26_f7eb4715.ServiceType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StatusHttpProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdk8s-valheim.SupervisorHttpProps",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "password": "password",
        "port": "port",
        "service_type": "serviceType",
        "username": "username",
    },
)
class SupervisorHttpProps:
    def __init__(
        self,
        *,
        enabled: builtins.bool,
        password: typing.Union[PasswordProps, typing.Dict[builtins.str, typing.Any]],
        port: typing.Optional[jsii.Number] = None,
        service_type: typing.Optional[_cdk8s_plus_26_f7eb4715.ServiceType] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Props for configuring the supervisor.

        :param enabled: Should the supervisor http server be enabled. Default: false
        :param password: The supervisor password.
        :param port: The port the supervisor http server runs on. Default: 9001
        :param service_type: The service type for the supervisor http server. Default: ServiceType.CLUSTER_IP
        :param username: The supervisor username. Default: admin
        '''
        if isinstance(password, dict):
            password = PasswordProps(**password)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78ae3e7ec9e9691dda6e769c226a7d4e2259007dec8e263cc5958f9d74daeeed)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument service_type", value=service_type, expected_type=type_hints["service_type"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "password": password,
        }
        if port is not None:
            self._values["port"] = port
        if service_type is not None:
            self._values["service_type"] = service_type
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''Should the supervisor http server be enabled.

        :default: false
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def password(self) -> PasswordProps:
        '''The supervisor password.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(PasswordProps, result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port the supervisor http server runs on.

        :default: 9001
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_type(self) -> typing.Optional[_cdk8s_plus_26_f7eb4715.ServiceType]:
        '''The service type for the supervisor http server.

        :default: ServiceType.CLUSTER_IP
        '''
        result = self._values.get("service_type")
        return typing.cast(typing.Optional[_cdk8s_plus_26_f7eb4715.ServiceType], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The supervisor username.

        :default: admin
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SupervisorHttpProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdk8s-valheim.SysLogProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_local": "logLocal",
        "remote_host": "remoteHost",
        "remote_port": "remotePort",
    },
)
class SysLogProps:
    def __init__(
        self,
        *,
        log_local: typing.Optional[builtins.bool] = None,
        remote_host: typing.Optional[builtins.str] = None,
        remote_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Props for configuring syslog.

        :param log_local: Should logging be done local.
        :param remote_host: The remote syslog host.
        :param remote_port: The remote syslog port. Default: 514
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23731290e435e1df7408bae1ee1ed19041b5a1588a4a2df202cf0bfab0d7af88)
            check_type(argname="argument log_local", value=log_local, expected_type=type_hints["log_local"])
            check_type(argname="argument remote_host", value=remote_host, expected_type=type_hints["remote_host"])
            check_type(argname="argument remote_port", value=remote_port, expected_type=type_hints["remote_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_local is not None:
            self._values["log_local"] = log_local
        if remote_host is not None:
            self._values["remote_host"] = remote_host
        if remote_port is not None:
            self._values["remote_port"] = remote_port

    @builtins.property
    def log_local(self) -> typing.Optional[builtins.bool]:
        '''Should logging be done local.'''
        result = self._values.get("log_local")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def remote_host(self) -> typing.Optional[builtins.str]:
        '''The remote syslog host.'''
        result = self._values.get("remote_host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_port(self) -> typing.Optional[jsii.Number]:
        '''The remote syslog port.

        :default: 514
        '''
        result = self._values.get("remote_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SysLogProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ValheimChart(
    _cdk8s_d3d9af27.Chart,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdk8s-valheim.ValheimChart",
):
    '''A chart to deploy a Valheim server Uses the container by @lloesche.

    :see: https://github.com/lloesche/valheim-server-docker
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        name: builtins.str,
        *,
        backup: typing.Optional[typing.Union[BackupProps, typing.Dict[builtins.str, typing.Any]]] = None,
        image_tag: typing.Optional[builtins.str] = None,
        persistence: typing.Optional[typing.Union[PersistanceProps, typing.Dict[builtins.str, typing.Any]]] = None,
        resource_limits: typing.Optional[typing.Union[ResourceLimitsProps, typing.Dict[builtins.str, typing.Any]]] = None,
        security: typing.Optional[typing.Union[SecurityProps, typing.Dict[builtins.str, typing.Any]]] = None,
        server: typing.Optional[typing.Union[ServerProps, typing.Dict[builtins.str, typing.Any]]] = None,
        status_http: typing.Optional[typing.Union[StatusHttpProps, typing.Dict[builtins.str, typing.Any]]] = None,
        supervisor_http: typing.Optional[typing.Union[SupervisorHttpProps, typing.Dict[builtins.str, typing.Any]]] = None,
        sys_log: typing.Optional[typing.Union[SysLogProps, typing.Dict[builtins.str, typing.Any]]] = None,
        disable_resource_name_hashes: typing.Optional[builtins.bool] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param backup: 
        :param image_tag: 
        :param persistence: 
        :param resource_limits: 
        :param security: 
        :param server: 
        :param status_http: 
        :param supervisor_http: 
        :param sys_log: 
        :param disable_resource_name_hashes: The autogenerated resource name by default is suffixed with a stable hash of the construct path. Setting this property to true drops the hash suffix. Default: false
        :param labels: Labels to apply to all resources in this chart. Default: - no common labels
        :param namespace: The default namespace for all objects defined in this chart (directly or indirectly). This namespace will only apply to objects that don't have a ``namespace`` explicitly defined for them. Default: - no namespace is synthesized (usually this implies "default")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d01c9553c44cdee780e5d7641379a94a3ec85a53ae32074e5064800ee03f7433)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = ValheimChartProps(
            backup=backup,
            image_tag=image_tag,
            persistence=persistence,
            resource_limits=resource_limits,
            security=security,
            server=server,
            status_http=status_http,
            supervisor_http=supervisor_http,
            sys_log=sys_log,
            disable_resource_name_hashes=disable_resource_name_hashes,
            labels=labels,
            namespace=namespace,
        )

        jsii.create(self.__class__, self, [scope, name, props])


@jsii.data_type(
    jsii_type="@awlsring/cdk8s-valheim.ValheimChartProps",
    jsii_struct_bases=[_cdk8s_d3d9af27.ChartProps],
    name_mapping={
        "disable_resource_name_hashes": "disableResourceNameHashes",
        "labels": "labels",
        "namespace": "namespace",
        "backup": "backup",
        "image_tag": "imageTag",
        "persistence": "persistence",
        "resource_limits": "resourceLimits",
        "security": "security",
        "server": "server",
        "status_http": "statusHttp",
        "supervisor_http": "supervisorHttp",
        "sys_log": "sysLog",
    },
)
class ValheimChartProps(_cdk8s_d3d9af27.ChartProps):
    def __init__(
        self,
        *,
        disable_resource_name_hashes: typing.Optional[builtins.bool] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
        backup: typing.Optional[typing.Union[BackupProps, typing.Dict[builtins.str, typing.Any]]] = None,
        image_tag: typing.Optional[builtins.str] = None,
        persistence: typing.Optional[typing.Union[PersistanceProps, typing.Dict[builtins.str, typing.Any]]] = None,
        resource_limits: typing.Optional[typing.Union[ResourceLimitsProps, typing.Dict[builtins.str, typing.Any]]] = None,
        security: typing.Optional[typing.Union[SecurityProps, typing.Dict[builtins.str, typing.Any]]] = None,
        server: typing.Optional[typing.Union[ServerProps, typing.Dict[builtins.str, typing.Any]]] = None,
        status_http: typing.Optional[typing.Union[StatusHttpProps, typing.Dict[builtins.str, typing.Any]]] = None,
        supervisor_http: typing.Optional[typing.Union[SupervisorHttpProps, typing.Dict[builtins.str, typing.Any]]] = None,
        sys_log: typing.Optional[typing.Union[SysLogProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''The props for the chart.

        :param disable_resource_name_hashes: The autogenerated resource name by default is suffixed with a stable hash of the construct path. Setting this property to true drops the hash suffix. Default: false
        :param labels: Labels to apply to all resources in this chart. Default: - no common labels
        :param namespace: The default namespace for all objects defined in this chart (directly or indirectly). This namespace will only apply to objects that don't have a ``namespace`` explicitly defined for them. Default: - no namespace is synthesized (usually this implies "default")
        :param backup: 
        :param image_tag: 
        :param persistence: 
        :param resource_limits: 
        :param security: 
        :param server: 
        :param status_http: 
        :param supervisor_http: 
        :param sys_log: 
        '''
        if isinstance(backup, dict):
            backup = BackupProps(**backup)
        if isinstance(persistence, dict):
            persistence = PersistanceProps(**persistence)
        if isinstance(resource_limits, dict):
            resource_limits = ResourceLimitsProps(**resource_limits)
        if isinstance(security, dict):
            security = SecurityProps(**security)
        if isinstance(server, dict):
            server = ServerProps(**server)
        if isinstance(status_http, dict):
            status_http = StatusHttpProps(**status_http)
        if isinstance(supervisor_http, dict):
            supervisor_http = SupervisorHttpProps(**supervisor_http)
        if isinstance(sys_log, dict):
            sys_log = SysLogProps(**sys_log)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e68bced55517921304998b25fa497e6f978a9d5dae610e902fbd8850275e654)
            check_type(argname="argument disable_resource_name_hashes", value=disable_resource_name_hashes, expected_type=type_hints["disable_resource_name_hashes"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument backup", value=backup, expected_type=type_hints["backup"])
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
            check_type(argname="argument persistence", value=persistence, expected_type=type_hints["persistence"])
            check_type(argname="argument resource_limits", value=resource_limits, expected_type=type_hints["resource_limits"])
            check_type(argname="argument security", value=security, expected_type=type_hints["security"])
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
            check_type(argname="argument status_http", value=status_http, expected_type=type_hints["status_http"])
            check_type(argname="argument supervisor_http", value=supervisor_http, expected_type=type_hints["supervisor_http"])
            check_type(argname="argument sys_log", value=sys_log, expected_type=type_hints["sys_log"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable_resource_name_hashes is not None:
            self._values["disable_resource_name_hashes"] = disable_resource_name_hashes
        if labels is not None:
            self._values["labels"] = labels
        if namespace is not None:
            self._values["namespace"] = namespace
        if backup is not None:
            self._values["backup"] = backup
        if image_tag is not None:
            self._values["image_tag"] = image_tag
        if persistence is not None:
            self._values["persistence"] = persistence
        if resource_limits is not None:
            self._values["resource_limits"] = resource_limits
        if security is not None:
            self._values["security"] = security
        if server is not None:
            self._values["server"] = server
        if status_http is not None:
            self._values["status_http"] = status_http
        if supervisor_http is not None:
            self._values["supervisor_http"] = supervisor_http
        if sys_log is not None:
            self._values["sys_log"] = sys_log

    @builtins.property
    def disable_resource_name_hashes(self) -> typing.Optional[builtins.bool]:
        '''The autogenerated resource name by default is suffixed with a stable hash of the construct path.

        Setting this property to true drops the hash suffix.

        :default: false
        '''
        result = self._values.get("disable_resource_name_hashes")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to apply to all resources in this chart.

        :default: - no common labels
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The default namespace for all objects defined in this chart (directly or indirectly).

        This namespace will only apply to objects that don't have a
        ``namespace`` explicitly defined for them.

        :default: - no namespace is synthesized (usually this implies "default")
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup(self) -> typing.Optional[BackupProps]:
        result = self._values.get("backup")
        return typing.cast(typing.Optional[BackupProps], result)

    @builtins.property
    def image_tag(self) -> typing.Optional[builtins.str]:
        result = self._values.get("image_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def persistence(self) -> typing.Optional[PersistanceProps]:
        result = self._values.get("persistence")
        return typing.cast(typing.Optional[PersistanceProps], result)

    @builtins.property
    def resource_limits(self) -> typing.Optional[ResourceLimitsProps]:
        result = self._values.get("resource_limits")
        return typing.cast(typing.Optional[ResourceLimitsProps], result)

    @builtins.property
    def security(self) -> typing.Optional[SecurityProps]:
        result = self._values.get("security")
        return typing.cast(typing.Optional[SecurityProps], result)

    @builtins.property
    def server(self) -> typing.Optional[ServerProps]:
        result = self._values.get("server")
        return typing.cast(typing.Optional[ServerProps], result)

    @builtins.property
    def status_http(self) -> typing.Optional[StatusHttpProps]:
        result = self._values.get("status_http")
        return typing.cast(typing.Optional[StatusHttpProps], result)

    @builtins.property
    def supervisor_http(self) -> typing.Optional[SupervisorHttpProps]:
        result = self._values.get("supervisor_http")
        return typing.cast(typing.Optional[SupervisorHttpProps], result)

    @builtins.property
    def sys_log(self) -> typing.Optional[SysLogProps]:
        result = self._values.get("sys_log")
        return typing.cast(typing.Optional[SysLogProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ValheimChartProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdk8s-valheim.ValheimPlusProps",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "release": "release"},
)
class ValheimPlusProps:
    def __init__(
        self,
        *,
        enabled: builtins.bool,
        release: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Props for configuring valheim plus.

        :param enabled: Should valheim plus be enabled. Default: false
        :param release: The version of valheim plus to use. Default: latest
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48b2975f830e30d4d97df6eab5e593a5ffa68886d51b3bcf1dae6aee3ded687d)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument release", value=release, expected_type=type_hints["release"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if release is not None:
            self._values["release"] = release

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''Should valheim plus be enabled.

        :default: false
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def release(self) -> typing.Optional[builtins.str]:
        '''The version of valheim plus to use.

        :default: latest
        '''
        result = self._values.get("release")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ValheimPlusProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BackupProps",
    "PasswordProps",
    "PersistanceProps",
    "PersistentVolumeClaimConfigProps",
    "ResourceLimitsProps",
    "SecurityProps",
    "ServerProps",
    "StatusHttpProps",
    "SupervisorHttpProps",
    "SysLogProps",
    "ValheimChart",
    "ValheimChartProps",
    "ValheimPlusProps",
]

publication.publish()

def _typecheckingstub__c264ff7780c484f1a5326cdabaacaaff929f5acdf98711fd644b912afa8c927e(
    *,
    enabled: builtins.bool,
    directory: typing.Optional[builtins.str] = None,
    idle_grace_period: typing.Optional[jsii.Number] = None,
    max_backups: typing.Optional[jsii.Number] = None,
    perform_if_idle: typing.Optional[builtins.bool] = None,
    permission_umask: typing.Optional[builtins.str] = None,
    retention_age: typing.Optional[jsii.Number] = None,
    schedule_cron: typing.Optional[builtins.str] = None,
    zip: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10a2ff508053e2f157bc94c5c8692cee63656a8c44910b9294f6a733044fa85(
    *,
    raw: typing.Optional[builtins.str] = None,
    secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f45d8688f22acbc5d39a51fb5f6cf60015ad619af12f37ebd195a5f74b9560e5(
    *,
    config: typing.Optional[typing.Union[PersistentVolumeClaimConfigProps, typing.Dict[builtins.str, typing.Any]]] = None,
    server: typing.Optional[typing.Union[PersistentVolumeClaimConfigProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84056e1fc7ec6d02a5e23b88e7f61a58bf2f75fdebdb1db5fd7044fa84813949(
    *,
    storage_class: builtins.str,
    access_modes: typing.Optional[typing.Sequence[_cdk8s_plus_26_f7eb4715.PersistentVolumeAccessMode]] = None,
    storage: typing.Optional[_cdk8s_d3d9af27.Size] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a3967a9651a36d81448049048c76b15c3087cdaa87bb61be6eb9a639f185d1(
    *,
    cpu: typing.Optional[typing.Union[_cdk8s_plus_26_f7eb4715.CpuResources, typing.Dict[builtins.str, typing.Any]]] = None,
    memory: typing.Optional[typing.Union[_cdk8s_plus_26_f7eb4715.MemoryResources, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25616d80468fd1cf5132ae0ac4ef2b0c47a415e36f603f9deac6e3322d30521(
    *,
    allow_privilege_escalation: typing.Optional[builtins.bool] = None,
    group: typing.Optional[jsii.Number] = None,
    privileged: typing.Optional[builtins.bool] = None,
    read_only_root_filesystem: typing.Optional[builtins.bool] = None,
    user: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151b650527fa4a60446e13898faf6e68c9e95ee12094894aeea8910627a0a555(
    *,
    admin_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    block_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    crossplay: typing.Optional[builtins.bool] = None,
    idle_datagram_max_count: typing.Optional[jsii.Number] = None,
    idle_datagram_window: typing.Optional[jsii.Number] = None,
    launch_args: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    password: typing.Optional[typing.Union[PasswordProps, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[jsii.Number] = None,
    public: typing.Optional[builtins.bool] = None,
    public_beta: typing.Optional[builtins.bool] = None,
    restart_cron: typing.Optional[builtins.str] = None,
    restart_if_idle: typing.Optional[builtins.bool] = None,
    service_type: typing.Optional[_cdk8s_plus_26_f7eb4715.ServiceType] = None,
    steam_cmd_args: typing.Optional[builtins.str] = None,
    timezone: typing.Optional[builtins.str] = None,
    update_cron: typing.Optional[builtins.str] = None,
    update_when_idle: typing.Optional[builtins.bool] = None,
    valheim_plus: typing.Optional[typing.Union[ValheimPlusProps, typing.Dict[builtins.str, typing.Any]]] = None,
    world_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27ddd642c99404f3afb6fb613c058236203c662f2b47f1d9dc98e0632edffdc(
    *,
    enabled: builtins.bool,
    config_path: typing.Optional[builtins.str] = None,
    htdoc_location: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    service_type: typing.Optional[_cdk8s_plus_26_f7eb4715.ServiceType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ae3e7ec9e9691dda6e769c226a7d4e2259007dec8e263cc5958f9d74daeeed(
    *,
    enabled: builtins.bool,
    password: typing.Union[PasswordProps, typing.Dict[builtins.str, typing.Any]],
    port: typing.Optional[jsii.Number] = None,
    service_type: typing.Optional[_cdk8s_plus_26_f7eb4715.ServiceType] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23731290e435e1df7408bae1ee1ed19041b5a1588a4a2df202cf0bfab0d7af88(
    *,
    log_local: typing.Optional[builtins.bool] = None,
    remote_host: typing.Optional[builtins.str] = None,
    remote_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d01c9553c44cdee780e5d7641379a94a3ec85a53ae32074e5064800ee03f7433(
    scope: _constructs_77d1e7e8.Construct,
    name: builtins.str,
    *,
    backup: typing.Optional[typing.Union[BackupProps, typing.Dict[builtins.str, typing.Any]]] = None,
    image_tag: typing.Optional[builtins.str] = None,
    persistence: typing.Optional[typing.Union[PersistanceProps, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_limits: typing.Optional[typing.Union[ResourceLimitsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    security: typing.Optional[typing.Union[SecurityProps, typing.Dict[builtins.str, typing.Any]]] = None,
    server: typing.Optional[typing.Union[ServerProps, typing.Dict[builtins.str, typing.Any]]] = None,
    status_http: typing.Optional[typing.Union[StatusHttpProps, typing.Dict[builtins.str, typing.Any]]] = None,
    supervisor_http: typing.Optional[typing.Union[SupervisorHttpProps, typing.Dict[builtins.str, typing.Any]]] = None,
    sys_log: typing.Optional[typing.Union[SysLogProps, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_resource_name_hashes: typing.Optional[builtins.bool] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e68bced55517921304998b25fa497e6f978a9d5dae610e902fbd8850275e654(
    *,
    disable_resource_name_hashes: typing.Optional[builtins.bool] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
    backup: typing.Optional[typing.Union[BackupProps, typing.Dict[builtins.str, typing.Any]]] = None,
    image_tag: typing.Optional[builtins.str] = None,
    persistence: typing.Optional[typing.Union[PersistanceProps, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_limits: typing.Optional[typing.Union[ResourceLimitsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    security: typing.Optional[typing.Union[SecurityProps, typing.Dict[builtins.str, typing.Any]]] = None,
    server: typing.Optional[typing.Union[ServerProps, typing.Dict[builtins.str, typing.Any]]] = None,
    status_http: typing.Optional[typing.Union[StatusHttpProps, typing.Dict[builtins.str, typing.Any]]] = None,
    supervisor_http: typing.Optional[typing.Union[SupervisorHttpProps, typing.Dict[builtins.str, typing.Any]]] = None,
    sys_log: typing.Optional[typing.Union[SysLogProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48b2975f830e30d4d97df6eab5e593a5ffa68886d51b3bcf1dae6aee3ded687d(
    *,
    enabled: builtins.bool,
    release: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
