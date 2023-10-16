'''
# cdk-amazon-chime-resources

![Experimental](https://img.shields.io/badge/experimental-important.svg?style=for-the-badge)

An AWS Cloud Development Kit (AWS CDK) construct library that allows you to provision Amazon Chime resources with npm and pypi.

## Background

Amazon Chime resources (Amazon Chime Messaging and Amazon Chime PSTN resources) are not natively available in AWS CloudFormation or AWS CDK. Therefore, in order to create these resources with AWS CDK, an AWS Lambda backed custom resource must be used. In an effort to simplify that process, this AWS CDK construct has been created. This AWS CDK construct will create a custom resource and associated Lambda and expose constructs that can be used to create corresponding resources. This construct includes resources for both Amazon Chime Messaging and Amazon Chime PSTN.

## Resources

* [Amazon Chime SDK PSTN Resources](PSTNRESOURCES.MD)
* [Amazon Chime SDK Messaging Resources](MESSAGINGRESOURCES.MD)
* [Amazon Chime SDK Media Insights Resources](MEDIAINSIGHTS.MD)

## Installing

To add to your AWS CDK package.json file:

```
yarn add cdk-amazon-chime-resources
```

## Version 3 Upgrade

Version 3.0 is a potentially breaking change that involves multiple upgrades and changes. Version 3.0 revises the deployment to streamline and make more efficient the multiple configurations. This should result in an increased speed of deployment. All namespaces were updated to the current `chime-sdk-voice`, `chime-sdk-messaging`, `chime-sdk-identity`, or `chime-sdk-media-pipelines` namespace. Along with these changes, IAM policies were reduced where possible. If you encounter issues, please open an Issue.

> Potential Breaking Change with Streaming Messaging Data
>
> As part of the namespace change, this has been updated:
>
> ```python
> const appInstance = new MessagingAppInstance(this, 'appInstance', {
>   name: 'MessagingAppInstanceExample',
> });
> appInstance.streaming([
>   {
>     dataType: MessagingDataType.CHANNEL,
>     resourceArn: kinesisStream.streamArn,
>   },
> ]);
> ```

## Not Supported Yet

This is a work in progress.

Features that are not supported yet:

* [ ] Amazon Chime Voice Connector Groups
* [ ] Amazon Chime Voice Connector Emergency Calling
* [ ] Updates to created resources

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for more information.

## License

This project is licensed under the Apache-2.0 License.
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

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="cdk-amazon-chime-resources.AlexaSkillStatus")
class AlexaSkillStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.AmazonTranscribeCallAnalyticsProcessorConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "language_code": "languageCode",
        "call_analytics_stream_categories": "callAnalyticsStreamCategories",
        "content_identification_type": "contentIdentificationType",
        "content_redaction_type": "contentRedactionType",
        "enable_partial_results_stabilization": "enablePartialResultsStabilization",
        "filter_partial_results": "filterPartialResults",
        "language_model_name": "languageModelName",
        "partial_results_stability": "partialResultsStability",
        "pii_entity_types": "piiEntityTypes",
        "post_call_analytics_settings": "postCallAnalyticsSettings",
        "vocabulary_filter_method": "vocabularyFilterMethod",
        "vocabulary_filter_name": "vocabularyFilterName",
        "vocabulary_name": "vocabularyName",
    },
)
class AmazonTranscribeCallAnalyticsProcessorConfiguration:
    def __init__(
        self,
        *,
        language_code: "LanguageCode",
        call_analytics_stream_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        content_identification_type: typing.Optional["ContentIdentificationType"] = None,
        content_redaction_type: typing.Optional["ContentRedactionType"] = None,
        enable_partial_results_stabilization: typing.Optional[builtins.bool] = None,
        filter_partial_results: typing.Optional[builtins.bool] = None,
        language_model_name: typing.Optional[builtins.str] = None,
        partial_results_stability: typing.Optional["PartialResultsStability"] = None,
        pii_entity_types: typing.Optional[builtins.str] = None,
        post_call_analytics_settings: typing.Optional[typing.Union["PostCallAnalyticsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        vocabulary_filter_method: typing.Optional["VocabularyFilterMethod"] = None,
        vocabulary_filter_name: typing.Optional[builtins.str] = None,
        vocabulary_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param language_code: 
        :param call_analytics_stream_categories: 
        :param content_identification_type: 
        :param content_redaction_type: 
        :param enable_partial_results_stabilization: 
        :param filter_partial_results: 
        :param language_model_name: 
        :param partial_results_stability: 
        :param pii_entity_types: 
        :param post_call_analytics_settings: 
        :param vocabulary_filter_method: 
        :param vocabulary_filter_name: 
        :param vocabulary_name: 
        '''
        if isinstance(post_call_analytics_settings, dict):
            post_call_analytics_settings = PostCallAnalyticsSettings(**post_call_analytics_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79208c31cb44a1d663acf03b7c40c60fbd13a5cfad1ac090cbfbcddd566f31f2)
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument call_analytics_stream_categories", value=call_analytics_stream_categories, expected_type=type_hints["call_analytics_stream_categories"])
            check_type(argname="argument content_identification_type", value=content_identification_type, expected_type=type_hints["content_identification_type"])
            check_type(argname="argument content_redaction_type", value=content_redaction_type, expected_type=type_hints["content_redaction_type"])
            check_type(argname="argument enable_partial_results_stabilization", value=enable_partial_results_stabilization, expected_type=type_hints["enable_partial_results_stabilization"])
            check_type(argname="argument filter_partial_results", value=filter_partial_results, expected_type=type_hints["filter_partial_results"])
            check_type(argname="argument language_model_name", value=language_model_name, expected_type=type_hints["language_model_name"])
            check_type(argname="argument partial_results_stability", value=partial_results_stability, expected_type=type_hints["partial_results_stability"])
            check_type(argname="argument pii_entity_types", value=pii_entity_types, expected_type=type_hints["pii_entity_types"])
            check_type(argname="argument post_call_analytics_settings", value=post_call_analytics_settings, expected_type=type_hints["post_call_analytics_settings"])
            check_type(argname="argument vocabulary_filter_method", value=vocabulary_filter_method, expected_type=type_hints["vocabulary_filter_method"])
            check_type(argname="argument vocabulary_filter_name", value=vocabulary_filter_name, expected_type=type_hints["vocabulary_filter_name"])
            check_type(argname="argument vocabulary_name", value=vocabulary_name, expected_type=type_hints["vocabulary_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "language_code": language_code,
        }
        if call_analytics_stream_categories is not None:
            self._values["call_analytics_stream_categories"] = call_analytics_stream_categories
        if content_identification_type is not None:
            self._values["content_identification_type"] = content_identification_type
        if content_redaction_type is not None:
            self._values["content_redaction_type"] = content_redaction_type
        if enable_partial_results_stabilization is not None:
            self._values["enable_partial_results_stabilization"] = enable_partial_results_stabilization
        if filter_partial_results is not None:
            self._values["filter_partial_results"] = filter_partial_results
        if language_model_name is not None:
            self._values["language_model_name"] = language_model_name
        if partial_results_stability is not None:
            self._values["partial_results_stability"] = partial_results_stability
        if pii_entity_types is not None:
            self._values["pii_entity_types"] = pii_entity_types
        if post_call_analytics_settings is not None:
            self._values["post_call_analytics_settings"] = post_call_analytics_settings
        if vocabulary_filter_method is not None:
            self._values["vocabulary_filter_method"] = vocabulary_filter_method
        if vocabulary_filter_name is not None:
            self._values["vocabulary_filter_name"] = vocabulary_filter_name
        if vocabulary_name is not None:
            self._values["vocabulary_name"] = vocabulary_name

    @builtins.property
    def language_code(self) -> "LanguageCode":
        result = self._values.get("language_code")
        assert result is not None, "Required property 'language_code' is missing"
        return typing.cast("LanguageCode", result)

    @builtins.property
    def call_analytics_stream_categories(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("call_analytics_stream_categories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def content_identification_type(
        self,
    ) -> typing.Optional["ContentIdentificationType"]:
        result = self._values.get("content_identification_type")
        return typing.cast(typing.Optional["ContentIdentificationType"], result)

    @builtins.property
    def content_redaction_type(self) -> typing.Optional["ContentRedactionType"]:
        result = self._values.get("content_redaction_type")
        return typing.cast(typing.Optional["ContentRedactionType"], result)

    @builtins.property
    def enable_partial_results_stabilization(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_partial_results_stabilization")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def filter_partial_results(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("filter_partial_results")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def language_model_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("language_model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partial_results_stability(self) -> typing.Optional["PartialResultsStability"]:
        result = self._values.get("partial_results_stability")
        return typing.cast(typing.Optional["PartialResultsStability"], result)

    @builtins.property
    def pii_entity_types(self) -> typing.Optional[builtins.str]:
        result = self._values.get("pii_entity_types")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_call_analytics_settings(
        self,
    ) -> typing.Optional["PostCallAnalyticsSettings"]:
        result = self._values.get("post_call_analytics_settings")
        return typing.cast(typing.Optional["PostCallAnalyticsSettings"], result)

    @builtins.property
    def vocabulary_filter_method(self) -> typing.Optional["VocabularyFilterMethod"]:
        result = self._values.get("vocabulary_filter_method")
        return typing.cast(typing.Optional["VocabularyFilterMethod"], result)

    @builtins.property
    def vocabulary_filter_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("vocabulary_filter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vocabulary_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("vocabulary_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AmazonTranscribeCallAnalyticsProcessorConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.AmazonTranscribeProcessorConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "language_code": "languageCode",
        "content_identification_type": "contentIdentificationType",
        "content_redaction_type": "contentRedactionType",
        "enable_partial_results_stabilization": "enablePartialResultsStabilization",
        "filter_partial_results": "filterPartialResults",
        "language_model_name": "languageModelName",
        "partial_results_stability": "partialResultsStability",
        "pii_entity_types": "piiEntityTypes",
        "show_speaker_label": "showSpeakerLabel",
        "vocabulary_filter_method": "vocabularyFilterMethod",
        "vocabulary_filter_name": "vocabularyFilterName",
        "vocabulary_name": "vocabularyName",
    },
)
class AmazonTranscribeProcessorConfiguration:
    def __init__(
        self,
        *,
        language_code: "LanguageCode",
        content_identification_type: typing.Optional["ContentIdentificationType"] = None,
        content_redaction_type: typing.Optional["ContentRedactionType"] = None,
        enable_partial_results_stabilization: typing.Optional[builtins.bool] = None,
        filter_partial_results: typing.Optional[builtins.bool] = None,
        language_model_name: typing.Optional[builtins.str] = None,
        partial_results_stability: typing.Optional["PartialResultsStability"] = None,
        pii_entity_types: typing.Optional[builtins.str] = None,
        show_speaker_label: typing.Optional[builtins.bool] = None,
        vocabulary_filter_method: typing.Optional["VocabularyFilterMethod"] = None,
        vocabulary_filter_name: typing.Optional[builtins.str] = None,
        vocabulary_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param language_code: 
        :param content_identification_type: 
        :param content_redaction_type: 
        :param enable_partial_results_stabilization: 
        :param filter_partial_results: 
        :param language_model_name: 
        :param partial_results_stability: 
        :param pii_entity_types: 
        :param show_speaker_label: 
        :param vocabulary_filter_method: 
        :param vocabulary_filter_name: 
        :param vocabulary_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6144a5c0e924118e78f03a8dfb38cc1521ec946a8703b571a6202c66cee502d)
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument content_identification_type", value=content_identification_type, expected_type=type_hints["content_identification_type"])
            check_type(argname="argument content_redaction_type", value=content_redaction_type, expected_type=type_hints["content_redaction_type"])
            check_type(argname="argument enable_partial_results_stabilization", value=enable_partial_results_stabilization, expected_type=type_hints["enable_partial_results_stabilization"])
            check_type(argname="argument filter_partial_results", value=filter_partial_results, expected_type=type_hints["filter_partial_results"])
            check_type(argname="argument language_model_name", value=language_model_name, expected_type=type_hints["language_model_name"])
            check_type(argname="argument partial_results_stability", value=partial_results_stability, expected_type=type_hints["partial_results_stability"])
            check_type(argname="argument pii_entity_types", value=pii_entity_types, expected_type=type_hints["pii_entity_types"])
            check_type(argname="argument show_speaker_label", value=show_speaker_label, expected_type=type_hints["show_speaker_label"])
            check_type(argname="argument vocabulary_filter_method", value=vocabulary_filter_method, expected_type=type_hints["vocabulary_filter_method"])
            check_type(argname="argument vocabulary_filter_name", value=vocabulary_filter_name, expected_type=type_hints["vocabulary_filter_name"])
            check_type(argname="argument vocabulary_name", value=vocabulary_name, expected_type=type_hints["vocabulary_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "language_code": language_code,
        }
        if content_identification_type is not None:
            self._values["content_identification_type"] = content_identification_type
        if content_redaction_type is not None:
            self._values["content_redaction_type"] = content_redaction_type
        if enable_partial_results_stabilization is not None:
            self._values["enable_partial_results_stabilization"] = enable_partial_results_stabilization
        if filter_partial_results is not None:
            self._values["filter_partial_results"] = filter_partial_results
        if language_model_name is not None:
            self._values["language_model_name"] = language_model_name
        if partial_results_stability is not None:
            self._values["partial_results_stability"] = partial_results_stability
        if pii_entity_types is not None:
            self._values["pii_entity_types"] = pii_entity_types
        if show_speaker_label is not None:
            self._values["show_speaker_label"] = show_speaker_label
        if vocabulary_filter_method is not None:
            self._values["vocabulary_filter_method"] = vocabulary_filter_method
        if vocabulary_filter_name is not None:
            self._values["vocabulary_filter_name"] = vocabulary_filter_name
        if vocabulary_name is not None:
            self._values["vocabulary_name"] = vocabulary_name

    @builtins.property
    def language_code(self) -> "LanguageCode":
        result = self._values.get("language_code")
        assert result is not None, "Required property 'language_code' is missing"
        return typing.cast("LanguageCode", result)

    @builtins.property
    def content_identification_type(
        self,
    ) -> typing.Optional["ContentIdentificationType"]:
        result = self._values.get("content_identification_type")
        return typing.cast(typing.Optional["ContentIdentificationType"], result)

    @builtins.property
    def content_redaction_type(self) -> typing.Optional["ContentRedactionType"]:
        result = self._values.get("content_redaction_type")
        return typing.cast(typing.Optional["ContentRedactionType"], result)

    @builtins.property
    def enable_partial_results_stabilization(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_partial_results_stabilization")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def filter_partial_results(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("filter_partial_results")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def language_model_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("language_model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partial_results_stability(self) -> typing.Optional["PartialResultsStability"]:
        result = self._values.get("partial_results_stability")
        return typing.cast(typing.Optional["PartialResultsStability"], result)

    @builtins.property
    def pii_entity_types(self) -> typing.Optional[builtins.str]:
        result = self._values.get("pii_entity_types")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def show_speaker_label(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("show_speaker_label")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vocabulary_filter_method(self) -> typing.Optional["VocabularyFilterMethod"]:
        result = self._values.get("vocabulary_filter_method")
        return typing.cast(typing.Optional["VocabularyFilterMethod"], result)

    @builtins.property
    def vocabulary_filter_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("vocabulary_filter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vocabulary_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("vocabulary_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AmazonTranscribeProcessorConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.AppInstanceAdminProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_instance_admin_arn": "appInstanceAdminArn",
        "app_instance_arn": "appInstanceArn",
    },
)
class AppInstanceAdminProps:
    def __init__(
        self,
        *,
        app_instance_admin_arn: builtins.str,
        app_instance_arn: builtins.str,
    ) -> None:
        '''Props for ``AppInstance``.

        :param app_instance_admin_arn: The name of the app instance. Default: - None
        :param app_instance_arn: The name of the app instance. Default: - None
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8613bd8924c62f360b8fd11191005b6b40de3e5805e2906daf559c0c4591022d)
            check_type(argname="argument app_instance_admin_arn", value=app_instance_admin_arn, expected_type=type_hints["app_instance_admin_arn"])
            check_type(argname="argument app_instance_arn", value=app_instance_arn, expected_type=type_hints["app_instance_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_instance_admin_arn": app_instance_admin_arn,
            "app_instance_arn": app_instance_arn,
        }

    @builtins.property
    def app_instance_admin_arn(self) -> builtins.str:
        '''The name of the app instance.

        :default: - None
        '''
        result = self._values.get("app_instance_admin_arn")
        assert result is not None, "Required property 'app_instance_admin_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_instance_arn(self) -> builtins.str:
        '''The name of the app instance.

        :default: - None
        '''
        result = self._values.get("app_instance_arn")
        assert result is not None, "Required property 'app_instance_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppInstanceAdminProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.AppInstanceBotConfiguration",
    jsii_struct_bases=[],
    name_mapping={"lex": "lex"},
)
class AppInstanceBotConfiguration:
    def __init__(
        self,
        *,
        lex: typing.Union["AppInstanceBotLexConfiguration", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''Props for ``Configuration``.

        :param lex: 
        '''
        if isinstance(lex, dict):
            lex = AppInstanceBotLexConfiguration(**lex)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__190753a8664ba7ea97729e7c4d6d1834c2054c274acf0d3d9b76090a2a2e392a)
            check_type(argname="argument lex", value=lex, expected_type=type_hints["lex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lex": lex,
        }

    @builtins.property
    def lex(self) -> "AppInstanceBotLexConfiguration":
        result = self._values.get("lex")
        assert result is not None, "Required property 'lex' is missing"
        return typing.cast("AppInstanceBotLexConfiguration", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppInstanceBotConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.AppInstanceBotLexConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "lex_bot_alias_arn": "lexBotAliasArn",
        "locale_id": "localeId",
        "responds_to": "respondsTo",
        "welcome_intent": "welcomeIntent",
    },
)
class AppInstanceBotLexConfiguration:
    def __init__(
        self,
        *,
        lex_bot_alias_arn: builtins.str,
        locale_id: builtins.str,
        responds_to: "LexConfigurationRespondsTo",
        welcome_intent: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for AppInstanceBot with Lex.

        :param lex_bot_alias_arn: Lex ``BotAliasArn`` from setup Lex Bot.
        :param locale_id: LocaleId to use. This needs to match one of the localIds that BotAliasArn is configured with.
        :param responds_to: Setting for when Lex is invoked.
        :param welcome_intent: An optional welcome intent to trigger when the Bot is added to the channel.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a903a5ac908975450f7ca736d64edea6baf40428ec15f115e16ac1960f6206a3)
            check_type(argname="argument lex_bot_alias_arn", value=lex_bot_alias_arn, expected_type=type_hints["lex_bot_alias_arn"])
            check_type(argname="argument locale_id", value=locale_id, expected_type=type_hints["locale_id"])
            check_type(argname="argument responds_to", value=responds_to, expected_type=type_hints["responds_to"])
            check_type(argname="argument welcome_intent", value=welcome_intent, expected_type=type_hints["welcome_intent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lex_bot_alias_arn": lex_bot_alias_arn,
            "locale_id": locale_id,
            "responds_to": responds_to,
        }
        if welcome_intent is not None:
            self._values["welcome_intent"] = welcome_intent

    @builtins.property
    def lex_bot_alias_arn(self) -> builtins.str:
        '''Lex ``BotAliasArn`` from setup Lex Bot.'''
        result = self._values.get("lex_bot_alias_arn")
        assert result is not None, "Required property 'lex_bot_alias_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def locale_id(self) -> builtins.str:
        '''LocaleId to use.

        This needs to match one of the localIds that BotAliasArn is configured with.
        '''
        result = self._values.get("locale_id")
        assert result is not None, "Required property 'locale_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def responds_to(self) -> "LexConfigurationRespondsTo":
        '''Setting for when Lex is invoked.'''
        result = self._values.get("responds_to")
        assert result is not None, "Required property 'responds_to' is missing"
        return typing.cast("LexConfigurationRespondsTo", result)

    @builtins.property
    def welcome_intent(self) -> typing.Optional[builtins.str]:
        '''An optional welcome intent to trigger when the Bot is added to the channel.'''
        result = self._values.get("welcome_intent")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppInstanceBotLexConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.AppInstanceBotProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_instance_arn": "appInstanceArn",
        "configuration": "configuration",
        "client_request_token": "clientRequestToken",
        "metadata": "metadata",
        "name": "name",
        "tags": "tags",
    },
)
class AppInstanceBotProps:
    def __init__(
        self,
        *,
        app_instance_arn: builtins.str,
        configuration: typing.Union[AppInstanceBotConfiguration, typing.Dict[builtins.str, typing.Any]],
        client_request_token: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["InstanceBotTags", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Props for ``AppInstance``.

        :param app_instance_arn: The name of the app instance. Default: - None
        :param configuration: The configuration of the bot. This field populates Lex settings.
        :param client_request_token: The ClientRequestToken of the app instance. This field is autopopulated if not provided. Default: - None
        :param metadata: The metadata of the app instance. Limited to a 1KB string in UTF-8. Default: - None
        :param name: The name of the app instance. Default: - None
        :param tags: The tags for the creation request. Default: - None
        '''
        if isinstance(configuration, dict):
            configuration = AppInstanceBotConfiguration(**configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6f2d70e0e345c32a108d1b5e826706bde29fa7b412c11d521a2baab05d643ef)
            check_type(argname="argument app_instance_arn", value=app_instance_arn, expected_type=type_hints["app_instance_arn"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument client_request_token", value=client_request_token, expected_type=type_hints["client_request_token"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_instance_arn": app_instance_arn,
            "configuration": configuration,
        }
        if client_request_token is not None:
            self._values["client_request_token"] = client_request_token
        if metadata is not None:
            self._values["metadata"] = metadata
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app_instance_arn(self) -> builtins.str:
        '''The name of the app instance.

        :default: - None
        '''
        result = self._values.get("app_instance_arn")
        assert result is not None, "Required property 'app_instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration(self) -> AppInstanceBotConfiguration:
        '''The configuration of the bot.

        This field populates Lex settings.
        '''
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast(AppInstanceBotConfiguration, result)

    @builtins.property
    def client_request_token(self) -> typing.Optional[builtins.str]:
        '''The ClientRequestToken of the app instance.

        This field is autopopulated if not provided.

        :default: - None
        '''
        result = self._values.get("client_request_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''The metadata of the app instance.

        Limited to a 1KB string in UTF-8.

        :default: - None
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the app instance.

        :default: - None
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["InstanceBotTags"]]:
        '''The tags for the creation request.

        :default: - None
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["InstanceBotTags"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppInstanceBotProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.AppInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "client_request_token": "clientRequestToken",
        "metadata": "metadata",
        "name": "name",
        "tags": "tags",
    },
)
class AppInstanceProps:
    def __init__(
        self,
        *,
        client_request_token: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["AppInstanceTags", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Props for ``AppInstance``.

        :param client_request_token: The ClientRequestToken of the app instance. This field is autopopulated if not provided. Default: - None
        :param metadata: The metadata of the app instance. Limited to a 1KB string in UTF-8. Default: - None
        :param name: The name of the app instance. Default: - None
        :param tags: The tags for the creation request. Default: - None
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99641216bdb1ac5ae72a17b34ac6ca8ff8cbb075d8ddc07e9db8b47a39a2e63c)
            check_type(argname="argument client_request_token", value=client_request_token, expected_type=type_hints["client_request_token"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_request_token is not None:
            self._values["client_request_token"] = client_request_token
        if metadata is not None:
            self._values["metadata"] = metadata
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def client_request_token(self) -> typing.Optional[builtins.str]:
        '''The ClientRequestToken of the app instance.

        This field is autopopulated if not provided.

        :default: - None
        '''
        result = self._values.get("client_request_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''The metadata of the app instance.

        Limited to a 1KB string in UTF-8.

        :default: - None
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the app instance.

        :default: - None
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["AppInstanceTags"]]:
        '''The tags for the creation request.

        :default: - None
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["AppInstanceTags"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppInstanceStreamingConfigurations(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.AppInstanceStreamingConfigurations",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        app_instance_arn: builtins.str,
        streaming_configs: typing.Sequence[typing.Union["StreamingConfig", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param app_instance_arn: The ARN of the App Instance. Default: - None
        :param streaming_configs: The AppInstanceStreamingConfigurations. Default: - None
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9b5592853474342b6381b5e6c00a9b05345b286c1268a4def64d116f5fc5143)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StreamingConfigurationProps(
            app_instance_arn=app_instance_arn, streaming_configs=streaming_configs
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="streamingConfigs")
    def streaming_configs(self) -> typing.List["StreamingConfig"]:
        return typing.cast(typing.List["StreamingConfig"], jsii.get(self, "streamingConfigs"))


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.AppInstanceTags",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class AppInstanceTags:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: 
        :param value: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e7c2248211c91c5400947a073a327c5891999890c50d304103a4b2ede75eda)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppInstanceTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.AppInstanceUserProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_instance_arn": "appInstanceArn",
        "app_instance_user_id": "appInstanceUserId",
        "client_request_token": "clientRequestToken",
        "metadata": "metadata",
        "name": "name",
        "tags": "tags",
    },
)
class AppInstanceUserProps:
    def __init__(
        self,
        *,
        app_instance_arn: builtins.str,
        app_instance_user_id: builtins.str,
        client_request_token: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["InstanceUserTags", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Props for ``AppInstance``.

        :param app_instance_arn: The name of the app instance. Default: - None
        :param app_instance_user_id: The id of the app instance user. Default: - None
        :param client_request_token: The ClientRequestToken of the app instance. This field is autopopulated if not provided. Default: - None
        :param metadata: The metadata of the app instance. Limited to a 1KB string in UTF-8. Default: - None
        :param name: The name of the app instance. Default: - None
        :param tags: The tags for the creation request. Default: - None
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f1d2afec2a1ee54c9c8c65d06e6449432e7ccd47c39718154ace20f293608b)
            check_type(argname="argument app_instance_arn", value=app_instance_arn, expected_type=type_hints["app_instance_arn"])
            check_type(argname="argument app_instance_user_id", value=app_instance_user_id, expected_type=type_hints["app_instance_user_id"])
            check_type(argname="argument client_request_token", value=client_request_token, expected_type=type_hints["client_request_token"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_instance_arn": app_instance_arn,
            "app_instance_user_id": app_instance_user_id,
        }
        if client_request_token is not None:
            self._values["client_request_token"] = client_request_token
        if metadata is not None:
            self._values["metadata"] = metadata
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app_instance_arn(self) -> builtins.str:
        '''The name of the app instance.

        :default: - None
        '''
        result = self._values.get("app_instance_arn")
        assert result is not None, "Required property 'app_instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_instance_user_id(self) -> builtins.str:
        '''The id of the app instance user.

        :default: - None
        '''
        result = self._values.get("app_instance_user_id")
        assert result is not None, "Required property 'app_instance_user_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_request_token(self) -> typing.Optional[builtins.str]:
        '''The ClientRequestToken of the app instance.

        This field is autopopulated if not provided.

        :default: - None
        '''
        result = self._values.get("client_request_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''The metadata of the app instance.

        Limited to a 1KB string in UTF-8.

        :default: - None
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the app instance.

        :default: - None
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["InstanceUserTags"]]:
        '''The tags for the creation request.

        :default: - None
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["InstanceUserTags"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppInstanceUserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChannelFlow(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.ChannelFlow",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        app_instance_arn: builtins.str,
        client_request_token: builtins.str,
        processors: typing.Sequence[typing.Union["Processors", typing.Dict[builtins.str, typing.Any]]],
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["ChannelFlowTags", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param app_instance_arn: The ARN of the App Instance. Default: - None
        :param client_request_token: The client token for the request. An Idempotency token. Default: - None
        :param processors: Information about the processor Lambda functions. Default: - None
        :param name: The name of the channel flow. Default: - None
        :param tags: The tags for the creation request. Default: - None
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c12dc139a0c6c2028b7459eefbf26ae09174ec3a969cc2f61ac8d92aac274d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ChannelFlowProps(
            app_instance_arn=app_instance_arn,
            client_request_token=client_request_token,
            processors=processors,
            name=name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="channelFlowArn")
    def channel_flow_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channelFlowArn"))


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.ChannelFlowProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_instance_arn": "appInstanceArn",
        "client_request_token": "clientRequestToken",
        "processors": "processors",
        "name": "name",
        "tags": "tags",
    },
)
class ChannelFlowProps:
    def __init__(
        self,
        *,
        app_instance_arn: builtins.str,
        client_request_token: builtins.str,
        processors: typing.Sequence[typing.Union["Processors", typing.Dict[builtins.str, typing.Any]]],
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["ChannelFlowTags", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Props for ``AppInstance``.

        See: https://docs.aws.amazon.com/chime-sdk/latest/APIReference/API_messaging-chime_CreateChannelFlow.html

        :param app_instance_arn: The ARN of the App Instance. Default: - None
        :param client_request_token: The client token for the request. An Idempotency token. Default: - None
        :param processors: Information about the processor Lambda functions. Default: - None
        :param name: The name of the channel flow. Default: - None
        :param tags: The tags for the creation request. Default: - None
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4318c557157fab467f7f5003cd7f6be7ef8ee2b6efc6a633e86ac38c75fc6aaf)
            check_type(argname="argument app_instance_arn", value=app_instance_arn, expected_type=type_hints["app_instance_arn"])
            check_type(argname="argument client_request_token", value=client_request_token, expected_type=type_hints["client_request_token"])
            check_type(argname="argument processors", value=processors, expected_type=type_hints["processors"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_instance_arn": app_instance_arn,
            "client_request_token": client_request_token,
            "processors": processors,
        }
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app_instance_arn(self) -> builtins.str:
        '''The ARN of the App Instance.

        :default: - None
        '''
        result = self._values.get("app_instance_arn")
        assert result is not None, "Required property 'app_instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_request_token(self) -> builtins.str:
        '''The client token for the request.

        An Idempotency token.

        :default: - None
        '''
        result = self._values.get("client_request_token")
        assert result is not None, "Required property 'client_request_token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def processors(self) -> typing.List["Processors"]:
        '''Information about the processor Lambda functions.

        :default: - None
        '''
        result = self._values.get("processors")
        assert result is not None, "Required property 'processors' is missing"
        return typing.cast(typing.List["Processors"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the channel flow.

        :default: - None
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["ChannelFlowTags"]]:
        '''The tags for the creation request.

        :default: - None
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["ChannelFlowTags"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChannelFlowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.ChannelFlowTags",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class ChannelFlowTags:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: 
        :param value: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__423e2b447054eb5049c198e4c2c919b7bcdaeb6ee0e8a7b3792d33ee6a0b1d7b)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChannelFlowTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimePhoneNumber(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.ChimePhoneNumber",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        phone_product_type: "PhoneProductType",
        phone_area_code: typing.Optional[jsii.Number] = None,
        phone_city: typing.Optional[builtins.str] = None,
        phone_country: typing.Optional["PhoneCountry"] = None,
        phone_number_toll_free_prefix: typing.Optional[jsii.Number] = None,
        phone_number_type: typing.Optional["PhoneNumberType"] = None,
        phone_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param phone_product_type: Phone Product Type (required) - SipMediaApplicationDialIn or VoiceConnector. Default: - None
        :param phone_area_code: Area Code for phone number request (optional) - Usable only with US Country. Default: - None
        :param phone_city: City for phone number request (optional) - Usable only with US Country. Default: - None
        :param phone_country: Country for phone number request (optional) - See https://docs.aws.amazon.com/chime/latest/ag/phone-country-reqs.html for more details. Default: - US
        :param phone_number_toll_free_prefix: Toll Free Prefix for phone number request (optional). Default: - None
        :param phone_number_type: Phone Number Type for phone number request (optional) - Local or TollFree - Required with non-US country. Default: - None
        :param phone_state: State for phone number request (optional) - Usable only with US Country. Default: - None
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7115b79d2edc74ff917d518a81f7a6651e02418753fab2a2a35e2bff1587b5a7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PhoneNumberProps(
            phone_product_type=phone_product_type,
            phone_area_code=phone_area_code,
            phone_city=phone_city,
            phone_country=phone_country,
            phone_number_toll_free_prefix=phone_number_toll_free_prefix,
            phone_number_type=phone_number_type,
            phone_state=phone_state,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="associateWithVoiceConnector")
    def associate_with_voice_connector(
        self,
        voice_connector_id: "ChimeVoiceConnector",
    ) -> None:
        '''
        :param voice_connector_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__113f835f1247755909e4fbd1d3eb6d53265ab846dcd51487ecbfc26db4f5e50b)
            check_type(argname="argument voice_connector_id", value=voice_connector_id, expected_type=type_hints["voice_connector_id"])
        return typing.cast(None, jsii.invoke(self, "associateWithVoiceConnector", [voice_connector_id]))

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))


class ChimeSipMediaApp(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.ChimeSipMediaApp",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        endpoint: builtins.str,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param endpoint: endpoint for SipMediaApplication(required). Default: - none
        :param name: name for SipMediaApplication (optional). Default: - unique ID for resource
        :param region: region for SipMediaApplication(required) - Must us-east-1 or us-west-2 and in the same region as the SipMediaApplication Lambda handler. Default: - same region as stack deployment
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37db274aeecb4545734b8fe6863b37da6a06c91ab04fbd007ee1878c7cfc2cf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SipMediaAppProps(endpoint=endpoint, name=name, region=region)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="alexaSkill")
    def alexa_skill(
        self,
        *,
        alexa_skill_ids: typing.Sequence[builtins.str],
        alexa_skill_status: AlexaSkillStatus,
    ) -> _aws_cdk_ceddda9d.Reference:
        '''
        :param alexa_skill_ids: 
        :param alexa_skill_status: 
        '''
        sip_media_application_alexa_skill_configuration = SipMediaApplicationAlexaSkillConfiguration(
            alexa_skill_ids=alexa_skill_ids, alexa_skill_status=alexa_skill_status
        )

        return typing.cast(_aws_cdk_ceddda9d.Reference, jsii.invoke(self, "alexaSkill", [sip_media_application_alexa_skill_configuration]))

    @jsii.member(jsii_name="logging")
    def logging(
        self,
        *,
        enable_sip_media_application_message_logs: builtins.bool,
    ) -> "PSTNResources":
        '''
        :param enable_sip_media_application_message_logs: Enables message logging for the specified SIP media application.
        '''
        sip_media_application_logging_configuration = SipMediaApplicationLoggingConfiguration(
            enable_sip_media_application_message_logs=enable_sip_media_application_message_logs,
        )

        return typing.cast("PSTNResources", jsii.invoke(self, "logging", [sip_media_application_logging_configuration]))

    @builtins.property
    @jsii.member(jsii_name="sipMediaAppId")
    def sip_media_app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sipMediaAppId"))


class ChimeSipRule(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.ChimeSipRule",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        target_applications: typing.Sequence[typing.Union["SipRuleTargetApplication", typing.Dict[builtins.str, typing.Any]]],
        trigger_type: "TriggerType",
        trigger_value: builtins.str,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param target_applications: 
        :param trigger_type: Trigger Type for SipRule (required) - TO_PHONE_NUMBER or REQUEST_URI_HOSTNAME. Default: - none
        :param trigger_value: Trigger Value for SipRule (required) - EE.164 Phone Number or Voice Connector URI. Default: - none
        :param name: name for SipRule (optional). Default: - unique ID for resource
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39a8ee26df03196f53b578da14beb4b9253b7c5e47bb51611c9cefd974b2996b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SipRuleProps(
            target_applications=target_applications,
            trigger_type=trigger_type,
            trigger_value=trigger_value,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="sipRuleId")
    def sip_rule_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sipRuleId"))


class ChimeVoiceConnector(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.ChimeVoiceConnector",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        encryption: typing.Optional[builtins.bool] = None,
        logging_configuration: typing.Optional[typing.Union["VoiceConnectorLoggingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        origination: typing.Optional[typing.Sequence[typing.Union["Routes", typing.Dict[builtins.str, typing.Any]]]] = None,
        region: typing.Optional[builtins.str] = None,
        streaming: typing.Optional[typing.Union["Streaming", typing.Dict[builtins.str, typing.Any]]] = None,
        termination: typing.Optional[typing.Union["Termination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param encryption: Encryption boolean for VoiceConnector. Default: - False
        :param logging_configuration: 
        :param name: name for VoiceConnector. Default: - unique ID for resource
        :param origination: 
        :param region: region for SipMediaApplication(required) - Must us-east-1 or us-west-2 and in the same region as the SipMediaApplication Lambda handler. Default: - same region as stack deployment
        :param streaming: 
        :param termination: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3322e6fa91f7b318e813d5bf83683474955e25e8180642a7921f91e501c051de)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VoiceConnectorProps(
            encryption=encryption,
            logging_configuration=logging_configuration,
            name=name,
            origination=origination,
            region=region,
            streaming=streaming,
            termination=termination,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="voiceConnectorId")
    def voice_connector_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "voiceConnectorId"))


class ChimeVoiceProfileDomain(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.ChimeVoiceProfileDomain",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        server_side_encryption_configuration: typing.Union["ServerSideEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]],
        client_request_token: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["VoiceProfileDomainTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param server_side_encryption_configuration: 
        :param client_request_token: 
        :param description: 
        :param name: 
        :param tags: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b0fc61758880ca42be4625a894cd88dc46a46e2648a09cdc061099fef6d75d2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VoiceProfileDomainProps(
            server_side_encryption_configuration=server_side_encryption_configuration,
            client_request_token=client_request_token,
            description=description,
            name=name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="voiceProfileDomainArn")
    def voice_profile_domain_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "voiceProfileDomainArn"))

    @builtins.property
    @jsii.member(jsii_name="voiceProfileDomainId")
    def voice_profile_domain_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "voiceProfileDomainId"))

    @builtins.property
    @jsii.member(jsii_name="voiceProfileDomainName")
    def voice_profile_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "voiceProfileDomainName"))


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.Configuration",
    jsii_struct_bases=[],
    name_mapping={"lambda_": "lambda"},
)
class Configuration:
    def __init__(
        self,
        *,
        lambda_: typing.Union["Lambda", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''Props for ``Configuration``.

        See: https://docs.aws.amazon.com/chime-sdk/latest/APIReference/API_messaging-chime_ProcessorConfiguration.html

        :param lambda_: Indicates that the processor is of type Lambda. Default: - None
        '''
        if isinstance(lambda_, dict):
            lambda_ = Lambda(**lambda_)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4571f43b9d6d9c78c9a4194cd81c8f6d0723c84dfad67e0dc37cee78b008d9b5)
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lambda_": lambda_,
        }

    @builtins.property
    def lambda_(self) -> "Lambda":
        '''Indicates that the processor is of type Lambda.

        :default: - None
        '''
        result = self._values.get("lambda_")
        assert result is not None, "Required property 'lambda_' is missing"
        return typing.cast("Lambda", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Configuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-amazon-chime-resources.ContentIdentificationType")
class ContentIdentificationType(enum.Enum):
    PII = "PII"


@jsii.enum(jsii_type="cdk-amazon-chime-resources.ContentRedactionOutput")
class ContentRedactionOutput(enum.Enum):
    REDACTED = "REDACTED"
    REDACTED_AND_UNREDACTED = "REDACTED_AND_UNREDACTED"


@jsii.enum(jsii_type="cdk-amazon-chime-resources.ContentRedactionType")
class ContentRedactionType(enum.Enum):
    PII = "PII"


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.Elements",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "amazon_transcribe_call_analytics_processor_configuration": "amazonTranscribeCallAnalyticsProcessorConfiguration",
        "amazon_transcribe_processor_configuration": "amazonTranscribeProcessorConfiguration",
        "kinesis_data_stream_sink_configuration": "kinesisDataStreamSinkConfiguration",
        "lambda_function_sink_configuration": "lambdaFunctionSinkConfiguration",
        "s3_recording_sink_configuration": "s3RecordingSinkConfiguration",
        "sns_topic_sink_configuration": "snsTopicSinkConfiguration",
        "sqs_queue_sink_configuration": "sqsQueueSinkConfiguration",
        "voice_analytics_processor_configuration": "voiceAnalyticsProcessorConfiguration",
    },
)
class Elements:
    def __init__(
        self,
        *,
        type: "ElementsType",
        amazon_transcribe_call_analytics_processor_configuration: typing.Optional[typing.Union[AmazonTranscribeCallAnalyticsProcessorConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        amazon_transcribe_processor_configuration: typing.Optional[typing.Union[AmazonTranscribeProcessorConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_data_stream_sink_configuration: typing.Optional[typing.Union["KinesisDataStreamSinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_function_sink_configuration: typing.Optional[typing.Union["LambdaFunctionSinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_recording_sink_configuration: typing.Optional[typing.Union["S3RecordingSinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        sns_topic_sink_configuration: typing.Optional[typing.Union["SnsTopicSinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs_queue_sink_configuration: typing.Optional[typing.Union["SqsQueueSinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        voice_analytics_processor_configuration: typing.Optional[typing.Union["VoiceAnalyticsProcessorConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: 
        :param amazon_transcribe_call_analytics_processor_configuration: 
        :param amazon_transcribe_processor_configuration: 
        :param kinesis_data_stream_sink_configuration: 
        :param lambda_function_sink_configuration: 
        :param s3_recording_sink_configuration: 
        :param sns_topic_sink_configuration: 
        :param sqs_queue_sink_configuration: 
        :param voice_analytics_processor_configuration: 
        '''
        if isinstance(amazon_transcribe_call_analytics_processor_configuration, dict):
            amazon_transcribe_call_analytics_processor_configuration = AmazonTranscribeCallAnalyticsProcessorConfiguration(**amazon_transcribe_call_analytics_processor_configuration)
        if isinstance(amazon_transcribe_processor_configuration, dict):
            amazon_transcribe_processor_configuration = AmazonTranscribeProcessorConfiguration(**amazon_transcribe_processor_configuration)
        if isinstance(kinesis_data_stream_sink_configuration, dict):
            kinesis_data_stream_sink_configuration = KinesisDataStreamSinkConfiguration(**kinesis_data_stream_sink_configuration)
        if isinstance(lambda_function_sink_configuration, dict):
            lambda_function_sink_configuration = LambdaFunctionSinkConfiguration(**lambda_function_sink_configuration)
        if isinstance(s3_recording_sink_configuration, dict):
            s3_recording_sink_configuration = S3RecordingSinkConfiguration(**s3_recording_sink_configuration)
        if isinstance(sns_topic_sink_configuration, dict):
            sns_topic_sink_configuration = SnsTopicSinkConfiguration(**sns_topic_sink_configuration)
        if isinstance(sqs_queue_sink_configuration, dict):
            sqs_queue_sink_configuration = SqsQueueSinkConfiguration(**sqs_queue_sink_configuration)
        if isinstance(voice_analytics_processor_configuration, dict):
            voice_analytics_processor_configuration = VoiceAnalyticsProcessorConfiguration(**voice_analytics_processor_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47c8270166e256f6acc8ed44f959fcc2423bbdfa1366007fa7934305820464d8)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument amazon_transcribe_call_analytics_processor_configuration", value=amazon_transcribe_call_analytics_processor_configuration, expected_type=type_hints["amazon_transcribe_call_analytics_processor_configuration"])
            check_type(argname="argument amazon_transcribe_processor_configuration", value=amazon_transcribe_processor_configuration, expected_type=type_hints["amazon_transcribe_processor_configuration"])
            check_type(argname="argument kinesis_data_stream_sink_configuration", value=kinesis_data_stream_sink_configuration, expected_type=type_hints["kinesis_data_stream_sink_configuration"])
            check_type(argname="argument lambda_function_sink_configuration", value=lambda_function_sink_configuration, expected_type=type_hints["lambda_function_sink_configuration"])
            check_type(argname="argument s3_recording_sink_configuration", value=s3_recording_sink_configuration, expected_type=type_hints["s3_recording_sink_configuration"])
            check_type(argname="argument sns_topic_sink_configuration", value=sns_topic_sink_configuration, expected_type=type_hints["sns_topic_sink_configuration"])
            check_type(argname="argument sqs_queue_sink_configuration", value=sqs_queue_sink_configuration, expected_type=type_hints["sqs_queue_sink_configuration"])
            check_type(argname="argument voice_analytics_processor_configuration", value=voice_analytics_processor_configuration, expected_type=type_hints["voice_analytics_processor_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if amazon_transcribe_call_analytics_processor_configuration is not None:
            self._values["amazon_transcribe_call_analytics_processor_configuration"] = amazon_transcribe_call_analytics_processor_configuration
        if amazon_transcribe_processor_configuration is not None:
            self._values["amazon_transcribe_processor_configuration"] = amazon_transcribe_processor_configuration
        if kinesis_data_stream_sink_configuration is not None:
            self._values["kinesis_data_stream_sink_configuration"] = kinesis_data_stream_sink_configuration
        if lambda_function_sink_configuration is not None:
            self._values["lambda_function_sink_configuration"] = lambda_function_sink_configuration
        if s3_recording_sink_configuration is not None:
            self._values["s3_recording_sink_configuration"] = s3_recording_sink_configuration
        if sns_topic_sink_configuration is not None:
            self._values["sns_topic_sink_configuration"] = sns_topic_sink_configuration
        if sqs_queue_sink_configuration is not None:
            self._values["sqs_queue_sink_configuration"] = sqs_queue_sink_configuration
        if voice_analytics_processor_configuration is not None:
            self._values["voice_analytics_processor_configuration"] = voice_analytics_processor_configuration

    @builtins.property
    def type(self) -> "ElementsType":
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("ElementsType", result)

    @builtins.property
    def amazon_transcribe_call_analytics_processor_configuration(
        self,
    ) -> typing.Optional[AmazonTranscribeCallAnalyticsProcessorConfiguration]:
        result = self._values.get("amazon_transcribe_call_analytics_processor_configuration")
        return typing.cast(typing.Optional[AmazonTranscribeCallAnalyticsProcessorConfiguration], result)

    @builtins.property
    def amazon_transcribe_processor_configuration(
        self,
    ) -> typing.Optional[AmazonTranscribeProcessorConfiguration]:
        result = self._values.get("amazon_transcribe_processor_configuration")
        return typing.cast(typing.Optional[AmazonTranscribeProcessorConfiguration], result)

    @builtins.property
    def kinesis_data_stream_sink_configuration(
        self,
    ) -> typing.Optional["KinesisDataStreamSinkConfiguration"]:
        result = self._values.get("kinesis_data_stream_sink_configuration")
        return typing.cast(typing.Optional["KinesisDataStreamSinkConfiguration"], result)

    @builtins.property
    def lambda_function_sink_configuration(
        self,
    ) -> typing.Optional["LambdaFunctionSinkConfiguration"]:
        result = self._values.get("lambda_function_sink_configuration")
        return typing.cast(typing.Optional["LambdaFunctionSinkConfiguration"], result)

    @builtins.property
    def s3_recording_sink_configuration(
        self,
    ) -> typing.Optional["S3RecordingSinkConfiguration"]:
        result = self._values.get("s3_recording_sink_configuration")
        return typing.cast(typing.Optional["S3RecordingSinkConfiguration"], result)

    @builtins.property
    def sns_topic_sink_configuration(
        self,
    ) -> typing.Optional["SnsTopicSinkConfiguration"]:
        result = self._values.get("sns_topic_sink_configuration")
        return typing.cast(typing.Optional["SnsTopicSinkConfiguration"], result)

    @builtins.property
    def sqs_queue_sink_configuration(
        self,
    ) -> typing.Optional["SqsQueueSinkConfiguration"]:
        result = self._values.get("sqs_queue_sink_configuration")
        return typing.cast(typing.Optional["SqsQueueSinkConfiguration"], result)

    @builtins.property
    def voice_analytics_processor_configuration(
        self,
    ) -> typing.Optional["VoiceAnalyticsProcessorConfiguration"]:
        result = self._values.get("voice_analytics_processor_configuration")
        return typing.cast(typing.Optional["VoiceAnalyticsProcessorConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Elements(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-amazon-chime-resources.ElementsType")
class ElementsType(enum.Enum):
    AMAZON_TRANSCRIPT_CALL_ANALYTICS_PROCESS = "AMAZON_TRANSCRIPT_CALL_ANALYTICS_PROCESS"
    VOICE_ANALYTICS_PROCESSOR = "VOICE_ANALYTICS_PROCESSOR"
    AMAZON_TRANSCRIBE_PROCESSOR = "AMAZON_TRANSCRIBE_PROCESSOR"
    KINESIS_DATA_STREAM_SINK = "KINESIS_DATA_STREAM_SINK"
    LAMBDA_FUNCTION_SINK = "LAMBDA_FUNCTION_SINK"
    SQS_QUEUE_SINK = "SQS_QUEUE_SINK"
    SNS_TOPICS_SINK = "SNS_TOPICS_SINK"
    S3_RECORDING_SINK = "S3_RECORDING_SINK"


@jsii.enum(jsii_type="cdk-amazon-chime-resources.FallbackAction")
class FallbackAction(enum.Enum):
    CONTINUE = "CONTINUE"
    ABORT = "ABORT"


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.InstanceBotTags",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class InstanceBotTags:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: 
        :param value: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466e1fc6ac2865f25390b9cd8e5cf20df99008f2afbc5e9b1525746d6e5e4d0b)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InstanceBotTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.InstanceUserTags",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class InstanceUserTags:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: 
        :param value: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73075b4d361aeb287fc052a39e6ab5aa8840b8d2c65afb20519d4ff51266dc64)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InstanceUserTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-amazon-chime-resources.InvocationType")
class InvocationType(enum.Enum):
    ASYNC = "ASYNC"


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.IssueDetectionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"rule_name": "ruleName"},
)
class IssueDetectionConfiguration:
    def __init__(self, *, rule_name: builtins.str) -> None:
        '''
        :param rule_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab246d92d61207ce86ecb74c94285dea93a8dd2924e18ae9f6fddd0396b6a415)
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_name": rule_name,
        }

    @builtins.property
    def rule_name(self) -> builtins.str:
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IssueDetectionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.KeywordMatchConfiguration",
    jsii_struct_bases=[],
    name_mapping={"keywords": "keywords", "rule_name": "ruleName", "negate": "negate"},
)
class KeywordMatchConfiguration:
    def __init__(
        self,
        *,
        keywords: typing.Sequence[builtins.str],
        rule_name: builtins.str,
        negate: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param keywords: 
        :param rule_name: 
        :param negate: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64725845ce6afa3341958fde6bfa8db2429f6d1ecf85d69a1b86c761ae8d3ddb)
            check_type(argname="argument keywords", value=keywords, expected_type=type_hints["keywords"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument negate", value=negate, expected_type=type_hints["negate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "keywords": keywords,
            "rule_name": rule_name,
        }
        if negate is not None:
            self._values["negate"] = negate

    @builtins.property
    def keywords(self) -> typing.List[builtins.str]:
        result = self._values.get("keywords")
        assert result is not None, "Required property 'keywords' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def rule_name(self) -> builtins.str:
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def negate(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("negate")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeywordMatchConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.KinesisDataStreamSinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"insights_target": "insightsTarget"},
)
class KinesisDataStreamSinkConfiguration:
    def __init__(self, *, insights_target: builtins.str) -> None:
        '''
        :param insights_target: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04bdccaa55d185310cf53553bb92d683f06df4a8a44c499b3136280f57f5e961)
            check_type(argname="argument insights_target", value=insights_target, expected_type=type_hints["insights_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "insights_target": insights_target,
        }

    @builtins.property
    def insights_target(self) -> builtins.str:
        result = self._values.get("insights_target")
        assert result is not None, "Required property 'insights_target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisDataStreamSinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.Lambda",
    jsii_struct_bases=[],
    name_mapping={"invocation_type": "invocationType", "resource_arn": "resourceArn"},
)
class Lambda:
    def __init__(
        self,
        *,
        invocation_type: InvocationType,
        resource_arn: builtins.str,
    ) -> None:
        '''Props for ``LambdaConfiguration``.

        See: https://docs.aws.amazon.com/chime-sdk/latest/APIReference/API_messaging-chime_LambdaConfiguration.html

        :param invocation_type: Controls how the Lambda function is invoked. Default: - None
        :param resource_arn: The ARN of the Lambda message processing function. Default: - None
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__578b648f0cf5bcbae9bf298c3b4ec202747ea61fcc36e3c12421adbf714050a6)
            check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "invocation_type": invocation_type,
            "resource_arn": resource_arn,
        }

    @builtins.property
    def invocation_type(self) -> InvocationType:
        '''Controls how the Lambda function is invoked.

        :default: - None
        '''
        result = self._values.get("invocation_type")
        assert result is not None, "Required property 'invocation_type' is missing"
        return typing.cast(InvocationType, result)

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''The ARN of the Lambda message processing function.

        :default: - None
        '''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Lambda(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.LambdaFunctionSinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"insights_target": "insightsTarget"},
)
class LambdaFunctionSinkConfiguration:
    def __init__(self, *, insights_target: builtins.str) -> None:
        '''
        :param insights_target: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ad1da5fd4a9bb89891753d494e60eaff7b4500917ff9ba2c3057b720c1ddb65)
            check_type(argname="argument insights_target", value=insights_target, expected_type=type_hints["insights_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "insights_target": insights_target,
        }

    @builtins.property
    def insights_target(self) -> builtins.str:
        result = self._values.get("insights_target")
        assert result is not None, "Required property 'insights_target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionSinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-amazon-chime-resources.LanguageCode")
class LanguageCode(enum.Enum):
    EN_US = "EN_US"
    EN_GB = "EN_GB"
    ES_US = "ES_US"
    FR_CA = "FR_CA"
    FR_FR = "FR_FR"
    EN_AU = "EN_AU"
    IT_IT = "IT_IT"
    DE_DE = "DE_DE"
    PT_BR = "PT_BR"


@jsii.enum(jsii_type="cdk-amazon-chime-resources.LexConfigurationRespondsTo")
class LexConfigurationRespondsTo(enum.Enum):
    '''Props for ``Configuration`` when Configuration is for Lex.'''

    STANDARD_MESSAGES = "STANDARD_MESSAGES"


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.MediaInsightsConfiguration",
    jsii_struct_bases=[],
    name_mapping={"configuration_arn": "configurationArn", "disabled": "disabled"},
)
class MediaInsightsConfiguration:
    def __init__(
        self,
        *,
        configuration_arn: builtins.str,
        disabled: builtins.bool,
    ) -> None:
        '''
        :param configuration_arn: 
        :param disabled: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d3fd94ae5af25b8c7bbd19af5501900af73d8db411381ec98cf7c788dbbcc45)
            check_type(argname="argument configuration_arn", value=configuration_arn, expected_type=type_hints["configuration_arn"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration_arn": configuration_arn,
            "disabled": disabled,
        }

    @builtins.property
    def configuration_arn(self) -> builtins.str:
        result = self._values.get("configuration_arn")
        assert result is not None, "Required property 'configuration_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disabled(self) -> builtins.bool:
        result = self._values.get("disabled")
        assert result is not None, "Required property 'disabled' is missing"
        return typing.cast(builtins.bool, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaInsightsConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaInsightsPipeline(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.MediaInsightsPipeline",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        elements: typing.Sequence[typing.Union[Elements, typing.Dict[builtins.str, typing.Any]]],
        resource_access_role_arn: builtins.str,
        client_request_token: typing.Optional[builtins.str] = None,
        media_insights_pipeline_configuration_name: typing.Optional[builtins.str] = None,
        real_time_alert_configuration: typing.Optional[typing.Union["RealTimeAlertConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["MediaPipelineInsightsTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param elements: 
        :param resource_access_role_arn: 
        :param client_request_token: 
        :param media_insights_pipeline_configuration_name: 
        :param real_time_alert_configuration: 
        :param tags: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__498d2a9395dfedaec2caffb27327afd8a3d5cd1f27f7f3e971bc1ef8c85745d8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MediaInsightsPipelineProps(
            elements=elements,
            resource_access_role_arn=resource_access_role_arn,
            client_request_token=client_request_token,
            media_insights_pipeline_configuration_name=media_insights_pipeline_configuration_name,
            real_time_alert_configuration=real_time_alert_configuration,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="mediaInsightsPipelineConfigurationArn")
    def media_insights_pipeline_configuration_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mediaInsightsPipelineConfigurationArn"))

    @builtins.property
    @jsii.member(jsii_name="mediaInsightsPipelineConfigurationId")
    def media_insights_pipeline_configuration_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mediaInsightsPipelineConfigurationId"))

    @builtins.property
    @jsii.member(jsii_name="mediaInsightsPipelineConfigurationName")
    def media_insights_pipeline_configuration_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mediaInsightsPipelineConfigurationName"))


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.MediaInsightsPipelineProps",
    jsii_struct_bases=[],
    name_mapping={
        "elements": "elements",
        "resource_access_role_arn": "resourceAccessRoleArn",
        "client_request_token": "clientRequestToken",
        "media_insights_pipeline_configuration_name": "mediaInsightsPipelineConfigurationName",
        "real_time_alert_configuration": "realTimeAlertConfiguration",
        "tags": "tags",
    },
)
class MediaInsightsPipelineProps:
    def __init__(
        self,
        *,
        elements: typing.Sequence[typing.Union[Elements, typing.Dict[builtins.str, typing.Any]]],
        resource_access_role_arn: builtins.str,
        client_request_token: typing.Optional[builtins.str] = None,
        media_insights_pipeline_configuration_name: typing.Optional[builtins.str] = None,
        real_time_alert_configuration: typing.Optional[typing.Union["RealTimeAlertConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["MediaPipelineInsightsTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param elements: 
        :param resource_access_role_arn: 
        :param client_request_token: 
        :param media_insights_pipeline_configuration_name: 
        :param real_time_alert_configuration: 
        :param tags: 
        '''
        if isinstance(real_time_alert_configuration, dict):
            real_time_alert_configuration = RealTimeAlertConfiguration(**real_time_alert_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb0c085f4f2337763da4b7a97077d9be818b2ed003e6600afd55e3203733a579)
            check_type(argname="argument elements", value=elements, expected_type=type_hints["elements"])
            check_type(argname="argument resource_access_role_arn", value=resource_access_role_arn, expected_type=type_hints["resource_access_role_arn"])
            check_type(argname="argument client_request_token", value=client_request_token, expected_type=type_hints["client_request_token"])
            check_type(argname="argument media_insights_pipeline_configuration_name", value=media_insights_pipeline_configuration_name, expected_type=type_hints["media_insights_pipeline_configuration_name"])
            check_type(argname="argument real_time_alert_configuration", value=real_time_alert_configuration, expected_type=type_hints["real_time_alert_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "elements": elements,
            "resource_access_role_arn": resource_access_role_arn,
        }
        if client_request_token is not None:
            self._values["client_request_token"] = client_request_token
        if media_insights_pipeline_configuration_name is not None:
            self._values["media_insights_pipeline_configuration_name"] = media_insights_pipeline_configuration_name
        if real_time_alert_configuration is not None:
            self._values["real_time_alert_configuration"] = real_time_alert_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def elements(self) -> typing.List[Elements]:
        result = self._values.get("elements")
        assert result is not None, "Required property 'elements' is missing"
        return typing.cast(typing.List[Elements], result)

    @builtins.property
    def resource_access_role_arn(self) -> builtins.str:
        result = self._values.get("resource_access_role_arn")
        assert result is not None, "Required property 'resource_access_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_request_token(self) -> typing.Optional[builtins.str]:
        result = self._values.get("client_request_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def media_insights_pipeline_configuration_name(
        self,
    ) -> typing.Optional[builtins.str]:
        result = self._values.get("media_insights_pipeline_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def real_time_alert_configuration(
        self,
    ) -> typing.Optional["RealTimeAlertConfiguration"]:
        result = self._values.get("real_time_alert_configuration")
        return typing.cast(typing.Optional["RealTimeAlertConfiguration"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["MediaPipelineInsightsTag"]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["MediaPipelineInsightsTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaInsightsPipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.MediaPipelineInsightsTag",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class MediaPipelineInsightsTag:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: 
        :param value: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2931f7be952ca8d873e6ad2f1c824103c35c9e8e7f4e95b985d45b95774656a4)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaPipelineInsightsTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MessagingAppInstance(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.MessagingAppInstance",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        client_request_token: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[AppInstanceTags, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param client_request_token: The ClientRequestToken of the app instance. This field is autopopulated if not provided. Default: - None
        :param metadata: The metadata of the app instance. Limited to a 1KB string in UTF-8. Default: - None
        :param name: The name of the app instance. Default: - None
        :param tags: The tags for the creation request. Default: - None
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a9f012fab9eb0d816a78f8f21fb2b6ca54774f162a1dd5769f1628ac6f2e8c9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AppInstanceProps(
            client_request_token=client_request_token,
            metadata=metadata,
            name=name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="retention")
    def retention(self, days: jsii.Number) -> "MessagingResources":
        '''
        :param days: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da36a029e1afaaefc489c020934e45363195f10c5727d992a321c13b0043e2c0)
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
        return typing.cast("MessagingResources", jsii.invoke(self, "retention", [days]))

    @jsii.member(jsii_name="streaming")
    def streaming(
        self,
        streaming_configs: typing.Sequence[typing.Union["StreamingConfig", typing.Dict[builtins.str, typing.Any]]],
    ) -> "MessagingResources":
        '''
        :param streaming_configs: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e11016e616c0eecf971ad1b8d44cee41698040c9f7bb7fc2ef89c3f2b4668454)
            check_type(argname="argument streaming_configs", value=streaming_configs, expected_type=type_hints["streaming_configs"])
        return typing.cast("MessagingResources", jsii.invoke(self, "streaming", [streaming_configs]))

    @builtins.property
    @jsii.member(jsii_name="appInstanceArn")
    def app_instance_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appInstanceArn"))


class MessagingAppInstanceAdmin(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.MessagingAppInstanceAdmin",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        app_instance_admin_arn: builtins.str,
        app_instance_arn: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param app_instance_admin_arn: The name of the app instance. Default: - None
        :param app_instance_arn: The name of the app instance. Default: - None
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40803d0180de29a1b7d03d21acba148c27c1a6eab510cd87e687d82d6108b3d5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AppInstanceAdminProps(
            app_instance_admin_arn=app_instance_admin_arn,
            app_instance_arn=app_instance_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="appInstanceAdminArn")
    def app_instance_admin_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appInstanceAdminArn"))

    @builtins.property
    @jsii.member(jsii_name="appInstanceAdminName")
    def app_instance_admin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appInstanceAdminName"))


class MessagingAppInstanceBot(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.MessagingAppInstanceBot",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        app_instance_arn: builtins.str,
        configuration: typing.Union[AppInstanceBotConfiguration, typing.Dict[builtins.str, typing.Any]],
        client_request_token: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[InstanceBotTags, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param app_instance_arn: The name of the app instance. Default: - None
        :param configuration: The configuration of the bot. This field populates Lex settings.
        :param client_request_token: The ClientRequestToken of the app instance. This field is autopopulated if not provided. Default: - None
        :param metadata: The metadata of the app instance. Limited to a 1KB string in UTF-8. Default: - None
        :param name: The name of the app instance. Default: - None
        :param tags: The tags for the creation request. Default: - None
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fab735ff921a58db4ce197742abd231baa840546c2d4a14735be63e8de8059d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AppInstanceBotProps(
            app_instance_arn=app_instance_arn,
            configuration=configuration,
            client_request_token=client_request_token,
            metadata=metadata,
            name=name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="appInstanceBotArn")
    def app_instance_bot_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appInstanceBotArn"))


class MessagingAppInstanceUser(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.MessagingAppInstanceUser",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        app_instance_arn: builtins.str,
        app_instance_user_id: builtins.str,
        client_request_token: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[InstanceUserTags, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param app_instance_arn: The name of the app instance. Default: - None
        :param app_instance_user_id: The id of the app instance user. Default: - None
        :param client_request_token: The ClientRequestToken of the app instance. This field is autopopulated if not provided. Default: - None
        :param metadata: The metadata of the app instance. Limited to a 1KB string in UTF-8. Default: - None
        :param name: The name of the app instance. Default: - None
        :param tags: The tags for the creation request. Default: - None
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__301eef12c49f4f86623f7326244dcbc9fc1774d26e08b7f5e344906a9f195cba)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AppInstanceUserProps(
            app_instance_arn=app_instance_arn,
            app_instance_user_id=app_instance_user_id,
            client_request_token=client_request_token,
            metadata=metadata,
            name=name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="appInstanceUserArn")
    def app_instance_user_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appInstanceUserArn"))


@jsii.enum(jsii_type="cdk-amazon-chime-resources.MessagingDataType")
class MessagingDataType(enum.Enum):
    CHANNEL = "CHANNEL"
    CHANNELMESSAGE = "CHANNELMESSAGE"


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.MessagingResourceProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "properties": "properties",
        "resource_type": "resourceType",
        "uid": "uid",
    },
)
class MessagingResourceProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        properties: typing.Mapping[builtins.str, typing.Any],
        resource_type: builtins.str,
        uid: builtins.str,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param properties: 
        :param resource_type: 
        :param uid: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7688c29fcfcbe8ff3316837ef27d8a5c7629b1f3879e46ab246754bb9571664f)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "properties": properties,
            "resource_type": resource_type,
            "uid": uid,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        result = self._values.get("properties")
        assert result is not None, "Required property 'properties' is missing"
        return typing.cast(typing.Mapping[builtins.str, typing.Any], result)

    @builtins.property
    def resource_type(self) -> builtins.str:
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uid(self) -> builtins.str:
        result = self._values.get("uid")
        assert result is not None, "Required property 'uid' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MessagingResourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MessagingResources(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.MessagingResources",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        properties: typing.Mapping[builtins.str, typing.Any],
        resource_type: builtins.str,
        uid: builtins.str,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param properties: 
        :param resource_type: 
        :param uid: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4c733c0cc8a171d0914be8696b8353206a7d5a17dbbdb5ab2171cdd3ffd266e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MessagingResourceProps(
            properties=properties,
            resource_type=resource_type,
            uid=uid,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="messagingCustomResource")
    def messaging_custom_resource(self) -> _aws_cdk_ceddda9d.CustomResource:
        return typing.cast(_aws_cdk_ceddda9d.CustomResource, jsii.get(self, "messagingCustomResource"))


@jsii.enum(jsii_type="cdk-amazon-chime-resources.NotificationTargetType")
class NotificationTargetType(enum.Enum):
    EVENTBRIDGE = "EVENTBRIDGE"
    SNS = "SNS"
    SQS = "SQS"


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.PSTNResourceProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "properties": "properties",
        "resource_type": "resourceType",
        "uid": "uid",
    },
)
class PSTNResourceProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        properties: typing.Mapping[builtins.str, typing.Any],
        resource_type: builtins.str,
        uid: builtins.str,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param properties: 
        :param resource_type: 
        :param uid: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e7326b3c0a86e27b49bf3d1d67d25db6fc4d4e818fb652a26c9b1a4959e1677)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "properties": properties,
            "resource_type": resource_type,
            "uid": uid,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        result = self._values.get("properties")
        assert result is not None, "Required property 'properties' is missing"
        return typing.cast(typing.Mapping[builtins.str, typing.Any], result)

    @builtins.property
    def resource_type(self) -> builtins.str:
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uid(self) -> builtins.str:
        result = self._values.get("uid")
        assert result is not None, "Required property 'uid' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PSTNResourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PSTNResources(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.PSTNResources",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        properties: typing.Mapping[builtins.str, typing.Any],
        resource_type: builtins.str,
        uid: builtins.str,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param properties: 
        :param resource_type: 
        :param uid: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd9372fb4e09a36da7cfd84d9bf339c9f4439d92326a5b861b6e029af5d9c892)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PSTNResourceProps(
            properties=properties,
            resource_type=resource_type,
            uid=uid,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="pstnCustomResource")
    def pstn_custom_resource(self) -> _aws_cdk_ceddda9d.CustomResource:
        return typing.cast(_aws_cdk_ceddda9d.CustomResource, jsii.get(self, "pstnCustomResource"))


@jsii.enum(jsii_type="cdk-amazon-chime-resources.PartialResultsStability")
class PartialResultsStability(enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@jsii.enum(jsii_type="cdk-amazon-chime-resources.PhoneCountry")
class PhoneCountry(enum.Enum):
    AU = "AU"
    AT = "AT"
    CA = "CA"
    DK = "DK"
    DE = "DE"
    IE = "IE"
    IT = "IT"
    NZ = "NZ"
    NG = "NG"
    PR = "PR"
    KR = "KR"
    SE = "SE"
    CH = "CH"
    UK = "UK"
    US = "US"


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.PhoneNumberProps",
    jsii_struct_bases=[],
    name_mapping={
        "phone_product_type": "phoneProductType",
        "phone_area_code": "phoneAreaCode",
        "phone_city": "phoneCity",
        "phone_country": "phoneCountry",
        "phone_number_toll_free_prefix": "phoneNumberTollFreePrefix",
        "phone_number_type": "phoneNumberType",
        "phone_state": "phoneState",
    },
)
class PhoneNumberProps:
    def __init__(
        self,
        *,
        phone_product_type: "PhoneProductType",
        phone_area_code: typing.Optional[jsii.Number] = None,
        phone_city: typing.Optional[builtins.str] = None,
        phone_country: typing.Optional[PhoneCountry] = None,
        phone_number_toll_free_prefix: typing.Optional[jsii.Number] = None,
        phone_number_type: typing.Optional["PhoneNumberType"] = None,
        phone_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Props for ``PhoneNumber``.

        :param phone_product_type: Phone Product Type (required) - SipMediaApplicationDialIn or VoiceConnector. Default: - None
        :param phone_area_code: Area Code for phone number request (optional) - Usable only with US Country. Default: - None
        :param phone_city: City for phone number request (optional) - Usable only with US Country. Default: - None
        :param phone_country: Country for phone number request (optional) - See https://docs.aws.amazon.com/chime/latest/ag/phone-country-reqs.html for more details. Default: - US
        :param phone_number_toll_free_prefix: Toll Free Prefix for phone number request (optional). Default: - None
        :param phone_number_type: Phone Number Type for phone number request (optional) - Local or TollFree - Required with non-US country. Default: - None
        :param phone_state: State for phone number request (optional) - Usable only with US Country. Default: - None
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c5b2ac2a9588b05b4d090bb324c4de18ab13008479ac747fb4c76d5aef2bc55)
            check_type(argname="argument phone_product_type", value=phone_product_type, expected_type=type_hints["phone_product_type"])
            check_type(argname="argument phone_area_code", value=phone_area_code, expected_type=type_hints["phone_area_code"])
            check_type(argname="argument phone_city", value=phone_city, expected_type=type_hints["phone_city"])
            check_type(argname="argument phone_country", value=phone_country, expected_type=type_hints["phone_country"])
            check_type(argname="argument phone_number_toll_free_prefix", value=phone_number_toll_free_prefix, expected_type=type_hints["phone_number_toll_free_prefix"])
            check_type(argname="argument phone_number_type", value=phone_number_type, expected_type=type_hints["phone_number_type"])
            check_type(argname="argument phone_state", value=phone_state, expected_type=type_hints["phone_state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "phone_product_type": phone_product_type,
        }
        if phone_area_code is not None:
            self._values["phone_area_code"] = phone_area_code
        if phone_city is not None:
            self._values["phone_city"] = phone_city
        if phone_country is not None:
            self._values["phone_country"] = phone_country
        if phone_number_toll_free_prefix is not None:
            self._values["phone_number_toll_free_prefix"] = phone_number_toll_free_prefix
        if phone_number_type is not None:
            self._values["phone_number_type"] = phone_number_type
        if phone_state is not None:
            self._values["phone_state"] = phone_state

    @builtins.property
    def phone_product_type(self) -> "PhoneProductType":
        '''Phone Product Type (required) - SipMediaApplicationDialIn or VoiceConnector.

        :default: - None
        '''
        result = self._values.get("phone_product_type")
        assert result is not None, "Required property 'phone_product_type' is missing"
        return typing.cast("PhoneProductType", result)

    @builtins.property
    def phone_area_code(self) -> typing.Optional[jsii.Number]:
        '''Area Code for phone number request (optional)  - Usable only with US Country.

        :default: - None
        '''
        result = self._values.get("phone_area_code")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def phone_city(self) -> typing.Optional[builtins.str]:
        '''City for phone number request (optional) - Usable only with US Country.

        :default: - None
        '''
        result = self._values.get("phone_city")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def phone_country(self) -> typing.Optional[PhoneCountry]:
        '''Country for phone number request (optional) - See https://docs.aws.amazon.com/chime/latest/ag/phone-country-reqs.html for more details.

        :default: - US
        '''
        result = self._values.get("phone_country")
        return typing.cast(typing.Optional[PhoneCountry], result)

    @builtins.property
    def phone_number_toll_free_prefix(self) -> typing.Optional[jsii.Number]:
        '''Toll Free Prefix for phone number request (optional).

        :default: - None
        '''
        result = self._values.get("phone_number_toll_free_prefix")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def phone_number_type(self) -> typing.Optional["PhoneNumberType"]:
        '''Phone Number Type for phone number request (optional) - Local or TollFree - Required with non-US country.

        :default: - None
        '''
        result = self._values.get("phone_number_type")
        return typing.cast(typing.Optional["PhoneNumberType"], result)

    @builtins.property
    def phone_state(self) -> typing.Optional[builtins.str]:
        '''State for phone number request (optional) - Usable only with US Country.

        :default: - None
        '''
        result = self._values.get("phone_state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PhoneNumberProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-amazon-chime-resources.PhoneNumberType")
class PhoneNumberType(enum.Enum):
    LOCAL = "LOCAL"
    TOLLFREE = "TOLLFREE"


@jsii.enum(jsii_type="cdk-amazon-chime-resources.PhoneProductType")
class PhoneProductType(enum.Enum):
    SMA = "SMA"
    VC = "VC"


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.PostCallAnalyticsSettings",
    jsii_struct_bases=[],
    name_mapping={
        "data_access_role_arn": "dataAccessRoleArn",
        "output_location": "outputLocation",
        "content_redaction_output": "contentRedactionOutput",
        "output_encryption_kms_key_id": "outputEncryptionKMSKeyId",
    },
)
class PostCallAnalyticsSettings:
    def __init__(
        self,
        *,
        data_access_role_arn: builtins.str,
        output_location: builtins.str,
        content_redaction_output: typing.Optional[ContentRedactionOutput] = None,
        output_encryption_kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_access_role_arn: 
        :param output_location: 
        :param content_redaction_output: 
        :param output_encryption_kms_key_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2244030f4fbace1e42d75ad09edd84b32e2f9a0187eadc9b372362afd6ebe8bc)
            check_type(argname="argument data_access_role_arn", value=data_access_role_arn, expected_type=type_hints["data_access_role_arn"])
            check_type(argname="argument output_location", value=output_location, expected_type=type_hints["output_location"])
            check_type(argname="argument content_redaction_output", value=content_redaction_output, expected_type=type_hints["content_redaction_output"])
            check_type(argname="argument output_encryption_kms_key_id", value=output_encryption_kms_key_id, expected_type=type_hints["output_encryption_kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_access_role_arn": data_access_role_arn,
            "output_location": output_location,
        }
        if content_redaction_output is not None:
            self._values["content_redaction_output"] = content_redaction_output
        if output_encryption_kms_key_id is not None:
            self._values["output_encryption_kms_key_id"] = output_encryption_kms_key_id

    @builtins.property
    def data_access_role_arn(self) -> builtins.str:
        result = self._values.get("data_access_role_arn")
        assert result is not None, "Required property 'data_access_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def output_location(self) -> builtins.str:
        result = self._values.get("output_location")
        assert result is not None, "Required property 'output_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_redaction_output(self) -> typing.Optional[ContentRedactionOutput]:
        result = self._values.get("content_redaction_output")
        return typing.cast(typing.Optional[ContentRedactionOutput], result)

    @builtins.property
    def output_encryption_kms_key_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("output_encryption_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PostCallAnalyticsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.Processors",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "execution_order": "executionOrder",
        "fallback_action": "fallbackAction",
        "name": "name",
    },
)
class Processors:
    def __init__(
        self,
        *,
        configuration: typing.Union[Configuration, typing.Dict[builtins.str, typing.Any]],
        execution_order: jsii.Number,
        fallback_action: FallbackAction,
        name: builtins.str,
    ) -> None:
        '''Props for ``Processors``.

        See: https://docs.aws.amazon.com/chime-sdk/latest/APIReference/API_messaging-chime_Processor.html

        :param configuration: The information about the type of processor and its identifier. Default: - None
        :param execution_order: The sequence in which processors run. If you have multiple processors in a channel flow, message processing goes through each processor in the sequence. The value determines the sequence. At this point, we support only 1 processor within a flow. Default: - None
        :param fallback_action: Determines whether to continue with message processing or stop it in cases where communication with a processor fails. If a processor has a fallback action of ABORT and communication with it fails, the processor sets the message status to FAILED and does not send the message to any recipients. Note that if the last processor in the channel flow sequence has a fallback action of CONTINUE and communication with the processor fails, then the message is considered processed and sent to recipients of the channel. Default: - None
        :param name: The name of the Channel Flow Processor. Default: - None
        '''
        if isinstance(configuration, dict):
            configuration = Configuration(**configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ddb27d8877eb97beb38e78204072b302c0a15e44306cc7d732983b023c5ee5)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument execution_order", value=execution_order, expected_type=type_hints["execution_order"])
            check_type(argname="argument fallback_action", value=fallback_action, expected_type=type_hints["fallback_action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration": configuration,
            "execution_order": execution_order,
            "fallback_action": fallback_action,
            "name": name,
        }

    @builtins.property
    def configuration(self) -> Configuration:
        '''The information about the type of processor and its identifier.

        :default: - None
        '''
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast(Configuration, result)

    @builtins.property
    def execution_order(self) -> jsii.Number:
        '''The sequence in which processors run.

        If you have multiple processors in a channel flow, message processing goes through each processor in the sequence. The value determines the sequence. At this point, we support only 1 processor within a flow.

        :default: - None
        '''
        result = self._values.get("execution_order")
        assert result is not None, "Required property 'execution_order' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def fallback_action(self) -> FallbackAction:
        '''Determines whether to continue with message processing or stop it in cases where communication with a processor fails.

        If a processor has a fallback action of ABORT and communication with it fails, the processor sets the message status to FAILED and does not send the message to any recipients. Note that if the last processor in the channel flow sequence has a fallback action of CONTINUE and communication with the processor fails, then the message is considered processed and sent to recipients of the channel.

        :default: - None
        '''
        result = self._values.get("fallback_action")
        assert result is not None, "Required property 'fallback_action' is missing"
        return typing.cast(FallbackAction, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Channel Flow Processor.

        :default: - None
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Processors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-amazon-chime-resources.Protocol")
class Protocol(enum.Enum):
    TCP = "TCP"
    UDP = "UDP"


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.RealTimeAlertConfiguration",
    jsii_struct_bases=[],
    name_mapping={"disabled": "disabled", "rules": "rules"},
)
class RealTimeAlertConfiguration:
    def __init__(
        self,
        *,
        disabled: builtins.bool,
        rules: typing.Sequence[typing.Union["Rules", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param disabled: 
        :param rules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11ba3e8e37516ce401aaf6bcbb6c3f1807abfdcda524f29ac31dc808ecdf0086)
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disabled": disabled,
            "rules": rules,
        }

    @builtins.property
    def disabled(self) -> builtins.bool:
        result = self._values.get("disabled")
        assert result is not None, "Required property 'disabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def rules(self) -> typing.List["Rules"]:
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.List["Rules"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RealTimeAlertConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.Routes",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "port": "port",
        "priority": "priority",
        "protocol": "protocol",
        "weight": "weight",
    },
)
class Routes:
    def __init__(
        self,
        *,
        host: builtins.str,
        port: jsii.Number,
        priority: jsii.Number,
        protocol: Protocol,
        weight: jsii.Number,
    ) -> None:
        '''
        :param host: 
        :param port: 
        :param priority: 
        :param protocol: 
        :param weight: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb30c4d59c6038c4d49567f143b8a4b4b5355d6c06cc090d64ec9ceaf4ae31ca)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host": host,
            "port": port,
            "priority": priority,
            "protocol": protocol,
            "weight": weight,
        }

    @builtins.property
    def host(self) -> builtins.str:
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def protocol(self) -> Protocol:
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(Protocol, result)

    @builtins.property
    def weight(self) -> jsii.Number:
        result = self._values.get("weight")
        assert result is not None, "Required property 'weight' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Routes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.Rules",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "issue_detection_configuration": "issueDetectionConfiguration",
        "keyword_match_configuration": "keywordMatchConfiguration",
        "sentiment_configuration": "sentimentConfiguration",
    },
)
class Rules:
    def __init__(
        self,
        *,
        type: "RulesType",
        issue_detection_configuration: typing.Optional[typing.Union[IssueDetectionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        keyword_match_configuration: typing.Optional[typing.Union[KeywordMatchConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        sentiment_configuration: typing.Optional[typing.Union["SentimentConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: 
        :param issue_detection_configuration: 
        :param keyword_match_configuration: 
        :param sentiment_configuration: 
        '''
        if isinstance(issue_detection_configuration, dict):
            issue_detection_configuration = IssueDetectionConfiguration(**issue_detection_configuration)
        if isinstance(keyword_match_configuration, dict):
            keyword_match_configuration = KeywordMatchConfiguration(**keyword_match_configuration)
        if isinstance(sentiment_configuration, dict):
            sentiment_configuration = SentimentConfiguration(**sentiment_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55b52d3daeeca4614bae10450af6c08fa2c6cdeda17a78af05d8f2416d41d85)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument issue_detection_configuration", value=issue_detection_configuration, expected_type=type_hints["issue_detection_configuration"])
            check_type(argname="argument keyword_match_configuration", value=keyword_match_configuration, expected_type=type_hints["keyword_match_configuration"])
            check_type(argname="argument sentiment_configuration", value=sentiment_configuration, expected_type=type_hints["sentiment_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if issue_detection_configuration is not None:
            self._values["issue_detection_configuration"] = issue_detection_configuration
        if keyword_match_configuration is not None:
            self._values["keyword_match_configuration"] = keyword_match_configuration
        if sentiment_configuration is not None:
            self._values["sentiment_configuration"] = sentiment_configuration

    @builtins.property
    def type(self) -> "RulesType":
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("RulesType", result)

    @builtins.property
    def issue_detection_configuration(
        self,
    ) -> typing.Optional[IssueDetectionConfiguration]:
        result = self._values.get("issue_detection_configuration")
        return typing.cast(typing.Optional[IssueDetectionConfiguration], result)

    @builtins.property
    def keyword_match_configuration(self) -> typing.Optional[KeywordMatchConfiguration]:
        result = self._values.get("keyword_match_configuration")
        return typing.cast(typing.Optional[KeywordMatchConfiguration], result)

    @builtins.property
    def sentiment_configuration(self) -> typing.Optional["SentimentConfiguration"]:
        result = self._values.get("sentiment_configuration")
        return typing.cast(typing.Optional["SentimentConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Rules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-amazon-chime-resources.RulesType")
class RulesType(enum.Enum):
    KEYWORD_MATCH = "KEYWORD_MATCH"
    SENTIMENT = "SENTIMENT"
    ISSUE_DETECTION = "ISSUE_DETECTION"


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.S3RecordingSinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class S3RecordingSinkConfiguration:
    def __init__(self, *, destination: builtins.str) -> None:
        '''
        :param destination: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f621dc09a1537ba38d1ccb6f9cde9c78051751c709f56fda9e4fac768ccea9b3)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }

    @builtins.property
    def destination(self) -> builtins.str:
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3RecordingSinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.SentimentConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "rule_name": "ruleName",
        "sentiment_type": "sentimentType",
        "time_period": "timePeriod",
    },
)
class SentimentConfiguration:
    def __init__(
        self,
        *,
        rule_name: builtins.str,
        sentiment_type: "SentimentType",
        time_period: jsii.Number,
    ) -> None:
        '''
        :param rule_name: 
        :param sentiment_type: 
        :param time_period: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1be1a4df47ab9cbf24ef68605eb06a085b33650a4189f037707b0aa02852d748)
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument sentiment_type", value=sentiment_type, expected_type=type_hints["sentiment_type"])
            check_type(argname="argument time_period", value=time_period, expected_type=type_hints["time_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_name": rule_name,
            "sentiment_type": sentiment_type,
            "time_period": time_period,
        }

    @builtins.property
    def rule_name(self) -> builtins.str:
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sentiment_type(self) -> "SentimentType":
        result = self._values.get("sentiment_type")
        assert result is not None, "Required property 'sentiment_type' is missing"
        return typing.cast("SentimentType", result)

    @builtins.property
    def time_period(self) -> jsii.Number:
        result = self._values.get("time_period")
        assert result is not None, "Required property 'time_period' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentimentConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-amazon-chime-resources.SentimentType")
class SentimentType(enum.Enum):
    NEGATIVE = "NEGATIVE"


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.ServerSideEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"kms_key_arn": "kmsKeyArn"},
)
class ServerSideEncryptionConfiguration:
    def __init__(self, *, kms_key_arn: builtins.str) -> None:
        '''
        :param kms_key_arn: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bc6d411185f4913b704cc0dba752198bfe0aaa0821b38e63b927d7f5c0f115a)
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_arn": kms_key_arn,
        }

    @builtins.property
    def kms_key_arn(self) -> builtins.str:
        result = self._values.get("kms_key_arn")
        assert result is not None, "Required property 'kms_key_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerSideEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.SipMediaAppProps",
    jsii_struct_bases=[],
    name_mapping={"endpoint": "endpoint", "name": "name", "region": "region"},
)
class SipMediaAppProps:
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Props for ``SipMediaApplication``.

        :param endpoint: endpoint for SipMediaApplication(required). Default: - none
        :param name: name for SipMediaApplication (optional). Default: - unique ID for resource
        :param region: region for SipMediaApplication(required) - Must us-east-1 or us-west-2 and in the same region as the SipMediaApplication Lambda handler. Default: - same region as stack deployment
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1800988fcf2743216f6eab079fae412c1cc4d1fd0a60c264fb6dab0dec2bd5b7)
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint": endpoint,
        }
        if name is not None:
            self._values["name"] = name
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''endpoint for SipMediaApplication(required).

        :default: - none
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''name for SipMediaApplication (optional).

        :default: - unique ID for resource
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''region for SipMediaApplication(required) - Must us-east-1 or us-west-2 and in the same region as the SipMediaApplication Lambda handler.

        :default: - same region as stack deployment
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SipMediaAppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.SipMediaApplicationAlexaSkillConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "alexa_skill_ids": "alexaSkillIds",
        "alexa_skill_status": "alexaSkillStatus",
    },
)
class SipMediaApplicationAlexaSkillConfiguration:
    def __init__(
        self,
        *,
        alexa_skill_ids: typing.Sequence[builtins.str],
        alexa_skill_status: AlexaSkillStatus,
    ) -> None:
        '''
        :param alexa_skill_ids: 
        :param alexa_skill_status: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c9e16054c1863d170b9b208caa0ba2aa47e20d82abe3bd3841cd27e3c34f30f)
            check_type(argname="argument alexa_skill_ids", value=alexa_skill_ids, expected_type=type_hints["alexa_skill_ids"])
            check_type(argname="argument alexa_skill_status", value=alexa_skill_status, expected_type=type_hints["alexa_skill_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alexa_skill_ids": alexa_skill_ids,
            "alexa_skill_status": alexa_skill_status,
        }

    @builtins.property
    def alexa_skill_ids(self) -> typing.List[builtins.str]:
        result = self._values.get("alexa_skill_ids")
        assert result is not None, "Required property 'alexa_skill_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def alexa_skill_status(self) -> AlexaSkillStatus:
        result = self._values.get("alexa_skill_status")
        assert result is not None, "Required property 'alexa_skill_status' is missing"
        return typing.cast(AlexaSkillStatus, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SipMediaApplicationAlexaSkillConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.SipMediaApplicationLoggingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "enable_sip_media_application_message_logs": "enableSipMediaApplicationMessageLogs",
    },
)
class SipMediaApplicationLoggingConfiguration:
    def __init__(
        self,
        *,
        enable_sip_media_application_message_logs: builtins.bool,
    ) -> None:
        '''Props for ``AppInstanceStreamingConfiguration``.

        See: https://docs.aws.amazon.com/chime-sdk/latest/APIReference/API_AppInstanceStreamingConfiguration.html

        :param enable_sip_media_application_message_logs: Enables message logging for the specified SIP media application.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d62db8768173128e1b08db50f094542e716a3b570d3b88e9b91b7ceafc9474b6)
            check_type(argname="argument enable_sip_media_application_message_logs", value=enable_sip_media_application_message_logs, expected_type=type_hints["enable_sip_media_application_message_logs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_sip_media_application_message_logs": enable_sip_media_application_message_logs,
        }

    @builtins.property
    def enable_sip_media_application_message_logs(self) -> builtins.bool:
        '''Enables message logging for the specified SIP media application.'''
        result = self._values.get("enable_sip_media_application_message_logs")
        assert result is not None, "Required property 'enable_sip_media_application_message_logs' is missing"
        return typing.cast(builtins.bool, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SipMediaApplicationLoggingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.SipRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "target_applications": "targetApplications",
        "trigger_type": "triggerType",
        "trigger_value": "triggerValue",
        "name": "name",
    },
)
class SipRuleProps:
    def __init__(
        self,
        *,
        target_applications: typing.Sequence[typing.Union["SipRuleTargetApplication", typing.Dict[builtins.str, typing.Any]]],
        trigger_type: "TriggerType",
        trigger_value: builtins.str,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Props for ``SipRule``.

        :param target_applications: 
        :param trigger_type: Trigger Type for SipRule (required) - TO_PHONE_NUMBER or REQUEST_URI_HOSTNAME. Default: - none
        :param trigger_value: Trigger Value for SipRule (required) - EE.164 Phone Number or Voice Connector URI. Default: - none
        :param name: name for SipRule (optional). Default: - unique ID for resource
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89736ac741fdf808dcb095891a5694b63dd4f0371e5bbc368635a3e619ce1010)
            check_type(argname="argument target_applications", value=target_applications, expected_type=type_hints["target_applications"])
            check_type(argname="argument trigger_type", value=trigger_type, expected_type=type_hints["trigger_type"])
            check_type(argname="argument trigger_value", value=trigger_value, expected_type=type_hints["trigger_value"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_applications": target_applications,
            "trigger_type": trigger_type,
            "trigger_value": trigger_value,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def target_applications(self) -> typing.List["SipRuleTargetApplication"]:
        result = self._values.get("target_applications")
        assert result is not None, "Required property 'target_applications' is missing"
        return typing.cast(typing.List["SipRuleTargetApplication"], result)

    @builtins.property
    def trigger_type(self) -> "TriggerType":
        '''Trigger Type for SipRule (required) - TO_PHONE_NUMBER or REQUEST_URI_HOSTNAME.

        :default: - none
        '''
        result = self._values.get("trigger_type")
        assert result is not None, "Required property 'trigger_type' is missing"
        return typing.cast("TriggerType", result)

    @builtins.property
    def trigger_value(self) -> builtins.str:
        '''Trigger Value for SipRule (required) - EE.164 Phone Number or Voice Connector URI.

        :default: - none
        '''
        result = self._values.get("trigger_value")
        assert result is not None, "Required property 'trigger_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''name for SipRule (optional).

        :default: - unique ID for resource
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SipRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.SipRuleTargetApplication",
    jsii_struct_bases=[],
    name_mapping={
        "priority": "priority",
        "sip_media_application_id": "sipMediaApplicationId",
        "region": "region",
    },
)
class SipRuleTargetApplication:
    def __init__(
        self,
        *,
        priority: jsii.Number,
        sip_media_application_id: builtins.str,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param priority: Priority for SipRule (required) - 1 to 25. Default: - none
        :param sip_media_application_id: SipMediaApplicationId for SipRule (required). Default: - none
        :param region: Region for SipRule (optional). Default: - same region as stack deployment
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c5b839d48377f54265f9cfec24ede27aa6a8c4343f3a3c72630e8aea5ca8635)
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument sip_media_application_id", value=sip_media_application_id, expected_type=type_hints["sip_media_application_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "priority": priority,
            "sip_media_application_id": sip_media_application_id,
        }
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def priority(self) -> jsii.Number:
        '''Priority for SipRule (required) - 1 to 25.

        :default: - none
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def sip_media_application_id(self) -> builtins.str:
        '''SipMediaApplicationId for SipRule (required).

        :default: - none
        '''
        result = self._values.get("sip_media_application_id")
        assert result is not None, "Required property 'sip_media_application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region for SipRule (optional).

        :default: - same region as stack deployment
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SipRuleTargetApplication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.SnsTopicSinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"insights_target": "insightsTarget"},
)
class SnsTopicSinkConfiguration:
    def __init__(self, *, insights_target: builtins.str) -> None:
        '''
        :param insights_target: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f09fd3dc91837bc04c4ab731b92c54a3e158bac3f4c7f5724e8dee69d45724)
            check_type(argname="argument insights_target", value=insights_target, expected_type=type_hints["insights_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "insights_target": insights_target,
        }

    @builtins.property
    def insights_target(self) -> builtins.str:
        result = self._values.get("insights_target")
        assert result is not None, "Required property 'insights_target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsTopicSinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-amazon-chime-resources.SpeakerSearchStatus")
