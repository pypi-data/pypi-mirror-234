import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

from .. import (
    Component as _Component_2b0ad27f,
    DependencyType as _DependencyType_6b786d68,
    GitOptions as _GitOptions_a65916a3,
    GroupRunnerOptions as _GroupRunnerOptions_148c59c1,
    IgnoreFile as _IgnoreFile_3df2076a,
    IgnoreFileOptions as _IgnoreFileOptions_86c48b91,
    JsonFile as _JsonFile_fa8164db,
    LoggerOptions as _LoggerOptions_eb0f6309,
    Project as _Project_57d89203,
    ProjectType as _ProjectType_fd80c725,
    ProjenrcFile as _ProjenrcFile_50432c7e,
    ProjenrcJsonOptions as _ProjenrcJsonOptions_9c40dd4f,
    ReleasableCommits as _ReleasableCommits_d481ce10,
    RenovatebotOptions as _RenovatebotOptions_18e6b8a1,
    SampleReadmeProps as _SampleReadmeProps_3518b03b,
    Task as _Task_9fa875b6,
)
from ..build import BuildWorkflow as _BuildWorkflow_bdd5e6cc
from ..github import (
    AutoApproveOptions as _AutoApproveOptions_dac86cbe,
    AutoMerge as _AutoMerge_f73f9be0,
    AutoMergeOptions as _AutoMergeOptions_d112cd3c,
    DependabotOptions as _DependabotOptions_0cedc635,
    GitHubOptions as _GitHubOptions_21553699,
    GitHubProject as _GitHubProject_c48bc7ea,
    GitHubProjectOptions as _GitHubProjectOptions_547f2d08,
    GitIdentity as _GitIdentity_6effc3de,
    GithubCredentials as _GithubCredentials_ae257072,
    GithubWorkflow as _GithubWorkflow_a1772357,
    MergifyOptions as _MergifyOptions_a6faaab3,
    StaleOptions as _StaleOptions_929db764,
)
from ..github.workflows import (
    ContainerOptions as _ContainerOptions_f50907af,
    JobPermissions as _JobPermissions_3b5b53dc,
    JobStep as _JobStep_c3287c05,
    Triggers as _Triggers_e9ae7617,
)
from ..release import (
    BranchOptions as _BranchOptions_13663d08,
    Publisher as _Publisher_4a29b2cd,
    Release as _Release_30ee2d91,
    ReleaseProjectOptions as _ReleaseProjectOptions_929803c8,
    ReleaseTrigger as _ReleaseTrigger_e4dc221f,
)


@jsii.enum(jsii_type="projen.javascript.ArrowParens")
class ArrowParens(enum.Enum):
    '''
    :stability: experimental
    '''

    ALWAYS = "ALWAYS"
    '''(experimental) Always include parens.

    Example: ``(x) => x``

    :stability: experimental
    '''
    AVOID = "AVOID"
    '''(experimental) Omit parens when possible.

    Example: ``x => x``

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.javascript.AutoRelease")
class AutoRelease(enum.Enum):
    '''(experimental) Automatic bump modes.

    :stability: experimental
    '''

    EVERY_COMMIT = "EVERY_COMMIT"
    '''(experimental) Automatically bump & release a new version for every commit to "main".

    :stability: experimental
    '''
    DAILY = "DAILY"
    '''(experimental) Automatically bump & release a new version on a daily basis.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.javascript.Bundle",
    jsii_struct_bases=[],
    name_mapping={
        "bundle_task": "bundleTask",
        "outdir": "outdir",
        "outfile": "outfile",
        "watch_task": "watchTask",
    },
)
class Bundle:
    def __init__(
        self,
        *,
        bundle_task: _Task_9fa875b6,
        outdir: builtins.str,
        outfile: builtins.str,
        watch_task: typing.Optional[_Task_9fa875b6] = None,
    ) -> None:
        '''
        :param bundle_task: (experimental) The task that produces this bundle.
        :param outdir: (experimental) Base directory containing the output file (relative to project root).
        :param outfile: (experimental) Location of the output file (relative to project root).
        :param watch_task: (experimental) The "watch" task for this bundle.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61e51544f8a1488a41b14a0ee08df5b86eb83b8852c5ea8c95747007b7c012de)
            check_type(argname="argument bundle_task", value=bundle_task, expected_type=type_hints["bundle_task"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument outfile", value=outfile, expected_type=type_hints["outfile"])
            check_type(argname="argument watch_task", value=watch_task, expected_type=type_hints["watch_task"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bundle_task": bundle_task,
            "outdir": outdir,
            "outfile": outfile,
        }
        if watch_task is not None:
            self._values["watch_task"] = watch_task

    @builtins.property
    def bundle_task(self) -> _Task_9fa875b6:
        '''(experimental) The task that produces this bundle.

        :stability: experimental
        '''
        result = self._values.get("bundle_task")
        assert result is not None, "Required property 'bundle_task' is missing"
        return typing.cast(_Task_9fa875b6, result)

    @builtins.property
    def outdir(self) -> builtins.str:
        '''(experimental) Base directory containing the output file (relative to project root).

        :stability: experimental
        '''
        result = self._values.get("outdir")
        assert result is not None, "Required property 'outdir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def outfile(self) -> builtins.str:
        '''(experimental) Location of the output file (relative to project root).

        :stability: experimental
        '''
        result = self._values.get("outfile")
        assert result is not None, "Required property 'outfile' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def watch_task(self) -> typing.Optional[_Task_9fa875b6]:
        '''(experimental) The "watch" task for this bundle.

        :stability: experimental
        '''
        result = self._values.get("watch_task")
        return typing.cast(typing.Optional[_Task_9fa875b6], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Bundle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Bundler(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.javascript.Bundler",
):
    '''(experimental) Adds support for bundling JavaScript applications and dependencies into a single file.

    In the future, this will also supports bundling websites.

    :stability: experimental
    '''

    def __init__(
        self,
        project: _Project_57d89203,
        *,
        add_to_pre_compile: typing.Optional[builtins.bool] = None,
        assets_dir: typing.Optional[builtins.str] = None,
        esbuild_version: typing.Optional[builtins.str] = None,
        loaders: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Creates a ``Bundler``.

        :param project: -
        :param add_to_pre_compile: (experimental) Install the ``bundle`` command as a pre-compile phase. Default: true
        :param assets_dir: (experimental) Output directory for all bundles. Default: "assets"
        :param esbuild_version: (experimental) The semantic version requirement for ``esbuild``. Default: - no specific version (implies latest)
        :param loaders: (experimental) Map of file extensions (without dot) and loaders to use for this file type. Loaders are appended to the esbuild command by ``--loader:.extension=loader``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39a2a4441a612906ad5a7b87f1a6c53ed88fb86f4e31bd1a7283a06a2e9ebf7)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = BundlerOptions(
            add_to_pre_compile=add_to_pre_compile,
            assets_dir=assets_dir,
            esbuild_version=esbuild_version,
            loaders=loaders,
        )

        jsii.create(self.__class__, self, [project, options])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, project: _Project_57d89203) -> typing.Optional["Bundler"]:
        '''(experimental) Returns the ``Bundler`` instance associated with a project or ``undefined`` if there is no Bundler.

        :param project: The project.

        :return: A bundler

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bef383122352b305e57b5282e27bdaa8a9889f1dd224d03d28a1c2cc73120b0)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        return typing.cast(typing.Optional["Bundler"], jsii.sinvoke(cls, "of", [project]))

    @jsii.member(jsii_name="addBundle")
    def add_bundle(
        self,
        entrypoint: builtins.str,
        *,
        platform: builtins.str,
        target: builtins.str,
        executable: typing.Optional[builtins.bool] = None,
        loaders: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        outfile: typing.Optional[builtins.str] = None,
        tsconfig_path: typing.Optional[builtins.str] = None,
        externals: typing.Optional[typing.Sequence[builtins.str]] = None,
        sourcemap: typing.Optional[builtins.bool] = None,
        watch_task: typing.Optional[builtins.bool] = None,
    ) -> Bundle:
        '''(experimental) Adds a task to the project which bundles a specific entrypoint and all of its dependencies into a single javascript output file.

        :param entrypoint: The relative path of the artifact within the project.
        :param platform: (experimental) esbuild platform.
        :param target: (experimental) esbuild target.
        :param executable: (experimental) Mark the output file as executable. Default: false
        :param loaders: (experimental) Map of file extensions (without dot) and loaders to use for this file type. Loaders are appended to the esbuild command by ``--loader:.extension=loader``
        :param outfile: (experimental) Bundler output path relative to the asset's output directory. Default: "index.js"
        :param tsconfig_path: (experimental) The path of the tsconfig.json file to use for bundling. Default: "tsconfig.json"
        :param externals: (experimental) You can mark a file or a package as external to exclude it from your build. Instead of being bundled, the import will be preserved (using require for the iife and cjs formats and using import for the esm format) and will be evaluated at run time instead. This has several uses. First of all, it can be used to trim unnecessary code from your bundle for a code path that you know will never be executed. For example, a package may contain code that only runs in node but you will only be using that package in the browser. It can also be used to import code in node at run time from a package that cannot be bundled. For example, the fsevents package contains a native extension, which esbuild doesn't support. Default: []
        :param sourcemap: (experimental) Include a source map in the bundle. Default: false
        :param watch_task: (experimental) In addition to the ``bundle:xyz`` task, creates ``bundle:xyz:watch`` task which will invoke the same esbuild command with the ``--watch`` flag. This can be used to continusouly watch for changes. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3fe067eb8c7b6b184c855eea4d40743f016f5de6e522e14523a7e7695ad811)
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
        options = AddBundleOptions(
            platform=platform,
            target=target,
            executable=executable,
            loaders=loaders,
            outfile=outfile,
            tsconfig_path=tsconfig_path,
            externals=externals,
            sourcemap=sourcemap,
            watch_task=watch_task,
        )

        return typing.cast(Bundle, jsii.invoke(self, "addBundle", [entrypoint, options]))

    @builtins.property
    @jsii.member(jsii_name="bundledir")
    def bundledir(self) -> builtins.str:
        '''(experimental) Root bundle directory.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bundledir"))

    @builtins.property
    @jsii.member(jsii_name="bundleTask")
    def bundle_task(self) -> _Task_9fa875b6:
        '''(experimental) Gets or creates the singleton "bundle" task of the project.

        If the project doesn't have a "bundle" task, it will be created and spawned
        during the pre-compile phase.

        :stability: experimental
        '''
        return typing.cast(_Task_9fa875b6, jsii.get(self, "bundleTask"))

    @builtins.property
    @jsii.member(jsii_name="esbuildVersion")
    def esbuild_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The semantic version requirement for ``esbuild`` (if defined).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "esbuildVersion"))


@jsii.data_type(
    jsii_type="projen.javascript.BundlerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "add_to_pre_compile": "addToPreCompile",
        "assets_dir": "assetsDir",
        "esbuild_version": "esbuildVersion",
        "loaders": "loaders",
    },
)
class BundlerOptions:
    def __init__(
        self,
        *,
        add_to_pre_compile: typing.Optional[builtins.bool] = None,
        assets_dir: typing.Optional[builtins.str] = None,
        esbuild_version: typing.Optional[builtins.str] = None,
        loaders: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for ``Bundler``.

        :param add_to_pre_compile: (experimental) Install the ``bundle`` command as a pre-compile phase. Default: true
        :param assets_dir: (experimental) Output directory for all bundles. Default: "assets"
        :param esbuild_version: (experimental) The semantic version requirement for ``esbuild``. Default: - no specific version (implies latest)
        :param loaders: (experimental) Map of file extensions (without dot) and loaders to use for this file type. Loaders are appended to the esbuild command by ``--loader:.extension=loader``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a14ca8f2b867bbbf0d45b5661abe92e6975540f78ea16f7ed21f5f213c4913)
            check_type(argname="argument add_to_pre_compile", value=add_to_pre_compile, expected_type=type_hints["add_to_pre_compile"])
            check_type(argname="argument assets_dir", value=assets_dir, expected_type=type_hints["assets_dir"])
            check_type(argname="argument esbuild_version", value=esbuild_version, expected_type=type_hints["esbuild_version"])
            check_type(argname="argument loaders", value=loaders, expected_type=type_hints["loaders"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_to_pre_compile is not None:
            self._values["add_to_pre_compile"] = add_to_pre_compile
        if assets_dir is not None:
            self._values["assets_dir"] = assets_dir
        if esbuild_version is not None:
            self._values["esbuild_version"] = esbuild_version
        if loaders is not None:
            self._values["loaders"] = loaders

    @builtins.property
    def add_to_pre_compile(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Install the ``bundle`` command as a pre-compile phase.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("add_to_pre_compile")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def assets_dir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Output directory for all bundles.

        :default: "assets"

        :stability: experimental
        '''
        result = self._values.get("assets_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def esbuild_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The semantic version requirement for ``esbuild``.

        :default: - no specific version (implies latest)

        :stability: experimental
        '''
        result = self._values.get("esbuild_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def loaders(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Map of file extensions (without dot) and loaders to use for this file type.

        Loaders are appended to the esbuild command by ``--loader:.extension=loader``

        :stability: experimental
        '''
        result = self._values.get("loaders")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BundlerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.BundlingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "externals": "externals",
        "sourcemap": "sourcemap",
        "watch_task": "watchTask",
    },
)
class BundlingOptions:
    def __init__(
        self,
        *,
        externals: typing.Optional[typing.Sequence[builtins.str]] = None,
        sourcemap: typing.Optional[builtins.bool] = None,
        watch_task: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for bundling.

        :param externals: (experimental) You can mark a file or a package as external to exclude it from your build. Instead of being bundled, the import will be preserved (using require for the iife and cjs formats and using import for the esm format) and will be evaluated at run time instead. This has several uses. First of all, it can be used to trim unnecessary code from your bundle for a code path that you know will never be executed. For example, a package may contain code that only runs in node but you will only be using that package in the browser. It can also be used to import code in node at run time from a package that cannot be bundled. For example, the fsevents package contains a native extension, which esbuild doesn't support. Default: []
        :param sourcemap: (experimental) Include a source map in the bundle. Default: false
        :param watch_task: (experimental) In addition to the ``bundle:xyz`` task, creates ``bundle:xyz:watch`` task which will invoke the same esbuild command with the ``--watch`` flag. This can be used to continusouly watch for changes. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e252fd4be8ae854f73a85420360ed4acf437d507d78f6a911faa76a8abd5be7)
            check_type(argname="argument externals", value=externals, expected_type=type_hints["externals"])
            check_type(argname="argument sourcemap", value=sourcemap, expected_type=type_hints["sourcemap"])
            check_type(argname="argument watch_task", value=watch_task, expected_type=type_hints["watch_task"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if externals is not None:
            self._values["externals"] = externals
        if sourcemap is not None:
            self._values["sourcemap"] = sourcemap
        if watch_task is not None:
            self._values["watch_task"] = watch_task

    @builtins.property
    def externals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) You can mark a file or a package as external to exclude it from your build.

        Instead of being bundled, the import will be preserved (using require for
        the iife and cjs formats and using import for the esm format) and will be
        evaluated at run time instead.

        This has several uses. First of all, it can be used to trim unnecessary
        code from your bundle for a code path that you know will never be executed.
        For example, a package may contain code that only runs in node but you will
        only be using that package in the browser. It can also be used to import
        code in node at run time from a package that cannot be bundled. For
        example, the fsevents package contains a native extension, which esbuild
        doesn't support.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("externals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sourcemap(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include a source map in the bundle.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("sourcemap")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def watch_task(self) -> typing.Optional[builtins.bool]:
        '''(experimental) In addition to the ``bundle:xyz`` task, creates ``bundle:xyz:watch`` task which will invoke the same esbuild command with the ``--watch`` flag.

        This can be used
        to continusouly watch for changes.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("watch_task")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BundlingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.CodeArtifactAuthProvider")
class CodeArtifactAuthProvider(enum.Enum):
    '''(experimental) Options for authorizing requests to a AWS CodeArtifact npm repository.

    :stability: experimental
    '''

    ACCESS_AND_SECRET_KEY_PAIR = "ACCESS_AND_SECRET_KEY_PAIR"
    '''(experimental) Fixed credentials provided via Github secrets.

    :stability: experimental
    '''
    GITHUB_OIDC = "GITHUB_OIDC"
    '''(experimental) Ephemeral credentials provided via Github's OIDC integration with an IAM role.

    See:
    https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html
    https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.javascript.CodeArtifactOptions",
    jsii_struct_bases=[],
    name_mapping={
        "access_key_id_secret": "accessKeyIdSecret",
        "auth_provider": "authProvider",
        "role_to_assume": "roleToAssume",
        "secret_access_key_secret": "secretAccessKeySecret",
    },
)
class CodeArtifactOptions:
    def __init__(
        self,
        *,
        access_key_id_secret: typing.Optional[builtins.str] = None,
        auth_provider: typing.Optional[CodeArtifactAuthProvider] = None,
        role_to_assume: typing.Optional[builtins.str] = None,
        secret_access_key_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for publishing npm packages to AWS CodeArtifact.

        :param access_key_id_secret: (experimental) GitHub secret which contains the AWS access key ID to use when publishing packages to AWS CodeArtifact. This property must be specified only when publishing to AWS CodeArtifact (``npmRegistryUrl`` contains AWS CodeArtifact URL). Default: - When the ``authProvider`` value is set to ``CodeArtifactAuthProvider.ACCESS_AND_SECRET_KEY_PAIR``, the default is "AWS_ACCESS_KEY_ID". For ``CodeArtifactAuthProvider.GITHUB_OIDC``, this value must be left undefined.
        :param auth_provider: (experimental) Provider to use for authorizing requests to AWS CodeArtifact. Default: CodeArtifactAuthProvider.ACCESS_AND_SECRET_KEY_PAIR
        :param role_to_assume: (experimental) ARN of AWS role to be assumed prior to get authorization token from AWS CodeArtifact This property must be specified only when publishing to AWS CodeArtifact (``registry`` contains AWS CodeArtifact URL). When using the ``CodeArtifactAuthProvider.GITHUB_OIDC`` auth provider, this value must be defined. Default: undefined
        :param secret_access_key_secret: (experimental) GitHub secret which contains the AWS secret access key to use when publishing packages to AWS CodeArtifact. This property must be specified only when publishing to AWS CodeArtifact (``npmRegistryUrl`` contains AWS CodeArtifact URL). Default: - When the ``authProvider`` value is set to ``CodeArtifactAuthProvider.ACCESS_AND_SECRET_KEY_PAIR``, the default is "AWS_SECRET_ACCESS_KEY". For ``CodeArtifactAuthProvider.GITHUB_OIDC``, this value must be left undefined.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__002c9939ff1c7990e7c7029095bb5f21d1cc7e5576d9a2db081cbf690aec60f8)
            check_type(argname="argument access_key_id_secret", value=access_key_id_secret, expected_type=type_hints["access_key_id_secret"])
            check_type(argname="argument auth_provider", value=auth_provider, expected_type=type_hints["auth_provider"])
            check_type(argname="argument role_to_assume", value=role_to_assume, expected_type=type_hints["role_to_assume"])
            check_type(argname="argument secret_access_key_secret", value=secret_access_key_secret, expected_type=type_hints["secret_access_key_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_key_id_secret is not None:
            self._values["access_key_id_secret"] = access_key_id_secret
        if auth_provider is not None:
            self._values["auth_provider"] = auth_provider
        if role_to_assume is not None:
            self._values["role_to_assume"] = role_to_assume
        if secret_access_key_secret is not None:
            self._values["secret_access_key_secret"] = secret_access_key_secret

    @builtins.property
    def access_key_id_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret which contains the AWS access key ID to use when publishing packages to AWS CodeArtifact.

        This property must be specified only when publishing to AWS CodeArtifact (``npmRegistryUrl`` contains AWS CodeArtifact URL).

        :default:

        - When the ``authProvider`` value is set to
        ``CodeArtifactAuthProvider.ACCESS_AND_SECRET_KEY_PAIR``, the default is
        "AWS_ACCESS_KEY_ID". For ``CodeArtifactAuthProvider.GITHUB_OIDC``, this
        value must be left undefined.

        :stability: experimental
        '''
        result = self._values.get("access_key_id_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_provider(self) -> typing.Optional[CodeArtifactAuthProvider]:
        '''(experimental) Provider to use for authorizing requests to AWS CodeArtifact.

        :default: CodeArtifactAuthProvider.ACCESS_AND_SECRET_KEY_PAIR

        :stability: experimental
        '''
        result = self._values.get("auth_provider")
        return typing.cast(typing.Optional[CodeArtifactAuthProvider], result)

    @builtins.property
    def role_to_assume(self) -> typing.Optional[builtins.str]:
        '''(experimental) ARN of AWS role to be assumed prior to get authorization token from AWS CodeArtifact This property must be specified only when publishing to AWS CodeArtifact (``registry`` contains AWS CodeArtifact URL).

        When using the ``CodeArtifactAuthProvider.GITHUB_OIDC`` auth provider, this value must be defined.

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("role_to_assume")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_access_key_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret which contains the AWS secret access key to use when publishing packages to AWS CodeArtifact.

        This property must be specified only when publishing to AWS CodeArtifact (``npmRegistryUrl`` contains AWS CodeArtifact URL).

        :default:

        - When the ``authProvider`` value is set to
        ``CodeArtifactAuthProvider.ACCESS_AND_SECRET_KEY_PAIR``, the default is
        "AWS_SECRET_ACCESS_KEY". For ``CodeArtifactAuthProvider.GITHUB_OIDC``, this
        value must be left undefined.

        :stability: experimental
        '''
        result = self._values.get("secret_access_key_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeArtifactOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.CoverageThreshold",
    jsii_struct_bases=[],
    name_mapping={
        "branches": "branches",
        "functions": "functions",
        "lines": "lines",
        "statements": "statements",
    },
)
class CoverageThreshold:
    def __init__(
        self,
        *,
        branches: typing.Optional[jsii.Number] = None,
        functions: typing.Optional[jsii.Number] = None,
        lines: typing.Optional[jsii.Number] = None,
        statements: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param branches: 
        :param functions: 
        :param lines: 
        :param statements: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9f20f577fcce2d29c8caf0cf8580b22e6e9616455ddbbdda0e6f84e331b0660)
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument functions", value=functions, expected_type=type_hints["functions"])
            check_type(argname="argument lines", value=lines, expected_type=type_hints["lines"])
            check_type(argname="argument statements", value=statements, expected_type=type_hints["statements"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches
        if functions is not None:
            self._values["functions"] = functions
        if lines is not None:
            self._values["lines"] = lines
        if statements is not None:
            self._values["statements"] = statements

    @builtins.property
    def branches(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def functions(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("functions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lines(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lines")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def statements(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("statements")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CoverageThreshold(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.EmbeddedLanguageFormatting")
class EmbeddedLanguageFormatting(enum.Enum):
    '''
    :stability: experimental
    '''

    AUTO = "AUTO"
    '''(experimental) Format embedded code if Prettier can automatically identify it.

    :stability: experimental
    '''
    OFF = "OFF"
    '''(experimental) Never automatically format embedded code.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.javascript.EndOfLine")
class EndOfLine(enum.Enum):
    '''
    :stability: experimental
    '''

    AUTO = "AUTO"
    '''(experimental) Maintain existing (mixed values within one file are normalised by looking at what's used after the first line).

    :stability: experimental
    '''
    CR = "CR"
    '''(experimental) Carriage Return character only (\\r), used very rarely.

    :stability: experimental
    '''
    CRLF = "CRLF"
    '''(experimental) Carriage Return + Line Feed characters (\\r\\n), common on Windows.

    :stability: experimental
    '''
    LF = "LF"
    '''(experimental) Line Feed only (\\n), common on Linux and macOS as well as inside git repos.

    :stability: experimental
    '''


class Eslint(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.javascript.Eslint",
):
    '''(experimental) Represents eslint configuration.

    :stability: experimental
    '''

    def __init__(
        self,
        project: "NodeProject",
        *,
        dirs: typing.Sequence[builtins.str],
        alias_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        alias_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        devdirs: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        lint_projen_rc: typing.Optional[builtins.bool] = None,
        lint_projen_rc_file: typing.Optional[builtins.str] = None,
        prettier: typing.Optional[builtins.bool] = None,
        ts_always_try_types: typing.Optional[builtins.bool] = None,
        tsconfig_path: typing.Optional[builtins.str] = None,
        yaml: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param project: -
        :param dirs: (experimental) Files or glob patterns or directories with source files to lint (e.g. [ "src" ]).
        :param alias_extensions: (experimental) Enable import alias for module paths. Default: undefined
        :param alias_map: (experimental) Enable import alias for module paths. Default: undefined
        :param devdirs: (experimental) Files or glob patterns or directories with source files that include tests and build tools. These sources are linted but may also import packages from ``devDependencies``. Default: []
        :param file_extensions: (experimental) File types that should be linted (e.g. [ ".js", ".ts" ]). Default: [".ts"]
        :param ignore_patterns: (experimental) List of file patterns that should not be linted, using the same syntax as .gitignore patterns. Default: [ '*.js', '*.d.ts', 'node_modules/', '*.generated.ts', 'coverage' ]
        :param lint_projen_rc: (deprecated) Should we lint .projenrc.js. Default: true
        :param lint_projen_rc_file: (deprecated) Projenrc file to lint. Use empty string to disable. Default: PROJEN_RC
        :param prettier: (experimental) Enable prettier for code formatting. Default: false
        :param ts_always_try_types: (experimental) Always try to resolve types under ``<root>@types`` directory even it doesn't contain any source code. This prevents ``import/no-unresolved`` eslint errors when importing a ``@types/*`` module that would otherwise remain unresolved. Default: true
        :param tsconfig_path: (experimental) Path to ``tsconfig.json`` which should be used by eslint. Default: "./tsconfig.json"
        :param yaml: (experimental) Write eslint configuration as YAML instead of JSON. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41d20792db723180b2558eb351d1b15e6cc51985fdc95dd8481c5fae78aa6963)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = EslintOptions(
            dirs=dirs,
            alias_extensions=alias_extensions,
            alias_map=alias_map,
            devdirs=devdirs,
            file_extensions=file_extensions,
            ignore_patterns=ignore_patterns,
            lint_projen_rc=lint_projen_rc,
            lint_projen_rc_file=lint_projen_rc_file,
            prettier=prettier,
            ts_always_try_types=ts_always_try_types,
            tsconfig_path=tsconfig_path,
            yaml=yaml,
        )

        jsii.create(self.__class__, self, [project, options])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, project: _Project_57d89203) -> typing.Optional["Eslint"]:
        '''(experimental) Returns the singletone Eslint component of a project or undefined if there is none.

        :param project: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e06eae7f2f48a5d785ab71742d0b102d7eb8b056db43d7828d871b53a8004a5)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        return typing.cast(typing.Optional["Eslint"], jsii.sinvoke(cls, "of", [project]))

    @jsii.member(jsii_name="addExtends")
    def add_extends(self, *extend_list: builtins.str) -> None:
        '''(experimental) Adds an ``extends`` item to the eslint configuration.

        :param extend_list: The list of "extends" to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93136ac5c9172a02dce49add560ad232b311f1482a6693dca9b52cb68af2ca4)
            check_type(argname="argument extend_list", value=extend_list, expected_type=typing.Tuple[type_hints["extend_list"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addExtends", [*extend_list]))

    @jsii.member(jsii_name="addIgnorePattern")
    def add_ignore_pattern(self, pattern: builtins.str) -> None:
        '''(experimental) Do not lint these files.

        :param pattern: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d763feccbd0bc84b224afc2b98acef5e87f938260e31532e536772fb599fbc88)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(None, jsii.invoke(self, "addIgnorePattern", [pattern]))

    @jsii.member(jsii_name="addLintPattern")
    def add_lint_pattern(self, pattern: builtins.str) -> None:
        '''(experimental) Add a file, glob pattern or directory with source files to lint (e.g. [ "src" ]).

        :param pattern: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3c302914aeeb5275b37b60ab64fa0cc6a10a65a08a8f7d8b2aba9aebcc4f75f)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(None, jsii.invoke(self, "addLintPattern", [pattern]))

    @jsii.member(jsii_name="addOverride")
    def add_override(
        self,
        *,
        files: typing.Sequence[builtins.str],
        parser: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''(experimental) Add an eslint override.

        :param files: (experimental) Files or file patterns on which to apply the override.
        :param parser: (experimental) The overridden parser.
        :param rules: (experimental) The overriden rules.

        :stability: experimental
        '''
        override = EslintOverride(files=files, parser=parser, rules=rules)

        return typing.cast(None, jsii.invoke(self, "addOverride", [override]))

    @jsii.member(jsii_name="addPlugins")
    def add_plugins(self, *plugins: builtins.str) -> None:
        '''(experimental) Adds an eslint plugin.

        :param plugins: The names of plugins to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f336402a11e766eb80cbfa5e80fea16b3ef9d7b18f0aa3a2a7b17e24647aa6c9)
            check_type(argname="argument plugins", value=plugins, expected_type=typing.Tuple[type_hints["plugins"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addPlugins", [*plugins]))

    @jsii.member(jsii_name="addRules")
    def add_rules(self, rules: typing.Mapping[builtins.str, typing.Any]) -> None:
        '''(experimental) Add an eslint rule.

        :param rules: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ea4c9051e61eb8d25919e5b5cb6ba7ef44e9a5d642dec514714c13c4b9141c)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        return typing.cast(None, jsii.invoke(self, "addRules", [rules]))

    @jsii.member(jsii_name="allowDevDeps")
    def allow_dev_deps(self, pattern: builtins.str) -> None:
        '''(experimental) Add a glob file pattern which allows importing dev dependencies.

        :param pattern: glob pattern.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45c512f160dd2d4145e1c0d43de9571ffe4d89e10b34c7d9a7b9fbba3f85ca56)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(None, jsii.invoke(self, "allowDevDeps", [pattern]))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> typing.Any:
        '''(experimental) Direct access to the eslint configuration (escape hatch).

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="eslintTask")
    def eslint_task(self) -> _Task_9fa875b6:
        '''(experimental) eslint task.

        :stability: experimental
        '''
        return typing.cast(_Task_9fa875b6, jsii.get(self, "eslintTask"))

    @builtins.property
    @jsii.member(jsii_name="ignorePatterns")
    def ignore_patterns(self) -> typing.List[builtins.str]:
        '''(experimental) File patterns that should not be linted.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ignorePatterns"))

    @builtins.property
    @jsii.member(jsii_name="overrides")
    def overrides(self) -> typing.List["EslintOverride"]:
        '''(experimental) eslint overrides.

        :stability: experimental
        '''
        return typing.cast(typing.List["EslintOverride"], jsii.get(self, "overrides"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> typing.Mapping[builtins.str, typing.List[typing.Any]]:
        '''(experimental) eslint rules.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.List[typing.Any]], jsii.get(self, "rules"))


@jsii.data_type(
    jsii_type="projen.javascript.EslintOptions",
    jsii_struct_bases=[],
    name_mapping={
        "dirs": "dirs",
        "alias_extensions": "aliasExtensions",
        "alias_map": "aliasMap",
        "devdirs": "devdirs",
        "file_extensions": "fileExtensions",
        "ignore_patterns": "ignorePatterns",
        "lint_projen_rc": "lintProjenRc",
        "lint_projen_rc_file": "lintProjenRcFile",
        "prettier": "prettier",
        "ts_always_try_types": "tsAlwaysTryTypes",
        "tsconfig_path": "tsconfigPath",
        "yaml": "yaml",
    },
)
class EslintOptions:
    def __init__(
        self,
        *,
        dirs: typing.Sequence[builtins.str],
        alias_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        alias_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        devdirs: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        lint_projen_rc: typing.Optional[builtins.bool] = None,
        lint_projen_rc_file: typing.Optional[builtins.str] = None,
        prettier: typing.Optional[builtins.bool] = None,
        ts_always_try_types: typing.Optional[builtins.bool] = None,
        tsconfig_path: typing.Optional[builtins.str] = None,
        yaml: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param dirs: (experimental) Files or glob patterns or directories with source files to lint (e.g. [ "src" ]).
        :param alias_extensions: (experimental) Enable import alias for module paths. Default: undefined
        :param alias_map: (experimental) Enable import alias for module paths. Default: undefined
        :param devdirs: (experimental) Files or glob patterns or directories with source files that include tests and build tools. These sources are linted but may also import packages from ``devDependencies``. Default: []
        :param file_extensions: (experimental) File types that should be linted (e.g. [ ".js", ".ts" ]). Default: [".ts"]
        :param ignore_patterns: (experimental) List of file patterns that should not be linted, using the same syntax as .gitignore patterns. Default: [ '*.js', '*.d.ts', 'node_modules/', '*.generated.ts', 'coverage' ]
        :param lint_projen_rc: (deprecated) Should we lint .projenrc.js. Default: true
        :param lint_projen_rc_file: (deprecated) Projenrc file to lint. Use empty string to disable. Default: PROJEN_RC
        :param prettier: (experimental) Enable prettier for code formatting. Default: false
        :param ts_always_try_types: (experimental) Always try to resolve types under ``<root>@types`` directory even it doesn't contain any source code. This prevents ``import/no-unresolved`` eslint errors when importing a ``@types/*`` module that would otherwise remain unresolved. Default: true
        :param tsconfig_path: (experimental) Path to ``tsconfig.json`` which should be used by eslint. Default: "./tsconfig.json"
        :param yaml: (experimental) Write eslint configuration as YAML instead of JSON. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26892c968b7bf4d64dd2597bbdabf1f1e9ced92002225a4eedfae6cbe3c22894)
            check_type(argname="argument dirs", value=dirs, expected_type=type_hints["dirs"])
            check_type(argname="argument alias_extensions", value=alias_extensions, expected_type=type_hints["alias_extensions"])
            check_type(argname="argument alias_map", value=alias_map, expected_type=type_hints["alias_map"])
            check_type(argname="argument devdirs", value=devdirs, expected_type=type_hints["devdirs"])
            check_type(argname="argument file_extensions", value=file_extensions, expected_type=type_hints["file_extensions"])
            check_type(argname="argument ignore_patterns", value=ignore_patterns, expected_type=type_hints["ignore_patterns"])
            check_type(argname="argument lint_projen_rc", value=lint_projen_rc, expected_type=type_hints["lint_projen_rc"])
            check_type(argname="argument lint_projen_rc_file", value=lint_projen_rc_file, expected_type=type_hints["lint_projen_rc_file"])
            check_type(argname="argument prettier", value=prettier, expected_type=type_hints["prettier"])
            check_type(argname="argument ts_always_try_types", value=ts_always_try_types, expected_type=type_hints["ts_always_try_types"])
            check_type(argname="argument tsconfig_path", value=tsconfig_path, expected_type=type_hints["tsconfig_path"])
            check_type(argname="argument yaml", value=yaml, expected_type=type_hints["yaml"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dirs": dirs,
        }
        if alias_extensions is not None:
            self._values["alias_extensions"] = alias_extensions
        if alias_map is not None:
            self._values["alias_map"] = alias_map
        if devdirs is not None:
            self._values["devdirs"] = devdirs
        if file_extensions is not None:
            self._values["file_extensions"] = file_extensions
        if ignore_patterns is not None:
            self._values["ignore_patterns"] = ignore_patterns
        if lint_projen_rc is not None:
            self._values["lint_projen_rc"] = lint_projen_rc
        if lint_projen_rc_file is not None:
            self._values["lint_projen_rc_file"] = lint_projen_rc_file
        if prettier is not None:
            self._values["prettier"] = prettier
        if ts_always_try_types is not None:
            self._values["ts_always_try_types"] = ts_always_try_types
        if tsconfig_path is not None:
            self._values["tsconfig_path"] = tsconfig_path
        if yaml is not None:
            self._values["yaml"] = yaml

    @builtins.property
    def dirs(self) -> typing.List[builtins.str]:
        '''(experimental) Files or glob patterns or directories with source files to lint (e.g. [ "src" ]).

        :stability: experimental
        '''
        result = self._values.get("dirs")
        assert result is not None, "Required property 'dirs' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def alias_extensions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Enable import alias for module paths.

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("alias_extensions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def alias_map(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Enable import alias for module paths.

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("alias_map")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def devdirs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Files or glob patterns or directories with source files that include tests and build tools.

        These sources are linted but may also import packages from ``devDependencies``.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("devdirs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_extensions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) File types that should be linted (e.g. [ ".js", ".ts" ]).

        :default: [".ts"]

        :stability: experimental
        '''
        result = self._values.get("file_extensions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ignore_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of file patterns that should not be linted, using the same syntax as .gitignore patterns.

        :default: [ '*.js', '*.d.ts', 'node_modules/', '*.generated.ts', 'coverage' ]

        :stability: experimental
        '''
        result = self._values.get("ignore_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def lint_projen_rc(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Should we lint .projenrc.js.

        :default: true

        :deprecated: set to ``false`` to remove any automatic rules and add manually

        :stability: deprecated
        '''
        result = self._values.get("lint_projen_rc")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def lint_projen_rc_file(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Projenrc file to lint.

        Use empty string to disable.

        :default: PROJEN_RC

        :deprecated: provide as ``devdirs``

        :stability: deprecated
        '''
        result = self._values.get("lint_projen_rc_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prettier(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable prettier for code formatting.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("prettier")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ts_always_try_types(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Always try to resolve types under ``<root>@types`` directory even it doesn't contain any source code.

        This prevents ``import/no-unresolved`` eslint errors when importing a ``@types/*`` module that would otherwise remain unresolved.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("ts_always_try_types")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tsconfig_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to ``tsconfig.json`` which should be used by eslint.

        :default: "./tsconfig.json"

        :stability: experimental
        '''
        result = self._values.get("tsconfig_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def yaml(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Write eslint configuration as YAML instead of JSON.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("yaml")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EslintOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.EslintOverride",
    jsii_struct_bases=[],
    name_mapping={"files": "files", "parser": "parser", "rules": "rules"},
)
class EslintOverride:
    def __init__(
        self,
        *,
        files: typing.Sequence[builtins.str],
        parser: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''(experimental) eslint rules override.

        :param files: (experimental) Files or file patterns on which to apply the override.
        :param parser: (experimental) The overridden parser.
        :param rules: (experimental) The overriden rules.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31a0dd46abf45fc4e6701aa5424796361affd0e9c44ed0f9005dd4fe08f3a136)
            check_type(argname="argument files", value=files, expected_type=type_hints["files"])
            check_type(argname="argument parser", value=parser, expected_type=type_hints["parser"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "files": files,
        }
        if parser is not None:
            self._values["parser"] = parser
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def files(self) -> typing.List[builtins.str]:
        '''(experimental) Files or file patterns on which to apply the override.

        :stability: experimental
        '''
        result = self._values.get("files")
        assert result is not None, "Required property 'files' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def parser(self) -> typing.Optional[builtins.str]:
        '''(experimental) The overridden parser.

        :stability: experimental
        '''
        result = self._values.get("parser")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) The overriden rules.

        :stability: experimental
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EslintOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.HTMLWhitespaceSensitivity")
class HTMLWhitespaceSensitivity(enum.Enum):
    '''
    :stability: experimental
    '''

    CSS = "CSS"
    '''(experimental) Respect the default value of CSS display property.

    :stability: experimental
    '''
    IGNORE = "IGNORE"
    '''(experimental) Whitespaces are considered insignificant.

    :stability: experimental
    '''
    STRICT = "STRICT"
    '''(experimental) Whitespaces are considered significant.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.javascript.HasteConfig",
    jsii_struct_bases=[],
    name_mapping={
        "compute_sha1": "computeSha1",
        "default_platform": "defaultPlatform",
        "haste_impl_module_path": "hasteImplModulePath",
        "platforms": "platforms",
        "throw_on_module_collision": "throwOnModuleCollision",
    },
)
class HasteConfig:
    def __init__(
        self,
        *,
        compute_sha1: typing.Optional[builtins.bool] = None,
        default_platform: typing.Optional[builtins.str] = None,
        haste_impl_module_path: typing.Optional[builtins.str] = None,
        platforms: typing.Optional[typing.Sequence[builtins.str]] = None,
        throw_on_module_collision: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param compute_sha1: 
        :param default_platform: 
        :param haste_impl_module_path: 
        :param platforms: 
        :param throw_on_module_collision: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d0f97663aee053bcca0e3b33c8be45ef5c6271b8e0c683a67d717aa914e2a89)
            check_type(argname="argument compute_sha1", value=compute_sha1, expected_type=type_hints["compute_sha1"])
            check_type(argname="argument default_platform", value=default_platform, expected_type=type_hints["default_platform"])
            check_type(argname="argument haste_impl_module_path", value=haste_impl_module_path, expected_type=type_hints["haste_impl_module_path"])
            check_type(argname="argument platforms", value=platforms, expected_type=type_hints["platforms"])
            check_type(argname="argument throw_on_module_collision", value=throw_on_module_collision, expected_type=type_hints["throw_on_module_collision"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_sha1 is not None:
            self._values["compute_sha1"] = compute_sha1
        if default_platform is not None:
            self._values["default_platform"] = default_platform
        if haste_impl_module_path is not None:
            self._values["haste_impl_module_path"] = haste_impl_module_path
        if platforms is not None:
            self._values["platforms"] = platforms
        if throw_on_module_collision is not None:
            self._values["throw_on_module_collision"] = throw_on_module_collision

    @builtins.property
    def compute_sha1(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("compute_sha1")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def default_platform(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("default_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def haste_impl_module_path(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("haste_impl_module_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("platforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def throw_on_module_collision(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("throw_on_module_collision")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HasteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Jest(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.javascript.Jest",
):
    '''(experimental) Installs the following npm scripts:.

    - ``test``, intended for testing locally and in CI. Will update snapshots unless ``updateSnapshot: UpdateSnapshot: NEVER`` is set.
    - ``test:watch``, intended for automatically rerunning tests when files change.
    - ``test:update``, intended for testing locally and updating snapshots to match the latest unit under test. Only available when ``updateSnapshot: UpdateSnapshot: NEVER``.

    :stability: experimental
    '''

    def __init__(
        self,
        project: "NodeProject",
        *,
        config_file_path: typing.Optional[builtins.str] = None,
        coverage: typing.Optional[builtins.bool] = None,
        coverage_text: typing.Optional[builtins.bool] = None,
        extra_cli_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        jest_config: typing.Optional[typing.Union["JestConfigOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        jest_version: typing.Optional[builtins.str] = None,
        junit_reporting: typing.Optional[builtins.bool] = None,
        preserve_default_reporters: typing.Optional[builtins.bool] = None,
        update_snapshot: typing.Optional["UpdateSnapshot"] = None,
    ) -> None:
        '''
        :param project: -
        :param config_file_path: (experimental) Path to JSON config file for Jest. Default: - No separate config file, jest settings are stored in package.json
        :param coverage: (deprecated) Collect coverage. Deprecated Default: true
        :param coverage_text: (experimental) Include the ``text`` coverage reporter, which means that coverage summary is printed at the end of the jest execution. Default: true
        :param extra_cli_options: (experimental) Additional options to pass to the Jest CLI invocation. Default: - no extra options
        :param ignore_patterns: (deprecated) Defines ``testPathIgnorePatterns`` and ``coveragePathIgnorePatterns``. Default: ["/node_modules/"]
        :param jest_config: (experimental) Jest configuration. Default: - default jest configuration
        :param jest_version: (experimental) The version of jest to use. Note that same version is used as version of ``@types/jest`` and ``ts-jest`` (if Typescript in use), so given version should work also for those. Default: - installs the latest jest version
        :param junit_reporting: (experimental) Result processing with jest-junit. Output directory is ``test-reports/``. Default: true
        :param preserve_default_reporters: (experimental) Preserve the default Jest reporter when additional reporters are added. Default: true
        :param update_snapshot: (experimental) Whether to update snapshots in task "test" (which is executed in task "build" and build workflows), or create a separate task "test:update" for updating snapshots. Default: - ALWAYS

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f22158e02967239263c228b0eadfa82f5edd4d7b172b8506a5b32bc46ab7738)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = JestOptions(
            config_file_path=config_file_path,
            coverage=coverage,
            coverage_text=coverage_text,
            extra_cli_options=extra_cli_options,
            ignore_patterns=ignore_patterns,
            jest_config=jest_config,
            jest_version=jest_version,
            junit_reporting=junit_reporting,
            preserve_default_reporters=preserve_default_reporters,
            update_snapshot=update_snapshot,
        )

        jsii.create(self.__class__, self, [project, options])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, project: _Project_57d89203) -> typing.Optional["Jest"]:
        '''(experimental) Returns the singletone Jest component of a project or undefined if there is none.

        :param project: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f7fcc78583eceb598afdcb95edc0f1b1e50996f7069e12c4379c4826f26209)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        return typing.cast(typing.Optional["Jest"], jsii.sinvoke(cls, "of", [project]))

    @jsii.member(jsii_name="addIgnorePattern")
    def add_ignore_pattern(self, pattern: builtins.str) -> None:
        '''
        :param pattern: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e87fe808869e615e76d29eee7ca1d2238a1385943c81f0a2e892460ceedb5ed)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(None, jsii.invoke(self, "addIgnorePattern", [pattern]))

    @jsii.member(jsii_name="addReporter")
    def add_reporter(self, reporter: "JestReporter") -> None:
        '''
        :param reporter: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c4c1ef11a85bcfb37b6e70871ed29cf5fa4c0462b66dc45e117870bbc694112)
            check_type(argname="argument reporter", value=reporter, expected_type=type_hints["reporter"])
        return typing.cast(None, jsii.invoke(self, "addReporter", [reporter]))

    @jsii.member(jsii_name="addSetupFile")
    def add_setup_file(self, file: builtins.str) -> None:
        '''(experimental) Adds a a setup file to Jest's setupFiles configuration.

        :param file: File path to setup file.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ac5cebbfb17927ec2e8823a44f46135f97967d425da95c8fb3e9178d5692325)
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
        return typing.cast(None, jsii.invoke(self, "addSetupFile", [file]))

    @jsii.member(jsii_name="addSetupFileAfterEnv")
    def add_setup_file_after_env(self, file: builtins.str) -> None:
        '''(experimental) Adds a a setup file to Jest's setupFilesAfterEnv configuration.

        :param file: File path to setup file.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e0d94b263ceb92e7dbb69cd4c07c5974658fb7c8657d66df3942b0de62fdd0)
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
        return typing.cast(None, jsii.invoke(self, "addSetupFileAfterEnv", [file]))

    @jsii.member(jsii_name="addSnapshotResolver")
    def add_snapshot_resolver(self, file: builtins.str) -> None:
        '''
        :param file: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e90cd9fa168c9e74d2ff0170f7a1eab10a2368f21ff1133964d018b8019d7268)
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
        return typing.cast(None, jsii.invoke(self, "addSnapshotResolver", [file]))

    @jsii.member(jsii_name="addTestMatch")
    def add_test_match(self, pattern: builtins.str) -> None:
        '''(experimental) Adds a test match pattern.

        :param pattern: glob pattern to match for tests.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79885cc12d31e7c903be82393a87b275c69824c1f59cae5ba5c8d4f5de5982e4)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(None, jsii.invoke(self, "addTestMatch", [pattern]))

    @jsii.member(jsii_name="addWatchIgnorePattern")
    def add_watch_ignore_pattern(self, pattern: builtins.str) -> None:
        '''(experimental) Adds a watch ignore pattern.

        :param pattern: The pattern (regular expression).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__340f8ef9eed036d2e1af02ee13866e070b25e032c7262d1181adf28bbee99b5a)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(None, jsii.invoke(self, "addWatchIgnorePattern", [pattern]))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> typing.Any:
        '''(experimental) Escape hatch.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="jestVersion")
    def jest_version(self) -> builtins.str:
        '''(experimental) Jest version, including ``@`` symbol, like ``@^29``.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "jestVersion"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> typing.Optional[_JsonFile_fa8164db]:
        '''(experimental) Jest config file.

        ``undefined`` if settings are written to ``package.json``

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_JsonFile_fa8164db], jsii.get(self, "file"))


@jsii.data_type(
    jsii_type="projen.javascript.JestConfigOptions",
    jsii_struct_bases=[],
    name_mapping={
        "additional_options": "additionalOptions",
        "automock": "automock",
        "bail": "bail",
        "cache_directory": "cacheDirectory",
        "clear_mocks": "clearMocks",
        "collect_coverage": "collectCoverage",
        "collect_coverage_from": "collectCoverageFrom",
        "coverage_directory": "coverageDirectory",
        "coverage_path_ignore_patterns": "coveragePathIgnorePatterns",
        "coverage_provider": "coverageProvider",
        "coverage_reporters": "coverageReporters",
        "coverage_threshold": "coverageThreshold",
        "dependency_extractor": "dependencyExtractor",
        "display_name": "displayName",
        "error_on_deprecated": "errorOnDeprecated",
        "extra_globals": "extraGlobals",
        "force_coverage_match": "forceCoverageMatch",
        "globals": "globals",
        "global_setup": "globalSetup",
        "global_teardown": "globalTeardown",
        "haste": "haste",
        "inject_globals": "injectGlobals",
        "max_concurrency": "maxConcurrency",
        "max_workers": "maxWorkers",
        "module_directories": "moduleDirectories",
        "module_file_extensions": "moduleFileExtensions",
        "module_name_mapper": "moduleNameMapper",
        "module_path_ignore_patterns": "modulePathIgnorePatterns",
        "module_paths": "modulePaths",
        "notify": "notify",
        "notify_mode": "notifyMode",
        "preset": "preset",
        "prettier_path": "prettierPath",
        "projects": "projects",
        "reporters": "reporters",
        "reset_mocks": "resetMocks",
        "reset_modules": "resetModules",
        "resolver": "resolver",
        "restore_mocks": "restoreMocks",
        "root_dir": "rootDir",
        "roots": "roots",
        "runner": "runner",
        "setup_files": "setupFiles",
        "setup_files_after_env": "setupFilesAfterEnv",
        "slow_test_threshold": "slowTestThreshold",
        "snapshot_resolver": "snapshotResolver",
        "snapshot_serializers": "snapshotSerializers",
        "test_environment": "testEnvironment",
        "test_environment_options": "testEnvironmentOptions",
        "test_failure_exit_code": "testFailureExitCode",
        "test_match": "testMatch",
        "test_path_ignore_patterns": "testPathIgnorePatterns",
        "test_regex": "testRegex",
        "test_results_processor": "testResultsProcessor",
        "test_runner": "testRunner",
        "test_sequencer": "testSequencer",
        "test_timeout": "testTimeout",
        "test_url": "testURL",
        "timers": "timers",
        "transform": "transform",
        "transform_ignore_patterns": "transformIgnorePatterns",
        "unmocked_module_path_patterns": "unmockedModulePathPatterns",
        "verbose": "verbose",
        "watchman": "watchman",
        "watch_path_ignore_patterns": "watchPathIgnorePatterns",
        "watch_plugins": "watchPlugins",
    },
)
class JestConfigOptions:
    def __init__(
        self,
        *,
        additional_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        automock: typing.Optional[builtins.bool] = None,
        bail: typing.Optional[typing.Union[jsii.Number, builtins.bool]] = None,
        cache_directory: typing.Optional[builtins.str] = None,
        clear_mocks: typing.Optional[builtins.bool] = None,
        collect_coverage: typing.Optional[builtins.bool] = None,
        collect_coverage_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        coverage_directory: typing.Optional[builtins.str] = None,
        coverage_path_ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        coverage_provider: typing.Optional[builtins.str] = None,
        coverage_reporters: typing.Optional[typing.Sequence[builtins.str]] = None,
        coverage_threshold: typing.Optional[typing.Union[CoverageThreshold, typing.Dict[builtins.str, typing.Any]]] = None,
        dependency_extractor: typing.Optional[builtins.str] = None,
        display_name: typing.Any = None,
        error_on_deprecated: typing.Optional[builtins.bool] = None,
        extra_globals: typing.Optional[typing.Sequence[builtins.str]] = None,
        force_coverage_match: typing.Optional[typing.Sequence[builtins.str]] = None,
        globals: typing.Any = None,
        global_setup: typing.Optional[builtins.str] = None,
        global_teardown: typing.Optional[builtins.str] = None,
        haste: typing.Optional[typing.Union[HasteConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        inject_globals: typing.Optional[builtins.bool] = None,
        max_concurrency: typing.Optional[jsii.Number] = None,
        max_workers: typing.Optional[typing.Union[builtins.str, jsii.Number]] = None,
        module_directories: typing.Optional[typing.Sequence[builtins.str]] = None,
        module_file_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        module_name_mapper: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]] = None,
        module_path_ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        module_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        notify: typing.Optional[builtins.bool] = None,
        notify_mode: typing.Optional[builtins.str] = None,
        preset: typing.Optional[builtins.str] = None,
        prettier_path: typing.Optional[builtins.str] = None,
        projects: typing.Optional[typing.Sequence[typing.Union[builtins.str, typing.Mapping[builtins.str, typing.Any]]]] = None,
        reporters: typing.Optional[typing.Sequence["JestReporter"]] = None,
        reset_mocks: typing.Optional[builtins.bool] = None,
        reset_modules: typing.Optional[builtins.bool] = None,
        resolver: typing.Optional[builtins.str] = None,
        restore_mocks: typing.Optional[builtins.bool] = None,
        root_dir: typing.Optional[builtins.str] = None,
        roots: typing.Optional[typing.Sequence[builtins.str]] = None,
        runner: typing.Optional[builtins.str] = None,
        setup_files: typing.Optional[typing.Sequence[builtins.str]] = None,
        setup_files_after_env: typing.Optional[typing.Sequence[builtins.str]] = None,
        slow_test_threshold: typing.Optional[jsii.Number] = None,
        snapshot_resolver: typing.Optional[builtins.str] = None,
        snapshot_serializers: typing.Optional[typing.Sequence[builtins.str]] = None,
        test_environment: typing.Optional[builtins.str] = None,
        test_environment_options: typing.Any = None,
        test_failure_exit_code: typing.Optional[jsii.Number] = None,
        test_match: typing.Optional[typing.Sequence[builtins.str]] = None,
        test_path_ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        test_regex: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        test_results_processor: typing.Optional[builtins.str] = None,
        test_runner: typing.Optional[builtins.str] = None,
        test_sequencer: typing.Optional[builtins.str] = None,
        test_timeout: typing.Optional[jsii.Number] = None,
        test_url: typing.Optional[builtins.str] = None,
        timers: typing.Optional[builtins.str] = None,
        transform: typing.Optional[typing.Mapping[builtins.str, "Transform"]] = None,
        transform_ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        unmocked_module_path_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        verbose: typing.Optional[builtins.bool] = None,
        watchman: typing.Optional[builtins.bool] = None,
        watch_path_ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        watch_plugins: typing.Optional[typing.Sequence["WatchPlugin"]] = None,
    ) -> None:
        '''
        :param additional_options: (experimental) Escape hatch to allow any value.
        :param automock: (experimental) This option tells Jest that all imported modules in your tests should be mocked automatically. All modules used in your tests will have a replacement implementation, keeping the API surface Default: - false
        :param bail: (experimental) By default, Jest runs all tests and produces all errors into the console upon completion. The bail config option can be used here to have Jest stop running tests after n failures. Setting bail to true is the same as setting bail to 1. Default: - 0
        :param cache_directory: (experimental) The directory where Jest should store its cached dependency information. Default: - "/tmp/"
        :param clear_mocks: (experimental) Automatically clear mock calls and instances before every test. Equivalent to calling jest.clearAllMocks() before each test. This does not remove any mock implementation that may have been provided Default: true
        :param collect_coverage: (experimental) Indicates whether the coverage information should be collected while executing the test. Because this retrofits all executed files with coverage collection statements, it may significantly slow down your tests Default: true
        :param collect_coverage_from: (experimental) An array of glob patterns indicating a set of files for which coverage information should be collected. Default: - undefined
        :param coverage_directory: (experimental) The directory where Jest should output its coverage files. Default: "coverage"
        :param coverage_path_ignore_patterns: (experimental) An array of regexp pattern strings that are matched against all file paths before executing the test. If the file path matches any of the patterns, coverage information will be skipped Default: "/node_modules/"
        :param coverage_provider: (experimental) Indicates which provider should be used to instrument code for coverage. Allowed values are babel (default) or v8 Default: - "babel"
        :param coverage_reporters: (experimental) A list of reporter names that Jest uses when writing coverage reports. Any istanbul reporter can be used Default: - ["json", "lcov", "text", "clover", "cobertura"]
        :param coverage_threshold: (experimental) Specify the global coverage thresholds. This will be used to configure minimum threshold enforcement for coverage results. Thresholds can be specified as global, as a glob, and as a directory or file path. If thresholds aren't met, jest will fail. Default: - undefined
        :param dependency_extractor: (experimental) This option allows the use of a custom dependency extractor. It must be a node module that exports an object with an extract function Default: - undefined
        :param display_name: (experimental) Allows for a label to be printed alongside a test while it is running. Default: - undefined
        :param error_on_deprecated: (experimental) Make calling deprecated APIs throw helpful error messages. Useful for easing the upgrade process. Default: - false
        :param extra_globals: (experimental) Test files run inside a vm, which slows calls to global context properties (e.g. Math). With this option you can specify extra properties to be defined inside the vm for faster lookups. Default: - undefined
        :param force_coverage_match: (experimental) Test files are normally ignored from collecting code coverage. With this option, you can overwrite this behavior and include otherwise ignored files in code coverage. Default: - ['']
        :param globals: (experimental) A set of global variables that need to be available in all test environments. Default: - {}
        :param global_setup: (experimental) This option allows the use of a custom global setup module which exports an async function that is triggered once before all test suites. This function gets Jest's globalConfig object as a parameter. Default: - undefined
        :param global_teardown: (experimental) This option allows the use of a custom global teardown module which exports an async function that is triggered once after all test suites. This function gets Jest's globalConfig object as a parameter. Default: - undefined
        :param haste: (experimental) This will be used to configure the behavior of jest-haste-map, Jest's internal file crawler/cache system. Default: - {}
        :param inject_globals: (experimental) Insert Jest's globals (expect, test, describe, beforeEach etc.) into the global environment. If you set this to false, you should import from. Default: - true
        :param max_concurrency: (experimental) A number limiting the number of tests that are allowed to run at the same time when using test.concurrent. Any test above this limit will be queued and executed once a slot is released. Default: - 5
        :param max_workers: (experimental) Specifies the maximum number of workers the worker-pool will spawn for running tests. In single run mode, this defaults to the number of the cores available on your machine minus one for the main thread In watch mode, this defaults to half of the available cores on your machine. For environments with variable CPUs available, you can use percentage based configuration: "maxWorkers": "50%" Default: - the number of the cores available on your machine minus one for the main thread
        :param module_directories: (experimental) An array of directory names to be searched recursively up from the requiring module's location. Setting this option will override the default, if you wish to still search node_modules for packages include it along with any other options: ["node_modules", "bower_components"] Default: - ["node_modules"]
        :param module_file_extensions: (experimental) An array of file extensions your modules use. If you require modules without specifying a file extension, these are the extensions Jest will look for, in left-to-right order. Default: - ["js", "json", "jsx", "ts", "tsx", "node"]
        :param module_name_mapper: (experimental) A map from regular expressions to module names or to arrays of module names that allow to stub out resources, like images or styles with a single module. Default: - null
        :param module_path_ignore_patterns: (experimental) An array of regexp pattern strings that are matched against all module paths before those paths are to be considered 'visible' to the module loader. If a given module's path matches any of the patterns, it will not be require()-able in the test environment. Default: - []
        :param module_paths: (experimental) An alternative API to setting the NODE_PATH env variable, modulePaths is an array of absolute paths to additional locations to search when resolving modules. Use the string token to include the path to your project's root directory. Example: ["/app/"]. Default: - []
        :param notify: (experimental) Activates notifications for test results. Default: - false
        :param notify_mode: (experimental) Specifies notification mode. Requires notify: true Default: - failure-change
        :param preset: (experimental) A preset that is used as a base for Jest's configuration. A preset should point to an npm module that has a jest-preset.json or jest-preset.js file at the root. Default: - undefined
        :param prettier_path: (experimental) Sets the path to the prettier node module used to update inline snapshots. Default: - "prettier"
        :param projects: (experimental) When the projects configuration is provided with an array of paths or glob patterns, Jest will run tests in all of the specified projects at the same time. This is great for monorepos or when working on multiple projects at the same time. Default: - undefined
        :param reporters: (experimental) Use this configuration option to add custom reporters to Jest. A custom reporter is a class that implements onRunStart, onTestStart, onTestResult, onRunComplete methods that will be called when any of those events occurs. Default: - undefined
        :param reset_mocks: (experimental) Automatically reset mock state before every test. Equivalent to calling jest.resetAllMocks() before each test. This will lead to any mocks having their fake implementations removed but does not restore their initial implementation. Default: - false
        :param reset_modules: (experimental) By default, each test file gets its own independent module registry. Enabling resetModules goes a step further and resets the module registry before running each individual test. Default: - false
        :param resolver: (experimental) This option allows the use of a custom resolver. https://jestjs.io/docs/en/configuration#resolver-string Default: - undefined
        :param restore_mocks: (experimental) Automatically restore mock state before every test. Equivalent to calling jest.restoreAllMocks() before each test. This will lead to any mocks having their fake implementations removed and restores their initial implementation. Default: - false
        :param root_dir: (experimental) The root directory that Jest should scan for tests and modules within. If you put your Jest config inside your package.json and want the root directory to be the root of your repo, the value for this config param will default to the directory of the package.json. Default: - directory of the package.json
        :param roots: (experimental) A list of paths to directories that Jest should use to search for files in. Default: - [""]
        :param runner: (experimental) This option allows you to use a custom runner instead of Jest's default test runner. Default: - "jest-runner"
        :param setup_files: (experimental) A list of paths to modules that run some code to configure or set up the testing environment. Each setupFile will be run once per test file. Since every test runs in its own environment, these scripts will be executed in the testing environment immediately before executing the test code itself. Default: - []
        :param setup_files_after_env: (experimental) A list of paths to modules that run some code to configure or set up the testing framework before each test file in the suite is executed. Since setupFiles executes before the test framework is installed in the environment, this script file presents you the opportunity of running some code immediately after the test framework has been installed in the environment. Default: - []
        :param slow_test_threshold: (experimental) The number of seconds after which a test is considered as slow and reported as such in the results. Default: - 5
        :param snapshot_resolver: (experimental) The path to a module that can resolve test<->snapshot path. This config option lets you customize where Jest stores snapshot files on disk. Default: - undefined
        :param snapshot_serializers: (experimental) A list of paths to snapshot serializer modules Jest should use for snapshot testing. Default: = []
        :param test_environment: (experimental) The test environment that will be used for testing. The default environment in Jest is a browser-like environment through jsdom. If you are building a node service, you can use the node option to use a node-like environment instead. Default: - "jsdom"
        :param test_environment_options: (experimental) Test environment options that will be passed to the testEnvironment. The relevant options depend on the environment. Default: - {}
        :param test_failure_exit_code: (experimental) The exit code Jest returns on test failure. Default: - 1
        :param test_match: (experimental) The glob patterns Jest uses to detect test files. By default it looks for .js, .jsx, .ts and .tsx files inside of **tests** folders, as well as any files with a suffix of .test or .spec (e.g. Component.test.js or Component.spec.js). It will also find files called test.js or spec.js. Default: ['**/**tests**/**/*.[jt]s?(x)', '**/?(*.)+(spec|test).[tj]s?(x)']
        :param test_path_ignore_patterns: (experimental) An array of regexp pattern strings that are matched against all test paths before executing the test. If the test path matches any of the patterns, it will be skipped. Default: - ["/node_modules/"]
        :param test_regex: (experimental) The pattern or patterns Jest uses to detect test files. By default it looks for .js, .jsx, .ts and .tsx files inside of **tests** folders, as well as any files with a suffix of .test or .spec (e.g. Component.test.js or Component.spec.js). It will also find files called test.js or spec.js. Default: - (/**tests**/.*|(\\.|/)(test|spec))\\.[jt]sx?$
        :param test_results_processor: (experimental) This option allows the use of a custom results processor. Default: - undefined
        :param test_runner: (experimental) This option allows the use of a custom test runner. The default is jasmine2. A custom test runner can be provided by specifying a path to a test runner implementation. Default: - "jasmine2"
        :param test_sequencer: (experimental) This option allows you to use a custom sequencer instead of Jest's default. Sort may optionally return a Promise. Default: - "@jest/test-sequencer"
        :param test_timeout: (experimental) Default timeout of a test in milliseconds. Default: - 5000
        :param test_url: (experimental) This option sets the URL for the jsdom environment. It is reflected in properties such as location.href. Default: - "http://localhost"
        :param timers: (experimental) Setting this value to legacy or fake allows the use of fake timers for functions such as setTimeout. Fake timers are useful when a piece of code sets a long timeout that we don't want to wait for in a test. Default: - "real"
        :param transform: (experimental) A map from regular expressions to paths to transformers. A transformer is a module that provides a synchronous function for transforming source files. Default: - {"\\.[jt]sx?$": "babel-jest"}
        :param transform_ignore_patterns: (experimental) An array of regexp pattern strings that are matched against all source file paths before transformation. If the test path matches any of the patterns, it will not be transformed. Default: - ["/node_modules/", "\\.pnp\\.[^\\/]+$"]
        :param unmocked_module_path_patterns: (experimental) An array of regexp pattern strings that are matched against all modules before the module loader will automatically return a mock for them. If a module's path matches any of the patterns in this list, it will not be automatically mocked by the module loader. Default: - []
        :param verbose: (experimental) Indicates whether each individual test should be reported during the run. All errors will also still be shown on the bottom after execution. Note that if there is only one test file being run it will default to true. Default: - false
        :param watchman: (experimental) Whether to use watchman for file crawling. Default: - true
        :param watch_path_ignore_patterns: (experimental) An array of RegExp patterns that are matched against all source file paths before re-running tests in watch mode. If the file path matches any of the patterns, when it is updated, it will not trigger a re-run of tests. Default: - []
        :param watch_plugins: Default: -

        :stability: experimental
        '''
        if isinstance(coverage_threshold, dict):
            coverage_threshold = CoverageThreshold(**coverage_threshold)
        if isinstance(haste, dict):
            haste = HasteConfig(**haste)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38439e86b40e7bc302e4faa48880e15ba8a10e5a2769a5b73cbf33a01a318752)
            check_type(argname="argument additional_options", value=additional_options, expected_type=type_hints["additional_options"])
            check_type(argname="argument automock", value=automock, expected_type=type_hints["automock"])
            check_type(argname="argument bail", value=bail, expected_type=type_hints["bail"])
            check_type(argname="argument cache_directory", value=cache_directory, expected_type=type_hints["cache_directory"])
            check_type(argname="argument clear_mocks", value=clear_mocks, expected_type=type_hints["clear_mocks"])
            check_type(argname="argument collect_coverage", value=collect_coverage, expected_type=type_hints["collect_coverage"])
            check_type(argname="argument collect_coverage_from", value=collect_coverage_from, expected_type=type_hints["collect_coverage_from"])
            check_type(argname="argument coverage_directory", value=coverage_directory, expected_type=type_hints["coverage_directory"])
            check_type(argname="argument coverage_path_ignore_patterns", value=coverage_path_ignore_patterns, expected_type=type_hints["coverage_path_ignore_patterns"])
            check_type(argname="argument coverage_provider", value=coverage_provider, expected_type=type_hints["coverage_provider"])
            check_type(argname="argument coverage_reporters", value=coverage_reporters, expected_type=type_hints["coverage_reporters"])
            check_type(argname="argument coverage_threshold", value=coverage_threshold, expected_type=type_hints["coverage_threshold"])
            check_type(argname="argument dependency_extractor", value=dependency_extractor, expected_type=type_hints["dependency_extractor"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument error_on_deprecated", value=error_on_deprecated, expected_type=type_hints["error_on_deprecated"])
            check_type(argname="argument extra_globals", value=extra_globals, expected_type=type_hints["extra_globals"])
            check_type(argname="argument force_coverage_match", value=force_coverage_match, expected_type=type_hints["force_coverage_match"])
            check_type(argname="argument globals", value=globals, expected_type=type_hints["globals"])
            check_type(argname="argument global_setup", value=global_setup, expected_type=type_hints["global_setup"])
            check_type(argname="argument global_teardown", value=global_teardown, expected_type=type_hints["global_teardown"])
            check_type(argname="argument haste", value=haste, expected_type=type_hints["haste"])
            check_type(argname="argument inject_globals", value=inject_globals, expected_type=type_hints["inject_globals"])
            check_type(argname="argument max_concurrency", value=max_concurrency, expected_type=type_hints["max_concurrency"])
            check_type(argname="argument max_workers", value=max_workers, expected_type=type_hints["max_workers"])
            check_type(argname="argument module_directories", value=module_directories, expected_type=type_hints["module_directories"])
            check_type(argname="argument module_file_extensions", value=module_file_extensions, expected_type=type_hints["module_file_extensions"])
            check_type(argname="argument module_name_mapper", value=module_name_mapper, expected_type=type_hints["module_name_mapper"])
            check_type(argname="argument module_path_ignore_patterns", value=module_path_ignore_patterns, expected_type=type_hints["module_path_ignore_patterns"])
            check_type(argname="argument module_paths", value=module_paths, expected_type=type_hints["module_paths"])
            check_type(argname="argument notify", value=notify, expected_type=type_hints["notify"])
            check_type(argname="argument notify_mode", value=notify_mode, expected_type=type_hints["notify_mode"])
            check_type(argname="argument preset", value=preset, expected_type=type_hints["preset"])
            check_type(argname="argument prettier_path", value=prettier_path, expected_type=type_hints["prettier_path"])
            check_type(argname="argument projects", value=projects, expected_type=type_hints["projects"])
            check_type(argname="argument reporters", value=reporters, expected_type=type_hints["reporters"])
            check_type(argname="argument reset_mocks", value=reset_mocks, expected_type=type_hints["reset_mocks"])
            check_type(argname="argument reset_modules", value=reset_modules, expected_type=type_hints["reset_modules"])
            check_type(argname="argument resolver", value=resolver, expected_type=type_hints["resolver"])
            check_type(argname="argument restore_mocks", value=restore_mocks, expected_type=type_hints["restore_mocks"])
            check_type(argname="argument root_dir", value=root_dir, expected_type=type_hints["root_dir"])
            check_type(argname="argument roots", value=roots, expected_type=type_hints["roots"])
            check_type(argname="argument runner", value=runner, expected_type=type_hints["runner"])
            check_type(argname="argument setup_files", value=setup_files, expected_type=type_hints["setup_files"])
            check_type(argname="argument setup_files_after_env", value=setup_files_after_env, expected_type=type_hints["setup_files_after_env"])
            check_type(argname="argument slow_test_threshold", value=slow_test_threshold, expected_type=type_hints["slow_test_threshold"])
            check_type(argname="argument snapshot_resolver", value=snapshot_resolver, expected_type=type_hints["snapshot_resolver"])
            check_type(argname="argument snapshot_serializers", value=snapshot_serializers, expected_type=type_hints["snapshot_serializers"])
            check_type(argname="argument test_environment", value=test_environment, expected_type=type_hints["test_environment"])
            check_type(argname="argument test_environment_options", value=test_environment_options, expected_type=type_hints["test_environment_options"])
            check_type(argname="argument test_failure_exit_code", value=test_failure_exit_code, expected_type=type_hints["test_failure_exit_code"])
            check_type(argname="argument test_match", value=test_match, expected_type=type_hints["test_match"])
            check_type(argname="argument test_path_ignore_patterns", value=test_path_ignore_patterns, expected_type=type_hints["test_path_ignore_patterns"])
            check_type(argname="argument test_regex", value=test_regex, expected_type=type_hints["test_regex"])
            check_type(argname="argument test_results_processor", value=test_results_processor, expected_type=type_hints["test_results_processor"])
            check_type(argname="argument test_runner", value=test_runner, expected_type=type_hints["test_runner"])
            check_type(argname="argument test_sequencer", value=test_sequencer, expected_type=type_hints["test_sequencer"])
            check_type(argname="argument test_timeout", value=test_timeout, expected_type=type_hints["test_timeout"])
            check_type(argname="argument test_url", value=test_url, expected_type=type_hints["test_url"])
            check_type(argname="argument timers", value=timers, expected_type=type_hints["timers"])
            check_type(argname="argument transform", value=transform, expected_type=type_hints["transform"])
            check_type(argname="argument transform_ignore_patterns", value=transform_ignore_patterns, expected_type=type_hints["transform_ignore_patterns"])
            check_type(argname="argument unmocked_module_path_patterns", value=unmocked_module_path_patterns, expected_type=type_hints["unmocked_module_path_patterns"])
            check_type(argname="argument verbose", value=verbose, expected_type=type_hints["verbose"])
            check_type(argname="argument watchman", value=watchman, expected_type=type_hints["watchman"])
            check_type(argname="argument watch_path_ignore_patterns", value=watch_path_ignore_patterns, expected_type=type_hints["watch_path_ignore_patterns"])
            check_type(argname="argument watch_plugins", value=watch_plugins, expected_type=type_hints["watch_plugins"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_options is not None:
            self._values["additional_options"] = additional_options
        if automock is not None:
            self._values["automock"] = automock
        if bail is not None:
            self._values["bail"] = bail
        if cache_directory is not None:
            self._values["cache_directory"] = cache_directory
        if clear_mocks is not None:
            self._values["clear_mocks"] = clear_mocks
        if collect_coverage is not None:
            self._values["collect_coverage"] = collect_coverage
        if collect_coverage_from is not None:
            self._values["collect_coverage_from"] = collect_coverage_from
        if coverage_directory is not None:
            self._values["coverage_directory"] = coverage_directory
        if coverage_path_ignore_patterns is not None:
            self._values["coverage_path_ignore_patterns"] = coverage_path_ignore_patterns
        if coverage_provider is not None:
            self._values["coverage_provider"] = coverage_provider
        if coverage_reporters is not None:
            self._values["coverage_reporters"] = coverage_reporters
        if coverage_threshold is not None:
            self._values["coverage_threshold"] = coverage_threshold
        if dependency_extractor is not None:
            self._values["dependency_extractor"] = dependency_extractor
        if display_name is not None:
            self._values["display_name"] = display_name
        if error_on_deprecated is not None:
            self._values["error_on_deprecated"] = error_on_deprecated
        if extra_globals is not None:
            self._values["extra_globals"] = extra_globals
        if force_coverage_match is not None:
            self._values["force_coverage_match"] = force_coverage_match
        if globals is not None:
            self._values["globals"] = globals
        if global_setup is not None:
            self._values["global_setup"] = global_setup
        if global_teardown is not None:
            self._values["global_teardown"] = global_teardown
        if haste is not None:
            self._values["haste"] = haste
        if inject_globals is not None:
            self._values["inject_globals"] = inject_globals
        if max_concurrency is not None:
            self._values["max_concurrency"] = max_concurrency
        if max_workers is not None:
            self._values["max_workers"] = max_workers
        if module_directories is not None:
            self._values["module_directories"] = module_directories
        if module_file_extensions is not None:
            self._values["module_file_extensions"] = module_file_extensions
        if module_name_mapper is not None:
            self._values["module_name_mapper"] = module_name_mapper
        if module_path_ignore_patterns is not None:
            self._values["module_path_ignore_patterns"] = module_path_ignore_patterns
        if module_paths is not None:
            self._values["module_paths"] = module_paths
        if notify is not None:
            self._values["notify"] = notify
        if notify_mode is not None:
            self._values["notify_mode"] = notify_mode
        if preset is not None:
            self._values["preset"] = preset
        if prettier_path is not None:
            self._values["prettier_path"] = prettier_path
        if projects is not None:
            self._values["projects"] = projects
        if reporters is not None:
            self._values["reporters"] = reporters
        if reset_mocks is not None:
            self._values["reset_mocks"] = reset_mocks
        if reset_modules is not None:
            self._values["reset_modules"] = reset_modules
        if resolver is not None:
            self._values["resolver"] = resolver
        if restore_mocks is not None:
            self._values["restore_mocks"] = restore_mocks
        if root_dir is not None:
            self._values["root_dir"] = root_dir
        if roots is not None:
            self._values["roots"] = roots
        if runner is not None:
            self._values["runner"] = runner
        if setup_files is not None:
            self._values["setup_files"] = setup_files
        if setup_files_after_env is not None:
            self._values["setup_files_after_env"] = setup_files_after_env
        if slow_test_threshold is not None:
            self._values["slow_test_threshold"] = slow_test_threshold
        if snapshot_resolver is not None:
            self._values["snapshot_resolver"] = snapshot_resolver
        if snapshot_serializers is not None:
            self._values["snapshot_serializers"] = snapshot_serializers
        if test_environment is not None:
            self._values["test_environment"] = test_environment
        if test_environment_options is not None:
            self._values["test_environment_options"] = test_environment_options
        if test_failure_exit_code is not None:
            self._values["test_failure_exit_code"] = test_failure_exit_code
        if test_match is not None:
            self._values["test_match"] = test_match
        if test_path_ignore_patterns is not None:
            self._values["test_path_ignore_patterns"] = test_path_ignore_patterns
        if test_regex is not None:
            self._values["test_regex"] = test_regex
        if test_results_processor is not None:
            self._values["test_results_processor"] = test_results_processor
        if test_runner is not None:
            self._values["test_runner"] = test_runner
        if test_sequencer is not None:
            self._values["test_sequencer"] = test_sequencer
        if test_timeout is not None:
            self._values["test_timeout"] = test_timeout
        if test_url is not None:
            self._values["test_url"] = test_url
        if timers is not None:
            self._values["timers"] = timers
        if transform is not None:
            self._values["transform"] = transform
        if transform_ignore_patterns is not None:
            self._values["transform_ignore_patterns"] = transform_ignore_patterns
        if unmocked_module_path_patterns is not None:
            self._values["unmocked_module_path_patterns"] = unmocked_module_path_patterns
        if verbose is not None:
            self._values["verbose"] = verbose
        if watchman is not None:
            self._values["watchman"] = watchman
        if watch_path_ignore_patterns is not None:
            self._values["watch_path_ignore_patterns"] = watch_path_ignore_patterns
        if watch_plugins is not None:
            self._values["watch_plugins"] = watch_plugins

    @builtins.property
    def additional_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Escape hatch to allow any value.

        :stability: experimental
        '''
        result = self._values.get("additional_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def automock(self) -> typing.Optional[builtins.bool]:
        '''(experimental) This option tells Jest that all imported modules in your tests should be mocked automatically.

        All modules used in your tests will have a replacement implementation, keeping the API surface

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("automock")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bail(self) -> typing.Optional[typing.Union[jsii.Number, builtins.bool]]:
        '''(experimental) By default, Jest runs all tests and produces all errors into the console upon completion.

        The bail config option can be used here to have Jest stop running tests after n failures.
        Setting bail to true is the same as setting bail to 1.

        :default: - 0

        :stability: experimental
        '''
        result = self._values.get("bail")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, builtins.bool]], result)

    @builtins.property
    def cache_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) The directory where Jest should store its cached dependency information.

        :default: - "/tmp/"

        :stability: experimental
        '''
        result = self._values.get("cache_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def clear_mocks(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically clear mock calls and instances before every test.

        Equivalent to calling jest.clearAllMocks() before each test.
        This does not remove any mock implementation that may have been provided

        :default: true

        :stability: experimental
        '''
        result = self._values.get("clear_mocks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def collect_coverage(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the coverage information should be collected while executing the test.

        Because this retrofits all executed files with coverage collection statements,
        it may significantly slow down your tests

        :default: true

        :stability: experimental
        '''
        result = self._values.get("collect_coverage")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def collect_coverage_from(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of glob patterns indicating a set of files for which coverage information should be collected.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("collect_coverage_from")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def coverage_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) The directory where Jest should output its coverage files.

        :default: "coverage"

        :stability: experimental
        '''
        result = self._values.get("coverage_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def coverage_path_ignore_patterns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of regexp pattern strings that are matched against all file paths before executing the test.

        If the file path matches any of the patterns, coverage information will be skipped

        :default: "/node_modules/"

        :stability: experimental
        '''
        result = self._values.get("coverage_path_ignore_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def coverage_provider(self) -> typing.Optional[builtins.str]:
        '''(experimental) Indicates which provider should be used to instrument code for coverage.

        Allowed values are babel (default) or v8

        :default: - "babel"

        :stability: experimental
        '''
        result = self._values.get("coverage_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def coverage_reporters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of reporter names that Jest uses when writing coverage reports.

        Any istanbul reporter can be used

        :default: - ["json", "lcov", "text", "clover", "cobertura"]

        :stability: experimental
        '''
        result = self._values.get("coverage_reporters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def coverage_threshold(self) -> typing.Optional[CoverageThreshold]:
        '''(experimental) Specify the global coverage thresholds.

        This will be used to configure minimum threshold enforcement
        for coverage results. Thresholds can be specified as global, as a glob, and as a directory or file path.
        If thresholds aren't met, jest will fail.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("coverage_threshold")
        return typing.cast(typing.Optional[CoverageThreshold], result)

    @builtins.property
    def dependency_extractor(self) -> typing.Optional[builtins.str]:
        '''(experimental) This option allows the use of a custom dependency extractor.

        It must be a node module that exports an object with an extract function

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("dependency_extractor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Any:
        '''(experimental) Allows for a label to be printed alongside a test while it is running.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Any, result)

    @builtins.property
    def error_on_deprecated(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Make calling deprecated APIs throw helpful error messages.

        Useful for easing the upgrade process.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("error_on_deprecated")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def extra_globals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Test files run inside a vm, which slows calls to global context properties (e.g. Math). With this option you can specify extra properties to be defined inside the vm for faster lookups.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("extra_globals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def force_coverage_match(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Test files are normally ignored from collecting code coverage.

        With this option, you can overwrite this behavior and include otherwise ignored files in code coverage.

        :default: - ['']

        :stability: experimental
        '''
        result = self._values.get("force_coverage_match")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def globals(self) -> typing.Any:
        '''(experimental) A set of global variables that need to be available in all test environments.

        :default: - {}

        :stability: experimental
        '''
        result = self._values.get("globals")
        return typing.cast(typing.Any, result)

    @builtins.property
    def global_setup(self) -> typing.Optional[builtins.str]:
        '''(experimental) This option allows the use of a custom global setup module which exports an async function that is triggered once before all test suites.

        This function gets Jest's globalConfig object as a parameter.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("global_setup")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_teardown(self) -> typing.Optional[builtins.str]:
        '''(experimental) This option allows the use of a custom global teardown module which exports an async function that is triggered once after all test suites.

        This function gets Jest's globalConfig object as a parameter.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("global_teardown")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def haste(self) -> typing.Optional[HasteConfig]:
        '''(experimental) This will be used to configure the behavior of jest-haste-map, Jest's internal file crawler/cache system.

        :default: - {}

        :stability: experimental
        '''
        result = self._values.get("haste")
        return typing.cast(typing.Optional[HasteConfig], result)

    @builtins.property
    def inject_globals(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Insert Jest's globals (expect, test, describe, beforeEach etc.) into the global environment. If you set this to false, you should import from.

        :default: - true

        :stability: experimental
        :jest: /globals
        '''
        result = self._values.get("inject_globals")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_concurrency(self) -> typing.Optional[jsii.Number]:
        '''(experimental) A number limiting the number of tests that are allowed to run at the same time when using test.concurrent. Any test above this limit will be queued and executed once a slot is released.

        :default: - 5

        :stability: experimental
        '''
        result = self._values.get("max_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_workers(self) -> typing.Optional[typing.Union[builtins.str, jsii.Number]]:
        '''(experimental) Specifies the maximum number of workers the worker-pool will spawn for running tests.

        In single run mode,
        this defaults to the number of the cores available on your machine minus one for the main thread
        In watch mode, this defaults to half of the available cores on your machine.
        For environments with variable CPUs available, you can use percentage based configuration: "maxWorkers": "50%"

        :default: - the number of the cores available on your machine minus one for the main thread

        :stability: experimental
        '''
        result = self._values.get("max_workers")
        return typing.cast(typing.Optional[typing.Union[builtins.str, jsii.Number]], result)

    @builtins.property
    def module_directories(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of directory names to be searched recursively up from the requiring module's location.

        Setting this option will override the default, if you wish to still search node_modules for packages
        include it along with any other options: ["node_modules", "bower_components"]

        :default: - ["node_modules"]

        :stability: experimental
        '''
        result = self._values.get("module_directories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def module_file_extensions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of file extensions your modules use.

        If you require modules without specifying a file extension,
        these are the extensions Jest will look for, in left-to-right order.

        :default: - ["js", "json", "jsx", "ts", "tsx", "node"]

        :stability: experimental
        '''
        result = self._values.get("module_file_extensions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def module_name_mapper(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, typing.List[builtins.str]]]]:
        '''(experimental) A map from regular expressions to module names or to arrays of module names that allow to stub out resources, like images or styles with a single module.

        :default: - null

        :stability: experimental
        '''
        result = self._values.get("module_name_mapper")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, typing.List[builtins.str]]]], result)

    @builtins.property
    def module_path_ignore_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of regexp pattern strings that are matched against all module paths before those paths are to be considered 'visible' to the module loader.

        If a given module's path matches any of the patterns,
        it will not be require()-able in the test environment.

        :default: - []

        :stability: experimental
        '''
        result = self._values.get("module_path_ignore_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def module_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An alternative API to setting the NODE_PATH env variable, modulePaths is an array of absolute paths to additional locations to search when resolving modules.

        Use the  string token to include
        the path to your project's root directory. Example: ["/app/"].

        :default: - []

        :stability: experimental
        '''
        result = self._values.get("module_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def notify(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Activates notifications for test results.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("notify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def notify_mode(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies notification mode.

        Requires notify: true

        :default: - failure-change

        :stability: experimental
        '''
        result = self._values.get("notify_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preset(self) -> typing.Optional[builtins.str]:
        '''(experimental) A preset that is used as a base for Jest's configuration.

        A preset should point to an npm module
        that has a jest-preset.json or jest-preset.js file at the root.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("preset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prettier_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Sets the path to the prettier node module used to update inline snapshots.

        :default: - "prettier"

        :stability: experimental
        '''
        result = self._values.get("prettier_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def projects(
        self,
    ) -> typing.Optional[typing.List[typing.Union[builtins.str, typing.Mapping[builtins.str, typing.Any]]]]:
        '''(experimental) When the projects configuration is provided with an array of paths or glob patterns, Jest will run tests in all of the specified projects at the same time.

        This is great for monorepos or
        when working on multiple projects at the same time.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("projects")
        return typing.cast(typing.Optional[typing.List[typing.Union[builtins.str, typing.Mapping[builtins.str, typing.Any]]]], result)

    @builtins.property
    def reporters(self) -> typing.Optional[typing.List["JestReporter"]]:
        '''(experimental) Use this configuration option to add custom reporters to Jest.

        A custom reporter is a class
        that implements onRunStart, onTestStart, onTestResult, onRunComplete methods that will be
        called when any of those events occurs.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("reporters")
        return typing.cast(typing.Optional[typing.List["JestReporter"]], result)

    @builtins.property
    def reset_mocks(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically reset mock state before every test.

        Equivalent to calling jest.resetAllMocks()
        before each test. This will lead to any mocks having their fake implementations removed but
        does not restore their initial implementation.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("reset_mocks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def reset_modules(self) -> typing.Optional[builtins.bool]:
        '''(experimental) By default, each test file gets its own independent module registry.

        Enabling resetModules
        goes a step further and resets the module registry before running each individual test.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("reset_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def resolver(self) -> typing.Optional[builtins.str]:
        '''(experimental) This option allows the use of a custom resolver.

        https://jestjs.io/docs/en/configuration#resolver-string

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("resolver")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_mocks(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically restore mock state before every test.

        Equivalent to calling jest.restoreAllMocks()
        before each test. This will lead to any mocks having their fake implementations removed and
        restores their initial implementation.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("restore_mocks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def root_dir(self) -> typing.Optional[builtins.str]:
        '''(experimental) The root directory that Jest should scan for tests and modules within.

        If you put your Jest
        config inside your package.json and want the root directory to be the root of your repo, the
        value for this config param will default to the directory of the package.json.

        :default: - directory of the package.json

        :stability: experimental
        '''
        result = self._values.get("root_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def roots(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of paths to directories that Jest should use to search for files in.

        :default: - [""]

        :stability: experimental
        '''
        result = self._values.get("roots")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def runner(self) -> typing.Optional[builtins.str]:
        '''(experimental) This option allows you to use a custom runner instead of Jest's default test runner.

        :default: - "jest-runner"

        :stability: experimental
        '''
        result = self._values.get("runner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def setup_files(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of paths to modules that run some code to configure or set up the testing environment.

        Each setupFile will be run once per test file. Since every test runs in its own environment,
        these scripts will be executed in the testing environment immediately before executing the
        test code itself.

        :default: - []

        :stability: experimental
        '''
        result = self._values.get("setup_files")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def setup_files_after_env(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of paths to modules that run some code to configure or set up the testing framework before each test file in the suite is executed.

        Since setupFiles executes before the test
        framework is installed in the environment, this script file presents you the opportunity of
        running some code immediately after the test framework has been installed in the environment.

        :default: - []

        :stability: experimental
        '''
        result = self._values.get("setup_files_after_env")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def slow_test_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of seconds after which a test is considered as slow and reported as such in the results.

        :default: - 5

        :stability: experimental
        '''
        result = self._values.get("slow_test_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snapshot_resolver(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path to a module that can resolve test<->snapshot path.

        This config option lets you customize
        where Jest stores snapshot files on disk.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("snapshot_resolver")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_serializers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of paths to snapshot serializer modules Jest should use for snapshot testing.

        :default: = []

        :stability: experimental
        '''
        result = self._values.get("snapshot_serializers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def test_environment(self) -> typing.Optional[builtins.str]:
        '''(experimental) The test environment that will be used for testing.

        The default environment in Jest is a
        browser-like environment through jsdom. If you are building a node service, you can use the node
        option to use a node-like environment instead.

        :default: - "jsdom"

        :stability: experimental
        '''
        result = self._values.get("test_environment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def test_environment_options(self) -> typing.Any:
        '''(experimental) Test environment options that will be passed to the testEnvironment.

        The relevant options depend on the environment.

        :default: - {}

        :stability: experimental
        '''
        result = self._values.get("test_environment_options")
        return typing.cast(typing.Any, result)

    @builtins.property
    def test_failure_exit_code(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The exit code Jest returns on test failure.

        :default: - 1

        :stability: experimental
        '''
        result = self._values.get("test_failure_exit_code")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def test_match(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The glob patterns Jest uses to detect test files.

        By default it looks for .js, .jsx, .ts and .tsx
        files inside of **tests** folders, as well as any files with a suffix of .test or .spec
        (e.g. Component.test.js or Component.spec.js). It will also find files called test.js or spec.js.

        :default: ['**/**tests**/**/*.[jt]s?(x)', '**/?(*.)+(spec|test).[tj]s?(x)']

        :stability: experimental
        '''
        result = self._values.get("test_match")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def test_path_ignore_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of regexp pattern strings that are matched against all test paths before executing the test.

        If the test path matches any of the patterns, it will be skipped.

        :default: - ["/node_modules/"]

        :stability: experimental
        '''
        result = self._values.get("test_path_ignore_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def test_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]]:
        '''(experimental) The pattern or patterns Jest uses to detect test files.

        By default it looks for .js, .jsx, .ts and .tsx
        files inside of **tests** folders, as well as any files with a suffix of .test or .spec
        (e.g. Component.test.js or Component.spec.js). It will also find files called test.js or spec.js.

        :default: - (/**tests**/.*|(\\.|/)(test|spec))\\.[jt]sx?$

        :stability: experimental
        '''
        result = self._values.get("test_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]], result)

    @builtins.property
    def test_results_processor(self) -> typing.Optional[builtins.str]:
        '''(experimental) This option allows the use of a custom results processor.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("test_results_processor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def test_runner(self) -> typing.Optional[builtins.str]:
        '''(experimental) This option allows the use of a custom test runner.

        The default is jasmine2. A custom test runner
        can be provided by specifying a path to a test runner implementation.

        :default: - "jasmine2"

        :stability: experimental
        '''
        result = self._values.get("test_runner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def test_sequencer(self) -> typing.Optional[builtins.str]:
        '''(experimental) This option allows you to use a custom sequencer instead of Jest's default.

        Sort may optionally return a Promise.

        :default: - "@jest/test-sequencer"

        :stability: experimental
        '''
        result = self._values.get("test_sequencer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def test_timeout(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Default timeout of a test in milliseconds.

        :default: - 5000

        :stability: experimental
        '''
        result = self._values.get("test_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def test_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) This option sets the URL for the jsdom environment.

        It is reflected in properties such as location.href.

        :default: - "http://localhost"

        :stability: experimental
        '''
        result = self._values.get("test_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timers(self) -> typing.Optional[builtins.str]:
        '''(experimental) Setting this value to legacy or fake allows the use of fake timers for functions such as setTimeout.

        Fake timers are useful when a piece of code sets a long timeout that we don't want to wait for in a test.

        :default: - "real"

        :stability: experimental
        '''
        result = self._values.get("timers")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transform(self) -> typing.Optional[typing.Mapping[builtins.str, "Transform"]]:
        '''(experimental) A map from regular expressions to paths to transformers.

        A transformer is a module that provides a
        synchronous function for transforming source files.

        :default: - {"\\.[jt]sx?$": "babel-jest"}

        :stability: experimental
        '''
        result = self._values.get("transform")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "Transform"]], result)

    @builtins.property
    def transform_ignore_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of regexp pattern strings that are matched against all source file paths before transformation.

        If the test path matches any of the patterns, it will not be transformed.

        :default: - ["/node_modules/", "\\.pnp\\.[^\\/]+$"]

        :stability: experimental
        '''
        result = self._values.get("transform_ignore_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def unmocked_module_path_patterns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of regexp pattern strings that are matched against all modules before the module loader will automatically return a mock for them.

        If a module's path matches any of the patterns in this list, it
        will not be automatically mocked by the module loader.

        :default: - []

        :stability: experimental
        '''
        result = self._values.get("unmocked_module_path_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def verbose(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether each individual test should be reported during the run.

        All errors will also
        still be shown on the bottom after execution. Note that if there is only one test file being run
        it will default to true.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("verbose")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def watchman(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to use watchman for file crawling.

        :default: - true

        :stability: experimental
        '''
        result = self._values.get("watchman")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def watch_path_ignore_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of RegExp patterns that are matched against all source file paths before re-running tests in watch mode.

        If the file path matches any of the patterns, when it is updated, it will not trigger
        a re-run of tests.

        :default: - []

        :stability: experimental
        '''
        result = self._values.get("watch_path_ignore_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def watch_plugins(self) -> typing.Optional[typing.List["WatchPlugin"]]:
        '''
        :default: -

        :stability: experimental
        '''
        result = self._values.get("watch_plugins")
        return typing.cast(typing.Optional[typing.List["WatchPlugin"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JestConfigOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.JestOptions",
    jsii_struct_bases=[],
    name_mapping={
        "config_file_path": "configFilePath",
        "coverage": "coverage",
        "coverage_text": "coverageText",
        "extra_cli_options": "extraCliOptions",
        "ignore_patterns": "ignorePatterns",
        "jest_config": "jestConfig",
        "jest_version": "jestVersion",
        "junit_reporting": "junitReporting",
        "preserve_default_reporters": "preserveDefaultReporters",
        "update_snapshot": "updateSnapshot",
    },
)
class JestOptions:
    def __init__(
        self,
        *,
        config_file_path: typing.Optional[builtins.str] = None,
        coverage: typing.Optional[builtins.bool] = None,
        coverage_text: typing.Optional[builtins.bool] = None,
        extra_cli_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        jest_config: typing.Optional[typing.Union[JestConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        jest_version: typing.Optional[builtins.str] = None,
        junit_reporting: typing.Optional[builtins.bool] = None,
        preserve_default_reporters: typing.Optional[builtins.bool] = None,
        update_snapshot: typing.Optional["UpdateSnapshot"] = None,
    ) -> None:
        '''
        :param config_file_path: (experimental) Path to JSON config file for Jest. Default: - No separate config file, jest settings are stored in package.json
        :param coverage: (deprecated) Collect coverage. Deprecated Default: true
        :param coverage_text: (experimental) Include the ``text`` coverage reporter, which means that coverage summary is printed at the end of the jest execution. Default: true
        :param extra_cli_options: (experimental) Additional options to pass to the Jest CLI invocation. Default: - no extra options
        :param ignore_patterns: (deprecated) Defines ``testPathIgnorePatterns`` and ``coveragePathIgnorePatterns``. Default: ["/node_modules/"]
        :param jest_config: (experimental) Jest configuration. Default: - default jest configuration
        :param jest_version: (experimental) The version of jest to use. Note that same version is used as version of ``@types/jest`` and ``ts-jest`` (if Typescript in use), so given version should work also for those. Default: - installs the latest jest version
        :param junit_reporting: (experimental) Result processing with jest-junit. Output directory is ``test-reports/``. Default: true
        :param preserve_default_reporters: (experimental) Preserve the default Jest reporter when additional reporters are added. Default: true
        :param update_snapshot: (experimental) Whether to update snapshots in task "test" (which is executed in task "build" and build workflows), or create a separate task "test:update" for updating snapshots. Default: - ALWAYS

        :stability: experimental
        '''
        if isinstance(jest_config, dict):
            jest_config = JestConfigOptions(**jest_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fea73c8bcc51e881c3829384cb90956e3310a1a08296d32da54fc51bd1b0872)
            check_type(argname="argument config_file_path", value=config_file_path, expected_type=type_hints["config_file_path"])
            check_type(argname="argument coverage", value=coverage, expected_type=type_hints["coverage"])
            check_type(argname="argument coverage_text", value=coverage_text, expected_type=type_hints["coverage_text"])
            check_type(argname="argument extra_cli_options", value=extra_cli_options, expected_type=type_hints["extra_cli_options"])
            check_type(argname="argument ignore_patterns", value=ignore_patterns, expected_type=type_hints["ignore_patterns"])
            check_type(argname="argument jest_config", value=jest_config, expected_type=type_hints["jest_config"])
            check_type(argname="argument jest_version", value=jest_version, expected_type=type_hints["jest_version"])
            check_type(argname="argument junit_reporting", value=junit_reporting, expected_type=type_hints["junit_reporting"])
            check_type(argname="argument preserve_default_reporters", value=preserve_default_reporters, expected_type=type_hints["preserve_default_reporters"])
            check_type(argname="argument update_snapshot", value=update_snapshot, expected_type=type_hints["update_snapshot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config_file_path is not None:
            self._values["config_file_path"] = config_file_path
        if coverage is not None:
            self._values["coverage"] = coverage
        if coverage_text is not None:
            self._values["coverage_text"] = coverage_text
        if extra_cli_options is not None:
            self._values["extra_cli_options"] = extra_cli_options
        if ignore_patterns is not None:
            self._values["ignore_patterns"] = ignore_patterns
        if jest_config is not None:
            self._values["jest_config"] = jest_config
        if jest_version is not None:
            self._values["jest_version"] = jest_version
        if junit_reporting is not None:
            self._values["junit_reporting"] = junit_reporting
        if preserve_default_reporters is not None:
            self._values["preserve_default_reporters"] = preserve_default_reporters
        if update_snapshot is not None:
            self._values["update_snapshot"] = update_snapshot

    @builtins.property
    def config_file_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to JSON config file for Jest.

        :default: - No separate config file, jest settings are stored in package.json

        :stability: experimental
        '''
        result = self._values.get("config_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def coverage(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Collect coverage.

        Deprecated

        :default: true

        :deprecated: use jestConfig.collectCoverage

        :stability: deprecated
        '''
        result = self._values.get("coverage")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def coverage_text(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include the ``text`` coverage reporter, which means that coverage summary is printed at the end of the jest execution.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("coverage_text")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def extra_cli_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional options to pass to the Jest CLI invocation.

        :default: - no extra options

        :stability: experimental
        '''
        result = self._values.get("extra_cli_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ignore_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Defines ``testPathIgnorePatterns`` and ``coveragePathIgnorePatterns``.

        :default: ["/node_modules/"]

        :deprecated: use jestConfig.coveragePathIgnorePatterns or jestConfig.testPathIgnorePatterns respectively

        :stability: deprecated
        '''
        result = self._values.get("ignore_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jest_config(self) -> typing.Optional[JestConfigOptions]:
        '''(experimental) Jest configuration.

        :default: - default jest configuration

        :stability: experimental
        '''
        result = self._values.get("jest_config")
        return typing.cast(typing.Optional[JestConfigOptions], result)

    @builtins.property
    def jest_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of jest to use.

        Note that same version is used as version of ``@types/jest`` and ``ts-jest`` (if Typescript in use), so given version should work also for those.

        :default: - installs the latest jest version

        :stability: experimental
        '''
        result = self._values.get("jest_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def junit_reporting(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Result processing with jest-junit.

        Output directory is ``test-reports/``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("junit_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def preserve_default_reporters(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Preserve the default Jest reporter when additional reporters are added.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("preserve_default_reporters")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def update_snapshot(self) -> typing.Optional["UpdateSnapshot"]:
        '''(experimental) Whether to update snapshots in task "test" (which is executed in task "build" and build workflows), or create a separate task "test:update" for updating snapshots.

        :default: - ALWAYS

        :stability: experimental
        '''
        result = self._values.get("update_snapshot")
        return typing.cast(typing.Optional["UpdateSnapshot"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class JestReporter(metaclass=jsii.JSIIMeta, jsii_type="projen.javascript.JestReporter"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        name: builtins.str,
        options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''
        :param name: -
        :param options: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1adfce4c8efbbf8de3e660eb3dc3c2d165cf8436faf2119d2f15900dda8e814a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
        jsii.create(self.__class__, self, [name, options])


class NodePackage(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.javascript.NodePackage",
):
    '''(experimental) Represents the npm ``package.json`` file.

    :stability: experimental
    '''

    def __init__(
        self,
        project: _Project_57d89203,
        *,
        allow_library_dependencies: typing.Optional[builtins.bool] = None,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        author_organization: typing.Optional[builtins.bool] = None,
        author_url: typing.Optional[builtins.str] = None,
        auto_detect_bin: typing.Optional[builtins.bool] = None,
        bin: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bugs_email: typing.Optional[builtins.str] = None,
        bugs_url: typing.Optional[builtins.str] = None,
        bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        code_artifact_options: typing.Optional[typing.Union[CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        entrypoint: typing.Optional[builtins.str] = None,
        homepage: typing.Optional[builtins.str] = None,
        keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
        license: typing.Optional[builtins.str] = None,
        licensed: typing.Optional[builtins.bool] = None,
        max_node_version: typing.Optional[builtins.str] = None,
        min_node_version: typing.Optional[builtins.str] = None,
        npm_access: typing.Optional["NpmAccess"] = None,
        npm_registry: typing.Optional[builtins.str] = None,
        npm_registry_url: typing.Optional[builtins.str] = None,
        npm_token_secret: typing.Optional[builtins.str] = None,
        package_manager: typing.Optional["NodePackageManager"] = None,
        package_name: typing.Optional[builtins.str] = None,
        peer_dependency_options: typing.Optional[typing.Union["PeerDependencyOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        peer_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        pnpm_version: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        repository_directory: typing.Optional[builtins.str] = None,
        scoped_packages_options: typing.Optional[typing.Sequence[typing.Union["ScopedPackagesOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
        scripts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        stability: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param allow_library_dependencies: (experimental) Allow the project to include ``peerDependencies`` and ``bundledDependencies``. This is normally only allowed for libraries. For apps, there's no meaning for specifying these. Default: true
        :param author_email: (experimental) Author's e-mail.
        :param author_name: (experimental) Author's name.
        :param author_organization: (experimental) Is the author an organization.
        :param author_url: (experimental) Author's URL / Website.
        :param auto_detect_bin: (experimental) Automatically add all executables under the ``bin`` directory to your ``package.json`` file under the ``bin`` section. Default: true
        :param bin: (experimental) Binary programs vended with your module. You can use this option to add/customize how binaries are represented in your ``package.json``, but unless ``autoDetectBin`` is ``false``, every executable file under ``bin`` will automatically be added to this section.
        :param bugs_email: (experimental) The email address to which issues should be reported.
        :param bugs_url: (experimental) The url to your project's issue tracker.
        :param bundled_deps: (experimental) List of dependencies to bundle into this module. These modules will be added both to the ``dependencies`` section and ``bundledDependencies`` section of your ``package.json``. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include.
        :param code_artifact_options: (experimental) Options for npm packages using AWS CodeArtifact. This is required if publishing packages to, or installing scoped packages from AWS CodeArtifact Default: - undefined
        :param deps: (experimental) Runtime dependencies of this module. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include. Default: []
        :param description: (experimental) The description is just a string that helps people understand the purpose of the package. It can be used when searching for packages in a package manager as well. See https://classic.yarnpkg.com/en/docs/package-json/#toc-description
        :param dev_deps: (experimental) Build dependencies for this module. These dependencies will only be available in your build environment but will not be fetched when this module is consumed. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include. Default: []
        :param entrypoint: (experimental) Module entrypoint (``main`` in ``package.json``). Set to an empty string to not include ``main`` in your package.json Default: "lib/index.js"
        :param homepage: (experimental) Package's Homepage / Website.
        :param keywords: (experimental) Keywords to include in ``package.json``.
        :param license: (experimental) License's SPDX identifier. See https://github.com/projen/projen/tree/main/license-text for a list of supported licenses. Use the ``licensed`` option if you want to no license to be specified. Default: "Apache-2.0"
        :param licensed: (experimental) Indicates if a license should be added. Default: true
        :param max_node_version: (experimental) Minimum node.js version to require via ``engines`` (inclusive). Default: - no max
        :param min_node_version: (experimental) Minimum Node.js version to require via package.json ``engines`` (inclusive). Default: - no "engines" specified
        :param npm_access: (experimental) Access level of the npm package. Default: - for scoped packages (e.g. ``foo@bar``), the default is ``NpmAccess.RESTRICTED``, for non-scoped packages, the default is ``NpmAccess.PUBLIC``.
        :param npm_registry: (deprecated) The host name of the npm registry to publish to. Cannot be set together with ``npmRegistryUrl``.
        :param npm_registry_url: (experimental) The base URL of the npm package registry. Must be a URL (e.g. start with "https://" or "http://") Default: "https://registry.npmjs.org"
        :param npm_token_secret: (experimental) GitHub secret which contains the NPM token to use when publishing packages. Default: "NPM_TOKEN"
        :param package_manager: (experimental) The Node Package Manager used to execute scripts. Default: NodePackageManager.YARN
        :param package_name: (experimental) The "name" in package.json. Default: - defaults to project name
        :param peer_dependency_options: (experimental) Options for ``peerDeps``.
        :param peer_deps: (experimental) Peer dependencies for this module. Dependencies listed here are required to be installed (and satisfied) by the *consumer* of this library. Using peer dependencies allows you to ensure that only a single module of a certain library exists in the ``node_modules`` tree of your consumers. Note that prior to npm@7, peer dependencies are *not* automatically installed, which means that adding peer dependencies to a library will be a breaking change for your customers. Unless ``peerDependencyOptions.pinnedDevDependency`` is disabled (it is enabled by default), projen will automatically add a dev dependency with a pinned version for each peer dependency. This will ensure that you build & test your module against the lowest peer version required. Default: []
        :param pnpm_version: (experimental) The version of PNPM to use if using PNPM as a package manager. Default: "7"
        :param repository: (experimental) The repository is the location where the actual code for your package lives. See https://classic.yarnpkg.com/en/docs/package-json/#toc-repository
        :param repository_directory: (experimental) If the package.json for your package is not in the root directory (for example if it is part of a monorepo), you can specify the directory in which it lives.
        :param scoped_packages_options: (experimental) Options for privately hosted scoped packages. Default: - fetch all scoped packages from the public npm registry
        :param scripts: (deprecated) npm scripts to include. If a script has the same name as a standard script, the standard script will be overwritten. Also adds the script as a task. Default: {}
        :param stability: (experimental) Package's Stability.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10cd20471c8ed8e2de153476379f00bfa1b587c92e8982006812a0e3e9c846b)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = NodePackageOptions(
            allow_library_dependencies=allow_library_dependencies,
            author_email=author_email,
            author_name=author_name,
            author_organization=author_organization,
            author_url=author_url,
            auto_detect_bin=auto_detect_bin,
            bin=bin,
            bugs_email=bugs_email,
            bugs_url=bugs_url,
            bundled_deps=bundled_deps,
            code_artifact_options=code_artifact_options,
            deps=deps,
            description=description,
            dev_deps=dev_deps,
            entrypoint=entrypoint,
            homepage=homepage,
            keywords=keywords,
            license=license,
            licensed=licensed,
            max_node_version=max_node_version,
            min_node_version=min_node_version,
            npm_access=npm_access,
            npm_registry=npm_registry,
            npm_registry_url=npm_registry_url,
            npm_token_secret=npm_token_secret,
            package_manager=package_manager,
            package_name=package_name,
            peer_dependency_options=peer_dependency_options,
            peer_deps=peer_deps,
            pnpm_version=pnpm_version,
            repository=repository,
            repository_directory=repository_directory,
            scoped_packages_options=scoped_packages_options,
            scripts=scripts,
            stability=stability,
        )

        jsii.create(self.__class__, self, [project, options])

    @jsii.member(jsii_name="addBin")
    def add_bin(self, bins: typing.Mapping[builtins.str, builtins.str]) -> None:
        '''
        :param bins: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e4b0ad9e59ff790a5783923af9f1d0af9bff2ab30e03185a659093189f08f3)
            check_type(argname="argument bins", value=bins, expected_type=type_hints["bins"])
        return typing.cast(None, jsii.invoke(self, "addBin", [bins]))

    @jsii.member(jsii_name="addBundledDeps")
    def add_bundled_deps(self, *deps: builtins.str) -> None:
        '''(experimental) Defines bundled dependencies.

        Bundled dependencies will be added as normal dependencies as well as to the
        ``bundledDependencies`` section of your ``package.json``.

        :param deps: Names modules to install. By default, the the dependency will be installed in the next ``npx projen`` run and the version will be recorded in your ``package.json`` file. You can upgrade manually or using ``yarn add/upgrade``. If you wish to specify a version range use this syntax: ``module@^7``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f25a81261c7551ce7372a9e98c98143fde0ccda688f4a7f1b1d64783c6fa198)
            check_type(argname="argument deps", value=deps, expected_type=typing.Tuple[type_hints["deps"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addBundledDeps", [*deps]))

    @jsii.member(jsii_name="addDeps")
    def add_deps(self, *deps: builtins.str) -> None:
        '''(experimental) Defines normal dependencies.

        :param deps: Names modules to install. By default, the the dependency will be installed in the next ``npx projen`` run and the version will be recorded in your ``package.json`` file. You can upgrade manually or using ``yarn add/upgrade``. If you wish to specify a version range use this syntax: ``module@^7``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c66a164e21aa660923f1f9ca9a679f353501f43d2c6de87372bb0dadcc74e863)
            check_type(argname="argument deps", value=deps, expected_type=typing.Tuple[type_hints["deps"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addDeps", [*deps]))

    @jsii.member(jsii_name="addDevDeps")
    def add_dev_deps(self, *deps: builtins.str) -> None:
        '''(experimental) Defines development/test dependencies.

        :param deps: Names modules to install. By default, the the dependency will be installed in the next ``npx projen`` run and the version will be recorded in your ``package.json`` file. You can upgrade manually or using ``yarn add/upgrade``. If you wish to specify a version range use this syntax: ``module@^7``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80cd6a4a71ddbf3dcbb4c76baab6b84aa13c5bb5b4e36d4e51cb18378a0d733d)
            check_type(argname="argument deps", value=deps, expected_type=typing.Tuple[type_hints["deps"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addDevDeps", [*deps]))

    @jsii.member(jsii_name="addEngine")
    def add_engine(self, engine: builtins.str, version: builtins.str) -> None:
        '''(experimental) Adds an ``engines`` requirement to your package.

        :param engine: The engine (e.g. ``node``).
        :param version: The semantic version requirement (e.g. ``^10``).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944e49e6183bbfb83f5284a94826a5dc27eb1d8daf9f1c782135dc5893acfcae)
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast(None, jsii.invoke(self, "addEngine", [engine, version]))

    @jsii.member(jsii_name="addField")
    def add_field(self, name: builtins.str, value: typing.Any) -> None:
        '''(experimental) Directly set fields in ``package.json``.

        :param name: field name.
        :param value: field value.

        :stability: experimental
        :escape: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85137a3059fcbe1e4bfe64a7b2d097445ae0743f4ff0ecde43a1c4cefbeafa7a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addField", [name, value]))

    @jsii.member(jsii_name="addKeywords")
    def add_keywords(self, *keywords: builtins.str) -> None:
        '''(experimental) Adds keywords to package.json (deduplicated).

        :param keywords: The keywords to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a4904c7ed7ae8a2b9f8ade987155393a1f966700d60dc9e833e6615cc57118b)
            check_type(argname="argument keywords", value=keywords, expected_type=typing.Tuple[type_hints["keywords"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addKeywords", [*keywords]))

    @jsii.member(jsii_name="addPackageResolutions")
    def add_package_resolutions(self, *resolutions: builtins.str) -> None:
        '''(experimental) Defines resolutions for dependencies to change the normally resolved version of a dependency to something else.

        :param resolutions: Names resolutions to be added. Specify a version or range with this syntax: ``module@^7``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bc2a812647b8c3d299d563a0f6381c44edd2be02fb67a3dcd27d127bb238ba5)
            check_type(argname="argument resolutions", value=resolutions, expected_type=typing.Tuple[type_hints["resolutions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addPackageResolutions", [*resolutions]))

    @jsii.member(jsii_name="addPeerDeps")
    def add_peer_deps(self, *deps: builtins.str) -> None:
        '''(experimental) Defines peer dependencies.

        When adding peer dependencies, a devDependency will also be added on the
        pinned version of the declared peer. This will ensure that you are testing
        your code against the minimum version required from your consumers.

        :param deps: Names modules to install. By default, the the dependency will be installed in the next ``npx projen`` run and the version will be recorded in your ``package.json`` file. You can upgrade manually or using ``yarn add/upgrade``. If you wish to specify a version range use this syntax: ``module@^7``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__665c114cee41c00dba6a88193e09aacf3c44c03eeb33f5248f4a0715ee25f803)
            check_type(argname="argument deps", value=deps, expected_type=typing.Tuple[type_hints["deps"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addPeerDeps", [*deps]))

    @jsii.member(jsii_name="addVersion")
    def add_version(self, version: builtins.str) -> None:
        '''(experimental) Sets the package version.

        :param version: Package version.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d456bed502e180a081411555ef7dae9f59ac8b07e536f2a144d134c8593a095)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast(None, jsii.invoke(self, "addVersion", [version]))

    @jsii.member(jsii_name="hasScript")
    def has_script(self, name: builtins.str) -> builtins.bool:
        '''(deprecated) Indicates if a script by the given name is defined.

        :param name: The name of the script.

        :deprecated: Use ``project.tasks.tryFind(name)``

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12c7fbb63b42bcfe1afac4c97478186870515282ad2fec02e2dfe5256265514)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(builtins.bool, jsii.invoke(self, "hasScript", [name]))

    @jsii.member(jsii_name="postSynthesize")
    def post_synthesize(self) -> None:
        '''(experimental) Called after synthesis.

        Order is *not* guaranteed.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "postSynthesize", []))

    @jsii.member(jsii_name="removeScript")
    def remove_script(self, name: builtins.str) -> None:
        '''(experimental) Removes an npm script (always successful).

        :param name: The name of the script.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfa2462931cf54e94ef49bfaf6682ca11a2539f8cdd625d39c838f78b350e770)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(None, jsii.invoke(self, "removeScript", [name]))

    @jsii.member(jsii_name="setScript")
    def set_script(self, name: builtins.str, command: builtins.str) -> None:
        '''(experimental) Add a npm package.json script.

        :param name: The script name.
        :param command: The command to execute.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a17ecc6ba7925a0e02706203a5f4f1888b6b3708f11e2bc0aab1ce1b5343b5ea)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
        return typing.cast(None, jsii.invoke(self, "setScript", [name, command]))

    @jsii.member(jsii_name="synthesize")
    def synthesize(self) -> None:
        '''(experimental) Synthesizes files to the project output directory.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "synthesize", []))

    @jsii.member(jsii_name="tryResolveDependencyVersion")
    def try_resolve_dependency_version(
        self,
        dependency_name: builtins.str,
    ) -> typing.Optional[builtins.str]:
        '''(experimental) Attempt to resolve the currently installed version for a given dependency.

        :param dependency_name: Dependency to resolve for.

        :stability: experimental
        :remarks:

        This method will first look through the current project's dependencies.
        If found and semantically valid (not '*'), that will be used.
        Otherwise, it will fall back to locating a ``package.json`` manifest for the dependency
        through node's internal resolution reading the version from there.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29de3cb9e10a8965e109e3d914eff0debf87b70a39d82f150168063dd734ac03)
            check_type(argname="argument dependency_name", value=dependency_name, expected_type=type_hints["dependency_name"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "tryResolveDependencyVersion", [dependency_name]))

    @builtins.property
    @jsii.member(jsii_name="allowLibraryDependencies")
    def allow_library_dependencies(self) -> builtins.bool:
        '''(experimental) Allow project to take library dependencies.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "allowLibraryDependencies"))

    @builtins.property
    @jsii.member(jsii_name="entrypoint")
    def entrypoint(self) -> builtins.str:
        '''(experimental) The module's entrypoint (e.g. ``lib/index.js``).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "entrypoint"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> _JsonFile_fa8164db:
        '''(experimental) The package.json file.

        :stability: experimental
        '''
        return typing.cast(_JsonFile_fa8164db, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="installAndUpdateLockfileCommand")
    def install_and_update_lockfile_command(self) -> builtins.str:
        '''(experimental) Renders ``yarn install`` or ``npm install`` with lockfile update (not frozen).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "installAndUpdateLockfileCommand"))

    @builtins.property
    @jsii.member(jsii_name="installCiTask")
    def install_ci_task(self) -> _Task_9fa875b6:
        '''(experimental) The task for installing project dependencies (frozen).

        :stability: experimental
        '''
        return typing.cast(_Task_9fa875b6, jsii.get(self, "installCiTask"))

    @builtins.property
    @jsii.member(jsii_name="installCommand")
    def install_command(self) -> builtins.str:
        '''(experimental) Returns the command to execute in order to install all dependencies (always frozen).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "installCommand"))

    @builtins.property
    @jsii.member(jsii_name="installTask")
    def install_task(self) -> _Task_9fa875b6:
        '''(experimental) The task for installing project dependencies (non-frozen).

        :stability: experimental
        '''
        return typing.cast(_Task_9fa875b6, jsii.get(self, "installTask"))

    @builtins.property
    @jsii.member(jsii_name="lockFile")
    def lock_file(self) -> builtins.str:
        '''(experimental) The name of the lock file.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "lockFile"))

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> typing.Any:
        '''
        :deprecated: use ``addField(x, y)``

        :stability: deprecated
        '''
        return typing.cast(typing.Any, jsii.get(self, "manifest"))

    @builtins.property
    @jsii.member(jsii_name="npmAccess")
    def npm_access(self) -> "NpmAccess":
        '''(experimental) npm package access level.

        :stability: experimental
        '''
        return typing.cast("NpmAccess", jsii.get(self, "npmAccess"))

    @builtins.property
    @jsii.member(jsii_name="npmRegistry")
    def npm_registry(self) -> builtins.str:
        '''(experimental) The npm registry host (e.g. ``registry.npmjs.org``).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "npmRegistry"))

    @builtins.property
    @jsii.member(jsii_name="npmRegistryUrl")
    def npm_registry_url(self) -> builtins.str:
        '''(experimental) npm registry (e.g. ``https://registry.npmjs.org``). Use ``npmRegistryHost`` to get just the host name.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "npmRegistryUrl"))

    @builtins.property
    @jsii.member(jsii_name="packageManager")
    def package_manager(self) -> "NodePackageManager":
        '''(experimental) The package manager to use.

        :stability: experimental
        '''
        return typing.cast("NodePackageManager", jsii.get(self, "packageManager"))

    @builtins.property
    @jsii.member(jsii_name="packageName")
    def package_name(self) -> builtins.str:
        '''(experimental) The name of the npm package.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "packageName"))

    @builtins.property
    @jsii.member(jsii_name="projenCommand")
    def projen_command(self) -> builtins.str:
        '''(experimental) The command which executes "projen".

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "projenCommand"))

    @builtins.property
    @jsii.member(jsii_name="codeArtifactOptions")
    def code_artifact_options(self) -> typing.Optional[CodeArtifactOptions]:
        '''(experimental) Options for npm packages using AWS CodeArtifact.

        This is required if publishing packages to, or installing scoped packages from AWS CodeArtifact

        :default: - undefined

        :stability: experimental
        '''
        return typing.cast(typing.Optional[CodeArtifactOptions], jsii.get(self, "codeArtifactOptions"))

    @builtins.property
    @jsii.member(jsii_name="license")
    def license(self) -> typing.Optional[builtins.str]:
        '''(experimental) The SPDX license of this module.

        ``undefined`` if this package is not licensed.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "license"))

    @builtins.property
    @jsii.member(jsii_name="maxNodeVersion")
    def max_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Maximum node version required by this package.

        :default: - no maximum.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxNodeVersion"))

    @builtins.property
    @jsii.member(jsii_name="minNodeVersion")
    def min_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum node.js version required by this package.

        :default: - no minimum

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minNodeVersion"))

    @builtins.property
    @jsii.member(jsii_name="npmTokenSecret")
    def npm_token_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret which contains the NPM token to use when publishing packages.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "npmTokenSecret"))

    @builtins.property
    @jsii.member(jsii_name="pnpmVersion")
    def pnpm_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of PNPM to use if using PNPM as a package manager.

        :default: "7"

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pnpmVersion"))

    @builtins.property
    @jsii.member(jsii_name="scopedPackagesOptions")
    def scoped_packages_options(
        self,
    ) -> typing.Optional[typing.List["ScopedPackagesOptions"]]:
        '''(experimental) Options for privately hosted scoped packages.

        :default: undefined

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List["ScopedPackagesOptions"]], jsii.get(self, "scopedPackagesOptions"))


@jsii.enum(jsii_type="projen.javascript.NodePackageManager")
class NodePackageManager(enum.Enum):
    '''(experimental) The node package manager to use.

    :stability: experimental
    '''

    YARN = "YARN"
    '''(experimental) Use ``yarn`` as the package manager.

    :stability: experimental
    '''
    YARN2 = "YARN2"
    '''(experimental) Use ``yarn`` versions >= 2 as the package manager.

    :stability: experimental
    '''
    NPM = "NPM"
    '''(experimental) Use ``npm`` as the package manager.

    :stability: experimental
    '''
    PNPM = "PNPM"
    '''(experimental) Use ``pnpm`` as the package manager.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.javascript.NodePackageOptions",
    jsii_struct_bases=[],
    name_mapping={
        "allow_library_dependencies": "allowLibraryDependencies",
        "author_email": "authorEmail",
        "author_name": "authorName",
        "author_organization": "authorOrganization",
        "author_url": "authorUrl",
        "auto_detect_bin": "autoDetectBin",
        "bin": "bin",
        "bugs_email": "bugsEmail",
        "bugs_url": "bugsUrl",
        "bundled_deps": "bundledDeps",
        "code_artifact_options": "codeArtifactOptions",
        "deps": "deps",
        "description": "description",
        "dev_deps": "devDeps",
        "entrypoint": "entrypoint",
        "homepage": "homepage",
        "keywords": "keywords",
        "license": "license",
        "licensed": "licensed",
        "max_node_version": "maxNodeVersion",
        "min_node_version": "minNodeVersion",
        "npm_access": "npmAccess",
        "npm_registry": "npmRegistry",
        "npm_registry_url": "npmRegistryUrl",
        "npm_token_secret": "npmTokenSecret",
        "package_manager": "packageManager",
        "package_name": "packageName",
        "peer_dependency_options": "peerDependencyOptions",
        "peer_deps": "peerDeps",
        "pnpm_version": "pnpmVersion",
        "repository": "repository",
        "repository_directory": "repositoryDirectory",
        "scoped_packages_options": "scopedPackagesOptions",
        "scripts": "scripts",
        "stability": "stability",
    },
)
class NodePackageOptions:
    def __init__(
        self,
        *,
        allow_library_dependencies: typing.Optional[builtins.bool] = None,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        author_organization: typing.Optional[builtins.bool] = None,
        author_url: typing.Optional[builtins.str] = None,
        auto_detect_bin: typing.Optional[builtins.bool] = None,
        bin: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bugs_email: typing.Optional[builtins.str] = None,
        bugs_url: typing.Optional[builtins.str] = None,
        bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        code_artifact_options: typing.Optional[typing.Union[CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        entrypoint: typing.Optional[builtins.str] = None,
        homepage: typing.Optional[builtins.str] = None,
        keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
        license: typing.Optional[builtins.str] = None,
        licensed: typing.Optional[builtins.bool] = None,
        max_node_version: typing.Optional[builtins.str] = None,
        min_node_version: typing.Optional[builtins.str] = None,
        npm_access: typing.Optional["NpmAccess"] = None,
        npm_registry: typing.Optional[builtins.str] = None,
        npm_registry_url: typing.Optional[builtins.str] = None,
        npm_token_secret: typing.Optional[builtins.str] = None,
        package_manager: typing.Optional[NodePackageManager] = None,
        package_name: typing.Optional[builtins.str] = None,
        peer_dependency_options: typing.Optional[typing.Union["PeerDependencyOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        peer_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        pnpm_version: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        repository_directory: typing.Optional[builtins.str] = None,
        scoped_packages_options: typing.Optional[typing.Sequence[typing.Union["ScopedPackagesOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
        scripts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        stability: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_library_dependencies: (experimental) Allow the project to include ``peerDependencies`` and ``bundledDependencies``. This is normally only allowed for libraries. For apps, there's no meaning for specifying these. Default: true
        :param author_email: (experimental) Author's e-mail.
        :param author_name: (experimental) Author's name.
        :param author_organization: (experimental) Is the author an organization.
        :param author_url: (experimental) Author's URL / Website.
        :param auto_detect_bin: (experimental) Automatically add all executables under the ``bin`` directory to your ``package.json`` file under the ``bin`` section. Default: true
        :param bin: (experimental) Binary programs vended with your module. You can use this option to add/customize how binaries are represented in your ``package.json``, but unless ``autoDetectBin`` is ``false``, every executable file under ``bin`` will automatically be added to this section.
        :param bugs_email: (experimental) The email address to which issues should be reported.
        :param bugs_url: (experimental) The url to your project's issue tracker.
        :param bundled_deps: (experimental) List of dependencies to bundle into this module. These modules will be added both to the ``dependencies`` section and ``bundledDependencies`` section of your ``package.json``. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include.
        :param code_artifact_options: (experimental) Options for npm packages using AWS CodeArtifact. This is required if publishing packages to, or installing scoped packages from AWS CodeArtifact Default: - undefined
        :param deps: (experimental) Runtime dependencies of this module. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include. Default: []
        :param description: (experimental) The description is just a string that helps people understand the purpose of the package. It can be used when searching for packages in a package manager as well. See https://classic.yarnpkg.com/en/docs/package-json/#toc-description
        :param dev_deps: (experimental) Build dependencies for this module. These dependencies will only be available in your build environment but will not be fetched when this module is consumed. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include. Default: []
        :param entrypoint: (experimental) Module entrypoint (``main`` in ``package.json``). Set to an empty string to not include ``main`` in your package.json Default: "lib/index.js"
        :param homepage: (experimental) Package's Homepage / Website.
        :param keywords: (experimental) Keywords to include in ``package.json``.
        :param license: (experimental) License's SPDX identifier. See https://github.com/projen/projen/tree/main/license-text for a list of supported licenses. Use the ``licensed`` option if you want to no license to be specified. Default: "Apache-2.0"
        :param licensed: (experimental) Indicates if a license should be added. Default: true
        :param max_node_version: (experimental) Minimum node.js version to require via ``engines`` (inclusive). Default: - no max
        :param min_node_version: (experimental) Minimum Node.js version to require via package.json ``engines`` (inclusive). Default: - no "engines" specified
        :param npm_access: (experimental) Access level of the npm package. Default: - for scoped packages (e.g. ``foo@bar``), the default is ``NpmAccess.RESTRICTED``, for non-scoped packages, the default is ``NpmAccess.PUBLIC``.
        :param npm_registry: (deprecated) The host name of the npm registry to publish to. Cannot be set together with ``npmRegistryUrl``.
        :param npm_registry_url: (experimental) The base URL of the npm package registry. Must be a URL (e.g. start with "https://" or "http://") Default: "https://registry.npmjs.org"
        :param npm_token_secret: (experimental) GitHub secret which contains the NPM token to use when publishing packages. Default: "NPM_TOKEN"
        :param package_manager: (experimental) The Node Package Manager used to execute scripts. Default: NodePackageManager.YARN
        :param package_name: (experimental) The "name" in package.json. Default: - defaults to project name
        :param peer_dependency_options: (experimental) Options for ``peerDeps``.
        :param peer_deps: (experimental) Peer dependencies for this module. Dependencies listed here are required to be installed (and satisfied) by the *consumer* of this library. Using peer dependencies allows you to ensure that only a single module of a certain library exists in the ``node_modules`` tree of your consumers. Note that prior to npm@7, peer dependencies are *not* automatically installed, which means that adding peer dependencies to a library will be a breaking change for your customers. Unless ``peerDependencyOptions.pinnedDevDependency`` is disabled (it is enabled by default), projen will automatically add a dev dependency with a pinned version for each peer dependency. This will ensure that you build & test your module against the lowest peer version required. Default: []
        :param pnpm_version: (experimental) The version of PNPM to use if using PNPM as a package manager. Default: "7"
        :param repository: (experimental) The repository is the location where the actual code for your package lives. See https://classic.yarnpkg.com/en/docs/package-json/#toc-repository
        :param repository_directory: (experimental) If the package.json for your package is not in the root directory (for example if it is part of a monorepo), you can specify the directory in which it lives.
        :param scoped_packages_options: (experimental) Options for privately hosted scoped packages. Default: - fetch all scoped packages from the public npm registry
        :param scripts: (deprecated) npm scripts to include. If a script has the same name as a standard script, the standard script will be overwritten. Also adds the script as a task. Default: {}
        :param stability: (experimental) Package's Stability.

        :stability: experimental
        '''
        if isinstance(code_artifact_options, dict):
            code_artifact_options = CodeArtifactOptions(**code_artifact_options)
        if isinstance(peer_dependency_options, dict):
            peer_dependency_options = PeerDependencyOptions(**peer_dependency_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32555a77b63910142de45100c4a6d74880ddece00a3cbae9c278034675668ea0)
            check_type(argname="argument allow_library_dependencies", value=allow_library_dependencies, expected_type=type_hints["allow_library_dependencies"])
            check_type(argname="argument author_email", value=author_email, expected_type=type_hints["author_email"])
            check_type(argname="argument author_name", value=author_name, expected_type=type_hints["author_name"])
            check_type(argname="argument author_organization", value=author_organization, expected_type=type_hints["author_organization"])
            check_type(argname="argument author_url", value=author_url, expected_type=type_hints["author_url"])
            check_type(argname="argument auto_detect_bin", value=auto_detect_bin, expected_type=type_hints["auto_detect_bin"])
            check_type(argname="argument bin", value=bin, expected_type=type_hints["bin"])
            check_type(argname="argument bugs_email", value=bugs_email, expected_type=type_hints["bugs_email"])
            check_type(argname="argument bugs_url", value=bugs_url, expected_type=type_hints["bugs_url"])
            check_type(argname="argument bundled_deps", value=bundled_deps, expected_type=type_hints["bundled_deps"])
            check_type(argname="argument code_artifact_options", value=code_artifact_options, expected_type=type_hints["code_artifact_options"])
            check_type(argname="argument deps", value=deps, expected_type=type_hints["deps"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dev_deps", value=dev_deps, expected_type=type_hints["dev_deps"])
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
            check_type(argname="argument homepage", value=homepage, expected_type=type_hints["homepage"])
            check_type(argname="argument keywords", value=keywords, expected_type=type_hints["keywords"])
            check_type(argname="argument license", value=license, expected_type=type_hints["license"])
            check_type(argname="argument licensed", value=licensed, expected_type=type_hints["licensed"])
            check_type(argname="argument max_node_version", value=max_node_version, expected_type=type_hints["max_node_version"])
            check_type(argname="argument min_node_version", value=min_node_version, expected_type=type_hints["min_node_version"])
            check_type(argname="argument npm_access", value=npm_access, expected_type=type_hints["npm_access"])
            check_type(argname="argument npm_registry", value=npm_registry, expected_type=type_hints["npm_registry"])
            check_type(argname="argument npm_registry_url", value=npm_registry_url, expected_type=type_hints["npm_registry_url"])
            check_type(argname="argument npm_token_secret", value=npm_token_secret, expected_type=type_hints["npm_token_secret"])
            check_type(argname="argument package_manager", value=package_manager, expected_type=type_hints["package_manager"])
            check_type(argname="argument package_name", value=package_name, expected_type=type_hints["package_name"])
            check_type(argname="argument peer_dependency_options", value=peer_dependency_options, expected_type=type_hints["peer_dependency_options"])
            check_type(argname="argument peer_deps", value=peer_deps, expected_type=type_hints["peer_deps"])
            check_type(argname="argument pnpm_version", value=pnpm_version, expected_type=type_hints["pnpm_version"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument repository_directory", value=repository_directory, expected_type=type_hints["repository_directory"])
            check_type(argname="argument scoped_packages_options", value=scoped_packages_options, expected_type=type_hints["scoped_packages_options"])
            check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
            check_type(argname="argument stability", value=stability, expected_type=type_hints["stability"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_library_dependencies is not None:
            self._values["allow_library_dependencies"] = allow_library_dependencies
        if author_email is not None:
            self._values["author_email"] = author_email
        if author_name is not None:
            self._values["author_name"] = author_name
        if author_organization is not None:
            self._values["author_organization"] = author_organization
        if author_url is not None:
            self._values["author_url"] = author_url
        if auto_detect_bin is not None:
            self._values["auto_detect_bin"] = auto_detect_bin
        if bin is not None:
            self._values["bin"] = bin
        if bugs_email is not None:
            self._values["bugs_email"] = bugs_email
        if bugs_url is not None:
            self._values["bugs_url"] = bugs_url
        if bundled_deps is not None:
            self._values["bundled_deps"] = bundled_deps
        if code_artifact_options is not None:
            self._values["code_artifact_options"] = code_artifact_options
        if deps is not None:
            self._values["deps"] = deps
        if description is not None:
            self._values["description"] = description
        if dev_deps is not None:
            self._values["dev_deps"] = dev_deps
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint
        if homepage is not None:
            self._values["homepage"] = homepage
        if keywords is not None:
            self._values["keywords"] = keywords
        if license is not None:
            self._values["license"] = license
        if licensed is not None:
            self._values["licensed"] = licensed
        if max_node_version is not None:
            self._values["max_node_version"] = max_node_version
        if min_node_version is not None:
            self._values["min_node_version"] = min_node_version
        if npm_access is not None:
            self._values["npm_access"] = npm_access
        if npm_registry is not None:
            self._values["npm_registry"] = npm_registry
        if npm_registry_url is not None:
            self._values["npm_registry_url"] = npm_registry_url
        if npm_token_secret is not None:
            self._values["npm_token_secret"] = npm_token_secret
        if package_manager is not None:
            self._values["package_manager"] = package_manager
        if package_name is not None:
            self._values["package_name"] = package_name
        if peer_dependency_options is not None:
            self._values["peer_dependency_options"] = peer_dependency_options
        if peer_deps is not None:
            self._values["peer_deps"] = peer_deps
        if pnpm_version is not None:
            self._values["pnpm_version"] = pnpm_version
        if repository is not None:
            self._values["repository"] = repository
        if repository_directory is not None:
            self._values["repository_directory"] = repository_directory
        if scoped_packages_options is not None:
            self._values["scoped_packages_options"] = scoped_packages_options
        if scripts is not None:
            self._values["scripts"] = scripts
        if stability is not None:
            self._values["stability"] = stability

    @builtins.property
    def allow_library_dependencies(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow the project to include ``peerDependencies`` and ``bundledDependencies``.

        This is normally only allowed for libraries. For apps, there's no meaning
        for specifying these.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("allow_library_dependencies")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def author_email(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's e-mail.

        :stability: experimental
        '''
        result = self._values.get("author_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def author_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's name.

        :stability: experimental
        '''
        result = self._values.get("author_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def author_organization(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Is the author an organization.

        :stability: experimental
        '''
        result = self._values.get("author_organization")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def author_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's URL / Website.

        :stability: experimental
        '''
        result = self._values.get("author_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_detect_bin(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically add all executables under the ``bin`` directory to your ``package.json`` file under the ``bin`` section.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_detect_bin")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bin(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Binary programs vended with your module.

        You can use this option to add/customize how binaries are represented in
        your ``package.json``, but unless ``autoDetectBin`` is ``false``, every
        executable file under ``bin`` will automatically be added to this section.

        :stability: experimental
        '''
        result = self._values.get("bin")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def bugs_email(self) -> typing.Optional[builtins.str]:
        '''(experimental) The email address to which issues should be reported.

        :stability: experimental
        '''
        result = self._values.get("bugs_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bugs_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The url to your project's issue tracker.

        :stability: experimental
        '''
        result = self._values.get("bugs_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bundled_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of dependencies to bundle into this module.

        These modules will be
        added both to the ``dependencies`` section and ``bundledDependencies`` section of
        your ``package.json``.

        The recommendation is to only specify the module name here (e.g.
        ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the
        sense that it will add the module as a dependency to your ``package.json``
        file with the latest version (``^``). You can specify semver requirements in
        the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and
        this will be what you ``package.json`` will eventually include.

        :stability: experimental
        '''
        result = self._values.get("bundled_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def code_artifact_options(self) -> typing.Optional[CodeArtifactOptions]:
        '''(experimental) Options for npm packages using AWS CodeArtifact.

        This is required if publishing packages to, or installing scoped packages from AWS CodeArtifact

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("code_artifact_options")
        return typing.cast(typing.Optional[CodeArtifactOptions], result)

    @builtins.property
    def deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Runtime dependencies of this module.

        The recommendation is to only specify the module name here (e.g.
        ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the
        sense that it will add the module as a dependency to your ``package.json``
        file with the latest version (``^``). You can specify semver requirements in
        the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and
        this will be what you ``package.json`` will eventually include.

        :default: []

        :stability: experimental
        :featured: true

        Example::

            [ 'express', 'lodash', 'foo@^2' ]
        '''
        result = self._values.get("deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description is just a string that helps people understand the purpose of the package.

        It can be used when searching for packages in a package manager as well.
        See https://classic.yarnpkg.com/en/docs/package-json/#toc-description

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dev_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Build dependencies for this module.

        These dependencies will only be
        available in your build environment but will not be fetched when this
        module is consumed.

        The recommendation is to only specify the module name here (e.g.
        ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the
        sense that it will add the module as a dependency to your ``package.json``
        file with the latest version (``^``). You can specify semver requirements in
        the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and
        this will be what you ``package.json`` will eventually include.

        :default: []

        :stability: experimental
        :featured: true

        Example::

            [ 'typescript', '@types/express' ]
        '''
        result = self._values.get("dev_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def entrypoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) Module entrypoint (``main`` in ``package.json``).

        Set to an empty string to not include ``main`` in your package.json

        :default: "lib/index.js"

        :stability: experimental
        '''
        result = self._values.get("entrypoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def homepage(self) -> typing.Optional[builtins.str]:
        '''(experimental) Package's Homepage / Website.

        :stability: experimental
        '''
        result = self._values.get("homepage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keywords(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Keywords to include in ``package.json``.

        :stability: experimental
        '''
        result = self._values.get("keywords")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def license(self) -> typing.Optional[builtins.str]:
        '''(experimental) License's SPDX identifier.

        See https://github.com/projen/projen/tree/main/license-text for a list of supported licenses.
        Use the ``licensed`` option if you want to no license to be specified.

        :default: "Apache-2.0"

        :stability: experimental
        '''
        result = self._values.get("license")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def licensed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates if a license should be added.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("licensed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum node.js version to require via ``engines`` (inclusive).

        :default: - no max

        :stability: experimental
        '''
        result = self._values.get("max_node_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum Node.js version to require via package.json ``engines`` (inclusive).

        :default: - no "engines" specified

        :stability: experimental
        '''
        result = self._values.get("min_node_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_access(self) -> typing.Optional["NpmAccess"]:
        '''(experimental) Access level of the npm package.

        :default:

        - for scoped packages (e.g. ``foo@bar``), the default is
        ``NpmAccess.RESTRICTED``, for non-scoped packages, the default is
        ``NpmAccess.PUBLIC``.

        :stability: experimental
        '''
        result = self._values.get("npm_access")
        return typing.cast(typing.Optional["NpmAccess"], result)

    @builtins.property
    def npm_registry(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The host name of the npm registry to publish to.

        Cannot be set together with ``npmRegistryUrl``.

        :deprecated: use ``npmRegistryUrl`` instead

        :stability: deprecated
        '''
        result = self._values.get("npm_registry")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_registry_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The base URL of the npm package registry.

        Must be a URL (e.g. start with "https://" or "http://")

        :default: "https://registry.npmjs.org"

        :stability: experimental
        '''
        result = self._values.get("npm_registry_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_token_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret which contains the NPM token to use when publishing packages.

        :default: "NPM_TOKEN"

        :stability: experimental
        '''
        result = self._values.get("npm_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def package_manager(self) -> typing.Optional[NodePackageManager]:
        '''(experimental) The Node Package Manager used to execute scripts.

        :default: NodePackageManager.YARN

        :stability: experimental
        '''
        result = self._values.get("package_manager")
        return typing.cast(typing.Optional[NodePackageManager], result)

    @builtins.property
    def package_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The "name" in package.json.

        :default: - defaults to project name

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("package_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_dependency_options(self) -> typing.Optional["PeerDependencyOptions"]:
        '''(experimental) Options for ``peerDeps``.

        :stability: experimental
        '''
        result = self._values.get("peer_dependency_options")
        return typing.cast(typing.Optional["PeerDependencyOptions"], result)

    @builtins.property
    def peer_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Peer dependencies for this module.

        Dependencies listed here are required to
        be installed (and satisfied) by the *consumer* of this library. Using peer
        dependencies allows you to ensure that only a single module of a certain
        library exists in the ``node_modules`` tree of your consumers.

        Note that prior to npm@7, peer dependencies are *not* automatically
        installed, which means that adding peer dependencies to a library will be a
        breaking change for your customers.

        Unless ``peerDependencyOptions.pinnedDevDependency`` is disabled (it is
        enabled by default), projen will automatically add a dev dependency with a
        pinned version for each peer dependency. This will ensure that you build &
        test your module against the lowest peer version required.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("peer_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pnpm_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of PNPM to use if using PNPM as a package manager.

        :default: "7"

        :stability: experimental
        '''
        result = self._values.get("pnpm_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''(experimental) The repository is the location where the actual code for your package lives.

        See https://classic.yarnpkg.com/en/docs/package-json/#toc-repository

        :stability: experimental
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) If the package.json for your package is not in the root directory (for example if it is part of a monorepo), you can specify the directory in which it lives.

        :stability: experimental
        '''
        result = self._values.get("repository_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scoped_packages_options(
        self,
    ) -> typing.Optional[typing.List["ScopedPackagesOptions"]]:
        '''(experimental) Options for privately hosted scoped packages.

        :default: - fetch all scoped packages from the public npm registry

        :stability: experimental
        '''
        result = self._values.get("scoped_packages_options")
        return typing.cast(typing.Optional[typing.List["ScopedPackagesOptions"]], result)

    @builtins.property
    def scripts(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(deprecated) npm scripts to include.

        If a script has the same name as a standard script,
        the standard script will be overwritten.
        Also adds the script as a task.

        :default: {}

        :deprecated: use ``project.addTask()`` or ``package.setScript()``

        :stability: deprecated
        '''
        result = self._values.get("scripts")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def stability(self) -> typing.Optional[builtins.str]:
        '''(experimental) Package's Stability.

        :stability: experimental
        '''
        result = self._values.get("stability")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NodePackageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NodeProject(
    _GitHubProject_c48bc7ea,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.javascript.NodeProject",
):
    '''(experimental) Node.js project.

    :stability: experimental
    :pjid: node
    '''

    def __init__(
        self,
        *,
        default_release_branch: builtins.str,
        artifacts_directory: typing.Optional[builtins.str] = None,
        auto_approve_upgrades: typing.Optional[builtins.bool] = None,
        build_workflow: typing.Optional[builtins.bool] = None,
        build_workflow_triggers: typing.Optional[typing.Union[_Triggers_e9ae7617, typing.Dict[builtins.str, typing.Any]]] = None,
        bundler_options: typing.Optional[typing.Union[BundlerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        code_cov: typing.Optional[builtins.bool] = None,
        code_cov_token_secret: typing.Optional[builtins.str] = None,
        copyright_owner: typing.Optional[builtins.str] = None,
        copyright_period: typing.Optional[builtins.str] = None,
        dependabot: typing.Optional[builtins.bool] = None,
        dependabot_options: typing.Optional[typing.Union[_DependabotOptions_0cedc635, typing.Dict[builtins.str, typing.Any]]] = None,
        deps_upgrade: typing.Optional[builtins.bool] = None,
        deps_upgrade_options: typing.Optional[typing.Union["UpgradeDependenciesOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        gitignore: typing.Optional[typing.Sequence[builtins.str]] = None,
        jest: typing.Optional[builtins.bool] = None,
        jest_options: typing.Optional[typing.Union[JestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        mutable_build: typing.Optional[builtins.bool] = None,
        npmignore: typing.Optional[typing.Sequence[builtins.str]] = None,
        npmignore_enabled: typing.Optional[builtins.bool] = None,
        npm_ignore_options: typing.Optional[typing.Union[_IgnoreFileOptions_86c48b91, typing.Dict[builtins.str, typing.Any]]] = None,
        package: typing.Optional[builtins.bool] = None,
        prettier: typing.Optional[builtins.bool] = None,
        prettier_options: typing.Optional[typing.Union["PrettierOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        projen_dev_dependency: typing.Optional[builtins.bool] = None,
        projenrc_js: typing.Optional[builtins.bool] = None,
        projenrc_js_options: typing.Optional[typing.Union["ProjenrcOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        projen_version: typing.Optional[builtins.str] = None,
        pull_request_template: typing.Optional[builtins.bool] = None,
        pull_request_template_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
        release: typing.Optional[builtins.bool] = None,
        release_to_npm: typing.Optional[builtins.bool] = None,
        release_workflow: typing.Optional[builtins.bool] = None,
        workflow_bootstrap_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        workflow_git_identity: typing.Optional[typing.Union[_GitIdentity_6effc3de, typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_node_version: typing.Optional[builtins.str] = None,
        workflow_package_cache: typing.Optional[builtins.bool] = None,
        auto_approve_options: typing.Optional[typing.Union[_AutoApproveOptions_dac86cbe, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_AutoMergeOptions_d112cd3c, typing.Dict[builtins.str, typing.Any]]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union[_GitHubOptions_21553699, typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        mergify: typing.Optional[builtins.bool] = None,
        mergify_options: typing.Optional[typing.Union[_MergifyOptions_a6faaab3, typing.Dict[builtins.str, typing.Any]]] = None,
        project_type: typing.Optional[_ProjectType_fd80c725] = None,
        projen_credentials: typing.Optional[_GithubCredentials_ae257072] = None,
        projen_token_secret: typing.Optional[builtins.str] = None,
        readme: typing.Optional[typing.Union[_SampleReadmeProps_3518b03b, typing.Dict[builtins.str, typing.Any]]] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_StaleOptions_929db764, typing.Dict[builtins.str, typing.Any]]] = None,
        vscode: typing.Optional[builtins.bool] = None,
        allow_library_dependencies: typing.Optional[builtins.bool] = None,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        author_organization: typing.Optional[builtins.bool] = None,
        author_url: typing.Optional[builtins.str] = None,
        auto_detect_bin: typing.Optional[builtins.bool] = None,
        bin: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bugs_email: typing.Optional[builtins.str] = None,
        bugs_url: typing.Optional[builtins.str] = None,
        bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        code_artifact_options: typing.Optional[typing.Union[CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        entrypoint: typing.Optional[builtins.str] = None,
        homepage: typing.Optional[builtins.str] = None,
        keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
        license: typing.Optional[builtins.str] = None,
        licensed: typing.Optional[builtins.bool] = None,
        max_node_version: typing.Optional[builtins.str] = None,
        min_node_version: typing.Optional[builtins.str] = None,
        npm_access: typing.Optional["NpmAccess"] = None,
        npm_registry: typing.Optional[builtins.str] = None,
        npm_registry_url: typing.Optional[builtins.str] = None,
        npm_token_secret: typing.Optional[builtins.str] = None,
        package_manager: typing.Optional[NodePackageManager] = None,
        package_name: typing.Optional[builtins.str] = None,
        peer_dependency_options: typing.Optional[typing.Union["PeerDependencyOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        peer_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        pnpm_version: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        repository_directory: typing.Optional[builtins.str] = None,
        scoped_packages_options: typing.Optional[typing.Sequence[typing.Union["ScopedPackagesOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
        scripts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        stability: typing.Optional[builtins.str] = None,
        jsii_release_version: typing.Optional[builtins.str] = None,
        major_version: typing.Optional[jsii.Number] = None,
        min_major_version: typing.Optional[jsii.Number] = None,
        npm_dist_tag: typing.Optional[builtins.str] = None,
        post_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        prerelease: typing.Optional[builtins.str] = None,
        publish_dry_run: typing.Optional[builtins.bool] = None,
        publish_tasks: typing.Optional[builtins.bool] = None,
        releasable_commits: typing.Optional[_ReleasableCommits_d481ce10] = None,
        release_branches: typing.Optional[typing.Mapping[builtins.str, typing.Union[_BranchOptions_13663d08, typing.Dict[builtins.str, typing.Any]]]] = None,
        release_every_commit: typing.Optional[builtins.bool] = None,
        release_failure_issue: typing.Optional[builtins.bool] = None,
        release_failure_issue_label: typing.Optional[builtins.str] = None,
        release_schedule: typing.Optional[builtins.str] = None,
        release_tag_prefix: typing.Optional[builtins.str] = None,
        release_trigger: typing.Optional[_ReleaseTrigger_e4dc221f] = None,
        release_workflow_name: typing.Optional[builtins.str] = None,
        release_workflow_setup_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workflow_container_image: typing.Optional[builtins.str] = None,
        workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        workflow_runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
        name: builtins.str,
        commit_generated: typing.Optional[builtins.bool] = None,
        git_ignore_options: typing.Optional[typing.Union[_IgnoreFileOptions_86c48b91, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_GitOptions_a65916a3, typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union[_LoggerOptions_eb0f6309, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        parent: typing.Optional[_Project_57d89203] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union[_ProjenrcJsonOptions_9c40dd4f, typing.Dict[builtins.str, typing.Any]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union[_RenovatebotOptions_18e6b8a1, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param default_release_branch: (experimental) The name of the main release branch. Default: "main"
        :param artifacts_directory: (experimental) A directory which will contain build artifacts. Default: "dist"
        :param auto_approve_upgrades: (experimental) Automatically approve deps upgrade PRs, allowing them to be merged by mergify (if configued). Throw if set to true but ``autoApproveOptions`` are not defined. Default: - true
        :param build_workflow: (experimental) Define a GitHub workflow for building PRs. Default: - true if not a subproject
        :param build_workflow_triggers: (experimental) Build workflow triggers. Default: "{ pullRequest: {}, workflowDispatch: {} }"
        :param bundler_options: (experimental) Options for ``Bundler``.
        :param code_cov: (experimental) Define a GitHub workflow step for sending code coverage metrics to https://codecov.io/ Uses codecov/codecov-action@v3 A secret is required for private repos. Configured with ``@codeCovTokenSecret``. Default: false
        :param code_cov_token_secret: (experimental) Define the secret name for a specified https://codecov.io/ token A secret is required to send coverage for private repositories. Default: - if this option is not specified, only public repositories are supported
        :param copyright_owner: (experimental) License copyright owner. Default: - defaults to the value of authorName or "" if ``authorName`` is undefined.
        :param copyright_period: (experimental) The copyright years to put in the LICENSE file. Default: - current year
        :param dependabot: (experimental) Use dependabot to handle dependency upgrades. Cannot be used in conjunction with ``depsUpgrade``. Default: false
        :param dependabot_options: (experimental) Options for dependabot. Default: - default options
        :param deps_upgrade: (experimental) Use tasks and github workflows to handle dependency upgrades. Cannot be used in conjunction with ``dependabot``. Default: true
        :param deps_upgrade_options: (experimental) Options for ``UpgradeDependencies``. Default: - default options
        :param gitignore: (experimental) Additional entries to .gitignore.
        :param jest: (experimental) Setup jest unit tests. Default: true
        :param jest_options: (experimental) Jest options. Default: - default options
        :param mutable_build: (experimental) Automatically update files modified during builds to pull-request branches. This means that any files synthesized by projen or e.g. test snapshots will always be up-to-date before a PR is merged. Implies that PR builds do not have anti-tamper checks. Default: true
        :param npmignore: (deprecated) Additional entries to .npmignore.
        :param npmignore_enabled: (experimental) Defines an .npmignore file. Normally this is only needed for libraries that are packaged as tarballs. Default: true
        :param npm_ignore_options: (experimental) Configuration options for .npmignore file.
        :param package: (experimental) Defines a ``package`` task that will produce an npm tarball under the artifacts directory (e.g. ``dist``). Default: true
        :param prettier: (experimental) Setup prettier. Default: false
        :param prettier_options: (experimental) Prettier options. Default: - default options
        :param projen_dev_dependency: (experimental) Indicates of "projen" should be installed as a devDependency. Default: true
        :param projenrc_js: (experimental) Generate (once) .projenrc.js (in JavaScript). Set to ``false`` in order to disable .projenrc.js generation. Default: - true if projenrcJson is false
        :param projenrc_js_options: (experimental) Options for .projenrc.js. Default: - default options
        :param projen_version: (experimental) Version of projen to install. Default: - Defaults to the latest version.
        :param pull_request_template: (experimental) Include a GitHub pull request template. Default: true
        :param pull_request_template_contents: (experimental) The contents of the pull request template. Default: - default content
        :param release: (experimental) Add release management to this project. Default: - true (false for subprojects)
        :param release_to_npm: (experimental) Automatically release to npm when new versions are introduced. Default: false
        :param release_workflow: (deprecated) DEPRECATED: renamed to ``release``. Default: - true if not a subproject
        :param workflow_bootstrap_steps: (experimental) Workflow steps to use in order to bootstrap this repo. Default: "yarn install --frozen-lockfile && yarn projen"
        :param workflow_git_identity: (experimental) The git identity to use in workflows. Default: - GitHub Actions
        :param workflow_node_version: (experimental) The node version to use in GitHub workflows. Default: - same as ``minNodeVersion``
        :param workflow_package_cache: (experimental) Enable Node.js package cache in GitHub workflows. Default: false
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param github: (experimental) Enable GitHub integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param github_options: (experimental) Options for GitHub integration. Default: - see GitHubOptions
        :param gitpod: (experimental) Add a Gitpod development environment. Default: false
        :param mergify: (deprecated) Whether mergify should be enabled on this repository or not. Default: true
        :param mergify_options: (deprecated) Options for mergify. Default: - default options
        :param project_type: (deprecated) Which type of project this is (library/app). Default: ProjectType.UNKNOWN
        :param projen_credentials: (experimental) Choose a method of providing GitHub API access for projen workflows. Default: - use a personal access token named PROJEN_GITHUB_TOKEN
        :param projen_token_secret: (deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows. This token needs to have the ``repo``, ``workflows`` and ``packages`` scope. Default: "PROJEN_GITHUB_TOKEN"
        :param readme: (experimental) The README setup. Default: - { filename: 'README.md', contents: '# replace this' }
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param allow_library_dependencies: (experimental) Allow the project to include ``peerDependencies`` and ``bundledDependencies``. This is normally only allowed for libraries. For apps, there's no meaning for specifying these. Default: true
        :param author_email: (experimental) Author's e-mail.
        :param author_name: (experimental) Author's name.
        :param author_organization: (experimental) Is the author an organization.
        :param author_url: (experimental) Author's URL / Website.
        :param auto_detect_bin: (experimental) Automatically add all executables under the ``bin`` directory to your ``package.json`` file under the ``bin`` section. Default: true
        :param bin: (experimental) Binary programs vended with your module. You can use this option to add/customize how binaries are represented in your ``package.json``, but unless ``autoDetectBin`` is ``false``, every executable file under ``bin`` will automatically be added to this section.
        :param bugs_email: (experimental) The email address to which issues should be reported.
        :param bugs_url: (experimental) The url to your project's issue tracker.
        :param bundled_deps: (experimental) List of dependencies to bundle into this module. These modules will be added both to the ``dependencies`` section and ``bundledDependencies`` section of your ``package.json``. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include.
        :param code_artifact_options: (experimental) Options for npm packages using AWS CodeArtifact. This is required if publishing packages to, or installing scoped packages from AWS CodeArtifact Default: - undefined
        :param deps: (experimental) Runtime dependencies of this module. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include. Default: []
        :param description: (experimental) The description is just a string that helps people understand the purpose of the package. It can be used when searching for packages in a package manager as well. See https://classic.yarnpkg.com/en/docs/package-json/#toc-description
        :param dev_deps: (experimental) Build dependencies for this module. These dependencies will only be available in your build environment but will not be fetched when this module is consumed. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include. Default: []
        :param entrypoint: (experimental) Module entrypoint (``main`` in ``package.json``). Set to an empty string to not include ``main`` in your package.json Default: "lib/index.js"
        :param homepage: (experimental) Package's Homepage / Website.
        :param keywords: (experimental) Keywords to include in ``package.json``.
        :param license: (experimental) License's SPDX identifier. See https://github.com/projen/projen/tree/main/license-text for a list of supported licenses. Use the ``licensed`` option if you want to no license to be specified. Default: "Apache-2.0"
        :param licensed: (experimental) Indicates if a license should be added. Default: true
        :param max_node_version: (experimental) Minimum node.js version to require via ``engines`` (inclusive). Default: - no max
        :param min_node_version: (experimental) Minimum Node.js version to require via package.json ``engines`` (inclusive). Default: - no "engines" specified
        :param npm_access: (experimental) Access level of the npm package. Default: - for scoped packages (e.g. ``foo@bar``), the default is ``NpmAccess.RESTRICTED``, for non-scoped packages, the default is ``NpmAccess.PUBLIC``.
        :param npm_registry: (deprecated) The host name of the npm registry to publish to. Cannot be set together with ``npmRegistryUrl``.
        :param npm_registry_url: (experimental) The base URL of the npm package registry. Must be a URL (e.g. start with "https://" or "http://") Default: "https://registry.npmjs.org"
        :param npm_token_secret: (experimental) GitHub secret which contains the NPM token to use when publishing packages. Default: "NPM_TOKEN"
        :param package_manager: (experimental) The Node Package Manager used to execute scripts. Default: NodePackageManager.YARN
        :param package_name: (experimental) The "name" in package.json. Default: - defaults to project name
        :param peer_dependency_options: (experimental) Options for ``peerDeps``.
        :param peer_deps: (experimental) Peer dependencies for this module. Dependencies listed here are required to be installed (and satisfied) by the *consumer* of this library. Using peer dependencies allows you to ensure that only a single module of a certain library exists in the ``node_modules`` tree of your consumers. Note that prior to npm@7, peer dependencies are *not* automatically installed, which means that adding peer dependencies to a library will be a breaking change for your customers. Unless ``peerDependencyOptions.pinnedDevDependency`` is disabled (it is enabled by default), projen will automatically add a dev dependency with a pinned version for each peer dependency. This will ensure that you build & test your module against the lowest peer version required. Default: []
        :param pnpm_version: (experimental) The version of PNPM to use if using PNPM as a package manager. Default: "7"
        :param repository: (experimental) The repository is the location where the actual code for your package lives. See https://classic.yarnpkg.com/en/docs/package-json/#toc-repository
        :param repository_directory: (experimental) If the package.json for your package is not in the root directory (for example if it is part of a monorepo), you can specify the directory in which it lives.
        :param scoped_packages_options: (experimental) Options for privately hosted scoped packages. Default: - fetch all scoped packages from the public npm registry
        :param scripts: (deprecated) npm scripts to include. If a script has the same name as a standard script, the standard script will be overwritten. Also adds the script as a task. Default: {}
        :param stability: (experimental) Package's Stability.
        :param jsii_release_version: (experimental) Version requirement of ``publib`` which is used to publish modules to npm. Default: "latest"
        :param major_version: (experimental) Major version to release from the default branch. If this is specified, we bump the latest version of this major version line. If not specified, we bump the global latest version. Default: - Major version is not enforced.
        :param min_major_version: (experimental) Minimal Major version to release. This can be useful to set to 1, as breaking changes before the 1.x major release are not incrementing the major version number. Can not be set together with ``majorVersion``. Default: - No minimum version is being enforced
        :param npm_dist_tag: (experimental) The npmDistTag to use when publishing from the default branch. To set the npm dist-tag for release branches, set the ``npmDistTag`` property for each branch. Default: "latest"
        :param post_build_steps: (experimental) Steps to execute after build as part of the release workflow. Default: []
        :param prerelease: (experimental) Bump versions from the default branch as pre-releases (e.g. "beta", "alpha", "pre"). Default: - normal semantic versions
        :param publish_dry_run: (experimental) Instead of actually publishing to package managers, just print the publishing command. Default: false
        :param publish_tasks: (experimental) Define publishing tasks that can be executed manually as well as workflows. Normally, publishing only happens within automated workflows. Enable this in order to create a publishing task for each publishing activity. Default: false
        :param releasable_commits: (experimental) Find commits that should be considered releasable Used to decide if a release is required. Default: ReleasableCommits.everyCommit()
        :param release_branches: (experimental) Defines additional release branches. A workflow will be created for each release branch which will publish releases from commits in this branch. Each release branch *must* be assigned a major version number which is used to enforce that versions published from that branch always use that major version. If multiple branches are used, the ``majorVersion`` field must also be provided for the default branch. Default: - no additional branches are used for release. you can use ``addBranch()`` to add additional branches.
        :param release_every_commit: (deprecated) Automatically release new versions every commit to one of branches in ``releaseBranches``. Default: true
        :param release_failure_issue: (experimental) Create a github issue on every failed publishing task. Default: false
        :param release_failure_issue_label: (experimental) The label to apply to issues indicating publish failures. Only applies if ``releaseFailureIssue`` is true. Default: "failed-release"
        :param release_schedule: (deprecated) CRON schedule to trigger new releases. Default: - no scheduled releases
        :param release_tag_prefix: (experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers. Note: this prefix is used to detect the latest tagged version when bumping, so if you change this on a project with an existing version history, you may need to manually tag your latest release with the new prefix. Default: "v"
        :param release_trigger: (experimental) The release trigger to use. Default: - Continuous releases (``ReleaseTrigger.continuous()``)
        :param release_workflow_name: (experimental) The name of the default release workflow. Default: "Release"
        :param release_workflow_setup_steps: (experimental) A set of workflow steps to execute in order to setup the workflow container.
        :param versionrc_options: (experimental) Custom configuration used when creating changelog with standard-version package. Given values either append to default configuration or overwrite values in it. Default: - standard configuration applicable for GitHub repositories
        :param workflow_container_image: (experimental) Container image to use for GitHub workflows. Default: - default image
        :param workflow_runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param workflow_runs_on_group: (experimental) Github Runner Group selection options.
        :param name: (experimental) This is the name of your project. Default: $BASEDIR
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other sub-projects. Default: "."
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options

        :stability: experimental
        '''
        options = NodeProjectOptions(
            default_release_branch=default_release_branch,
            artifacts_directory=artifacts_directory,
            auto_approve_upgrades=auto_approve_upgrades,
            build_workflow=build_workflow,
            build_workflow_triggers=build_workflow_triggers,
            bundler_options=bundler_options,
            code_cov=code_cov,
            code_cov_token_secret=code_cov_token_secret,
            copyright_owner=copyright_owner,
            copyright_period=copyright_period,
            dependabot=dependabot,
            dependabot_options=dependabot_options,
            deps_upgrade=deps_upgrade,
            deps_upgrade_options=deps_upgrade_options,
            gitignore=gitignore,
            jest=jest,
            jest_options=jest_options,
            mutable_build=mutable_build,
            npmignore=npmignore,
            npmignore_enabled=npmignore_enabled,
            npm_ignore_options=npm_ignore_options,
            package=package,
            prettier=prettier,
            prettier_options=prettier_options,
            projen_dev_dependency=projen_dev_dependency,
            projenrc_js=projenrc_js,
            projenrc_js_options=projenrc_js_options,
            projen_version=projen_version,
            pull_request_template=pull_request_template,
            pull_request_template_contents=pull_request_template_contents,
            release=release,
            release_to_npm=release_to_npm,
            release_workflow=release_workflow,
            workflow_bootstrap_steps=workflow_bootstrap_steps,
            workflow_git_identity=workflow_git_identity,
            workflow_node_version=workflow_node_version,
            workflow_package_cache=workflow_package_cache,
            auto_approve_options=auto_approve_options,
            auto_merge=auto_merge,
            auto_merge_options=auto_merge_options,
            clobber=clobber,
            dev_container=dev_container,
            github=github,
            github_options=github_options,
            gitpod=gitpod,
            mergify=mergify,
            mergify_options=mergify_options,
            project_type=project_type,
            projen_credentials=projen_credentials,
            projen_token_secret=projen_token_secret,
            readme=readme,
            stale=stale,
            stale_options=stale_options,
            vscode=vscode,
            allow_library_dependencies=allow_library_dependencies,
            author_email=author_email,
            author_name=author_name,
            author_organization=author_organization,
            author_url=author_url,
            auto_detect_bin=auto_detect_bin,
            bin=bin,
            bugs_email=bugs_email,
            bugs_url=bugs_url,
            bundled_deps=bundled_deps,
            code_artifact_options=code_artifact_options,
            deps=deps,
            description=description,
            dev_deps=dev_deps,
            entrypoint=entrypoint,
            homepage=homepage,
            keywords=keywords,
            license=license,
            licensed=licensed,
            max_node_version=max_node_version,
            min_node_version=min_node_version,
            npm_access=npm_access,
            npm_registry=npm_registry,
            npm_registry_url=npm_registry_url,
            npm_token_secret=npm_token_secret,
            package_manager=package_manager,
            package_name=package_name,
            peer_dependency_options=peer_dependency_options,
            peer_deps=peer_deps,
            pnpm_version=pnpm_version,
            repository=repository,
            repository_directory=repository_directory,
            scoped_packages_options=scoped_packages_options,
            scripts=scripts,
            stability=stability,
            jsii_release_version=jsii_release_version,
            major_version=major_version,
            min_major_version=min_major_version,
            npm_dist_tag=npm_dist_tag,
            post_build_steps=post_build_steps,
            prerelease=prerelease,
            publish_dry_run=publish_dry_run,
            publish_tasks=publish_tasks,
            releasable_commits=releasable_commits,
            release_branches=release_branches,
            release_every_commit=release_every_commit,
            release_failure_issue=release_failure_issue,
            release_failure_issue_label=release_failure_issue_label,
            release_schedule=release_schedule,
            release_tag_prefix=release_tag_prefix,
            release_trigger=release_trigger,
            release_workflow_name=release_workflow_name,
            release_workflow_setup_steps=release_workflow_setup_steps,
            versionrc_options=versionrc_options,
            workflow_container_image=workflow_container_image,
            workflow_runs_on=workflow_runs_on,
            workflow_runs_on_group=workflow_runs_on_group,
            name=name,
            commit_generated=commit_generated,
            git_ignore_options=git_ignore_options,
            git_options=git_options,
            logging=logging,
            outdir=outdir,
            parent=parent,
            projen_command=projen_command,
            projenrc_json=projenrc_json,
            projenrc_json_options=projenrc_json_options,
            renovatebot=renovatebot,
            renovatebot_options=renovatebot_options,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="addBins")
    def add_bins(self, bins: typing.Mapping[builtins.str, builtins.str]) -> None:
        '''
        :param bins: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd0850dc1bf763fca52fa1a885d8979a0b159e53cb34c36ec7df070d31707319)
            check_type(argname="argument bins", value=bins, expected_type=type_hints["bins"])
        return typing.cast(None, jsii.invoke(self, "addBins", [bins]))

    @jsii.member(jsii_name="addBundledDeps")
    def add_bundled_deps(self, *deps: builtins.str) -> None:
        '''(experimental) Defines bundled dependencies.

        Bundled dependencies will be added as normal dependencies as well as to the
        ``bundledDependencies`` section of your ``package.json``.

        :param deps: Names modules to install. By default, the the dependency will be installed in the next ``npx projen`` run and the version will be recorded in your ``package.json`` file. You can upgrade manually or using ``yarn add/upgrade``. If you wish to specify a version range use this syntax: ``module@^7``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b1ff4594cefe0f3ab31e92f5ac8583fbe3df4f5ba62df16850e03b36a3c4161)
            check_type(argname="argument deps", value=deps, expected_type=typing.Tuple[type_hints["deps"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addBundledDeps", [*deps]))

    @jsii.member(jsii_name="addCompileCommand")
    def add_compile_command(self, *commands: builtins.str) -> None:
        '''(deprecated) DEPRECATED.

        :param commands: -

        :deprecated: use ``project.compileTask.exec()``

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b059cfc104068a0054d877fddb1a1af37e0a7e039d5c911c34d1119017de502e)
            check_type(argname="argument commands", value=commands, expected_type=typing.Tuple[type_hints["commands"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addCompileCommand", [*commands]))

    @jsii.member(jsii_name="addDeps")
    def add_deps(self, *deps: builtins.str) -> None:
        '''(experimental) Defines normal dependencies.

        :param deps: Names modules to install. By default, the the dependency will be installed in the next ``npx projen`` run and the version will be recorded in your ``package.json`` file. You can upgrade manually or using ``yarn add/upgrade``. If you wish to specify a version range use this syntax: ``module@^7``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b576514c0c963fa1e2e9fd3f1e8c1815cf1421fec5e99d2ac2eef18555fb9f9)
            check_type(argname="argument deps", value=deps, expected_type=typing.Tuple[type_hints["deps"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addDeps", [*deps]))

    @jsii.member(jsii_name="addDevDeps")
    def add_dev_deps(self, *deps: builtins.str) -> None:
        '''(experimental) Defines development/test dependencies.

        :param deps: Names modules to install. By default, the the dependency will be installed in the next ``npx projen`` run and the version will be recorded in your ``package.json`` file. You can upgrade manually or using ``yarn add/upgrade``. If you wish to specify a version range use this syntax: ``module@^7``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c2f5af66b63e317689cb319c22794a60ef4c8c60f02bab83df451259bfd266)
            check_type(argname="argument deps", value=deps, expected_type=typing.Tuple[type_hints["deps"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addDevDeps", [*deps]))

    @jsii.member(jsii_name="addFields")
    def add_fields(self, fields: typing.Mapping[builtins.str, typing.Any]) -> None:
        '''(experimental) Directly set fields in ``package.json``.

        :param fields: The fields to set.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aefed21bd0a280406323e1e4bb1ad79ba060becec09ea745a15f9de0ff27c701)
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
        return typing.cast(None, jsii.invoke(self, "addFields", [fields]))

    @jsii.member(jsii_name="addKeywords")
    def add_keywords(self, *keywords: builtins.str) -> None:
        '''(experimental) Adds keywords to package.json (deduplicated).

        :param keywords: The keywords to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bae4903fb76e287886deb4a0fc6eda837b193a8386de55770a9b5ff3203549b2)
            check_type(argname="argument keywords", value=keywords, expected_type=typing.Tuple[type_hints["keywords"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addKeywords", [*keywords]))

    @jsii.member(jsii_name="addPackageIgnore")
    def add_package_ignore(self, pattern: builtins.str) -> None:
        '''(experimental) Exclude these files from the bundled package.

        Implemented by project types based on the
        packaging mechanism. For example, ``NodeProject`` delegates this to ``.npmignore``.

        :param pattern: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75374e653c3f5969c1d17e74843bf9de7c8b57c83155a5d8f2054617e584c587)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(None, jsii.invoke(self, "addPackageIgnore", [pattern]))

    @jsii.member(jsii_name="addPeerDeps")
    def add_peer_deps(self, *deps: builtins.str) -> None:
        '''(experimental) Defines peer dependencies.

        When adding peer dependencies, a devDependency will also be added on the
        pinned version of the declared peer. This will ensure that you are testing
        your code against the minimum version required from your consumers.

        :param deps: Names modules to install. By default, the the dependency will be installed in the next ``npx projen`` run and the version will be recorded in your ``package.json`` file. You can upgrade manually or using ``yarn add/upgrade``. If you wish to specify a version range use this syntax: ``module@^7``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed50dcce11d164846dc05e1944054760e40bc33bcad4ed78ac8fc35bee9ca41b)
            check_type(argname="argument deps", value=deps, expected_type=typing.Tuple[type_hints["deps"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addPeerDeps", [*deps]))

    @jsii.member(jsii_name="addScripts")
    def add_scripts(self, scripts: typing.Mapping[builtins.str, builtins.str]) -> None:
        '''(experimental) Replaces the contents of multiple npm package.json scripts.

        :param scripts: The scripts to set.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67b7bc6c222da42e565aff91a82f7ebf8f7da5dfb913473bab13597487a1322)
            check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
        return typing.cast(None, jsii.invoke(self, "addScripts", [scripts]))

    @jsii.member(jsii_name="addTestCommand")
    def add_test_command(self, *commands: builtins.str) -> None:
        '''(deprecated) DEPRECATED.

        :param commands: -

        :deprecated: use ``project.testTask.exec()``

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__260e615a7142e436fcdeda572a6911528eb33c495f725efeb25c208eed3d88a0)
            check_type(argname="argument commands", value=commands, expected_type=typing.Tuple[type_hints["commands"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addTestCommand", [*commands]))

    @jsii.member(jsii_name="hasScript")
    def has_script(self, name: builtins.str) -> builtins.bool:
        '''(deprecated) Indicates if a script by the name name is defined.

        :param name: The name of the script.

        :deprecated: Use ``project.tasks.tryFind(name)``

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a96d563d99caecd8428704d41d3b4f2d83e16d8cf2c5b251709f03f0482f5d8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(builtins.bool, jsii.invoke(self, "hasScript", [name]))

    @jsii.member(jsii_name="removeScript")
    def remove_script(self, name: builtins.str) -> None:
        '''(experimental) Removes the npm script (always successful).

        :param name: The name of the script.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__224de74cc912dc2ec9fe8eebc20f7a52b63c2e04ee88bb72ef9f775a2d8b33ab)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(None, jsii.invoke(self, "removeScript", [name]))

    @jsii.member(jsii_name="renderWorkflowSetup")
    def render_workflow_setup(
        self,
        *,
        mutable: typing.Optional[builtins.bool] = None,
    ) -> typing.List[_JobStep_c3287c05]:
        '''(experimental) Returns the set of workflow steps which should be executed to bootstrap a workflow.

        :param mutable: (experimental) Should the pacakge lockfile be updated? Default: false

        :return: Job steps

        :stability: experimental
        '''
        options = RenderWorkflowSetupOptions(mutable=mutable)

        return typing.cast(typing.List[_JobStep_c3287c05], jsii.invoke(self, "renderWorkflowSetup", [options]))

    @jsii.member(jsii_name="runTaskCommand")
    def run_task_command(self, task: _Task_9fa875b6) -> builtins.str:
        '''(experimental) Returns the shell command to execute in order to run a task.

        This will
        typically be ``npx projen TASK``.

        :param task: The task for which the command is required.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0dba0b4edb6058c71da788f75e31bbfa6a73ef88319ba1c5fbe6f3606470049)
            check_type(argname="argument task", value=task, expected_type=type_hints["task"])
        return typing.cast(builtins.str, jsii.invoke(self, "runTaskCommand", [task]))

    @jsii.member(jsii_name="setScript")
    def set_script(self, name: builtins.str, command: builtins.str) -> None:
        '''(experimental) Replaces the contents of an npm package.json script.

        :param name: The script name.
        :param command: The command to execute.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a4eb807c608f50b2ade2ec2fbbb9f5443b474a504acfa34e6cf39edb04ad208)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
        return typing.cast(None, jsii.invoke(self, "setScript", [name, command]))

    @builtins.property
    @jsii.member(jsii_name="allowLibraryDependencies")
    def allow_library_dependencies(self) -> builtins.bool:
        '''
        :deprecated: use ``package.allowLibraryDependencies``

        :stability: deprecated
        '''
        return typing.cast(builtins.bool, jsii.get(self, "allowLibraryDependencies"))

    @builtins.property
    @jsii.member(jsii_name="artifactsDirectory")
    def artifacts_directory(self) -> builtins.str:
        '''(experimental) The build output directory.

        An npm tarball will be created under the ``js``
        subdirectory. For example, if this is set to ``dist`` (the default), the npm
        tarball will be placed under ``dist/js/boom-boom-1.2.3.tg``.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "artifactsDirectory"))

    @builtins.property
    @jsii.member(jsii_name="artifactsJavascriptDirectory")
    def artifacts_javascript_directory(self) -> builtins.str:
        '''(experimental) The location of the npm tarball after build (``${artifactsDirectory}/js``).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "artifactsJavascriptDirectory"))

    @builtins.property
    @jsii.member(jsii_name="bundler")
    def bundler(self) -> Bundler:
        '''
        :stability: experimental
        '''
        return typing.cast(Bundler, jsii.get(self, "bundler"))

    @builtins.property
    @jsii.member(jsii_name="entrypoint")
    def entrypoint(self) -> builtins.str:
        '''
        :deprecated: use ``package.entrypoint``

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "entrypoint"))

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> typing.Any:
        '''
        :deprecated: use ``package.addField(x, y)``

        :stability: deprecated
        '''
        return typing.cast(typing.Any, jsii.get(self, "manifest"))

    @builtins.property
    @jsii.member(jsii_name="npmrc")
    def npmrc(self) -> "NpmConfig":
        '''(experimental) The .npmrc file.

        :stability: experimental
        '''
        return typing.cast("NpmConfig", jsii.get(self, "npmrc"))

    @builtins.property
    @jsii.member(jsii_name="package")
    def package(self) -> NodePackage:
        '''(experimental) API for managing the node package.

        :stability: experimental
        '''
        return typing.cast(NodePackage, jsii.get(self, "package"))

    @builtins.property
    @jsii.member(jsii_name="packageManager")
    def package_manager(self) -> NodePackageManager:
        '''(deprecated) The package manager to use.

        :deprecated: use ``package.packageManager``

        :stability: deprecated
        '''
        return typing.cast(NodePackageManager, jsii.get(self, "packageManager"))

    @builtins.property
    @jsii.member(jsii_name="runScriptCommand")
    def run_script_command(self) -> builtins.str:
        '''(experimental) The command to use to run scripts (e.g. ``yarn run`` or ``npm run`` depends on the package manager).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "runScriptCommand"))

    @builtins.property
    @jsii.member(jsii_name="workflowBootstrapSteps")
    def _workflow_bootstrap_steps(self) -> typing.List[_JobStep_c3287c05]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[_JobStep_c3287c05], jsii.get(self, "workflowBootstrapSteps"))

    @builtins.property
    @jsii.member(jsii_name="workflowPackageCache")
    def _workflow_package_cache(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "workflowPackageCache"))

    @builtins.property
    @jsii.member(jsii_name="autoMerge")
    def auto_merge(self) -> typing.Optional[_AutoMerge_f73f9be0]:
        '''(experimental) Component that sets up mergify for merging approved pull requests.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_AutoMerge_f73f9be0], jsii.get(self, "autoMerge"))

    @builtins.property
    @jsii.member(jsii_name="buildWorkflow")
    def build_workflow(self) -> typing.Optional[_BuildWorkflow_bdd5e6cc]:
        '''(experimental) The PR build GitHub workflow.

        ``undefined`` if ``buildWorkflow`` is disabled.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_BuildWorkflow_bdd5e6cc], jsii.get(self, "buildWorkflow"))

    @builtins.property
    @jsii.member(jsii_name="buildWorkflowJobId")
    def build_workflow_job_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The job ID of the build workflow.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildWorkflowJobId"))

    @builtins.property
    @jsii.member(jsii_name="jest")
    def jest(self) -> typing.Optional[Jest]:
        '''(experimental) The Jest configuration (if enabled).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[Jest], jsii.get(self, "jest"))

    @builtins.property
    @jsii.member(jsii_name="maxNodeVersion")
    def max_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Maximum node version required by this package.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxNodeVersion"))

    @builtins.property
    @jsii.member(jsii_name="minNodeVersion")
    def min_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum node.js version required by this package.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minNodeVersion"))

    @builtins.property
    @jsii.member(jsii_name="nodeVersion")
    def _node_version(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeVersion"))

    @builtins.property
    @jsii.member(jsii_name="npmignore")
    def npmignore(self) -> typing.Optional[_IgnoreFile_3df2076a]:
        '''(experimental) The .npmignore file.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IgnoreFile_3df2076a], jsii.get(self, "npmignore"))

    @builtins.property
    @jsii.member(jsii_name="prettier")
    def prettier(self) -> typing.Optional["Prettier"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["Prettier"], jsii.get(self, "prettier"))

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> typing.Optional[_Publisher_4a29b2cd]:
        '''(deprecated) Package publisher.

        This will be ``undefined`` if the project does not have a
        release workflow.

        :deprecated: use ``release.publisher``.

        :stability: deprecated
        '''
        return typing.cast(typing.Optional[_Publisher_4a29b2cd], jsii.get(self, "publisher"))

    @builtins.property
    @jsii.member(jsii_name="release")
    def release(self) -> typing.Optional[_Release_30ee2d91]:
        '''(experimental) Release management.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_Release_30ee2d91], jsii.get(self, "release"))

    @builtins.property
    @jsii.member(jsii_name="upgradeWorkflow")
    def upgrade_workflow(self) -> typing.Optional["UpgradeDependencies"]:
        '''(experimental) The upgrade workflow.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["UpgradeDependencies"], jsii.get(self, "upgradeWorkflow"))


@jsii.data_type(
    jsii_type="projen.javascript.NodeProjectOptions",
    jsii_struct_bases=[
        _GitHubProjectOptions_547f2d08,
        NodePackageOptions,
        _ReleaseProjectOptions_929803c8,
    ],
    name_mapping={
        "name": "name",
        "commit_generated": "commitGenerated",
        "git_ignore_options": "gitIgnoreOptions",
        "git_options": "gitOptions",
        "logging": "logging",
        "outdir": "outdir",
        "parent": "parent",
        "projen_command": "projenCommand",
        "projenrc_json": "projenrcJson",
        "projenrc_json_options": "projenrcJsonOptions",
        "renovatebot": "renovatebot",
        "renovatebot_options": "renovatebotOptions",
        "auto_approve_options": "autoApproveOptions",
        "auto_merge": "autoMerge",
        "auto_merge_options": "autoMergeOptions",
        "clobber": "clobber",
        "dev_container": "devContainer",
        "github": "github",
        "github_options": "githubOptions",
        "gitpod": "gitpod",
        "mergify": "mergify",
        "mergify_options": "mergifyOptions",
        "project_type": "projectType",
        "projen_credentials": "projenCredentials",
        "projen_token_secret": "projenTokenSecret",
        "readme": "readme",
        "stale": "stale",
        "stale_options": "staleOptions",
        "vscode": "vscode",
        "allow_library_dependencies": "allowLibraryDependencies",
        "author_email": "authorEmail",
        "author_name": "authorName",
        "author_organization": "authorOrganization",
        "author_url": "authorUrl",
        "auto_detect_bin": "autoDetectBin",
        "bin": "bin",
        "bugs_email": "bugsEmail",
        "bugs_url": "bugsUrl",
        "bundled_deps": "bundledDeps",
        "code_artifact_options": "codeArtifactOptions",
        "deps": "deps",
        "description": "description",
        "dev_deps": "devDeps",
        "entrypoint": "entrypoint",
        "homepage": "homepage",
        "keywords": "keywords",
        "license": "license",
        "licensed": "licensed",
        "max_node_version": "maxNodeVersion",
        "min_node_version": "minNodeVersion",
        "npm_access": "npmAccess",
        "npm_registry": "npmRegistry",
        "npm_registry_url": "npmRegistryUrl",
        "npm_token_secret": "npmTokenSecret",
        "package_manager": "packageManager",
        "package_name": "packageName",
        "peer_dependency_options": "peerDependencyOptions",
        "peer_deps": "peerDeps",
        "pnpm_version": "pnpmVersion",
        "repository": "repository",
        "repository_directory": "repositoryDirectory",
        "scoped_packages_options": "scopedPackagesOptions",
        "scripts": "scripts",
        "stability": "stability",
        "jsii_release_version": "jsiiReleaseVersion",
        "major_version": "majorVersion",
        "min_major_version": "minMajorVersion",
        "npm_dist_tag": "npmDistTag",
        "post_build_steps": "postBuildSteps",
        "prerelease": "prerelease",
        "publish_dry_run": "publishDryRun",
        "publish_tasks": "publishTasks",
        "releasable_commits": "releasableCommits",
        "release_branches": "releaseBranches",
        "release_every_commit": "releaseEveryCommit",
        "release_failure_issue": "releaseFailureIssue",
        "release_failure_issue_label": "releaseFailureIssueLabel",
        "release_schedule": "releaseSchedule",
        "release_tag_prefix": "releaseTagPrefix",
        "release_trigger": "releaseTrigger",
        "release_workflow_name": "releaseWorkflowName",
        "release_workflow_setup_steps": "releaseWorkflowSetupSteps",
        "versionrc_options": "versionrcOptions",
        "workflow_container_image": "workflowContainerImage",
        "workflow_runs_on": "workflowRunsOn",
        "workflow_runs_on_group": "workflowRunsOnGroup",
        "default_release_branch": "defaultReleaseBranch",
        "artifacts_directory": "artifactsDirectory",
        "auto_approve_upgrades": "autoApproveUpgrades",
        "build_workflow": "buildWorkflow",
        "build_workflow_triggers": "buildWorkflowTriggers",
        "bundler_options": "bundlerOptions",
        "code_cov": "codeCov",
        "code_cov_token_secret": "codeCovTokenSecret",
        "copyright_owner": "copyrightOwner",
        "copyright_period": "copyrightPeriod",
        "dependabot": "dependabot",
        "dependabot_options": "dependabotOptions",
        "deps_upgrade": "depsUpgrade",
        "deps_upgrade_options": "depsUpgradeOptions",
        "gitignore": "gitignore",
        "jest": "jest",
        "jest_options": "jestOptions",
        "mutable_build": "mutableBuild",
        "npmignore": "npmignore",
        "npmignore_enabled": "npmignoreEnabled",
        "npm_ignore_options": "npmIgnoreOptions",
        "package": "package",
        "prettier": "prettier",
        "prettier_options": "prettierOptions",
        "projen_dev_dependency": "projenDevDependency",
        "projenrc_js": "projenrcJs",
        "projenrc_js_options": "projenrcJsOptions",
        "projen_version": "projenVersion",
        "pull_request_template": "pullRequestTemplate",
        "pull_request_template_contents": "pullRequestTemplateContents",
        "release": "release",
        "release_to_npm": "releaseToNpm",
        "release_workflow": "releaseWorkflow",
        "workflow_bootstrap_steps": "workflowBootstrapSteps",
        "workflow_git_identity": "workflowGitIdentity",
        "workflow_node_version": "workflowNodeVersion",
        "workflow_package_cache": "workflowPackageCache",
    },
)
class NodeProjectOptions(
    _GitHubProjectOptions_547f2d08,
    NodePackageOptions,
    _ReleaseProjectOptions_929803c8,
):
    def __init__(
        self,
        *,
        name: builtins.str,
        commit_generated: typing.Optional[builtins.bool] = None,
        git_ignore_options: typing.Optional[typing.Union[_IgnoreFileOptions_86c48b91, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_GitOptions_a65916a3, typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union[_LoggerOptions_eb0f6309, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        parent: typing.Optional[_Project_57d89203] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union[_ProjenrcJsonOptions_9c40dd4f, typing.Dict[builtins.str, typing.Any]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union[_RenovatebotOptions_18e6b8a1, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_approve_options: typing.Optional[typing.Union[_AutoApproveOptions_dac86cbe, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_merge: typing.Optional[builtins.bool] = None,
        auto_merge_options: typing.Optional[typing.Union[_AutoMergeOptions_d112cd3c, typing.Dict[builtins.str, typing.Any]]] = None,
        clobber: typing.Optional[builtins.bool] = None,
        dev_container: typing.Optional[builtins.bool] = None,
        github: typing.Optional[builtins.bool] = None,
        github_options: typing.Optional[typing.Union[_GitHubOptions_21553699, typing.Dict[builtins.str, typing.Any]]] = None,
        gitpod: typing.Optional[builtins.bool] = None,
        mergify: typing.Optional[builtins.bool] = None,
        mergify_options: typing.Optional[typing.Union[_MergifyOptions_a6faaab3, typing.Dict[builtins.str, typing.Any]]] = None,
        project_type: typing.Optional[_ProjectType_fd80c725] = None,
        projen_credentials: typing.Optional[_GithubCredentials_ae257072] = None,
        projen_token_secret: typing.Optional[builtins.str] = None,
        readme: typing.Optional[typing.Union[_SampleReadmeProps_3518b03b, typing.Dict[builtins.str, typing.Any]]] = None,
        stale: typing.Optional[builtins.bool] = None,
        stale_options: typing.Optional[typing.Union[_StaleOptions_929db764, typing.Dict[builtins.str, typing.Any]]] = None,
        vscode: typing.Optional[builtins.bool] = None,
        allow_library_dependencies: typing.Optional[builtins.bool] = None,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        author_organization: typing.Optional[builtins.bool] = None,
        author_url: typing.Optional[builtins.str] = None,
        auto_detect_bin: typing.Optional[builtins.bool] = None,
        bin: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bugs_email: typing.Optional[builtins.str] = None,
        bugs_url: typing.Optional[builtins.str] = None,
        bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        code_artifact_options: typing.Optional[typing.Union[CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        entrypoint: typing.Optional[builtins.str] = None,
        homepage: typing.Optional[builtins.str] = None,
        keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
        license: typing.Optional[builtins.str] = None,
        licensed: typing.Optional[builtins.bool] = None,
        max_node_version: typing.Optional[builtins.str] = None,
        min_node_version: typing.Optional[builtins.str] = None,
        npm_access: typing.Optional["NpmAccess"] = None,
        npm_registry: typing.Optional[builtins.str] = None,
        npm_registry_url: typing.Optional[builtins.str] = None,
        npm_token_secret: typing.Optional[builtins.str] = None,
        package_manager: typing.Optional[NodePackageManager] = None,
        package_name: typing.Optional[builtins.str] = None,
        peer_dependency_options: typing.Optional[typing.Union["PeerDependencyOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        peer_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        pnpm_version: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        repository_directory: typing.Optional[builtins.str] = None,
        scoped_packages_options: typing.Optional[typing.Sequence[typing.Union["ScopedPackagesOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
        scripts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        stability: typing.Optional[builtins.str] = None,
        jsii_release_version: typing.Optional[builtins.str] = None,
        major_version: typing.Optional[jsii.Number] = None,
        min_major_version: typing.Optional[jsii.Number] = None,
        npm_dist_tag: typing.Optional[builtins.str] = None,
        post_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        prerelease: typing.Optional[builtins.str] = None,
        publish_dry_run: typing.Optional[builtins.bool] = None,
        publish_tasks: typing.Optional[builtins.bool] = None,
        releasable_commits: typing.Optional[_ReleasableCommits_d481ce10] = None,
        release_branches: typing.Optional[typing.Mapping[builtins.str, typing.Union[_BranchOptions_13663d08, typing.Dict[builtins.str, typing.Any]]]] = None,
        release_every_commit: typing.Optional[builtins.bool] = None,
        release_failure_issue: typing.Optional[builtins.bool] = None,
        release_failure_issue_label: typing.Optional[builtins.str] = None,
        release_schedule: typing.Optional[builtins.str] = None,
        release_tag_prefix: typing.Optional[builtins.str] = None,
        release_trigger: typing.Optional[_ReleaseTrigger_e4dc221f] = None,
        release_workflow_name: typing.Optional[builtins.str] = None,
        release_workflow_setup_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workflow_container_image: typing.Optional[builtins.str] = None,
        workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        workflow_runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
        default_release_branch: builtins.str,
        artifacts_directory: typing.Optional[builtins.str] = None,
        auto_approve_upgrades: typing.Optional[builtins.bool] = None,
        build_workflow: typing.Optional[builtins.bool] = None,
        build_workflow_triggers: typing.Optional[typing.Union[_Triggers_e9ae7617, typing.Dict[builtins.str, typing.Any]]] = None,
        bundler_options: typing.Optional[typing.Union[BundlerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        code_cov: typing.Optional[builtins.bool] = None,
        code_cov_token_secret: typing.Optional[builtins.str] = None,
        copyright_owner: typing.Optional[builtins.str] = None,
        copyright_period: typing.Optional[builtins.str] = None,
        dependabot: typing.Optional[builtins.bool] = None,
        dependabot_options: typing.Optional[typing.Union[_DependabotOptions_0cedc635, typing.Dict[builtins.str, typing.Any]]] = None,
        deps_upgrade: typing.Optional[builtins.bool] = None,
        deps_upgrade_options: typing.Optional[typing.Union["UpgradeDependenciesOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        gitignore: typing.Optional[typing.Sequence[builtins.str]] = None,
        jest: typing.Optional[builtins.bool] = None,
        jest_options: typing.Optional[typing.Union[JestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        mutable_build: typing.Optional[builtins.bool] = None,
        npmignore: typing.Optional[typing.Sequence[builtins.str]] = None,
        npmignore_enabled: typing.Optional[builtins.bool] = None,
        npm_ignore_options: typing.Optional[typing.Union[_IgnoreFileOptions_86c48b91, typing.Dict[builtins.str, typing.Any]]] = None,
        package: typing.Optional[builtins.bool] = None,
        prettier: typing.Optional[builtins.bool] = None,
        prettier_options: typing.Optional[typing.Union["PrettierOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        projen_dev_dependency: typing.Optional[builtins.bool] = None,
        projenrc_js: typing.Optional[builtins.bool] = None,
        projenrc_js_options: typing.Optional[typing.Union["ProjenrcOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        projen_version: typing.Optional[builtins.str] = None,
        pull_request_template: typing.Optional[builtins.bool] = None,
        pull_request_template_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
        release: typing.Optional[builtins.bool] = None,
        release_to_npm: typing.Optional[builtins.bool] = None,
        release_workflow: typing.Optional[builtins.bool] = None,
        workflow_bootstrap_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        workflow_git_identity: typing.Optional[typing.Union[_GitIdentity_6effc3de, typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_node_version: typing.Optional[builtins.str] = None,
        workflow_package_cache: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param name: (experimental) This is the name of your project. Default: $BASEDIR
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other sub-projects. Default: "."
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options
        :param auto_approve_options: (experimental) Enable and configure the 'auto approve' workflow. Default: - auto approve is disabled
        :param auto_merge: (experimental) Enable automatic merging on GitHub. Has no effect if ``github.mergify`` is set to false. Default: true
        :param auto_merge_options: (experimental) Configure options for automatic merging on GitHub. Has no effect if ``github.mergify`` or ``autoMerge`` is set to false. Default: - see defaults in ``AutoMergeOptions``
        :param clobber: (experimental) Add a ``clobber`` task which resets the repo to origin. Default: - true, but false for subprojects
        :param dev_container: (experimental) Add a VSCode development environment (used for GitHub Codespaces). Default: false
        :param github: (experimental) Enable GitHub integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param github_options: (experimental) Options for GitHub integration. Default: - see GitHubOptions
        :param gitpod: (experimental) Add a Gitpod development environment. Default: false
        :param mergify: (deprecated) Whether mergify should be enabled on this repository or not. Default: true
        :param mergify_options: (deprecated) Options for mergify. Default: - default options
        :param project_type: (deprecated) Which type of project this is (library/app). Default: ProjectType.UNKNOWN
        :param projen_credentials: (experimental) Choose a method of providing GitHub API access for projen workflows. Default: - use a personal access token named PROJEN_GITHUB_TOKEN
        :param projen_token_secret: (deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows. This token needs to have the ``repo``, ``workflows`` and ``packages`` scope. Default: "PROJEN_GITHUB_TOKEN"
        :param readme: (experimental) The README setup. Default: - { filename: 'README.md', contents: '# replace this' }
        :param stale: (experimental) Auto-close of stale issues and pull request. See ``staleOptions`` for options. Default: false
        :param stale_options: (experimental) Auto-close stale issues and pull requests. To disable set ``stale`` to ``false``. Default: - see defaults in ``StaleOptions``
        :param vscode: (experimental) Enable VSCode integration. Enabled by default for root projects. Disabled for non-root projects. Default: true
        :param allow_library_dependencies: (experimental) Allow the project to include ``peerDependencies`` and ``bundledDependencies``. This is normally only allowed for libraries. For apps, there's no meaning for specifying these. Default: true
        :param author_email: (experimental) Author's e-mail.
        :param author_name: (experimental) Author's name.
        :param author_organization: (experimental) Is the author an organization.
        :param author_url: (experimental) Author's URL / Website.
        :param auto_detect_bin: (experimental) Automatically add all executables under the ``bin`` directory to your ``package.json`` file under the ``bin`` section. Default: true
        :param bin: (experimental) Binary programs vended with your module. You can use this option to add/customize how binaries are represented in your ``package.json``, but unless ``autoDetectBin`` is ``false``, every executable file under ``bin`` will automatically be added to this section.
        :param bugs_email: (experimental) The email address to which issues should be reported.
        :param bugs_url: (experimental) The url to your project's issue tracker.
        :param bundled_deps: (experimental) List of dependencies to bundle into this module. These modules will be added both to the ``dependencies`` section and ``bundledDependencies`` section of your ``package.json``. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include.
        :param code_artifact_options: (experimental) Options for npm packages using AWS CodeArtifact. This is required if publishing packages to, or installing scoped packages from AWS CodeArtifact Default: - undefined
        :param deps: (experimental) Runtime dependencies of this module. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include. Default: []
        :param description: (experimental) The description is just a string that helps people understand the purpose of the package. It can be used when searching for packages in a package manager as well. See https://classic.yarnpkg.com/en/docs/package-json/#toc-description
        :param dev_deps: (experimental) Build dependencies for this module. These dependencies will only be available in your build environment but will not be fetched when this module is consumed. The recommendation is to only specify the module name here (e.g. ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the sense that it will add the module as a dependency to your ``package.json`` file with the latest version (``^``). You can specify semver requirements in the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and this will be what you ``package.json`` will eventually include. Default: []
        :param entrypoint: (experimental) Module entrypoint (``main`` in ``package.json``). Set to an empty string to not include ``main`` in your package.json Default: "lib/index.js"
        :param homepage: (experimental) Package's Homepage / Website.
        :param keywords: (experimental) Keywords to include in ``package.json``.
        :param license: (experimental) License's SPDX identifier. See https://github.com/projen/projen/tree/main/license-text for a list of supported licenses. Use the ``licensed`` option if you want to no license to be specified. Default: "Apache-2.0"
        :param licensed: (experimental) Indicates if a license should be added. Default: true
        :param max_node_version: (experimental) Minimum node.js version to require via ``engines`` (inclusive). Default: - no max
        :param min_node_version: (experimental) Minimum Node.js version to require via package.json ``engines`` (inclusive). Default: - no "engines" specified
        :param npm_access: (experimental) Access level of the npm package. Default: - for scoped packages (e.g. ``foo@bar``), the default is ``NpmAccess.RESTRICTED``, for non-scoped packages, the default is ``NpmAccess.PUBLIC``.
        :param npm_registry: (deprecated) The host name of the npm registry to publish to. Cannot be set together with ``npmRegistryUrl``.
        :param npm_registry_url: (experimental) The base URL of the npm package registry. Must be a URL (e.g. start with "https://" or "http://") Default: "https://registry.npmjs.org"
        :param npm_token_secret: (experimental) GitHub secret which contains the NPM token to use when publishing packages. Default: "NPM_TOKEN"
        :param package_manager: (experimental) The Node Package Manager used to execute scripts. Default: NodePackageManager.YARN
        :param package_name: (experimental) The "name" in package.json. Default: - defaults to project name
        :param peer_dependency_options: (experimental) Options for ``peerDeps``.
        :param peer_deps: (experimental) Peer dependencies for this module. Dependencies listed here are required to be installed (and satisfied) by the *consumer* of this library. Using peer dependencies allows you to ensure that only a single module of a certain library exists in the ``node_modules`` tree of your consumers. Note that prior to npm@7, peer dependencies are *not* automatically installed, which means that adding peer dependencies to a library will be a breaking change for your customers. Unless ``peerDependencyOptions.pinnedDevDependency`` is disabled (it is enabled by default), projen will automatically add a dev dependency with a pinned version for each peer dependency. This will ensure that you build & test your module against the lowest peer version required. Default: []
        :param pnpm_version: (experimental) The version of PNPM to use if using PNPM as a package manager. Default: "7"
        :param repository: (experimental) The repository is the location where the actual code for your package lives. See https://classic.yarnpkg.com/en/docs/package-json/#toc-repository
        :param repository_directory: (experimental) If the package.json for your package is not in the root directory (for example if it is part of a monorepo), you can specify the directory in which it lives.
        :param scoped_packages_options: (experimental) Options for privately hosted scoped packages. Default: - fetch all scoped packages from the public npm registry
        :param scripts: (deprecated) npm scripts to include. If a script has the same name as a standard script, the standard script will be overwritten. Also adds the script as a task. Default: {}
        :param stability: (experimental) Package's Stability.
        :param jsii_release_version: (experimental) Version requirement of ``publib`` which is used to publish modules to npm. Default: "latest"
        :param major_version: (experimental) Major version to release from the default branch. If this is specified, we bump the latest version of this major version line. If not specified, we bump the global latest version. Default: - Major version is not enforced.
        :param min_major_version: (experimental) Minimal Major version to release. This can be useful to set to 1, as breaking changes before the 1.x major release are not incrementing the major version number. Can not be set together with ``majorVersion``. Default: - No minimum version is being enforced
        :param npm_dist_tag: (experimental) The npmDistTag to use when publishing from the default branch. To set the npm dist-tag for release branches, set the ``npmDistTag`` property for each branch. Default: "latest"
        :param post_build_steps: (experimental) Steps to execute after build as part of the release workflow. Default: []
        :param prerelease: (experimental) Bump versions from the default branch as pre-releases (e.g. "beta", "alpha", "pre"). Default: - normal semantic versions
        :param publish_dry_run: (experimental) Instead of actually publishing to package managers, just print the publishing command. Default: false
        :param publish_tasks: (experimental) Define publishing tasks that can be executed manually as well as workflows. Normally, publishing only happens within automated workflows. Enable this in order to create a publishing task for each publishing activity. Default: false
        :param releasable_commits: (experimental) Find commits that should be considered releasable Used to decide if a release is required. Default: ReleasableCommits.everyCommit()
        :param release_branches: (experimental) Defines additional release branches. A workflow will be created for each release branch which will publish releases from commits in this branch. Each release branch *must* be assigned a major version number which is used to enforce that versions published from that branch always use that major version. If multiple branches are used, the ``majorVersion`` field must also be provided for the default branch. Default: - no additional branches are used for release. you can use ``addBranch()`` to add additional branches.
        :param release_every_commit: (deprecated) Automatically release new versions every commit to one of branches in ``releaseBranches``. Default: true
        :param release_failure_issue: (experimental) Create a github issue on every failed publishing task. Default: false
        :param release_failure_issue_label: (experimental) The label to apply to issues indicating publish failures. Only applies if ``releaseFailureIssue`` is true. Default: "failed-release"
        :param release_schedule: (deprecated) CRON schedule to trigger new releases. Default: - no scheduled releases
        :param release_tag_prefix: (experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers. Note: this prefix is used to detect the latest tagged version when bumping, so if you change this on a project with an existing version history, you may need to manually tag your latest release with the new prefix. Default: "v"
        :param release_trigger: (experimental) The release trigger to use. Default: - Continuous releases (``ReleaseTrigger.continuous()``)
        :param release_workflow_name: (experimental) The name of the default release workflow. Default: "Release"
        :param release_workflow_setup_steps: (experimental) A set of workflow steps to execute in order to setup the workflow container.
        :param versionrc_options: (experimental) Custom configuration used when creating changelog with standard-version package. Given values either append to default configuration or overwrite values in it. Default: - standard configuration applicable for GitHub repositories
        :param workflow_container_image: (experimental) Container image to use for GitHub workflows. Default: - default image
        :param workflow_runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param workflow_runs_on_group: (experimental) Github Runner Group selection options.
        :param default_release_branch: (experimental) The name of the main release branch. Default: "main"
        :param artifacts_directory: (experimental) A directory which will contain build artifacts. Default: "dist"
        :param auto_approve_upgrades: (experimental) Automatically approve deps upgrade PRs, allowing them to be merged by mergify (if configued). Throw if set to true but ``autoApproveOptions`` are not defined. Default: - true
        :param build_workflow: (experimental) Define a GitHub workflow for building PRs. Default: - true if not a subproject
        :param build_workflow_triggers: (experimental) Build workflow triggers. Default: "{ pullRequest: {}, workflowDispatch: {} }"
        :param bundler_options: (experimental) Options for ``Bundler``.
        :param code_cov: (experimental) Define a GitHub workflow step for sending code coverage metrics to https://codecov.io/ Uses codecov/codecov-action@v3 A secret is required for private repos. Configured with ``@codeCovTokenSecret``. Default: false
        :param code_cov_token_secret: (experimental) Define the secret name for a specified https://codecov.io/ token A secret is required to send coverage for private repositories. Default: - if this option is not specified, only public repositories are supported
        :param copyright_owner: (experimental) License copyright owner. Default: - defaults to the value of authorName or "" if ``authorName`` is undefined.
        :param copyright_period: (experimental) The copyright years to put in the LICENSE file. Default: - current year
        :param dependabot: (experimental) Use dependabot to handle dependency upgrades. Cannot be used in conjunction with ``depsUpgrade``. Default: false
        :param dependabot_options: (experimental) Options for dependabot. Default: - default options
        :param deps_upgrade: (experimental) Use tasks and github workflows to handle dependency upgrades. Cannot be used in conjunction with ``dependabot``. Default: true
        :param deps_upgrade_options: (experimental) Options for ``UpgradeDependencies``. Default: - default options
        :param gitignore: (experimental) Additional entries to .gitignore.
        :param jest: (experimental) Setup jest unit tests. Default: true
        :param jest_options: (experimental) Jest options. Default: - default options
        :param mutable_build: (experimental) Automatically update files modified during builds to pull-request branches. This means that any files synthesized by projen or e.g. test snapshots will always be up-to-date before a PR is merged. Implies that PR builds do not have anti-tamper checks. Default: true
        :param npmignore: (deprecated) Additional entries to .npmignore.
        :param npmignore_enabled: (experimental) Defines an .npmignore file. Normally this is only needed for libraries that are packaged as tarballs. Default: true
        :param npm_ignore_options: (experimental) Configuration options for .npmignore file.
        :param package: (experimental) Defines a ``package`` task that will produce an npm tarball under the artifacts directory (e.g. ``dist``). Default: true
        :param prettier: (experimental) Setup prettier. Default: false
        :param prettier_options: (experimental) Prettier options. Default: - default options
        :param projen_dev_dependency: (experimental) Indicates of "projen" should be installed as a devDependency. Default: true
        :param projenrc_js: (experimental) Generate (once) .projenrc.js (in JavaScript). Set to ``false`` in order to disable .projenrc.js generation. Default: - true if projenrcJson is false
        :param projenrc_js_options: (experimental) Options for .projenrc.js. Default: - default options
        :param projen_version: (experimental) Version of projen to install. Default: - Defaults to the latest version.
        :param pull_request_template: (experimental) Include a GitHub pull request template. Default: true
        :param pull_request_template_contents: (experimental) The contents of the pull request template. Default: - default content
        :param release: (experimental) Add release management to this project. Default: - true (false for subprojects)
        :param release_to_npm: (experimental) Automatically release to npm when new versions are introduced. Default: false
        :param release_workflow: (deprecated) DEPRECATED: renamed to ``release``. Default: - true if not a subproject
        :param workflow_bootstrap_steps: (experimental) Workflow steps to use in order to bootstrap this repo. Default: "yarn install --frozen-lockfile && yarn projen"
        :param workflow_git_identity: (experimental) The git identity to use in workflows. Default: - GitHub Actions
        :param workflow_node_version: (experimental) The node version to use in GitHub workflows. Default: - same as ``minNodeVersion``
        :param workflow_package_cache: (experimental) Enable Node.js package cache in GitHub workflows. Default: false

        :stability: experimental
        '''
        if isinstance(git_ignore_options, dict):
            git_ignore_options = _IgnoreFileOptions_86c48b91(**git_ignore_options)
        if isinstance(git_options, dict):
            git_options = _GitOptions_a65916a3(**git_options)
        if isinstance(logging, dict):
            logging = _LoggerOptions_eb0f6309(**logging)
        if isinstance(projenrc_json_options, dict):
            projenrc_json_options = _ProjenrcJsonOptions_9c40dd4f(**projenrc_json_options)
        if isinstance(renovatebot_options, dict):
            renovatebot_options = _RenovatebotOptions_18e6b8a1(**renovatebot_options)
        if isinstance(auto_approve_options, dict):
            auto_approve_options = _AutoApproveOptions_dac86cbe(**auto_approve_options)
        if isinstance(auto_merge_options, dict):
            auto_merge_options = _AutoMergeOptions_d112cd3c(**auto_merge_options)
        if isinstance(github_options, dict):
            github_options = _GitHubOptions_21553699(**github_options)
        if isinstance(mergify_options, dict):
            mergify_options = _MergifyOptions_a6faaab3(**mergify_options)
        if isinstance(readme, dict):
            readme = _SampleReadmeProps_3518b03b(**readme)
        if isinstance(stale_options, dict):
            stale_options = _StaleOptions_929db764(**stale_options)
        if isinstance(code_artifact_options, dict):
            code_artifact_options = CodeArtifactOptions(**code_artifact_options)
        if isinstance(peer_dependency_options, dict):
            peer_dependency_options = PeerDependencyOptions(**peer_dependency_options)
        if isinstance(workflow_runs_on_group, dict):
            workflow_runs_on_group = _GroupRunnerOptions_148c59c1(**workflow_runs_on_group)
        if isinstance(build_workflow_triggers, dict):
            build_workflow_triggers = _Triggers_e9ae7617(**build_workflow_triggers)
        if isinstance(bundler_options, dict):
            bundler_options = BundlerOptions(**bundler_options)
        if isinstance(dependabot_options, dict):
            dependabot_options = _DependabotOptions_0cedc635(**dependabot_options)
        if isinstance(deps_upgrade_options, dict):
            deps_upgrade_options = UpgradeDependenciesOptions(**deps_upgrade_options)
        if isinstance(jest_options, dict):
            jest_options = JestOptions(**jest_options)
        if isinstance(npm_ignore_options, dict):
            npm_ignore_options = _IgnoreFileOptions_86c48b91(**npm_ignore_options)
        if isinstance(prettier_options, dict):
            prettier_options = PrettierOptions(**prettier_options)
        if isinstance(projenrc_js_options, dict):
            projenrc_js_options = ProjenrcOptions(**projenrc_js_options)
        if isinstance(workflow_git_identity, dict):
            workflow_git_identity = _GitIdentity_6effc3de(**workflow_git_identity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c2eb8aa04095bbe6af788737363089516ccd341e3a6624f153e8ff7eeaee29)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument commit_generated", value=commit_generated, expected_type=type_hints["commit_generated"])
            check_type(argname="argument git_ignore_options", value=git_ignore_options, expected_type=type_hints["git_ignore_options"])
            check_type(argname="argument git_options", value=git_options, expected_type=type_hints["git_options"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument projen_command", value=projen_command, expected_type=type_hints["projen_command"])
            check_type(argname="argument projenrc_json", value=projenrc_json, expected_type=type_hints["projenrc_json"])
            check_type(argname="argument projenrc_json_options", value=projenrc_json_options, expected_type=type_hints["projenrc_json_options"])
            check_type(argname="argument renovatebot", value=renovatebot, expected_type=type_hints["renovatebot"])
            check_type(argname="argument renovatebot_options", value=renovatebot_options, expected_type=type_hints["renovatebot_options"])
            check_type(argname="argument auto_approve_options", value=auto_approve_options, expected_type=type_hints["auto_approve_options"])
            check_type(argname="argument auto_merge", value=auto_merge, expected_type=type_hints["auto_merge"])
            check_type(argname="argument auto_merge_options", value=auto_merge_options, expected_type=type_hints["auto_merge_options"])
            check_type(argname="argument clobber", value=clobber, expected_type=type_hints["clobber"])
            check_type(argname="argument dev_container", value=dev_container, expected_type=type_hints["dev_container"])
            check_type(argname="argument github", value=github, expected_type=type_hints["github"])
            check_type(argname="argument github_options", value=github_options, expected_type=type_hints["github_options"])
            check_type(argname="argument gitpod", value=gitpod, expected_type=type_hints["gitpod"])
            check_type(argname="argument mergify", value=mergify, expected_type=type_hints["mergify"])
            check_type(argname="argument mergify_options", value=mergify_options, expected_type=type_hints["mergify_options"])
            check_type(argname="argument project_type", value=project_type, expected_type=type_hints["project_type"])
            check_type(argname="argument projen_credentials", value=projen_credentials, expected_type=type_hints["projen_credentials"])
            check_type(argname="argument projen_token_secret", value=projen_token_secret, expected_type=type_hints["projen_token_secret"])
            check_type(argname="argument readme", value=readme, expected_type=type_hints["readme"])
            check_type(argname="argument stale", value=stale, expected_type=type_hints["stale"])
            check_type(argname="argument stale_options", value=stale_options, expected_type=type_hints["stale_options"])
            check_type(argname="argument vscode", value=vscode, expected_type=type_hints["vscode"])
            check_type(argname="argument allow_library_dependencies", value=allow_library_dependencies, expected_type=type_hints["allow_library_dependencies"])
            check_type(argname="argument author_email", value=author_email, expected_type=type_hints["author_email"])
            check_type(argname="argument author_name", value=author_name, expected_type=type_hints["author_name"])
            check_type(argname="argument author_organization", value=author_organization, expected_type=type_hints["author_organization"])
            check_type(argname="argument author_url", value=author_url, expected_type=type_hints["author_url"])
            check_type(argname="argument auto_detect_bin", value=auto_detect_bin, expected_type=type_hints["auto_detect_bin"])
            check_type(argname="argument bin", value=bin, expected_type=type_hints["bin"])
            check_type(argname="argument bugs_email", value=bugs_email, expected_type=type_hints["bugs_email"])
            check_type(argname="argument bugs_url", value=bugs_url, expected_type=type_hints["bugs_url"])
            check_type(argname="argument bundled_deps", value=bundled_deps, expected_type=type_hints["bundled_deps"])
            check_type(argname="argument code_artifact_options", value=code_artifact_options, expected_type=type_hints["code_artifact_options"])
            check_type(argname="argument deps", value=deps, expected_type=type_hints["deps"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dev_deps", value=dev_deps, expected_type=type_hints["dev_deps"])
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
            check_type(argname="argument homepage", value=homepage, expected_type=type_hints["homepage"])
            check_type(argname="argument keywords", value=keywords, expected_type=type_hints["keywords"])
            check_type(argname="argument license", value=license, expected_type=type_hints["license"])
            check_type(argname="argument licensed", value=licensed, expected_type=type_hints["licensed"])
            check_type(argname="argument max_node_version", value=max_node_version, expected_type=type_hints["max_node_version"])
            check_type(argname="argument min_node_version", value=min_node_version, expected_type=type_hints["min_node_version"])
            check_type(argname="argument npm_access", value=npm_access, expected_type=type_hints["npm_access"])
            check_type(argname="argument npm_registry", value=npm_registry, expected_type=type_hints["npm_registry"])
            check_type(argname="argument npm_registry_url", value=npm_registry_url, expected_type=type_hints["npm_registry_url"])
            check_type(argname="argument npm_token_secret", value=npm_token_secret, expected_type=type_hints["npm_token_secret"])
            check_type(argname="argument package_manager", value=package_manager, expected_type=type_hints["package_manager"])
            check_type(argname="argument package_name", value=package_name, expected_type=type_hints["package_name"])
            check_type(argname="argument peer_dependency_options", value=peer_dependency_options, expected_type=type_hints["peer_dependency_options"])
            check_type(argname="argument peer_deps", value=peer_deps, expected_type=type_hints["peer_deps"])
            check_type(argname="argument pnpm_version", value=pnpm_version, expected_type=type_hints["pnpm_version"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument repository_directory", value=repository_directory, expected_type=type_hints["repository_directory"])
            check_type(argname="argument scoped_packages_options", value=scoped_packages_options, expected_type=type_hints["scoped_packages_options"])
            check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
            check_type(argname="argument stability", value=stability, expected_type=type_hints["stability"])
            check_type(argname="argument jsii_release_version", value=jsii_release_version, expected_type=type_hints["jsii_release_version"])
            check_type(argname="argument major_version", value=major_version, expected_type=type_hints["major_version"])
            check_type(argname="argument min_major_version", value=min_major_version, expected_type=type_hints["min_major_version"])
            check_type(argname="argument npm_dist_tag", value=npm_dist_tag, expected_type=type_hints["npm_dist_tag"])
            check_type(argname="argument post_build_steps", value=post_build_steps, expected_type=type_hints["post_build_steps"])
            check_type(argname="argument prerelease", value=prerelease, expected_type=type_hints["prerelease"])
            check_type(argname="argument publish_dry_run", value=publish_dry_run, expected_type=type_hints["publish_dry_run"])
            check_type(argname="argument publish_tasks", value=publish_tasks, expected_type=type_hints["publish_tasks"])
            check_type(argname="argument releasable_commits", value=releasable_commits, expected_type=type_hints["releasable_commits"])
            check_type(argname="argument release_branches", value=release_branches, expected_type=type_hints["release_branches"])
            check_type(argname="argument release_every_commit", value=release_every_commit, expected_type=type_hints["release_every_commit"])
            check_type(argname="argument release_failure_issue", value=release_failure_issue, expected_type=type_hints["release_failure_issue"])
            check_type(argname="argument release_failure_issue_label", value=release_failure_issue_label, expected_type=type_hints["release_failure_issue_label"])
            check_type(argname="argument release_schedule", value=release_schedule, expected_type=type_hints["release_schedule"])
            check_type(argname="argument release_tag_prefix", value=release_tag_prefix, expected_type=type_hints["release_tag_prefix"])
            check_type(argname="argument release_trigger", value=release_trigger, expected_type=type_hints["release_trigger"])
            check_type(argname="argument release_workflow_name", value=release_workflow_name, expected_type=type_hints["release_workflow_name"])
            check_type(argname="argument release_workflow_setup_steps", value=release_workflow_setup_steps, expected_type=type_hints["release_workflow_setup_steps"])
            check_type(argname="argument versionrc_options", value=versionrc_options, expected_type=type_hints["versionrc_options"])
            check_type(argname="argument workflow_container_image", value=workflow_container_image, expected_type=type_hints["workflow_container_image"])
            check_type(argname="argument workflow_runs_on", value=workflow_runs_on, expected_type=type_hints["workflow_runs_on"])
            check_type(argname="argument workflow_runs_on_group", value=workflow_runs_on_group, expected_type=type_hints["workflow_runs_on_group"])
            check_type(argname="argument default_release_branch", value=default_release_branch, expected_type=type_hints["default_release_branch"])
            check_type(argname="argument artifacts_directory", value=artifacts_directory, expected_type=type_hints["artifacts_directory"])
            check_type(argname="argument auto_approve_upgrades", value=auto_approve_upgrades, expected_type=type_hints["auto_approve_upgrades"])
            check_type(argname="argument build_workflow", value=build_workflow, expected_type=type_hints["build_workflow"])
            check_type(argname="argument build_workflow_triggers", value=build_workflow_triggers, expected_type=type_hints["build_workflow_triggers"])
            check_type(argname="argument bundler_options", value=bundler_options, expected_type=type_hints["bundler_options"])
            check_type(argname="argument code_cov", value=code_cov, expected_type=type_hints["code_cov"])
            check_type(argname="argument code_cov_token_secret", value=code_cov_token_secret, expected_type=type_hints["code_cov_token_secret"])
            check_type(argname="argument copyright_owner", value=copyright_owner, expected_type=type_hints["copyright_owner"])
            check_type(argname="argument copyright_period", value=copyright_period, expected_type=type_hints["copyright_period"])
            check_type(argname="argument dependabot", value=dependabot, expected_type=type_hints["dependabot"])
            check_type(argname="argument dependabot_options", value=dependabot_options, expected_type=type_hints["dependabot_options"])
            check_type(argname="argument deps_upgrade", value=deps_upgrade, expected_type=type_hints["deps_upgrade"])
            check_type(argname="argument deps_upgrade_options", value=deps_upgrade_options, expected_type=type_hints["deps_upgrade_options"])
            check_type(argname="argument gitignore", value=gitignore, expected_type=type_hints["gitignore"])
            check_type(argname="argument jest", value=jest, expected_type=type_hints["jest"])
            check_type(argname="argument jest_options", value=jest_options, expected_type=type_hints["jest_options"])
            check_type(argname="argument mutable_build", value=mutable_build, expected_type=type_hints["mutable_build"])
            check_type(argname="argument npmignore", value=npmignore, expected_type=type_hints["npmignore"])
            check_type(argname="argument npmignore_enabled", value=npmignore_enabled, expected_type=type_hints["npmignore_enabled"])
            check_type(argname="argument npm_ignore_options", value=npm_ignore_options, expected_type=type_hints["npm_ignore_options"])
            check_type(argname="argument package", value=package, expected_type=type_hints["package"])
            check_type(argname="argument prettier", value=prettier, expected_type=type_hints["prettier"])
            check_type(argname="argument prettier_options", value=prettier_options, expected_type=type_hints["prettier_options"])
            check_type(argname="argument projen_dev_dependency", value=projen_dev_dependency, expected_type=type_hints["projen_dev_dependency"])
            check_type(argname="argument projenrc_js", value=projenrc_js, expected_type=type_hints["projenrc_js"])
            check_type(argname="argument projenrc_js_options", value=projenrc_js_options, expected_type=type_hints["projenrc_js_options"])
            check_type(argname="argument projen_version", value=projen_version, expected_type=type_hints["projen_version"])
            check_type(argname="argument pull_request_template", value=pull_request_template, expected_type=type_hints["pull_request_template"])
            check_type(argname="argument pull_request_template_contents", value=pull_request_template_contents, expected_type=type_hints["pull_request_template_contents"])
            check_type(argname="argument release", value=release, expected_type=type_hints["release"])
            check_type(argname="argument release_to_npm", value=release_to_npm, expected_type=type_hints["release_to_npm"])
            check_type(argname="argument release_workflow", value=release_workflow, expected_type=type_hints["release_workflow"])
            check_type(argname="argument workflow_bootstrap_steps", value=workflow_bootstrap_steps, expected_type=type_hints["workflow_bootstrap_steps"])
            check_type(argname="argument workflow_git_identity", value=workflow_git_identity, expected_type=type_hints["workflow_git_identity"])
            check_type(argname="argument workflow_node_version", value=workflow_node_version, expected_type=type_hints["workflow_node_version"])
            check_type(argname="argument workflow_package_cache", value=workflow_package_cache, expected_type=type_hints["workflow_package_cache"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "default_release_branch": default_release_branch,
        }
        if commit_generated is not None:
            self._values["commit_generated"] = commit_generated
        if git_ignore_options is not None:
            self._values["git_ignore_options"] = git_ignore_options
        if git_options is not None:
            self._values["git_options"] = git_options
        if logging is not None:
            self._values["logging"] = logging
        if outdir is not None:
            self._values["outdir"] = outdir
        if parent is not None:
            self._values["parent"] = parent
        if projen_command is not None:
            self._values["projen_command"] = projen_command
        if projenrc_json is not None:
            self._values["projenrc_json"] = projenrc_json
        if projenrc_json_options is not None:
            self._values["projenrc_json_options"] = projenrc_json_options
        if renovatebot is not None:
            self._values["renovatebot"] = renovatebot
        if renovatebot_options is not None:
            self._values["renovatebot_options"] = renovatebot_options
        if auto_approve_options is not None:
            self._values["auto_approve_options"] = auto_approve_options
        if auto_merge is not None:
            self._values["auto_merge"] = auto_merge
        if auto_merge_options is not None:
            self._values["auto_merge_options"] = auto_merge_options
        if clobber is not None:
            self._values["clobber"] = clobber
        if dev_container is not None:
            self._values["dev_container"] = dev_container
        if github is not None:
            self._values["github"] = github
        if github_options is not None:
            self._values["github_options"] = github_options
        if gitpod is not None:
            self._values["gitpod"] = gitpod
        if mergify is not None:
            self._values["mergify"] = mergify
        if mergify_options is not None:
            self._values["mergify_options"] = mergify_options
        if project_type is not None:
            self._values["project_type"] = project_type
        if projen_credentials is not None:
            self._values["projen_credentials"] = projen_credentials
        if projen_token_secret is not None:
            self._values["projen_token_secret"] = projen_token_secret
        if readme is not None:
            self._values["readme"] = readme
        if stale is not None:
            self._values["stale"] = stale
        if stale_options is not None:
            self._values["stale_options"] = stale_options
        if vscode is not None:
            self._values["vscode"] = vscode
        if allow_library_dependencies is not None:
            self._values["allow_library_dependencies"] = allow_library_dependencies
        if author_email is not None:
            self._values["author_email"] = author_email
        if author_name is not None:
            self._values["author_name"] = author_name
        if author_organization is not None:
            self._values["author_organization"] = author_organization
        if author_url is not None:
            self._values["author_url"] = author_url
        if auto_detect_bin is not None:
            self._values["auto_detect_bin"] = auto_detect_bin
        if bin is not None:
            self._values["bin"] = bin
        if bugs_email is not None:
            self._values["bugs_email"] = bugs_email
        if bugs_url is not None:
            self._values["bugs_url"] = bugs_url
        if bundled_deps is not None:
            self._values["bundled_deps"] = bundled_deps
        if code_artifact_options is not None:
            self._values["code_artifact_options"] = code_artifact_options
        if deps is not None:
            self._values["deps"] = deps
        if description is not None:
            self._values["description"] = description
        if dev_deps is not None:
            self._values["dev_deps"] = dev_deps
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint
        if homepage is not None:
            self._values["homepage"] = homepage
        if keywords is not None:
            self._values["keywords"] = keywords
        if license is not None:
            self._values["license"] = license
        if licensed is not None:
            self._values["licensed"] = licensed
        if max_node_version is not None:
            self._values["max_node_version"] = max_node_version
        if min_node_version is not None:
            self._values["min_node_version"] = min_node_version
        if npm_access is not None:
            self._values["npm_access"] = npm_access
        if npm_registry is not None:
            self._values["npm_registry"] = npm_registry
        if npm_registry_url is not None:
            self._values["npm_registry_url"] = npm_registry_url
        if npm_token_secret is not None:
            self._values["npm_token_secret"] = npm_token_secret
        if package_manager is not None:
            self._values["package_manager"] = package_manager
        if package_name is not None:
            self._values["package_name"] = package_name
        if peer_dependency_options is not None:
            self._values["peer_dependency_options"] = peer_dependency_options
        if peer_deps is not None:
            self._values["peer_deps"] = peer_deps
        if pnpm_version is not None:
            self._values["pnpm_version"] = pnpm_version
        if repository is not None:
            self._values["repository"] = repository
        if repository_directory is not None:
            self._values["repository_directory"] = repository_directory
        if scoped_packages_options is not None:
            self._values["scoped_packages_options"] = scoped_packages_options
        if scripts is not None:
            self._values["scripts"] = scripts
        if stability is not None:
            self._values["stability"] = stability
        if jsii_release_version is not None:
            self._values["jsii_release_version"] = jsii_release_version
        if major_version is not None:
            self._values["major_version"] = major_version
        if min_major_version is not None:
            self._values["min_major_version"] = min_major_version
        if npm_dist_tag is not None:
            self._values["npm_dist_tag"] = npm_dist_tag
        if post_build_steps is not None:
            self._values["post_build_steps"] = post_build_steps
        if prerelease is not None:
            self._values["prerelease"] = prerelease
        if publish_dry_run is not None:
            self._values["publish_dry_run"] = publish_dry_run
        if publish_tasks is not None:
            self._values["publish_tasks"] = publish_tasks
        if releasable_commits is not None:
            self._values["releasable_commits"] = releasable_commits
        if release_branches is not None:
            self._values["release_branches"] = release_branches
        if release_every_commit is not None:
            self._values["release_every_commit"] = release_every_commit
        if release_failure_issue is not None:
            self._values["release_failure_issue"] = release_failure_issue
        if release_failure_issue_label is not None:
            self._values["release_failure_issue_label"] = release_failure_issue_label
        if release_schedule is not None:
            self._values["release_schedule"] = release_schedule
        if release_tag_prefix is not None:
            self._values["release_tag_prefix"] = release_tag_prefix
        if release_trigger is not None:
            self._values["release_trigger"] = release_trigger
        if release_workflow_name is not None:
            self._values["release_workflow_name"] = release_workflow_name
        if release_workflow_setup_steps is not None:
            self._values["release_workflow_setup_steps"] = release_workflow_setup_steps
        if versionrc_options is not None:
            self._values["versionrc_options"] = versionrc_options
        if workflow_container_image is not None:
            self._values["workflow_container_image"] = workflow_container_image
        if workflow_runs_on is not None:
            self._values["workflow_runs_on"] = workflow_runs_on
        if workflow_runs_on_group is not None:
            self._values["workflow_runs_on_group"] = workflow_runs_on_group
        if artifacts_directory is not None:
            self._values["artifacts_directory"] = artifacts_directory
        if auto_approve_upgrades is not None:
            self._values["auto_approve_upgrades"] = auto_approve_upgrades
        if build_workflow is not None:
            self._values["build_workflow"] = build_workflow
        if build_workflow_triggers is not None:
            self._values["build_workflow_triggers"] = build_workflow_triggers
        if bundler_options is not None:
            self._values["bundler_options"] = bundler_options
        if code_cov is not None:
            self._values["code_cov"] = code_cov
        if code_cov_token_secret is not None:
            self._values["code_cov_token_secret"] = code_cov_token_secret
        if copyright_owner is not None:
            self._values["copyright_owner"] = copyright_owner
        if copyright_period is not None:
            self._values["copyright_period"] = copyright_period
        if dependabot is not None:
            self._values["dependabot"] = dependabot
        if dependabot_options is not None:
            self._values["dependabot_options"] = dependabot_options
        if deps_upgrade is not None:
            self._values["deps_upgrade"] = deps_upgrade
        if deps_upgrade_options is not None:
            self._values["deps_upgrade_options"] = deps_upgrade_options
        if gitignore is not None:
            self._values["gitignore"] = gitignore
        if jest is not None:
            self._values["jest"] = jest
        if jest_options is not None:
            self._values["jest_options"] = jest_options
        if mutable_build is not None:
            self._values["mutable_build"] = mutable_build
        if npmignore is not None:
            self._values["npmignore"] = npmignore
        if npmignore_enabled is not None:
            self._values["npmignore_enabled"] = npmignore_enabled
        if npm_ignore_options is not None:
            self._values["npm_ignore_options"] = npm_ignore_options
        if package is not None:
            self._values["package"] = package
        if prettier is not None:
            self._values["prettier"] = prettier
        if prettier_options is not None:
            self._values["prettier_options"] = prettier_options
        if projen_dev_dependency is not None:
            self._values["projen_dev_dependency"] = projen_dev_dependency
        if projenrc_js is not None:
            self._values["projenrc_js"] = projenrc_js
        if projenrc_js_options is not None:
            self._values["projenrc_js_options"] = projenrc_js_options
        if projen_version is not None:
            self._values["projen_version"] = projen_version
        if pull_request_template is not None:
            self._values["pull_request_template"] = pull_request_template
        if pull_request_template_contents is not None:
            self._values["pull_request_template_contents"] = pull_request_template_contents
        if release is not None:
            self._values["release"] = release
        if release_to_npm is not None:
            self._values["release_to_npm"] = release_to_npm
        if release_workflow is not None:
            self._values["release_workflow"] = release_workflow
        if workflow_bootstrap_steps is not None:
            self._values["workflow_bootstrap_steps"] = workflow_bootstrap_steps
        if workflow_git_identity is not None:
            self._values["workflow_git_identity"] = workflow_git_identity
        if workflow_node_version is not None:
            self._values["workflow_node_version"] = workflow_node_version
        if workflow_package_cache is not None:
            self._values["workflow_package_cache"] = workflow_package_cache

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) This is the name of your project.

        :default: $BASEDIR

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def commit_generated(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to commit the managed files by default.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("commit_generated")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def git_ignore_options(self) -> typing.Optional[_IgnoreFileOptions_86c48b91]:
        '''(experimental) Configuration options for .gitignore file.

        :stability: experimental
        '''
        result = self._values.get("git_ignore_options")
        return typing.cast(typing.Optional[_IgnoreFileOptions_86c48b91], result)

    @builtins.property
    def git_options(self) -> typing.Optional[_GitOptions_a65916a3]:
        '''(experimental) Configuration options for git.

        :stability: experimental
        '''
        result = self._values.get("git_options")
        return typing.cast(typing.Optional[_GitOptions_a65916a3], result)

    @builtins.property
    def logging(self) -> typing.Optional[_LoggerOptions_eb0f6309]:
        '''(experimental) Configure logging options such as verbosity.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[_LoggerOptions_eb0f6309], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) The root directory of the project.

        Relative to this directory, all files are synthesized.

        If this project has a parent, this directory is relative to the parent
        directory and it cannot be the same as the parent or any of it's other
        sub-projects.

        :default: "."

        :stability: experimental
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[_Project_57d89203]:
        '''(experimental) The parent project, if this project is part of a bigger project.

        :stability: experimental
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[_Project_57d89203], result)

    @builtins.property
    def projen_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The shell command to use in order to run the projen CLI.

        Can be used to customize in special environments.

        :default: "npx projen"

        :stability: experimental
        '''
        result = self._values.get("projen_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def projenrc_json(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("projenrc_json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_json_options(self) -> typing.Optional[_ProjenrcJsonOptions_9c40dd4f]:
        '''(experimental) Options for .projenrc.json.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_json_options")
        return typing.cast(typing.Optional[_ProjenrcJsonOptions_9c40dd4f], result)

    @builtins.property
    def renovatebot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use renovatebot to handle dependency upgrades.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("renovatebot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def renovatebot_options(self) -> typing.Optional[_RenovatebotOptions_18e6b8a1]:
        '''(experimental) Options for renovatebot.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("renovatebot_options")
        return typing.cast(typing.Optional[_RenovatebotOptions_18e6b8a1], result)

    @builtins.property
    def auto_approve_options(self) -> typing.Optional[_AutoApproveOptions_dac86cbe]:
        '''(experimental) Enable and configure the 'auto approve' workflow.

        :default: - auto approve is disabled

        :stability: experimental
        '''
        result = self._values.get("auto_approve_options")
        return typing.cast(typing.Optional[_AutoApproveOptions_dac86cbe], result)

    @builtins.property
    def auto_merge(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable automatic merging on GitHub.

        Has no effect if ``github.mergify``
        is set to false.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_merge")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_merge_options(self) -> typing.Optional[_AutoMergeOptions_d112cd3c]:
        '''(experimental) Configure options for automatic merging on GitHub.

        Has no effect if
        ``github.mergify`` or ``autoMerge`` is set to false.

        :default: - see defaults in ``AutoMergeOptions``

        :stability: experimental
        '''
        result = self._values.get("auto_merge_options")
        return typing.cast(typing.Optional[_AutoMergeOptions_d112cd3c], result)

    @builtins.property
    def clobber(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a ``clobber`` task which resets the repo to origin.

        :default: - true, but false for subprojects

        :stability: experimental
        '''
        result = self._values.get("clobber")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dev_container(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a VSCode development environment (used for GitHub Codespaces).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("dev_container")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def github(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable GitHub integration.

        Enabled by default for root projects. Disabled for non-root projects.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("github")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def github_options(self) -> typing.Optional[_GitHubOptions_21553699]:
        '''(experimental) Options for GitHub integration.

        :default: - see GitHubOptions

        :stability: experimental
        '''
        result = self._values.get("github_options")
        return typing.cast(typing.Optional[_GitHubOptions_21553699], result)

    @builtins.property
    def gitpod(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a Gitpod development environment.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("gitpod")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def mergify(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether mergify should be enabled on this repository or not.

        :default: true

        :deprecated: use ``githubOptions.mergify`` instead

        :stability: deprecated
        '''
        result = self._values.get("mergify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def mergify_options(self) -> typing.Optional[_MergifyOptions_a6faaab3]:
        '''(deprecated) Options for mergify.

        :default: - default options

        :deprecated: use ``githubOptions.mergifyOptions`` instead

        :stability: deprecated
        '''
        result = self._values.get("mergify_options")
        return typing.cast(typing.Optional[_MergifyOptions_a6faaab3], result)

    @builtins.property
    def project_type(self) -> typing.Optional[_ProjectType_fd80c725]:
        '''(deprecated) Which type of project this is (library/app).

        :default: ProjectType.UNKNOWN

        :deprecated: no longer supported at the base project level

        :stability: deprecated
        '''
        result = self._values.get("project_type")
        return typing.cast(typing.Optional[_ProjectType_fd80c725], result)

    @builtins.property
    def projen_credentials(self) -> typing.Optional[_GithubCredentials_ae257072]:
        '''(experimental) Choose a method of providing GitHub API access for projen workflows.

        :default: - use a personal access token named PROJEN_GITHUB_TOKEN

        :stability: experimental
        '''
        result = self._values.get("projen_credentials")
        return typing.cast(typing.Optional[_GithubCredentials_ae257072], result)

    @builtins.property
    def projen_token_secret(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name of a secret which includes a GitHub Personal Access Token to be used by projen workflows.

        This token needs to have the ``repo``, ``workflows``
        and ``packages`` scope.

        :default: "PROJEN_GITHUB_TOKEN"

        :deprecated: use ``projenCredentials``

        :stability: deprecated
        '''
        result = self._values.get("projen_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readme(self) -> typing.Optional[_SampleReadmeProps_3518b03b]:
        '''(experimental) The README setup.

        :default: - { filename: 'README.md', contents: '# replace this' }

        :stability: experimental

        Example::

            "{ filename: 'readme.md', contents: '# title' }"
        '''
        result = self._values.get("readme")
        return typing.cast(typing.Optional[_SampleReadmeProps_3518b03b], result)

    @builtins.property
    def stale(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Auto-close of stale issues and pull request.

        See ``staleOptions`` for options.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("stale")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stale_options(self) -> typing.Optional[_StaleOptions_929db764]:
        '''(experimental) Auto-close stale issues and pull requests.

        To disable set ``stale`` to ``false``.

        :default: - see defaults in ``StaleOptions``

        :stability: experimental
        '''
        result = self._values.get("stale_options")
        return typing.cast(typing.Optional[_StaleOptions_929db764], result)

    @builtins.property
    def vscode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable VSCode integration.

        Enabled by default for root projects. Disabled for non-root projects.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("vscode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_library_dependencies(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow the project to include ``peerDependencies`` and ``bundledDependencies``.

        This is normally only allowed for libraries. For apps, there's no meaning
        for specifying these.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("allow_library_dependencies")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def author_email(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's e-mail.

        :stability: experimental
        '''
        result = self._values.get("author_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def author_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's name.

        :stability: experimental
        '''
        result = self._values.get("author_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def author_organization(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Is the author an organization.

        :stability: experimental
        '''
        result = self._values.get("author_organization")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def author_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) Author's URL / Website.

        :stability: experimental
        '''
        result = self._values.get("author_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_detect_bin(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically add all executables under the ``bin`` directory to your ``package.json`` file under the ``bin`` section.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_detect_bin")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bin(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Binary programs vended with your module.

        You can use this option to add/customize how binaries are represented in
        your ``package.json``, but unless ``autoDetectBin`` is ``false``, every
        executable file under ``bin`` will automatically be added to this section.

        :stability: experimental
        '''
        result = self._values.get("bin")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def bugs_email(self) -> typing.Optional[builtins.str]:
        '''(experimental) The email address to which issues should be reported.

        :stability: experimental
        '''
        result = self._values.get("bugs_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bugs_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The url to your project's issue tracker.

        :stability: experimental
        '''
        result = self._values.get("bugs_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bundled_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of dependencies to bundle into this module.

        These modules will be
        added both to the ``dependencies`` section and ``bundledDependencies`` section of
        your ``package.json``.

        The recommendation is to only specify the module name here (e.g.
        ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the
        sense that it will add the module as a dependency to your ``package.json``
        file with the latest version (``^``). You can specify semver requirements in
        the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and
        this will be what you ``package.json`` will eventually include.

        :stability: experimental
        '''
        result = self._values.get("bundled_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def code_artifact_options(self) -> typing.Optional[CodeArtifactOptions]:
        '''(experimental) Options for npm packages using AWS CodeArtifact.

        This is required if publishing packages to, or installing scoped packages from AWS CodeArtifact

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("code_artifact_options")
        return typing.cast(typing.Optional[CodeArtifactOptions], result)

    @builtins.property
    def deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Runtime dependencies of this module.

        The recommendation is to only specify the module name here (e.g.
        ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the
        sense that it will add the module as a dependency to your ``package.json``
        file with the latest version (``^``). You can specify semver requirements in
        the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and
        this will be what you ``package.json`` will eventually include.

        :default: []

        :stability: experimental
        :featured: true

        Example::

            [ 'express', 'lodash', 'foo@^2' ]
        '''
        result = self._values.get("deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description is just a string that helps people understand the purpose of the package.

        It can be used when searching for packages in a package manager as well.
        See https://classic.yarnpkg.com/en/docs/package-json/#toc-description

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dev_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Build dependencies for this module.

        These dependencies will only be
        available in your build environment but will not be fetched when this
        module is consumed.

        The recommendation is to only specify the module name here (e.g.
        ``express``). This will behave similar to ``yarn add`` or ``npm install`` in the
        sense that it will add the module as a dependency to your ``package.json``
        file with the latest version (``^``). You can specify semver requirements in
        the same syntax passed to ``npm i`` or ``yarn add`` (e.g. ``express@^2``) and
        this will be what you ``package.json`` will eventually include.

        :default: []

        :stability: experimental
        :featured: true

        Example::

            [ 'typescript', '@types/express' ]
        '''
        result = self._values.get("dev_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def entrypoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) Module entrypoint (``main`` in ``package.json``).

        Set to an empty string to not include ``main`` in your package.json

        :default: "lib/index.js"

        :stability: experimental
        '''
        result = self._values.get("entrypoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def homepage(self) -> typing.Optional[builtins.str]:
        '''(experimental) Package's Homepage / Website.

        :stability: experimental
        '''
        result = self._values.get("homepage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keywords(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Keywords to include in ``package.json``.

        :stability: experimental
        '''
        result = self._values.get("keywords")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def license(self) -> typing.Optional[builtins.str]:
        '''(experimental) License's SPDX identifier.

        See https://github.com/projen/projen/tree/main/license-text for a list of supported licenses.
        Use the ``licensed`` option if you want to no license to be specified.

        :default: "Apache-2.0"

        :stability: experimental
        '''
        result = self._values.get("license")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def licensed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates if a license should be added.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("licensed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum node.js version to require via ``engines`` (inclusive).

        :default: - no max

        :stability: experimental
        '''
        result = self._values.get("max_node_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Minimum Node.js version to require via package.json ``engines`` (inclusive).

        :default: - no "engines" specified

        :stability: experimental
        '''
        result = self._values.get("min_node_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_access(self) -> typing.Optional["NpmAccess"]:
        '''(experimental) Access level of the npm package.

        :default:

        - for scoped packages (e.g. ``foo@bar``), the default is
        ``NpmAccess.RESTRICTED``, for non-scoped packages, the default is
        ``NpmAccess.PUBLIC``.

        :stability: experimental
        '''
        result = self._values.get("npm_access")
        return typing.cast(typing.Optional["NpmAccess"], result)

    @builtins.property
    def npm_registry(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The host name of the npm registry to publish to.

        Cannot be set together with ``npmRegistryUrl``.

        :deprecated: use ``npmRegistryUrl`` instead

        :stability: deprecated
        '''
        result = self._values.get("npm_registry")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_registry_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The base URL of the npm package registry.

        Must be a URL (e.g. start with "https://" or "http://")

        :default: "https://registry.npmjs.org"

        :stability: experimental
        '''
        result = self._values.get("npm_registry_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_token_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret which contains the NPM token to use when publishing packages.

        :default: "NPM_TOKEN"

        :stability: experimental
        '''
        result = self._values.get("npm_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def package_manager(self) -> typing.Optional[NodePackageManager]:
        '''(experimental) The Node Package Manager used to execute scripts.

        :default: NodePackageManager.YARN

        :stability: experimental
        '''
        result = self._values.get("package_manager")
        return typing.cast(typing.Optional[NodePackageManager], result)

    @builtins.property
    def package_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The "name" in package.json.

        :default: - defaults to project name

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("package_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_dependency_options(self) -> typing.Optional["PeerDependencyOptions"]:
        '''(experimental) Options for ``peerDeps``.

        :stability: experimental
        '''
        result = self._values.get("peer_dependency_options")
        return typing.cast(typing.Optional["PeerDependencyOptions"], result)

    @builtins.property
    def peer_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Peer dependencies for this module.

        Dependencies listed here are required to
        be installed (and satisfied) by the *consumer* of this library. Using peer
        dependencies allows you to ensure that only a single module of a certain
        library exists in the ``node_modules`` tree of your consumers.

        Note that prior to npm@7, peer dependencies are *not* automatically
        installed, which means that adding peer dependencies to a library will be a
        breaking change for your customers.

        Unless ``peerDependencyOptions.pinnedDevDependency`` is disabled (it is
        enabled by default), projen will automatically add a dev dependency with a
        pinned version for each peer dependency. This will ensure that you build &
        test your module against the lowest peer version required.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("peer_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pnpm_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of PNPM to use if using PNPM as a package manager.

        :default: "7"

        :stability: experimental
        '''
        result = self._values.get("pnpm_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''(experimental) The repository is the location where the actual code for your package lives.

        See https://classic.yarnpkg.com/en/docs/package-json/#toc-repository

        :stability: experimental
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) If the package.json for your package is not in the root directory (for example if it is part of a monorepo), you can specify the directory in which it lives.

        :stability: experimental
        '''
        result = self._values.get("repository_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scoped_packages_options(
        self,
    ) -> typing.Optional[typing.List["ScopedPackagesOptions"]]:
        '''(experimental) Options for privately hosted scoped packages.

        :default: - fetch all scoped packages from the public npm registry

        :stability: experimental
        '''
        result = self._values.get("scoped_packages_options")
        return typing.cast(typing.Optional[typing.List["ScopedPackagesOptions"]], result)

    @builtins.property
    def scripts(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(deprecated) npm scripts to include.

        If a script has the same name as a standard script,
        the standard script will be overwritten.
        Also adds the script as a task.

        :default: {}

        :deprecated: use ``project.addTask()`` or ``package.setScript()``

        :stability: deprecated
        '''
        result = self._values.get("scripts")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def stability(self) -> typing.Optional[builtins.str]:
        '''(experimental) Package's Stability.

        :stability: experimental
        '''
        result = self._values.get("stability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsii_release_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version requirement of ``publib`` which is used to publish modules to npm.

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("jsii_release_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def major_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Major version to release from the default branch.

        If this is specified, we bump the latest version of this major version line.
        If not specified, we bump the global latest version.

        :default: - Major version is not enforced.

        :stability: experimental
        '''
        result = self._values.get("major_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_major_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Minimal Major version to release.

        This can be useful to set to 1, as breaking changes before the 1.x major
        release are not incrementing the major version number.

        Can not be set together with ``majorVersion``.

        :default: - No minimum version is being enforced

        :stability: experimental
        '''
        result = self._values.get("min_major_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def npm_dist_tag(self) -> typing.Optional[builtins.str]:
        '''(experimental) The npmDistTag to use when publishing from the default branch.

        To set the npm dist-tag for release branches, set the ``npmDistTag`` property
        for each branch.

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("npm_dist_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_build_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute after build as part of the release workflow.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("post_build_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def prerelease(self) -> typing.Optional[builtins.str]:
        '''(experimental) Bump versions from the default branch as pre-releases (e.g. "beta", "alpha", "pre").

        :default: - normal semantic versions

        :stability: experimental
        '''
        result = self._values.get("prerelease")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_dry_run(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Instead of actually publishing to package managers, just print the publishing command.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("publish_dry_run")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def publish_tasks(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Define publishing tasks that can be executed manually as well as workflows.

        Normally, publishing only happens within automated workflows. Enable this
        in order to create a publishing task for each publishing activity.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("publish_tasks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def releasable_commits(self) -> typing.Optional[_ReleasableCommits_d481ce10]:
        '''(experimental) Find commits that should be considered releasable Used to decide if a release is required.

        :default: ReleasableCommits.everyCommit()

        :stability: experimental
        '''
        result = self._values.get("releasable_commits")
        return typing.cast(typing.Optional[_ReleasableCommits_d481ce10], result)

    @builtins.property
    def release_branches(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _BranchOptions_13663d08]]:
        '''(experimental) Defines additional release branches.

        A workflow will be created for each
        release branch which will publish releases from commits in this branch.
        Each release branch *must* be assigned a major version number which is used
        to enforce that versions published from that branch always use that major
        version. If multiple branches are used, the ``majorVersion`` field must also
        be provided for the default branch.

        :default:

        - no additional branches are used for release. you can use
        ``addBranch()`` to add additional branches.

        :stability: experimental
        '''
        result = self._values.get("release_branches")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _BranchOptions_13663d08]], result)

    @builtins.property
    def release_every_commit(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Automatically release new versions every commit to one of branches in ``releaseBranches``.

        :default: true

        :deprecated: Use ``releaseTrigger: ReleaseTrigger.continuous()`` instead

        :stability: deprecated
        '''
        result = self._values.get("release_every_commit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_failure_issue(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Create a github issue on every failed publishing task.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("release_failure_issue")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_failure_issue_label(self) -> typing.Optional[builtins.str]:
        '''(experimental) The label to apply to issues indicating publish failures.

        Only applies if ``releaseFailureIssue`` is true.

        :default: "failed-release"

        :stability: experimental
        '''
        result = self._values.get("release_failure_issue_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_schedule(self) -> typing.Optional[builtins.str]:
        '''(deprecated) CRON schedule to trigger new releases.

        :default: - no scheduled releases

        :deprecated: Use ``releaseTrigger: ReleaseTrigger.scheduled()`` instead

        :stability: deprecated
        '''
        result = self._values.get("release_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_tag_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers.

        Note: this prefix is used to detect the latest tagged version
        when bumping, so if you change this on a project with an existing version
        history, you may need to manually tag your latest release
        with the new prefix.

        :default: "v"

        :stability: experimental
        '''
        result = self._values.get("release_tag_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_trigger(self) -> typing.Optional[_ReleaseTrigger_e4dc221f]:
        '''(experimental) The release trigger to use.

        :default: - Continuous releases (``ReleaseTrigger.continuous()``)

        :stability: experimental
        '''
        result = self._values.get("release_trigger")
        return typing.cast(typing.Optional[_ReleaseTrigger_e4dc221f], result)

    @builtins.property
    def release_workflow_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the default release workflow.

        :default: "Release"

        :stability: experimental
        '''
        result = self._values.get("release_workflow_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_workflow_setup_steps(
        self,
    ) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) A set of workflow steps to execute in order to setup the workflow container.

        :stability: experimental
        '''
        result = self._values.get("release_workflow_setup_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def versionrc_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Custom configuration used when creating changelog with standard-version package.

        Given values either append to default configuration or overwrite values in it.

        :default: - standard configuration applicable for GitHub repositories

        :stability: experimental
        '''
        result = self._values.get("versionrc_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workflow_container_image(self) -> typing.Optional[builtins.str]:
        '''(experimental) Container image to use for GitHub workflows.

        :default: - default image

        :stability: experimental
        '''
        result = self._values.get("workflow_container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_runs_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Github Runner selection labels.

        :default: ["ubuntu-latest"]

        :stability: experimental
        :description: Defines a target Runner by labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("workflow_runs_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def workflow_runs_on_group(self) -> typing.Optional[_GroupRunnerOptions_148c59c1]:
        '''(experimental) Github Runner Group selection options.

        :stability: experimental
        :description: Defines a target Runner Group by name and/or labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("workflow_runs_on_group")
        return typing.cast(typing.Optional[_GroupRunnerOptions_148c59c1], result)

    @builtins.property
    def default_release_branch(self) -> builtins.str:
        '''(experimental) The name of the main release branch.

        :default: "main"

        :stability: experimental
        '''
        result = self._values.get("default_release_branch")
        assert result is not None, "Required property 'default_release_branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def artifacts_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) A directory which will contain build artifacts.

        :default: "dist"

        :stability: experimental
        '''
        result = self._values.get("artifacts_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_approve_upgrades(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically approve deps upgrade PRs, allowing them to be merged by mergify (if configued).

        Throw if set to true but ``autoApproveOptions`` are not defined.

        :default: - true

        :stability: experimental
        '''
        result = self._values.get("auto_approve_upgrades")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def build_workflow(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Define a GitHub workflow for building PRs.

        :default: - true if not a subproject

        :stability: experimental
        '''
        result = self._values.get("build_workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def build_workflow_triggers(self) -> typing.Optional[_Triggers_e9ae7617]:
        '''(experimental) Build workflow triggers.

        :default: "{ pullRequest: {}, workflowDispatch: {} }"

        :stability: experimental
        '''
        result = self._values.get("build_workflow_triggers")
        return typing.cast(typing.Optional[_Triggers_e9ae7617], result)

    @builtins.property
    def bundler_options(self) -> typing.Optional[BundlerOptions]:
        '''(experimental) Options for ``Bundler``.

        :stability: experimental
        '''
        result = self._values.get("bundler_options")
        return typing.cast(typing.Optional[BundlerOptions], result)

    @builtins.property
    def code_cov(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Define a GitHub workflow step for sending code coverage metrics to https://codecov.io/ Uses codecov/codecov-action@v3 A secret is required for private repos. Configured with ``@codeCovTokenSecret``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("code_cov")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def code_cov_token_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) Define the secret name for a specified https://codecov.io/ token A secret is required to send coverage for private repositories.

        :default: - if this option is not specified, only public repositories are supported

        :stability: experimental
        '''
        result = self._values.get("code_cov_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copyright_owner(self) -> typing.Optional[builtins.str]:
        '''(experimental) License copyright owner.

        :default: - defaults to the value of authorName or "" if ``authorName`` is undefined.

        :stability: experimental
        '''
        result = self._values.get("copyright_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copyright_period(self) -> typing.Optional[builtins.str]:
        '''(experimental) The copyright years to put in the LICENSE file.

        :default: - current year

        :stability: experimental
        '''
        result = self._values.get("copyright_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dependabot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use dependabot to handle dependency upgrades.

        Cannot be used in conjunction with ``depsUpgrade``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("dependabot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dependabot_options(self) -> typing.Optional[_DependabotOptions_0cedc635]:
        '''(experimental) Options for dependabot.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("dependabot_options")
        return typing.cast(typing.Optional[_DependabotOptions_0cedc635], result)

    @builtins.property
    def deps_upgrade(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use tasks and github workflows to handle dependency upgrades.

        Cannot be used in conjunction with ``dependabot``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("deps_upgrade")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def deps_upgrade_options(self) -> typing.Optional["UpgradeDependenciesOptions"]:
        '''(experimental) Options for ``UpgradeDependencies``.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("deps_upgrade_options")
        return typing.cast(typing.Optional["UpgradeDependenciesOptions"], result)

    @builtins.property
    def gitignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional entries to .gitignore.

        :stability: experimental
        '''
        result = self._values.get("gitignore")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jest(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Setup jest unit tests.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("jest")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def jest_options(self) -> typing.Optional[JestOptions]:
        '''(experimental) Jest options.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("jest_options")
        return typing.cast(typing.Optional[JestOptions], result)

    @builtins.property
    def mutable_build(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically update files modified during builds to pull-request branches.

        This means
        that any files synthesized by projen or e.g. test snapshots will always be up-to-date
        before a PR is merged.

        Implies that PR builds do not have anti-tamper checks.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("mutable_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def npmignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Additional entries to .npmignore.

        :deprecated: - use ``project.addPackageIgnore``

        :stability: deprecated
        '''
        result = self._values.get("npmignore")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def npmignore_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Defines an .npmignore file. Normally this is only needed for libraries that are packaged as tarballs.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("npmignore_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def npm_ignore_options(self) -> typing.Optional[_IgnoreFileOptions_86c48b91]:
        '''(experimental) Configuration options for .npmignore file.

        :stability: experimental
        '''
        result = self._values.get("npm_ignore_options")
        return typing.cast(typing.Optional[_IgnoreFileOptions_86c48b91], result)

    @builtins.property
    def package(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Defines a ``package`` task that will produce an npm tarball under the artifacts directory (e.g. ``dist``).

        :default: true

        :stability: experimental
        '''
        result = self._values.get("package")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def prettier(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Setup prettier.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("prettier")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def prettier_options(self) -> typing.Optional["PrettierOptions"]:
        '''(experimental) Prettier options.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("prettier_options")
        return typing.cast(typing.Optional["PrettierOptions"], result)

    @builtins.property
    def projen_dev_dependency(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates of "projen" should be installed as a devDependency.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("projen_dev_dependency")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_js(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate (once) .projenrc.js (in JavaScript). Set to ``false`` in order to disable .projenrc.js generation.

        :default: - true if projenrcJson is false

        :stability: experimental
        '''
        result = self._values.get("projenrc_js")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_js_options(self) -> typing.Optional["ProjenrcOptions"]:
        '''(experimental) Options for .projenrc.js.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_js_options")
        return typing.cast(typing.Optional["ProjenrcOptions"], result)

    @builtins.property
    def projen_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version of projen to install.

        :default: - Defaults to the latest version.

        :stability: experimental
        '''
        result = self._values.get("projen_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_request_template(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include a GitHub pull request template.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("pull_request_template")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pull_request_template_contents(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The contents of the pull request template.

        :default: - default content

        :stability: experimental
        '''
        result = self._values.get("pull_request_template_contents")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def release(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add release management to this project.

        :default: - true (false for subprojects)

        :stability: experimental
        '''
        result = self._values.get("release")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_to_npm(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically release to npm when new versions are introduced.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("release_to_npm")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_workflow(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) DEPRECATED: renamed to ``release``.

        :default: - true if not a subproject

        :deprecated: see ``release``.

        :stability: deprecated
        '''
        result = self._values.get("release_workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def workflow_bootstrap_steps(
        self,
    ) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Workflow steps to use in order to bootstrap this repo.

        :default: "yarn install --frozen-lockfile && yarn projen"

        :stability: experimental
        '''
        result = self._values.get("workflow_bootstrap_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def workflow_git_identity(self) -> typing.Optional[_GitIdentity_6effc3de]:
        '''(experimental) The git identity to use in workflows.

        :default: - GitHub Actions

        :stability: experimental
        '''
        result = self._values.get("workflow_git_identity")
        return typing.cast(typing.Optional[_GitIdentity_6effc3de], result)

    @builtins.property
    def workflow_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The node version to use in GitHub workflows.

        :default: - same as ``minNodeVersion``

        :stability: experimental
        '''
        result = self._values.get("workflow_node_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_package_cache(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable Node.js package cache in GitHub workflows.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("workflow_package_cache")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NodeProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.NpmAccess")
class NpmAccess(enum.Enum):
    '''(experimental) Npm package access level.

    :stability: experimental
    '''

    PUBLIC = "PUBLIC"
    '''(experimental) Package is public.

    :stability: experimental
    '''
    RESTRICTED = "RESTRICTED"
    '''(experimental) Package can only be accessed with credentials.

    :stability: experimental
    '''


class NpmConfig(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.javascript.NpmConfig",
):
    '''(experimental) File representing the local NPM config in .npmrc.

    :stability: experimental
    '''

    def __init__(
        self,
        project: NodeProject,
        *,
        omit_empty: typing.Optional[builtins.bool] = None,
        registry: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param omit_empty: (experimental) Omits empty objects and arrays. Default: false
        :param registry: (experimental) URL of the registry mirror to use. You can change this or add scoped registries using the addRegistry method Default: - use npmjs default registry

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b746251f1b75ba953324566d41e0b8f83e1f3c11b8bdc5916f09fd559914d7)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = NpmConfigOptions(omit_empty=omit_empty, registry=registry)

        jsii.create(self.__class__, self, [project, options])

    @jsii.member(jsii_name="addConfig")
    def add_config(self, name: builtins.str, value: builtins.str) -> None:
        '''(experimental) configure a generic property.

        :param name: the name of the property.
        :param value: the value of the property.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ffe4a0f2f0471b68c6ec185cbf4f5c192b37a79c19e45ac41370d2378eff782)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addConfig", [name, value]))

    @jsii.member(jsii_name="addRegistry")
    def add_registry(
        self,
        url: builtins.str,
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) configure a scoped registry.

        :param url: the URL of the registry to use.
        :param scope: the scope the registry is used for; leave empty for the default registry

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__921c1baed18b2592b0599b66374de0e67495b5712f0889a23b2f5fd572fa7378)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(None, jsii.invoke(self, "addRegistry", [url, scope]))


@jsii.data_type(
    jsii_type="projen.javascript.NpmConfigOptions",
    jsii_struct_bases=[],
    name_mapping={"omit_empty": "omitEmpty", "registry": "registry"},
)
class NpmConfigOptions:
    def __init__(
        self,
        *,
        omit_empty: typing.Optional[builtins.bool] = None,
        registry: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options to configure the local NPM config.

        :param omit_empty: (experimental) Omits empty objects and arrays. Default: false
        :param registry: (experimental) URL of the registry mirror to use. You can change this or add scoped registries using the addRegistry method Default: - use npmjs default registry

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572f231bc39b987387ccaf3d47dab1ff17bcba6b190a9675a89313a364b340f6)
            check_type(argname="argument omit_empty", value=omit_empty, expected_type=type_hints["omit_empty"])
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if omit_empty is not None:
            self._values["omit_empty"] = omit_empty
        if registry is not None:
            self._values["registry"] = registry

    @builtins.property
    def omit_empty(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Omits empty objects and arrays.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("omit_empty")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def registry(self) -> typing.Optional[builtins.str]:
        '''(experimental) URL of the registry mirror to use.

        You can change this or add scoped registries using the addRegistry method

        :default: - use npmjs default registry

        :stability: experimental
        '''
        result = self._values.get("registry")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NpmConfigOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.PeerDependencyOptions",
    jsii_struct_bases=[],
    name_mapping={"pinned_dev_dependency": "pinnedDevDependency"},
)
class PeerDependencyOptions:
    def __init__(
        self,
        *,
        pinned_dev_dependency: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param pinned_dev_dependency: (experimental) Automatically add a pinned dev dependency. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc70f793ab1a81781f2ffafe90b1661555f4fb8d4aeb489bcb926e034f01a743)
            check_type(argname="argument pinned_dev_dependency", value=pinned_dev_dependency, expected_type=type_hints["pinned_dev_dependency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pinned_dev_dependency is not None:
            self._values["pinned_dev_dependency"] = pinned_dev_dependency

    @builtins.property
    def pinned_dev_dependency(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically add a pinned dev dependency.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("pinned_dev_dependency")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PeerDependencyOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Prettier(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.javascript.Prettier",
):
    '''(experimental) Represents prettier configuration.

    :stability: experimental
    '''

    def __init__(
        self,
        project: NodeProject,
        *,
        ignore_file: typing.Optional[builtins.bool] = None,
        ignore_file_options: typing.Optional[typing.Union[_IgnoreFileOptions_86c48b91, typing.Dict[builtins.str, typing.Any]]] = None,
        overrides: typing.Optional[typing.Sequence[typing.Union["PrettierOverride", typing.Dict[builtins.str, typing.Any]]]] = None,
        settings: typing.Optional[typing.Union["PrettierSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        yaml: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param project: -
        :param ignore_file: (experimental) Defines an .prettierIgnore file. Default: true
        :param ignore_file_options: (experimental) Configuration options for .prettierignore file.
        :param overrides: (experimental) Provide a list of patterns to override prettier configuration. Default: []
        :param settings: (experimental) Prettier settings. Default: - default settings
        :param yaml: (experimental) Write prettier configuration as YAML instead of JSON. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc54704eb480a73e451f86bffd16f1d9313443e3d2f9b556889330fd0715ad95)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = PrettierOptions(
            ignore_file=ignore_file,
            ignore_file_options=ignore_file_options,
            overrides=overrides,
            settings=settings,
            yaml=yaml,
        )

        jsii.create(self.__class__, self, [project, options])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, project: _Project_57d89203) -> typing.Optional["Prettier"]:
        '''
        :param project: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1fd367ba7a3d51b9e260e79983f7d6fb9647a9bad81693c033d3218ba83e83f)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        return typing.cast(typing.Optional["Prettier"], jsii.sinvoke(cls, "of", [project]))

    @jsii.member(jsii_name="addIgnorePattern")
    def add_ignore_pattern(self, pattern: builtins.str) -> None:
        '''(experimental) Defines Prettier ignore Patterns these patterns will be added to the file .prettierignore.

        :param pattern: filepatterns so exclude from prettier formatting.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__564118067a14c8c300f791c1ea85edc55544d5c6098386e20c2b6bc3e7b10df4)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(None, jsii.invoke(self, "addIgnorePattern", [pattern]))

    @jsii.member(jsii_name="addOverride")
    def add_override(
        self,
        *,
        files: typing.Union[builtins.str, typing.Sequence[builtins.str]],
        options: typing.Union["PrettierSettings", typing.Dict[builtins.str, typing.Any]],
        exclude_files: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    ) -> None:
        '''(experimental) Add a prettier override.

        :param files: (experimental) Include these files in this override.
        :param options: (experimental) The options to apply for this override.
        :param exclude_files: (experimental) Exclude these files from this override.

        :see: https://prettier.io/docs/en/configuration.html#configuration-overrides
        :stability: experimental
        '''
        override = PrettierOverride(
            files=files, options=options, exclude_files=exclude_files
        )

        return typing.cast(None, jsii.invoke(self, "addOverride", [override]))

    @jsii.member(jsii_name="preSynthesize")
    def pre_synthesize(self) -> None:
        '''(experimental) Called before synthesis.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "preSynthesize", []))

    @builtins.property
    @jsii.member(jsii_name="overrides")
    def overrides(self) -> typing.List["PrettierOverride"]:
        '''(experimental) Returns all Prettier overrides.

        :stability: experimental
        '''
        return typing.cast(typing.List["PrettierOverride"], jsii.get(self, "overrides"))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(self) -> "PrettierSettings":
        '''(experimental) Direct access to the prettier settings.

        :stability: experimental
        '''
        return typing.cast("PrettierSettings", jsii.get(self, "settings"))

    @builtins.property
    @jsii.member(jsii_name="ignoreFile")
    def ignore_file(self) -> typing.Optional[_IgnoreFile_3df2076a]:
        '''(experimental) The .prettierIgnore file.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IgnoreFile_3df2076a], jsii.get(self, "ignoreFile"))


@jsii.data_type(
    jsii_type="projen.javascript.PrettierOptions",
    jsii_struct_bases=[],
    name_mapping={
        "ignore_file": "ignoreFile",
        "ignore_file_options": "ignoreFileOptions",
        "overrides": "overrides",
        "settings": "settings",
        "yaml": "yaml",
    },
)
class PrettierOptions:
    def __init__(
        self,
        *,
        ignore_file: typing.Optional[builtins.bool] = None,
        ignore_file_options: typing.Optional[typing.Union[_IgnoreFileOptions_86c48b91, typing.Dict[builtins.str, typing.Any]]] = None,
        overrides: typing.Optional[typing.Sequence[typing.Union["PrettierOverride", typing.Dict[builtins.str, typing.Any]]]] = None,
        settings: typing.Optional[typing.Union["PrettierSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        yaml: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for Prettier.

        :param ignore_file: (experimental) Defines an .prettierIgnore file. Default: true
        :param ignore_file_options: (experimental) Configuration options for .prettierignore file.
        :param overrides: (experimental) Provide a list of patterns to override prettier configuration. Default: []
        :param settings: (experimental) Prettier settings. Default: - default settings
        :param yaml: (experimental) Write prettier configuration as YAML instead of JSON. Default: false

        :stability: experimental
        '''
        if isinstance(ignore_file_options, dict):
            ignore_file_options = _IgnoreFileOptions_86c48b91(**ignore_file_options)
        if isinstance(settings, dict):
            settings = PrettierSettings(**settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83f36238b807da08b92be98c6d4956285442f99303983562db38dda7f23c13ae)
            check_type(argname="argument ignore_file", value=ignore_file, expected_type=type_hints["ignore_file"])
            check_type(argname="argument ignore_file_options", value=ignore_file_options, expected_type=type_hints["ignore_file_options"])
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
            check_type(argname="argument yaml", value=yaml, expected_type=type_hints["yaml"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ignore_file is not None:
            self._values["ignore_file"] = ignore_file
        if ignore_file_options is not None:
            self._values["ignore_file_options"] = ignore_file_options
        if overrides is not None:
            self._values["overrides"] = overrides
        if settings is not None:
            self._values["settings"] = settings
        if yaml is not None:
            self._values["yaml"] = yaml

    @builtins.property
    def ignore_file(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Defines an .prettierIgnore file.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("ignore_file")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ignore_file_options(self) -> typing.Optional[_IgnoreFileOptions_86c48b91]:
        '''(experimental) Configuration options for .prettierignore file.

        :stability: experimental
        '''
        result = self._values.get("ignore_file_options")
        return typing.cast(typing.Optional[_IgnoreFileOptions_86c48b91], result)

    @builtins.property
    def overrides(self) -> typing.Optional[typing.List["PrettierOverride"]]:
        '''(experimental) Provide a list of patterns to override prettier configuration.

        :default: []

        :see: https://prettier.io/docs/en/configuration.html#configuration-overrides
        :stability: experimental
        '''
        result = self._values.get("overrides")
        return typing.cast(typing.Optional[typing.List["PrettierOverride"]], result)

    @builtins.property
    def settings(self) -> typing.Optional["PrettierSettings"]:
        '''(experimental) Prettier settings.

        :default: - default settings

        :stability: experimental
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Optional["PrettierSettings"], result)

    @builtins.property
    def yaml(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Write prettier configuration as YAML instead of JSON.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("yaml")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrettierOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.PrettierOverride",
    jsii_struct_bases=[],
    name_mapping={
        "files": "files",
        "options": "options",
        "exclude_files": "excludeFiles",
    },
)
class PrettierOverride:
    def __init__(
        self,
        *,
        files: typing.Union[builtins.str, typing.Sequence[builtins.str]],
        options: typing.Union["PrettierSettings", typing.Dict[builtins.str, typing.Any]],
        exclude_files: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    ) -> None:
        '''
        :param files: (experimental) Include these files in this override.
        :param options: (experimental) The options to apply for this override.
        :param exclude_files: (experimental) Exclude these files from this override.

        :stability: experimental
        '''
        if isinstance(options, dict):
            options = PrettierSettings(**options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bbdf8c18a86fcbd11c29b6e1ec1c6cb7b1e3a7ae688bedb8e25c15099f3e25e)
            check_type(argname="argument files", value=files, expected_type=type_hints["files"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument exclude_files", value=exclude_files, expected_type=type_hints["exclude_files"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "files": files,
            "options": options,
        }
        if exclude_files is not None:
            self._values["exclude_files"] = exclude_files

    @builtins.property
    def files(self) -> typing.Union[builtins.str, typing.List[builtins.str]]:
        '''(experimental) Include these files in this override.

        :stability: experimental
        '''
        result = self._values.get("files")
        assert result is not None, "Required property 'files' is missing"
        return typing.cast(typing.Union[builtins.str, typing.List[builtins.str]], result)

    @builtins.property
    def options(self) -> "PrettierSettings":
        '''(experimental) The options to apply for this override.

        :stability: experimental
        '''
        result = self._values.get("options")
        assert result is not None, "Required property 'options' is missing"
        return typing.cast("PrettierSettings", result)

    @builtins.property
    def exclude_files(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]]:
        '''(experimental) Exclude these files from this override.

        :stability: experimental
        '''
        result = self._values.get("exclude_files")
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrettierOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.PrettierSettings",
    jsii_struct_bases=[],
    name_mapping={
        "arrow_parens": "arrowParens",
        "bracket_same_line": "bracketSameLine",
        "bracket_spacing": "bracketSpacing",
        "cursor_offset": "cursorOffset",
        "embedded_language_formatting": "embeddedLanguageFormatting",
        "end_of_line": "endOfLine",
        "filepath": "filepath",
        "html_whitespace_sensitivity": "htmlWhitespaceSensitivity",
        "insert_pragma": "insertPragma",
        "jsx_single_quote": "jsxSingleQuote",
        "parser": "parser",
        "plugins": "plugins",
        "plugin_search_dirs": "pluginSearchDirs",
        "print_width": "printWidth",
        "prose_wrap": "proseWrap",
        "quote_props": "quoteProps",
        "range_end": "rangeEnd",
        "range_start": "rangeStart",
        "require_pragma": "requirePragma",
        "semi": "semi",
        "single_quote": "singleQuote",
        "tab_width": "tabWidth",
        "trailing_comma": "trailingComma",
        "use_tabs": "useTabs",
        "vue_indent_script_and_style": "vueIndentScriptAndStyle",
    },
)
class PrettierSettings:
    def __init__(
        self,
        *,
        arrow_parens: typing.Optional[ArrowParens] = None,
        bracket_same_line: typing.Optional[builtins.bool] = None,
        bracket_spacing: typing.Optional[builtins.bool] = None,
        cursor_offset: typing.Optional[jsii.Number] = None,
        embedded_language_formatting: typing.Optional[EmbeddedLanguageFormatting] = None,
        end_of_line: typing.Optional[EndOfLine] = None,
        filepath: typing.Optional[builtins.str] = None,
        html_whitespace_sensitivity: typing.Optional[HTMLWhitespaceSensitivity] = None,
        insert_pragma: typing.Optional[builtins.bool] = None,
        jsx_single_quote: typing.Optional[builtins.bool] = None,
        parser: typing.Optional[builtins.str] = None,
        plugins: typing.Optional[typing.Sequence[builtins.str]] = None,
        plugin_search_dirs: typing.Optional[typing.Sequence[builtins.str]] = None,
        print_width: typing.Optional[jsii.Number] = None,
        prose_wrap: typing.Optional["ProseWrap"] = None,
        quote_props: typing.Optional["QuoteProps"] = None,
        range_end: typing.Optional[jsii.Number] = None,
        range_start: typing.Optional[jsii.Number] = None,
        require_pragma: typing.Optional[builtins.bool] = None,
        semi: typing.Optional[builtins.bool] = None,
        single_quote: typing.Optional[builtins.bool] = None,
        tab_width: typing.Optional[jsii.Number] = None,
        trailing_comma: typing.Optional["TrailingComma"] = None,
        use_tabs: typing.Optional[builtins.bool] = None,
        vue_indent_script_and_style: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options to set in Prettier directly or through overrides.

        :param arrow_parens: (experimental) Include parentheses around a sole arrow function parameter. Default: ArrowParens.ALWAYS
        :param bracket_same_line: (experimental) Put > of opening tags on the last line instead of on a new line. Default: false
        :param bracket_spacing: (experimental) Print spaces between brackets. Default: true
        :param cursor_offset: (experimental) Print (to stderr) where a cursor at the given position would move to after formatting. This option cannot be used with --range-start and --range-end. Default: -1
        :param embedded_language_formatting: (experimental) Control how Prettier formats quoted code embedded in the file. Default: EmbeddedLanguageFormatting.AUTO
        :param end_of_line: (experimental) Which end of line characters to apply. Default: EndOfLine.LF
        :param filepath: (experimental) Specify the input filepath. This will be used to do parser inference. Default: none
        :param html_whitespace_sensitivity: (experimental) How to handle whitespaces in HTML. Default: HTMLWhitespaceSensitivity.CSS
        :param insert_pragma: (experimental) Insert. Default: false
        :param jsx_single_quote: (experimental) Use single quotes in JSX. Default: false
        :param parser: (experimental) Which parser to use. Default: - Prettier automatically infers the parser from the input file path, so you shouldn’t have to change this setting.
        :param plugins: (experimental) Add a plugin. Multiple plugins can be passed as separate ``--plugin``s. Default: []
        :param plugin_search_dirs: (experimental) Custom directory that contains prettier plugins in node_modules subdirectory. Overrides default behavior when plugins are searched relatively to the location of Prettier. Multiple values are accepted. Default: []
        :param print_width: (experimental) The line length where Prettier will try wrap. Default: 80
        :param prose_wrap: (experimental) How to wrap prose. Default: ProseWrap.PRESERVE
        :param quote_props: (experimental) Change when properties in objects are quoted. Default: QuoteProps.ASNEEDED
        :param range_end: (experimental) Format code ending at a given character offset (exclusive). The range will extend forwards to the end of the selected statement. This option cannot be used with --cursor-offset. Default: null
        :param range_start: (experimental) Format code starting at a given character offset. The range will extend backwards to the start of the first line containing the selected statement. This option cannot be used with --cursor-offset. Default: 0
        :param require_pragma: (experimental) Require either '@prettier' or '@format' to be present in the file's first docblock comment in order for it to be formatted. Default: false
        :param semi: (experimental) Print semicolons. Default: true
        :param single_quote: (experimental) Use single quotes instead of double quotes. Default: false
        :param tab_width: (experimental) Number of spaces per indentation level. Default: 2
        :param trailing_comma: (experimental) Print trailing commas wherever possible when multi-line. Default: TrailingComma.ES5
        :param use_tabs: (experimental) Indent with tabs instead of spaces. Default: false
        :param vue_indent_script_and_style: (experimental) Indent script and style tags in Vue files. Default: false

        :see: https://prettier.io/docs/en/options.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__887661cb2874a1d4a18112ca0d8607d9340a20c3becbf5d16df966a4dfda6434)
            check_type(argname="argument arrow_parens", value=arrow_parens, expected_type=type_hints["arrow_parens"])
            check_type(argname="argument bracket_same_line", value=bracket_same_line, expected_type=type_hints["bracket_same_line"])
            check_type(argname="argument bracket_spacing", value=bracket_spacing, expected_type=type_hints["bracket_spacing"])
            check_type(argname="argument cursor_offset", value=cursor_offset, expected_type=type_hints["cursor_offset"])
            check_type(argname="argument embedded_language_formatting", value=embedded_language_formatting, expected_type=type_hints["embedded_language_formatting"])
            check_type(argname="argument end_of_line", value=end_of_line, expected_type=type_hints["end_of_line"])
            check_type(argname="argument filepath", value=filepath, expected_type=type_hints["filepath"])
            check_type(argname="argument html_whitespace_sensitivity", value=html_whitespace_sensitivity, expected_type=type_hints["html_whitespace_sensitivity"])
            check_type(argname="argument insert_pragma", value=insert_pragma, expected_type=type_hints["insert_pragma"])
            check_type(argname="argument jsx_single_quote", value=jsx_single_quote, expected_type=type_hints["jsx_single_quote"])
            check_type(argname="argument parser", value=parser, expected_type=type_hints["parser"])
            check_type(argname="argument plugins", value=plugins, expected_type=type_hints["plugins"])
            check_type(argname="argument plugin_search_dirs", value=plugin_search_dirs, expected_type=type_hints["plugin_search_dirs"])
            check_type(argname="argument print_width", value=print_width, expected_type=type_hints["print_width"])
            check_type(argname="argument prose_wrap", value=prose_wrap, expected_type=type_hints["prose_wrap"])
            check_type(argname="argument quote_props", value=quote_props, expected_type=type_hints["quote_props"])
            check_type(argname="argument range_end", value=range_end, expected_type=type_hints["range_end"])
            check_type(argname="argument range_start", value=range_start, expected_type=type_hints["range_start"])
            check_type(argname="argument require_pragma", value=require_pragma, expected_type=type_hints["require_pragma"])
            check_type(argname="argument semi", value=semi, expected_type=type_hints["semi"])
            check_type(argname="argument single_quote", value=single_quote, expected_type=type_hints["single_quote"])
            check_type(argname="argument tab_width", value=tab_width, expected_type=type_hints["tab_width"])
            check_type(argname="argument trailing_comma", value=trailing_comma, expected_type=type_hints["trailing_comma"])
            check_type(argname="argument use_tabs", value=use_tabs, expected_type=type_hints["use_tabs"])
            check_type(argname="argument vue_indent_script_and_style", value=vue_indent_script_and_style, expected_type=type_hints["vue_indent_script_and_style"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arrow_parens is not None:
            self._values["arrow_parens"] = arrow_parens
        if bracket_same_line is not None:
            self._values["bracket_same_line"] = bracket_same_line
        if bracket_spacing is not None:
            self._values["bracket_spacing"] = bracket_spacing
        if cursor_offset is not None:
            self._values["cursor_offset"] = cursor_offset
        if embedded_language_formatting is not None:
            self._values["embedded_language_formatting"] = embedded_language_formatting
        if end_of_line is not None:
            self._values["end_of_line"] = end_of_line
        if filepath is not None:
            self._values["filepath"] = filepath
        if html_whitespace_sensitivity is not None:
            self._values["html_whitespace_sensitivity"] = html_whitespace_sensitivity
        if insert_pragma is not None:
            self._values["insert_pragma"] = insert_pragma
        if jsx_single_quote is not None:
            self._values["jsx_single_quote"] = jsx_single_quote
        if parser is not None:
            self._values["parser"] = parser
        if plugins is not None:
            self._values["plugins"] = plugins
        if plugin_search_dirs is not None:
            self._values["plugin_search_dirs"] = plugin_search_dirs
        if print_width is not None:
            self._values["print_width"] = print_width
        if prose_wrap is not None:
            self._values["prose_wrap"] = prose_wrap
        if quote_props is not None:
            self._values["quote_props"] = quote_props
        if range_end is not None:
            self._values["range_end"] = range_end
        if range_start is not None:
            self._values["range_start"] = range_start
        if require_pragma is not None:
            self._values["require_pragma"] = require_pragma
        if semi is not None:
            self._values["semi"] = semi
        if single_quote is not None:
            self._values["single_quote"] = single_quote
        if tab_width is not None:
            self._values["tab_width"] = tab_width
        if trailing_comma is not None:
            self._values["trailing_comma"] = trailing_comma
        if use_tabs is not None:
            self._values["use_tabs"] = use_tabs
        if vue_indent_script_and_style is not None:
            self._values["vue_indent_script_and_style"] = vue_indent_script_and_style

    @builtins.property
    def arrow_parens(self) -> typing.Optional[ArrowParens]:
        '''(experimental) Include parentheses around a sole arrow function parameter.

        :default: ArrowParens.ALWAYS

        :stability: experimental
        '''
        result = self._values.get("arrow_parens")
        return typing.cast(typing.Optional[ArrowParens], result)

    @builtins.property
    def bracket_same_line(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Put > of opening tags on the last line instead of on a new line.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("bracket_same_line")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Print spaces between brackets.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("bracket_spacing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cursor_offset(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Print (to stderr) where a cursor at the given position would move to after formatting.

        This option cannot be used with --range-start and --range-end.

        :default: -1

        :stability: experimental
        '''
        result = self._values.get("cursor_offset")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def embedded_language_formatting(
        self,
    ) -> typing.Optional[EmbeddedLanguageFormatting]:
        '''(experimental) Control how Prettier formats quoted code embedded in the file.

        :default: EmbeddedLanguageFormatting.AUTO

        :stability: experimental
        '''
        result = self._values.get("embedded_language_formatting")
        return typing.cast(typing.Optional[EmbeddedLanguageFormatting], result)

    @builtins.property
    def end_of_line(self) -> typing.Optional[EndOfLine]:
        '''(experimental) Which end of line characters to apply.

        :default: EndOfLine.LF

        :stability: experimental
        '''
        result = self._values.get("end_of_line")
        return typing.cast(typing.Optional[EndOfLine], result)

    @builtins.property
    def filepath(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specify the input filepath.

        This will be used to do parser inference.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("filepath")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def html_whitespace_sensitivity(self) -> typing.Optional[HTMLWhitespaceSensitivity]:
        '''(experimental) How to handle whitespaces in HTML.

        :default: HTMLWhitespaceSensitivity.CSS

        :stability: experimental
        '''
        result = self._values.get("html_whitespace_sensitivity")
        return typing.cast(typing.Optional[HTMLWhitespaceSensitivity], result)

    @builtins.property
    def insert_pragma(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Insert.

        :default: false

        :stability: experimental
        :format: pragma into file's first docblock comment.
        '''
        result = self._values.get("insert_pragma")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def jsx_single_quote(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use single quotes in JSX.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("jsx_single_quote")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def parser(self) -> typing.Optional[builtins.str]:
        '''(experimental) Which parser to use.

        :default: - Prettier automatically infers the parser from the input file path, so you shouldn’t have to change this setting.

        :stability: experimental
        '''
        result = self._values.get("parser")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Add a plugin.

        Multiple plugins can be passed as separate ``--plugin``s.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("plugins")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def plugin_search_dirs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Custom directory that contains prettier plugins in node_modules subdirectory.

        Overrides default behavior when plugins are searched relatively to the location of
        Prettier.
        Multiple values are accepted.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("plugin_search_dirs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def print_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The line length where Prettier will try wrap.

        :default: 80

        :stability: experimental
        '''
        result = self._values.get("print_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def prose_wrap(self) -> typing.Optional["ProseWrap"]:
        '''(experimental) How to wrap prose.

        :default: ProseWrap.PRESERVE

        :stability: experimental
        '''
        result = self._values.get("prose_wrap")
        return typing.cast(typing.Optional["ProseWrap"], result)

    @builtins.property
    def quote_props(self) -> typing.Optional["QuoteProps"]:
        '''(experimental) Change when properties in objects are quoted.

        :default: QuoteProps.ASNEEDED

        :stability: experimental
        '''
        result = self._values.get("quote_props")
        return typing.cast(typing.Optional["QuoteProps"], result)

    @builtins.property
    def range_end(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Format code ending at a given character offset (exclusive).

        The range will extend forwards to the end of the selected statement.
        This option cannot be used with --cursor-offset.

        :default: null

        :stability: experimental
        '''
        result = self._values.get("range_end")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def range_start(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Format code starting at a given character offset.

        The range will extend backwards to the start of the first line containing the selected
        statement.
        This option cannot be used with --cursor-offset.

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("range_start")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def require_pragma(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Require either '@prettier' or '@format' to be present in the file's first docblock comment in order for it to be formatted.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("require_pragma")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def semi(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Print semicolons.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("semi")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def single_quote(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use single quotes instead of double quotes.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("single_quote")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tab_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Number of spaces per indentation level.

        :default: 2

        :stability: experimental
        '''
        result = self._values.get("tab_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def trailing_comma(self) -> typing.Optional["TrailingComma"]:
        '''(experimental) Print trailing commas wherever possible when multi-line.

        :default: TrailingComma.ES5

        :stability: experimental
        '''
        result = self._values.get("trailing_comma")
        return typing.cast(typing.Optional["TrailingComma"], result)

    @builtins.property
    def use_tabs(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indent with tabs instead of spaces.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("use_tabs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vue_indent_script_and_style(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indent script and style tags in Vue files.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("vue_indent_script_and_style")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrettierSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Projenrc(
    _ProjenrcFile_50432c7e,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.javascript.Projenrc",
):
    '''(experimental) Sets up a javascript project to use TypeScript for projenrc.

    :stability: experimental
    '''

    def __init__(
        self,
        project: _Project_57d89203,
        *,
        filename: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param filename: (experimental) The name of the projenrc file. Default: ".projenrc.js"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aaddb790f6b7d088afb273f85e8c279374e3017865fb4c91b0780864fb6e306)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = ProjenrcOptions(filename=filename)

        jsii.create(self.__class__, self, [project, options])

    @jsii.member(jsii_name="preSynthesize")
    def pre_synthesize(self) -> None:
        '''(experimental) Called before synthesis.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "preSynthesize", []))

    @builtins.property
    @jsii.member(jsii_name="filePath")
    def file_path(self) -> builtins.str:
        '''(experimental) The path of the projenrc file.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "filePath"))


@jsii.data_type(
    jsii_type="projen.javascript.ProjenrcOptions",
    jsii_struct_bases=[],
    name_mapping={"filename": "filename"},
)
class ProjenrcOptions:
    def __init__(self, *, filename: typing.Optional[builtins.str] = None) -> None:
        '''
        :param filename: (experimental) The name of the projenrc file. Default: ".projenrc.js"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c3b878e5a2d5b01df88ea94af1a0f3f101f4340d3dba514d5e748ef2f199f6)
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filename is not None:
            self._values["filename"] = filename

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the projenrc file.

        :default: ".projenrc.js"

        :stability: experimental
        '''
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjenrcOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.ProseWrap")
class ProseWrap(enum.Enum):
    '''
    :stability: experimental
    '''

    ALWAYS = "ALWAYS"
    '''(experimental) Wrap prose if it exceeds the print width.

    :stability: experimental
    '''
    NEVER = "NEVER"
    '''(experimental) Do not wrap prose.

    :stability: experimental
    '''
    PRESERVE = "PRESERVE"
    '''(experimental) Wrap prose as-is.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.javascript.QuoteProps")
class QuoteProps(enum.Enum):
    '''
    :stability: experimental
    '''

    ASNEEDED = "ASNEEDED"
    '''(experimental) Only add quotes around object properties where required.

    :stability: experimental
    '''
    CONSISTENT = "CONSISTENT"
    '''(experimental) If at least one property in an object requires quotes, quote all properties.

    :stability: experimental
    '''
    PRESERVE = "PRESERVE"
    '''(experimental) Respect the input use of quotes in object properties.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.javascript.RenderWorkflowSetupOptions",
    jsii_struct_bases=[],
    name_mapping={"mutable": "mutable"},
)
class RenderWorkflowSetupOptions:
    def __init__(self, *, mutable: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Options for ``renderInstallSteps()``.

        :param mutable: (experimental) Should the pacakge lockfile be updated? Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7894334d4e6bef30e70628d87bf6b8f27ab4cf85a14e93ed26d04abcba1356d)
            check_type(argname="argument mutable", value=mutable, expected_type=type_hints["mutable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mutable is not None:
            self._values["mutable"] = mutable

    @builtins.property
    def mutable(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Should the pacakge lockfile be updated?

        :default: false

        :stability: experimental
        '''
        result = self._values.get("mutable")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderWorkflowSetupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.ScopedPackagesOptions",
    jsii_struct_bases=[],
    name_mapping={"registry_url": "registryUrl", "scope": "scope"},
)
class ScopedPackagesOptions:
    def __init__(self, *, registry_url: builtins.str, scope: builtins.str) -> None:
        '''(experimental) Options for scoped packages.

        :param registry_url: (experimental) URL of the registry for scoped packages.
        :param scope: (experimental) Scope of the packages.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c6e79d2b5de89d5ea21ca58635c0e3f3ed941e2f5533f9365aca8c6bac689e)
            check_type(argname="argument registry_url", value=registry_url, expected_type=type_hints["registry_url"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "registry_url": registry_url,
            "scope": scope,
        }

    @builtins.property
    def registry_url(self) -> builtins.str:
        '''(experimental) URL of the registry for scoped packages.

        :stability: experimental
        '''
        result = self._values.get("registry_url")
        assert result is not None, "Required property 'registry_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> builtins.str:
        '''(experimental) Scope of the packages.

        :stability: experimental

        Example::

            "@angular"
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScopedPackagesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.TrailingComma")
class TrailingComma(enum.Enum):
    '''
    :stability: experimental
    '''

    ALL = "ALL"
    '''(experimental) Trailing commas wherever possible (including function arguments).

    :stability: experimental
    '''
    ES5 = "ES5"
    '''(experimental) Trailing commas where valid in ES5 (objects, arrays, etc.).

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) No trailing commas.

    :stability: experimental
    '''


class Transform(metaclass=jsii.JSIIMeta, jsii_type="projen.javascript.Transform"):
    '''
    :stability: experimental
    '''

    def __init__(self, name: builtins.str, options: typing.Any = None) -> None:
        '''
        :param name: -
        :param options: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b434df824fd38c8bd7ed7eb8a8cf4f2f0559fd4c13a28bd06bd0f481c6389984)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
        jsii.create(self.__class__, self, [name, options])


@jsii.data_type(
    jsii_type="projen.javascript.TypeScriptCompilerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "allow_arbitrary_extensions": "allowArbitraryExtensions",
        "allow_importing_ts_extensions": "allowImportingTsExtensions",
        "allow_js": "allowJs",
        "allow_synthetic_default_imports": "allowSyntheticDefaultImports",
        "always_strict": "alwaysStrict",
        "base_url": "baseUrl",
        "custom_conditions": "customConditions",
        "declaration": "declaration",
        "declaration_dir": "declarationDir",
        "emit_declaration_only": "emitDeclarationOnly",
        "emit_decorator_metadata": "emitDecoratorMetadata",
        "es_module_interop": "esModuleInterop",
        "exact_optional_property_types": "exactOptionalPropertyTypes",
        "experimental_decorators": "experimentalDecorators",
        "force_consistent_casing_in_file_names": "forceConsistentCasingInFileNames",
        "imports_not_used_as_values": "importsNotUsedAsValues",
        "inline_source_map": "inlineSourceMap",
        "inline_sources": "inlineSources",
        "isolated_modules": "isolatedModules",
        "jsx": "jsx",
        "jsx_import_source": "jsxImportSource",
        "lib": "lib",
        "module": "module",
        "module_resolution": "moduleResolution",
        "no_emit": "noEmit",
        "no_emit_on_error": "noEmitOnError",
        "no_fallthrough_cases_in_switch": "noFallthroughCasesInSwitch",
        "no_implicit_any": "noImplicitAny",
        "no_implicit_override": "noImplicitOverride",
        "no_implicit_returns": "noImplicitReturns",
        "no_implicit_this": "noImplicitThis",
        "no_property_access_from_index_signature": "noPropertyAccessFromIndexSignature",
        "no_unchecked_indexed_access": "noUncheckedIndexedAccess",
        "no_unused_locals": "noUnusedLocals",
        "no_unused_parameters": "noUnusedParameters",
        "out_dir": "outDir",
        "paths": "paths",
        "resolve_json_module": "resolveJsonModule",
        "resolve_package_json_exports": "resolvePackageJsonExports",
        "resolve_package_json_imports": "resolvePackageJsonImports",
        "root_dir": "rootDir",
        "skip_lib_check": "skipLibCheck",
        "source_map": "sourceMap",
        "source_root": "sourceRoot",
        "strict": "strict",
        "strict_null_checks": "strictNullChecks",
        "strict_property_initialization": "strictPropertyInitialization",
        "strip_internal": "stripInternal",
        "target": "target",
        "use_unknown_in_catch_variables": "useUnknownInCatchVariables",
        "verbatim_module_syntax": "verbatimModuleSyntax",
    },
)
class TypeScriptCompilerOptions:
    def __init__(
        self,
        *,
        allow_arbitrary_extensions: typing.Optional[builtins.bool] = None,
        allow_importing_ts_extensions: typing.Optional[builtins.bool] = None,
        allow_js: typing.Optional[builtins.bool] = None,
        allow_synthetic_default_imports: typing.Optional[builtins.bool] = None,
        always_strict: typing.Optional[builtins.bool] = None,
        base_url: typing.Optional[builtins.str] = None,
        custom_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
        declaration: typing.Optional[builtins.bool] = None,
        declaration_dir: typing.Optional[builtins.str] = None,
        emit_declaration_only: typing.Optional[builtins.bool] = None,
        emit_decorator_metadata: typing.Optional[builtins.bool] = None,
        es_module_interop: typing.Optional[builtins.bool] = None,
        exact_optional_property_types: typing.Optional[builtins.bool] = None,
        experimental_decorators: typing.Optional[builtins.bool] = None,
        force_consistent_casing_in_file_names: typing.Optional[builtins.bool] = None,
        imports_not_used_as_values: typing.Optional["TypeScriptImportsNotUsedAsValues"] = None,
        inline_source_map: typing.Optional[builtins.bool] = None,
        inline_sources: typing.Optional[builtins.bool] = None,
        isolated_modules: typing.Optional[builtins.bool] = None,
        jsx: typing.Optional["TypeScriptJsxMode"] = None,
        jsx_import_source: typing.Optional[builtins.str] = None,
        lib: typing.Optional[typing.Sequence[builtins.str]] = None,
        module: typing.Optional[builtins.str] = None,
        module_resolution: typing.Optional["TypeScriptModuleResolution"] = None,
        no_emit: typing.Optional[builtins.bool] = None,
        no_emit_on_error: typing.Optional[builtins.bool] = None,
        no_fallthrough_cases_in_switch: typing.Optional[builtins.bool] = None,
        no_implicit_any: typing.Optional[builtins.bool] = None,
        no_implicit_override: typing.Optional[builtins.bool] = None,
        no_implicit_returns: typing.Optional[builtins.bool] = None,
        no_implicit_this: typing.Optional[builtins.bool] = None,
        no_property_access_from_index_signature: typing.Optional[builtins.bool] = None,
        no_unchecked_indexed_access: typing.Optional[builtins.bool] = None,
        no_unused_locals: typing.Optional[builtins.bool] = None,
        no_unused_parameters: typing.Optional[builtins.bool] = None,
        out_dir: typing.Optional[builtins.str] = None,
        paths: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
        resolve_json_module: typing.Optional[builtins.bool] = None,
        resolve_package_json_exports: typing.Optional[builtins.bool] = None,
        resolve_package_json_imports: typing.Optional[builtins.bool] = None,
        root_dir: typing.Optional[builtins.str] = None,
        skip_lib_check: typing.Optional[builtins.bool] = None,
        source_map: typing.Optional[builtins.bool] = None,
        source_root: typing.Optional[builtins.str] = None,
        strict: typing.Optional[builtins.bool] = None,
        strict_null_checks: typing.Optional[builtins.bool] = None,
        strict_property_initialization: typing.Optional[builtins.bool] = None,
        strip_internal: typing.Optional[builtins.bool] = None,
        target: typing.Optional[builtins.str] = None,
        use_unknown_in_catch_variables: typing.Optional[builtins.bool] = None,
        verbatim_module_syntax: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param allow_arbitrary_extensions: (experimental) Suppress arbitrary extension import errors with the assumption that a bundler will be handling it. Default: undefined
        :param allow_importing_ts_extensions: (experimental) Allows TypeScript files to import each other with TypeScript-specific extensions (``.ts``, ``.mts``, ``.tsx``). Requires ``noEmit`` or ``emitDeclarationOnly``. Default: undefined
        :param allow_js: (experimental) Allow JavaScript files to be compiled. Default: false
        :param allow_synthetic_default_imports: (experimental) Allow default imports from modules with no default export. This does not affect code emit, just typechecking.
        :param always_strict: (experimental) Ensures that your files are parsed in the ECMAScript strict mode, and emit “use strict” for each source file. Default: true
        :param base_url: (experimental) Lets you set a base directory to resolve non-absolute module names. You can define a root folder where you can do absolute file resolution.
        :param custom_conditions: (experimental) List of additional conditions that should succeed when TypeScript resolves from an ``exports`` or ``imports`` field of a ``package.json``. Default: undefined
        :param declaration: (experimental) To be specified along with the above.
        :param declaration_dir: (experimental) Offers a way to configure the root directory for where declaration files are emitted.
        :param emit_declaration_only: (experimental) Only emit .d.ts files; do not emit .js files. Default: false
        :param emit_decorator_metadata: (experimental) Enables experimental support for decorators, which is in stage 2 of the TC39 standardization process. Decorators are a language feature which hasn’t yet been fully ratified into the JavaScript specification. This means that the implementation version in TypeScript may differ from the implementation in JavaScript when it it decided by TC39. You can find out more about decorator support in TypeScript in the handbook. Default: undefined
        :param es_module_interop: (experimental) Emit __importStar and __importDefault helpers for runtime babel ecosystem compatibility and enable --allowSyntheticDefaultImports for typesystem compatibility. Default: false
        :param exact_optional_property_types: (experimental) Specifies that optional property types should be interpreted exactly as written, meaning that ``| undefined`` is not added to the type Available with TypeScript 4.4 and newer. Default: false
        :param experimental_decorators: (experimental) Enables experimental support for decorators, which is in stage 2 of the TC39 standardization process. Default: true
        :param force_consistent_casing_in_file_names: (experimental) Disallow inconsistently-cased references to the same file. Default: false
        :param imports_not_used_as_values: (experimental) This flag works because you can use ``import type`` to explicitly create an ``import`` statement which should never be emitted into JavaScript. Default: "remove"
        :param inline_source_map: (experimental) When set, instead of writing out a .js.map file to provide source maps, TypeScript will embed the source map content in the .js files. Default: true
        :param inline_sources: (experimental) When set, TypeScript will include the original content of the .ts file as an embedded string in the source map. This is often useful in the same cases as inlineSourceMap. Default: true
        :param isolated_modules: (experimental) Perform additional checks to ensure that separate compilation (such as with transpileModule or. Default: false
        :param jsx: (experimental) Support JSX in .tsx files: "react", "preserve", "react-native" etc. Default: undefined
        :param jsx_import_source: (experimental) Declares the module specifier to be used for importing the jsx and jsxs factory functions when using jsx. Default: undefined
        :param lib: (experimental) Reference for type definitions / libraries to use (eg. ES2016, ES5, ES2018). Default: [ "es2018" ]
        :param module: (experimental) Sets the module system for the program. See https://www.typescriptlang.org/docs/handbook/modules.html#ambient-modules. Default: "CommonJS"
        :param module_resolution: (experimental) Determine how modules get resolved. Either "Node" for Node.js/io.js style resolution, or "Classic". Default: "node"
        :param no_emit: (experimental) Do not emit outputs. Default: false
        :param no_emit_on_error: (experimental) Do not emit compiler output files like JavaScript source code, source-maps or declarations if any errors were reported. Default: true
        :param no_fallthrough_cases_in_switch: (experimental) Report errors for fallthrough cases in switch statements. Ensures that any non-empty case inside a switch statement includes either break or return. This means you won’t accidentally ship a case fallthrough bug. Default: true
        :param no_implicit_any: (experimental) In some cases where no type annotations are present, TypeScript will fall back to a type of any for a variable when it cannot infer the type. Default: true
        :param no_implicit_override: (experimental) Using ``noImplicitOverride``, you can ensure that sub-classes never go out of sync as they are required to explicitly declare that they are overriding a member using the ``override`` keyword. This also improves readability of the programmer's intent. Available with TypeScript 4.3 and newer. Default: false
        :param no_implicit_returns: (experimental) When enabled, TypeScript will check all code paths in a function to ensure they return a value. Default: true
        :param no_implicit_this: (experimental) Raise error on ‘this’ expressions with an implied ‘any’ type. Default: true
        :param no_property_access_from_index_signature: (experimental) Raise error on use of the dot syntax to access fields which are not defined. Default: true
        :param no_unchecked_indexed_access: (experimental) Raise error when accessing indexes on objects with unknown keys defined in index signatures. Default: true
        :param no_unused_locals: (experimental) Report errors on unused local variables. Default: true
        :param no_unused_parameters: (experimental) Report errors on unused parameters in functions. Default: true
        :param out_dir: (experimental) Output directory for the compiled files.
        :param paths: (experimental) A series of entries which re-map imports to lookup locations relative to the baseUrl, there is a larger coverage of paths in the handbook. paths lets you declare how TypeScript should resolve an import in your require/imports.
        :param resolve_json_module: (experimental) Allows importing modules with a ‘.json’ extension, which is a common practice in node projects. This includes generating a type for the import based on the static JSON shape. Default: true
        :param resolve_package_json_exports: (experimental) Forces TypeScript to consult the ``exports`` field of ``package.json`` files if it ever reads from a package in ``node_modules``. Default: true
        :param resolve_package_json_imports: (experimental) Forces TypeScript to consult the ``imports`` field of ``package.json`` when performing a lookup that begins with ``#`` from a file that has a ``package.json`` as an ancestor. Default: undefined
        :param root_dir: (experimental) Specifies the root directory of input files. Only use to control the output directory structure with ``outDir``.
        :param skip_lib_check: (experimental) Skip type checking of all declaration files (*.d.ts). Default: false
        :param source_map: (experimental) Enables the generation of sourcemap files. Default: undefined
        :param source_root: (experimental) Specify the location where a debugger should locate TypeScript files instead of relative source locations. Default: undefined
        :param strict: (experimental) The strict flag enables a wide range of type checking behavior that results in stronger guarantees of program correctness. Turning this on is equivalent to enabling all of the strict mode family options, which are outlined below. You can then turn off individual strict mode family checks as needed. Default: true
        :param strict_null_checks: (experimental) When strictNullChecks is false, null and undefined are effectively ignored by the language. This can lead to unexpected errors at runtime. When strictNullChecks is true, null and undefined have their own distinct types and you’ll get a type error if you try to use them where a concrete value is expected. Default: true
        :param strict_property_initialization: (experimental) When set to true, TypeScript will raise an error when a class property was declared but not set in the constructor. Default: true
        :param strip_internal: (experimental) Do not emit declarations for code that has an ``@internal`` annotation in it’s JSDoc comment. Default: true
        :param target: (experimental) Modern browsers support all ES6 features, so ES6 is a good choice. You might choose to set a lower target if your code is deployed to older environments, or a higher target if your code is guaranteed to run in newer environments. Default: "ES2018"
        :param use_unknown_in_catch_variables: (experimental) Change the type of the variable in a catch clause from any to unknown Available with TypeScript 4.4 and newer. Default: true
        :param verbatim_module_syntax: (experimental) Simplifies TypeScript's handling of import/export ``type`` modifiers. Default: undefined

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3368fe3a3107764de1a64c16f7fe4c15d510477a888b2a74df2afb14b632c7e)
            check_type(argname="argument allow_arbitrary_extensions", value=allow_arbitrary_extensions, expected_type=type_hints["allow_arbitrary_extensions"])
            check_type(argname="argument allow_importing_ts_extensions", value=allow_importing_ts_extensions, expected_type=type_hints["allow_importing_ts_extensions"])
            check_type(argname="argument allow_js", value=allow_js, expected_type=type_hints["allow_js"])
            check_type(argname="argument allow_synthetic_default_imports", value=allow_synthetic_default_imports, expected_type=type_hints["allow_synthetic_default_imports"])
            check_type(argname="argument always_strict", value=always_strict, expected_type=type_hints["always_strict"])
            check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            check_type(argname="argument custom_conditions", value=custom_conditions, expected_type=type_hints["custom_conditions"])
            check_type(argname="argument declaration", value=declaration, expected_type=type_hints["declaration"])
            check_type(argname="argument declaration_dir", value=declaration_dir, expected_type=type_hints["declaration_dir"])
            check_type(argname="argument emit_declaration_only", value=emit_declaration_only, expected_type=type_hints["emit_declaration_only"])
            check_type(argname="argument emit_decorator_metadata", value=emit_decorator_metadata, expected_type=type_hints["emit_decorator_metadata"])
            check_type(argname="argument es_module_interop", value=es_module_interop, expected_type=type_hints["es_module_interop"])
            check_type(argname="argument exact_optional_property_types", value=exact_optional_property_types, expected_type=type_hints["exact_optional_property_types"])
            check_type(argname="argument experimental_decorators", value=experimental_decorators, expected_type=type_hints["experimental_decorators"])
            check_type(argname="argument force_consistent_casing_in_file_names", value=force_consistent_casing_in_file_names, expected_type=type_hints["force_consistent_casing_in_file_names"])
            check_type(argname="argument imports_not_used_as_values", value=imports_not_used_as_values, expected_type=type_hints["imports_not_used_as_values"])
            check_type(argname="argument inline_source_map", value=inline_source_map, expected_type=type_hints["inline_source_map"])
            check_type(argname="argument inline_sources", value=inline_sources, expected_type=type_hints["inline_sources"])
            check_type(argname="argument isolated_modules", value=isolated_modules, expected_type=type_hints["isolated_modules"])
            check_type(argname="argument jsx", value=jsx, expected_type=type_hints["jsx"])
            check_type(argname="argument jsx_import_source", value=jsx_import_source, expected_type=type_hints["jsx_import_source"])
            check_type(argname="argument lib", value=lib, expected_type=type_hints["lib"])
            check_type(argname="argument module", value=module, expected_type=type_hints["module"])
            check_type(argname="argument module_resolution", value=module_resolution, expected_type=type_hints["module_resolution"])
            check_type(argname="argument no_emit", value=no_emit, expected_type=type_hints["no_emit"])
            check_type(argname="argument no_emit_on_error", value=no_emit_on_error, expected_type=type_hints["no_emit_on_error"])
            check_type(argname="argument no_fallthrough_cases_in_switch", value=no_fallthrough_cases_in_switch, expected_type=type_hints["no_fallthrough_cases_in_switch"])
            check_type(argname="argument no_implicit_any", value=no_implicit_any, expected_type=type_hints["no_implicit_any"])
            check_type(argname="argument no_implicit_override", value=no_implicit_override, expected_type=type_hints["no_implicit_override"])
            check_type(argname="argument no_implicit_returns", value=no_implicit_returns, expected_type=type_hints["no_implicit_returns"])
            check_type(argname="argument no_implicit_this", value=no_implicit_this, expected_type=type_hints["no_implicit_this"])
            check_type(argname="argument no_property_access_from_index_signature", value=no_property_access_from_index_signature, expected_type=type_hints["no_property_access_from_index_signature"])
            check_type(argname="argument no_unchecked_indexed_access", value=no_unchecked_indexed_access, expected_type=type_hints["no_unchecked_indexed_access"])
            check_type(argname="argument no_unused_locals", value=no_unused_locals, expected_type=type_hints["no_unused_locals"])
            check_type(argname="argument no_unused_parameters", value=no_unused_parameters, expected_type=type_hints["no_unused_parameters"])
            check_type(argname="argument out_dir", value=out_dir, expected_type=type_hints["out_dir"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument resolve_json_module", value=resolve_json_module, expected_type=type_hints["resolve_json_module"])
            check_type(argname="argument resolve_package_json_exports", value=resolve_package_json_exports, expected_type=type_hints["resolve_package_json_exports"])
            check_type(argname="argument resolve_package_json_imports", value=resolve_package_json_imports, expected_type=type_hints["resolve_package_json_imports"])
            check_type(argname="argument root_dir", value=root_dir, expected_type=type_hints["root_dir"])
            check_type(argname="argument skip_lib_check", value=skip_lib_check, expected_type=type_hints["skip_lib_check"])
            check_type(argname="argument source_map", value=source_map, expected_type=type_hints["source_map"])
            check_type(argname="argument source_root", value=source_root, expected_type=type_hints["source_root"])
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
            check_type(argname="argument strict_null_checks", value=strict_null_checks, expected_type=type_hints["strict_null_checks"])
            check_type(argname="argument strict_property_initialization", value=strict_property_initialization, expected_type=type_hints["strict_property_initialization"])
            check_type(argname="argument strip_internal", value=strip_internal, expected_type=type_hints["strip_internal"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument use_unknown_in_catch_variables", value=use_unknown_in_catch_variables, expected_type=type_hints["use_unknown_in_catch_variables"])
            check_type(argname="argument verbatim_module_syntax", value=verbatim_module_syntax, expected_type=type_hints["verbatim_module_syntax"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_arbitrary_extensions is not None:
            self._values["allow_arbitrary_extensions"] = allow_arbitrary_extensions
        if allow_importing_ts_extensions is not None:
            self._values["allow_importing_ts_extensions"] = allow_importing_ts_extensions
        if allow_js is not None:
            self._values["allow_js"] = allow_js
        if allow_synthetic_default_imports is not None:
            self._values["allow_synthetic_default_imports"] = allow_synthetic_default_imports
        if always_strict is not None:
            self._values["always_strict"] = always_strict
        if base_url is not None:
            self._values["base_url"] = base_url
        if custom_conditions is not None:
            self._values["custom_conditions"] = custom_conditions
        if declaration is not None:
            self._values["declaration"] = declaration
        if declaration_dir is not None:
            self._values["declaration_dir"] = declaration_dir
        if emit_declaration_only is not None:
            self._values["emit_declaration_only"] = emit_declaration_only
        if emit_decorator_metadata is not None:
            self._values["emit_decorator_metadata"] = emit_decorator_metadata
        if es_module_interop is not None:
            self._values["es_module_interop"] = es_module_interop
        if exact_optional_property_types is not None:
            self._values["exact_optional_property_types"] = exact_optional_property_types
        if experimental_decorators is not None:
            self._values["experimental_decorators"] = experimental_decorators
        if force_consistent_casing_in_file_names is not None:
            self._values["force_consistent_casing_in_file_names"] = force_consistent_casing_in_file_names
        if imports_not_used_as_values is not None:
            self._values["imports_not_used_as_values"] = imports_not_used_as_values
        if inline_source_map is not None:
            self._values["inline_source_map"] = inline_source_map
        if inline_sources is not None:
            self._values["inline_sources"] = inline_sources
        if isolated_modules is not None:
            self._values["isolated_modules"] = isolated_modules
        if jsx is not None:
            self._values["jsx"] = jsx
        if jsx_import_source is not None:
            self._values["jsx_import_source"] = jsx_import_source
        if lib is not None:
            self._values["lib"] = lib
        if module is not None:
            self._values["module"] = module
        if module_resolution is not None:
            self._values["module_resolution"] = module_resolution
        if no_emit is not None:
            self._values["no_emit"] = no_emit
        if no_emit_on_error is not None:
            self._values["no_emit_on_error"] = no_emit_on_error
        if no_fallthrough_cases_in_switch is not None:
            self._values["no_fallthrough_cases_in_switch"] = no_fallthrough_cases_in_switch
        if no_implicit_any is not None:
            self._values["no_implicit_any"] = no_implicit_any
        if no_implicit_override is not None:
            self._values["no_implicit_override"] = no_implicit_override
        if no_implicit_returns is not None:
            self._values["no_implicit_returns"] = no_implicit_returns
        if no_implicit_this is not None:
            self._values["no_implicit_this"] = no_implicit_this
        if no_property_access_from_index_signature is not None:
            self._values["no_property_access_from_index_signature"] = no_property_access_from_index_signature
        if no_unchecked_indexed_access is not None:
            self._values["no_unchecked_indexed_access"] = no_unchecked_indexed_access
        if no_unused_locals is not None:
            self._values["no_unused_locals"] = no_unused_locals
        if no_unused_parameters is not None:
            self._values["no_unused_parameters"] = no_unused_parameters
        if out_dir is not None:
            self._values["out_dir"] = out_dir
        if paths is not None:
            self._values["paths"] = paths
        if resolve_json_module is not None:
            self._values["resolve_json_module"] = resolve_json_module
        if resolve_package_json_exports is not None:
            self._values["resolve_package_json_exports"] = resolve_package_json_exports
        if resolve_package_json_imports is not None:
            self._values["resolve_package_json_imports"] = resolve_package_json_imports
        if root_dir is not None:
            self._values["root_dir"] = root_dir
        if skip_lib_check is not None:
            self._values["skip_lib_check"] = skip_lib_check
        if source_map is not None:
            self._values["source_map"] = source_map
        if source_root is not None:
            self._values["source_root"] = source_root
        if strict is not None:
            self._values["strict"] = strict
        if strict_null_checks is not None:
            self._values["strict_null_checks"] = strict_null_checks
        if strict_property_initialization is not None:
            self._values["strict_property_initialization"] = strict_property_initialization
        if strip_internal is not None:
            self._values["strip_internal"] = strip_internal
        if target is not None:
            self._values["target"] = target
        if use_unknown_in_catch_variables is not None:
            self._values["use_unknown_in_catch_variables"] = use_unknown_in_catch_variables
        if verbatim_module_syntax is not None:
            self._values["verbatim_module_syntax"] = verbatim_module_syntax

    @builtins.property
    def allow_arbitrary_extensions(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Suppress arbitrary extension import errors with the assumption that a bundler will be handling it.

        :default: undefined

        :see: https://www.typescriptlang.org/tsconfig#allowArbitraryExtensions
        :stability: experimental
        '''
        result = self._values.get("allow_arbitrary_extensions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_importing_ts_extensions(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allows TypeScript files to import each other with TypeScript-specific extensions (``.ts``, ``.mts``, ``.tsx``). Requires ``noEmit`` or ``emitDeclarationOnly``.

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("allow_importing_ts_extensions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_js(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow JavaScript files to be compiled.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("allow_js")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_synthetic_default_imports(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow default imports from modules with no default export.

        This does not affect code emit, just typechecking.

        :stability: experimental
        '''
        result = self._values.get("allow_synthetic_default_imports")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def always_strict(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Ensures that your files are parsed in the ECMAScript strict mode, and emit “use strict” for each source file.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("always_strict")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def base_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) Lets you set a base directory to resolve non-absolute module names.

        You can define a root folder where you can do absolute file resolution.

        :stability: experimental
        '''
        result = self._values.get("base_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_conditions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of additional conditions that should succeed when TypeScript resolves from an ``exports`` or ``imports`` field of a ``package.json``.

        :default: undefined

        :see: https://www.typescriptlang.org/tsconfig#customConditions
        :stability: experimental
        '''
        result = self._values.get("custom_conditions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def declaration(self) -> typing.Optional[builtins.bool]:
        '''(experimental) To be specified along with the above.

        :stability: experimental
        '''
        result = self._values.get("declaration")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def declaration_dir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Offers a way to configure the root directory for where declaration files are emitted.

        :stability: experimental
        '''
        result = self._values.get("declaration_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def emit_declaration_only(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Only emit .d.ts files; do not emit .js files.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("emit_declaration_only")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def emit_decorator_metadata(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables experimental support for decorators, which is in stage 2 of the TC39 standardization process.

        Decorators are a language feature which hasn’t yet been fully ratified into the JavaScript specification.
        This means that the implementation version in TypeScript may differ from the implementation in JavaScript when it it decided by TC39.
        You can find out more about decorator support in TypeScript in the handbook.

        :default: undefined

        :see: https://www.typescriptlang.org/docs/handbook/decorators.html
        :stability: experimental
        '''
        result = self._values.get("emit_decorator_metadata")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def es_module_interop(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Emit __importStar and __importDefault helpers for runtime babel ecosystem compatibility and enable --allowSyntheticDefaultImports for typesystem compatibility.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("es_module_interop")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def exact_optional_property_types(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies that optional property types should be interpreted exactly as written, meaning that ``| undefined`` is not added to the type Available with TypeScript 4.4 and newer.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("exact_optional_property_types")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def experimental_decorators(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables experimental support for decorators, which is in stage 2 of the TC39 standardization process.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("experimental_decorators")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def force_consistent_casing_in_file_names(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Disallow inconsistently-cased references to the same file.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("force_consistent_casing_in_file_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def imports_not_used_as_values(
        self,
    ) -> typing.Optional["TypeScriptImportsNotUsedAsValues"]:
        '''(experimental) This flag works because you can use ``import type`` to explicitly create an ``import`` statement which should never be emitted into JavaScript.

        :default: "remove"

        :see: https://www.typescriptlang.org/tsconfig#importsNotUsedAsValues
        :stability: experimental
        :remarks:

        For TypeScript 5.0+ use ``verbatimModuleSyntax`` instead.
        Posed for deprecation upon TypeScript 5.5.
        '''
        result = self._values.get("imports_not_used_as_values")
        return typing.cast(typing.Optional["TypeScriptImportsNotUsedAsValues"], result)

    @builtins.property
    def inline_source_map(self) -> typing.Optional[builtins.bool]:
        '''(experimental) When set, instead of writing out a .js.map file to provide source maps, TypeScript will embed the source map content in the .js files.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("inline_source_map")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def inline_sources(self) -> typing.Optional[builtins.bool]:
        '''(experimental) When set, TypeScript will include the original content of the .ts file as an embedded string in the source map. This is often useful in the same cases as inlineSourceMap.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("inline_sources")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def isolated_modules(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Perform additional checks to ensure that separate compilation (such as with transpileModule or.

        :default: false

        :stability: experimental
        :babel: /plugin-transform-typescript) would be safe.
        '''
        result = self._values.get("isolated_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def jsx(self) -> typing.Optional["TypeScriptJsxMode"]:
        '''(experimental) Support JSX in .tsx files: "react", "preserve", "react-native" etc.

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("jsx")
        return typing.cast(typing.Optional["TypeScriptJsxMode"], result)

    @builtins.property
    def jsx_import_source(self) -> typing.Optional[builtins.str]:
        '''(experimental) Declares the module specifier to be used for importing the jsx and jsxs factory functions when using jsx.

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("jsx_import_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lib(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Reference for type definitions / libraries to use (eg.

        ES2016, ES5, ES2018).

        :default: [ "es2018" ]

        :stability: experimental
        '''
        result = self._values.get("lib")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def module(self) -> typing.Optional[builtins.str]:
        '''(experimental) Sets the module system for the program.

        See https://www.typescriptlang.org/docs/handbook/modules.html#ambient-modules.

        :default: "CommonJS"

        :stability: experimental
        '''
        result = self._values.get("module")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def module_resolution(self) -> typing.Optional["TypeScriptModuleResolution"]:
        '''(experimental) Determine how modules get resolved.

        Either "Node" for Node.js/io.js style resolution, or "Classic".

        :default: "node"

        :stability: experimental
        '''
        result = self._values.get("module_resolution")
        return typing.cast(typing.Optional["TypeScriptModuleResolution"], result)

    @builtins.property
    def no_emit(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Do not emit outputs.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("no_emit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_emit_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Do not emit compiler output files like JavaScript source code, source-maps or declarations if any errors were reported.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("no_emit_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_fallthrough_cases_in_switch(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Report errors for fallthrough cases in switch statements.

        Ensures that any non-empty
        case inside a switch statement includes either break or return. This means you won’t
        accidentally ship a case fallthrough bug.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("no_fallthrough_cases_in_switch")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_implicit_any(self) -> typing.Optional[builtins.bool]:
        '''(experimental) In some cases where no type annotations are present, TypeScript will fall back to a type of any for a variable when it cannot infer the type.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("no_implicit_any")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_implicit_override(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Using ``noImplicitOverride``, you can ensure that sub-classes never go out of sync as they are required to explicitly declare that they are overriding a member using the ``override`` keyword.

        This also improves readability of the programmer's intent.

        Available with TypeScript 4.3 and newer.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("no_implicit_override")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_implicit_returns(self) -> typing.Optional[builtins.bool]:
        '''(experimental) When enabled, TypeScript will check all code paths in a function to ensure they return a value.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("no_implicit_returns")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_implicit_this(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Raise error on ‘this’ expressions with an implied ‘any’ type.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("no_implicit_this")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_property_access_from_index_signature(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Raise error on use of the dot syntax to access fields which are not defined.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("no_property_access_from_index_signature")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_unchecked_indexed_access(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Raise error when accessing indexes on objects with unknown keys defined in index signatures.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("no_unchecked_indexed_access")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_unused_locals(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Report errors on unused local variables.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("no_unused_locals")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_unused_parameters(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Report errors on unused parameters in functions.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("no_unused_parameters")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def out_dir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Output directory for the compiled files.

        :stability: experimental
        '''
        result = self._values.get("out_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def paths(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]]:
        '''(experimental) A series of entries which re-map imports to lookup locations relative to the baseUrl, there is a larger coverage of paths in the handbook.

        paths lets you declare how TypeScript should resolve an import in your require/imports.

        :stability: experimental
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]], result)

    @builtins.property
    def resolve_json_module(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allows importing modules with a ‘.json’ extension, which is a common practice in node projects. This includes generating a type for the import based on the static JSON shape.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("resolve_json_module")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def resolve_package_json_exports(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Forces TypeScript to consult the ``exports`` field of ``package.json`` files if it ever reads from a package in ``node_modules``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("resolve_package_json_exports")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def resolve_package_json_imports(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Forces TypeScript to consult the ``imports`` field of ``package.json`` when performing a lookup that begins with ``#`` from a file that has a ``package.json`` as an ancestor.

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("resolve_package_json_imports")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def root_dir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the root directory of input files.

        Only use to control the output directory structure with ``outDir``.

        :stability: experimental
        '''
        result = self._values.get("root_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_lib_check(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Skip type checking of all declaration files (*.d.ts).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("skip_lib_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def source_map(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables the generation of sourcemap files.

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("source_map")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def source_root(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specify the location where a debugger should locate TypeScript files instead of relative source locations.

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("source_root")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strict(self) -> typing.Optional[builtins.bool]:
        '''(experimental) The strict flag enables a wide range of type checking behavior that results in stronger guarantees of program correctness.

        Turning this on is equivalent to enabling all of the strict mode family
        options, which are outlined below. You can then turn off individual strict mode family checks as
        needed.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("strict")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def strict_null_checks(self) -> typing.Optional[builtins.bool]:
        '''(experimental) When strictNullChecks is false, null and undefined are effectively ignored by the language.

        This can lead to unexpected errors at runtime.
        When strictNullChecks is true, null and undefined have their own distinct types and you’ll
        get a type error if you try to use them where a concrete value is expected.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("strict_null_checks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def strict_property_initialization(self) -> typing.Optional[builtins.bool]:
        '''(experimental) When set to true, TypeScript will raise an error when a class property was declared but not set in the constructor.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("strict_property_initialization")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def strip_internal(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Do not emit declarations for code that has an ``@internal`` annotation in it’s JSDoc comment.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("strip_internal")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''(experimental) Modern browsers support all ES6 features, so ES6 is a good choice.

        You might choose to set
        a lower target if your code is deployed to older environments, or a higher target if your
        code is guaranteed to run in newer environments.

        :default: "ES2018"

        :stability: experimental
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_unknown_in_catch_variables(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Change the type of the variable in a catch clause from any to unknown Available with TypeScript 4.4 and newer.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("use_unknown_in_catch_variables")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def verbatim_module_syntax(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Simplifies TypeScript's handling of import/export ``type`` modifiers.

        :default: undefined

        :see: https://www.typescriptlang.org/tsconfig#verbatimModuleSyntax
        :stability: experimental
        '''
        result = self._values.get("verbatim_module_syntax")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TypeScriptCompilerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.TypeScriptImportsNotUsedAsValues")
class TypeScriptImportsNotUsedAsValues(enum.Enum):
    '''(experimental) This flag controls how ``import`` works, there are 3 different options.

    :see: https://www.typescriptlang.org/tsconfig#importsNotUsedAsValues
    :stability: experimental
    '''

    REMOVE = "REMOVE"
    '''(experimental) The default behavior of dropping ``import`` statements which only reference types.

    :stability: experimental
    '''
    PRESERVE = "PRESERVE"
    '''(experimental) Preserves all ``import`` statements whose values or types are never used.

    This can cause imports/side-effects to be preserved.

    :stability: experimental
    '''
    ERROR = "ERROR"
    '''(experimental) This preserves all imports (the same as the preserve option), but will error when a value import is only used as a type.

    This might be useful if you want to ensure no values are being accidentally imported, but still make side-effect imports explicit.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.javascript.TypeScriptJsxMode")
class TypeScriptJsxMode(enum.Enum):
    '''(experimental) Determines how JSX should get transformed into valid JavaScript.

    :see: https://www.typescriptlang.org/docs/handbook/jsx.html
    :stability: experimental
    '''

    PRESERVE = "PRESERVE"
    '''(experimental) Keeps the JSX as part of the output to be further consumed by another transform step (e.g. Babel).

    :stability: experimental
    '''
    REACT = "REACT"
    '''(experimental) Converts JSX syntax into React.createElement, does not need to go through a JSX transformation before use, and the output will have a .js file extension.

    :stability: experimental
    '''
    REACT_NATIVE = "REACT_NATIVE"
    '''(experimental) Keeps all JSX like 'preserve' mode, but output will have a .js extension.

    :stability: experimental
    '''
    REACT_JSX = "REACT_JSX"
    '''(experimental) Passes ``key`` separately from props and always passes ``children`` as props (since React 17).

    :see: https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-1.html#react-17-jsx-factories
    :stability: experimental
    '''
    REACT_JSXDEV = "REACT_JSXDEV"
    '''(experimental) Same as ``REACT_JSX`` with additional debug data.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.javascript.TypeScriptModuleResolution")
class TypeScriptModuleResolution(enum.Enum):
    '''(experimental) Determines how modules get resolved.

    :see: https://www.typescriptlang.org/docs/handbook/module-resolution.html
    :stability: experimental
    '''

    CLASSIC = "CLASSIC"
    '''(experimental) TypeScript's former default resolution strategy.

    :see: https://www.typescriptlang.org/docs/handbook/module-resolution.html#classic
    :stability: experimental
    '''
    NODE = "NODE"
    '''(experimental) Resolution strategy which attempts to mimic the Node.js module resolution strategy at runtime.

    :see: https://www.typescriptlang.org/docs/handbook/module-resolution.html#node
    :stability: experimental
    '''
    NODE16 = "NODE16"
    '''(experimental) Node.js’ ECMAScript Module Support from TypeScript 4.7 onwards.

    :see: https://www.typescriptlang.org/tsconfig#moduleResolution
    :stability: experimental
    '''
    NODE_NEXT = "NODE_NEXT"
    '''(experimental) Node.js’ ECMAScript Module Support from TypeScript 4.7 onwards.

    :see: https://www.typescriptlang.org/tsconfig#moduleResolution
    :stability: experimental
    '''
    BUNDLER = "BUNDLER"
    '''(experimental) Resolution strategy which attempts to mimic resolution patterns of modern bundlers;

    from TypeScript 5.0 onwards.

    :see: https://www.typescriptlang.org/tsconfig#moduleResolution
    :stability: experimental
    '''


class TypescriptConfig(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.javascript.TypescriptConfig",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        project: _Project_57d89203,
        *,
        compiler_options: typing.Union[TypeScriptCompilerOptions, typing.Dict[builtins.str, typing.Any]],
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        extends: typing.Optional["TypescriptConfigExtends"] = None,
        file_name: typing.Optional[builtins.str] = None,
        include: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param project: -
        :param compiler_options: (experimental) Compiler options to use.
        :param exclude: (experimental) Filters results from the "include" option. Default: - node_modules is excluded by default
        :param extends: (experimental) Base ``tsconfig.json`` configuration(s) to inherit from.
        :param file_name: Default: "tsconfig.json"
        :param include: (experimental) Specifies a list of glob patterns that match TypeScript files to be included in compilation. Default: - all .ts files recursively

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdd8e9cd126102b8184e52538d49523cef64724ec6ad410a5e2d5169e1ef0fe0)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = TypescriptConfigOptions(
            compiler_options=compiler_options,
            exclude=exclude,
            extends=extends,
            file_name=file_name,
            include=include,
        )

        jsii.create(self.__class__, self, [project, options])

    @jsii.member(jsii_name="addExclude")
    def add_exclude(self, pattern: builtins.str) -> None:
        '''
        :param pattern: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22043cd196520a238283f3d057c0a0a29f8679bf2501608e058f551552b3a6c5)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(None, jsii.invoke(self, "addExclude", [pattern]))

    @jsii.member(jsii_name="addExtends")
    def add_extends(self, value: "TypescriptConfig") -> None:
        '''(experimental) Extend from base ``TypescriptConfig`` instance.

        :param value: Base ``TypescriptConfig`` instance.

        :stability: experimental
        :remarks: TypeScript 5.0+ is required to extend from more than one base ``TypescriptConfig``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e19373d5818f12b8d7ae04b7e689d8a06b0470d6eb5c5886f5a9255a0221fd9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addExtends", [value]))

    @jsii.member(jsii_name="addInclude")
    def add_include(self, pattern: builtins.str) -> None:
        '''
        :param pattern: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecc6431d5d9f322d469f99e5739da10bb780beb09da03305a82dac281906fc5b)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(None, jsii.invoke(self, "addInclude", [pattern]))

    @jsii.member(jsii_name="preSynthesize")
    def pre_synthesize(self) -> None:
        '''(experimental) Called before synthesis.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "preSynthesize", []))

    @jsii.member(jsii_name="resolveExtendsPath")
    def resolve_extends_path(self, config_path: builtins.str) -> builtins.str:
        '''(experimental) Resolve valid TypeScript extends paths relative to this config.

        :param config_path: Path to resolve against.

        :stability: experimental
        :remarks:

        This will only resolve the relative path from this config to another given
        an absolute path as input. Any non-absolute path or other string will be returned as is.
        This is to preserve manually specified relative paths as well as npm import paths.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4b076d47872be6e9462b52280fba0e6d5509d09e6f0c405542d8edb8b704f3d)
            check_type(argname="argument config_path", value=config_path, expected_type=type_hints["config_path"])
        return typing.cast(builtins.str, jsii.invoke(self, "resolveExtendsPath", [config_path]))

    @builtins.property
    @jsii.member(jsii_name="compilerOptions")
    def compiler_options(self) -> TypeScriptCompilerOptions:
        '''
        :stability: experimental
        '''
        return typing.cast(TypeScriptCompilerOptions, jsii.get(self, "compilerOptions"))

    @builtins.property
    @jsii.member(jsii_name="exclude")
    def exclude(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclude"))

    @builtins.property
    @jsii.member(jsii_name="extends")
    def extends(self) -> typing.List[builtins.str]:
        '''(experimental) Array of base ``tsconfig.json`` paths. Any absolute paths are resolved relative to this instance, while any relative paths are used as is.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "extends"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> _JsonFile_fa8164db:
        '''
        :stability: experimental
        '''
        return typing.cast(_JsonFile_fa8164db, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="fileName")
    def file_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fileName"))

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "include"))


class TypescriptConfigExtends(
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.javascript.TypescriptConfigExtends",
):
    '''(experimental) Container for ``TypescriptConfig`` ``tsconfig.json`` base configuration(s). Extending from more than one base config file requires TypeScript 5.0+.

    :stability: experimental
    '''

    @jsii.member(jsii_name="fromPaths")
    @builtins.classmethod
    def from_paths(
        cls,
        paths: typing.Sequence[builtins.str],
    ) -> "TypescriptConfigExtends":
        '''(experimental) Factory for creation from array of file paths.

        :param paths: Absolute or relative paths to base ``tsconfig.json`` files.

        :stability: experimental
        :remarks: TypeScript 5.0+ is required to specify more than one value in ``paths``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b13693458818b040e6f9da122d60b4f324f8ab7721d6eb1c08300c101500f0aa)
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
        return typing.cast("TypescriptConfigExtends", jsii.sinvoke(cls, "fromPaths", [paths]))

    @jsii.member(jsii_name="fromTypescriptConfigs")
    @builtins.classmethod
    def from_typescript_configs(
        cls,
        configs: typing.Sequence[TypescriptConfig],
    ) -> "TypescriptConfigExtends":
        '''(experimental) Factory for creation from array of other ``TypescriptConfig`` instances.

        :param configs: Base ``TypescriptConfig`` instances.

        :stability: experimental
        :remarks: TypeScript 5.0+ is required to specify more than on value in ``configs``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb44c1fe8356fe5ed46d657b7a5c3f2198926eaf1f5780cf30a365a3e170a5e)
            check_type(argname="argument configs", value=configs, expected_type=type_hints["configs"])
        return typing.cast("TypescriptConfigExtends", jsii.sinvoke(cls, "fromTypescriptConfigs", [configs]))

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "toJSON", []))


@jsii.data_type(
    jsii_type="projen.javascript.TypescriptConfigOptions",
    jsii_struct_bases=[],
    name_mapping={
        "compiler_options": "compilerOptions",
        "exclude": "exclude",
        "extends": "extends",
        "file_name": "fileName",
        "include": "include",
    },
)
class TypescriptConfigOptions:
    def __init__(
        self,
        *,
        compiler_options: typing.Union[TypeScriptCompilerOptions, typing.Dict[builtins.str, typing.Any]],
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        extends: typing.Optional[TypescriptConfigExtends] = None,
        file_name: typing.Optional[builtins.str] = None,
        include: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param compiler_options: (experimental) Compiler options to use.
        :param exclude: (experimental) Filters results from the "include" option. Default: - node_modules is excluded by default
        :param extends: (experimental) Base ``tsconfig.json`` configuration(s) to inherit from.
        :param file_name: Default: "tsconfig.json"
        :param include: (experimental) Specifies a list of glob patterns that match TypeScript files to be included in compilation. Default: - all .ts files recursively

        :stability: experimental
        '''
        if isinstance(compiler_options, dict):
            compiler_options = TypeScriptCompilerOptions(**compiler_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f928658806d66c2cd4f3977b17ae3d10092cf4b9afb10e736c01729b7451dbb9)
            check_type(argname="argument compiler_options", value=compiler_options, expected_type=type_hints["compiler_options"])
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument extends", value=extends, expected_type=type_hints["extends"])
            check_type(argname="argument file_name", value=file_name, expected_type=type_hints["file_name"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compiler_options": compiler_options,
        }
        if exclude is not None:
            self._values["exclude"] = exclude
        if extends is not None:
            self._values["extends"] = extends
        if file_name is not None:
            self._values["file_name"] = file_name
        if include is not None:
            self._values["include"] = include

    @builtins.property
    def compiler_options(self) -> TypeScriptCompilerOptions:
        '''(experimental) Compiler options to use.

        :stability: experimental
        '''
        result = self._values.get("compiler_options")
        assert result is not None, "Required property 'compiler_options' is missing"
        return typing.cast(TypeScriptCompilerOptions, result)

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Filters results from the "include" option.

        :default: - node_modules is excluded by default

        :stability: experimental
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def extends(self) -> typing.Optional[TypescriptConfigExtends]:
        '''(experimental) Base ``tsconfig.json`` configuration(s) to inherit from.

        :stability: experimental
        '''
        result = self._values.get("extends")
        return typing.cast(typing.Optional[TypescriptConfigExtends], result)

    @builtins.property
    def file_name(self) -> typing.Optional[builtins.str]:
        '''
        :default: "tsconfig.json"

        :stability: experimental
        '''
        result = self._values.get("file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Specifies a list of glob patterns that match TypeScript files to be included in compilation.

        :default: - all .ts files recursively

        :stability: experimental
        '''
        result = self._values.get("include")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TypescriptConfigOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.UpdateSnapshot")
class UpdateSnapshot(enum.Enum):
    '''
    :stability: experimental
    '''

    ALWAYS = "ALWAYS"
    '''(experimental) Always update snapshots in "test" task.

    :stability: experimental
    '''
    NEVER = "NEVER"
    '''(experimental) Never update snapshots in "test" task and create a separate "test:update" task.

    :stability: experimental
    '''


class UpgradeDependencies(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.javascript.UpgradeDependencies",
):
    '''(experimental) Upgrade node project dependencies.

    :stability: experimental
    '''

    def __init__(
        self,
        project: NodeProject,
        *,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        include: typing.Optional[typing.Sequence[builtins.str]] = None,
        pull_request_title: typing.Optional[builtins.str] = None,
        satisfy_peer_dependencies: typing.Optional[builtins.bool] = None,
        semantic_commit: typing.Optional[builtins.str] = None,
        signoff: typing.Optional[builtins.bool] = None,
        target: typing.Optional[builtins.str] = None,
        task_name: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Sequence[_DependencyType_6b786d68]] = None,
        workflow: typing.Optional[builtins.bool] = None,
        workflow_options: typing.Optional[typing.Union["UpgradeDependenciesWorkflowOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param project: -
        :param exclude: (experimental) List of package names to exclude during the upgrade. Default: - Nothing is excluded.
        :param include: (experimental) List of package names to include during the upgrade. Default: - Everything is included.
        :param pull_request_title: (experimental) Title of the pull request to use (should be all lower-case). Default: "upgrade dependencies"
        :param satisfy_peer_dependencies: (experimental) Check peer dependencies of installed packages and filter updates to compatible versions. By default, the upgrade workflow will adhere to version constraints from peer dependencies. Sometimes this is not desirable and can be disabled. Default: true
        :param semantic_commit: (experimental) The semantic commit type. Default: 'chore'
        :param signoff: (experimental) Add Signed-off-by line by the committer at the end of the commit log message. Default: true
        :param target: (experimental) Determines the target version to upgrade dependencies to. Default: "minor"
        :param task_name: (experimental) The name of the task that will be created. This will also be the workflow name. Default: "upgrade".
        :param types: (experimental) Specify which dependency types the upgrade should operate on. Default: - All dependency types.
        :param workflow: (experimental) Include a github workflow for creating PR's that upgrades the required dependencies, either by manual dispatch, or by a schedule. If this is ``false``, only a local projen task is created, which can be executed manually to upgrade the dependencies. Default: - true for root projects, false for sub-projects.
        :param workflow_options: (experimental) Options for the github workflow. Only applies if ``workflow`` is true. Default: - default options.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__497e18a2c8dc3200cff8b21dfad7c418d29517aa6d67e2a2555ee78fa63ff385)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = UpgradeDependenciesOptions(
            exclude=exclude,
            include=include,
            pull_request_title=pull_request_title,
            satisfy_peer_dependencies=satisfy_peer_dependencies,
            semantic_commit=semantic_commit,
            signoff=signoff,
            target=target,
            task_name=task_name,
            types=types,
            workflow=workflow,
            workflow_options=workflow_options,
        )

        jsii.create(self.__class__, self, [project, options])

    @jsii.member(jsii_name="addPostBuildSteps")
    def add_post_build_steps(self, *steps: _JobStep_c3287c05) -> None:
        '''(experimental) Add steps to execute a successful build.

        :param steps: workflow steps.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff92c41406c3198455d1dfec862b6c0109c8239ff2a3eed09afaaaf67774467b)
            check_type(argname="argument steps", value=steps, expected_type=typing.Tuple[type_hints["steps"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addPostBuildSteps", [*steps]))

    @builtins.property
    @jsii.member(jsii_name="postUpgradeTask")
    def post_upgrade_task(self) -> _Task_9fa875b6:
        '''(experimental) A task run after the upgrade task.

        :stability: experimental
        '''
        return typing.cast(_Task_9fa875b6, jsii.get(self, "postUpgradeTask"))

    @builtins.property
    @jsii.member(jsii_name="upgradeTask")
    def upgrade_task(self) -> _Task_9fa875b6:
        '''(experimental) The upgrade task.

        :stability: experimental
        '''
        return typing.cast(_Task_9fa875b6, jsii.get(self, "upgradeTask"))

    @builtins.property
    @jsii.member(jsii_name="workflows")
    def workflows(self) -> typing.List[_GithubWorkflow_a1772357]:
        '''(experimental) The workflows that execute the upgrades.

        One workflow per branch.

        :stability: experimental
        '''
        return typing.cast(typing.List[_GithubWorkflow_a1772357], jsii.get(self, "workflows"))

    @builtins.property
    @jsii.member(jsii_name="containerOptions")
    def container_options(self) -> typing.Optional[_ContainerOptions_f50907af]:
        '''(experimental) Container definitions for the upgrade workflow.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_ContainerOptions_f50907af], jsii.get(self, "containerOptions"))

    @container_options.setter
    def container_options(
        self,
        value: typing.Optional[_ContainerOptions_f50907af],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66ba20de6f144f37e582e192e3ed592a6be0e8bc3d10e3b730af62082afa0010)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerOptions", value)


@jsii.data_type(
    jsii_type="projen.javascript.UpgradeDependenciesOptions",
    jsii_struct_bases=[],
    name_mapping={
        "exclude": "exclude",
        "include": "include",
        "pull_request_title": "pullRequestTitle",
        "satisfy_peer_dependencies": "satisfyPeerDependencies",
        "semantic_commit": "semanticCommit",
        "signoff": "signoff",
        "target": "target",
        "task_name": "taskName",
        "types": "types",
        "workflow": "workflow",
        "workflow_options": "workflowOptions",
    },
)
class UpgradeDependenciesOptions:
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        include: typing.Optional[typing.Sequence[builtins.str]] = None,
        pull_request_title: typing.Optional[builtins.str] = None,
        satisfy_peer_dependencies: typing.Optional[builtins.bool] = None,
        semantic_commit: typing.Optional[builtins.str] = None,
        signoff: typing.Optional[builtins.bool] = None,
        target: typing.Optional[builtins.str] = None,
        task_name: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Sequence[_DependencyType_6b786d68]] = None,
        workflow: typing.Optional[builtins.bool] = None,
        workflow_options: typing.Optional[typing.Union["UpgradeDependenciesWorkflowOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options for ``UpgradeDependencies``.

        :param exclude: (experimental) List of package names to exclude during the upgrade. Default: - Nothing is excluded.
        :param include: (experimental) List of package names to include during the upgrade. Default: - Everything is included.
        :param pull_request_title: (experimental) Title of the pull request to use (should be all lower-case). Default: "upgrade dependencies"
        :param satisfy_peer_dependencies: (experimental) Check peer dependencies of installed packages and filter updates to compatible versions. By default, the upgrade workflow will adhere to version constraints from peer dependencies. Sometimes this is not desirable and can be disabled. Default: true
        :param semantic_commit: (experimental) The semantic commit type. Default: 'chore'
        :param signoff: (experimental) Add Signed-off-by line by the committer at the end of the commit log message. Default: true
        :param target: (experimental) Determines the target version to upgrade dependencies to. Default: "minor"
        :param task_name: (experimental) The name of the task that will be created. This will also be the workflow name. Default: "upgrade".
        :param types: (experimental) Specify which dependency types the upgrade should operate on. Default: - All dependency types.
        :param workflow: (experimental) Include a github workflow for creating PR's that upgrades the required dependencies, either by manual dispatch, or by a schedule. If this is ``false``, only a local projen task is created, which can be executed manually to upgrade the dependencies. Default: - true for root projects, false for sub-projects.
        :param workflow_options: (experimental) Options for the github workflow. Only applies if ``workflow`` is true. Default: - default options.

        :stability: experimental
        '''
        if isinstance(workflow_options, dict):
            workflow_options = UpgradeDependenciesWorkflowOptions(**workflow_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f7b896c11469470869bc4bfc86c9bb13fd308223e316ba71124c00b5709af1e)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            check_type(argname="argument pull_request_title", value=pull_request_title, expected_type=type_hints["pull_request_title"])
            check_type(argname="argument satisfy_peer_dependencies", value=satisfy_peer_dependencies, expected_type=type_hints["satisfy_peer_dependencies"])
            check_type(argname="argument semantic_commit", value=semantic_commit, expected_type=type_hints["semantic_commit"])
            check_type(argname="argument signoff", value=signoff, expected_type=type_hints["signoff"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument task_name", value=task_name, expected_type=type_hints["task_name"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
            check_type(argname="argument workflow", value=workflow, expected_type=type_hints["workflow"])
            check_type(argname="argument workflow_options", value=workflow_options, expected_type=type_hints["workflow_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude is not None:
            self._values["exclude"] = exclude
        if include is not None:
            self._values["include"] = include
        if pull_request_title is not None:
            self._values["pull_request_title"] = pull_request_title
        if satisfy_peer_dependencies is not None:
            self._values["satisfy_peer_dependencies"] = satisfy_peer_dependencies
        if semantic_commit is not None:
            self._values["semantic_commit"] = semantic_commit
        if signoff is not None:
            self._values["signoff"] = signoff
        if target is not None:
            self._values["target"] = target
        if task_name is not None:
            self._values["task_name"] = task_name
        if types is not None:
            self._values["types"] = types
        if workflow is not None:
            self._values["workflow"] = workflow
        if workflow_options is not None:
            self._values["workflow_options"] = workflow_options

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of package names to exclude during the upgrade.

        :default: - Nothing is excluded.

        :stability: experimental
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of package names to include during the upgrade.

        :default: - Everything is included.

        :stability: experimental
        '''
        result = self._values.get("include")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pull_request_title(self) -> typing.Optional[builtins.str]:
        '''(experimental) Title of the pull request to use (should be all lower-case).

        :default: "upgrade dependencies"

        :stability: experimental
        '''
        result = self._values.get("pull_request_title")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def satisfy_peer_dependencies(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Check peer dependencies of installed packages and filter updates to compatible versions.

        By default, the upgrade workflow will adhere to version constraints from peer dependencies.
        Sometimes this is not desirable and can be disabled.

        :default: true

        :see: https://github.com/raineorshine/npm-check-updates#peer
        :stability: experimental
        '''
        result = self._values.get("satisfy_peer_dependencies")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def semantic_commit(self) -> typing.Optional[builtins.str]:
        '''(experimental) The semantic commit type.

        :default: 'chore'

        :stability: experimental
        '''
        result = self._values.get("semantic_commit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signoff(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add Signed-off-by line by the committer at the end of the commit log message.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("signoff")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''(experimental) Determines the target version to upgrade dependencies to.

        :default: "minor"

        :see: https://github.com/raineorshine/npm-check-updates#target
        :stability: experimental
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def task_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the task that will be created.

        This will also be the workflow name.

        :default: "upgrade".

        :stability: experimental
        '''
        result = self._values.get("task_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def types(self) -> typing.Optional[typing.List[_DependencyType_6b786d68]]:
        '''(experimental) Specify which dependency types the upgrade should operate on.

        :default: - All dependency types.

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[_DependencyType_6b786d68]], result)

    @builtins.property
    def workflow(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include a github workflow for creating PR's that upgrades the required dependencies, either by manual dispatch, or by a schedule.

        If this is ``false``, only a local projen task is created, which can be executed manually to
        upgrade the dependencies.

        :default: - true for root projects, false for sub-projects.

        :stability: experimental
        '''
        result = self._values.get("workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def workflow_options(self) -> typing.Optional["UpgradeDependenciesWorkflowOptions"]:
        '''(experimental) Options for the github workflow.

        Only applies if ``workflow`` is true.

        :default: - default options.

        :stability: experimental
        '''
        result = self._values.get("workflow_options")
        return typing.cast(typing.Optional["UpgradeDependenciesWorkflowOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UpgradeDependenciesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UpgradeDependenciesSchedule(
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.javascript.UpgradeDependenciesSchedule",
):
    '''(experimental) How often to check for new versions and raise pull requests for version upgrades.

    :stability: experimental
    '''

    @jsii.member(jsii_name="expressions")
    @builtins.classmethod
    def expressions(
        cls,
        cron: typing.Sequence[builtins.str],
    ) -> "UpgradeDependenciesSchedule":
        '''(experimental) Create a schedule from a raw cron expression.

        :param cron: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0616cac83033da3960c6645511af30fae841bea5f2cf5229410d6113065c8dd2)
            check_type(argname="argument cron", value=cron, expected_type=type_hints["cron"])
        return typing.cast("UpgradeDependenciesSchedule", jsii.sinvoke(cls, "expressions", [cron]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DAILY")
    def DAILY(cls) -> "UpgradeDependenciesSchedule":
        '''(experimental) At 00:00.

        :stability: experimental
        '''
        return typing.cast("UpgradeDependenciesSchedule", jsii.sget(cls, "DAILY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MONTHLY")
    def MONTHLY(cls) -> "UpgradeDependenciesSchedule":
        '''(experimental) At 00:00 on day-of-month 1.

        :stability: experimental
        '''
        return typing.cast("UpgradeDependenciesSchedule", jsii.sget(cls, "MONTHLY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NEVER")
    def NEVER(cls) -> "UpgradeDependenciesSchedule":
        '''(experimental) Disables automatic upgrades.

        :stability: experimental
        '''
        return typing.cast("UpgradeDependenciesSchedule", jsii.sget(cls, "NEVER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WEEKDAY")
    def WEEKDAY(cls) -> "UpgradeDependenciesSchedule":
        '''(experimental) At 00:00 on every day-of-week from Monday through Friday.

        :stability: experimental
        '''
        return typing.cast("UpgradeDependenciesSchedule", jsii.sget(cls, "WEEKDAY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WEEKLY")
    def WEEKLY(cls) -> "UpgradeDependenciesSchedule":
        '''(experimental) At 00:00 on Monday.

        :stability: experimental
        '''
        return typing.cast("UpgradeDependenciesSchedule", jsii.sget(cls, "WEEKLY"))

    @builtins.property
    @jsii.member(jsii_name="cron")
    def cron(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cron"))


@jsii.data_type(
    jsii_type="projen.javascript.UpgradeDependenciesWorkflowOptions",
    jsii_struct_bases=[],
    name_mapping={
        "assignees": "assignees",
        "branches": "branches",
        "container": "container",
        "git_identity": "gitIdentity",
        "labels": "labels",
        "permissions": "permissions",
        "projen_credentials": "projenCredentials",
        "runs_on": "runsOn",
        "runs_on_group": "runsOnGroup",
        "schedule": "schedule",
    },
)
class UpgradeDependenciesWorkflowOptions:
    def __init__(
        self,
        *,
        assignees: typing.Optional[typing.Sequence[builtins.str]] = None,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        container: typing.Optional[typing.Union[_ContainerOptions_f50907af, typing.Dict[builtins.str, typing.Any]]] = None,
        git_identity: typing.Optional[typing.Union[_GitIdentity_6effc3de, typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        permissions: typing.Optional[typing.Union[_JobPermissions_3b5b53dc, typing.Dict[builtins.str, typing.Any]]] = None,
        projen_credentials: typing.Optional[_GithubCredentials_ae257072] = None,
        runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[UpgradeDependenciesSchedule] = None,
    ) -> None:
        '''(experimental) Options for ``UpgradeDependencies.workflowOptions``.

        :param assignees: (experimental) Assignees to add on the PR. Default: - no assignees
        :param branches: (experimental) List of branches to create PR's for. Default: - All release branches configured for the project.
        :param container: (experimental) Job container options. Default: - defaults
        :param git_identity: (experimental) The git identity to use for commits. Default: "github-actions@github.com"
        :param labels: (experimental) Labels to apply on the PR. Default: - no labels.
        :param permissions: (experimental) Permissions granted to the upgrade job To limit job permissions for ``contents``, the desired permissions have to be explicitly set, e.g.: ``{ contents: JobPermission.NONE }``. Default: ``{ contents: JobPermission.READ }``
        :param projen_credentials: (experimental) Choose a method for authenticating with GitHub for creating the PR. When using the default github token, PR's created by this workflow will not trigger any subsequent workflows (i.e the build workflow), so projen requires API access to be provided through e.g. a personal access token or other method. Default: - personal access token named PROJEN_GITHUB_TOKEN
        :param runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param runs_on_group: (experimental) Github Runner Group selection options.
        :param schedule: (experimental) Schedule to run on. Default: UpgradeDependenciesSchedule.DAILY

        :stability: experimental
        '''
        if isinstance(container, dict):
            container = _ContainerOptions_f50907af(**container)
        if isinstance(git_identity, dict):
            git_identity = _GitIdentity_6effc3de(**git_identity)
        if isinstance(permissions, dict):
            permissions = _JobPermissions_3b5b53dc(**permissions)
        if isinstance(runs_on_group, dict):
            runs_on_group = _GroupRunnerOptions_148c59c1(**runs_on_group)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59fa39c2475322c21b2f7d03f2f2ada171b7e546b1d88beb8a75baa8238b629e)
            check_type(argname="argument assignees", value=assignees, expected_type=type_hints["assignees"])
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument git_identity", value=git_identity, expected_type=type_hints["git_identity"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument projen_credentials", value=projen_credentials, expected_type=type_hints["projen_credentials"])
            check_type(argname="argument runs_on", value=runs_on, expected_type=type_hints["runs_on"])
            check_type(argname="argument runs_on_group", value=runs_on_group, expected_type=type_hints["runs_on_group"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assignees is not None:
            self._values["assignees"] = assignees
        if branches is not None:
            self._values["branches"] = branches
        if container is not None:
            self._values["container"] = container
        if git_identity is not None:
            self._values["git_identity"] = git_identity
        if labels is not None:
            self._values["labels"] = labels
        if permissions is not None:
            self._values["permissions"] = permissions
        if projen_credentials is not None:
            self._values["projen_credentials"] = projen_credentials
        if runs_on is not None:
            self._values["runs_on"] = runs_on
        if runs_on_group is not None:
            self._values["runs_on_group"] = runs_on_group
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def assignees(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Assignees to add on the PR.

        :default: - no assignees

        :stability: experimental
        '''
        result = self._values.get("assignees")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of branches to create PR's for.

        :default: - All release branches configured for the project.

        :stability: experimental
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def container(self) -> typing.Optional[_ContainerOptions_f50907af]:
        '''(experimental) Job container options.

        :default: - defaults

        :stability: experimental
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[_ContainerOptions_f50907af], result)

    @builtins.property
    def git_identity(self) -> typing.Optional[_GitIdentity_6effc3de]:
        '''(experimental) The git identity to use for commits.

        :default: "github-actions@github.com"

        :stability: experimental
        '''
        result = self._values.get("git_identity")
        return typing.cast(typing.Optional[_GitIdentity_6effc3de], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Labels to apply on the PR.

        :default: - no labels.

        :stability: experimental
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permissions(self) -> typing.Optional[_JobPermissions_3b5b53dc]:
        '''(experimental) Permissions granted to the upgrade job To limit job permissions for ``contents``, the desired permissions have to be explicitly set, e.g.: ``{ contents: JobPermission.NONE }``.

        :default: ``{ contents: JobPermission.READ }``

        :stability: experimental
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[_JobPermissions_3b5b53dc], result)

    @builtins.property
    def projen_credentials(self) -> typing.Optional[_GithubCredentials_ae257072]:
        '''(experimental) Choose a method for authenticating with GitHub for creating the PR.

        When using the default github token, PR's created by this workflow
        will not trigger any subsequent workflows (i.e the build workflow), so
        projen requires API access to be provided through e.g. a personal
        access token or other method.

        :default: - personal access token named PROJEN_GITHUB_TOKEN

        :see: https://github.com/peter-evans/create-pull-request/issues/48
        :stability: experimental
        '''
        result = self._values.get("projen_credentials")
        return typing.cast(typing.Optional[_GithubCredentials_ae257072], result)

    @builtins.property
    def runs_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Github Runner selection labels.

        :default: ["ubuntu-latest"]

        :stability: experimental
        :description: Defines a target Runner by labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("runs_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def runs_on_group(self) -> typing.Optional[_GroupRunnerOptions_148c59c1]:
        '''(experimental) Github Runner Group selection options.

        :stability: experimental
        :description: Defines a target Runner Group by name and/or labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("runs_on_group")
        return typing.cast(typing.Optional[_GroupRunnerOptions_148c59c1], result)

    @builtins.property
    def schedule(self) -> typing.Optional[UpgradeDependenciesSchedule]:
        '''(experimental) Schedule to run on.

        :default: UpgradeDependenciesSchedule.DAILY

        :stability: experimental
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[UpgradeDependenciesSchedule], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UpgradeDependenciesWorkflowOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WatchPlugin(metaclass=jsii.JSIIMeta, jsii_type="projen.javascript.WatchPlugin"):
    '''
    :stability: experimental
    '''

    def __init__(self, name: builtins.str, options: typing.Any = None) -> None:
        '''
        :param name: -
        :param options: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82731b5aeb15fc642017d0dee706d4e02c814dbcf91efe82eb0ac07b490a354a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
        jsii.create(self.__class__, self, [name, options])


@jsii.data_type(
    jsii_type="projen.javascript.AddBundleOptions",
    jsii_struct_bases=[BundlingOptions],
    name_mapping={
        "externals": "externals",
        "sourcemap": "sourcemap",
        "watch_task": "watchTask",
        "platform": "platform",
        "target": "target",
        "executable": "executable",
        "loaders": "loaders",
        "outfile": "outfile",
        "tsconfig_path": "tsconfigPath",
    },
)
class AddBundleOptions(BundlingOptions):
    def __init__(
        self,
        *,
        externals: typing.Optional[typing.Sequence[builtins.str]] = None,
        sourcemap: typing.Optional[builtins.bool] = None,
        watch_task: typing.Optional[builtins.bool] = None,
        platform: builtins.str,
        target: builtins.str,
        executable: typing.Optional[builtins.bool] = None,
        loaders: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        outfile: typing.Optional[builtins.str] = None,
        tsconfig_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for ``addBundle()``.

        :param externals: (experimental) You can mark a file or a package as external to exclude it from your build. Instead of being bundled, the import will be preserved (using require for the iife and cjs formats and using import for the esm format) and will be evaluated at run time instead. This has several uses. First of all, it can be used to trim unnecessary code from your bundle for a code path that you know will never be executed. For example, a package may contain code that only runs in node but you will only be using that package in the browser. It can also be used to import code in node at run time from a package that cannot be bundled. For example, the fsevents package contains a native extension, which esbuild doesn't support. Default: []
        :param sourcemap: (experimental) Include a source map in the bundle. Default: false
        :param watch_task: (experimental) In addition to the ``bundle:xyz`` task, creates ``bundle:xyz:watch`` task which will invoke the same esbuild command with the ``--watch`` flag. This can be used to continusouly watch for changes. Default: true
        :param platform: (experimental) esbuild platform.
        :param target: (experimental) esbuild target.
        :param executable: (experimental) Mark the output file as executable. Default: false
        :param loaders: (experimental) Map of file extensions (without dot) and loaders to use for this file type. Loaders are appended to the esbuild command by ``--loader:.extension=loader``
        :param outfile: (experimental) Bundler output path relative to the asset's output directory. Default: "index.js"
        :param tsconfig_path: (experimental) The path of the tsconfig.json file to use for bundling. Default: "tsconfig.json"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fda879bb1fe52a68839c7634ab5ab9f2cedf7154361c8a0487248d72bab68e62)
            check_type(argname="argument externals", value=externals, expected_type=type_hints["externals"])
            check_type(argname="argument sourcemap", value=sourcemap, expected_type=type_hints["sourcemap"])
            check_type(argname="argument watch_task", value=watch_task, expected_type=type_hints["watch_task"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
            check_type(argname="argument loaders", value=loaders, expected_type=type_hints["loaders"])
            check_type(argname="argument outfile", value=outfile, expected_type=type_hints["outfile"])
            check_type(argname="argument tsconfig_path", value=tsconfig_path, expected_type=type_hints["tsconfig_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "platform": platform,
            "target": target,
        }
        if externals is not None:
            self._values["externals"] = externals
        if sourcemap is not None:
            self._values["sourcemap"] = sourcemap
        if watch_task is not None:
            self._values["watch_task"] = watch_task
        if executable is not None:
            self._values["executable"] = executable
        if loaders is not None:
            self._values["loaders"] = loaders
        if outfile is not None:
            self._values["outfile"] = outfile
        if tsconfig_path is not None:
            self._values["tsconfig_path"] = tsconfig_path

    @builtins.property
    def externals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) You can mark a file or a package as external to exclude it from your build.

        Instead of being bundled, the import will be preserved (using require for
        the iife and cjs formats and using import for the esm format) and will be
        evaluated at run time instead.

        This has several uses. First of all, it can be used to trim unnecessary
        code from your bundle for a code path that you know will never be executed.
        For example, a package may contain code that only runs in node but you will
        only be using that package in the browser. It can also be used to import
        code in node at run time from a package that cannot be bundled. For
        example, the fsevents package contains a native extension, which esbuild
        doesn't support.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("externals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sourcemap(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include a source map in the bundle.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("sourcemap")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def watch_task(self) -> typing.Optional[builtins.bool]:
        '''(experimental) In addition to the ``bundle:xyz`` task, creates ``bundle:xyz:watch`` task which will invoke the same esbuild command with the ``--watch`` flag.

        This can be used
        to continusouly watch for changes.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("watch_task")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def platform(self) -> builtins.str:
        '''(experimental) esbuild platform.

        :stability: experimental

        Example::

            "node"
        '''
        result = self._values.get("platform")
        assert result is not None, "Required property 'platform' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''(experimental) esbuild target.

        :stability: experimental

        Example::

            "node12"
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def executable(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Mark the output file as executable.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("executable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def loaders(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Map of file extensions (without dot) and loaders to use for this file type.

        Loaders are appended to the esbuild command by ``--loader:.extension=loader``

        :stability: experimental
        '''
        result = self._values.get("loaders")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def outfile(self) -> typing.Optional[builtins.str]:
        '''(experimental) Bundler output path relative to the asset's output directory.

        :default: "index.js"

        :stability: experimental
        '''
        result = self._values.get("outfile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tsconfig_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path of the tsconfig.json file to use for bundling.

        :default: "tsconfig.json"

        :stability: experimental
        '''
        result = self._values.get("tsconfig_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddBundleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddBundleOptions",
    "ArrowParens",
    "AutoRelease",
    "Bundle",
    "Bundler",
    "BundlerOptions",
    "BundlingOptions",
    "CodeArtifactAuthProvider",
    "CodeArtifactOptions",
    "CoverageThreshold",
    "EmbeddedLanguageFormatting",
    "EndOfLine",
    "Eslint",
    "EslintOptions",
    "EslintOverride",
    "HTMLWhitespaceSensitivity",
    "HasteConfig",
    "Jest",
    "JestConfigOptions",
    "JestOptions",
    "JestReporter",
    "NodePackage",
    "NodePackageManager",
    "NodePackageOptions",
    "NodeProject",
    "NodeProjectOptions",
    "NpmAccess",
    "NpmConfig",
    "NpmConfigOptions",
    "PeerDependencyOptions",
    "Prettier",
    "PrettierOptions",
    "PrettierOverride",
    "PrettierSettings",
    "Projenrc",
    "ProjenrcOptions",
    "ProseWrap",
    "QuoteProps",
    "RenderWorkflowSetupOptions",
    "ScopedPackagesOptions",
    "TrailingComma",
    "Transform",
    "TypeScriptCompilerOptions",
    "TypeScriptImportsNotUsedAsValues",
    "TypeScriptJsxMode",
    "TypeScriptModuleResolution",
    "TypescriptConfig",
    "TypescriptConfigExtends",
    "TypescriptConfigOptions",
    "UpdateSnapshot",
    "UpgradeDependencies",
    "UpgradeDependenciesOptions",
    "UpgradeDependenciesSchedule",
    "UpgradeDependenciesWorkflowOptions",
    "WatchPlugin",
]

publication.publish()

def _typecheckingstub__61e51544f8a1488a41b14a0ee08df5b86eb83b8852c5ea8c95747007b7c012de(
    *,
    bundle_task: _Task_9fa875b6,
    outdir: builtins.str,
    outfile: builtins.str,
    watch_task: typing.Optional[_Task_9fa875b6] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39a2a4441a612906ad5a7b87f1a6c53ed88fb86f4e31bd1a7283a06a2e9ebf7(
    project: _Project_57d89203,
    *,
    add_to_pre_compile: typing.Optional[builtins.bool] = None,
    assets_dir: typing.Optional[builtins.str] = None,
    esbuild_version: typing.Optional[builtins.str] = None,
    loaders: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bef383122352b305e57b5282e27bdaa8a9889f1dd224d03d28a1c2cc73120b0(
    project: _Project_57d89203,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3fe067eb8c7b6b184c855eea4d40743f016f5de6e522e14523a7e7695ad811(
    entrypoint: builtins.str,
    *,
    platform: builtins.str,
    target: builtins.str,
    executable: typing.Optional[builtins.bool] = None,
    loaders: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    outfile: typing.Optional[builtins.str] = None,
    tsconfig_path: typing.Optional[builtins.str] = None,
    externals: typing.Optional[typing.Sequence[builtins.str]] = None,
    sourcemap: typing.Optional[builtins.bool] = None,
    watch_task: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a14ca8f2b867bbbf0d45b5661abe92e6975540f78ea16f7ed21f5f213c4913(
    *,
    add_to_pre_compile: typing.Optional[builtins.bool] = None,
    assets_dir: typing.Optional[builtins.str] = None,
    esbuild_version: typing.Optional[builtins.str] = None,
    loaders: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e252fd4be8ae854f73a85420360ed4acf437d507d78f6a911faa76a8abd5be7(
    *,
    externals: typing.Optional[typing.Sequence[builtins.str]] = None,
    sourcemap: typing.Optional[builtins.bool] = None,
    watch_task: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002c9939ff1c7990e7c7029095bb5f21d1cc7e5576d9a2db081cbf690aec60f8(
    *,
    access_key_id_secret: typing.Optional[builtins.str] = None,
    auth_provider: typing.Optional[CodeArtifactAuthProvider] = None,
    role_to_assume: typing.Optional[builtins.str] = None,
    secret_access_key_secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f20f577fcce2d29c8caf0cf8580b22e6e9616455ddbbdda0e6f84e331b0660(
    *,
    branches: typing.Optional[jsii.Number] = None,
    functions: typing.Optional[jsii.Number] = None,
    lines: typing.Optional[jsii.Number] = None,
    statements: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41d20792db723180b2558eb351d1b15e6cc51985fdc95dd8481c5fae78aa6963(
    project: NodeProject,
    *,
    dirs: typing.Sequence[builtins.str],
    alias_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    alias_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    devdirs: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    lint_projen_rc: typing.Optional[builtins.bool] = None,
    lint_projen_rc_file: typing.Optional[builtins.str] = None,
    prettier: typing.Optional[builtins.bool] = None,
    ts_always_try_types: typing.Optional[builtins.bool] = None,
    tsconfig_path: typing.Optional[builtins.str] = None,
    yaml: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e06eae7f2f48a5d785ab71742d0b102d7eb8b056db43d7828d871b53a8004a5(
    project: _Project_57d89203,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93136ac5c9172a02dce49add560ad232b311f1482a6693dca9b52cb68af2ca4(
    *extend_list: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d763feccbd0bc84b224afc2b98acef5e87f938260e31532e536772fb599fbc88(
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c302914aeeb5275b37b60ab64fa0cc6a10a65a08a8f7d8b2aba9aebcc4f75f(
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f336402a11e766eb80cbfa5e80fea16b3ef9d7b18f0aa3a2a7b17e24647aa6c9(
    *plugins: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ea4c9051e61eb8d25919e5b5cb6ba7ef44e9a5d642dec514714c13c4b9141c(
    rules: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c512f160dd2d4145e1c0d43de9571ffe4d89e10b34c7d9a7b9fbba3f85ca56(
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26892c968b7bf4d64dd2597bbdabf1f1e9ced92002225a4eedfae6cbe3c22894(
    *,
    dirs: typing.Sequence[builtins.str],
    alias_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    alias_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    devdirs: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    lint_projen_rc: typing.Optional[builtins.bool] = None,
    lint_projen_rc_file: typing.Optional[builtins.str] = None,
    prettier: typing.Optional[builtins.bool] = None,
    ts_always_try_types: typing.Optional[builtins.bool] = None,
    tsconfig_path: typing.Optional[builtins.str] = None,
    yaml: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31a0dd46abf45fc4e6701aa5424796361affd0e9c44ed0f9005dd4fe08f3a136(
    *,
    files: typing.Sequence[builtins.str],
    parser: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d0f97663aee053bcca0e3b33c8be45ef5c6271b8e0c683a67d717aa914e2a89(
    *,
    compute_sha1: typing.Optional[builtins.bool] = None,
    default_platform: typing.Optional[builtins.str] = None,
    haste_impl_module_path: typing.Optional[builtins.str] = None,
    platforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    throw_on_module_collision: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f22158e02967239263c228b0eadfa82f5edd4d7b172b8506a5b32bc46ab7738(
    project: NodeProject,
    *,
    config_file_path: typing.Optional[builtins.str] = None,
    coverage: typing.Optional[builtins.bool] = None,
    coverage_text: typing.Optional[builtins.bool] = None,
    extra_cli_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    jest_config: typing.Optional[typing.Union[JestConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    jest_version: typing.Optional[builtins.str] = None,
    junit_reporting: typing.Optional[builtins.bool] = None,
    preserve_default_reporters: typing.Optional[builtins.bool] = None,
    update_snapshot: typing.Optional[UpdateSnapshot] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f7fcc78583eceb598afdcb95edc0f1b1e50996f7069e12c4379c4826f26209(
    project: _Project_57d89203,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e87fe808869e615e76d29eee7ca1d2238a1385943c81f0a2e892460ceedb5ed(
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4c1ef11a85bcfb37b6e70871ed29cf5fa4c0462b66dc45e117870bbc694112(
    reporter: JestReporter,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac5cebbfb17927ec2e8823a44f46135f97967d425da95c8fb3e9178d5692325(
    file: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e0d94b263ceb92e7dbb69cd4c07c5974658fb7c8657d66df3942b0de62fdd0(
    file: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90cd9fa168c9e74d2ff0170f7a1eab10a2368f21ff1133964d018b8019d7268(
    file: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79885cc12d31e7c903be82393a87b275c69824c1f59cae5ba5c8d4f5de5982e4(
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340f8ef9eed036d2e1af02ee13866e070b25e032c7262d1181adf28bbee99b5a(
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38439e86b40e7bc302e4faa48880e15ba8a10e5a2769a5b73cbf33a01a318752(
    *,
    additional_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    automock: typing.Optional[builtins.bool] = None,
    bail: typing.Optional[typing.Union[jsii.Number, builtins.bool]] = None,
    cache_directory: typing.Optional[builtins.str] = None,
    clear_mocks: typing.Optional[builtins.bool] = None,
    collect_coverage: typing.Optional[builtins.bool] = None,
    collect_coverage_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    coverage_directory: typing.Optional[builtins.str] = None,
    coverage_path_ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    coverage_provider: typing.Optional[builtins.str] = None,
    coverage_reporters: typing.Optional[typing.Sequence[builtins.str]] = None,
    coverage_threshold: typing.Optional[typing.Union[CoverageThreshold, typing.Dict[builtins.str, typing.Any]]] = None,
    dependency_extractor: typing.Optional[builtins.str] = None,
    display_name: typing.Any = None,
    error_on_deprecated: typing.Optional[builtins.bool] = None,
    extra_globals: typing.Optional[typing.Sequence[builtins.str]] = None,
    force_coverage_match: typing.Optional[typing.Sequence[builtins.str]] = None,
    globals: typing.Any = None,
    global_setup: typing.Optional[builtins.str] = None,
    global_teardown: typing.Optional[builtins.str] = None,
    haste: typing.Optional[typing.Union[HasteConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    inject_globals: typing.Optional[builtins.bool] = None,
    max_concurrency: typing.Optional[jsii.Number] = None,
    max_workers: typing.Optional[typing.Union[builtins.str, jsii.Number]] = None,
    module_directories: typing.Optional[typing.Sequence[builtins.str]] = None,
    module_file_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    module_name_mapper: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[builtins.str]]]] = None,
    module_path_ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    module_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    notify: typing.Optional[builtins.bool] = None,
    notify_mode: typing.Optional[builtins.str] = None,
    preset: typing.Optional[builtins.str] = None,
    prettier_path: typing.Optional[builtins.str] = None,
    projects: typing.Optional[typing.Sequence[typing.Union[builtins.str, typing.Mapping[builtins.str, typing.Any]]]] = None,
    reporters: typing.Optional[typing.Sequence[JestReporter]] = None,
    reset_mocks: typing.Optional[builtins.bool] = None,
    reset_modules: typing.Optional[builtins.bool] = None,
    resolver: typing.Optional[builtins.str] = None,
    restore_mocks: typing.Optional[builtins.bool] = None,
    root_dir: typing.Optional[builtins.str] = None,
    roots: typing.Optional[typing.Sequence[builtins.str]] = None,
    runner: typing.Optional[builtins.str] = None,
    setup_files: typing.Optional[typing.Sequence[builtins.str]] = None,
    setup_files_after_env: typing.Optional[typing.Sequence[builtins.str]] = None,
    slow_test_threshold: typing.Optional[jsii.Number] = None,
    snapshot_resolver: typing.Optional[builtins.str] = None,
    snapshot_serializers: typing.Optional[typing.Sequence[builtins.str]] = None,
    test_environment: typing.Optional[builtins.str] = None,
    test_environment_options: typing.Any = None,
    test_failure_exit_code: typing.Optional[jsii.Number] = None,
    test_match: typing.Optional[typing.Sequence[builtins.str]] = None,
    test_path_ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    test_regex: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    test_results_processor: typing.Optional[builtins.str] = None,
    test_runner: typing.Optional[builtins.str] = None,
    test_sequencer: typing.Optional[builtins.str] = None,
    test_timeout: typing.Optional[jsii.Number] = None,
    test_url: typing.Optional[builtins.str] = None,
    timers: typing.Optional[builtins.str] = None,
    transform: typing.Optional[typing.Mapping[builtins.str, Transform]] = None,
    transform_ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    unmocked_module_path_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    verbose: typing.Optional[builtins.bool] = None,
    watchman: typing.Optional[builtins.bool] = None,
    watch_path_ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    watch_plugins: typing.Optional[typing.Sequence[WatchPlugin]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fea73c8bcc51e881c3829384cb90956e3310a1a08296d32da54fc51bd1b0872(
    *,
    config_file_path: typing.Optional[builtins.str] = None,
    coverage: typing.Optional[builtins.bool] = None,
    coverage_text: typing.Optional[builtins.bool] = None,
    extra_cli_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    jest_config: typing.Optional[typing.Union[JestConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    jest_version: typing.Optional[builtins.str] = None,
    junit_reporting: typing.Optional[builtins.bool] = None,
    preserve_default_reporters: typing.Optional[builtins.bool] = None,
    update_snapshot: typing.Optional[UpdateSnapshot] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1adfce4c8efbbf8de3e660eb3dc3c2d165cf8436faf2119d2f15900dda8e814a(
    name: builtins.str,
    options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10cd20471c8ed8e2de153476379f00bfa1b587c92e8982006812a0e3e9c846b(
    project: _Project_57d89203,
    *,
    allow_library_dependencies: typing.Optional[builtins.bool] = None,
    author_email: typing.Optional[builtins.str] = None,
    author_name: typing.Optional[builtins.str] = None,
    author_organization: typing.Optional[builtins.bool] = None,
    author_url: typing.Optional[builtins.str] = None,
    auto_detect_bin: typing.Optional[builtins.bool] = None,
    bin: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bugs_email: typing.Optional[builtins.str] = None,
    bugs_url: typing.Optional[builtins.str] = None,
    bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    code_artifact_options: typing.Optional[typing.Union[CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    entrypoint: typing.Optional[builtins.str] = None,
    homepage: typing.Optional[builtins.str] = None,
    keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
    license: typing.Optional[builtins.str] = None,
    licensed: typing.Optional[builtins.bool] = None,
    max_node_version: typing.Optional[builtins.str] = None,
    min_node_version: typing.Optional[builtins.str] = None,
    npm_access: typing.Optional[NpmAccess] = None,
    npm_registry: typing.Optional[builtins.str] = None,
    npm_registry_url: typing.Optional[builtins.str] = None,
    npm_token_secret: typing.Optional[builtins.str] = None,
    package_manager: typing.Optional[NodePackageManager] = None,
    package_name: typing.Optional[builtins.str] = None,
    peer_dependency_options: typing.Optional[typing.Union[PeerDependencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    peer_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    pnpm_version: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    repository_directory: typing.Optional[builtins.str] = None,
    scoped_packages_options: typing.Optional[typing.Sequence[typing.Union[ScopedPackagesOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    scripts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    stability: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e4b0ad9e59ff790a5783923af9f1d0af9bff2ab30e03185a659093189f08f3(
    bins: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f25a81261c7551ce7372a9e98c98143fde0ccda688f4a7f1b1d64783c6fa198(
    *deps: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66a164e21aa660923f1f9ca9a679f353501f43d2c6de87372bb0dadcc74e863(
    *deps: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80cd6a4a71ddbf3dcbb4c76baab6b84aa13c5bb5b4e36d4e51cb18378a0d733d(
    *deps: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944e49e6183bbfb83f5284a94826a5dc27eb1d8daf9f1c782135dc5893acfcae(
    engine: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85137a3059fcbe1e4bfe64a7b2d097445ae0743f4ff0ecde43a1c4cefbeafa7a(
    name: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a4904c7ed7ae8a2b9f8ade987155393a1f966700d60dc9e833e6615cc57118b(
    *keywords: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bc2a812647b8c3d299d563a0f6381c44edd2be02fb67a3dcd27d127bb238ba5(
    *resolutions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665c114cee41c00dba6a88193e09aacf3c44c03eeb33f5248f4a0715ee25f803(
    *deps: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d456bed502e180a081411555ef7dae9f59ac8b07e536f2a144d134c8593a095(
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12c7fbb63b42bcfe1afac4c97478186870515282ad2fec02e2dfe5256265514(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfa2462931cf54e94ef49bfaf6682ca11a2539f8cdd625d39c838f78b350e770(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17ecc6ba7925a0e02706203a5f4f1888b6b3708f11e2bc0aab1ce1b5343b5ea(
    name: builtins.str,
    command: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29de3cb9e10a8965e109e3d914eff0debf87b70a39d82f150168063dd734ac03(
    dependency_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32555a77b63910142de45100c4a6d74880ddece00a3cbae9c278034675668ea0(
    *,
    allow_library_dependencies: typing.Optional[builtins.bool] = None,
    author_email: typing.Optional[builtins.str] = None,
    author_name: typing.Optional[builtins.str] = None,
    author_organization: typing.Optional[builtins.bool] = None,
    author_url: typing.Optional[builtins.str] = None,
    auto_detect_bin: typing.Optional[builtins.bool] = None,
    bin: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bugs_email: typing.Optional[builtins.str] = None,
    bugs_url: typing.Optional[builtins.str] = None,
    bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    code_artifact_options: typing.Optional[typing.Union[CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    entrypoint: typing.Optional[builtins.str] = None,
    homepage: typing.Optional[builtins.str] = None,
    keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
    license: typing.Optional[builtins.str] = None,
    licensed: typing.Optional[builtins.bool] = None,
    max_node_version: typing.Optional[builtins.str] = None,
    min_node_version: typing.Optional[builtins.str] = None,
    npm_access: typing.Optional[NpmAccess] = None,
    npm_registry: typing.Optional[builtins.str] = None,
    npm_registry_url: typing.Optional[builtins.str] = None,
    npm_token_secret: typing.Optional[builtins.str] = None,
    package_manager: typing.Optional[NodePackageManager] = None,
    package_name: typing.Optional[builtins.str] = None,
    peer_dependency_options: typing.Optional[typing.Union[PeerDependencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    peer_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    pnpm_version: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    repository_directory: typing.Optional[builtins.str] = None,
    scoped_packages_options: typing.Optional[typing.Sequence[typing.Union[ScopedPackagesOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    scripts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    stability: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0850dc1bf763fca52fa1a885d8979a0b159e53cb34c36ec7df070d31707319(
    bins: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b1ff4594cefe0f3ab31e92f5ac8583fbe3df4f5ba62df16850e03b36a3c4161(
    *deps: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b059cfc104068a0054d877fddb1a1af37e0a7e039d5c911c34d1119017de502e(
    *commands: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b576514c0c963fa1e2e9fd3f1e8c1815cf1421fec5e99d2ac2eef18555fb9f9(
    *deps: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c2f5af66b63e317689cb319c22794a60ef4c8c60f02bab83df451259bfd266(
    *deps: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aefed21bd0a280406323e1e4bb1ad79ba060becec09ea745a15f9de0ff27c701(
    fields: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae4903fb76e287886deb4a0fc6eda837b193a8386de55770a9b5ff3203549b2(
    *keywords: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75374e653c3f5969c1d17e74843bf9de7c8b57c83155a5d8f2054617e584c587(
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed50dcce11d164846dc05e1944054760e40bc33bcad4ed78ac8fc35bee9ca41b(
    *deps: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67b7bc6c222da42e565aff91a82f7ebf8f7da5dfb913473bab13597487a1322(
    scripts: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__260e615a7142e436fcdeda572a6911528eb33c495f725efeb25c208eed3d88a0(
    *commands: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a96d563d99caecd8428704d41d3b4f2d83e16d8cf2c5b251709f03f0482f5d8(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__224de74cc912dc2ec9fe8eebc20f7a52b63c2e04ee88bb72ef9f775a2d8b33ab(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0dba0b4edb6058c71da788f75e31bbfa6a73ef88319ba1c5fbe6f3606470049(
    task: _Task_9fa875b6,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4eb807c608f50b2ade2ec2fbbb9f5443b474a504acfa34e6cf39edb04ad208(
    name: builtins.str,
    command: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c2eb8aa04095bbe6af788737363089516ccd341e3a6624f153e8ff7eeaee29(
    *,
    name: builtins.str,
    commit_generated: typing.Optional[builtins.bool] = None,
    git_ignore_options: typing.Optional[typing.Union[_IgnoreFileOptions_86c48b91, typing.Dict[builtins.str, typing.Any]]] = None,
    git_options: typing.Optional[typing.Union[_GitOptions_a65916a3, typing.Dict[builtins.str, typing.Any]]] = None,
    logging: typing.Optional[typing.Union[_LoggerOptions_eb0f6309, typing.Dict[builtins.str, typing.Any]]] = None,
    outdir: typing.Optional[builtins.str] = None,
    parent: typing.Optional[_Project_57d89203] = None,
    projen_command: typing.Optional[builtins.str] = None,
    projenrc_json: typing.Optional[builtins.bool] = None,
    projenrc_json_options: typing.Optional[typing.Union[_ProjenrcJsonOptions_9c40dd4f, typing.Dict[builtins.str, typing.Any]]] = None,
    renovatebot: typing.Optional[builtins.bool] = None,
    renovatebot_options: typing.Optional[typing.Union[_RenovatebotOptions_18e6b8a1, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_approve_options: typing.Optional[typing.Union[_AutoApproveOptions_dac86cbe, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_merge: typing.Optional[builtins.bool] = None,
    auto_merge_options: typing.Optional[typing.Union[_AutoMergeOptions_d112cd3c, typing.Dict[builtins.str, typing.Any]]] = None,
    clobber: typing.Optional[builtins.bool] = None,
    dev_container: typing.Optional[builtins.bool] = None,
    github: typing.Optional[builtins.bool] = None,
    github_options: typing.Optional[typing.Union[_GitHubOptions_21553699, typing.Dict[builtins.str, typing.Any]]] = None,
    gitpod: typing.Optional[builtins.bool] = None,
    mergify: typing.Optional[builtins.bool] = None,
    mergify_options: typing.Optional[typing.Union[_MergifyOptions_a6faaab3, typing.Dict[builtins.str, typing.Any]]] = None,
    project_type: typing.Optional[_ProjectType_fd80c725] = None,
    projen_credentials: typing.Optional[_GithubCredentials_ae257072] = None,
    projen_token_secret: typing.Optional[builtins.str] = None,
    readme: typing.Optional[typing.Union[_SampleReadmeProps_3518b03b, typing.Dict[builtins.str, typing.Any]]] = None,
    stale: typing.Optional[builtins.bool] = None,
    stale_options: typing.Optional[typing.Union[_StaleOptions_929db764, typing.Dict[builtins.str, typing.Any]]] = None,
    vscode: typing.Optional[builtins.bool] = None,
    allow_library_dependencies: typing.Optional[builtins.bool] = None,
    author_email: typing.Optional[builtins.str] = None,
    author_name: typing.Optional[builtins.str] = None,
    author_organization: typing.Optional[builtins.bool] = None,
    author_url: typing.Optional[builtins.str] = None,
    auto_detect_bin: typing.Optional[builtins.bool] = None,
    bin: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bugs_email: typing.Optional[builtins.str] = None,
    bugs_url: typing.Optional[builtins.str] = None,
    bundled_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    code_artifact_options: typing.Optional[typing.Union[CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    entrypoint: typing.Optional[builtins.str] = None,
    homepage: typing.Optional[builtins.str] = None,
    keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
    license: typing.Optional[builtins.str] = None,
    licensed: typing.Optional[builtins.bool] = None,
    max_node_version: typing.Optional[builtins.str] = None,
    min_node_version: typing.Optional[builtins.str] = None,
    npm_access: typing.Optional[NpmAccess] = None,
    npm_registry: typing.Optional[builtins.str] = None,
    npm_registry_url: typing.Optional[builtins.str] = None,
    npm_token_secret: typing.Optional[builtins.str] = None,
    package_manager: typing.Optional[NodePackageManager] = None,
    package_name: typing.Optional[builtins.str] = None,
    peer_dependency_options: typing.Optional[typing.Union[PeerDependencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    peer_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    pnpm_version: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    repository_directory: typing.Optional[builtins.str] = None,
    scoped_packages_options: typing.Optional[typing.Sequence[typing.Union[ScopedPackagesOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    scripts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    stability: typing.Optional[builtins.str] = None,
    jsii_release_version: typing.Optional[builtins.str] = None,
    major_version: typing.Optional[jsii.Number] = None,
    min_major_version: typing.Optional[jsii.Number] = None,
    npm_dist_tag: typing.Optional[builtins.str] = None,
    post_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    prerelease: typing.Optional[builtins.str] = None,
    publish_dry_run: typing.Optional[builtins.bool] = None,
    publish_tasks: typing.Optional[builtins.bool] = None,
    releasable_commits: typing.Optional[_ReleasableCommits_d481ce10] = None,
    release_branches: typing.Optional[typing.Mapping[builtins.str, typing.Union[_BranchOptions_13663d08, typing.Dict[builtins.str, typing.Any]]]] = None,
    release_every_commit: typing.Optional[builtins.bool] = None,
    release_failure_issue: typing.Optional[builtins.bool] = None,
    release_failure_issue_label: typing.Optional[builtins.str] = None,
    release_schedule: typing.Optional[builtins.str] = None,
    release_tag_prefix: typing.Optional[builtins.str] = None,
    release_trigger: typing.Optional[_ReleaseTrigger_e4dc221f] = None,
    release_workflow_name: typing.Optional[builtins.str] = None,
    release_workflow_setup_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    workflow_container_image: typing.Optional[builtins.str] = None,
    workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    workflow_runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
    default_release_branch: builtins.str,
    artifacts_directory: typing.Optional[builtins.str] = None,
    auto_approve_upgrades: typing.Optional[builtins.bool] = None,
    build_workflow: typing.Optional[builtins.bool] = None,
    build_workflow_triggers: typing.Optional[typing.Union[_Triggers_e9ae7617, typing.Dict[builtins.str, typing.Any]]] = None,
    bundler_options: typing.Optional[typing.Union[BundlerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    code_cov: typing.Optional[builtins.bool] = None,
    code_cov_token_secret: typing.Optional[builtins.str] = None,
    copyright_owner: typing.Optional[builtins.str] = None,
    copyright_period: typing.Optional[builtins.str] = None,
    dependabot: typing.Optional[builtins.bool] = None,
    dependabot_options: typing.Optional[typing.Union[_DependabotOptions_0cedc635, typing.Dict[builtins.str, typing.Any]]] = None,
    deps_upgrade: typing.Optional[builtins.bool] = None,
    deps_upgrade_options: typing.Optional[typing.Union[UpgradeDependenciesOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gitignore: typing.Optional[typing.Sequence[builtins.str]] = None,
    jest: typing.Optional[builtins.bool] = None,
    jest_options: typing.Optional[typing.Union[JestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    mutable_build: typing.Optional[builtins.bool] = None,
    npmignore: typing.Optional[typing.Sequence[builtins.str]] = None,
    npmignore_enabled: typing.Optional[builtins.bool] = None,
    npm_ignore_options: typing.Optional[typing.Union[_IgnoreFileOptions_86c48b91, typing.Dict[builtins.str, typing.Any]]] = None,
    package: typing.Optional[builtins.bool] = None,
    prettier: typing.Optional[builtins.bool] = None,
    prettier_options: typing.Optional[typing.Union[PrettierOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projen_dev_dependency: typing.Optional[builtins.bool] = None,
    projenrc_js: typing.Optional[builtins.bool] = None,
    projenrc_js_options: typing.Optional[typing.Union[ProjenrcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projen_version: typing.Optional[builtins.str] = None,
    pull_request_template: typing.Optional[builtins.bool] = None,
    pull_request_template_contents: typing.Optional[typing.Sequence[builtins.str]] = None,
    release: typing.Optional[builtins.bool] = None,
    release_to_npm: typing.Optional[builtins.bool] = None,
    release_workflow: typing.Optional[builtins.bool] = None,
    workflow_bootstrap_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    workflow_git_identity: typing.Optional[typing.Union[_GitIdentity_6effc3de, typing.Dict[builtins.str, typing.Any]]] = None,
    workflow_node_version: typing.Optional[builtins.str] = None,
    workflow_package_cache: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b746251f1b75ba953324566d41e0b8f83e1f3c11b8bdc5916f09fd559914d7(
    project: NodeProject,
    *,
    omit_empty: typing.Optional[builtins.bool] = None,
    registry: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ffe4a0f2f0471b68c6ec185cbf4f5c192b37a79c19e45ac41370d2378eff782(
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921c1baed18b2592b0599b66374de0e67495b5712f0889a23b2f5fd572fa7378(
    url: builtins.str,
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572f231bc39b987387ccaf3d47dab1ff17bcba6b190a9675a89313a364b340f6(
    *,
    omit_empty: typing.Optional[builtins.bool] = None,
    registry: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc70f793ab1a81781f2ffafe90b1661555f4fb8d4aeb489bcb926e034f01a743(
    *,
    pinned_dev_dependency: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc54704eb480a73e451f86bffd16f1d9313443e3d2f9b556889330fd0715ad95(
    project: NodeProject,
    *,
    ignore_file: typing.Optional[builtins.bool] = None,
    ignore_file_options: typing.Optional[typing.Union[_IgnoreFileOptions_86c48b91, typing.Dict[builtins.str, typing.Any]]] = None,
    overrides: typing.Optional[typing.Sequence[typing.Union[PrettierOverride, typing.Dict[builtins.str, typing.Any]]]] = None,
    settings: typing.Optional[typing.Union[PrettierSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    yaml: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1fd367ba7a3d51b9e260e79983f7d6fb9647a9bad81693c033d3218ba83e83f(
    project: _Project_57d89203,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__564118067a14c8c300f791c1ea85edc55544d5c6098386e20c2b6bc3e7b10df4(
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83f36238b807da08b92be98c6d4956285442f99303983562db38dda7f23c13ae(
    *,
    ignore_file: typing.Optional[builtins.bool] = None,
    ignore_file_options: typing.Optional[typing.Union[_IgnoreFileOptions_86c48b91, typing.Dict[builtins.str, typing.Any]]] = None,
    overrides: typing.Optional[typing.Sequence[typing.Union[PrettierOverride, typing.Dict[builtins.str, typing.Any]]]] = None,
    settings: typing.Optional[typing.Union[PrettierSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    yaml: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bbdf8c18a86fcbd11c29b6e1ec1c6cb7b1e3a7ae688bedb8e25c15099f3e25e(
    *,
    files: typing.Union[builtins.str, typing.Sequence[builtins.str]],
    options: typing.Union[PrettierSettings, typing.Dict[builtins.str, typing.Any]],
    exclude_files: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887661cb2874a1d4a18112ca0d8607d9340a20c3becbf5d16df966a4dfda6434(
    *,
    arrow_parens: typing.Optional[ArrowParens] = None,
    bracket_same_line: typing.Optional[builtins.bool] = None,
    bracket_spacing: typing.Optional[builtins.bool] = None,
    cursor_offset: typing.Optional[jsii.Number] = None,
    embedded_language_formatting: typing.Optional[EmbeddedLanguageFormatting] = None,
    end_of_line: typing.Optional[EndOfLine] = None,
    filepath: typing.Optional[builtins.str] = None,
    html_whitespace_sensitivity: typing.Optional[HTMLWhitespaceSensitivity] = None,
    insert_pragma: typing.Optional[builtins.bool] = None,
    jsx_single_quote: typing.Optional[builtins.bool] = None,
    parser: typing.Optional[builtins.str] = None,
    plugins: typing.Optional[typing.Sequence[builtins.str]] = None,
    plugin_search_dirs: typing.Optional[typing.Sequence[builtins.str]] = None,
    print_width: typing.Optional[jsii.Number] = None,
    prose_wrap: typing.Optional[ProseWrap] = None,
    quote_props: typing.Optional[QuoteProps] = None,
    range_end: typing.Optional[jsii.Number] = None,
    range_start: typing.Optional[jsii.Number] = None,
    require_pragma: typing.Optional[builtins.bool] = None,
    semi: typing.Optional[builtins.bool] = None,
    single_quote: typing.Optional[builtins.bool] = None,
    tab_width: typing.Optional[jsii.Number] = None,
    trailing_comma: typing.Optional[TrailingComma] = None,
    use_tabs: typing.Optional[builtins.bool] = None,
    vue_indent_script_and_style: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aaddb790f6b7d088afb273f85e8c279374e3017865fb4c91b0780864fb6e306(
    project: _Project_57d89203,
    *,
    filename: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c3b878e5a2d5b01df88ea94af1a0f3f101f4340d3dba514d5e748ef2f199f6(
    *,
    filename: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7894334d4e6bef30e70628d87bf6b8f27ab4cf85a14e93ed26d04abcba1356d(
    *,
    mutable: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c6e79d2b5de89d5ea21ca58635c0e3f3ed941e2f5533f9365aca8c6bac689e(
    *,
    registry_url: builtins.str,
    scope: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b434df824fd38c8bd7ed7eb8a8cf4f2f0559fd4c13a28bd06bd0f481c6389984(
    name: builtins.str,
    options: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3368fe3a3107764de1a64c16f7fe4c15d510477a888b2a74df2afb14b632c7e(
    *,
    allow_arbitrary_extensions: typing.Optional[builtins.bool] = None,
    allow_importing_ts_extensions: typing.Optional[builtins.bool] = None,
    allow_js: typing.Optional[builtins.bool] = None,
    allow_synthetic_default_imports: typing.Optional[builtins.bool] = None,
    always_strict: typing.Optional[builtins.bool] = None,
    base_url: typing.Optional[builtins.str] = None,
    custom_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
    declaration: typing.Optional[builtins.bool] = None,
    declaration_dir: typing.Optional[builtins.str] = None,
    emit_declaration_only: typing.Optional[builtins.bool] = None,
    emit_decorator_metadata: typing.Optional[builtins.bool] = None,
    es_module_interop: typing.Optional[builtins.bool] = None,
    exact_optional_property_types: typing.Optional[builtins.bool] = None,
    experimental_decorators: typing.Optional[builtins.bool] = None,
    force_consistent_casing_in_file_names: typing.Optional[builtins.bool] = None,
    imports_not_used_as_values: typing.Optional[TypeScriptImportsNotUsedAsValues] = None,
    inline_source_map: typing.Optional[builtins.bool] = None,
    inline_sources: typing.Optional[builtins.bool] = None,
    isolated_modules: typing.Optional[builtins.bool] = None,
    jsx: typing.Optional[TypeScriptJsxMode] = None,
    jsx_import_source: typing.Optional[builtins.str] = None,
    lib: typing.Optional[typing.Sequence[builtins.str]] = None,
    module: typing.Optional[builtins.str] = None,
    module_resolution: typing.Optional[TypeScriptModuleResolution] = None,
    no_emit: typing.Optional[builtins.bool] = None,
    no_emit_on_error: typing.Optional[builtins.bool] = None,
    no_fallthrough_cases_in_switch: typing.Optional[builtins.bool] = None,
    no_implicit_any: typing.Optional[builtins.bool] = None,
    no_implicit_override: typing.Optional[builtins.bool] = None,
    no_implicit_returns: typing.Optional[builtins.bool] = None,
    no_implicit_this: typing.Optional[builtins.bool] = None,
    no_property_access_from_index_signature: typing.Optional[builtins.bool] = None,
    no_unchecked_indexed_access: typing.Optional[builtins.bool] = None,
    no_unused_locals: typing.Optional[builtins.bool] = None,
    no_unused_parameters: typing.Optional[builtins.bool] = None,
    out_dir: typing.Optional[builtins.str] = None,
    paths: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
    resolve_json_module: typing.Optional[builtins.bool] = None,
    resolve_package_json_exports: typing.Optional[builtins.bool] = None,
    resolve_package_json_imports: typing.Optional[builtins.bool] = None,
    root_dir: typing.Optional[builtins.str] = None,
    skip_lib_check: typing.Optional[builtins.bool] = None,
    source_map: typing.Optional[builtins.bool] = None,
    source_root: typing.Optional[builtins.str] = None,
    strict: typing.Optional[builtins.bool] = None,
    strict_null_checks: typing.Optional[builtins.bool] = None,
    strict_property_initialization: typing.Optional[builtins.bool] = None,
    strip_internal: typing.Optional[builtins.bool] = None,
    target: typing.Optional[builtins.str] = None,
    use_unknown_in_catch_variables: typing.Optional[builtins.bool] = None,
    verbatim_module_syntax: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdd8e9cd126102b8184e52538d49523cef64724ec6ad410a5e2d5169e1ef0fe0(
    project: _Project_57d89203,
    *,
    compiler_options: typing.Union[TypeScriptCompilerOptions, typing.Dict[builtins.str, typing.Any]],
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    extends: typing.Optional[TypescriptConfigExtends] = None,
    file_name: typing.Optional[builtins.str] = None,
    include: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22043cd196520a238283f3d057c0a0a29f8679bf2501608e058f551552b3a6c5(
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19373d5818f12b8d7ae04b7e689d8a06b0470d6eb5c5886f5a9255a0221fd9f(
    value: TypescriptConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc6431d5d9f322d469f99e5739da10bb780beb09da03305a82dac281906fc5b(
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b076d47872be6e9462b52280fba0e6d5509d09e6f0c405542d8edb8b704f3d(
    config_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b13693458818b040e6f9da122d60b4f324f8ab7721d6eb1c08300c101500f0aa(
    paths: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb44c1fe8356fe5ed46d657b7a5c3f2198926eaf1f5780cf30a365a3e170a5e(
    configs: typing.Sequence[TypescriptConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f928658806d66c2cd4f3977b17ae3d10092cf4b9afb10e736c01729b7451dbb9(
    *,
    compiler_options: typing.Union[TypeScriptCompilerOptions, typing.Dict[builtins.str, typing.Any]],
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    extends: typing.Optional[TypescriptConfigExtends] = None,
    file_name: typing.Optional[builtins.str] = None,
    include: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497e18a2c8dc3200cff8b21dfad7c418d29517aa6d67e2a2555ee78fa63ff385(
    project: NodeProject,
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    include: typing.Optional[typing.Sequence[builtins.str]] = None,
    pull_request_title: typing.Optional[builtins.str] = None,
    satisfy_peer_dependencies: typing.Optional[builtins.bool] = None,
    semantic_commit: typing.Optional[builtins.str] = None,
    signoff: typing.Optional[builtins.bool] = None,
    target: typing.Optional[builtins.str] = None,
    task_name: typing.Optional[builtins.str] = None,
    types: typing.Optional[typing.Sequence[_DependencyType_6b786d68]] = None,
    workflow: typing.Optional[builtins.bool] = None,
    workflow_options: typing.Optional[typing.Union[UpgradeDependenciesWorkflowOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff92c41406c3198455d1dfec862b6c0109c8239ff2a3eed09afaaaf67774467b(
    *steps: _JobStep_c3287c05,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ba20de6f144f37e582e192e3ed592a6be0e8bc3d10e3b730af62082afa0010(
    value: typing.Optional[_ContainerOptions_f50907af],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7b896c11469470869bc4bfc86c9bb13fd308223e316ba71124c00b5709af1e(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    include: typing.Optional[typing.Sequence[builtins.str]] = None,
    pull_request_title: typing.Optional[builtins.str] = None,
    satisfy_peer_dependencies: typing.Optional[builtins.bool] = None,
    semantic_commit: typing.Optional[builtins.str] = None,
    signoff: typing.Optional[builtins.bool] = None,
    target: typing.Optional[builtins.str] = None,
    task_name: typing.Optional[builtins.str] = None,
    types: typing.Optional[typing.Sequence[_DependencyType_6b786d68]] = None,
    workflow: typing.Optional[builtins.bool] = None,
    workflow_options: typing.Optional[typing.Union[UpgradeDependenciesWorkflowOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0616cac83033da3960c6645511af30fae841bea5f2cf5229410d6113065c8dd2(
    cron: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59fa39c2475322c21b2f7d03f2f2ada171b7e546b1d88beb8a75baa8238b629e(
    *,
    assignees: typing.Optional[typing.Sequence[builtins.str]] = None,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    container: typing.Optional[typing.Union[_ContainerOptions_f50907af, typing.Dict[builtins.str, typing.Any]]] = None,
    git_identity: typing.Optional[typing.Union[_GitIdentity_6effc3de, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    permissions: typing.Optional[typing.Union[_JobPermissions_3b5b53dc, typing.Dict[builtins.str, typing.Any]]] = None,
    projen_credentials: typing.Optional[_GithubCredentials_ae257072] = None,
    runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: typing.Optional[UpgradeDependenciesSchedule] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82731b5aeb15fc642017d0dee706d4e02c814dbcf91efe82eb0ac07b490a354a(
    name: builtins.str,
    options: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda879bb1fe52a68839c7634ab5ab9f2cedf7154361c8a0487248d72bab68e62(
    *,
    externals: typing.Optional[typing.Sequence[builtins.str]] = None,
    sourcemap: typing.Optional[builtins.bool] = None,
    watch_task: typing.Optional[builtins.bool] = None,
    platform: builtins.str,
    target: builtins.str,
    executable: typing.Optional[builtins.bool] = None,
    loaders: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    outfile: typing.Optional[builtins.str] = None,
    tsconfig_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
