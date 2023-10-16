'''
# `vault_pki_secret_backend_issuer`

Refer to the Terraform Registory for docs: [`vault_pki_secret_backend_issuer`](https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer).
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class PkiSecretBackendIssuer(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.pkiSecretBackendIssuer.PkiSecretBackendIssuer",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer vault_pki_secret_backend_issuer}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        backend: builtins.str,
        issuer_ref: builtins.str,
        crl_distribution_points: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_aia_url_templating: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        issuer_name: typing.Optional[builtins.str] = None,
        issuing_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
        leaf_not_after_behavior: typing.Optional[builtins.str] = None,
        manual_chain: typing.Optional[typing.Sequence[builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
        ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        revocation_signature_algorithm: typing.Optional[builtins.str] = None,
        usage: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer vault_pki_secret_backend_issuer} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param backend: Full path where PKI backend is mounted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#backend PkiSecretBackendIssuer#backend}
        :param issuer_ref: Reference to an existing issuer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#issuer_ref PkiSecretBackendIssuer#issuer_ref}
        :param crl_distribution_points: Specifies the URL values for the CRL Distribution Points field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#crl_distribution_points PkiSecretBackendIssuer#crl_distribution_points}
        :param enable_aia_url_templating: Specifies that the AIA URL values should be templated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#enable_aia_url_templating PkiSecretBackendIssuer#enable_aia_url_templating}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#id PkiSecretBackendIssuer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issuer_name: Reference to an existing issuer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#issuer_name PkiSecretBackendIssuer#issuer_name}
        :param issuing_certificates: Specifies the URL values for the Issuing Certificate field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#issuing_certificates PkiSecretBackendIssuer#issuing_certificates}
        :param leaf_not_after_behavior: Behavior of a leaf's 'NotAfter' field during issuance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#leaf_not_after_behavior PkiSecretBackendIssuer#leaf_not_after_behavior}
        :param manual_chain: Chain of issuer references to build this issuer's computed CAChain field from, when non-empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#manual_chain PkiSecretBackendIssuer#manual_chain}
        :param namespace: Target namespace. (requires Enterprise). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#namespace PkiSecretBackendIssuer#namespace}
        :param ocsp_servers: Specifies the URL values for the OCSP Servers field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#ocsp_servers PkiSecretBackendIssuer#ocsp_servers}
        :param revocation_signature_algorithm: Which signature algorithm to use when building CRLs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#revocation_signature_algorithm PkiSecretBackendIssuer#revocation_signature_algorithm}
        :param usage: Comma-separated list of allowed usages for this issuer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#usage PkiSecretBackendIssuer#usage}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1cdacd40fd82f5bbaa9ebb684ebd88dfa68566d289fec9a100f7112fcae72d8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PkiSecretBackendIssuerConfig(
            backend=backend,
            issuer_ref=issuer_ref,
            crl_distribution_points=crl_distribution_points,
            enable_aia_url_templating=enable_aia_url_templating,
            id=id,
            issuer_name=issuer_name,
            issuing_certificates=issuing_certificates,
            leaf_not_after_behavior=leaf_not_after_behavior,
            manual_chain=manual_chain,
            namespace=namespace,
            ocsp_servers=ocsp_servers,
            revocation_signature_algorithm=revocation_signature_algorithm,
            usage=usage,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetCrlDistributionPoints")
    def reset_crl_distribution_points(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrlDistributionPoints", []))

    @jsii.member(jsii_name="resetEnableAiaUrlTemplating")
    def reset_enable_aia_url_templating(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAiaUrlTemplating", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIssuerName")
    def reset_issuer_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuerName", []))

    @jsii.member(jsii_name="resetIssuingCertificates")
    def reset_issuing_certificates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuingCertificates", []))

    @jsii.member(jsii_name="resetLeafNotAfterBehavior")
    def reset_leaf_not_after_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLeafNotAfterBehavior", []))

    @jsii.member(jsii_name="resetManualChain")
    def reset_manual_chain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManualChain", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetOcspServers")
    def reset_ocsp_servers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOcspServers", []))

    @jsii.member(jsii_name="resetRevocationSignatureAlgorithm")
    def reset_revocation_signature_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRevocationSignatureAlgorithm", []))

    @jsii.member(jsii_name="resetUsage")
    def reset_usage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsage", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="issuerId")
    def issuer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerId"))

    @builtins.property
    @jsii.member(jsii_name="backendInput")
    def backend_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backendInput"))

    @builtins.property
    @jsii.member(jsii_name="crlDistributionPointsInput")
    def crl_distribution_points_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "crlDistributionPointsInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAiaUrlTemplatingInput")
    def enable_aia_url_templating_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableAiaUrlTemplatingInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerNameInput")
    def issuer_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerRefInput")
    def issuer_ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerRefInput"))

    @builtins.property
    @jsii.member(jsii_name="issuingCertificatesInput")
    def issuing_certificates_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "issuingCertificatesInput"))

    @builtins.property
    @jsii.member(jsii_name="leafNotAfterBehaviorInput")
    def leaf_not_after_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "leafNotAfterBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="manualChainInput")
    def manual_chain_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "manualChainInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="ocspServersInput")
    def ocsp_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ocspServersInput"))

    @builtins.property
    @jsii.member(jsii_name="revocationSignatureAlgorithmInput")
    def revocation_signature_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "revocationSignatureAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="usageInput")
    def usage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usageInput"))

    @builtins.property
    @jsii.member(jsii_name="backend")
    def backend(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backend"))

    @backend.setter
    def backend(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aff29c2b9355fb814c38b8dc8e56fb5a54a81f0453512810e189bb69858b23e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backend", value)

    @builtins.property
    @jsii.member(jsii_name="crlDistributionPoints")
    def crl_distribution_points(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "crlDistributionPoints"))

    @crl_distribution_points.setter
    def crl_distribution_points(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5c92258cf8a763793d466dce96dccfb3442045cd7ad108b012b6f1c98edc48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crlDistributionPoints", value)

    @builtins.property
    @jsii.member(jsii_name="enableAiaUrlTemplating")
    def enable_aia_url_templating(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableAiaUrlTemplating"))

    @enable_aia_url_templating.setter
    def enable_aia_url_templating(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f057823ec05f7c65be797f7c17c4544da5ce38d2f23906523c1446d86787147e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAiaUrlTemplating", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ff3e4cec06003747940be7e0ff005cbdb564bc8c9f9bdc027c495578fed19e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="issuerName")
    def issuer_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerName"))

    @issuer_name.setter
    def issuer_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d436476c682ec8353f98abe1b56db11d91136fb907d03dcf1e8b033a366606a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerName", value)

    @builtins.property
    @jsii.member(jsii_name="issuerRef")
    def issuer_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerRef"))

    @issuer_ref.setter
    def issuer_ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a1af7a6b0f204ceb1b8565940045f645f6bf73eebff5462b384144f1b9e2895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerRef", value)

    @builtins.property
    @jsii.member(jsii_name="issuingCertificates")
    def issuing_certificates(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "issuingCertificates"))

    @issuing_certificates.setter
    def issuing_certificates(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58bfef5bf149f61b18f57671366d5972a33e4e9c37bbf42dea5f8f280814db0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuingCertificates", value)

    @builtins.property
    @jsii.member(jsii_name="leafNotAfterBehavior")
    def leaf_not_after_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "leafNotAfterBehavior"))

    @leaf_not_after_behavior.setter
    def leaf_not_after_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d764dfbab97a53071d1733eff54b82016f1ffdfb6dc3f66e8d00d32adcf28b2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "leafNotAfterBehavior", value)

    @builtins.property
    @jsii.member(jsii_name="manualChain")
    def manual_chain(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "manualChain"))

    @manual_chain.setter
    def manual_chain(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560a42fdaea42b11e270f67f78ac3dec259841715fb75d616801ba26423fd65c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manualChain", value)

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4039b0c1443eff195670cf0b2f7653ba1a22163abc7652368507bb2fa239dce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value)

    @builtins.property
    @jsii.member(jsii_name="ocspServers")
    def ocsp_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ocspServers"))

    @ocsp_servers.setter
    def ocsp_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc50b4928575b9b88d03c5843478117e38a7f6a33986573f23092c5fc743f979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ocspServers", value)

    @builtins.property
    @jsii.member(jsii_name="revocationSignatureAlgorithm")
    def revocation_signature_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revocationSignatureAlgorithm"))

    @revocation_signature_algorithm.setter
    def revocation_signature_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c4dcf329380fd370aff7cc20c6595cee6eeb26ad83e484a61d5f06082e34200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revocationSignatureAlgorithm", value)

    @builtins.property
    @jsii.member(jsii_name="usage")
    def usage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usage"))

    @usage.setter
    def usage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb5f149d6713db4aadff6c9f49c8d3ca4d463a25c4f7640aa3df91765faf5be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usage", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.pkiSecretBackendIssuer.PkiSecretBackendIssuerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "backend": "backend",
        "issuer_ref": "issuerRef",
        "crl_distribution_points": "crlDistributionPoints",
        "enable_aia_url_templating": "enableAiaUrlTemplating",
        "id": "id",
        "issuer_name": "issuerName",
        "issuing_certificates": "issuingCertificates",
        "leaf_not_after_behavior": "leafNotAfterBehavior",
        "manual_chain": "manualChain",
        "namespace": "namespace",
        "ocsp_servers": "ocspServers",
        "revocation_signature_algorithm": "revocationSignatureAlgorithm",
        "usage": "usage",
    },
)
class PkiSecretBackendIssuerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        backend: builtins.str,
        issuer_ref: builtins.str,
        crl_distribution_points: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_aia_url_templating: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        issuer_name: typing.Optional[builtins.str] = None,
        issuing_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
        leaf_not_after_behavior: typing.Optional[builtins.str] = None,
        manual_chain: typing.Optional[typing.Sequence[builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
        ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        revocation_signature_algorithm: typing.Optional[builtins.str] = None,
        usage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param backend: Full path where PKI backend is mounted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#backend PkiSecretBackendIssuer#backend}
        :param issuer_ref: Reference to an existing issuer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#issuer_ref PkiSecretBackendIssuer#issuer_ref}
        :param crl_distribution_points: Specifies the URL values for the CRL Distribution Points field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#crl_distribution_points PkiSecretBackendIssuer#crl_distribution_points}
        :param enable_aia_url_templating: Specifies that the AIA URL values should be templated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#enable_aia_url_templating PkiSecretBackendIssuer#enable_aia_url_templating}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#id PkiSecretBackendIssuer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issuer_name: Reference to an existing issuer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#issuer_name PkiSecretBackendIssuer#issuer_name}
        :param issuing_certificates: Specifies the URL values for the Issuing Certificate field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#issuing_certificates PkiSecretBackendIssuer#issuing_certificates}
        :param leaf_not_after_behavior: Behavior of a leaf's 'NotAfter' field during issuance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#leaf_not_after_behavior PkiSecretBackendIssuer#leaf_not_after_behavior}
        :param manual_chain: Chain of issuer references to build this issuer's computed CAChain field from, when non-empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#manual_chain PkiSecretBackendIssuer#manual_chain}
        :param namespace: Target namespace. (requires Enterprise). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#namespace PkiSecretBackendIssuer#namespace}
        :param ocsp_servers: Specifies the URL values for the OCSP Servers field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#ocsp_servers PkiSecretBackendIssuer#ocsp_servers}
        :param revocation_signature_algorithm: Which signature algorithm to use when building CRLs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#revocation_signature_algorithm PkiSecretBackendIssuer#revocation_signature_algorithm}
        :param usage: Comma-separated list of allowed usages for this issuer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#usage PkiSecretBackendIssuer#usage}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e3aa2e9543aa0e1a5be28a90df8defa00068c8dd452ee06e37b673c0f54f573)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument backend", value=backend, expected_type=type_hints["backend"])
            check_type(argname="argument issuer_ref", value=issuer_ref, expected_type=type_hints["issuer_ref"])
            check_type(argname="argument crl_distribution_points", value=crl_distribution_points, expected_type=type_hints["crl_distribution_points"])
            check_type(argname="argument enable_aia_url_templating", value=enable_aia_url_templating, expected_type=type_hints["enable_aia_url_templating"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument issuer_name", value=issuer_name, expected_type=type_hints["issuer_name"])
            check_type(argname="argument issuing_certificates", value=issuing_certificates, expected_type=type_hints["issuing_certificates"])
            check_type(argname="argument leaf_not_after_behavior", value=leaf_not_after_behavior, expected_type=type_hints["leaf_not_after_behavior"])
            check_type(argname="argument manual_chain", value=manual_chain, expected_type=type_hints["manual_chain"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument ocsp_servers", value=ocsp_servers, expected_type=type_hints["ocsp_servers"])
            check_type(argname="argument revocation_signature_algorithm", value=revocation_signature_algorithm, expected_type=type_hints["revocation_signature_algorithm"])
            check_type(argname="argument usage", value=usage, expected_type=type_hints["usage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backend": backend,
            "issuer_ref": issuer_ref,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if crl_distribution_points is not None:
            self._values["crl_distribution_points"] = crl_distribution_points
        if enable_aia_url_templating is not None:
            self._values["enable_aia_url_templating"] = enable_aia_url_templating
        if id is not None:
            self._values["id"] = id
        if issuer_name is not None:
            self._values["issuer_name"] = issuer_name
        if issuing_certificates is not None:
            self._values["issuing_certificates"] = issuing_certificates
        if leaf_not_after_behavior is not None:
            self._values["leaf_not_after_behavior"] = leaf_not_after_behavior
        if manual_chain is not None:
            self._values["manual_chain"] = manual_chain
        if namespace is not None:
            self._values["namespace"] = namespace
        if ocsp_servers is not None:
            self._values["ocsp_servers"] = ocsp_servers
        if revocation_signature_algorithm is not None:
            self._values["revocation_signature_algorithm"] = revocation_signature_algorithm
        if usage is not None:
            self._values["usage"] = usage

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def backend(self) -> builtins.str:
        '''Full path where PKI backend is mounted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#backend PkiSecretBackendIssuer#backend}
        '''
        result = self._values.get("backend")
        assert result is not None, "Required property 'backend' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def issuer_ref(self) -> builtins.str:
        '''Reference to an existing issuer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#issuer_ref PkiSecretBackendIssuer#issuer_ref}
        '''
        result = self._values.get("issuer_ref")
        assert result is not None, "Required property 'issuer_ref' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def crl_distribution_points(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the URL values for the CRL Distribution Points field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#crl_distribution_points PkiSecretBackendIssuer#crl_distribution_points}
        '''
        result = self._values.get("crl_distribution_points")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_aia_url_templating(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies that the AIA URL values should be templated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#enable_aia_url_templating PkiSecretBackendIssuer#enable_aia_url_templating}
        '''
        result = self._values.get("enable_aia_url_templating")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#id PkiSecretBackendIssuer#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuer_name(self) -> typing.Optional[builtins.str]:
        '''Reference to an existing issuer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#issuer_name PkiSecretBackendIssuer#issuer_name}
        '''
        result = self._values.get("issuer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuing_certificates(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the URL values for the Issuing Certificate field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#issuing_certificates PkiSecretBackendIssuer#issuing_certificates}
        '''
        result = self._values.get("issuing_certificates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def leaf_not_after_behavior(self) -> typing.Optional[builtins.str]:
        '''Behavior of a leaf's 'NotAfter' field during issuance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#leaf_not_after_behavior PkiSecretBackendIssuer#leaf_not_after_behavior}
        '''
        result = self._values.get("leaf_not_after_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manual_chain(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Chain of issuer references to build this issuer's computed CAChain field from, when non-empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#manual_chain PkiSecretBackendIssuer#manual_chain}
        '''
        result = self._values.get("manual_chain")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Target namespace. (requires Enterprise).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#namespace PkiSecretBackendIssuer#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ocsp_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the URL values for the OCSP Servers field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#ocsp_servers PkiSecretBackendIssuer#ocsp_servers}
        '''
        result = self._values.get("ocsp_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def revocation_signature_algorithm(self) -> typing.Optional[builtins.str]:
        '''Which signature algorithm to use when building CRLs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#revocation_signature_algorithm PkiSecretBackendIssuer#revocation_signature_algorithm}
        '''
        result = self._values.get("revocation_signature_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def usage(self) -> typing.Optional[builtins.str]:
        '''Comma-separated list of allowed usages for this issuer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.21.0/docs/resources/pki_secret_backend_issuer#usage PkiSecretBackendIssuer#usage}
        '''
        result = self._values.get("usage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PkiSecretBackendIssuerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PkiSecretBackendIssuer",
    "PkiSecretBackendIssuerConfig",
]

publication.publish()

def _typecheckingstub__b1cdacd40fd82f5bbaa9ebb684ebd88dfa68566d289fec9a100f7112fcae72d8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    backend: builtins.str,
    issuer_ref: builtins.str,
    crl_distribution_points: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_aia_url_templating: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    issuer_name: typing.Optional[builtins.str] = None,
    issuing_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
    leaf_not_after_behavior: typing.Optional[builtins.str] = None,
    manual_chain: typing.Optional[typing.Sequence[builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
    ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    revocation_signature_algorithm: typing.Optional[builtins.str] = None,
    usage: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff29c2b9355fb814c38b8dc8e56fb5a54a81f0453512810e189bb69858b23e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5c92258cf8a763793d466dce96dccfb3442045cd7ad108b012b6f1c98edc48(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f057823ec05f7c65be797f7c17c4544da5ce38d2f23906523c1446d86787147e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff3e4cec06003747940be7e0ff005cbdb564bc8c9f9bdc027c495578fed19e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d436476c682ec8353f98abe1b56db11d91136fb907d03dcf1e8b033a366606a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1af7a6b0f204ceb1b8565940045f645f6bf73eebff5462b384144f1b9e2895(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58bfef5bf149f61b18f57671366d5972a33e4e9c37bbf42dea5f8f280814db0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d764dfbab97a53071d1733eff54b82016f1ffdfb6dc3f66e8d00d32adcf28b2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560a42fdaea42b11e270f67f78ac3dec259841715fb75d616801ba26423fd65c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4039b0c1443eff195670cf0b2f7653ba1a22163abc7652368507bb2fa239dce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc50b4928575b9b88d03c5843478117e38a7f6a33986573f23092c5fc743f979(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4dcf329380fd370aff7cc20c6595cee6eeb26ad83e484a61d5f06082e34200(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb5f149d6713db4aadff6c9f49c8d3ca4d463a25c4f7640aa3df91765faf5be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e3aa2e9543aa0e1a5be28a90df8defa00068c8dd452ee06e37b673c0f54f573(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backend: builtins.str,
    issuer_ref: builtins.str,
    crl_distribution_points: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_aia_url_templating: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    issuer_name: typing.Optional[builtins.str] = None,
    issuing_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
    leaf_not_after_behavior: typing.Optional[builtins.str] = None,
    manual_chain: typing.Optional[typing.Sequence[builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
    ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    revocation_signature_algorithm: typing.Optional[builtins.str] = None,
    usage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