class SpeakerSearchStatus(enum.Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.SqsQueueSinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"insights_target": "insightsTarget"},
)
class SqsQueueSinkConfiguration:
    def __init__(self, *, insights_target: builtins.str) -> None:
        '''
        :param insights_target: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3474b17055c695442aeb69b2f7bf28984ddf61d6852646dfd5673626b2b0e856)
            check_type(argname="argument insights_target", value=insights_target, expected_type=type_hints["insights_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "insights_target": insights_target,
        }

    @builtins.property
    def insights_target(self) -> builtins.str:
        result = self._values.get("insights_target")
        assert result is not None, "Required property 'insights_target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsQueueSinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.Streaming",
    jsii_struct_bases=[],
    name_mapping={
        "data_retention": "dataRetention",
        "enabled": "enabled",
        "notification_targets": "notificationTargets",
        "media_insights_configuration": "mediaInsightsConfiguration",
    },
)
class Streaming:
    def __init__(
        self,
        *,
        data_retention: jsii.Number,
        enabled: builtins.bool,
        notification_targets: typing.Sequence[NotificationTargetType],
        media_insights_configuration: typing.Optional[typing.Union[MediaInsightsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param data_retention: Streaming data retention for VoiceConnector. Default: - 0
        :param enabled: 
        :param notification_targets: Streaming data retention for VoiceConnector. Default: - 0
        :param media_insights_configuration: 
        '''
        if isinstance(media_insights_configuration, dict):
            media_insights_configuration = MediaInsightsConfiguration(**media_insights_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f414427bb66a4ab1b46218b712d0b4741f86dc6c403c4d7db1728d66c225e03)
            check_type(argname="argument data_retention", value=data_retention, expected_type=type_hints["data_retention"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument notification_targets", value=notification_targets, expected_type=type_hints["notification_targets"])
            check_type(argname="argument media_insights_configuration", value=media_insights_configuration, expected_type=type_hints["media_insights_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_retention": data_retention,
            "enabled": enabled,
            "notification_targets": notification_targets,
        }
        if media_insights_configuration is not None:
            self._values["media_insights_configuration"] = media_insights_configuration

    @builtins.property
    def data_retention(self) -> jsii.Number:
        '''Streaming data retention for VoiceConnector.

        :default: - 0
        '''
        result = self._values.get("data_retention")
        assert result is not None, "Required property 'data_retention' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def enabled(self) -> builtins.bool:
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def notification_targets(self) -> typing.List[NotificationTargetType]:
        '''Streaming data retention for VoiceConnector.

        :default: - 0
        '''
        result = self._values.get("notification_targets")
        assert result is not None, "Required property 'notification_targets' is missing"
        return typing.cast(typing.List[NotificationTargetType], result)

    @builtins.property
    def media_insights_configuration(
        self,
    ) -> typing.Optional[MediaInsightsConfiguration]:
        result = self._values.get("media_insights_configuration")
        return typing.cast(typing.Optional[MediaInsightsConfiguration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Streaming(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.StreamingConfig",
    jsii_struct_bases=[],
    name_mapping={"data_type": "dataType", "resource_arn": "resourceArn"},
)
class StreamingConfig:
    def __init__(
        self,
        *,
        data_type: MessagingDataType,
        resource_arn: builtins.str,
    ) -> None:
        '''Props for ``AppInstanceStreamingConfiguration``.

        See: https://docs.aws.amazon.com/chime-sdk/latest/APIReference/API_AppInstanceStreamingConfiguration.html

        :param data_type: The type of data to be streamed.
        :param resource_arn: The resource ARN of a Kinesis Stream.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13050f73faf4d4a7fa215575da8c79326b0e11ea10cfce2fa2d2ccede60fbeba)
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_type": data_type,
            "resource_arn": resource_arn,
        }

    @builtins.property
    def data_type(self) -> MessagingDataType:
        '''The type of data to be streamed.'''
        result = self._values.get("data_type")
        assert result is not None, "Required property 'data_type' is missing"
        return typing.cast(MessagingDataType, result)

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''The resource ARN of a Kinesis Stream.'''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.StreamingConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_instance_arn": "appInstanceArn",
        "streaming_configs": "streamingConfigs",
    },
)
class StreamingConfigurationProps:
    def __init__(
        self,
        *,
        app_instance_arn: builtins.str,
        streaming_configs: typing.Sequence[typing.Union[StreamingConfig, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''Props for ``PutAppInstanceStreamingConfigurations``.

        See: https://docs.aws.amazon.com/chime-sdk/latest/APIReference/API_PutAppInstanceStreamingConfigurations.html

        :param app_instance_arn: The ARN of the App Instance. Default: - None
        :param streaming_configs: The AppInstanceStreamingConfigurations. Default: - None
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61924b4976b5e1dcb35eac5d1cdef7ed3590982687eeca03b8b56f49eaac377d)
            check_type(argname="argument app_instance_arn", value=app_instance_arn, expected_type=type_hints["app_instance_arn"])
            check_type(argname="argument streaming_configs", value=streaming_configs, expected_type=type_hints["streaming_configs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_instance_arn": app_instance_arn,
            "streaming_configs": streaming_configs,
        }

    @builtins.property
    def app_instance_arn(self) -> builtins.str:
        '''The ARN of the App Instance.

        :default: - None
        '''
        result = self._values.get("app_instance_arn")
        assert result is not None, "Required property 'app_instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def streaming_configs(self) -> typing.List[StreamingConfig]:
        '''The AppInstanceStreamingConfigurations.

        :default: - None
        '''
        result = self._values.get("streaming_configs")
        assert result is not None, "Required property 'streaming_configs' is missing"
        return typing.cast(typing.List[StreamingConfig], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamingConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.Termination",
    jsii_struct_bases=[],
    name_mapping={
        "calling_regions": "callingRegions",
        "termination_cidrs": "terminationCidrs",
        "cps": "cps",
    },
)
class Termination:
    def __init__(
        self,
        *,
        calling_regions: typing.Sequence[builtins.str],
        termination_cidrs: typing.Sequence[builtins.str],
        cps: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param calling_regions: Calling Regions for VoiceConnector (optional). Default: - ['US']
        :param termination_cidrs: termination IP for VoiceConnector (optional). Default: - none
        :param cps: CPS Limit. Default: - 1
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9d582d2bde3fddff4ca587aa794f60b27efc8129a4781deadd46f0bbf95df8)
            check_type(argname="argument calling_regions", value=calling_regions, expected_type=type_hints["calling_regions"])
            check_type(argname="argument termination_cidrs", value=termination_cidrs, expected_type=type_hints["termination_cidrs"])
            check_type(argname="argument cps", value=cps, expected_type=type_hints["cps"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "calling_regions": calling_regions,
            "termination_cidrs": termination_cidrs,
        }
        if cps is not None:
            self._values["cps"] = cps

    @builtins.property
    def calling_regions(self) -> typing.List[builtins.str]:
        '''Calling Regions for VoiceConnector (optional).

        :default: - ['US']
        '''
        result = self._values.get("calling_regions")
        assert result is not None, "Required property 'calling_regions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def termination_cidrs(self) -> typing.List[builtins.str]:
        '''termination IP for VoiceConnector (optional).

        :default: - none
        '''
        result = self._values.get("termination_cidrs")
        assert result is not None, "Required property 'termination_cidrs' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cps(self) -> typing.Optional[jsii.Number]:
        '''CPS Limit.

        :default: - 1
        '''
        result = self._values.get("cps")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Termination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-amazon-chime-resources.TriggerType")
class TriggerType(enum.Enum):
    TO_PHONE_NUMBER = "TO_PHONE_NUMBER"
    REQUEST_URI_HOSTNAME = "REQUEST_URI_HOSTNAME"


@jsii.enum(jsii_type="cdk-amazon-chime-resources.VocabularyFilterMethod")
class VocabularyFilterMethod(enum.Enum):
    REMOVE = "REMOVE"
    MASK = "MASK"
    TAG = "TAG"


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.VoiceAnalyticsProcessorConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "speaker_search_status": "speakerSearchStatus",
        "voice_tone_analysis_status": "voiceToneAnalysisStatus",
    },
)
class VoiceAnalyticsProcessorConfiguration:
    def __init__(
        self,
        *,
        speaker_search_status: SpeakerSearchStatus,
        voice_tone_analysis_status: "VoiceToneAnalysisStatus",
    ) -> None:
        '''
        :param speaker_search_status: 
        :param voice_tone_analysis_status: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15fa4c52bfbd645c066f3041df673fb277b6f9a65f3fb6e882e0e3bfaedd33a4)
            check_type(argname="argument speaker_search_status", value=speaker_search_status, expected_type=type_hints["speaker_search_status"])
            check_type(argname="argument voice_tone_analysis_status", value=voice_tone_analysis_status, expected_type=type_hints["voice_tone_analysis_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "speaker_search_status": speaker_search_status,
            "voice_tone_analysis_status": voice_tone_analysis_status,
        }

    @builtins.property
    def speaker_search_status(self) -> SpeakerSearchStatus:
        result = self._values.get("speaker_search_status")
        assert result is not None, "Required property 'speaker_search_status' is missing"
        return typing.cast(SpeakerSearchStatus, result)

    @builtins.property
    def voice_tone_analysis_status(self) -> "VoiceToneAnalysisStatus":
        result = self._values.get("voice_tone_analysis_status")
        assert result is not None, "Required property 'voice_tone_analysis_status' is missing"
        return typing.cast("VoiceToneAnalysisStatus", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VoiceAnalyticsProcessorConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.VoiceConnectorLoggingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "enable_media_metric_logs": "enableMediaMetricLogs",
        "enable_sip_logs": "enableSIPLogs",
    },
)
class VoiceConnectorLoggingConfiguration:
    def __init__(
        self,
        *,
        enable_media_metric_logs: typing.Optional[builtins.bool] = None,
        enable_sip_logs: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param enable_media_metric_logs: 
        :param enable_sip_logs: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64dcb7922680bc224be519c5e7594b88e1acabe4f72e4d0658c8c3fb4f94e571)
            check_type(argname="argument enable_media_metric_logs", value=enable_media_metric_logs, expected_type=type_hints["enable_media_metric_logs"])
            check_type(argname="argument enable_sip_logs", value=enable_sip_logs, expected_type=type_hints["enable_sip_logs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_media_metric_logs is not None:
            self._values["enable_media_metric_logs"] = enable_media_metric_logs
        if enable_sip_logs is not None:
            self._values["enable_sip_logs"] = enable_sip_logs

    @builtins.property
    def enable_media_metric_logs(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_media_metric_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_sip_logs(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_sip_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VoiceConnectorLoggingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.VoiceConnectorProps",
    jsii_struct_bases=[],
    name_mapping={
        "encryption": "encryption",
        "logging_configuration": "loggingConfiguration",
        "name": "name",
        "origination": "origination",
        "region": "region",
        "streaming": "streaming",
        "termination": "termination",
    },
)
class VoiceConnectorProps:
    def __init__(
        self,
        *,
        encryption: typing.Optional[builtins.bool] = None,
        logging_configuration: typing.Optional[typing.Union[VoiceConnectorLoggingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        origination: typing.Optional[typing.Sequence[typing.Union[Routes, typing.Dict[builtins.str, typing.Any]]]] = None,
        region: typing.Optional[builtins.str] = None,
        streaming: typing.Optional[typing.Union[Streaming, typing.Dict[builtins.str, typing.Any]]] = None,
        termination: typing.Optional[typing.Union[Termination, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Props for ``SipMediaApplication``.

        :param encryption: Encryption boolean for VoiceConnector. Default: - False
        :param logging_configuration: 
        :param name: name for VoiceConnector. Default: - unique ID for resource
        :param origination: 
        :param region: region for SipMediaApplication(required) - Must us-east-1 or us-west-2 and in the same region as the SipMediaApplication Lambda handler. Default: - same region as stack deployment
        :param streaming: 
        :param termination: 
        '''
        if isinstance(logging_configuration, dict):
            logging_configuration = VoiceConnectorLoggingConfiguration(**logging_configuration)
        if isinstance(streaming, dict):
            streaming = Streaming(**streaming)
        if isinstance(termination, dict):
            termination = Termination(**termination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bd8e893e1094d68d415fe31b0a78a4d8ce0fb810ef4ab5d04d380bec83b608a)
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument logging_configuration", value=logging_configuration, expected_type=type_hints["logging_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument origination", value=origination, expected_type=type_hints["origination"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument streaming", value=streaming, expected_type=type_hints["streaming"])
            check_type(argname="argument termination", value=termination, expected_type=type_hints["termination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encryption is not None:
            self._values["encryption"] = encryption
        if logging_configuration is not None:
            self._values["logging_configuration"] = logging_configuration
        if name is not None:
            self._values["name"] = name
        if origination is not None:
            self._values["origination"] = origination
        if region is not None:
            self._values["region"] = region
        if streaming is not None:
            self._values["streaming"] = streaming
        if termination is not None:
            self._values["termination"] = termination

    @builtins.property
    def encryption(self) -> typing.Optional[builtins.bool]:
        '''Encryption boolean for VoiceConnector.

        :default: - False
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def logging_configuration(
        self,
    ) -> typing.Optional[VoiceConnectorLoggingConfiguration]:
        result = self._values.get("logging_configuration")
        return typing.cast(typing.Optional[VoiceConnectorLoggingConfiguration], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''name for VoiceConnector.

        :default: - unique ID for resource
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origination(self) -> typing.Optional[typing.List[Routes]]:
        result = self._values.get("origination")
        return typing.cast(typing.Optional[typing.List[Routes]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''region for SipMediaApplication(required) - Must us-east-1 or us-west-2 and in the same region as the SipMediaApplication Lambda handler.

        :default: - same region as stack deployment
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def streaming(self) -> typing.Optional[Streaming]:
        result = self._values.get("streaming")
        return typing.cast(typing.Optional[Streaming], result)

    @builtins.property
    def termination(self) -> typing.Optional[Termination]:
        result = self._values.get("termination")
        return typing.cast(typing.Optional[Termination], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VoiceConnectorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.VoiceProfileDomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "server_side_encryption_configuration": "serverSideEncryptionConfiguration",
        "client_request_token": "clientRequestToken",
        "description": "description",
        "name": "name",
        "tags": "tags",
    },
)
class VoiceProfileDomainProps:
    def __init__(
        self,
        *,
        server_side_encryption_configuration: typing.Union[ServerSideEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]],
        client_request_token: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["VoiceProfileDomainTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param server_side_encryption_configuration: 
        :param client_request_token: 
        :param description: 
        :param name: 
        :param tags: 
        '''
        if isinstance(server_side_encryption_configuration, dict):
            server_side_encryption_configuration = ServerSideEncryptionConfiguration(**server_side_encryption_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffeb5465c4d6c56134993e824bc50f8b5e2228f0c9f32ed0a4e144c85d290b3c)
            check_type(argname="argument server_side_encryption_configuration", value=server_side_encryption_configuration, expected_type=type_hints["server_side_encryption_configuration"])
            check_type(argname="argument client_request_token", value=client_request_token, expected_type=type_hints["client_request_token"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "server_side_encryption_configuration": server_side_encryption_configuration,
        }
        if client_request_token is not None:
            self._values["client_request_token"] = client_request_token
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def server_side_encryption_configuration(self) -> ServerSideEncryptionConfiguration:
        result = self._values.get("server_side_encryption_configuration")
        assert result is not None, "Required property 'server_side_encryption_configuration' is missing"
        return typing.cast(ServerSideEncryptionConfiguration, result)

    @builtins.property
    def client_request_token(self) -> typing.Optional[builtins.str]:
        result = self._values.get("client_request_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["VoiceProfileDomainTag"]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["VoiceProfileDomainTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VoiceProfileDomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.VoiceProfileDomainTag",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class VoiceProfileDomainTag:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: 
        :param value: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1faaf18f7494ff4d12a8a2e46f783271e4a67a2f1d0ac48a8cdc49f035ee44d9)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VoiceProfileDomainTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-amazon-chime-resources.VoiceToneAnalysisStatus")
class VoiceToneAnalysisStatus(enum.Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


__all__ = [
    "AlexaSkillStatus",
    "AmazonTranscribeCallAnalyticsProcessorConfiguration",
    "AmazonTranscribeProcessorConfiguration",
    "AppInstanceAdminProps",
    "AppInstanceBotConfiguration",
    "AppInstanceBotLexConfiguration",
    "AppInstanceBotProps",
    "AppInstanceProps",
    "AppInstanceStreamingConfigurations",
    "AppInstanceTags",
    "AppInstanceUserProps",
    "ChannelFlow",
    "ChannelFlowProps",
    "ChannelFlowTags",
    "ChimePhoneNumber",
    "ChimeSipMediaApp",
    "ChimeSipRule",
    "ChimeVoiceConnector",
    "ChimeVoiceProfileDomain",
    "Configuration",
    "ContentIdentificationType",
    "ContentRedactionOutput",
    "ContentRedactionType",
    "Elements",
    "ElementsType",
    "FallbackAction",
    "InstanceBotTags",
    "InstanceUserTags",
    "InvocationType",
    "IssueDetectionConfiguration",
    "KeywordMatchConfiguration",
    "KinesisDataStreamSinkConfiguration",
    "Lambda",
    "LambdaFunctionSinkConfiguration",
    "LanguageCode",
    "LexConfigurationRespondsTo",
    "MediaInsightsConfiguration",
    "MediaInsightsPipeline",
    "MediaInsightsPipelineProps",
    "MediaPipelineInsightsTag",
    "MessagingAppInstance",
    "MessagingAppInstanceAdmin",
    "MessagingAppInstanceBot",
    "MessagingAppInstanceUser",
    "MessagingDataType",
    "MessagingResourceProps",
    "MessagingResources",
    "NotificationTargetType",
    "PSTNResourceProps",
    "PSTNResources",
    "PartialResultsStability",
    "PhoneCountry",
    "PhoneNumberProps",
    "PhoneNumberType",
    "PhoneProductType",
    "PostCallAnalyticsSettings",
    "Processors",
    "Protocol",
    "RealTimeAlertConfiguration",
    "Routes",
    "Rules",
    "RulesType",
    "S3RecordingSinkConfiguration",
    "SentimentConfiguration",
    "SentimentType",
    "ServerSideEncryptionConfiguration",
    "SipMediaAppProps",
    "SipMediaApplicationAlexaSkillConfiguration",
    "SipMediaApplicationLoggingConfiguration",
    "SipRuleProps",
    "SipRuleTargetApplication",
    "SnsTopicSinkConfiguration",
    "SpeakerSearchStatus",
    "SqsQueueSinkConfiguration",
    "Streaming",
    "StreamingConfig",
    "StreamingConfigurationProps",
    "Termination",
    "TriggerType",
    "VocabularyFilterMethod",
    "VoiceAnalyticsProcessorConfiguration",
    "VoiceConnectorLoggingConfiguration",
    "VoiceConnectorProps",
    "VoiceProfileDomainProps",
    "VoiceProfileDomainTag",
    "VoiceToneAnalysisStatus",
]

publication.publish()

def _typecheckingstub__79208c31cb44a1d663acf03b7c40c60fbd13a5cfad1ac090cbfbcddd566f31f2(
    *,
    language_code: LanguageCode,
    call_analytics_stream_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    content_identification_type: typing.Optional[ContentIdentificationType] = None,
    content_redaction_type: typing.Optional[ContentRedactionType] = None,
    enable_partial_results_stabilization: typing.Optional[builtins.bool] = None,
    filter_partial_results: typing.Optional[builtins.bool] = None,
    language_model_name: typing.Optional[builtins.str] = None,
    partial_results_stability: typing.Optional[PartialResultsStability] = None,
    pii_entity_types: typing.Optional[builtins.str] = None,
    post_call_analytics_settings: typing.Optional[typing.Union[PostCallAnalyticsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    vocabulary_filter_method: typing.Optional[VocabularyFilterMethod] = None,
    vocabulary_filter_name: typing.Optional[builtins.str] = None,
    vocabulary_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6144a5c0e924118e78f03a8dfb38cc1521ec946a8703b571a6202c66cee502d(
    *,
    language_code: LanguageCode,
    content_identification_type: typing.Optional[ContentIdentificationType] = None,
    content_redaction_type: typing.Optional[ContentRedactionType] = None,
    enable_partial_results_stabilization: typing.Optional[builtins.bool] = None,
    filter_partial_results: typing.Optional[builtins.bool] = None,
    language_model_name: typing.Optional[builtins.str] = None,
    partial_results_stability: typing.Optional[PartialResultsStability] = None,
    pii_entity_types: typing.Optional[builtins.str] = None,
    show_speaker_label: typing.Optional[builtins.bool] = None,
    vocabulary_filter_method: typing.Optional[VocabularyFilterMethod] = None,
    vocabulary_filter_name: typing.Optional[builtins.str] = None,
    vocabulary_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8613bd8924c62f360b8fd11191005b6b40de3e5805e2906daf559c0c4591022d(
    *,
    app_instance_admin_arn: builtins.str,
    app_instance_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__190753a8664ba7ea97729e7c4d6d1834c2054c274acf0d3d9b76090a2a2e392a(
    *,
    lex: typing.Union[AppInstanceBotLexConfiguration, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a903a5ac908975450f7ca736d64edea6baf40428ec15f115e16ac1960f6206a3(
    *,
    lex_bot_alias_arn: builtins.str,
    locale_id: builtins.str,
    responds_to: LexConfigurationRespondsTo,
    welcome_intent: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f2d70e0e345c32a108d1b5e826706bde29fa7b412c11d521a2baab05d643ef(
    *,
    app_instance_arn: builtins.str,
    configuration: typing.Union[AppInstanceBotConfiguration, typing.Dict[builtins.str, typing.Any]],
    client_request_token: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[InstanceBotTags, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99641216bdb1ac5ae72a17b34ac6ca8ff8cbb075d8ddc07e9db8b47a39a2e63c(
    *,
    client_request_token: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[AppInstanceTags, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b5592853474342b6381b5e6c00a9b05345b286c1268a4def64d116f5fc5143(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app_instance_arn: builtins.str,
    streaming_configs: typing.Sequence[typing.Union[StreamingConfig, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e7c2248211c91c5400947a073a327c5891999890c50d304103a4b2ede75eda(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f1d2afec2a1ee54c9c8c65d06e6449432e7ccd47c39718154ace20f293608b(
    *,
    app_instance_arn: builtins.str,
    app_instance_user_id: builtins.str,
    client_request_token: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[InstanceUserTags, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c12dc139a0c6c2028b7459eefbf26ae09174ec3a969cc2f61ac8d92aac274d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app_instance_arn: builtins.str,
    client_request_token: builtins.str,
    processors: typing.Sequence[typing.Union[Processors, typing.Dict[builtins.str, typing.Any]]],
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[ChannelFlowTags, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4318c557157fab467f7f5003cd7f6be7ef8ee2b6efc6a633e86ac38c75fc6aaf(
    *,
    app_instance_arn: builtins.str,
    client_request_token: builtins.str,
    processors: typing.Sequence[typing.Union[Processors, typing.Dict[builtins.str, typing.Any]]],
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[ChannelFlowTags, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__423e2b447054eb5049c198e4c2c919b7bcdaeb6ee0e8a7b3792d33ee6a0b1d7b(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7115b79d2edc74ff917d518a81f7a6651e02418753fab2a2a35e2bff1587b5a7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    phone_product_type: PhoneProductType,
    phone_area_code: typing.Optional[jsii.Number] = None,
    phone_city: typing.Optional[builtins.str] = None,
    phone_country: typing.Optional[PhoneCountry] = None,
    phone_number_toll_free_prefix: typing.Optional[jsii.Number] = None,
    phone_number_type: typing.Optional[PhoneNumberType] = None,
    phone_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113f835f1247755909e4fbd1d3eb6d53265ab846dcd51487ecbfc26db4f5e50b(
    voice_connector_id: ChimeVoiceConnector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37db274aeecb4545734b8fe6863b37da6a06c91ab04fbd007ee1878c7cfc2cf(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    endpoint: builtins.str,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a8ee26df03196f53b578da14beb4b9253b7c5e47bb51611c9cefd974b2996b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    target_applications: typing.Sequence[typing.Union[SipRuleTargetApplication, typing.Dict[builtins.str, typing.Any]]],
    trigger_type: TriggerType,
    trigger_value: builtins.str,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3322e6fa91f7b318e813d5bf83683474955e25e8180642a7921f91e501c051de(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    encryption: typing.Optional[builtins.bool] = None,
    logging_configuration: typing.Optional[typing.Union[VoiceConnectorLoggingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    origination: typing.Optional[typing.Sequence[typing.Union[Routes, typing.Dict[builtins.str, typing.Any]]]] = None,
    region: typing.Optional[builtins.str] = None,
    streaming: typing.Optional[typing.Union[Streaming, typing.Dict[builtins.str, typing.Any]]] = None,
    termination: typing.Optional[typing.Union[Termination, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0fc61758880ca42be4625a894cd88dc46a46e2648a09cdc061099fef6d75d2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    server_side_encryption_configuration: typing.Union[ServerSideEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]],
    client_request_token: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[VoiceProfileDomainTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4571f43b9d6d9c78c9a4194cd81c8f6d0723c84dfad67e0dc37cee78b008d9b5(
    *,
    lambda_: typing.Union[Lambda, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c8270166e256f6acc8ed44f959fcc2423bbdfa1366007fa7934305820464d8(
    *,
    type: ElementsType,
    amazon_transcribe_call_analytics_processor_configuration: typing.Optional[typing.Union[AmazonTranscribeCallAnalyticsProcessorConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    amazon_transcribe_processor_configuration: typing.Optional[typing.Union[AmazonTranscribeProcessorConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis_data_stream_sink_configuration: typing.Optional[typing.Union[KinesisDataStreamSinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_function_sink_configuration: typing.Optional[typing.Union[LambdaFunctionSinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_recording_sink_configuration: typing.Optional[typing.Union[S3RecordingSinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    sns_topic_sink_configuration: typing.Optional[typing.Union[SnsTopicSinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    sqs_queue_sink_configuration: typing.Optional[typing.Union[SqsQueueSinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    voice_analytics_processor_configuration: typing.Optional[typing.Union[VoiceAnalyticsProcessorConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466e1fc6ac2865f25390b9cd8e5cf20df99008f2afbc5e9b1525746d6e5e4d0b(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73075b4d361aeb287fc052a39e6ab5aa8840b8d2c65afb20519d4ff51266dc64(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab246d92d61207ce86ecb74c94285dea93a8dd2924e18ae9f6fddd0396b6a415(
    *,
    rule_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64725845ce6afa3341958fde6bfa8db2429f6d1ecf85d69a1b86c761ae8d3ddb(
    *,
    keywords: typing.Sequence[builtins.str],
    rule_name: builtins.str,
    negate: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04bdccaa55d185310cf53553bb92d683f06df4a8a44c499b3136280f57f5e961(
    *,
    insights_target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__578b648f0cf5bcbae9bf298c3b4ec202747ea61fcc36e3c12421adbf714050a6(
    *,
    invocation_type: InvocationType,
    resource_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad1da5fd4a9bb89891753d494e60eaff7b4500917ff9ba2c3057b720c1ddb65(
    *,
    insights_target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d3fd94ae5af25b8c7bbd19af5501900af73d8db411381ec98cf7c788dbbcc45(
    *,
    configuration_arn: builtins.str,
    disabled: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__498d2a9395dfedaec2caffb27327afd8a3d5cd1f27f7f3e971bc1ef8c85745d8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    elements: typing.Sequence[typing.Union[Elements, typing.Dict[builtins.str, typing.Any]]],
    resource_access_role_arn: builtins.str,
    client_request_token: typing.Optional[builtins.str] = None,
    media_insights_pipeline_configuration_name: typing.Optional[builtins.str] = None,
    real_time_alert_configuration: typing.Optional[typing.Union[RealTimeAlertConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[MediaPipelineInsightsTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb0c085f4f2337763da4b7a97077d9be818b2ed003e6600afd55e3203733a579(
    *,
    elements: typing.Sequence[typing.Union[Elements, typing.Dict[builtins.str, typing.Any]]],
    resource_access_role_arn: builtins.str,
    client_request_token: typing.Optional[builtins.str] = None,
    media_insights_pipeline_configuration_name: typing.Optional[builtins.str] = None,
    real_time_alert_configuration: typing.Optional[typing.Union[RealTimeAlertConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[MediaPipelineInsightsTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2931f7be952ca8d873e6ad2f1c824103c35c9e8e7f4e95b985d45b95774656a4(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9f012fab9eb0d816a78f8f21fb2b6ca54774f162a1dd5769f1628ac6f2e8c9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    client_request_token: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[AppInstanceTags, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da36a029e1afaaefc489c020934e45363195f10c5727d992a321c13b0043e2c0(
    days: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11016e616c0eecf971ad1b8d44cee41698040c9f7bb7fc2ef89c3f2b4668454(
    streaming_configs: typing.Sequence[typing.Union[StreamingConfig, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40803d0180de29a1b7d03d21acba148c27c1a6eab510cd87e687d82d6108b3d5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app_instance_admin_arn: builtins.str,
    app_instance_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fab735ff921a58db4ce197742abd231baa840546c2d4a14735be63e8de8059d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app_instance_arn: builtins.str,
    configuration: typing.Union[AppInstanceBotConfiguration, typing.Dict[builtins.str, typing.Any]],
    client_request_token: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[InstanceBotTags, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301eef12c49f4f86623f7326244dcbc9fc1774d26e08b7f5e344906a9f195cba(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app_instance_arn: builtins.str,
    app_instance_user_id: builtins.str,
    client_request_token: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[InstanceUserTags, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7688c29fcfcbe8ff3316837ef27d8a5c7629b1f3879e46ab246754bb9571664f(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    properties: typing.Mapping[builtins.str, typing.Any],
    resource_type: builtins.str,
    uid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c733c0cc8a171d0914be8696b8353206a7d5a17dbbdb5ab2171cdd3ffd266e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    properties: typing.Mapping[builtins.str, typing.Any],
    resource_type: builtins.str,
    uid: builtins.str,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e7326b3c0a86e27b49bf3d1d67d25db6fc4d4e818fb652a26c9b1a4959e1677(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    properties: typing.Mapping[builtins.str, typing.Any],
    resource_type: builtins.str,
    uid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9372fb4e09a36da7cfd84d9bf339c9f4439d92326a5b861b6e029af5d9c892(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    properties: typing.Mapping[builtins.str, typing.Any],
    resource_type: builtins.str,
    uid: builtins.str,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5b2ac2a9588b05b4d090bb324c4de18ab13008479ac747fb4c76d5aef2bc55(
    *,
    phone_product_type: PhoneProductType,
    phone_area_code: typing.Optional[jsii.Number] = None,
    phone_city: typing.Optional[builtins.str] = None,
    phone_country: typing.Optional[PhoneCountry] = None,
    phone_number_toll_free_prefix: typing.Optional[jsii.Number] = None,
    phone_number_type: typing.Optional[PhoneNumberType] = None,
    phone_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2244030f4fbace1e42d75ad09edd84b32e2f9a0187eadc9b372362afd6ebe8bc(
    *,
    data_access_role_arn: builtins.str,
    output_location: builtins.str,
    content_redaction_output: typing.Optional[ContentRedactionOutput] = None,
    output_encryption_kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ddb27d8877eb97beb38e78204072b302c0a15e44306cc7d732983b023c5ee5(
    *,
    configuration: typing.Union[Configuration, typing.Dict[builtins.str, typing.Any]],
    execution_order: jsii.Number,
    fallback_action: FallbackAction,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ba3e8e37516ce401aaf6bcbb6c3f1807abfdcda524f29ac31dc808ecdf0086(
    *,
    disabled: builtins.bool,
    rules: typing.Sequence[typing.Union[Rules, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb30c4d59c6038c4d49567f143b8a4b4b5355d6c06cc090d64ec9ceaf4ae31ca(
    *,
    host: builtins.str,
    port: jsii.Number,
    priority: jsii.Number,
    protocol: Protocol,
    weight: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55b52d3daeeca4614bae10450af6c08fa2c6cdeda17a78af05d8f2416d41d85(
    *,
    type: RulesType,
    issue_detection_configuration: typing.Optional[typing.Union[IssueDetectionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    keyword_match_configuration: typing.Optional[typing.Union[KeywordMatchConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    sentiment_configuration: typing.Optional[typing.Union[SentimentConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f621dc09a1537ba38d1ccb6f9cde9c78051751c709f56fda9e4fac768ccea9b3(
    *,
    destination: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1be1a4df47ab9cbf24ef68605eb06a085b33650a4189f037707b0aa02852d748(
    *,
    rule_name: builtins.str,
    sentiment_type: SentimentType,
    time_period: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc6d411185f4913b704cc0dba752198bfe0aaa0821b38e63b927d7f5c0f115a(
    *,
    kms_key_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1800988fcf2743216f6eab079fae412c1cc4d1fd0a60c264fb6dab0dec2bd5b7(
    *,
    endpoint: builtins.str,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c9e16054c1863d170b9b208caa0ba2aa47e20d82abe3bd3841cd27e3c34f30f(
    *,
    alexa_skill_ids: typing.Sequence[builtins.str],
    alexa_skill_status: AlexaSkillStatus,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d62db8768173128e1b08db50f094542e716a3b570d3b88e9b91b7ceafc9474b6(
    *,
    enable_sip_media_application_message_logs: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89736ac741fdf808dcb095891a5694b63dd4f0371e5bbc368635a3e619ce1010(
    *,
    target_applications: typing.Sequence[typing.Union[SipRuleTargetApplication, typing.Dict[builtins.str, typing.Any]]],
    trigger_type: TriggerType,
    trigger_value: builtins.str,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5b839d48377f54265f9cfec24ede27aa6a8c4343f3a3c72630e8aea5ca8635(
    *,
    priority: jsii.Number,
    sip_media_application_id: builtins.str,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f09fd3dc91837bc04c4ab731b92c54a3e158bac3f4c7f5724e8dee69d45724(
    *,
    insights_target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3474b17055c695442aeb69b2f7bf28984ddf61d6852646dfd5673626b2b0e856(
    *,
    insights_target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f414427bb66a4ab1b46218b712d0b4741f86dc6c403c4d7db1728d66c225e03(
    *,
    data_retention: jsii.Number,
    enabled: builtins.bool,
    notification_targets: typing.Sequence[NotificationTargetType],
    media_insights_configuration: typing.Optional[typing.Union[MediaInsightsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13050f73faf4d4a7fa215575da8c79326b0e11ea10cfce2fa2d2ccede60fbeba(
    *,
    data_type: MessagingDataType,
    resource_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61924b4976b5e1dcb35eac5d1cdef7ed3590982687eeca03b8b56f49eaac377d(
    *,
    app_instance_arn: builtins.str,
    streaming_configs: typing.Sequence[typing.Union[StreamingConfig, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9d582d2bde3fddff4ca587aa794f60b27efc8129a4781deadd46f0bbf95df8(
    *,
    calling_regions: typing.Sequence[builtins.str],
    termination_cidrs: typing.Sequence[builtins.str],
    cps: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15fa4c52bfbd645c066f3041df673fb277b6f9a65f3fb6e882e0e3bfaedd33a4(
    *,
    speaker_search_status: SpeakerSearchStatus,
    voice_tone_analysis_status: VoiceToneAnalysisStatus,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64dcb7922680bc224be519c5e7594b88e1acabe4f72e4d0658c8c3fb4f94e571(
    *,
    enable_media_metric_logs: typing.Optional[builtins.bool] = None,
    enable_sip_logs: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd8e893e1094d68d415fe31b0a78a4d8ce0fb810ef4ab5d04d380bec83b608a(
    *,
    encryption: typing.Optional[builtins.bool] = None,
    logging_configuration: typing.Optional[typing.Union[VoiceConnectorLoggingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    origination: typing.Optional[typing.Sequence[typing.Union[Routes, typing.Dict[builtins.str, typing.Any]]]] = None,
    region: typing.Optional[builtins.str] = None,
    streaming: typing.Optional[typing.Union[Streaming, typing.Dict[builtins.str, typing.Any]]] = None,
    termination: typing.Optional[typing.Union[Termination, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffeb5465c4d6c56134993e824bc50f8b5e2228f0c9f32ed0a4e144c85d290b3c(
    *,
    server_side_encryption_configuration: typing.Union[ServerSideEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]],
    client_request_token: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[VoiceProfileDomainTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1faaf18f7494ff4d12a8a2e46f783271e4a67a2f1d0ac48a8cdc49f035ee44d9(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
