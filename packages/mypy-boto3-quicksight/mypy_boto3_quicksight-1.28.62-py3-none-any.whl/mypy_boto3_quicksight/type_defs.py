"""
Type annotations for quicksight service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/type_defs/)

Usage::

    ```python
    from mypy_boto3_quicksight.type_defs import AccountCustomizationTypeDef

    data: AccountCustomizationTypeDef = ...
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AnalysisErrorTypeType,
    AnalysisFilterAttributeType,
    ArcThicknessOptionsType,
    ArcThicknessType,
    AssetBundleExportFormatType,
    AssetBundleExportJobDataSourcePropertyToOverrideType,
    AssetBundleExportJobStatusType,
    AssetBundleExportJobVPCConnectionPropertyToOverrideType,
    AssetBundleImportFailureActionType,
    AssetBundleImportJobStatusType,
    AssignmentStatusType,
    AuthenticationMethodOptionType,
    AuthorSpecifiedAggregationType,
    AxisBindingType,
    BarChartOrientationType,
    BarsArrangementType,
    BaseMapStyleTypeType,
    BoxPlotFillStyleType,
    CategoricalAggregationFunctionType,
    CategoryFilterFunctionType,
    CategoryFilterMatchOperatorType,
    CategoryFilterTypeType,
    ColorFillTypeType,
    ColumnDataRoleType,
    ColumnDataTypeType,
    ColumnOrderingTypeType,
    ColumnRoleType,
    ColumnTagNameType,
    ComparisonMethodType,
    ConditionalFormattingIconSetTypeType,
    ConstantTypeType,
    CrossDatasetTypesType,
    CustomContentImageScalingConfigurationType,
    CustomContentTypeType,
    DashboardBehaviorType,
    DashboardErrorTypeType,
    DashboardFilterAttributeType,
    DashboardUIStateType,
    DataLabelContentType,
    DataLabelOverlapType,
    DataLabelPositionType,
    DataSetFilterAttributeType,
    DataSetImportModeType,
    DatasetParameterValueTypeType,
    DataSourceErrorInfoTypeType,
    DataSourceFilterAttributeType,
    DataSourceTypeType,
    DateAggregationFunctionType,
    DayOfWeekType,
    DefaultAggregationType,
    DisplayFormatType,
    EditionType,
    EmbeddingIdentityTypeType,
    FileFormatType,
    FilterClassType,
    FilterNullOptionType,
    FilterOperatorType,
    FilterVisualScopeType,
    FolderFilterAttributeType,
    FontDecorationType,
    FontStyleType,
    FontWeightNameType,
    ForecastComputationSeasonalityType,
    FunnelChartMeasureDataLabelStyleType,
    GeoSpatialDataRoleType,
    GeospatialSelectedPointStyleType,
    HistogramBinTypeType,
    HorizontalTextAlignmentType,
    IconType,
    IdentityTypeType,
    IngestionErrorTypeType,
    IngestionRequestSourceType,
    IngestionRequestTypeType,
    IngestionStatusType,
    IngestionTypeType,
    InputColumnDataTypeType,
    JoinTypeType,
    KPISparklineTypeType,
    KPIVisualStandardLayoutTypeType,
    LayoutElementTypeType,
    LegendPositionType,
    LineChartLineStyleType,
    LineChartMarkerShapeType,
    LineChartTypeType,
    LineInterpolationType,
    LookbackWindowSizeUnitType,
    MapZoomModeType,
    MaximumMinimumComputationTypeType,
    MemberTypeType,
    MissingDataTreatmentOptionType,
    NamedEntityAggTypeType,
    NamedFilterAggTypeType,
    NamedFilterTypeType,
    NamespaceErrorTypeType,
    NamespaceStatusType,
    NegativeValueDisplayModeType,
    NetworkInterfaceStatusType,
    NumberScaleType,
    NumericEqualityMatchOperatorType,
    NumericSeparatorSymbolType,
    OtherCategoriesType,
    PanelBorderStyleType,
    PaperOrientationType,
    PaperSizeType,
    ParameterValueTypeType,
    PivotTableConditionalFormattingScopeRoleType,
    PivotTableFieldCollapseStateType,
    PivotTableMetricPlacementType,
    PivotTableRowsLayoutType,
    PivotTableSubtotalLevelType,
    PrimaryValueDisplayTypeType,
    PropertyRoleType,
    PropertyUsageType,
    RadarChartAxesRangeScaleType,
    RadarChartShapeType,
    ReferenceLineLabelHorizontalPositionType,
    ReferenceLineLabelVerticalPositionType,
    ReferenceLinePatternTypeType,
    ReferenceLineValueLabelRelativePositionType,
    RefreshIntervalType,
    RelativeDateTypeType,
    RelativeFontSizeType,
    ResizeOptionType,
    ResourceStatusType,
    RowLevelPermissionFormatVersionType,
    RowLevelPermissionPolicyType,
    SectionPageBreakStatusType,
    SelectedTooltipTypeType,
    SharingModelType,
    SheetContentTypeType,
    SheetControlDateTimePickerTypeType,
    SheetControlListTypeType,
    SheetControlSliderTypeType,
    SimpleNumericalAggregationFunctionType,
    SmallMultiplesAxisPlacementType,
    SmallMultiplesAxisScaleType,
    SnapshotFileFormatTypeType,
    SnapshotFileSheetSelectionScopeType,
    SnapshotJobStatusType,
    SortDirectionType,
    SpecialValueType,
    StatusType,
    StyledCellTypeType,
    TableBorderStyleType,
    TableCellImageScalingConfigurationType,
    TableOrientationType,
    TableTotalsPlacementType,
    TableTotalsScrollStatusType,
    TemplateErrorTypeType,
    TextQualifierType,
    TextWrapType,
    ThemeTypeType,
    TimeGranularityType,
    TooltipTitleTypeType,
    TopBottomComputationTypeType,
    TopBottomSortOrderType,
    TopicNumericSeparatorSymbolType,
    TopicRefreshStatusType,
    TopicRelativeDateFilterFunctionType,
    TopicScheduleTypeType,
    TopicTimeGranularityType,
    UndefinedSpecifiedValueTypeType,
    URLTargetConfigurationType,
    UserRoleType,
    ValidationStrategyModeType,
    ValueWhenUnsetOptionType,
    VerticalTextAlignmentType,
    VisibilityType,
    VisualCustomActionTriggerType,
    VPCConnectionAvailabilityStatusType,
    VPCConnectionResourceStatusType,
    WidgetStatusType,
    WordCloudCloudLayoutType,
    WordCloudWordCasingType,
    WordCloudWordOrientationType,
    WordCloudWordPaddingType,
    WordCloudWordScalingType,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AccountCustomizationTypeDef",
    "AccountInfoTypeDef",
    "AccountSettingsTypeDef",
    "ActiveIAMPolicyAssignmentTypeDef",
    "AdHocFilteringOptionTypeDef",
    "AttributeAggregationFunctionTypeDef",
    "ColumnIdentifierTypeDef",
    "AmazonElasticsearchParametersTypeDef",
    "AmazonOpenSearchParametersTypeDef",
    "CalculatedFieldTypeDef",
    "DataSetIdentifierDeclarationTypeDef",
    "EntityTypeDef",
    "AnalysisSearchFilterTypeDef",
    "DataSetReferenceTypeDef",
    "AnalysisSummaryTypeDef",
    "SheetTypeDef",
    "AnchorDateConfigurationTypeDef",
    "AnonymousUserDashboardEmbeddingConfigurationTypeDef",
    "DashboardVisualIdTypeDef",
    "AnonymousUserQSearchBarEmbeddingConfigurationTypeDef",
    "ArcAxisDisplayRangeTypeDef",
    "ArcConfigurationTypeDef",
    "ArcOptionsTypeDef",
    "AssetBundleExportJobAnalysisOverridePropertiesTypeDef",
    "AssetBundleExportJobDashboardOverridePropertiesTypeDef",
    "AssetBundleExportJobDataSetOverridePropertiesTypeDef",
    "AssetBundleExportJobDataSourceOverridePropertiesTypeDef",
    "AssetBundleExportJobRefreshScheduleOverridePropertiesTypeDef",
    "AssetBundleExportJobResourceIdOverrideConfigurationTypeDef",
    "AssetBundleExportJobThemeOverridePropertiesTypeDef",
    "AssetBundleExportJobVPCConnectionOverridePropertiesTypeDef",
    "AssetBundleExportJobErrorTypeDef",
    "AssetBundleExportJobSummaryTypeDef",
    "AssetBundleImportJobAnalysisOverrideParametersTypeDef",
    "AssetBundleImportJobDashboardOverrideParametersTypeDef",
    "AssetBundleImportJobDataSetOverrideParametersTypeDef",
    "AssetBundleImportJobDataSourceCredentialPairTypeDef",
    "SslPropertiesTypeDef",
    "VpcConnectionPropertiesTypeDef",
    "AssetBundleImportJobErrorTypeDef",
    "AssetBundleImportJobRefreshScheduleOverrideParametersTypeDef",
    "AssetBundleImportJobResourceIdOverrideConfigurationTypeDef",
    "AssetBundleImportJobThemeOverrideParametersTypeDef",
    "AssetBundleImportJobVPCConnectionOverrideParametersTypeDef",
    "AssetBundleImportJobSummaryTypeDef",
    "AssetBundleImportSourceDescriptionTypeDef",
    "BlobTypeDef",
    "AthenaParametersTypeDef",
    "AuroraParametersTypeDef",
    "AuroraPostgreSqlParametersTypeDef",
    "AwsIotAnalyticsParametersTypeDef",
    "DateAxisOptionsTypeDef",
    "AxisDisplayMinMaxRangeTypeDef",
    "AxisLinearScaleTypeDef",
    "AxisLogarithmicScaleTypeDef",
    "ItemsLimitConfigurationTypeDef",
    "BinCountOptionsTypeDef",
    "BinWidthOptionsTypeDef",
    "BookmarksConfigurationsTypeDef",
    "BorderStyleTypeDef",
    "BoxPlotStyleOptionsTypeDef",
    "PaginationConfigurationTypeDef",
    "CalculatedColumnTypeDef",
    "CalculatedMeasureFieldTypeDef",
    "CancelIngestionRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CastColumnTypeOperationTypeDef",
    "CustomFilterConfigurationTypeDef",
    "CustomFilterListConfigurationTypeDef",
    "FilterListConfigurationTypeDef",
    "CellValueSynonymTypeDef",
    "SimpleClusterMarkerTypeDef",
    "CollectiveConstantTypeDef",
    "DataColorTypeDef",
    "CustomColorTypeDef",
    "ColumnDescriptionTypeDef",
    "ColumnGroupColumnSchemaTypeDef",
    "GeoSpatialColumnGroupTypeDef",
    "ColumnLevelPermissionRuleTypeDef",
    "ColumnSchemaTypeDef",
    "ComparativeOrderTypeDef",
    "ConditionalFormattingSolidColorTypeDef",
    "ConditionalFormattingCustomIconOptionsTypeDef",
    "ConditionalFormattingIconDisplayConfigurationTypeDef",
    "ConditionalFormattingIconSetTypeDef",
    "TagTypeDef",
    "CreateAccountSubscriptionRequestRequestTypeDef",
    "SignupResponseTypeDef",
    "ResourcePermissionTypeDef",
    "ValidationStrategyTypeDef",
    "DataSetUsageConfigurationTypeDef",
    "FieldFolderTypeDef",
    "RowLevelPermissionDataSetTypeDef",
    "CreateFolderMembershipRequestRequestTypeDef",
    "FolderMemberTypeDef",
    "CreateGroupMembershipRequestRequestTypeDef",
    "GroupMemberTypeDef",
    "CreateGroupRequestRequestTypeDef",
    "GroupTypeDef",
    "CreateIAMPolicyAssignmentRequestRequestTypeDef",
    "CreateIngestionRequestRequestTypeDef",
    "CreateTemplateAliasRequestRequestTypeDef",
    "TemplateAliasTypeDef",
    "CreateThemeAliasRequestRequestTypeDef",
    "ThemeAliasTypeDef",
    "DecimalPlacesConfigurationTypeDef",
    "NegativeValueConfigurationTypeDef",
    "NullValueFormatConfigurationTypeDef",
    "LocalNavigationConfigurationTypeDef",
    "CustomActionURLOperationTypeDef",
    "CustomContentConfigurationTypeDef",
    "CustomNarrativeOptionsTypeDef",
    "TimestampTypeDef",
    "InputColumnTypeDef",
    "DataPointDrillUpDownOptionTypeDef",
    "DataPointMenuLabelOptionTypeDef",
    "DataPointTooltipOptionTypeDef",
    "ExportToCSVOptionTypeDef",
    "ExportWithHiddenFieldsOptionTypeDef",
    "SheetControlsOptionTypeDef",
    "SheetLayoutElementMaximizationOptionTypeDef",
    "VisualAxisSortOptionTypeDef",
    "VisualMenuOptionTypeDef",
    "DashboardSearchFilterTypeDef",
    "DashboardSummaryTypeDef",
    "DashboardVersionSummaryTypeDef",
    "ExportHiddenFieldsOptionTypeDef",
    "DataAggregationTypeDef",
    "DataBarsOptionsTypeDef",
    "DataColorPaletteTypeDef",
    "DataPathLabelTypeTypeDef",
    "FieldLabelTypeTypeDef",
    "MaximumLabelTypeTypeDef",
    "MinimumLabelTypeTypeDef",
    "RangeEndsLabelTypeTypeDef",
    "DataPathValueTypeDef",
    "DataSetSearchFilterTypeDef",
    "OutputColumnTypeDef",
    "DataSourceErrorInfoTypeDef",
    "DatabricksParametersTypeDef",
    "ExasolParametersTypeDef",
    "JiraParametersTypeDef",
    "MariaDbParametersTypeDef",
    "MySqlParametersTypeDef",
    "OracleParametersTypeDef",
    "PostgreSqlParametersTypeDef",
    "PrestoParametersTypeDef",
    "RdsParametersTypeDef",
    "ServiceNowParametersTypeDef",
    "SnowflakeParametersTypeDef",
    "SparkParametersTypeDef",
    "SqlServerParametersTypeDef",
    "TeradataParametersTypeDef",
    "TwitterParametersTypeDef",
    "DataSourceSearchFilterTypeDef",
    "DataSourceSummaryTypeDef",
    "RollingDateConfigurationTypeDef",
    "MappedDataSetParameterTypeDef",
    "SheetControlInfoIconLabelOptionsTypeDef",
    "DecimalDatasetParameterDefaultValuesTypeDef",
    "DecimalValueWhenUnsetConfigurationTypeDef",
    "DecimalParameterTypeDef",
    "DeleteAccountCustomizationRequestRequestTypeDef",
    "DeleteAccountSubscriptionRequestRequestTypeDef",
    "DeleteAnalysisRequestRequestTypeDef",
    "DeleteDashboardRequestRequestTypeDef",
    "DeleteDataSetRefreshPropertiesRequestRequestTypeDef",
    "DeleteDataSetRequestRequestTypeDef",
    "DeleteDataSourceRequestRequestTypeDef",
    "DeleteFolderMembershipRequestRequestTypeDef",
    "DeleteFolderRequestRequestTypeDef",
    "DeleteGroupMembershipRequestRequestTypeDef",
    "DeleteGroupRequestRequestTypeDef",
    "DeleteIAMPolicyAssignmentRequestRequestTypeDef",
    "DeleteNamespaceRequestRequestTypeDef",
    "DeleteRefreshScheduleRequestRequestTypeDef",
    "DeleteTemplateAliasRequestRequestTypeDef",
    "DeleteTemplateRequestRequestTypeDef",
    "DeleteThemeAliasRequestRequestTypeDef",
    "DeleteThemeRequestRequestTypeDef",
    "DeleteTopicRefreshScheduleRequestRequestTypeDef",
    "DeleteTopicRequestRequestTypeDef",
    "DeleteUserByPrincipalIdRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DeleteVPCConnectionRequestRequestTypeDef",
    "DescribeAccountCustomizationRequestRequestTypeDef",
    "DescribeAccountSettingsRequestRequestTypeDef",
    "DescribeAccountSubscriptionRequestRequestTypeDef",
    "DescribeAnalysisDefinitionRequestRequestTypeDef",
    "DescribeAnalysisPermissionsRequestRequestTypeDef",
    "DescribeAnalysisRequestRequestTypeDef",
    "DescribeAssetBundleExportJobRequestRequestTypeDef",
    "DescribeAssetBundleImportJobRequestRequestTypeDef",
    "DescribeDashboardDefinitionRequestRequestTypeDef",
    "DescribeDashboardPermissionsRequestRequestTypeDef",
    "DescribeDashboardRequestRequestTypeDef",
    "DescribeDashboardSnapshotJobRequestRequestTypeDef",
    "DescribeDashboardSnapshotJobResultRequestRequestTypeDef",
    "SnapshotJobErrorInfoTypeDef",
    "DescribeDataSetPermissionsRequestRequestTypeDef",
    "DescribeDataSetRefreshPropertiesRequestRequestTypeDef",
    "DescribeDataSetRequestRequestTypeDef",
    "DescribeDataSourcePermissionsRequestRequestTypeDef",
    "DescribeDataSourceRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeFolderPermissionsRequestRequestTypeDef",
    "ResourcePermissionPaginatorTypeDef",
    "DescribeFolderRequestRequestTypeDef",
    "DescribeFolderResolvedPermissionsRequestRequestTypeDef",
    "FolderTypeDef",
    "DescribeGroupMembershipRequestRequestTypeDef",
    "DescribeGroupRequestRequestTypeDef",
    "DescribeIAMPolicyAssignmentRequestRequestTypeDef",
    "IAMPolicyAssignmentTypeDef",
    "DescribeIngestionRequestRequestTypeDef",
    "DescribeIpRestrictionRequestRequestTypeDef",
    "DescribeNamespaceRequestRequestTypeDef",
    "DescribeRefreshScheduleRequestRequestTypeDef",
    "DescribeTemplateAliasRequestRequestTypeDef",
    "DescribeTemplateDefinitionRequestRequestTypeDef",
    "DescribeTemplatePermissionsRequestRequestTypeDef",
    "DescribeTemplateRequestRequestTypeDef",
    "DescribeThemeAliasRequestRequestTypeDef",
    "DescribeThemePermissionsRequestRequestTypeDef",
    "DescribeThemeRequestRequestTypeDef",
    "DescribeTopicPermissionsRequestRequestTypeDef",
    "DescribeTopicRefreshRequestRequestTypeDef",
    "TopicRefreshDetailsTypeDef",
    "DescribeTopicRefreshScheduleRequestRequestTypeDef",
    "DescribeTopicRequestRequestTypeDef",
    "DescribeUserRequestRequestTypeDef",
    "UserTypeDef",
    "DescribeVPCConnectionRequestRequestTypeDef",
    "NegativeFormatTypeDef",
    "DonutCenterOptionsTypeDef",
    "ListControlSelectAllOptionsTypeDef",
    "ErrorInfoTypeDef",
    "ExcludePeriodConfigurationTypeDef",
    "FieldSortTypeDef",
    "FieldTooltipItemTypeDef",
    "GeospatialMapStyleOptionsTypeDef",
    "FilterSelectableValuesTypeDef",
    "SameSheetTargetVisualConfigurationTypeDef",
    "FilterOperationTypeDef",
    "FolderSearchFilterTypeDef",
    "FolderSummaryTypeDef",
    "FontSizeTypeDef",
    "FontWeightTypeDef",
    "FontTypeDef",
    "TimeBasedForecastPropertiesTypeDef",
    "FreeFormLayoutScreenCanvasSizeOptionsTypeDef",
    "FreeFormLayoutElementBackgroundStyleTypeDef",
    "FreeFormLayoutElementBorderStyleTypeDef",
    "LoadingAnimationTypeDef",
    "SessionTagTypeDef",
    "GeospatialCoordinateBoundsTypeDef",
    "GeospatialHeatmapDataColorTypeDef",
    "GetDashboardEmbedUrlRequestRequestTypeDef",
    "GetSessionEmbedUrlRequestRequestTypeDef",
    "TableBorderOptionsTypeDef",
    "GradientStopTypeDef",
    "GridLayoutScreenCanvasSizeOptionsTypeDef",
    "GridLayoutElementTypeDef",
    "GroupSearchFilterTypeDef",
    "GutterStyleTypeDef",
    "IAMPolicyAssignmentSummaryTypeDef",
    "LookbackWindowTypeDef",
    "QueueInfoTypeDef",
    "RowInfoTypeDef",
    "IntegerDatasetParameterDefaultValuesTypeDef",
    "IntegerValueWhenUnsetConfigurationTypeDef",
    "IntegerParameterTypeDef",
    "JoinKeyPropertiesTypeDef",
    "KPISparklineOptionsTypeDef",
    "ProgressBarOptionsTypeDef",
    "SecondaryValueOptionsTypeDef",
    "TrendArrowOptionsTypeDef",
    "KPIVisualStandardLayoutTypeDef",
    "LineChartLineStyleSettingsTypeDef",
    "LineChartMarkerStyleSettingsTypeDef",
    "MissingDataConfigurationTypeDef",
    "ListAnalysesRequestRequestTypeDef",
    "ListAssetBundleExportJobsRequestRequestTypeDef",
    "ListAssetBundleImportJobsRequestRequestTypeDef",
    "ListControlSearchOptionsTypeDef",
    "ListDashboardVersionsRequestRequestTypeDef",
    "ListDashboardsRequestRequestTypeDef",
    "ListDataSetsRequestRequestTypeDef",
    "ListDataSourcesRequestRequestTypeDef",
    "ListFolderMembersRequestRequestTypeDef",
    "MemberIdArnPairTypeDef",
    "ListFoldersRequestRequestTypeDef",
    "ListGroupMembershipsRequestRequestTypeDef",
    "ListGroupsRequestRequestTypeDef",
    "ListIAMPolicyAssignmentsForUserRequestRequestTypeDef",
    "ListIAMPolicyAssignmentsRequestRequestTypeDef",
    "ListIngestionsRequestRequestTypeDef",
    "ListNamespacesRequestRequestTypeDef",
    "ListRefreshSchedulesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTemplateAliasesRequestRequestTypeDef",
    "ListTemplateVersionsRequestRequestTypeDef",
    "TemplateVersionSummaryTypeDef",
    "ListTemplatesRequestRequestTypeDef",
    "TemplateSummaryTypeDef",
    "ListThemeAliasesRequestRequestTypeDef",
    "ListThemeVersionsRequestRequestTypeDef",
    "ThemeVersionSummaryTypeDef",
    "ListThemesRequestRequestTypeDef",
    "ThemeSummaryTypeDef",
    "ListTopicRefreshSchedulesRequestRequestTypeDef",
    "ListTopicsRequestRequestTypeDef",
    "TopicSummaryTypeDef",
    "ListUserGroupsRequestRequestTypeDef",
    "ListUsersRequestRequestTypeDef",
    "ListVPCConnectionsRequestRequestTypeDef",
    "LongFormatTextTypeDef",
    "ManifestFileLocationTypeDef",
    "MarginStyleTypeDef",
    "NamedEntityDefinitionMetricTypeDef",
    "NamespaceErrorTypeDef",
    "NetworkInterfaceTypeDef",
    "NumericRangeFilterValueTypeDef",
    "ThousandSeparatorOptionsTypeDef",
    "PercentileAggregationTypeDef",
    "StringParameterTypeDef",
    "PercentVisibleRangeTypeDef",
    "PivotTableConditionalFormattingScopeTypeDef",
    "PivotTablePaginatedReportOptionsTypeDef",
    "PivotTableFieldOptionTypeDef",
    "PivotTableFieldSubtotalOptionsTypeDef",
    "PivotTableRowsLabelOptionsTypeDef",
    "RowAlternateColorOptionsTypeDef",
    "ProjectOperationTypeDef",
    "RadarChartAreaStyleSettingsTypeDef",
    "RangeConstantTypeDef",
    "RedshiftIAMParametersPaginatorTypeDef",
    "RedshiftIAMParametersTypeDef",
    "ReferenceLineCustomLabelConfigurationTypeDef",
    "ReferenceLineStaticDataConfigurationTypeDef",
    "ReferenceLineStyleConfigurationTypeDef",
    "ScheduleRefreshOnEntityTypeDef",
    "StatePersistenceConfigurationsTypeDef",
    "RegisteredUserQSearchBarEmbeddingConfigurationTypeDef",
    "RenameColumnOperationTypeDef",
    "RestoreAnalysisRequestRequestTypeDef",
    "RowLevelPermissionTagRuleTypeDef",
    "S3BucketConfigurationTypeDef",
    "UploadSettingsTypeDef",
    "SectionAfterPageBreakTypeDef",
    "SpacingTypeDef",
    "SheetVisualScopingConfigurationTypeDef",
    "SemanticEntityTypeTypeDef",
    "SemanticTypeTypeDef",
    "SheetTextBoxTypeDef",
    "SheetElementConfigurationOverridesTypeDef",
    "ShortFormatTextTypeDef",
    "SmallMultiplesAxisPropertiesTypeDef",
    "SnapshotAnonymousUserRedactedTypeDef",
    "SnapshotFileSheetSelectionTypeDef",
    "SnapshotJobResultErrorInfoTypeDef",
    "StringDatasetParameterDefaultValuesTypeDef",
    "StringValueWhenUnsetConfigurationTypeDef",
    "TableStyleTargetTypeDef",
    "TableCellImageSizingConfigurationTypeDef",
    "TablePaginatedReportOptionsTypeDef",
    "TableFieldCustomIconContentTypeDef",
    "TablePinnedFieldOptionsTypeDef",
    "TemplateSourceTemplateTypeDef",
    "TextControlPlaceholderOptionsTypeDef",
    "UIColorPaletteTypeDef",
    "ThemeErrorTypeDef",
    "TopicSingularFilterConstantTypeDef",
    "UntagColumnOperationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAccountSettingsRequestRequestTypeDef",
    "UpdateDashboardPublishedVersionRequestRequestTypeDef",
    "UpdateFolderRequestRequestTypeDef",
    "UpdateGroupRequestRequestTypeDef",
    "UpdateIAMPolicyAssignmentRequestRequestTypeDef",
    "UpdateIpRestrictionRequestRequestTypeDef",
    "UpdatePublicSharingSettingsRequestRequestTypeDef",
    "UpdateTemplateAliasRequestRequestTypeDef",
    "UpdateThemeAliasRequestRequestTypeDef",
    "UpdateUserRequestRequestTypeDef",
    "UpdateVPCConnectionRequestRequestTypeDef",
    "WaterfallChartOptionsTypeDef",
    "WordCloudOptionsTypeDef",
    "UpdateAccountCustomizationRequestRequestTypeDef",
    "AxisLabelReferenceOptionsTypeDef",
    "CascadingControlSourceTypeDef",
    "CategoryDrillDownFilterTypeDef",
    "ContributionAnalysisDefaultTypeDef",
    "DynamicDefaultValueTypeDef",
    "FilterOperationSelectedFieldsConfigurationTypeDef",
    "NumericEqualityDrillDownFilterTypeDef",
    "ParameterSelectableValuesTypeDef",
    "AnalysisErrorTypeDef",
    "DashboardErrorTypeDef",
    "TemplateErrorTypeDef",
    "SearchAnalysesRequestRequestTypeDef",
    "AnalysisSourceTemplateTypeDef",
    "DashboardSourceTemplateTypeDef",
    "TemplateSourceAnalysisTypeDef",
    "AnonymousUserDashboardVisualEmbeddingConfigurationTypeDef",
    "RegisteredUserDashboardVisualEmbeddingConfigurationTypeDef",
    "ArcAxisConfigurationTypeDef",
    "AssetBundleCloudFormationOverridePropertyConfigurationTypeDef",
    "AssetBundleImportJobDataSourceCredentialsTypeDef",
    "AssetBundleImportSourceTypeDef",
    "AxisDisplayRangeTypeDef",
    "AxisScaleTypeDef",
    "HistogramBinOptionsTypeDef",
    "TileStyleTypeDef",
    "BoxPlotOptionsTypeDef",
    "CreateColumnsOperationTypeDef",
    "CancelIngestionResponseTypeDef",
    "CreateAccountCustomizationResponseTypeDef",
    "CreateAnalysisResponseTypeDef",
    "CreateDashboardResponseTypeDef",
    "CreateDataSetResponseTypeDef",
    "CreateDataSourceResponseTypeDef",
    "CreateFolderResponseTypeDef",
    "CreateIAMPolicyAssignmentResponseTypeDef",
    "CreateIngestionResponseTypeDef",
    "CreateNamespaceResponseTypeDef",
    "CreateRefreshScheduleResponseTypeDef",
    "CreateTemplateResponseTypeDef",
    "CreateThemeResponseTypeDef",
    "CreateTopicRefreshScheduleResponseTypeDef",
    "CreateTopicResponseTypeDef",
    "CreateVPCConnectionResponseTypeDef",
    "DeleteAccountCustomizationResponseTypeDef",
    "DeleteAccountSubscriptionResponseTypeDef",
    "DeleteAnalysisResponseTypeDef",
    "DeleteDashboardResponseTypeDef",
    "DeleteDataSetRefreshPropertiesResponseTypeDef",
    "DeleteDataSetResponseTypeDef",
    "DeleteDataSourceResponseTypeDef",
    "DeleteFolderMembershipResponseTypeDef",
    "DeleteFolderResponseTypeDef",
    "DeleteGroupMembershipResponseTypeDef",
    "DeleteGroupResponseTypeDef",
    "DeleteIAMPolicyAssignmentResponseTypeDef",
    "DeleteNamespaceResponseTypeDef",
    "DeleteRefreshScheduleResponseTypeDef",
    "DeleteTemplateAliasResponseTypeDef",
    "DeleteTemplateResponseTypeDef",
    "DeleteThemeAliasResponseTypeDef",
    "DeleteThemeResponseTypeDef",
    "DeleteTopicRefreshScheduleResponseTypeDef",
    "DeleteTopicResponseTypeDef",
    "DeleteUserByPrincipalIdResponseTypeDef",
    "DeleteUserResponseTypeDef",
    "DeleteVPCConnectionResponseTypeDef",
    "DescribeAccountCustomizationResponseTypeDef",
    "DescribeAccountSettingsResponseTypeDef",
    "DescribeAccountSubscriptionResponseTypeDef",
    "DescribeIpRestrictionResponseTypeDef",
    "GenerateEmbedUrlForAnonymousUserResponseTypeDef",
    "GenerateEmbedUrlForRegisteredUserResponseTypeDef",
    "GetDashboardEmbedUrlResponseTypeDef",
    "GetSessionEmbedUrlResponseTypeDef",
    "ListAnalysesResponseTypeDef",
    "ListAssetBundleExportJobsResponseTypeDef",
    "ListAssetBundleImportJobsResponseTypeDef",
    "ListIAMPolicyAssignmentsForUserResponseTypeDef",
    "PutDataSetRefreshPropertiesResponseTypeDef",
    "RestoreAnalysisResponseTypeDef",
    "SearchAnalysesResponseTypeDef",
    "StartAssetBundleExportJobResponseTypeDef",
    "StartAssetBundleImportJobResponseTypeDef",
    "StartDashboardSnapshotJobResponseTypeDef",
    "TagResourceResponseTypeDef",
    "UntagResourceResponseTypeDef",
    "UpdateAccountCustomizationResponseTypeDef",
    "UpdateAccountSettingsResponseTypeDef",
    "UpdateAnalysisResponseTypeDef",
    "UpdateDashboardPublishedVersionResponseTypeDef",
    "UpdateDashboardResponseTypeDef",
    "UpdateDataSetPermissionsResponseTypeDef",
    "UpdateDataSetResponseTypeDef",
    "UpdateDataSourcePermissionsResponseTypeDef",
    "UpdateDataSourceResponseTypeDef",
    "UpdateFolderResponseTypeDef",
    "UpdateIAMPolicyAssignmentResponseTypeDef",
    "UpdateIpRestrictionResponseTypeDef",
    "UpdatePublicSharingSettingsResponseTypeDef",
    "UpdateRefreshScheduleResponseTypeDef",
    "UpdateTemplateResponseTypeDef",
    "UpdateThemeResponseTypeDef",
    "UpdateTopicRefreshScheduleResponseTypeDef",
    "UpdateTopicResponseTypeDef",
    "UpdateVPCConnectionResponseTypeDef",
    "CategoryFilterConfigurationTypeDef",
    "ClusterMarkerTypeDef",
    "TopicCategoryFilterConstantTypeDef",
    "ColorScaleTypeDef",
    "ColorsConfigurationTypeDef",
    "ColumnTagTypeDef",
    "ColumnGroupSchemaTypeDef",
    "ColumnGroupTypeDef",
    "DataSetSchemaTypeDef",
    "ConditionalFormattingCustomIconConditionTypeDef",
    "CreateAccountCustomizationRequestRequestTypeDef",
    "CreateNamespaceRequestRequestTypeDef",
    "CreateVPCConnectionRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "RegisterUserRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateAccountSubscriptionResponseTypeDef",
    "CreateFolderRequestRequestTypeDef",
    "DescribeAnalysisPermissionsResponseTypeDef",
    "DescribeDataSetPermissionsResponseTypeDef",
    "DescribeDataSourcePermissionsResponseTypeDef",
    "DescribeFolderPermissionsResponseTypeDef",
    "DescribeFolderResolvedPermissionsResponseTypeDef",
    "DescribeTemplatePermissionsResponseTypeDef",
    "DescribeThemePermissionsResponseTypeDef",
    "DescribeTopicPermissionsResponseTypeDef",
    "LinkSharingConfigurationTypeDef",
    "UpdateAnalysisPermissionsRequestRequestTypeDef",
    "UpdateAnalysisPermissionsResponseTypeDef",
    "UpdateDashboardPermissionsRequestRequestTypeDef",
    "UpdateDataSetPermissionsRequestRequestTypeDef",
    "UpdateDataSourcePermissionsRequestRequestTypeDef",
    "UpdateFolderPermissionsRequestRequestTypeDef",
    "UpdateFolderPermissionsResponseTypeDef",
    "UpdateTemplatePermissionsRequestRequestTypeDef",
    "UpdateTemplatePermissionsResponseTypeDef",
    "UpdateThemePermissionsRequestRequestTypeDef",
    "UpdateThemePermissionsResponseTypeDef",
    "UpdateTopicPermissionsRequestRequestTypeDef",
    "UpdateTopicPermissionsResponseTypeDef",
    "DataSetSummaryTypeDef",
    "CreateFolderMembershipResponseTypeDef",
    "CreateGroupMembershipResponseTypeDef",
    "DescribeGroupMembershipResponseTypeDef",
    "ListGroupMembershipsResponseTypeDef",
    "CreateGroupResponseTypeDef",
    "DescribeGroupResponseTypeDef",
    "ListGroupsResponseTypeDef",
    "ListUserGroupsResponseTypeDef",
    "SearchGroupsResponseTypeDef",
    "UpdateGroupResponseTypeDef",
    "CreateTemplateAliasResponseTypeDef",
    "DescribeTemplateAliasResponseTypeDef",
    "ListTemplateAliasesResponseTypeDef",
    "UpdateTemplateAliasResponseTypeDef",
    "CreateThemeAliasResponseTypeDef",
    "DescribeThemeAliasResponseTypeDef",
    "ListThemeAliasesResponseTypeDef",
    "UpdateThemeAliasResponseTypeDef",
    "CustomActionNavigationOperationTypeDef",
    "CustomParameterValuesTypeDef",
    "DateTimeDatasetParameterDefaultValuesTypeDef",
    "DateTimeParameterTypeDef",
    "DateTimeValueWhenUnsetConfigurationTypeDef",
    "NewDefaultValuesTypeDef",
    "TimeEqualityFilterTypeDef",
    "TimeRangeDrillDownFilterTypeDef",
    "TopicRefreshScheduleTypeDef",
    "WhatIfPointScenarioTypeDef",
    "WhatIfRangeScenarioTypeDef",
    "CustomSqlTypeDef",
    "RelationalTableTypeDef",
    "SearchDashboardsRequestRequestTypeDef",
    "ListDashboardsResponseTypeDef",
    "SearchDashboardsResponseTypeDef",
    "ListDashboardVersionsResponseTypeDef",
    "DashboardVisualPublishOptionsTypeDef",
    "TableInlineVisualizationTypeDef",
    "DataLabelTypeTypeDef",
    "DataPathColorTypeDef",
    "DataPathSortTypeDef",
    "PivotTableDataPathOptionTypeDef",
    "PivotTableFieldCollapseStateTargetTypeDef",
    "SearchDataSetsRequestRequestTypeDef",
    "SearchDataSourcesRequestRequestTypeDef",
    "SearchDataSourcesResponseTypeDef",
    "TimeRangeFilterValueTypeDef",
    "DecimalDatasetParameterTypeDef",
    "DescribeFolderPermissionsRequestDescribeFolderPermissionsPaginateTypeDef",
    "DescribeFolderResolvedPermissionsRequestDescribeFolderResolvedPermissionsPaginateTypeDef",
    "ListAnalysesRequestListAnalysesPaginateTypeDef",
    "ListAssetBundleExportJobsRequestListAssetBundleExportJobsPaginateTypeDef",
    "ListAssetBundleImportJobsRequestListAssetBundleImportJobsPaginateTypeDef",
    "ListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef",
    "ListDashboardsRequestListDashboardsPaginateTypeDef",
    "ListDataSetsRequestListDataSetsPaginateTypeDef",
    "ListDataSourcesRequestListDataSourcesPaginateTypeDef",
    "ListFolderMembersRequestListFolderMembersPaginateTypeDef",
    "ListFoldersRequestListFoldersPaginateTypeDef",
    "ListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef",
    "ListGroupsRequestListGroupsPaginateTypeDef",
    "ListIAMPolicyAssignmentsForUserRequestListIAMPolicyAssignmentsForUserPaginateTypeDef",
    "ListIAMPolicyAssignmentsRequestListIAMPolicyAssignmentsPaginateTypeDef",
    "ListIngestionsRequestListIngestionsPaginateTypeDef",
    "ListNamespacesRequestListNamespacesPaginateTypeDef",
    "ListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef",
    "ListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef",
    "ListTemplatesRequestListTemplatesPaginateTypeDef",
    "ListThemeVersionsRequestListThemeVersionsPaginateTypeDef",
    "ListThemesRequestListThemesPaginateTypeDef",
    "ListUserGroupsRequestListUserGroupsPaginateTypeDef",
    "ListUsersRequestListUsersPaginateTypeDef",
    "SearchAnalysesRequestSearchAnalysesPaginateTypeDef",
    "SearchDashboardsRequestSearchDashboardsPaginateTypeDef",
    "SearchDataSetsRequestSearchDataSetsPaginateTypeDef",
    "SearchDataSourcesRequestSearchDataSourcesPaginateTypeDef",
    "DescribeFolderPermissionsResponsePaginatorTypeDef",
    "DescribeFolderResolvedPermissionsResponsePaginatorTypeDef",
    "DescribeFolderResponseTypeDef",
    "DescribeIAMPolicyAssignmentResponseTypeDef",
    "DescribeTopicRefreshResponseTypeDef",
    "DescribeUserResponseTypeDef",
    "ListUsersResponseTypeDef",
    "RegisterUserResponseTypeDef",
    "UpdateUserResponseTypeDef",
    "DisplayFormatOptionsTypeDef",
    "DonutOptionsTypeDef",
    "RelativeDatesFilterTypeDef",
    "FilterOperationTargetVisualsConfigurationTypeDef",
    "SearchFoldersRequestRequestTypeDef",
    "SearchFoldersRequestSearchFoldersPaginateTypeDef",
    "ListFoldersResponseTypeDef",
    "SearchFoldersResponseTypeDef",
    "FontConfigurationTypeDef",
    "TypographyTypeDef",
    "FreeFormLayoutCanvasSizeOptionsTypeDef",
    "SnapshotAnonymousUserTypeDef",
    "GeospatialWindowOptionsTypeDef",
    "GeospatialHeatmapColorScaleTypeDef",
    "TableSideBorderOptionsTypeDef",
    "GradientColorTypeDef",
    "GridLayoutCanvasSizeOptionsTypeDef",
    "SearchGroupsRequestRequestTypeDef",
    "SearchGroupsRequestSearchGroupsPaginateTypeDef",
    "ListIAMPolicyAssignmentsResponseTypeDef",
    "IncrementalRefreshTypeDef",
    "IngestionTypeDef",
    "IntegerDatasetParameterTypeDef",
    "JoinInstructionTypeDef",
    "KPIVisualLayoutOptionsTypeDef",
    "LineChartDefaultSeriesSettingsTypeDef",
    "LineChartSeriesSettingsTypeDef",
    "ListFolderMembersResponseTypeDef",
    "ListTemplateVersionsResponseTypeDef",
    "ListTemplatesResponseTypeDef",
    "ListThemeVersionsResponseTypeDef",
    "ListThemesResponseTypeDef",
    "ListTopicsResponseTypeDef",
    "VisualSubtitleLabelOptionsTypeDef",
    "S3ParametersTypeDef",
    "TileLayoutStyleTypeDef",
    "NamedEntityDefinitionTypeDef",
    "NamespaceInfoV2TypeDef",
    "VPCConnectionSummaryTypeDef",
    "VPCConnectionTypeDef",
    "NumericSeparatorConfigurationTypeDef",
    "NumericalAggregationFunctionTypeDef",
    "VisibleRangeOptionsTypeDef",
    "RadarChartSeriesSettingsTypeDef",
    "TopicRangeFilterConstantTypeDef",
    "RedshiftParametersPaginatorTypeDef",
    "RedshiftParametersTypeDef",
    "RefreshFrequencyTypeDef",
    "RegisteredUserConsoleFeatureConfigurationsTypeDef",
    "RegisteredUserDashboardFeatureConfigurationsTypeDef",
    "RowLevelPermissionTagConfigurationTypeDef",
    "SnapshotS3DestinationConfigurationTypeDef",
    "S3SourceTypeDef",
    "SectionPageBreakConfigurationTypeDef",
    "SectionBasedLayoutPaperCanvasSizeOptionsTypeDef",
    "SectionStyleTypeDef",
    "SelectedSheetsFilterScopeConfigurationTypeDef",
    "SheetElementRenderingRuleTypeDef",
    "VisualTitleLabelOptionsTypeDef",
    "SnapshotUserConfigurationRedactedTypeDef",
    "SnapshotFileTypeDef",
    "StringDatasetParameterTypeDef",
    "TableFieldImageConfigurationTypeDef",
    "TopicNumericEqualityFilterTypeDef",
    "TopicRelativeDateFilterTypeDef",
    "CascadingControlConfigurationTypeDef",
    "DateTimeDefaultValuesTypeDef",
    "DecimalDefaultValuesTypeDef",
    "IntegerDefaultValuesTypeDef",
    "StringDefaultValuesTypeDef",
    "AnalysisTypeDef",
    "DashboardVersionTypeDef",
    "AnalysisSourceEntityTypeDef",
    "DashboardSourceEntityTypeDef",
    "TemplateSourceEntityTypeDef",
    "AnonymousUserEmbeddingExperienceConfigurationTypeDef",
    "DescribeAssetBundleExportJobResponseTypeDef",
    "StartAssetBundleExportJobRequestRequestTypeDef",
    "NumericAxisOptionsTypeDef",
    "CategoryFilterTypeDef",
    "ClusterMarkerConfigurationTypeDef",
    "TopicCategoryFilterTypeDef",
    "TagColumnOperationTypeDef",
    "DataSetConfigurationTypeDef",
    "ConditionalFormattingIconTypeDef",
    "DescribeDashboardPermissionsResponseTypeDef",
    "UpdateDashboardPermissionsResponseTypeDef",
    "ListDataSetsResponseTypeDef",
    "SearchDataSetsResponseTypeDef",
    "CustomValuesConfigurationTypeDef",
    "DateTimeDatasetParameterTypeDef",
    "ParametersTypeDef",
    "OverrideDatasetParameterOperationTypeDef",
    "DrillDownFilterTypeDef",
    "CreateTopicRefreshScheduleRequestRequestTypeDef",
    "DescribeTopicRefreshScheduleResponseTypeDef",
    "TopicRefreshScheduleSummaryTypeDef",
    "UpdateTopicRefreshScheduleRequestRequestTypeDef",
    "ForecastScenarioTypeDef",
    "DashboardPublishOptionsTypeDef",
    "VisualPaletteTypeDef",
    "PivotTableFieldCollapseStateOptionTypeDef",
    "TimeRangeFilterTypeDef",
    "DefaultFormattingTypeDef",
    "CustomActionFilterOperationTypeDef",
    "AxisLabelOptionsTypeDef",
    "DataLabelOptionsTypeDef",
    "FunnelChartDataLabelOptionsTypeDef",
    "LabelOptionsTypeDef",
    "PanelTitleOptionsTypeDef",
    "TableFieldCustomTextContentTypeDef",
    "DefaultFreeFormLayoutConfigurationTypeDef",
    "SnapshotUserConfigurationTypeDef",
    "GeospatialHeatmapConfigurationTypeDef",
    "GlobalTableBorderOptionsTypeDef",
    "ConditionalFormattingGradientColorTypeDef",
    "DefaultGridLayoutConfigurationTypeDef",
    "GridLayoutConfigurationTypeDef",
    "RefreshConfigurationTypeDef",
    "DescribeIngestionResponseTypeDef",
    "ListIngestionsResponseTypeDef",
    "LogicalTableSourceTypeDef",
    "DataFieldSeriesItemTypeDef",
    "FieldSeriesItemTypeDef",
    "SheetStyleTypeDef",
    "TopicNamedEntityTypeDef",
    "DescribeNamespaceResponseTypeDef",
    "ListNamespacesResponseTypeDef",
    "ListVPCConnectionsResponseTypeDef",
    "DescribeVPCConnectionResponseTypeDef",
    "CurrencyDisplayFormatConfigurationTypeDef",
    "NumberDisplayFormatConfigurationTypeDef",
    "PercentageDisplayFormatConfigurationTypeDef",
    "AggregationFunctionTypeDef",
    "ScrollBarOptionsTypeDef",
    "TopicDateRangeFilterTypeDef",
    "TopicNumericRangeFilterTypeDef",
    "DataSourceParametersPaginatorTypeDef",
    "DataSourceParametersTypeDef",
    "RefreshScheduleTypeDef",
    "RegisteredUserQuickSightConsoleEmbeddingConfigurationTypeDef",
    "RegisteredUserDashboardEmbeddingConfigurationTypeDef",
    "SnapshotDestinationConfigurationTypeDef",
    "SnapshotJobS3ResultTypeDef",
    "PhysicalTableTypeDef",
    "SectionBasedLayoutCanvasSizeOptionsTypeDef",
    "FilterScopeConfigurationTypeDef",
    "FreeFormLayoutElementTypeDef",
    "SnapshotFileGroupTypeDef",
    "DateTimeParameterDeclarationTypeDef",
    "DecimalParameterDeclarationTypeDef",
    "IntegerParameterDeclarationTypeDef",
    "StringParameterDeclarationTypeDef",
    "DescribeAnalysisResponseTypeDef",
    "DashboardTypeDef",
    "GenerateEmbedUrlForAnonymousUserRequestRequestTypeDef",
    "AxisDataOptionsTypeDef",
    "TemplateVersionTypeDef",
    "DestinationParameterValueConfigurationTypeDef",
    "DatasetParameterTypeDef",
    "TransformOperationTypeDef",
    "DateTimeHierarchyTypeDef",
    "ExplicitHierarchyTypeDef",
    "PredefinedHierarchyTypeDef",
    "ListTopicRefreshSchedulesResponseTypeDef",
    "ForecastConfigurationTypeDef",
    "PivotTableFieldOptionsTypeDef",
    "TopicCalculatedFieldTypeDef",
    "TopicColumnTypeDef",
    "ChartAxisLabelOptionsTypeDef",
    "AxisTickLabelOptionsTypeDef",
    "DateTimePickerControlDisplayOptionsTypeDef",
    "DropDownControlDisplayOptionsTypeDef",
    "LegendOptionsTypeDef",
    "ListControlDisplayOptionsTypeDef",
    "RelativeDateTimeControlDisplayOptionsTypeDef",
    "SliderControlDisplayOptionsTypeDef",
    "TextAreaControlDisplayOptionsTypeDef",
    "TextFieldControlDisplayOptionsTypeDef",
    "PanelConfigurationTypeDef",
    "TableFieldLinkContentConfigurationTypeDef",
    "GeospatialPointStyleOptionsTypeDef",
    "TableCellStyleTypeDef",
    "ConditionalFormattingColorTypeDef",
    "DefaultInteractiveLayoutConfigurationTypeDef",
    "SheetControlLayoutConfigurationTypeDef",
    "DataSetRefreshPropertiesTypeDef",
    "SeriesItemTypeDef",
    "ThemeConfigurationTypeDef",
    "ComparisonFormatConfigurationTypeDef",
    "NumericFormatConfigurationTypeDef",
    "AggregationSortConfigurationTypeDef",
    "ColumnSortTypeDef",
    "ColumnTooltipItemTypeDef",
    "NumericEqualityFilterTypeDef",
    "NumericRangeFilterTypeDef",
    "ReferenceLineDynamicDataConfigurationTypeDef",
    "TopicFilterTypeDef",
    "DataSourcePaginatorTypeDef",
    "AssetBundleImportJobDataSourceOverrideParametersTypeDef",
    "CredentialPairTypeDef",
    "DataSourceTypeDef",
    "CreateRefreshScheduleRequestRequestTypeDef",
    "DescribeRefreshScheduleResponseTypeDef",
    "ListRefreshSchedulesResponseTypeDef",
    "UpdateRefreshScheduleRequestRequestTypeDef",
    "RegisteredUserEmbeddingExperienceConfigurationTypeDef",
    "SnapshotJobResultFileGroupTypeDef",
    "DefaultSectionBasedLayoutConfigurationTypeDef",
    "FreeFormLayoutConfigurationTypeDef",
    "FreeFormSectionLayoutConfigurationTypeDef",
    "SnapshotConfigurationTypeDef",
    "ParameterDeclarationTypeDef",
    "DescribeDashboardResponseTypeDef",
    "TemplateTypeDef",
    "SetParameterValueConfigurationTypeDef",
    "LogicalTableTypeDef",
    "ColumnHierarchyTypeDef",
    "AxisDisplayOptionsTypeDef",
    "FilterDateTimePickerControlTypeDef",
    "ParameterDateTimePickerControlTypeDef",
    "FilterDropDownControlTypeDef",
    "ParameterDropDownControlTypeDef",
    "FilterListControlTypeDef",
    "ParameterListControlTypeDef",
    "FilterRelativeDateTimeControlTypeDef",
    "FilterSliderControlTypeDef",
    "ParameterSliderControlTypeDef",
    "FilterTextAreaControlTypeDef",
    "ParameterTextAreaControlTypeDef",
    "FilterTextFieldControlTypeDef",
    "ParameterTextFieldControlTypeDef",
    "SmallMultiplesOptionsTypeDef",
    "TableFieldLinkConfigurationTypeDef",
    "PivotTableOptionsTypeDef",
    "PivotTotalOptionsTypeDef",
    "SubtotalOptionsTypeDef",
    "TableOptionsTypeDef",
    "TotalOptionsTypeDef",
    "GaugeChartArcConditionalFormattingTypeDef",
    "GaugeChartPrimaryValueConditionalFormattingTypeDef",
    "KPIActualValueConditionalFormattingTypeDef",
    "KPIComparisonValueConditionalFormattingTypeDef",
    "KPIPrimaryValueConditionalFormattingTypeDef",
    "KPIProgressBarConditionalFormattingTypeDef",
    "ShapeConditionalFormatTypeDef",
    "TableRowConditionalFormattingTypeDef",
    "TextConditionalFormatTypeDef",
    "SheetControlLayoutTypeDef",
    "DescribeDataSetRefreshPropertiesResponseTypeDef",
    "PutDataSetRefreshPropertiesRequestRequestTypeDef",
    "CreateThemeRequestRequestTypeDef",
    "ThemeVersionTypeDef",
    "UpdateThemeRequestRequestTypeDef",
    "ComparisonConfigurationTypeDef",
    "DateTimeFormatConfigurationTypeDef",
    "NumberFormatConfigurationTypeDef",
    "ReferenceLineValueLabelConfigurationTypeDef",
    "StringFormatConfigurationTypeDef",
    "TopBottomFilterTypeDef",
    "FieldSortOptionsTypeDef",
    "PivotTableSortByTypeDef",
    "TooltipItemTypeDef",
    "ReferenceLineDataConfigurationTypeDef",
    "DatasetMetadataTypeDef",
    "ListDataSourcesResponsePaginatorTypeDef",
    "AssetBundleImportJobOverrideParametersTypeDef",
    "DataSourceCredentialsTypeDef",
    "DescribeDataSourceResponseTypeDef",
    "ListDataSourcesResponseTypeDef",
    "GenerateEmbedUrlForRegisteredUserRequestRequestTypeDef",
    "AnonymousUserSnapshotJobResultTypeDef",
    "DefaultPaginatedLayoutConfigurationTypeDef",
    "SectionLayoutConfigurationTypeDef",
    "DescribeDashboardSnapshotJobResponseTypeDef",
    "StartDashboardSnapshotJobRequestRequestTypeDef",
    "DescribeTemplateResponseTypeDef",
    "CustomActionSetParametersOperationTypeDef",
    "CreateDataSetRequestRequestTypeDef",
    "DataSetTypeDef",
    "UpdateDataSetRequestRequestTypeDef",
    "LineSeriesAxisDisplayOptionsTypeDef",
    "FilterControlTypeDef",
    "ParameterControlTypeDef",
    "TableFieldURLConfigurationTypeDef",
    "PivotTableTotalOptionsTypeDef",
    "GaugeChartConditionalFormattingOptionTypeDef",
    "KPIConditionalFormattingOptionTypeDef",
    "FilledMapShapeConditionalFormattingTypeDef",
    "PivotTableCellConditionalFormattingTypeDef",
    "TableCellConditionalFormattingTypeDef",
    "ThemeTypeDef",
    "GaugeChartOptionsTypeDef",
    "KPIOptionsTypeDef",
    "DateDimensionFieldTypeDef",
    "DateMeasureFieldTypeDef",
    "NumericalDimensionFieldTypeDef",
    "NumericalMeasureFieldTypeDef",
    "ReferenceLineLabelConfigurationTypeDef",
    "CategoricalDimensionFieldTypeDef",
    "CategoricalMeasureFieldTypeDef",
    "FormatConfigurationTypeDef",
    "FilterTypeDef",
    "BarChartSortConfigurationTypeDef",
    "BoxPlotSortConfigurationTypeDef",
    "ComboChartSortConfigurationTypeDef",
    "FilledMapSortConfigurationTypeDef",
    "FunnelChartSortConfigurationTypeDef",
    "HeatMapSortConfigurationTypeDef",
    "KPISortConfigurationTypeDef",
    "LineChartSortConfigurationTypeDef",
    "PieChartSortConfigurationTypeDef",
    "RadarChartSortConfigurationTypeDef",
    "SankeyDiagramSortConfigurationTypeDef",
    "TableSortConfigurationTypeDef",
    "TreeMapSortConfigurationTypeDef",
    "WaterfallChartSortConfigurationTypeDef",
    "WordCloudSortConfigurationTypeDef",
    "PivotFieldSortOptionsTypeDef",
    "FieldBasedTooltipTypeDef",
    "TopicDetailsTypeDef",
    "DescribeAssetBundleImportJobResponseTypeDef",
    "StartAssetBundleImportJobRequestRequestTypeDef",
    "CreateDataSourceRequestRequestTypeDef",
    "UpdateDataSourceRequestRequestTypeDef",
    "SnapshotJobResultTypeDef",
    "DefaultNewSheetConfigurationTypeDef",
    "BodySectionContentTypeDef",
    "HeaderFooterSectionConfigurationTypeDef",
    "VisualCustomActionOperationTypeDef",
    "DescribeDataSetResponseTypeDef",
    "TableFieldOptionTypeDef",
    "GaugeChartConditionalFormattingTypeDef",
    "KPIConditionalFormattingTypeDef",
    "FilledMapConditionalFormattingOptionTypeDef",
    "PivotTableConditionalFormattingOptionTypeDef",
    "TableConditionalFormattingOptionTypeDef",
    "DescribeThemeResponseTypeDef",
    "ReferenceLineTypeDef",
    "DimensionFieldTypeDef",
    "MeasureFieldTypeDef",
    "ColumnConfigurationTypeDef",
    "UnaggregatedFieldTypeDef",
    "FilterGroupTypeDef",
    "PivotTableSortConfigurationTypeDef",
    "TooltipOptionsTypeDef",
    "CreateTopicRequestRequestTypeDef",
    "DescribeTopicResponseTypeDef",
    "UpdateTopicRequestRequestTypeDef",
    "DescribeDashboardSnapshotJobResultResponseTypeDef",
    "AnalysisDefaultsTypeDef",
    "BodySectionConfigurationTypeDef",
    "VisualCustomActionTypeDef",
    "TableFieldOptionsTypeDef",
    "FilledMapConditionalFormattingTypeDef",
    "PivotTableConditionalFormattingTypeDef",
    "TableConditionalFormattingTypeDef",
    "UniqueValuesComputationTypeDef",
    "BarChartAggregatedFieldWellsTypeDef",
    "BoxPlotAggregatedFieldWellsTypeDef",
    "ComboChartAggregatedFieldWellsTypeDef",
    "FilledMapAggregatedFieldWellsTypeDef",
    "ForecastComputationTypeDef",
    "FunnelChartAggregatedFieldWellsTypeDef",
    "GaugeChartFieldWellsTypeDef",
    "GeospatialMapAggregatedFieldWellsTypeDef",
    "GrowthRateComputationTypeDef",
    "HeatMapAggregatedFieldWellsTypeDef",
    "HistogramAggregatedFieldWellsTypeDef",
    "KPIFieldWellsTypeDef",
    "LineChartAggregatedFieldWellsTypeDef",
    "MaximumMinimumComputationTypeDef",
    "MetricComparisonComputationTypeDef",
    "PeriodOverPeriodComputationTypeDef",
    "PeriodToDateComputationTypeDef",
    "PieChartAggregatedFieldWellsTypeDef",
    "PivotTableAggregatedFieldWellsTypeDef",
    "RadarChartAggregatedFieldWellsTypeDef",
    "SankeyDiagramAggregatedFieldWellsTypeDef",
    "ScatterPlotCategoricallyAggregatedFieldWellsTypeDef",
    "ScatterPlotUnaggregatedFieldWellsTypeDef",
    "TableAggregatedFieldWellsTypeDef",
    "TopBottomMoversComputationTypeDef",
    "TopBottomRankedComputationTypeDef",
    "TotalAggregationComputationTypeDef",
    "TreeMapAggregatedFieldWellsTypeDef",
    "WaterfallChartAggregatedFieldWellsTypeDef",
    "WordCloudAggregatedFieldWellsTypeDef",
    "TableUnaggregatedFieldWellsTypeDef",
    "SectionBasedLayoutConfigurationTypeDef",
    "CustomContentVisualTypeDef",
    "EmptyVisualTypeDef",
    "BarChartFieldWellsTypeDef",
    "BoxPlotFieldWellsTypeDef",
    "ComboChartFieldWellsTypeDef",
    "FilledMapFieldWellsTypeDef",
    "FunnelChartFieldWellsTypeDef",
    "GaugeChartConfigurationTypeDef",
    "GeospatialMapFieldWellsTypeDef",
    "HeatMapFieldWellsTypeDef",
    "HistogramFieldWellsTypeDef",
    "KPIConfigurationTypeDef",
    "LineChartFieldWellsTypeDef",
    "PieChartFieldWellsTypeDef",
    "PivotTableFieldWellsTypeDef",
    "RadarChartFieldWellsTypeDef",
    "SankeyDiagramFieldWellsTypeDef",
    "ScatterPlotFieldWellsTypeDef",
    "ComputationTypeDef",
    "TreeMapFieldWellsTypeDef",
    "WaterfallChartFieldWellsTypeDef",
    "WordCloudFieldWellsTypeDef",
    "TableFieldWellsTypeDef",
    "LayoutConfigurationTypeDef",
    "BarChartConfigurationTypeDef",
    "BoxPlotChartConfigurationTypeDef",
    "ComboChartConfigurationTypeDef",
    "FilledMapConfigurationTypeDef",
    "FunnelChartConfigurationTypeDef",
    "GaugeChartVisualTypeDef",
    "GeospatialMapConfigurationTypeDef",
    "HeatMapConfigurationTypeDef",
    "HistogramConfigurationTypeDef",
    "KPIVisualTypeDef",
    "LineChartConfigurationTypeDef",
    "PieChartConfigurationTypeDef",
    "PivotTableConfigurationTypeDef",
    "RadarChartConfigurationTypeDef",
    "SankeyDiagramChartConfigurationTypeDef",
    "ScatterPlotConfigurationTypeDef",
    "InsightConfigurationTypeDef",
    "TreeMapConfigurationTypeDef",
    "WaterfallChartConfigurationTypeDef",
    "WordCloudChartConfigurationTypeDef",
    "TableConfigurationTypeDef",
    "LayoutTypeDef",
    "BarChartVisualTypeDef",
    "BoxPlotVisualTypeDef",
    "ComboChartVisualTypeDef",
    "FilledMapVisualTypeDef",
    "FunnelChartVisualTypeDef",
    "GeospatialMapVisualTypeDef",
    "HeatMapVisualTypeDef",
    "HistogramVisualTypeDef",
    "LineChartVisualTypeDef",
    "PieChartVisualTypeDef",
    "PivotTableVisualTypeDef",
    "RadarChartVisualTypeDef",
    "SankeyDiagramVisualTypeDef",
    "ScatterPlotVisualTypeDef",
    "InsightVisualTypeDef",
    "TreeMapVisualTypeDef",
    "WaterfallVisualTypeDef",
    "WordCloudVisualTypeDef",
    "TableVisualTypeDef",
    "VisualTypeDef",
    "SheetDefinitionTypeDef",
    "AnalysisDefinitionTypeDef",
    "DashboardVersionDefinitionTypeDef",
    "TemplateVersionDefinitionTypeDef",
    "CreateAnalysisRequestRequestTypeDef",
    "DescribeAnalysisDefinitionResponseTypeDef",
    "UpdateAnalysisRequestRequestTypeDef",
    "CreateDashboardRequestRequestTypeDef",
    "DescribeDashboardDefinitionResponseTypeDef",
    "UpdateDashboardRequestRequestTypeDef",
    "CreateTemplateRequestRequestTypeDef",
    "DescribeTemplateDefinitionResponseTypeDef",
    "UpdateTemplateRequestRequestTypeDef",
)

AccountCustomizationTypeDef = TypedDict(
    "AccountCustomizationTypeDef",
    {
        "DefaultTheme": NotRequired[str],
        "DefaultEmailCustomizationTemplate": NotRequired[str],
    },
)

AccountInfoTypeDef = TypedDict(
    "AccountInfoTypeDef",
    {
        "AccountName": NotRequired[str],
        "Edition": NotRequired[EditionType],
        "NotificationEmail": NotRequired[str],
        "AuthenticationType": NotRequired[str],
        "AccountSubscriptionStatus": NotRequired[str],
        "IAMIdentityCenterInstanceArn": NotRequired[str],
    },
)

AccountSettingsTypeDef = TypedDict(
    "AccountSettingsTypeDef",
    {
        "AccountName": NotRequired[str],
        "Edition": NotRequired[EditionType],
        "DefaultNamespace": NotRequired[str],
        "NotificationEmail": NotRequired[str],
        "PublicSharingEnabled": NotRequired[bool],
        "TerminationProtectionEnabled": NotRequired[bool],
    },
)

ActiveIAMPolicyAssignmentTypeDef = TypedDict(
    "ActiveIAMPolicyAssignmentTypeDef",
    {
        "AssignmentName": NotRequired[str],
        "PolicyArn": NotRequired[str],
    },
)

AdHocFilteringOptionTypeDef = TypedDict(
    "AdHocFilteringOptionTypeDef",
    {
        "AvailabilityStatus": NotRequired[DashboardBehaviorType],
    },
)

AttributeAggregationFunctionTypeDef = TypedDict(
    "AttributeAggregationFunctionTypeDef",
    {
        "SimpleAttributeAggregation": NotRequired[Literal["UNIQUE_VALUE"]],
        "ValueForMultipleValues": NotRequired[str],
    },
)

ColumnIdentifierTypeDef = TypedDict(
    "ColumnIdentifierTypeDef",
    {
        "DataSetIdentifier": str,
        "ColumnName": str,
    },
)

AmazonElasticsearchParametersTypeDef = TypedDict(
    "AmazonElasticsearchParametersTypeDef",
    {
        "Domain": str,
    },
)

AmazonOpenSearchParametersTypeDef = TypedDict(
    "AmazonOpenSearchParametersTypeDef",
    {
        "Domain": str,
    },
)

CalculatedFieldTypeDef = TypedDict(
    "CalculatedFieldTypeDef",
    {
        "DataSetIdentifier": str,
        "Name": str,
        "Expression": str,
    },
)

DataSetIdentifierDeclarationTypeDef = TypedDict(
    "DataSetIdentifierDeclarationTypeDef",
    {
        "Identifier": str,
        "DataSetArn": str,
    },
)

EntityTypeDef = TypedDict(
    "EntityTypeDef",
    {
        "Path": NotRequired[str],
    },
)

AnalysisSearchFilterTypeDef = TypedDict(
    "AnalysisSearchFilterTypeDef",
    {
        "Operator": NotRequired[FilterOperatorType],
        "Name": NotRequired[AnalysisFilterAttributeType],
        "Value": NotRequired[str],
    },
)

DataSetReferenceTypeDef = TypedDict(
    "DataSetReferenceTypeDef",
    {
        "DataSetPlaceholder": str,
        "DataSetArn": str,
    },
)

AnalysisSummaryTypeDef = TypedDict(
    "AnalysisSummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "AnalysisId": NotRequired[str],
        "Name": NotRequired[str],
        "Status": NotRequired[ResourceStatusType],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
    },
)

SheetTypeDef = TypedDict(
    "SheetTypeDef",
    {
        "SheetId": NotRequired[str],
        "Name": NotRequired[str],
    },
)

AnchorDateConfigurationTypeDef = TypedDict(
    "AnchorDateConfigurationTypeDef",
    {
        "AnchorOption": NotRequired[Literal["NOW"]],
        "ParameterName": NotRequired[str],
    },
)

AnonymousUserDashboardEmbeddingConfigurationTypeDef = TypedDict(
    "AnonymousUserDashboardEmbeddingConfigurationTypeDef",
    {
        "InitialDashboardId": str,
    },
)

DashboardVisualIdTypeDef = TypedDict(
    "DashboardVisualIdTypeDef",
    {
        "DashboardId": str,
        "SheetId": str,
        "VisualId": str,
    },
)

AnonymousUserQSearchBarEmbeddingConfigurationTypeDef = TypedDict(
    "AnonymousUserQSearchBarEmbeddingConfigurationTypeDef",
    {
        "InitialTopicId": str,
    },
)

ArcAxisDisplayRangeTypeDef = TypedDict(
    "ArcAxisDisplayRangeTypeDef",
    {
        "Min": NotRequired[float],
        "Max": NotRequired[float],
    },
)

ArcConfigurationTypeDef = TypedDict(
    "ArcConfigurationTypeDef",
    {
        "ArcAngle": NotRequired[float],
        "ArcThickness": NotRequired[ArcThicknessOptionsType],
    },
)

ArcOptionsTypeDef = TypedDict(
    "ArcOptionsTypeDef",
    {
        "ArcThickness": NotRequired[ArcThicknessType],
    },
)

AssetBundleExportJobAnalysisOverridePropertiesTypeDef = TypedDict(
    "AssetBundleExportJobAnalysisOverridePropertiesTypeDef",
    {
        "Properties": List[Literal["Name"]],
        "Arn": NotRequired[str],
    },
)

AssetBundleExportJobDashboardOverridePropertiesTypeDef = TypedDict(
    "AssetBundleExportJobDashboardOverridePropertiesTypeDef",
    {
        "Properties": List[Literal["Name"]],
        "Arn": NotRequired[str],
    },
)

AssetBundleExportJobDataSetOverridePropertiesTypeDef = TypedDict(
    "AssetBundleExportJobDataSetOverridePropertiesTypeDef",
    {
        "Properties": List[Literal["Name"]],
        "Arn": NotRequired[str],
    },
)

AssetBundleExportJobDataSourceOverridePropertiesTypeDef = TypedDict(
    "AssetBundleExportJobDataSourceOverridePropertiesTypeDef",
    {
        "Properties": List[AssetBundleExportJobDataSourcePropertyToOverrideType],
        "Arn": NotRequired[str],
    },
)

AssetBundleExportJobRefreshScheduleOverridePropertiesTypeDef = TypedDict(
    "AssetBundleExportJobRefreshScheduleOverridePropertiesTypeDef",
    {
        "Properties": List[Literal["StartAfterDateTime"]],
        "Arn": NotRequired[str],
    },
)

AssetBundleExportJobResourceIdOverrideConfigurationTypeDef = TypedDict(
    "AssetBundleExportJobResourceIdOverrideConfigurationTypeDef",
    {
        "PrefixForAllResources": NotRequired[bool],
    },
)

AssetBundleExportJobThemeOverridePropertiesTypeDef = TypedDict(
    "AssetBundleExportJobThemeOverridePropertiesTypeDef",
    {
        "Properties": List[Literal["Name"]],
        "Arn": NotRequired[str],
    },
)

AssetBundleExportJobVPCConnectionOverridePropertiesTypeDef = TypedDict(
    "AssetBundleExportJobVPCConnectionOverridePropertiesTypeDef",
    {
        "Properties": List[AssetBundleExportJobVPCConnectionPropertyToOverrideType],
        "Arn": NotRequired[str],
    },
)

AssetBundleExportJobErrorTypeDef = TypedDict(
    "AssetBundleExportJobErrorTypeDef",
    {
        "Arn": NotRequired[str],
        "Type": NotRequired[str],
        "Message": NotRequired[str],
    },
)

AssetBundleExportJobSummaryTypeDef = TypedDict(
    "AssetBundleExportJobSummaryTypeDef",
    {
        "JobStatus": NotRequired[AssetBundleExportJobStatusType],
        "Arn": NotRequired[str],
        "CreatedTime": NotRequired[datetime],
        "AssetBundleExportJobId": NotRequired[str],
        "IncludeAllDependencies": NotRequired[bool],
        "ExportFormat": NotRequired[AssetBundleExportFormatType],
    },
)

AssetBundleImportJobAnalysisOverrideParametersTypeDef = TypedDict(
    "AssetBundleImportJobAnalysisOverrideParametersTypeDef",
    {
        "AnalysisId": str,
        "Name": NotRequired[str],
    },
)

AssetBundleImportJobDashboardOverrideParametersTypeDef = TypedDict(
    "AssetBundleImportJobDashboardOverrideParametersTypeDef",
    {
        "DashboardId": str,
        "Name": NotRequired[str],
    },
)

AssetBundleImportJobDataSetOverrideParametersTypeDef = TypedDict(
    "AssetBundleImportJobDataSetOverrideParametersTypeDef",
    {
        "DataSetId": str,
        "Name": NotRequired[str],
    },
)

AssetBundleImportJobDataSourceCredentialPairTypeDef = TypedDict(
    "AssetBundleImportJobDataSourceCredentialPairTypeDef",
    {
        "Username": str,
        "Password": str,
    },
)

SslPropertiesTypeDef = TypedDict(
    "SslPropertiesTypeDef",
    {
        "DisableSsl": NotRequired[bool],
    },
)

VpcConnectionPropertiesTypeDef = TypedDict(
    "VpcConnectionPropertiesTypeDef",
    {
        "VpcConnectionArn": str,
    },
)

AssetBundleImportJobErrorTypeDef = TypedDict(
    "AssetBundleImportJobErrorTypeDef",
    {
        "Arn": NotRequired[str],
        "Type": NotRequired[str],
        "Message": NotRequired[str],
    },
)

AssetBundleImportJobRefreshScheduleOverrideParametersTypeDef = TypedDict(
    "AssetBundleImportJobRefreshScheduleOverrideParametersTypeDef",
    {
        "DataSetId": str,
        "ScheduleId": str,
        "StartAfterDateTime": NotRequired[datetime],
    },
)

AssetBundleImportJobResourceIdOverrideConfigurationTypeDef = TypedDict(
    "AssetBundleImportJobResourceIdOverrideConfigurationTypeDef",
    {
        "PrefixForAllResources": NotRequired[str],
    },
)

AssetBundleImportJobThemeOverrideParametersTypeDef = TypedDict(
    "AssetBundleImportJobThemeOverrideParametersTypeDef",
    {
        "ThemeId": str,
        "Name": NotRequired[str],
    },
)

AssetBundleImportJobVPCConnectionOverrideParametersTypeDef = TypedDict(
    "AssetBundleImportJobVPCConnectionOverrideParametersTypeDef",
    {
        "VPCConnectionId": str,
        "Name": NotRequired[str],
        "SubnetIds": NotRequired[List[str]],
        "SecurityGroupIds": NotRequired[List[str]],
        "DnsResolvers": NotRequired[List[str]],
        "RoleArn": NotRequired[str],
    },
)

AssetBundleImportJobSummaryTypeDef = TypedDict(
    "AssetBundleImportJobSummaryTypeDef",
    {
        "JobStatus": NotRequired[AssetBundleImportJobStatusType],
        "Arn": NotRequired[str],
        "CreatedTime": NotRequired[datetime],
        "AssetBundleImportJobId": NotRequired[str],
        "FailureAction": NotRequired[AssetBundleImportFailureActionType],
    },
)

AssetBundleImportSourceDescriptionTypeDef = TypedDict(
    "AssetBundleImportSourceDescriptionTypeDef",
    {
        "Body": NotRequired[str],
        "S3Uri": NotRequired[str],
    },
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
AthenaParametersTypeDef = TypedDict(
    "AthenaParametersTypeDef",
    {
        "WorkGroup": NotRequired[str],
        "RoleArn": NotRequired[str],
    },
)

AuroraParametersTypeDef = TypedDict(
    "AuroraParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

AuroraPostgreSqlParametersTypeDef = TypedDict(
    "AuroraPostgreSqlParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

AwsIotAnalyticsParametersTypeDef = TypedDict(
    "AwsIotAnalyticsParametersTypeDef",
    {
        "DataSetName": str,
    },
)

DateAxisOptionsTypeDef = TypedDict(
    "DateAxisOptionsTypeDef",
    {
        "MissingDateVisibility": NotRequired[VisibilityType],
    },
)

AxisDisplayMinMaxRangeTypeDef = TypedDict(
    "AxisDisplayMinMaxRangeTypeDef",
    {
        "Minimum": NotRequired[float],
        "Maximum": NotRequired[float],
    },
)

AxisLinearScaleTypeDef = TypedDict(
    "AxisLinearScaleTypeDef",
    {
        "StepCount": NotRequired[int],
        "StepSize": NotRequired[float],
    },
)

AxisLogarithmicScaleTypeDef = TypedDict(
    "AxisLogarithmicScaleTypeDef",
    {
        "Base": NotRequired[float],
    },
)

ItemsLimitConfigurationTypeDef = TypedDict(
    "ItemsLimitConfigurationTypeDef",
    {
        "ItemsLimit": NotRequired[int],
        "OtherCategories": NotRequired[OtherCategoriesType],
    },
)

BinCountOptionsTypeDef = TypedDict(
    "BinCountOptionsTypeDef",
    {
        "Value": NotRequired[int],
    },
)

BinWidthOptionsTypeDef = TypedDict(
    "BinWidthOptionsTypeDef",
    {
        "Value": NotRequired[float],
        "BinCountLimit": NotRequired[int],
    },
)

BookmarksConfigurationsTypeDef = TypedDict(
    "BookmarksConfigurationsTypeDef",
    {
        "Enabled": bool,
    },
)

BorderStyleTypeDef = TypedDict(
    "BorderStyleTypeDef",
    {
        "Show": NotRequired[bool],
    },
)

BoxPlotStyleOptionsTypeDef = TypedDict(
    "BoxPlotStyleOptionsTypeDef",
    {
        "FillStyle": NotRequired[BoxPlotFillStyleType],
    },
)

PaginationConfigurationTypeDef = TypedDict(
    "PaginationConfigurationTypeDef",
    {
        "PageSize": int,
        "PageNumber": int,
    },
)

CalculatedColumnTypeDef = TypedDict(
    "CalculatedColumnTypeDef",
    {
        "ColumnName": str,
        "ColumnId": str,
        "Expression": str,
    },
)

CalculatedMeasureFieldTypeDef = TypedDict(
    "CalculatedMeasureFieldTypeDef",
    {
        "FieldId": str,
        "Expression": str,
    },
)

CancelIngestionRequestRequestTypeDef = TypedDict(
    "CancelIngestionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
        "IngestionId": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

CastColumnTypeOperationTypeDef = TypedDict(
    "CastColumnTypeOperationTypeDef",
    {
        "ColumnName": str,
        "NewColumnType": ColumnDataTypeType,
        "Format": NotRequired[str],
    },
)

CustomFilterConfigurationTypeDef = TypedDict(
    "CustomFilterConfigurationTypeDef",
    {
        "MatchOperator": CategoryFilterMatchOperatorType,
        "NullOption": FilterNullOptionType,
        "CategoryValue": NotRequired[str],
        "SelectAllOptions": NotRequired[Literal["FILTER_ALL_VALUES"]],
        "ParameterName": NotRequired[str],
    },
)

CustomFilterListConfigurationTypeDef = TypedDict(
    "CustomFilterListConfigurationTypeDef",
    {
        "MatchOperator": CategoryFilterMatchOperatorType,
        "NullOption": FilterNullOptionType,
        "CategoryValues": NotRequired[Sequence[str]],
        "SelectAllOptions": NotRequired[Literal["FILTER_ALL_VALUES"]],
    },
)

FilterListConfigurationTypeDef = TypedDict(
    "FilterListConfigurationTypeDef",
    {
        "MatchOperator": CategoryFilterMatchOperatorType,
        "CategoryValues": NotRequired[Sequence[str]],
        "SelectAllOptions": NotRequired[Literal["FILTER_ALL_VALUES"]],
        "NullOption": NotRequired[FilterNullOptionType],
    },
)

CellValueSynonymTypeDef = TypedDict(
    "CellValueSynonymTypeDef",
    {
        "CellValue": NotRequired[str],
        "Synonyms": NotRequired[Sequence[str]],
    },
)

SimpleClusterMarkerTypeDef = TypedDict(
    "SimpleClusterMarkerTypeDef",
    {
        "Color": NotRequired[str],
    },
)

CollectiveConstantTypeDef = TypedDict(
    "CollectiveConstantTypeDef",
    {
        "ValueList": NotRequired[Sequence[str]],
    },
)

DataColorTypeDef = TypedDict(
    "DataColorTypeDef",
    {
        "Color": NotRequired[str],
        "DataValue": NotRequired[float],
    },
)

CustomColorTypeDef = TypedDict(
    "CustomColorTypeDef",
    {
        "Color": str,
        "FieldValue": NotRequired[str],
        "SpecialValue": NotRequired[SpecialValueType],
    },
)

ColumnDescriptionTypeDef = TypedDict(
    "ColumnDescriptionTypeDef",
    {
        "Text": NotRequired[str],
    },
)

ColumnGroupColumnSchemaTypeDef = TypedDict(
    "ColumnGroupColumnSchemaTypeDef",
    {
        "Name": NotRequired[str],
    },
)

GeoSpatialColumnGroupTypeDef = TypedDict(
    "GeoSpatialColumnGroupTypeDef",
    {
        "Name": str,
        "Columns": Sequence[str],
        "CountryCode": NotRequired[Literal["US"]],
    },
)

ColumnLevelPermissionRuleTypeDef = TypedDict(
    "ColumnLevelPermissionRuleTypeDef",
    {
        "Principals": NotRequired[Sequence[str]],
        "ColumnNames": NotRequired[Sequence[str]],
    },
)

ColumnSchemaTypeDef = TypedDict(
    "ColumnSchemaTypeDef",
    {
        "Name": NotRequired[str],
        "DataType": NotRequired[str],
        "GeographicRole": NotRequired[str],
    },
)

ComparativeOrderTypeDef = TypedDict(
    "ComparativeOrderTypeDef",
    {
        "UseOrdering": NotRequired[ColumnOrderingTypeType],
        "SpecifedOrder": NotRequired[Sequence[str]],
        "TreatUndefinedSpecifiedValues": NotRequired[UndefinedSpecifiedValueTypeType],
    },
)

ConditionalFormattingSolidColorTypeDef = TypedDict(
    "ConditionalFormattingSolidColorTypeDef",
    {
        "Expression": str,
        "Color": NotRequired[str],
    },
)

ConditionalFormattingCustomIconOptionsTypeDef = TypedDict(
    "ConditionalFormattingCustomIconOptionsTypeDef",
    {
        "Icon": NotRequired[IconType],
        "UnicodeIcon": NotRequired[str],
    },
)

ConditionalFormattingIconDisplayConfigurationTypeDef = TypedDict(
    "ConditionalFormattingIconDisplayConfigurationTypeDef",
    {
        "IconDisplayOption": NotRequired[Literal["ICON_ONLY"]],
    },
)

ConditionalFormattingIconSetTypeDef = TypedDict(
    "ConditionalFormattingIconSetTypeDef",
    {
        "Expression": str,
        "IconSetType": NotRequired[ConditionalFormattingIconSetTypeType],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

CreateAccountSubscriptionRequestRequestTypeDef = TypedDict(
    "CreateAccountSubscriptionRequestRequestTypeDef",
    {
        "Edition": EditionType,
        "AuthenticationMethod": AuthenticationMethodOptionType,
        "AwsAccountId": str,
        "AccountName": str,
        "NotificationEmail": str,
        "ActiveDirectoryName": NotRequired[str],
        "Realm": NotRequired[str],
        "DirectoryId": NotRequired[str],
        "AdminGroup": NotRequired[Sequence[str]],
        "AuthorGroup": NotRequired[Sequence[str]],
        "ReaderGroup": NotRequired[Sequence[str]],
        "FirstName": NotRequired[str],
        "LastName": NotRequired[str],
        "EmailAddress": NotRequired[str],
        "ContactNumber": NotRequired[str],
    },
)

SignupResponseTypeDef = TypedDict(
    "SignupResponseTypeDef",
    {
        "IAMUser": NotRequired[bool],
        "userLoginName": NotRequired[str],
        "accountName": NotRequired[str],
        "directoryType": NotRequired[str],
    },
)

ResourcePermissionTypeDef = TypedDict(
    "ResourcePermissionTypeDef",
    {
        "Principal": str,
        "Actions": Sequence[str],
    },
)

ValidationStrategyTypeDef = TypedDict(
    "ValidationStrategyTypeDef",
    {
        "Mode": ValidationStrategyModeType,
    },
)

DataSetUsageConfigurationTypeDef = TypedDict(
    "DataSetUsageConfigurationTypeDef",
    {
        "DisableUseAsDirectQuerySource": NotRequired[bool],
        "DisableUseAsImportedSource": NotRequired[bool],
    },
)

FieldFolderTypeDef = TypedDict(
    "FieldFolderTypeDef",
    {
        "description": NotRequired[str],
        "columns": NotRequired[Sequence[str]],
    },
)

RowLevelPermissionDataSetTypeDef = TypedDict(
    "RowLevelPermissionDataSetTypeDef",
    {
        "Arn": str,
        "PermissionPolicy": RowLevelPermissionPolicyType,
        "Namespace": NotRequired[str],
        "FormatVersion": NotRequired[RowLevelPermissionFormatVersionType],
        "Status": NotRequired[StatusType],
    },
)

CreateFolderMembershipRequestRequestTypeDef = TypedDict(
    "CreateFolderMembershipRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
        "MemberId": str,
        "MemberType": MemberTypeType,
    },
)

FolderMemberTypeDef = TypedDict(
    "FolderMemberTypeDef",
    {
        "MemberId": NotRequired[str],
        "MemberType": NotRequired[MemberTypeType],
    },
)

CreateGroupMembershipRequestRequestTypeDef = TypedDict(
    "CreateGroupMembershipRequestRequestTypeDef",
    {
        "MemberName": str,
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

GroupMemberTypeDef = TypedDict(
    "GroupMemberTypeDef",
    {
        "Arn": NotRequired[str],
        "MemberName": NotRequired[str],
    },
)

CreateGroupRequestRequestTypeDef = TypedDict(
    "CreateGroupRequestRequestTypeDef",
    {
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
        "Description": NotRequired[str],
    },
)

GroupTypeDef = TypedDict(
    "GroupTypeDef",
    {
        "Arn": NotRequired[str],
        "GroupName": NotRequired[str],
        "Description": NotRequired[str],
        "PrincipalId": NotRequired[str],
    },
)

CreateIAMPolicyAssignmentRequestRequestTypeDef = TypedDict(
    "CreateIAMPolicyAssignmentRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AssignmentName": str,
        "AssignmentStatus": AssignmentStatusType,
        "Namespace": str,
        "PolicyArn": NotRequired[str],
        "Identities": NotRequired[Mapping[str, Sequence[str]]],
    },
)

CreateIngestionRequestRequestTypeDef = TypedDict(
    "CreateIngestionRequestRequestTypeDef",
    {
        "DataSetId": str,
        "IngestionId": str,
        "AwsAccountId": str,
        "IngestionType": NotRequired[IngestionTypeType],
    },
)

CreateTemplateAliasRequestRequestTypeDef = TypedDict(
    "CreateTemplateAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "AliasName": str,
        "TemplateVersionNumber": int,
    },
)

TemplateAliasTypeDef = TypedDict(
    "TemplateAliasTypeDef",
    {
        "AliasName": NotRequired[str],
        "Arn": NotRequired[str],
        "TemplateVersionNumber": NotRequired[int],
    },
)

CreateThemeAliasRequestRequestTypeDef = TypedDict(
    "CreateThemeAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "AliasName": str,
        "ThemeVersionNumber": int,
    },
)

ThemeAliasTypeDef = TypedDict(
    "ThemeAliasTypeDef",
    {
        "Arn": NotRequired[str],
        "AliasName": NotRequired[str],
        "ThemeVersionNumber": NotRequired[int],
    },
)

DecimalPlacesConfigurationTypeDef = TypedDict(
    "DecimalPlacesConfigurationTypeDef",
    {
        "DecimalPlaces": int,
    },
)

NegativeValueConfigurationTypeDef = TypedDict(
    "NegativeValueConfigurationTypeDef",
    {
        "DisplayMode": NegativeValueDisplayModeType,
    },
)

NullValueFormatConfigurationTypeDef = TypedDict(
    "NullValueFormatConfigurationTypeDef",
    {
        "NullString": str,
    },
)

LocalNavigationConfigurationTypeDef = TypedDict(
    "LocalNavigationConfigurationTypeDef",
    {
        "TargetSheetId": str,
    },
)

CustomActionURLOperationTypeDef = TypedDict(
    "CustomActionURLOperationTypeDef",
    {
        "URLTemplate": str,
        "URLTarget": URLTargetConfigurationType,
    },
)

CustomContentConfigurationTypeDef = TypedDict(
    "CustomContentConfigurationTypeDef",
    {
        "ContentUrl": NotRequired[str],
        "ContentType": NotRequired[CustomContentTypeType],
        "ImageScaling": NotRequired[CustomContentImageScalingConfigurationType],
    },
)

CustomNarrativeOptionsTypeDef = TypedDict(
    "CustomNarrativeOptionsTypeDef",
    {
        "Narrative": str,
    },
)

TimestampTypeDef = Union[datetime, str]
InputColumnTypeDef = TypedDict(
    "InputColumnTypeDef",
    {
        "Name": str,
        "Type": InputColumnDataTypeType,
    },
)

DataPointDrillUpDownOptionTypeDef = TypedDict(
    "DataPointDrillUpDownOptionTypeDef",
    {
        "AvailabilityStatus": NotRequired[DashboardBehaviorType],
    },
)

DataPointMenuLabelOptionTypeDef = TypedDict(
    "DataPointMenuLabelOptionTypeDef",
    {
        "AvailabilityStatus": NotRequired[DashboardBehaviorType],
    },
)

DataPointTooltipOptionTypeDef = TypedDict(
    "DataPointTooltipOptionTypeDef",
    {
        "AvailabilityStatus": NotRequired[DashboardBehaviorType],
    },
)

ExportToCSVOptionTypeDef = TypedDict(
    "ExportToCSVOptionTypeDef",
    {
        "AvailabilityStatus": NotRequired[DashboardBehaviorType],
    },
)

ExportWithHiddenFieldsOptionTypeDef = TypedDict(
    "ExportWithHiddenFieldsOptionTypeDef",
    {
        "AvailabilityStatus": NotRequired[DashboardBehaviorType],
    },
)

SheetControlsOptionTypeDef = TypedDict(
    "SheetControlsOptionTypeDef",
    {
        "VisibilityState": NotRequired[DashboardUIStateType],
    },
)

SheetLayoutElementMaximizationOptionTypeDef = TypedDict(
    "SheetLayoutElementMaximizationOptionTypeDef",
    {
        "AvailabilityStatus": NotRequired[DashboardBehaviorType],
    },
)

VisualAxisSortOptionTypeDef = TypedDict(
    "VisualAxisSortOptionTypeDef",
    {
        "AvailabilityStatus": NotRequired[DashboardBehaviorType],
    },
)

VisualMenuOptionTypeDef = TypedDict(
    "VisualMenuOptionTypeDef",
    {
        "AvailabilityStatus": NotRequired[DashboardBehaviorType],
    },
)

DashboardSearchFilterTypeDef = TypedDict(
    "DashboardSearchFilterTypeDef",
    {
        "Operator": FilterOperatorType,
        "Name": NotRequired[DashboardFilterAttributeType],
        "Value": NotRequired[str],
    },
)

DashboardSummaryTypeDef = TypedDict(
    "DashboardSummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "DashboardId": NotRequired[str],
        "Name": NotRequired[str],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
        "PublishedVersionNumber": NotRequired[int],
        "LastPublishedTime": NotRequired[datetime],
    },
)

DashboardVersionSummaryTypeDef = TypedDict(
    "DashboardVersionSummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "CreatedTime": NotRequired[datetime],
        "VersionNumber": NotRequired[int],
        "Status": NotRequired[ResourceStatusType],
        "SourceEntityArn": NotRequired[str],
        "Description": NotRequired[str],
    },
)

ExportHiddenFieldsOptionTypeDef = TypedDict(
    "ExportHiddenFieldsOptionTypeDef",
    {
        "AvailabilityStatus": NotRequired[DashboardBehaviorType],
    },
)

DataAggregationTypeDef = TypedDict(
    "DataAggregationTypeDef",
    {
        "DatasetRowDateGranularity": NotRequired[TopicTimeGranularityType],
        "DefaultDateColumnName": NotRequired[str],
    },
)

DataBarsOptionsTypeDef = TypedDict(
    "DataBarsOptionsTypeDef",
    {
        "FieldId": str,
        "PositiveColor": NotRequired[str],
        "NegativeColor": NotRequired[str],
    },
)

DataColorPaletteTypeDef = TypedDict(
    "DataColorPaletteTypeDef",
    {
        "Colors": NotRequired[Sequence[str]],
        "MinMaxGradient": NotRequired[Sequence[str]],
        "EmptyFillColor": NotRequired[str],
    },
)

DataPathLabelTypeTypeDef = TypedDict(
    "DataPathLabelTypeTypeDef",
    {
        "FieldId": NotRequired[str],
        "FieldValue": NotRequired[str],
        "Visibility": NotRequired[VisibilityType],
    },
)

FieldLabelTypeTypeDef = TypedDict(
    "FieldLabelTypeTypeDef",
    {
        "FieldId": NotRequired[str],
        "Visibility": NotRequired[VisibilityType],
    },
)

MaximumLabelTypeTypeDef = TypedDict(
    "MaximumLabelTypeTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
    },
)

MinimumLabelTypeTypeDef = TypedDict(
    "MinimumLabelTypeTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
    },
)

RangeEndsLabelTypeTypeDef = TypedDict(
    "RangeEndsLabelTypeTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
    },
)

DataPathValueTypeDef = TypedDict(
    "DataPathValueTypeDef",
    {
        "FieldId": str,
        "FieldValue": str,
    },
)

DataSetSearchFilterTypeDef = TypedDict(
    "DataSetSearchFilterTypeDef",
    {
        "Operator": FilterOperatorType,
        "Name": DataSetFilterAttributeType,
        "Value": str,
    },
)

OutputColumnTypeDef = TypedDict(
    "OutputColumnTypeDef",
    {
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "Type": NotRequired[ColumnDataTypeType],
    },
)

DataSourceErrorInfoTypeDef = TypedDict(
    "DataSourceErrorInfoTypeDef",
    {
        "Type": NotRequired[DataSourceErrorInfoTypeType],
        "Message": NotRequired[str],
    },
)

DatabricksParametersTypeDef = TypedDict(
    "DatabricksParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "SqlEndpointPath": str,
    },
)

ExasolParametersTypeDef = TypedDict(
    "ExasolParametersTypeDef",
    {
        "Host": str,
        "Port": int,
    },
)

JiraParametersTypeDef = TypedDict(
    "JiraParametersTypeDef",
    {
        "SiteBaseUrl": str,
    },
)

MariaDbParametersTypeDef = TypedDict(
    "MariaDbParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

MySqlParametersTypeDef = TypedDict(
    "MySqlParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

OracleParametersTypeDef = TypedDict(
    "OracleParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

PostgreSqlParametersTypeDef = TypedDict(
    "PostgreSqlParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

PrestoParametersTypeDef = TypedDict(
    "PrestoParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Catalog": str,
    },
)

RdsParametersTypeDef = TypedDict(
    "RdsParametersTypeDef",
    {
        "InstanceId": str,
        "Database": str,
    },
)

ServiceNowParametersTypeDef = TypedDict(
    "ServiceNowParametersTypeDef",
    {
        "SiteBaseUrl": str,
    },
)

SnowflakeParametersTypeDef = TypedDict(
    "SnowflakeParametersTypeDef",
    {
        "Host": str,
        "Database": str,
        "Warehouse": str,
    },
)

SparkParametersTypeDef = TypedDict(
    "SparkParametersTypeDef",
    {
        "Host": str,
        "Port": int,
    },
)

SqlServerParametersTypeDef = TypedDict(
    "SqlServerParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

TeradataParametersTypeDef = TypedDict(
    "TeradataParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

TwitterParametersTypeDef = TypedDict(
    "TwitterParametersTypeDef",
    {
        "Query": str,
        "MaxRows": int,
    },
)

DataSourceSearchFilterTypeDef = TypedDict(
    "DataSourceSearchFilterTypeDef",
    {
        "Operator": FilterOperatorType,
        "Name": DataSourceFilterAttributeType,
        "Value": str,
    },
)

DataSourceSummaryTypeDef = TypedDict(
    "DataSourceSummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "DataSourceId": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[DataSourceTypeType],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
    },
)

RollingDateConfigurationTypeDef = TypedDict(
    "RollingDateConfigurationTypeDef",
    {
        "Expression": str,
        "DataSetIdentifier": NotRequired[str],
    },
)

MappedDataSetParameterTypeDef = TypedDict(
    "MappedDataSetParameterTypeDef",
    {
        "DataSetIdentifier": str,
        "DataSetParameterName": str,
    },
)

SheetControlInfoIconLabelOptionsTypeDef = TypedDict(
    "SheetControlInfoIconLabelOptionsTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
        "InfoIconText": NotRequired[str],
    },
)

DecimalDatasetParameterDefaultValuesTypeDef = TypedDict(
    "DecimalDatasetParameterDefaultValuesTypeDef",
    {
        "StaticValues": NotRequired[Sequence[float]],
    },
)

DecimalValueWhenUnsetConfigurationTypeDef = TypedDict(
    "DecimalValueWhenUnsetConfigurationTypeDef",
    {
        "ValueWhenUnsetOption": NotRequired[ValueWhenUnsetOptionType],
        "CustomValue": NotRequired[float],
    },
)

DecimalParameterTypeDef = TypedDict(
    "DecimalParameterTypeDef",
    {
        "Name": str,
        "Values": Sequence[float],
    },
)

DeleteAccountCustomizationRequestRequestTypeDef = TypedDict(
    "DeleteAccountCustomizationRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": NotRequired[str],
    },
)

DeleteAccountSubscriptionRequestRequestTypeDef = TypedDict(
    "DeleteAccountSubscriptionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)

DeleteAnalysisRequestRequestTypeDef = TypedDict(
    "DeleteAnalysisRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
        "RecoveryWindowInDays": NotRequired[int],
        "ForceDeleteWithoutRecovery": NotRequired[bool],
    },
)

DeleteDashboardRequestRequestTypeDef = TypedDict(
    "DeleteDashboardRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "VersionNumber": NotRequired[int],
    },
)

DeleteDataSetRefreshPropertiesRequestRequestTypeDef = TypedDict(
    "DeleteDataSetRefreshPropertiesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
    },
)

DeleteDataSetRequestRequestTypeDef = TypedDict(
    "DeleteDataSetRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
    },
)

DeleteDataSourceRequestRequestTypeDef = TypedDict(
    "DeleteDataSourceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
    },
)

DeleteFolderMembershipRequestRequestTypeDef = TypedDict(
    "DeleteFolderMembershipRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
        "MemberId": str,
        "MemberType": MemberTypeType,
    },
)

DeleteFolderRequestRequestTypeDef = TypedDict(
    "DeleteFolderRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
    },
)

DeleteGroupMembershipRequestRequestTypeDef = TypedDict(
    "DeleteGroupMembershipRequestRequestTypeDef",
    {
        "MemberName": str,
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DeleteGroupRequestRequestTypeDef = TypedDict(
    "DeleteGroupRequestRequestTypeDef",
    {
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DeleteIAMPolicyAssignmentRequestRequestTypeDef = TypedDict(
    "DeleteIAMPolicyAssignmentRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AssignmentName": str,
        "Namespace": str,
    },
)

DeleteNamespaceRequestRequestTypeDef = TypedDict(
    "DeleteNamespaceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DeleteRefreshScheduleRequestRequestTypeDef = TypedDict(
    "DeleteRefreshScheduleRequestRequestTypeDef",
    {
        "DataSetId": str,
        "AwsAccountId": str,
        "ScheduleId": str,
    },
)

DeleteTemplateAliasRequestRequestTypeDef = TypedDict(
    "DeleteTemplateAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "AliasName": str,
    },
)

DeleteTemplateRequestRequestTypeDef = TypedDict(
    "DeleteTemplateRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "VersionNumber": NotRequired[int],
    },
)

DeleteThemeAliasRequestRequestTypeDef = TypedDict(
    "DeleteThemeAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "AliasName": str,
    },
)

DeleteThemeRequestRequestTypeDef = TypedDict(
    "DeleteThemeRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "VersionNumber": NotRequired[int],
    },
)

DeleteTopicRefreshScheduleRequestRequestTypeDef = TypedDict(
    "DeleteTopicRefreshScheduleRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TopicId": str,
        "DatasetId": str,
    },
)

DeleteTopicRequestRequestTypeDef = TypedDict(
    "DeleteTopicRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TopicId": str,
    },
)

DeleteUserByPrincipalIdRequestRequestTypeDef = TypedDict(
    "DeleteUserByPrincipalIdRequestRequestTypeDef",
    {
        "PrincipalId": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DeleteUserRequestRequestTypeDef = TypedDict(
    "DeleteUserRequestRequestTypeDef",
    {
        "UserName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DeleteVPCConnectionRequestRequestTypeDef = TypedDict(
    "DeleteVPCConnectionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "VPCConnectionId": str,
    },
)

DescribeAccountCustomizationRequestRequestTypeDef = TypedDict(
    "DescribeAccountCustomizationRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": NotRequired[str],
        "Resolved": NotRequired[bool],
    },
)

DescribeAccountSettingsRequestRequestTypeDef = TypedDict(
    "DescribeAccountSettingsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)

DescribeAccountSubscriptionRequestRequestTypeDef = TypedDict(
    "DescribeAccountSubscriptionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)

DescribeAnalysisDefinitionRequestRequestTypeDef = TypedDict(
    "DescribeAnalysisDefinitionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
    },
)

DescribeAnalysisPermissionsRequestRequestTypeDef = TypedDict(
    "DescribeAnalysisPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
    },
)

DescribeAnalysisRequestRequestTypeDef = TypedDict(
    "DescribeAnalysisRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
    },
)

DescribeAssetBundleExportJobRequestRequestTypeDef = TypedDict(
    "DescribeAssetBundleExportJobRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AssetBundleExportJobId": str,
    },
)

DescribeAssetBundleImportJobRequestRequestTypeDef = TypedDict(
    "DescribeAssetBundleImportJobRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AssetBundleImportJobId": str,
    },
)

DescribeDashboardDefinitionRequestRequestTypeDef = TypedDict(
    "DescribeDashboardDefinitionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "VersionNumber": NotRequired[int],
        "AliasName": NotRequired[str],
    },
)

DescribeDashboardPermissionsRequestRequestTypeDef = TypedDict(
    "DescribeDashboardPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
    },
)

DescribeDashboardRequestRequestTypeDef = TypedDict(
    "DescribeDashboardRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "VersionNumber": NotRequired[int],
        "AliasName": NotRequired[str],
    },
)

DescribeDashboardSnapshotJobRequestRequestTypeDef = TypedDict(
    "DescribeDashboardSnapshotJobRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "SnapshotJobId": str,
    },
)

DescribeDashboardSnapshotJobResultRequestRequestTypeDef = TypedDict(
    "DescribeDashboardSnapshotJobResultRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "SnapshotJobId": str,
    },
)

SnapshotJobErrorInfoTypeDef = TypedDict(
    "SnapshotJobErrorInfoTypeDef",
    {
        "ErrorMessage": NotRequired[str],
        "ErrorType": NotRequired[str],
    },
)

DescribeDataSetPermissionsRequestRequestTypeDef = TypedDict(
    "DescribeDataSetPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
    },
)

DescribeDataSetRefreshPropertiesRequestRequestTypeDef = TypedDict(
    "DescribeDataSetRefreshPropertiesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
    },
)

DescribeDataSetRequestRequestTypeDef = TypedDict(
    "DescribeDataSetRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
    },
)

DescribeDataSourcePermissionsRequestRequestTypeDef = TypedDict(
    "DescribeDataSourcePermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
    },
)

DescribeDataSourceRequestRequestTypeDef = TypedDict(
    "DescribeDataSourceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)

DescribeFolderPermissionsRequestRequestTypeDef = TypedDict(
    "DescribeFolderPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
        "Namespace": NotRequired[str],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ResourcePermissionPaginatorTypeDef = TypedDict(
    "ResourcePermissionPaginatorTypeDef",
    {
        "Principal": str,
        "Actions": List[str],
    },
)

DescribeFolderRequestRequestTypeDef = TypedDict(
    "DescribeFolderRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
    },
)

DescribeFolderResolvedPermissionsRequestRequestTypeDef = TypedDict(
    "DescribeFolderResolvedPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
        "Namespace": NotRequired[str],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

FolderTypeDef = TypedDict(
    "FolderTypeDef",
    {
        "FolderId": NotRequired[str],
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "FolderType": NotRequired[Literal["SHARED"]],
        "FolderPath": NotRequired[List[str]],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
        "SharingModel": NotRequired[SharingModelType],
    },
)

DescribeGroupMembershipRequestRequestTypeDef = TypedDict(
    "DescribeGroupMembershipRequestRequestTypeDef",
    {
        "MemberName": str,
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DescribeGroupRequestRequestTypeDef = TypedDict(
    "DescribeGroupRequestRequestTypeDef",
    {
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DescribeIAMPolicyAssignmentRequestRequestTypeDef = TypedDict(
    "DescribeIAMPolicyAssignmentRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AssignmentName": str,
        "Namespace": str,
    },
)

IAMPolicyAssignmentTypeDef = TypedDict(
    "IAMPolicyAssignmentTypeDef",
    {
        "AwsAccountId": NotRequired[str],
        "AssignmentId": NotRequired[str],
        "AssignmentName": NotRequired[str],
        "PolicyArn": NotRequired[str],
        "Identities": NotRequired[Dict[str, List[str]]],
        "AssignmentStatus": NotRequired[AssignmentStatusType],
    },
)

DescribeIngestionRequestRequestTypeDef = TypedDict(
    "DescribeIngestionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
        "IngestionId": str,
    },
)

DescribeIpRestrictionRequestRequestTypeDef = TypedDict(
    "DescribeIpRestrictionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)

DescribeNamespaceRequestRequestTypeDef = TypedDict(
    "DescribeNamespaceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DescribeRefreshScheduleRequestRequestTypeDef = TypedDict(
    "DescribeRefreshScheduleRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
        "ScheduleId": str,
    },
)

DescribeTemplateAliasRequestRequestTypeDef = TypedDict(
    "DescribeTemplateAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "AliasName": str,
    },
)

DescribeTemplateDefinitionRequestRequestTypeDef = TypedDict(
    "DescribeTemplateDefinitionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "VersionNumber": NotRequired[int],
        "AliasName": NotRequired[str],
    },
)

DescribeTemplatePermissionsRequestRequestTypeDef = TypedDict(
    "DescribeTemplatePermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)

DescribeTemplateRequestRequestTypeDef = TypedDict(
    "DescribeTemplateRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "VersionNumber": NotRequired[int],
        "AliasName": NotRequired[str],
    },
)

DescribeThemeAliasRequestRequestTypeDef = TypedDict(
    "DescribeThemeAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "AliasName": str,
    },
)

DescribeThemePermissionsRequestRequestTypeDef = TypedDict(
    "DescribeThemePermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
    },
)

DescribeThemeRequestRequestTypeDef = TypedDict(
    "DescribeThemeRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "VersionNumber": NotRequired[int],
        "AliasName": NotRequired[str],
    },
)

DescribeTopicPermissionsRequestRequestTypeDef = TypedDict(
    "DescribeTopicPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TopicId": str,
    },
)

DescribeTopicRefreshRequestRequestTypeDef = TypedDict(
    "DescribeTopicRefreshRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TopicId": str,
        "RefreshId": str,
    },
)

TopicRefreshDetailsTypeDef = TypedDict(
    "TopicRefreshDetailsTypeDef",
    {
        "RefreshArn": NotRequired[str],
        "RefreshId": NotRequired[str],
        "RefreshStatus": NotRequired[TopicRefreshStatusType],
    },
)

DescribeTopicRefreshScheduleRequestRequestTypeDef = TypedDict(
    "DescribeTopicRefreshScheduleRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TopicId": str,
        "DatasetId": str,
    },
)

DescribeTopicRequestRequestTypeDef = TypedDict(
    "DescribeTopicRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TopicId": str,
    },
)

DescribeUserRequestRequestTypeDef = TypedDict(
    "DescribeUserRequestRequestTypeDef",
    {
        "UserName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "Arn": NotRequired[str],
        "UserName": NotRequired[str],
        "Email": NotRequired[str],
        "Role": NotRequired[UserRoleType],
        "IdentityType": NotRequired[IdentityTypeType],
        "Active": NotRequired[bool],
        "PrincipalId": NotRequired[str],
        "CustomPermissionsName": NotRequired[str],
        "ExternalLoginFederationProviderType": NotRequired[str],
        "ExternalLoginFederationProviderUrl": NotRequired[str],
        "ExternalLoginId": NotRequired[str],
    },
)

DescribeVPCConnectionRequestRequestTypeDef = TypedDict(
    "DescribeVPCConnectionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "VPCConnectionId": str,
    },
)

NegativeFormatTypeDef = TypedDict(
    "NegativeFormatTypeDef",
    {
        "Prefix": NotRequired[str],
        "Suffix": NotRequired[str],
    },
)

DonutCenterOptionsTypeDef = TypedDict(
    "DonutCenterOptionsTypeDef",
    {
        "LabelVisibility": NotRequired[VisibilityType],
    },
)

ListControlSelectAllOptionsTypeDef = TypedDict(
    "ListControlSelectAllOptionsTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
    },
)

ErrorInfoTypeDef = TypedDict(
    "ErrorInfoTypeDef",
    {
        "Type": NotRequired[IngestionErrorTypeType],
        "Message": NotRequired[str],
    },
)

ExcludePeriodConfigurationTypeDef = TypedDict(
    "ExcludePeriodConfigurationTypeDef",
    {
        "Amount": int,
        "Granularity": TimeGranularityType,
        "Status": NotRequired[WidgetStatusType],
    },
)

FieldSortTypeDef = TypedDict(
    "FieldSortTypeDef",
    {
        "FieldId": str,
        "Direction": SortDirectionType,
    },
)

FieldTooltipItemTypeDef = TypedDict(
    "FieldTooltipItemTypeDef",
    {
        "FieldId": str,
        "Label": NotRequired[str],
        "Visibility": NotRequired[VisibilityType],
    },
)

GeospatialMapStyleOptionsTypeDef = TypedDict(
    "GeospatialMapStyleOptionsTypeDef",
    {
        "BaseMapStyle": NotRequired[BaseMapStyleTypeType],
    },
)

FilterSelectableValuesTypeDef = TypedDict(
    "FilterSelectableValuesTypeDef",
    {
        "Values": NotRequired[Sequence[str]],
    },
)

SameSheetTargetVisualConfigurationTypeDef = TypedDict(
    "SameSheetTargetVisualConfigurationTypeDef",
    {
        "TargetVisuals": NotRequired[Sequence[str]],
        "TargetVisualOptions": NotRequired[Literal["ALL_VISUALS"]],
    },
)

FilterOperationTypeDef = TypedDict(
    "FilterOperationTypeDef",
    {
        "ConditionExpression": str,
    },
)

FolderSearchFilterTypeDef = TypedDict(
    "FolderSearchFilterTypeDef",
    {
        "Operator": NotRequired[FilterOperatorType],
        "Name": NotRequired[FolderFilterAttributeType],
        "Value": NotRequired[str],
    },
)

FolderSummaryTypeDef = TypedDict(
    "FolderSummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "FolderId": NotRequired[str],
        "Name": NotRequired[str],
        "FolderType": NotRequired[Literal["SHARED"]],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
        "SharingModel": NotRequired[SharingModelType],
    },
)

FontSizeTypeDef = TypedDict(
    "FontSizeTypeDef",
    {
        "Relative": NotRequired[RelativeFontSizeType],
    },
)

FontWeightTypeDef = TypedDict(
    "FontWeightTypeDef",
    {
        "Name": NotRequired[FontWeightNameType],
    },
)

FontTypeDef = TypedDict(
    "FontTypeDef",
    {
        "FontFamily": NotRequired[str],
    },
)

TimeBasedForecastPropertiesTypeDef = TypedDict(
    "TimeBasedForecastPropertiesTypeDef",
    {
        "PeriodsForward": NotRequired[int],
        "PeriodsBackward": NotRequired[int],
        "UpperBoundary": NotRequired[float],
        "LowerBoundary": NotRequired[float],
        "PredictionInterval": NotRequired[int],
        "Seasonality": NotRequired[int],
    },
)

FreeFormLayoutScreenCanvasSizeOptionsTypeDef = TypedDict(
    "FreeFormLayoutScreenCanvasSizeOptionsTypeDef",
    {
        "OptimizedViewPortWidth": str,
    },
)

FreeFormLayoutElementBackgroundStyleTypeDef = TypedDict(
    "FreeFormLayoutElementBackgroundStyleTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
        "Color": NotRequired[str],
    },
)

FreeFormLayoutElementBorderStyleTypeDef = TypedDict(
    "FreeFormLayoutElementBorderStyleTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
        "Color": NotRequired[str],
    },
)

LoadingAnimationTypeDef = TypedDict(
    "LoadingAnimationTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
    },
)

SessionTagTypeDef = TypedDict(
    "SessionTagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

GeospatialCoordinateBoundsTypeDef = TypedDict(
    "GeospatialCoordinateBoundsTypeDef",
    {
        "North": float,
        "South": float,
        "West": float,
        "East": float,
    },
)

GeospatialHeatmapDataColorTypeDef = TypedDict(
    "GeospatialHeatmapDataColorTypeDef",
    {
        "Color": str,
    },
)

GetDashboardEmbedUrlRequestRequestTypeDef = TypedDict(
    "GetDashboardEmbedUrlRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "IdentityType": EmbeddingIdentityTypeType,
        "SessionLifetimeInMinutes": NotRequired[int],
        "UndoRedoDisabled": NotRequired[bool],
        "ResetDisabled": NotRequired[bool],
        "StatePersistenceEnabled": NotRequired[bool],
        "UserArn": NotRequired[str],
        "Namespace": NotRequired[str],
        "AdditionalDashboardIds": NotRequired[Sequence[str]],
    },
)

GetSessionEmbedUrlRequestRequestTypeDef = TypedDict(
    "GetSessionEmbedUrlRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "EntryPoint": NotRequired[str],
        "SessionLifetimeInMinutes": NotRequired[int],
        "UserArn": NotRequired[str],
    },
)

TableBorderOptionsTypeDef = TypedDict(
    "TableBorderOptionsTypeDef",
    {
        "Color": NotRequired[str],
        "Thickness": NotRequired[int],
        "Style": NotRequired[TableBorderStyleType],
    },
)

GradientStopTypeDef = TypedDict(
    "GradientStopTypeDef",
    {
        "GradientOffset": float,
        "DataValue": NotRequired[float],
        "Color": NotRequired[str],
    },
)

GridLayoutScreenCanvasSizeOptionsTypeDef = TypedDict(
    "GridLayoutScreenCanvasSizeOptionsTypeDef",
    {
        "ResizeOption": ResizeOptionType,
        "OptimizedViewPortWidth": NotRequired[str],
    },
)

GridLayoutElementTypeDef = TypedDict(
    "GridLayoutElementTypeDef",
    {
        "ElementId": str,
        "ElementType": LayoutElementTypeType,
        "ColumnSpan": int,
        "RowSpan": int,
        "ColumnIndex": NotRequired[int],
        "RowIndex": NotRequired[int],
    },
)

GroupSearchFilterTypeDef = TypedDict(
    "GroupSearchFilterTypeDef",
    {
        "Operator": Literal["StartsWith"],
        "Name": Literal["GROUP_NAME"],
        "Value": str,
    },
)

GutterStyleTypeDef = TypedDict(
    "GutterStyleTypeDef",
    {
        "Show": NotRequired[bool],
    },
)

IAMPolicyAssignmentSummaryTypeDef = TypedDict(
    "IAMPolicyAssignmentSummaryTypeDef",
    {
        "AssignmentName": NotRequired[str],
        "AssignmentStatus": NotRequired[AssignmentStatusType],
    },
)

LookbackWindowTypeDef = TypedDict(
    "LookbackWindowTypeDef",
    {
        "ColumnName": str,
        "Size": int,
        "SizeUnit": LookbackWindowSizeUnitType,
    },
)

QueueInfoTypeDef = TypedDict(
    "QueueInfoTypeDef",
    {
        "WaitingOnIngestion": str,
        "QueuedIngestion": str,
    },
)

RowInfoTypeDef = TypedDict(
    "RowInfoTypeDef",
    {
        "RowsIngested": NotRequired[int],
        "RowsDropped": NotRequired[int],
        "TotalRowsInDataset": NotRequired[int],
    },
)

IntegerDatasetParameterDefaultValuesTypeDef = TypedDict(
    "IntegerDatasetParameterDefaultValuesTypeDef",
    {
        "StaticValues": NotRequired[Sequence[int]],
    },
)

IntegerValueWhenUnsetConfigurationTypeDef = TypedDict(
    "IntegerValueWhenUnsetConfigurationTypeDef",
    {
        "ValueWhenUnsetOption": NotRequired[ValueWhenUnsetOptionType],
        "CustomValue": NotRequired[int],
    },
)

IntegerParameterTypeDef = TypedDict(
    "IntegerParameterTypeDef",
    {
        "Name": str,
        "Values": Sequence[int],
    },
)

JoinKeyPropertiesTypeDef = TypedDict(
    "JoinKeyPropertiesTypeDef",
    {
        "UniqueKey": NotRequired[bool],
    },
)

KPISparklineOptionsTypeDef = TypedDict(
    "KPISparklineOptionsTypeDef",
    {
        "Type": KPISparklineTypeType,
        "Visibility": NotRequired[VisibilityType],
        "Color": NotRequired[str],
        "TooltipVisibility": NotRequired[VisibilityType],
    },
)

ProgressBarOptionsTypeDef = TypedDict(
    "ProgressBarOptionsTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
    },
)

SecondaryValueOptionsTypeDef = TypedDict(
    "SecondaryValueOptionsTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
    },
)

TrendArrowOptionsTypeDef = TypedDict(
    "TrendArrowOptionsTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
    },
)

KPIVisualStandardLayoutTypeDef = TypedDict(
    "KPIVisualStandardLayoutTypeDef",
    {
        "Type": KPIVisualStandardLayoutTypeType,
    },
)

LineChartLineStyleSettingsTypeDef = TypedDict(
    "LineChartLineStyleSettingsTypeDef",
    {
        "LineVisibility": NotRequired[VisibilityType],
        "LineInterpolation": NotRequired[LineInterpolationType],
        "LineStyle": NotRequired[LineChartLineStyleType],
        "LineWidth": NotRequired[str],
    },
)

LineChartMarkerStyleSettingsTypeDef = TypedDict(
    "LineChartMarkerStyleSettingsTypeDef",
    {
        "MarkerVisibility": NotRequired[VisibilityType],
        "MarkerShape": NotRequired[LineChartMarkerShapeType],
        "MarkerSize": NotRequired[str],
        "MarkerColor": NotRequired[str],
    },
)

MissingDataConfigurationTypeDef = TypedDict(
    "MissingDataConfigurationTypeDef",
    {
        "TreatmentOption": NotRequired[MissingDataTreatmentOptionType],
    },
)

ListAnalysesRequestRequestTypeDef = TypedDict(
    "ListAnalysesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListAssetBundleExportJobsRequestRequestTypeDef = TypedDict(
    "ListAssetBundleExportJobsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListAssetBundleImportJobsRequestRequestTypeDef = TypedDict(
    "ListAssetBundleImportJobsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListControlSearchOptionsTypeDef = TypedDict(
    "ListControlSearchOptionsTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
    },
)

ListDashboardVersionsRequestRequestTypeDef = TypedDict(
    "ListDashboardVersionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListDashboardsRequestRequestTypeDef = TypedDict(
    "ListDashboardsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListDataSetsRequestRequestTypeDef = TypedDict(
    "ListDataSetsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListDataSourcesRequestRequestTypeDef = TypedDict(
    "ListDataSourcesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListFolderMembersRequestRequestTypeDef = TypedDict(
    "ListFolderMembersRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

MemberIdArnPairTypeDef = TypedDict(
    "MemberIdArnPairTypeDef",
    {
        "MemberId": NotRequired[str],
        "MemberArn": NotRequired[str],
    },
)

ListFoldersRequestRequestTypeDef = TypedDict(
    "ListFoldersRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListGroupMembershipsRequestRequestTypeDef = TypedDict(
    "ListGroupMembershipsRequestRequestTypeDef",
    {
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListGroupsRequestRequestTypeDef = TypedDict(
    "ListGroupsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListIAMPolicyAssignmentsForUserRequestRequestTypeDef = TypedDict(
    "ListIAMPolicyAssignmentsForUserRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "UserName": str,
        "Namespace": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListIAMPolicyAssignmentsRequestRequestTypeDef = TypedDict(
    "ListIAMPolicyAssignmentsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
        "AssignmentStatus": NotRequired[AssignmentStatusType],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListIngestionsRequestRequestTypeDef = TypedDict(
    "ListIngestionsRequestRequestTypeDef",
    {
        "DataSetId": str,
        "AwsAccountId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListNamespacesRequestRequestTypeDef = TypedDict(
    "ListNamespacesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListRefreshSchedulesRequestRequestTypeDef = TypedDict(
    "ListRefreshSchedulesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

ListTemplateAliasesRequestRequestTypeDef = TypedDict(
    "ListTemplateAliasesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListTemplateVersionsRequestRequestTypeDef = TypedDict(
    "ListTemplateVersionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

TemplateVersionSummaryTypeDef = TypedDict(
    "TemplateVersionSummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "VersionNumber": NotRequired[int],
        "CreatedTime": NotRequired[datetime],
        "Status": NotRequired[ResourceStatusType],
        "Description": NotRequired[str],
    },
)

ListTemplatesRequestRequestTypeDef = TypedDict(
    "ListTemplatesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

TemplateSummaryTypeDef = TypedDict(
    "TemplateSummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "TemplateId": NotRequired[str],
        "Name": NotRequired[str],
        "LatestVersionNumber": NotRequired[int],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
    },
)

ListThemeAliasesRequestRequestTypeDef = TypedDict(
    "ListThemeAliasesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListThemeVersionsRequestRequestTypeDef = TypedDict(
    "ListThemeVersionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ThemeVersionSummaryTypeDef = TypedDict(
    "ThemeVersionSummaryTypeDef",
    {
        "VersionNumber": NotRequired[int],
        "Arn": NotRequired[str],
        "Description": NotRequired[str],
        "CreatedTime": NotRequired[datetime],
        "Status": NotRequired[ResourceStatusType],
    },
)

ListThemesRequestRequestTypeDef = TypedDict(
    "ListThemesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Type": NotRequired[ThemeTypeType],
    },
)

ThemeSummaryTypeDef = TypedDict(
    "ThemeSummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "ThemeId": NotRequired[str],
        "LatestVersionNumber": NotRequired[int],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
    },
)

ListTopicRefreshSchedulesRequestRequestTypeDef = TypedDict(
    "ListTopicRefreshSchedulesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TopicId": str,
    },
)

ListTopicsRequestRequestTypeDef = TypedDict(
    "ListTopicsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

TopicSummaryTypeDef = TypedDict(
    "TopicSummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "TopicId": NotRequired[str],
        "Name": NotRequired[str],
    },
)

ListUserGroupsRequestRequestTypeDef = TypedDict(
    "ListUserGroupsRequestRequestTypeDef",
    {
        "UserName": str,
        "AwsAccountId": str,
        "Namespace": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListUsersRequestRequestTypeDef = TypedDict(
    "ListUsersRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListVPCConnectionsRequestRequestTypeDef = TypedDict(
    "ListVPCConnectionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

LongFormatTextTypeDef = TypedDict(
    "LongFormatTextTypeDef",
    {
        "PlainText": NotRequired[str],
        "RichText": NotRequired[str],
    },
)

ManifestFileLocationTypeDef = TypedDict(
    "ManifestFileLocationTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)

MarginStyleTypeDef = TypedDict(
    "MarginStyleTypeDef",
    {
        "Show": NotRequired[bool],
    },
)

NamedEntityDefinitionMetricTypeDef = TypedDict(
    "NamedEntityDefinitionMetricTypeDef",
    {
        "Aggregation": NotRequired[NamedEntityAggTypeType],
        "AggregationFunctionParameters": NotRequired[Mapping[str, str]],
    },
)

NamespaceErrorTypeDef = TypedDict(
    "NamespaceErrorTypeDef",
    {
        "Type": NotRequired[NamespaceErrorTypeType],
        "Message": NotRequired[str],
    },
)

NetworkInterfaceTypeDef = TypedDict(
    "NetworkInterfaceTypeDef",
    {
        "SubnetId": NotRequired[str],
        "AvailabilityZone": NotRequired[str],
        "ErrorMessage": NotRequired[str],
        "Status": NotRequired[NetworkInterfaceStatusType],
        "NetworkInterfaceId": NotRequired[str],
    },
)

NumericRangeFilterValueTypeDef = TypedDict(
    "NumericRangeFilterValueTypeDef",
    {
        "StaticValue": NotRequired[float],
        "Parameter": NotRequired[str],
    },
)

ThousandSeparatorOptionsTypeDef = TypedDict(
    "ThousandSeparatorOptionsTypeDef",
    {
        "Symbol": NotRequired[NumericSeparatorSymbolType],
        "Visibility": NotRequired[VisibilityType],
    },
)

PercentileAggregationTypeDef = TypedDict(
    "PercentileAggregationTypeDef",
    {
        "PercentileValue": NotRequired[float],
    },
)

StringParameterTypeDef = TypedDict(
    "StringParameterTypeDef",
    {
        "Name": str,
        "Values": Sequence[str],
    },
)

PercentVisibleRangeTypeDef = TypedDict(
    "PercentVisibleRangeTypeDef",
    {
        "From": NotRequired[float],
        "To": NotRequired[float],
    },
)

PivotTableConditionalFormattingScopeTypeDef = TypedDict(
    "PivotTableConditionalFormattingScopeTypeDef",
    {
        "Role": NotRequired[PivotTableConditionalFormattingScopeRoleType],
    },
)

PivotTablePaginatedReportOptionsTypeDef = TypedDict(
    "PivotTablePaginatedReportOptionsTypeDef",
    {
        "VerticalOverflowVisibility": NotRequired[VisibilityType],
        "OverflowColumnHeaderVisibility": NotRequired[VisibilityType],
    },
)

PivotTableFieldOptionTypeDef = TypedDict(
    "PivotTableFieldOptionTypeDef",
    {
        "FieldId": str,
        "CustomLabel": NotRequired[str],
        "Visibility": NotRequired[VisibilityType],
    },
)

PivotTableFieldSubtotalOptionsTypeDef = TypedDict(
    "PivotTableFieldSubtotalOptionsTypeDef",
    {
        "FieldId": NotRequired[str],
    },
)

PivotTableRowsLabelOptionsTypeDef = TypedDict(
    "PivotTableRowsLabelOptionsTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
        "CustomLabel": NotRequired[str],
    },
)

RowAlternateColorOptionsTypeDef = TypedDict(
    "RowAlternateColorOptionsTypeDef",
    {
        "Status": NotRequired[WidgetStatusType],
        "RowAlternateColors": NotRequired[Sequence[str]],
        "UsePrimaryBackgroundColor": NotRequired[WidgetStatusType],
    },
)

ProjectOperationTypeDef = TypedDict(
    "ProjectOperationTypeDef",
    {
        "ProjectedColumns": Sequence[str],
    },
)

RadarChartAreaStyleSettingsTypeDef = TypedDict(
    "RadarChartAreaStyleSettingsTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
    },
)

RangeConstantTypeDef = TypedDict(
    "RangeConstantTypeDef",
    {
        "Minimum": NotRequired[str],
        "Maximum": NotRequired[str],
    },
)

RedshiftIAMParametersPaginatorTypeDef = TypedDict(
    "RedshiftIAMParametersPaginatorTypeDef",
    {
        "RoleArn": str,
        "DatabaseUser": str,
        "DatabaseGroups": NotRequired[List[str]],
        "AutoCreateDatabaseUser": NotRequired[bool],
    },
)

RedshiftIAMParametersTypeDef = TypedDict(
    "RedshiftIAMParametersTypeDef",
    {
        "RoleArn": str,
        "DatabaseUser": str,
        "DatabaseGroups": NotRequired[Sequence[str]],
        "AutoCreateDatabaseUser": NotRequired[bool],
    },
)

ReferenceLineCustomLabelConfigurationTypeDef = TypedDict(
    "ReferenceLineCustomLabelConfigurationTypeDef",
    {
        "CustomLabel": str,
    },
)

ReferenceLineStaticDataConfigurationTypeDef = TypedDict(
    "ReferenceLineStaticDataConfigurationTypeDef",
    {
        "Value": float,
    },
)

ReferenceLineStyleConfigurationTypeDef = TypedDict(
    "ReferenceLineStyleConfigurationTypeDef",
    {
        "Pattern": NotRequired[ReferenceLinePatternTypeType],
        "Color": NotRequired[str],
    },
)

ScheduleRefreshOnEntityTypeDef = TypedDict(
    "ScheduleRefreshOnEntityTypeDef",
    {
        "DayOfWeek": NotRequired[DayOfWeekType],
        "DayOfMonth": NotRequired[str],
    },
)

StatePersistenceConfigurationsTypeDef = TypedDict(
    "StatePersistenceConfigurationsTypeDef",
    {
        "Enabled": bool,
    },
)

RegisteredUserQSearchBarEmbeddingConfigurationTypeDef = TypedDict(
    "RegisteredUserQSearchBarEmbeddingConfigurationTypeDef",
    {
        "InitialTopicId": NotRequired[str],
    },
)

RenameColumnOperationTypeDef = TypedDict(
    "RenameColumnOperationTypeDef",
    {
        "ColumnName": str,
        "NewColumnName": str,
    },
)

RestoreAnalysisRequestRequestTypeDef = TypedDict(
    "RestoreAnalysisRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
    },
)

RowLevelPermissionTagRuleTypeDef = TypedDict(
    "RowLevelPermissionTagRuleTypeDef",
    {
        "TagKey": str,
        "ColumnName": str,
        "TagMultiValueDelimiter": NotRequired[str],
        "MatchAllValue": NotRequired[str],
    },
)

S3BucketConfigurationTypeDef = TypedDict(
    "S3BucketConfigurationTypeDef",
    {
        "BucketName": str,
        "BucketPrefix": str,
        "BucketRegion": str,
    },
)

UploadSettingsTypeDef = TypedDict(
    "UploadSettingsTypeDef",
    {
        "Format": NotRequired[FileFormatType],
        "StartFromRow": NotRequired[int],
        "ContainsHeader": NotRequired[bool],
        "TextQualifier": NotRequired[TextQualifierType],
        "Delimiter": NotRequired[str],
    },
)

SectionAfterPageBreakTypeDef = TypedDict(
    "SectionAfterPageBreakTypeDef",
    {
        "Status": NotRequired[SectionPageBreakStatusType],
    },
)

SpacingTypeDef = TypedDict(
    "SpacingTypeDef",
    {
        "Top": NotRequired[str],
        "Bottom": NotRequired[str],
        "Left": NotRequired[str],
        "Right": NotRequired[str],
    },
)

SheetVisualScopingConfigurationTypeDef = TypedDict(
    "SheetVisualScopingConfigurationTypeDef",
    {
        "SheetId": str,
        "Scope": FilterVisualScopeType,
        "VisualIds": NotRequired[Sequence[str]],
    },
)

SemanticEntityTypeTypeDef = TypedDict(
    "SemanticEntityTypeTypeDef",
    {
        "TypeName": NotRequired[str],
        "SubTypeName": NotRequired[str],
        "TypeParameters": NotRequired[Mapping[str, str]],
    },
)

SemanticTypeTypeDef = TypedDict(
    "SemanticTypeTypeDef",
    {
        "TypeName": NotRequired[str],
        "SubTypeName": NotRequired[str],
        "TypeParameters": NotRequired[Mapping[str, str]],
        "TruthyCellValue": NotRequired[str],
        "TruthyCellValueSynonyms": NotRequired[Sequence[str]],
        "FalseyCellValue": NotRequired[str],
        "FalseyCellValueSynonyms": NotRequired[Sequence[str]],
    },
)

SheetTextBoxTypeDef = TypedDict(
    "SheetTextBoxTypeDef",
    {
        "SheetTextBoxId": str,
        "Content": NotRequired[str],
    },
)

SheetElementConfigurationOverridesTypeDef = TypedDict(
    "SheetElementConfigurationOverridesTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
    },
)

ShortFormatTextTypeDef = TypedDict(
    "ShortFormatTextTypeDef",
    {
        "PlainText": NotRequired[str],
        "RichText": NotRequired[str],
    },
)

SmallMultiplesAxisPropertiesTypeDef = TypedDict(
    "SmallMultiplesAxisPropertiesTypeDef",
    {
        "Scale": NotRequired[SmallMultiplesAxisScaleType],
        "Placement": NotRequired[SmallMultiplesAxisPlacementType],
    },
)

SnapshotAnonymousUserRedactedTypeDef = TypedDict(
    "SnapshotAnonymousUserRedactedTypeDef",
    {
        "RowLevelPermissionTagKeys": NotRequired[List[str]],
    },
)

SnapshotFileSheetSelectionTypeDef = TypedDict(
    "SnapshotFileSheetSelectionTypeDef",
    {
        "SheetId": str,
        "SelectionScope": SnapshotFileSheetSelectionScopeType,
        "VisualIds": NotRequired[List[str]],
    },
)

SnapshotJobResultErrorInfoTypeDef = TypedDict(
    "SnapshotJobResultErrorInfoTypeDef",
    {
        "ErrorMessage": NotRequired[str],
        "ErrorType": NotRequired[str],
    },
)

StringDatasetParameterDefaultValuesTypeDef = TypedDict(
    "StringDatasetParameterDefaultValuesTypeDef",
    {
        "StaticValues": NotRequired[Sequence[str]],
    },
)

StringValueWhenUnsetConfigurationTypeDef = TypedDict(
    "StringValueWhenUnsetConfigurationTypeDef",
    {
        "ValueWhenUnsetOption": NotRequired[ValueWhenUnsetOptionType],
        "CustomValue": NotRequired[str],
    },
)

TableStyleTargetTypeDef = TypedDict(
    "TableStyleTargetTypeDef",
    {
        "CellType": StyledCellTypeType,
    },
)

TableCellImageSizingConfigurationTypeDef = TypedDict(
    "TableCellImageSizingConfigurationTypeDef",
    {
        "TableCellImageScalingConfiguration": NotRequired[TableCellImageScalingConfigurationType],
    },
)

TablePaginatedReportOptionsTypeDef = TypedDict(
    "TablePaginatedReportOptionsTypeDef",
    {
        "VerticalOverflowVisibility": NotRequired[VisibilityType],
        "OverflowColumnHeaderVisibility": NotRequired[VisibilityType],
    },
)

TableFieldCustomIconContentTypeDef = TypedDict(
    "TableFieldCustomIconContentTypeDef",
    {
        "Icon": NotRequired[Literal["LINK"]],
    },
)

TablePinnedFieldOptionsTypeDef = TypedDict(
    "TablePinnedFieldOptionsTypeDef",
    {
        "PinnedLeftFields": NotRequired[Sequence[str]],
    },
)

TemplateSourceTemplateTypeDef = TypedDict(
    "TemplateSourceTemplateTypeDef",
    {
        "Arn": str,
    },
)

TextControlPlaceholderOptionsTypeDef = TypedDict(
    "TextControlPlaceholderOptionsTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
    },
)

UIColorPaletteTypeDef = TypedDict(
    "UIColorPaletteTypeDef",
    {
        "PrimaryForeground": NotRequired[str],
        "PrimaryBackground": NotRequired[str],
        "SecondaryForeground": NotRequired[str],
        "SecondaryBackground": NotRequired[str],
        "Accent": NotRequired[str],
        "AccentForeground": NotRequired[str],
        "Danger": NotRequired[str],
        "DangerForeground": NotRequired[str],
        "Warning": NotRequired[str],
        "WarningForeground": NotRequired[str],
        "Success": NotRequired[str],
        "SuccessForeground": NotRequired[str],
        "Dimension": NotRequired[str],
        "DimensionForeground": NotRequired[str],
        "Measure": NotRequired[str],
        "MeasureForeground": NotRequired[str],
    },
)

ThemeErrorTypeDef = TypedDict(
    "ThemeErrorTypeDef",
    {
        "Type": NotRequired[Literal["INTERNAL_FAILURE"]],
        "Message": NotRequired[str],
    },
)

TopicSingularFilterConstantTypeDef = TypedDict(
    "TopicSingularFilterConstantTypeDef",
    {
        "ConstantType": NotRequired[ConstantTypeType],
        "SingularConstant": NotRequired[str],
    },
)

UntagColumnOperationTypeDef = TypedDict(
    "UntagColumnOperationTypeDef",
    {
        "ColumnName": str,
        "TagNames": Sequence[ColumnTagNameType],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

UpdateAccountSettingsRequestRequestTypeDef = TypedDict(
    "UpdateAccountSettingsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DefaultNamespace": str,
        "NotificationEmail": NotRequired[str],
        "TerminationProtectionEnabled": NotRequired[bool],
    },
)

UpdateDashboardPublishedVersionRequestRequestTypeDef = TypedDict(
    "UpdateDashboardPublishedVersionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "VersionNumber": int,
    },
)

UpdateFolderRequestRequestTypeDef = TypedDict(
    "UpdateFolderRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
        "Name": str,
    },
)

UpdateGroupRequestRequestTypeDef = TypedDict(
    "UpdateGroupRequestRequestTypeDef",
    {
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
        "Description": NotRequired[str],
    },
)

UpdateIAMPolicyAssignmentRequestRequestTypeDef = TypedDict(
    "UpdateIAMPolicyAssignmentRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AssignmentName": str,
        "Namespace": str,
        "AssignmentStatus": NotRequired[AssignmentStatusType],
        "PolicyArn": NotRequired[str],
        "Identities": NotRequired[Mapping[str, Sequence[str]]],
    },
)

UpdateIpRestrictionRequestRequestTypeDef = TypedDict(
    "UpdateIpRestrictionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "IpRestrictionRuleMap": NotRequired[Mapping[str, str]],
        "Enabled": NotRequired[bool],
    },
)

UpdatePublicSharingSettingsRequestRequestTypeDef = TypedDict(
    "UpdatePublicSharingSettingsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "PublicSharingEnabled": NotRequired[bool],
    },
)

UpdateTemplateAliasRequestRequestTypeDef = TypedDict(
    "UpdateTemplateAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "AliasName": str,
        "TemplateVersionNumber": int,
    },
)

UpdateThemeAliasRequestRequestTypeDef = TypedDict(
    "UpdateThemeAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "AliasName": str,
        "ThemeVersionNumber": int,
    },
)

UpdateUserRequestRequestTypeDef = TypedDict(
    "UpdateUserRequestRequestTypeDef",
    {
        "UserName": str,
        "AwsAccountId": str,
        "Namespace": str,
        "Email": str,
        "Role": UserRoleType,
        "CustomPermissionsName": NotRequired[str],
        "UnapplyCustomPermissions": NotRequired[bool],
        "ExternalLoginFederationProviderType": NotRequired[str],
        "CustomFederationProviderUrl": NotRequired[str],
        "ExternalLoginId": NotRequired[str],
    },
)

UpdateVPCConnectionRequestRequestTypeDef = TypedDict(
    "UpdateVPCConnectionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "VPCConnectionId": str,
        "Name": str,
        "SubnetIds": Sequence[str],
        "SecurityGroupIds": Sequence[str],
        "RoleArn": str,
        "DnsResolvers": NotRequired[Sequence[str]],
    },
)

WaterfallChartOptionsTypeDef = TypedDict(
    "WaterfallChartOptionsTypeDef",
    {
        "TotalBarLabel": NotRequired[str],
    },
)

WordCloudOptionsTypeDef = TypedDict(
    "WordCloudOptionsTypeDef",
    {
        "WordOrientation": NotRequired[WordCloudWordOrientationType],
        "WordScaling": NotRequired[WordCloudWordScalingType],
        "CloudLayout": NotRequired[WordCloudCloudLayoutType],
        "WordCasing": NotRequired[WordCloudWordCasingType],
        "WordPadding": NotRequired[WordCloudWordPaddingType],
        "MaximumStringLength": NotRequired[int],
    },
)

UpdateAccountCustomizationRequestRequestTypeDef = TypedDict(
    "UpdateAccountCustomizationRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AccountCustomization": AccountCustomizationTypeDef,
        "Namespace": NotRequired[str],
    },
)

AxisLabelReferenceOptionsTypeDef = TypedDict(
    "AxisLabelReferenceOptionsTypeDef",
    {
        "FieldId": str,
        "Column": ColumnIdentifierTypeDef,
    },
)

CascadingControlSourceTypeDef = TypedDict(
    "CascadingControlSourceTypeDef",
    {
        "SourceSheetControlId": NotRequired[str],
        "ColumnToMatch": NotRequired[ColumnIdentifierTypeDef],
    },
)

CategoryDrillDownFilterTypeDef = TypedDict(
    "CategoryDrillDownFilterTypeDef",
    {
        "Column": ColumnIdentifierTypeDef,
        "CategoryValues": Sequence[str],
    },
)

ContributionAnalysisDefaultTypeDef = TypedDict(
    "ContributionAnalysisDefaultTypeDef",
    {
        "MeasureFieldId": str,
        "ContributorDimensions": Sequence[ColumnIdentifierTypeDef],
    },
)

DynamicDefaultValueTypeDef = TypedDict(
    "DynamicDefaultValueTypeDef",
    {
        "DefaultValueColumn": ColumnIdentifierTypeDef,
        "UserNameColumn": NotRequired[ColumnIdentifierTypeDef],
        "GroupNameColumn": NotRequired[ColumnIdentifierTypeDef],
    },
)

FilterOperationSelectedFieldsConfigurationTypeDef = TypedDict(
    "FilterOperationSelectedFieldsConfigurationTypeDef",
    {
        "SelectedFields": NotRequired[Sequence[str]],
        "SelectedFieldOptions": NotRequired[Literal["ALL_FIELDS"]],
        "SelectedColumns": NotRequired[Sequence[ColumnIdentifierTypeDef]],
    },
)

NumericEqualityDrillDownFilterTypeDef = TypedDict(
    "NumericEqualityDrillDownFilterTypeDef",
    {
        "Column": ColumnIdentifierTypeDef,
        "Value": float,
    },
)

ParameterSelectableValuesTypeDef = TypedDict(
    "ParameterSelectableValuesTypeDef",
    {
        "Values": NotRequired[Sequence[str]],
        "LinkToDataSetColumn": NotRequired[ColumnIdentifierTypeDef],
    },
)

AnalysisErrorTypeDef = TypedDict(
    "AnalysisErrorTypeDef",
    {
        "Type": NotRequired[AnalysisErrorTypeType],
        "Message": NotRequired[str],
        "ViolatedEntities": NotRequired[List[EntityTypeDef]],
    },
)

DashboardErrorTypeDef = TypedDict(
    "DashboardErrorTypeDef",
    {
        "Type": NotRequired[DashboardErrorTypeType],
        "Message": NotRequired[str],
        "ViolatedEntities": NotRequired[List[EntityTypeDef]],
    },
)

TemplateErrorTypeDef = TypedDict(
    "TemplateErrorTypeDef",
    {
        "Type": NotRequired[TemplateErrorTypeType],
        "Message": NotRequired[str],
        "ViolatedEntities": NotRequired[List[EntityTypeDef]],
    },
)

SearchAnalysesRequestRequestTypeDef = TypedDict(
    "SearchAnalysesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[AnalysisSearchFilterTypeDef],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

AnalysisSourceTemplateTypeDef = TypedDict(
    "AnalysisSourceTemplateTypeDef",
    {
        "DataSetReferences": Sequence[DataSetReferenceTypeDef],
        "Arn": str,
    },
)

DashboardSourceTemplateTypeDef = TypedDict(
    "DashboardSourceTemplateTypeDef",
    {
        "DataSetReferences": Sequence[DataSetReferenceTypeDef],
        "Arn": str,
    },
)

TemplateSourceAnalysisTypeDef = TypedDict(
    "TemplateSourceAnalysisTypeDef",
    {
        "Arn": str,
        "DataSetReferences": Sequence[DataSetReferenceTypeDef],
    },
)

AnonymousUserDashboardVisualEmbeddingConfigurationTypeDef = TypedDict(
    "AnonymousUserDashboardVisualEmbeddingConfigurationTypeDef",
    {
        "InitialDashboardVisualId": DashboardVisualIdTypeDef,
    },
)

RegisteredUserDashboardVisualEmbeddingConfigurationTypeDef = TypedDict(
    "RegisteredUserDashboardVisualEmbeddingConfigurationTypeDef",
    {
        "InitialDashboardVisualId": DashboardVisualIdTypeDef,
    },
)

ArcAxisConfigurationTypeDef = TypedDict(
    "ArcAxisConfigurationTypeDef",
    {
        "Range": NotRequired[ArcAxisDisplayRangeTypeDef],
        "ReserveRange": NotRequired[int],
    },
)

AssetBundleCloudFormationOverridePropertyConfigurationTypeDef = TypedDict(
    "AssetBundleCloudFormationOverridePropertyConfigurationTypeDef",
    {
        "ResourceIdOverrideConfiguration": NotRequired[
            AssetBundleExportJobResourceIdOverrideConfigurationTypeDef
        ],
        "VPCConnections": NotRequired[
            List[AssetBundleExportJobVPCConnectionOverridePropertiesTypeDef]
        ],
        "RefreshSchedules": NotRequired[
            List[AssetBundleExportJobRefreshScheduleOverridePropertiesTypeDef]
        ],
        "DataSources": NotRequired[List[AssetBundleExportJobDataSourceOverridePropertiesTypeDef]],
        "DataSets": NotRequired[List[AssetBundleExportJobDataSetOverridePropertiesTypeDef]],
        "Themes": NotRequired[List[AssetBundleExportJobThemeOverridePropertiesTypeDef]],
        "Analyses": NotRequired[List[AssetBundleExportJobAnalysisOverridePropertiesTypeDef]],
        "Dashboards": NotRequired[List[AssetBundleExportJobDashboardOverridePropertiesTypeDef]],
    },
)

AssetBundleImportJobDataSourceCredentialsTypeDef = TypedDict(
    "AssetBundleImportJobDataSourceCredentialsTypeDef",
    {
        "CredentialPair": NotRequired[AssetBundleImportJobDataSourceCredentialPairTypeDef],
        "SecretArn": NotRequired[str],
    },
)

AssetBundleImportSourceTypeDef = TypedDict(
    "AssetBundleImportSourceTypeDef",
    {
        "Body": NotRequired[BlobTypeDef],
        "S3Uri": NotRequired[str],
    },
)

AxisDisplayRangeTypeDef = TypedDict(
    "AxisDisplayRangeTypeDef",
    {
        "MinMax": NotRequired[AxisDisplayMinMaxRangeTypeDef],
        "DataDriven": NotRequired[Mapping[str, Any]],
    },
)

AxisScaleTypeDef = TypedDict(
    "AxisScaleTypeDef",
    {
        "Linear": NotRequired[AxisLinearScaleTypeDef],
        "Logarithmic": NotRequired[AxisLogarithmicScaleTypeDef],
    },
)

HistogramBinOptionsTypeDef = TypedDict(
    "HistogramBinOptionsTypeDef",
    {
        "SelectedBinType": NotRequired[HistogramBinTypeType],
        "BinCount": NotRequired[BinCountOptionsTypeDef],
        "BinWidth": NotRequired[BinWidthOptionsTypeDef],
        "StartValue": NotRequired[float],
    },
)

TileStyleTypeDef = TypedDict(
    "TileStyleTypeDef",
    {
        "Border": NotRequired[BorderStyleTypeDef],
    },
)

BoxPlotOptionsTypeDef = TypedDict(
    "BoxPlotOptionsTypeDef",
    {
        "StyleOptions": NotRequired[BoxPlotStyleOptionsTypeDef],
        "OutlierVisibility": NotRequired[VisibilityType],
        "AllDataPointsVisibility": NotRequired[VisibilityType],
    },
)

CreateColumnsOperationTypeDef = TypedDict(
    "CreateColumnsOperationTypeDef",
    {
        "Columns": Sequence[CalculatedColumnTypeDef],
    },
)

CancelIngestionResponseTypeDef = TypedDict(
    "CancelIngestionResponseTypeDef",
    {
        "Arn": str,
        "IngestionId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAccountCustomizationResponseTypeDef = TypedDict(
    "CreateAccountCustomizationResponseTypeDef",
    {
        "Arn": str,
        "AwsAccountId": str,
        "Namespace": str,
        "AccountCustomization": AccountCustomizationTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAnalysisResponseTypeDef = TypedDict(
    "CreateAnalysisResponseTypeDef",
    {
        "Arn": str,
        "AnalysisId": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDashboardResponseTypeDef = TypedDict(
    "CreateDashboardResponseTypeDef",
    {
        "Arn": str,
        "VersionArn": str,
        "DashboardId": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDataSetResponseTypeDef = TypedDict(
    "CreateDataSetResponseTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "IngestionArn": str,
        "IngestionId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDataSourceResponseTypeDef = TypedDict(
    "CreateDataSourceResponseTypeDef",
    {
        "Arn": str,
        "DataSourceId": str,
        "CreationStatus": ResourceStatusType,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFolderResponseTypeDef = TypedDict(
    "CreateFolderResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "FolderId": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateIAMPolicyAssignmentResponseTypeDef = TypedDict(
    "CreateIAMPolicyAssignmentResponseTypeDef",
    {
        "AssignmentName": str,
        "AssignmentId": str,
        "AssignmentStatus": AssignmentStatusType,
        "PolicyArn": str,
        "Identities": Dict[str, List[str]],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateIngestionResponseTypeDef = TypedDict(
    "CreateIngestionResponseTypeDef",
    {
        "Arn": str,
        "IngestionId": str,
        "IngestionStatus": IngestionStatusType,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateNamespaceResponseTypeDef = TypedDict(
    "CreateNamespaceResponseTypeDef",
    {
        "Arn": str,
        "Name": str,
        "CapacityRegion": str,
        "CreationStatus": NamespaceStatusType,
        "IdentityStore": Literal["QUICKSIGHT"],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRefreshScheduleResponseTypeDef = TypedDict(
    "CreateRefreshScheduleResponseTypeDef",
    {
        "Status": int,
        "RequestId": str,
        "ScheduleId": str,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTemplateResponseTypeDef = TypedDict(
    "CreateTemplateResponseTypeDef",
    {
        "Arn": str,
        "VersionArn": str,
        "TemplateId": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateThemeResponseTypeDef = TypedDict(
    "CreateThemeResponseTypeDef",
    {
        "Arn": str,
        "VersionArn": str,
        "ThemeId": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTopicRefreshScheduleResponseTypeDef = TypedDict(
    "CreateTopicRefreshScheduleResponseTypeDef",
    {
        "TopicId": str,
        "TopicArn": str,
        "DatasetArn": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTopicResponseTypeDef = TypedDict(
    "CreateTopicResponseTypeDef",
    {
        "Arn": str,
        "TopicId": str,
        "RefreshArn": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateVPCConnectionResponseTypeDef = TypedDict(
    "CreateVPCConnectionResponseTypeDef",
    {
        "Arn": str,
        "VPCConnectionId": str,
        "CreationStatus": VPCConnectionResourceStatusType,
        "AvailabilityStatus": VPCConnectionAvailabilityStatusType,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAccountCustomizationResponseTypeDef = TypedDict(
    "DeleteAccountCustomizationResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAccountSubscriptionResponseTypeDef = TypedDict(
    "DeleteAccountSubscriptionResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAnalysisResponseTypeDef = TypedDict(
    "DeleteAnalysisResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "AnalysisId": str,
        "DeletionTime": datetime,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDashboardResponseTypeDef = TypedDict(
    "DeleteDashboardResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "DashboardId": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDataSetRefreshPropertiesResponseTypeDef = TypedDict(
    "DeleteDataSetRefreshPropertiesResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDataSetResponseTypeDef = TypedDict(
    "DeleteDataSetResponseTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDataSourceResponseTypeDef = TypedDict(
    "DeleteDataSourceResponseTypeDef",
    {
        "Arn": str,
        "DataSourceId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFolderMembershipResponseTypeDef = TypedDict(
    "DeleteFolderMembershipResponseTypeDef",
    {
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFolderResponseTypeDef = TypedDict(
    "DeleteFolderResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "FolderId": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteGroupMembershipResponseTypeDef = TypedDict(
    "DeleteGroupMembershipResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteGroupResponseTypeDef = TypedDict(
    "DeleteGroupResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteIAMPolicyAssignmentResponseTypeDef = TypedDict(
    "DeleteIAMPolicyAssignmentResponseTypeDef",
    {
        "AssignmentName": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteNamespaceResponseTypeDef = TypedDict(
    "DeleteNamespaceResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRefreshScheduleResponseTypeDef = TypedDict(
    "DeleteRefreshScheduleResponseTypeDef",
    {
        "Status": int,
        "RequestId": str,
        "ScheduleId": str,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTemplateAliasResponseTypeDef = TypedDict(
    "DeleteTemplateAliasResponseTypeDef",
    {
        "Status": int,
        "TemplateId": str,
        "AliasName": str,
        "Arn": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTemplateResponseTypeDef = TypedDict(
    "DeleteTemplateResponseTypeDef",
    {
        "RequestId": str,
        "Arn": str,
        "TemplateId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteThemeAliasResponseTypeDef = TypedDict(
    "DeleteThemeAliasResponseTypeDef",
    {
        "AliasName": str,
        "Arn": str,
        "RequestId": str,
        "Status": int,
        "ThemeId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteThemeResponseTypeDef = TypedDict(
    "DeleteThemeResponseTypeDef",
    {
        "Arn": str,
        "RequestId": str,
        "Status": int,
        "ThemeId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTopicRefreshScheduleResponseTypeDef = TypedDict(
    "DeleteTopicRefreshScheduleResponseTypeDef",
    {
        "TopicId": str,
        "TopicArn": str,
        "DatasetArn": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTopicResponseTypeDef = TypedDict(
    "DeleteTopicResponseTypeDef",
    {
        "Arn": str,
        "TopicId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteUserByPrincipalIdResponseTypeDef = TypedDict(
    "DeleteUserByPrincipalIdResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteUserResponseTypeDef = TypedDict(
    "DeleteUserResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVPCConnectionResponseTypeDef = TypedDict(
    "DeleteVPCConnectionResponseTypeDef",
    {
        "Arn": str,
        "VPCConnectionId": str,
        "DeletionStatus": VPCConnectionResourceStatusType,
        "AvailabilityStatus": VPCConnectionAvailabilityStatusType,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountCustomizationResponseTypeDef = TypedDict(
    "DescribeAccountCustomizationResponseTypeDef",
    {
        "Arn": str,
        "AwsAccountId": str,
        "Namespace": str,
        "AccountCustomization": AccountCustomizationTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountSettingsResponseTypeDef = TypedDict(
    "DescribeAccountSettingsResponseTypeDef",
    {
        "AccountSettings": AccountSettingsTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountSubscriptionResponseTypeDef = TypedDict(
    "DescribeAccountSubscriptionResponseTypeDef",
    {
        "AccountInfo": AccountInfoTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeIpRestrictionResponseTypeDef = TypedDict(
    "DescribeIpRestrictionResponseTypeDef",
    {
        "AwsAccountId": str,
        "IpRestrictionRuleMap": Dict[str, str],
        "Enabled": bool,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateEmbedUrlForAnonymousUserResponseTypeDef = TypedDict(
    "GenerateEmbedUrlForAnonymousUserResponseTypeDef",
    {
        "EmbedUrl": str,
        "Status": int,
        "RequestId": str,
        "AnonymousUserArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateEmbedUrlForRegisteredUserResponseTypeDef = TypedDict(
    "GenerateEmbedUrlForRegisteredUserResponseTypeDef",
    {
        "EmbedUrl": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDashboardEmbedUrlResponseTypeDef = TypedDict(
    "GetDashboardEmbedUrlResponseTypeDef",
    {
        "EmbedUrl": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSessionEmbedUrlResponseTypeDef = TypedDict(
    "GetSessionEmbedUrlResponseTypeDef",
    {
        "EmbedUrl": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAnalysesResponseTypeDef = TypedDict(
    "ListAnalysesResponseTypeDef",
    {
        "AnalysisSummaryList": List[AnalysisSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssetBundleExportJobsResponseTypeDef = TypedDict(
    "ListAssetBundleExportJobsResponseTypeDef",
    {
        "AssetBundleExportJobSummaryList": List[AssetBundleExportJobSummaryTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssetBundleImportJobsResponseTypeDef = TypedDict(
    "ListAssetBundleImportJobsResponseTypeDef",
    {
        "AssetBundleImportJobSummaryList": List[AssetBundleImportJobSummaryTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListIAMPolicyAssignmentsForUserResponseTypeDef = TypedDict(
    "ListIAMPolicyAssignmentsForUserResponseTypeDef",
    {
        "ActiveAssignments": List[ActiveIAMPolicyAssignmentTypeDef],
        "RequestId": str,
        "NextToken": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutDataSetRefreshPropertiesResponseTypeDef = TypedDict(
    "PutDataSetRefreshPropertiesResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RestoreAnalysisResponseTypeDef = TypedDict(
    "RestoreAnalysisResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "AnalysisId": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchAnalysesResponseTypeDef = TypedDict(
    "SearchAnalysesResponseTypeDef",
    {
        "AnalysisSummaryList": List[AnalysisSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartAssetBundleExportJobResponseTypeDef = TypedDict(
    "StartAssetBundleExportJobResponseTypeDef",
    {
        "Arn": str,
        "AssetBundleExportJobId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartAssetBundleImportJobResponseTypeDef = TypedDict(
    "StartAssetBundleImportJobResponseTypeDef",
    {
        "Arn": str,
        "AssetBundleImportJobId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartDashboardSnapshotJobResponseTypeDef = TypedDict(
    "StartDashboardSnapshotJobResponseTypeDef",
    {
        "Arn": str,
        "SnapshotJobId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceResponseTypeDef = TypedDict(
    "TagResourceResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UntagResourceResponseTypeDef = TypedDict(
    "UntagResourceResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAccountCustomizationResponseTypeDef = TypedDict(
    "UpdateAccountCustomizationResponseTypeDef",
    {
        "Arn": str,
        "AwsAccountId": str,
        "Namespace": str,
        "AccountCustomization": AccountCustomizationTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAccountSettingsResponseTypeDef = TypedDict(
    "UpdateAccountSettingsResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAnalysisResponseTypeDef = TypedDict(
    "UpdateAnalysisResponseTypeDef",
    {
        "Arn": str,
        "AnalysisId": str,
        "UpdateStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDashboardPublishedVersionResponseTypeDef = TypedDict(
    "UpdateDashboardPublishedVersionResponseTypeDef",
    {
        "DashboardId": str,
        "DashboardArn": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDashboardResponseTypeDef = TypedDict(
    "UpdateDashboardResponseTypeDef",
    {
        "Arn": str,
        "VersionArn": str,
        "DashboardId": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDataSetPermissionsResponseTypeDef = TypedDict(
    "UpdateDataSetPermissionsResponseTypeDef",
    {
        "DataSetArn": str,
        "DataSetId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDataSetResponseTypeDef = TypedDict(
    "UpdateDataSetResponseTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "IngestionArn": str,
        "IngestionId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDataSourcePermissionsResponseTypeDef = TypedDict(
    "UpdateDataSourcePermissionsResponseTypeDef",
    {
        "DataSourceArn": str,
        "DataSourceId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDataSourceResponseTypeDef = TypedDict(
    "UpdateDataSourceResponseTypeDef",
    {
        "Arn": str,
        "DataSourceId": str,
        "UpdateStatus": ResourceStatusType,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFolderResponseTypeDef = TypedDict(
    "UpdateFolderResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "FolderId": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateIAMPolicyAssignmentResponseTypeDef = TypedDict(
    "UpdateIAMPolicyAssignmentResponseTypeDef",
    {
        "AssignmentName": str,
        "AssignmentId": str,
        "PolicyArn": str,
        "Identities": Dict[str, List[str]],
        "AssignmentStatus": AssignmentStatusType,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateIpRestrictionResponseTypeDef = TypedDict(
    "UpdateIpRestrictionResponseTypeDef",
    {
        "AwsAccountId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePublicSharingSettingsResponseTypeDef = TypedDict(
    "UpdatePublicSharingSettingsResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRefreshScheduleResponseTypeDef = TypedDict(
    "UpdateRefreshScheduleResponseTypeDef",
    {
        "Status": int,
        "RequestId": str,
        "ScheduleId": str,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTemplateResponseTypeDef = TypedDict(
    "UpdateTemplateResponseTypeDef",
    {
        "TemplateId": str,
        "Arn": str,
        "VersionArn": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateThemeResponseTypeDef = TypedDict(
    "UpdateThemeResponseTypeDef",
    {
        "ThemeId": str,
        "Arn": str,
        "VersionArn": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTopicRefreshScheduleResponseTypeDef = TypedDict(
    "UpdateTopicRefreshScheduleResponseTypeDef",
    {
        "TopicId": str,
        "TopicArn": str,
        "DatasetArn": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTopicResponseTypeDef = TypedDict(
    "UpdateTopicResponseTypeDef",
    {
        "TopicId": str,
        "Arn": str,
        "RefreshArn": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateVPCConnectionResponseTypeDef = TypedDict(
    "UpdateVPCConnectionResponseTypeDef",
    {
        "Arn": str,
        "VPCConnectionId": str,
        "UpdateStatus": VPCConnectionResourceStatusType,
        "AvailabilityStatus": VPCConnectionAvailabilityStatusType,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CategoryFilterConfigurationTypeDef = TypedDict(
    "CategoryFilterConfigurationTypeDef",
    {
        "FilterListConfiguration": NotRequired[FilterListConfigurationTypeDef],
        "CustomFilterListConfiguration": NotRequired[CustomFilterListConfigurationTypeDef],
        "CustomFilterConfiguration": NotRequired[CustomFilterConfigurationTypeDef],
    },
)

ClusterMarkerTypeDef = TypedDict(
    "ClusterMarkerTypeDef",
    {
        "SimpleClusterMarker": NotRequired[SimpleClusterMarkerTypeDef],
    },
)

TopicCategoryFilterConstantTypeDef = TypedDict(
    "TopicCategoryFilterConstantTypeDef",
    {
        "ConstantType": NotRequired[ConstantTypeType],
        "SingularConstant": NotRequired[str],
        "CollectiveConstant": NotRequired[CollectiveConstantTypeDef],
    },
)

ColorScaleTypeDef = TypedDict(
    "ColorScaleTypeDef",
    {
        "Colors": Sequence[DataColorTypeDef],
        "ColorFillType": ColorFillTypeType,
        "NullValueColor": NotRequired[DataColorTypeDef],
    },
)

ColorsConfigurationTypeDef = TypedDict(
    "ColorsConfigurationTypeDef",
    {
        "CustomColors": NotRequired[Sequence[CustomColorTypeDef]],
    },
)

ColumnTagTypeDef = TypedDict(
    "ColumnTagTypeDef",
    {
        "ColumnGeographicRole": NotRequired[GeoSpatialDataRoleType],
        "ColumnDescription": NotRequired[ColumnDescriptionTypeDef],
    },
)

ColumnGroupSchemaTypeDef = TypedDict(
    "ColumnGroupSchemaTypeDef",
    {
        "Name": NotRequired[str],
        "ColumnGroupColumnSchemaList": NotRequired[Sequence[ColumnGroupColumnSchemaTypeDef]],
    },
)

ColumnGroupTypeDef = TypedDict(
    "ColumnGroupTypeDef",
    {
        "GeoSpatialColumnGroup": NotRequired[GeoSpatialColumnGroupTypeDef],
    },
)

DataSetSchemaTypeDef = TypedDict(
    "DataSetSchemaTypeDef",
    {
        "ColumnSchemaList": NotRequired[Sequence[ColumnSchemaTypeDef]],
    },
)

ConditionalFormattingCustomIconConditionTypeDef = TypedDict(
    "ConditionalFormattingCustomIconConditionTypeDef",
    {
        "Expression": str,
        "IconOptions": ConditionalFormattingCustomIconOptionsTypeDef,
        "Color": NotRequired[str],
        "DisplayConfiguration": NotRequired[ConditionalFormattingIconDisplayConfigurationTypeDef],
    },
)

CreateAccountCustomizationRequestRequestTypeDef = TypedDict(
    "CreateAccountCustomizationRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AccountCustomization": AccountCustomizationTypeDef,
        "Namespace": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

CreateNamespaceRequestRequestTypeDef = TypedDict(
    "CreateNamespaceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
        "IdentityStore": Literal["QUICKSIGHT"],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

CreateVPCConnectionRequestRequestTypeDef = TypedDict(
    "CreateVPCConnectionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "VPCConnectionId": str,
        "Name": str,
        "SubnetIds": Sequence[str],
        "SecurityGroupIds": Sequence[str],
        "RoleArn": str,
        "DnsResolvers": NotRequired[Sequence[str]],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterUserRequestRequestTypeDef = TypedDict(
    "RegisterUserRequestRequestTypeDef",
    {
        "IdentityType": IdentityTypeType,
        "Email": str,
        "UserRole": UserRoleType,
        "AwsAccountId": str,
        "Namespace": str,
        "IamArn": NotRequired[str],
        "SessionName": NotRequired[str],
        "UserName": NotRequired[str],
        "CustomPermissionsName": NotRequired[str],
        "ExternalLoginFederationProviderType": NotRequired[str],
        "CustomFederationProviderUrl": NotRequired[str],
        "ExternalLoginId": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateAccountSubscriptionResponseTypeDef = TypedDict(
    "CreateAccountSubscriptionResponseTypeDef",
    {
        "SignupResponse": SignupResponseTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFolderRequestRequestTypeDef = TypedDict(
    "CreateFolderRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
        "Name": NotRequired[str],
        "FolderType": NotRequired[Literal["SHARED"]],
        "ParentFolderArn": NotRequired[str],
        "Permissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "SharingModel": NotRequired[SharingModelType],
    },
)

DescribeAnalysisPermissionsResponseTypeDef = TypedDict(
    "DescribeAnalysisPermissionsResponseTypeDef",
    {
        "AnalysisId": str,
        "AnalysisArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDataSetPermissionsResponseTypeDef = TypedDict(
    "DescribeDataSetPermissionsResponseTypeDef",
    {
        "DataSetArn": str,
        "DataSetId": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDataSourcePermissionsResponseTypeDef = TypedDict(
    "DescribeDataSourcePermissionsResponseTypeDef",
    {
        "DataSourceArn": str,
        "DataSourceId": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFolderPermissionsResponseTypeDef = TypedDict(
    "DescribeFolderPermissionsResponseTypeDef",
    {
        "Status": int,
        "FolderId": str,
        "Arn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFolderResolvedPermissionsResponseTypeDef = TypedDict(
    "DescribeFolderResolvedPermissionsResponseTypeDef",
    {
        "Status": int,
        "FolderId": str,
        "Arn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTemplatePermissionsResponseTypeDef = TypedDict(
    "DescribeTemplatePermissionsResponseTypeDef",
    {
        "TemplateId": str,
        "TemplateArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeThemePermissionsResponseTypeDef = TypedDict(
    "DescribeThemePermissionsResponseTypeDef",
    {
        "ThemeId": str,
        "ThemeArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTopicPermissionsResponseTypeDef = TypedDict(
    "DescribeTopicPermissionsResponseTypeDef",
    {
        "TopicId": str,
        "TopicArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LinkSharingConfigurationTypeDef = TypedDict(
    "LinkSharingConfigurationTypeDef",
    {
        "Permissions": NotRequired[List[ResourcePermissionTypeDef]],
    },
)

UpdateAnalysisPermissionsRequestRequestTypeDef = TypedDict(
    "UpdateAnalysisPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
        "GrantPermissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
        "RevokePermissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
    },
)

UpdateAnalysisPermissionsResponseTypeDef = TypedDict(
    "UpdateAnalysisPermissionsResponseTypeDef",
    {
        "AnalysisArn": str,
        "AnalysisId": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDashboardPermissionsRequestRequestTypeDef = TypedDict(
    "UpdateDashboardPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "GrantPermissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
        "RevokePermissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
        "GrantLinkPermissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
        "RevokeLinkPermissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
    },
)

UpdateDataSetPermissionsRequestRequestTypeDef = TypedDict(
    "UpdateDataSetPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
        "GrantPermissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
        "RevokePermissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
    },
)

UpdateDataSourcePermissionsRequestRequestTypeDef = TypedDict(
    "UpdateDataSourcePermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
        "GrantPermissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
        "RevokePermissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
    },
)

UpdateFolderPermissionsRequestRequestTypeDef = TypedDict(
    "UpdateFolderPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
        "GrantPermissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
        "RevokePermissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
    },
)

UpdateFolderPermissionsResponseTypeDef = TypedDict(
    "UpdateFolderPermissionsResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "FolderId": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTemplatePermissionsRequestRequestTypeDef = TypedDict(
    "UpdateTemplatePermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "GrantPermissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
        "RevokePermissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
    },
)

UpdateTemplatePermissionsResponseTypeDef = TypedDict(
    "UpdateTemplatePermissionsResponseTypeDef",
    {
        "TemplateId": str,
        "TemplateArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateThemePermissionsRequestRequestTypeDef = TypedDict(
    "UpdateThemePermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "GrantPermissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
        "RevokePermissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
    },
)

UpdateThemePermissionsResponseTypeDef = TypedDict(
    "UpdateThemePermissionsResponseTypeDef",
    {
        "ThemeId": str,
        "ThemeArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTopicPermissionsRequestRequestTypeDef = TypedDict(
    "UpdateTopicPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TopicId": str,
        "GrantPermissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
        "RevokePermissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
    },
)

UpdateTopicPermissionsResponseTypeDef = TypedDict(
    "UpdateTopicPermissionsResponseTypeDef",
    {
        "TopicId": str,
        "TopicArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DataSetSummaryTypeDef = TypedDict(
    "DataSetSummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "DataSetId": NotRequired[str],
        "Name": NotRequired[str],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
        "ImportMode": NotRequired[DataSetImportModeType],
        "RowLevelPermissionDataSet": NotRequired[RowLevelPermissionDataSetTypeDef],
        "RowLevelPermissionTagConfigurationApplied": NotRequired[bool],
        "ColumnLevelPermissionRulesApplied": NotRequired[bool],
    },
)

CreateFolderMembershipResponseTypeDef = TypedDict(
    "CreateFolderMembershipResponseTypeDef",
    {
        "Status": int,
        "FolderMember": FolderMemberTypeDef,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGroupMembershipResponseTypeDef = TypedDict(
    "CreateGroupMembershipResponseTypeDef",
    {
        "GroupMember": GroupMemberTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGroupMembershipResponseTypeDef = TypedDict(
    "DescribeGroupMembershipResponseTypeDef",
    {
        "GroupMember": GroupMemberTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGroupMembershipsResponseTypeDef = TypedDict(
    "ListGroupMembershipsResponseTypeDef",
    {
        "GroupMemberList": List[GroupMemberTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGroupResponseTypeDef = TypedDict(
    "CreateGroupResponseTypeDef",
    {
        "Group": GroupTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGroupResponseTypeDef = TypedDict(
    "DescribeGroupResponseTypeDef",
    {
        "Group": GroupTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGroupsResponseTypeDef = TypedDict(
    "ListGroupsResponseTypeDef",
    {
        "GroupList": List[GroupTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUserGroupsResponseTypeDef = TypedDict(
    "ListUserGroupsResponseTypeDef",
    {
        "GroupList": List[GroupTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchGroupsResponseTypeDef = TypedDict(
    "SearchGroupsResponseTypeDef",
    {
        "GroupList": List[GroupTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGroupResponseTypeDef = TypedDict(
    "UpdateGroupResponseTypeDef",
    {
        "Group": GroupTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTemplateAliasResponseTypeDef = TypedDict(
    "CreateTemplateAliasResponseTypeDef",
    {
        "TemplateAlias": TemplateAliasTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTemplateAliasResponseTypeDef = TypedDict(
    "DescribeTemplateAliasResponseTypeDef",
    {
        "TemplateAlias": TemplateAliasTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTemplateAliasesResponseTypeDef = TypedDict(
    "ListTemplateAliasesResponseTypeDef",
    {
        "TemplateAliasList": List[TemplateAliasTypeDef],
        "Status": int,
        "RequestId": str,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTemplateAliasResponseTypeDef = TypedDict(
    "UpdateTemplateAliasResponseTypeDef",
    {
        "TemplateAlias": TemplateAliasTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateThemeAliasResponseTypeDef = TypedDict(
    "CreateThemeAliasResponseTypeDef",
    {
        "ThemeAlias": ThemeAliasTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeThemeAliasResponseTypeDef = TypedDict(
    "DescribeThemeAliasResponseTypeDef",
    {
        "ThemeAlias": ThemeAliasTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListThemeAliasesResponseTypeDef = TypedDict(
    "ListThemeAliasesResponseTypeDef",
    {
        "ThemeAliasList": List[ThemeAliasTypeDef],
        "Status": int,
        "RequestId": str,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateThemeAliasResponseTypeDef = TypedDict(
    "UpdateThemeAliasResponseTypeDef",
    {
        "ThemeAlias": ThemeAliasTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CustomActionNavigationOperationTypeDef = TypedDict(
    "CustomActionNavigationOperationTypeDef",
    {
        "LocalNavigationConfiguration": NotRequired[LocalNavigationConfigurationTypeDef],
    },
)

CustomParameterValuesTypeDef = TypedDict(
    "CustomParameterValuesTypeDef",
    {
        "StringValues": NotRequired[Sequence[str]],
        "IntegerValues": NotRequired[Sequence[int]],
        "DecimalValues": NotRequired[Sequence[float]],
        "DateTimeValues": NotRequired[Sequence[TimestampTypeDef]],
    },
)

DateTimeDatasetParameterDefaultValuesTypeDef = TypedDict(
    "DateTimeDatasetParameterDefaultValuesTypeDef",
    {
        "StaticValues": NotRequired[Sequence[TimestampTypeDef]],
    },
)

DateTimeParameterTypeDef = TypedDict(
    "DateTimeParameterTypeDef",
    {
        "Name": str,
        "Values": Sequence[TimestampTypeDef],
    },
)

DateTimeValueWhenUnsetConfigurationTypeDef = TypedDict(
    "DateTimeValueWhenUnsetConfigurationTypeDef",
    {
        "ValueWhenUnsetOption": NotRequired[ValueWhenUnsetOptionType],
        "CustomValue": NotRequired[TimestampTypeDef],
    },
)

NewDefaultValuesTypeDef = TypedDict(
    "NewDefaultValuesTypeDef",
    {
        "StringStaticValues": NotRequired[Sequence[str]],
        "DecimalStaticValues": NotRequired[Sequence[float]],
        "DateTimeStaticValues": NotRequired[Sequence[TimestampTypeDef]],
        "IntegerStaticValues": NotRequired[Sequence[int]],
    },
)

TimeEqualityFilterTypeDef = TypedDict(
    "TimeEqualityFilterTypeDef",
    {
        "FilterId": str,
        "Column": ColumnIdentifierTypeDef,
        "Value": NotRequired[TimestampTypeDef],
        "ParameterName": NotRequired[str],
        "TimeGranularity": NotRequired[TimeGranularityType],
    },
)

TimeRangeDrillDownFilterTypeDef = TypedDict(
    "TimeRangeDrillDownFilterTypeDef",
    {
        "Column": ColumnIdentifierTypeDef,
        "RangeMinimum": TimestampTypeDef,
        "RangeMaximum": TimestampTypeDef,
        "TimeGranularity": TimeGranularityType,
    },
)

TopicRefreshScheduleTypeDef = TypedDict(
    "TopicRefreshScheduleTypeDef",
    {
        "IsEnabled": bool,
        "BasedOnSpiceSchedule": bool,
        "StartingAt": NotRequired[TimestampTypeDef],
        "Timezone": NotRequired[str],
        "RepeatAt": NotRequired[str],
        "TopicScheduleType": NotRequired[TopicScheduleTypeType],
    },
)

WhatIfPointScenarioTypeDef = TypedDict(
    "WhatIfPointScenarioTypeDef",
    {
        "Date": TimestampTypeDef,
        "Value": float,
    },
)

WhatIfRangeScenarioTypeDef = TypedDict(
    "WhatIfRangeScenarioTypeDef",
    {
        "StartDate": TimestampTypeDef,
        "EndDate": TimestampTypeDef,
        "Value": float,
    },
)

CustomSqlTypeDef = TypedDict(
    "CustomSqlTypeDef",
    {
        "DataSourceArn": str,
        "Name": str,
        "SqlQuery": str,
        "Columns": NotRequired[Sequence[InputColumnTypeDef]],
    },
)

RelationalTableTypeDef = TypedDict(
    "RelationalTableTypeDef",
    {
        "DataSourceArn": str,
        "Name": str,
        "InputColumns": Sequence[InputColumnTypeDef],
        "Catalog": NotRequired[str],
        "Schema": NotRequired[str],
    },
)

SearchDashboardsRequestRequestTypeDef = TypedDict(
    "SearchDashboardsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[DashboardSearchFilterTypeDef],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListDashboardsResponseTypeDef = TypedDict(
    "ListDashboardsResponseTypeDef",
    {
        "DashboardSummaryList": List[DashboardSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchDashboardsResponseTypeDef = TypedDict(
    "SearchDashboardsResponseTypeDef",
    {
        "DashboardSummaryList": List[DashboardSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDashboardVersionsResponseTypeDef = TypedDict(
    "ListDashboardVersionsResponseTypeDef",
    {
        "DashboardVersionSummaryList": List[DashboardVersionSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DashboardVisualPublishOptionsTypeDef = TypedDict(
    "DashboardVisualPublishOptionsTypeDef",
    {
        "ExportHiddenFieldsOption": NotRequired[ExportHiddenFieldsOptionTypeDef],
    },
)

TableInlineVisualizationTypeDef = TypedDict(
    "TableInlineVisualizationTypeDef",
    {
        "DataBars": NotRequired[DataBarsOptionsTypeDef],
    },
)

DataLabelTypeTypeDef = TypedDict(
    "DataLabelTypeTypeDef",
    {
        "FieldLabelType": NotRequired[FieldLabelTypeTypeDef],
        "DataPathLabelType": NotRequired[DataPathLabelTypeTypeDef],
        "RangeEndsLabelType": NotRequired[RangeEndsLabelTypeTypeDef],
        "MinimumLabelType": NotRequired[MinimumLabelTypeTypeDef],
        "MaximumLabelType": NotRequired[MaximumLabelTypeTypeDef],
    },
)

DataPathColorTypeDef = TypedDict(
    "DataPathColorTypeDef",
    {
        "Element": DataPathValueTypeDef,
        "Color": str,
        "TimeGranularity": NotRequired[TimeGranularityType],
    },
)

DataPathSortTypeDef = TypedDict(
    "DataPathSortTypeDef",
    {
        "Direction": SortDirectionType,
        "SortPaths": Sequence[DataPathValueTypeDef],
    },
)

PivotTableDataPathOptionTypeDef = TypedDict(
    "PivotTableDataPathOptionTypeDef",
    {
        "DataPathList": Sequence[DataPathValueTypeDef],
        "Width": NotRequired[str],
    },
)

PivotTableFieldCollapseStateTargetTypeDef = TypedDict(
    "PivotTableFieldCollapseStateTargetTypeDef",
    {
        "FieldId": NotRequired[str],
        "FieldDataPathValues": NotRequired[Sequence[DataPathValueTypeDef]],
    },
)

SearchDataSetsRequestRequestTypeDef = TypedDict(
    "SearchDataSetsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[DataSetSearchFilterTypeDef],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

SearchDataSourcesRequestRequestTypeDef = TypedDict(
    "SearchDataSourcesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[DataSourceSearchFilterTypeDef],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

SearchDataSourcesResponseTypeDef = TypedDict(
    "SearchDataSourcesResponseTypeDef",
    {
        "DataSourceSummaries": List[DataSourceSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TimeRangeFilterValueTypeDef = TypedDict(
    "TimeRangeFilterValueTypeDef",
    {
        "StaticValue": NotRequired[TimestampTypeDef],
        "RollingDate": NotRequired[RollingDateConfigurationTypeDef],
        "Parameter": NotRequired[str],
    },
)

DecimalDatasetParameterTypeDef = TypedDict(
    "DecimalDatasetParameterTypeDef",
    {
        "Id": str,
        "Name": str,
        "ValueType": DatasetParameterValueTypeType,
        "DefaultValues": NotRequired[DecimalDatasetParameterDefaultValuesTypeDef],
    },
)

DescribeFolderPermissionsRequestDescribeFolderPermissionsPaginateTypeDef = TypedDict(
    "DescribeFolderPermissionsRequestDescribeFolderPermissionsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
        "Namespace": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeFolderResolvedPermissionsRequestDescribeFolderResolvedPermissionsPaginateTypeDef = (
    TypedDict(
        "DescribeFolderResolvedPermissionsRequestDescribeFolderResolvedPermissionsPaginateTypeDef",
        {
            "AwsAccountId": str,
            "FolderId": str,
            "Namespace": NotRequired[str],
            "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
        },
    )
)

ListAnalysesRequestListAnalysesPaginateTypeDef = TypedDict(
    "ListAnalysesRequestListAnalysesPaginateTypeDef",
    {
        "AwsAccountId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListAssetBundleExportJobsRequestListAssetBundleExportJobsPaginateTypeDef = TypedDict(
    "ListAssetBundleExportJobsRequestListAssetBundleExportJobsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListAssetBundleImportJobsRequestListAssetBundleImportJobsPaginateTypeDef = TypedDict(
    "ListAssetBundleImportJobsRequestListAssetBundleImportJobsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef = TypedDict(
    "ListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListDashboardsRequestListDashboardsPaginateTypeDef = TypedDict(
    "ListDashboardsRequestListDashboardsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListDataSetsRequestListDataSetsPaginateTypeDef = TypedDict(
    "ListDataSetsRequestListDataSetsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListDataSourcesRequestListDataSourcesPaginateTypeDef = TypedDict(
    "ListDataSourcesRequestListDataSourcesPaginateTypeDef",
    {
        "AwsAccountId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListFolderMembersRequestListFolderMembersPaginateTypeDef = TypedDict(
    "ListFolderMembersRequestListFolderMembersPaginateTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListFoldersRequestListFoldersPaginateTypeDef = TypedDict(
    "ListFoldersRequestListFoldersPaginateTypeDef",
    {
        "AwsAccountId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef = TypedDict(
    "ListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef",
    {
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListGroupsRequestListGroupsPaginateTypeDef = TypedDict(
    "ListGroupsRequestListGroupsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListIAMPolicyAssignmentsForUserRequestListIAMPolicyAssignmentsForUserPaginateTypeDef = TypedDict(
    "ListIAMPolicyAssignmentsForUserRequestListIAMPolicyAssignmentsForUserPaginateTypeDef",
    {
        "AwsAccountId": str,
        "UserName": str,
        "Namespace": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListIAMPolicyAssignmentsRequestListIAMPolicyAssignmentsPaginateTypeDef = TypedDict(
    "ListIAMPolicyAssignmentsRequestListIAMPolicyAssignmentsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
        "AssignmentStatus": NotRequired[AssignmentStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListIngestionsRequestListIngestionsPaginateTypeDef = TypedDict(
    "ListIngestionsRequestListIngestionsPaginateTypeDef",
    {
        "DataSetId": str,
        "AwsAccountId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListNamespacesRequestListNamespacesPaginateTypeDef = TypedDict(
    "ListNamespacesRequestListNamespacesPaginateTypeDef",
    {
        "AwsAccountId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef = TypedDict(
    "ListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef = TypedDict(
    "ListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListTemplatesRequestListTemplatesPaginateTypeDef = TypedDict(
    "ListTemplatesRequestListTemplatesPaginateTypeDef",
    {
        "AwsAccountId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListThemeVersionsRequestListThemeVersionsPaginateTypeDef = TypedDict(
    "ListThemeVersionsRequestListThemeVersionsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListThemesRequestListThemesPaginateTypeDef = TypedDict(
    "ListThemesRequestListThemesPaginateTypeDef",
    {
        "AwsAccountId": str,
        "Type": NotRequired[ThemeTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListUserGroupsRequestListUserGroupsPaginateTypeDef = TypedDict(
    "ListUserGroupsRequestListUserGroupsPaginateTypeDef",
    {
        "UserName": str,
        "AwsAccountId": str,
        "Namespace": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListUsersRequestListUsersPaginateTypeDef = TypedDict(
    "ListUsersRequestListUsersPaginateTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

SearchAnalysesRequestSearchAnalysesPaginateTypeDef = TypedDict(
    "SearchAnalysesRequestSearchAnalysesPaginateTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[AnalysisSearchFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

SearchDashboardsRequestSearchDashboardsPaginateTypeDef = TypedDict(
    "SearchDashboardsRequestSearchDashboardsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[DashboardSearchFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

SearchDataSetsRequestSearchDataSetsPaginateTypeDef = TypedDict(
    "SearchDataSetsRequestSearchDataSetsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[DataSetSearchFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

SearchDataSourcesRequestSearchDataSourcesPaginateTypeDef = TypedDict(
    "SearchDataSourcesRequestSearchDataSourcesPaginateTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[DataSourceSearchFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeFolderPermissionsResponsePaginatorTypeDef = TypedDict(
    "DescribeFolderPermissionsResponsePaginatorTypeDef",
    {
        "Status": int,
        "FolderId": str,
        "Arn": str,
        "Permissions": List[ResourcePermissionPaginatorTypeDef],
        "RequestId": str,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFolderResolvedPermissionsResponsePaginatorTypeDef = TypedDict(
    "DescribeFolderResolvedPermissionsResponsePaginatorTypeDef",
    {
        "Status": int,
        "FolderId": str,
        "Arn": str,
        "Permissions": List[ResourcePermissionPaginatorTypeDef],
        "RequestId": str,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFolderResponseTypeDef = TypedDict(
    "DescribeFolderResponseTypeDef",
    {
        "Status": int,
        "Folder": FolderTypeDef,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeIAMPolicyAssignmentResponseTypeDef = TypedDict(
    "DescribeIAMPolicyAssignmentResponseTypeDef",
    {
        "IAMPolicyAssignment": IAMPolicyAssignmentTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTopicRefreshResponseTypeDef = TypedDict(
    "DescribeTopicRefreshResponseTypeDef",
    {
        "RefreshDetails": TopicRefreshDetailsTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeUserResponseTypeDef = TypedDict(
    "DescribeUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUsersResponseTypeDef = TypedDict(
    "ListUsersResponseTypeDef",
    {
        "UserList": List[UserTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterUserResponseTypeDef = TypedDict(
    "RegisterUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "UserInvitationUrl": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateUserResponseTypeDef = TypedDict(
    "UpdateUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisplayFormatOptionsTypeDef = TypedDict(
    "DisplayFormatOptionsTypeDef",
    {
        "UseBlankCellFormat": NotRequired[bool],
        "BlankCellFormat": NotRequired[str],
        "DateFormat": NotRequired[str],
        "DecimalSeparator": NotRequired[TopicNumericSeparatorSymbolType],
        "GroupingSeparator": NotRequired[str],
        "UseGrouping": NotRequired[bool],
        "FractionDigits": NotRequired[int],
        "Prefix": NotRequired[str],
        "Suffix": NotRequired[str],
        "UnitScaler": NotRequired[NumberScaleType],
        "NegativeFormat": NotRequired[NegativeFormatTypeDef],
        "CurrencySymbol": NotRequired[str],
    },
)

DonutOptionsTypeDef = TypedDict(
    "DonutOptionsTypeDef",
    {
        "ArcOptions": NotRequired[ArcOptionsTypeDef],
        "DonutCenterOptions": NotRequired[DonutCenterOptionsTypeDef],
    },
)

RelativeDatesFilterTypeDef = TypedDict(
    "RelativeDatesFilterTypeDef",
    {
        "FilterId": str,
        "Column": ColumnIdentifierTypeDef,
        "AnchorDateConfiguration": AnchorDateConfigurationTypeDef,
        "TimeGranularity": TimeGranularityType,
        "RelativeDateType": RelativeDateTypeType,
        "NullOption": FilterNullOptionType,
        "MinimumGranularity": NotRequired[TimeGranularityType],
        "RelativeDateValue": NotRequired[int],
        "ParameterName": NotRequired[str],
        "ExcludePeriodConfiguration": NotRequired[ExcludePeriodConfigurationTypeDef],
    },
)

FilterOperationTargetVisualsConfigurationTypeDef = TypedDict(
    "FilterOperationTargetVisualsConfigurationTypeDef",
    {
        "SameSheetTargetVisualConfiguration": NotRequired[
            SameSheetTargetVisualConfigurationTypeDef
        ],
    },
)

SearchFoldersRequestRequestTypeDef = TypedDict(
    "SearchFoldersRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[FolderSearchFilterTypeDef],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

SearchFoldersRequestSearchFoldersPaginateTypeDef = TypedDict(
    "SearchFoldersRequestSearchFoldersPaginateTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[FolderSearchFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListFoldersResponseTypeDef = TypedDict(
    "ListFoldersResponseTypeDef",
    {
        "Status": int,
        "FolderSummaryList": List[FolderSummaryTypeDef],
        "NextToken": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchFoldersResponseTypeDef = TypedDict(
    "SearchFoldersResponseTypeDef",
    {
        "Status": int,
        "FolderSummaryList": List[FolderSummaryTypeDef],
        "NextToken": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FontConfigurationTypeDef = TypedDict(
    "FontConfigurationTypeDef",
    {
        "FontSize": NotRequired[FontSizeTypeDef],
        "FontDecoration": NotRequired[FontDecorationType],
        "FontColor": NotRequired[str],
        "FontWeight": NotRequired[FontWeightTypeDef],
        "FontStyle": NotRequired[FontStyleType],
    },
)

TypographyTypeDef = TypedDict(
    "TypographyTypeDef",
    {
        "FontFamilies": NotRequired[Sequence[FontTypeDef]],
    },
)

FreeFormLayoutCanvasSizeOptionsTypeDef = TypedDict(
    "FreeFormLayoutCanvasSizeOptionsTypeDef",
    {
        "ScreenCanvasSizeOptions": NotRequired[FreeFormLayoutScreenCanvasSizeOptionsTypeDef],
    },
)

SnapshotAnonymousUserTypeDef = TypedDict(
    "SnapshotAnonymousUserTypeDef",
    {
        "RowLevelPermissionTags": NotRequired[Sequence[SessionTagTypeDef]],
    },
)

GeospatialWindowOptionsTypeDef = TypedDict(
    "GeospatialWindowOptionsTypeDef",
    {
        "Bounds": NotRequired[GeospatialCoordinateBoundsTypeDef],
        "MapZoomMode": NotRequired[MapZoomModeType],
    },
)

GeospatialHeatmapColorScaleTypeDef = TypedDict(
    "GeospatialHeatmapColorScaleTypeDef",
    {
        "Colors": NotRequired[Sequence[GeospatialHeatmapDataColorTypeDef]],
    },
)

TableSideBorderOptionsTypeDef = TypedDict(
    "TableSideBorderOptionsTypeDef",
    {
        "InnerVertical": NotRequired[TableBorderOptionsTypeDef],
        "InnerHorizontal": NotRequired[TableBorderOptionsTypeDef],
        "Left": NotRequired[TableBorderOptionsTypeDef],
        "Right": NotRequired[TableBorderOptionsTypeDef],
        "Top": NotRequired[TableBorderOptionsTypeDef],
        "Bottom": NotRequired[TableBorderOptionsTypeDef],
    },
)

GradientColorTypeDef = TypedDict(
    "GradientColorTypeDef",
    {
        "Stops": NotRequired[Sequence[GradientStopTypeDef]],
    },
)

GridLayoutCanvasSizeOptionsTypeDef = TypedDict(
    "GridLayoutCanvasSizeOptionsTypeDef",
    {
        "ScreenCanvasSizeOptions": NotRequired[GridLayoutScreenCanvasSizeOptionsTypeDef],
    },
)

SearchGroupsRequestRequestTypeDef = TypedDict(
    "SearchGroupsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
        "Filters": Sequence[GroupSearchFilterTypeDef],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

SearchGroupsRequestSearchGroupsPaginateTypeDef = TypedDict(
    "SearchGroupsRequestSearchGroupsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
        "Filters": Sequence[GroupSearchFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListIAMPolicyAssignmentsResponseTypeDef = TypedDict(
    "ListIAMPolicyAssignmentsResponseTypeDef",
    {
        "IAMPolicyAssignments": List[IAMPolicyAssignmentSummaryTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

IncrementalRefreshTypeDef = TypedDict(
    "IncrementalRefreshTypeDef",
    {
        "LookbackWindow": LookbackWindowTypeDef,
    },
)

IngestionTypeDef = TypedDict(
    "IngestionTypeDef",
    {
        "Arn": str,
        "IngestionStatus": IngestionStatusType,
        "CreatedTime": datetime,
        "IngestionId": NotRequired[str],
        "ErrorInfo": NotRequired[ErrorInfoTypeDef],
        "RowInfo": NotRequired[RowInfoTypeDef],
        "QueueInfo": NotRequired[QueueInfoTypeDef],
        "IngestionTimeInSeconds": NotRequired[int],
        "IngestionSizeInBytes": NotRequired[int],
        "RequestSource": NotRequired[IngestionRequestSourceType],
        "RequestType": NotRequired[IngestionRequestTypeType],
    },
)

IntegerDatasetParameterTypeDef = TypedDict(
    "IntegerDatasetParameterTypeDef",
    {
        "Id": str,
        "Name": str,
        "ValueType": DatasetParameterValueTypeType,
        "DefaultValues": NotRequired[IntegerDatasetParameterDefaultValuesTypeDef],
    },
)

JoinInstructionTypeDef = TypedDict(
    "JoinInstructionTypeDef",
    {
        "LeftOperand": str,
        "RightOperand": str,
        "Type": JoinTypeType,
        "OnClause": str,
        "LeftJoinKeyProperties": NotRequired[JoinKeyPropertiesTypeDef],
        "RightJoinKeyProperties": NotRequired[JoinKeyPropertiesTypeDef],
    },
)

KPIVisualLayoutOptionsTypeDef = TypedDict(
    "KPIVisualLayoutOptionsTypeDef",
    {
        "StandardLayout": NotRequired[KPIVisualStandardLayoutTypeDef],
    },
)

LineChartDefaultSeriesSettingsTypeDef = TypedDict(
    "LineChartDefaultSeriesSettingsTypeDef",
    {
        "AxisBinding": NotRequired[AxisBindingType],
        "LineStyleSettings": NotRequired[LineChartLineStyleSettingsTypeDef],
        "MarkerStyleSettings": NotRequired[LineChartMarkerStyleSettingsTypeDef],
    },
)

LineChartSeriesSettingsTypeDef = TypedDict(
    "LineChartSeriesSettingsTypeDef",
    {
        "LineStyleSettings": NotRequired[LineChartLineStyleSettingsTypeDef],
        "MarkerStyleSettings": NotRequired[LineChartMarkerStyleSettingsTypeDef],
    },
)

ListFolderMembersResponseTypeDef = TypedDict(
    "ListFolderMembersResponseTypeDef",
    {
        "Status": int,
        "FolderMemberList": List[MemberIdArnPairTypeDef],
        "NextToken": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTemplateVersionsResponseTypeDef = TypedDict(
    "ListTemplateVersionsResponseTypeDef",
    {
        "TemplateVersionSummaryList": List[TemplateVersionSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTemplatesResponseTypeDef = TypedDict(
    "ListTemplatesResponseTypeDef",
    {
        "TemplateSummaryList": List[TemplateSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListThemeVersionsResponseTypeDef = TypedDict(
    "ListThemeVersionsResponseTypeDef",
    {
        "ThemeVersionSummaryList": List[ThemeVersionSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListThemesResponseTypeDef = TypedDict(
    "ListThemesResponseTypeDef",
    {
        "ThemeSummaryList": List[ThemeSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTopicsResponseTypeDef = TypedDict(
    "ListTopicsResponseTypeDef",
    {
        "TopicsSummaries": List[TopicSummaryTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VisualSubtitleLabelOptionsTypeDef = TypedDict(
    "VisualSubtitleLabelOptionsTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
        "FormatText": NotRequired[LongFormatTextTypeDef],
    },
)

S3ParametersTypeDef = TypedDict(
    "S3ParametersTypeDef",
    {
        "ManifestFileLocation": ManifestFileLocationTypeDef,
        "RoleArn": NotRequired[str],
    },
)

TileLayoutStyleTypeDef = TypedDict(
    "TileLayoutStyleTypeDef",
    {
        "Gutter": NotRequired[GutterStyleTypeDef],
        "Margin": NotRequired[MarginStyleTypeDef],
    },
)

NamedEntityDefinitionTypeDef = TypedDict(
    "NamedEntityDefinitionTypeDef",
    {
        "FieldName": NotRequired[str],
        "PropertyName": NotRequired[str],
        "PropertyRole": NotRequired[PropertyRoleType],
        "PropertyUsage": NotRequired[PropertyUsageType],
        "Metric": NotRequired[NamedEntityDefinitionMetricTypeDef],
    },
)

NamespaceInfoV2TypeDef = TypedDict(
    "NamespaceInfoV2TypeDef",
    {
        "Name": NotRequired[str],
        "Arn": NotRequired[str],
        "CapacityRegion": NotRequired[str],
        "CreationStatus": NotRequired[NamespaceStatusType],
        "IdentityStore": NotRequired[Literal["QUICKSIGHT"]],
        "NamespaceError": NotRequired[NamespaceErrorTypeDef],
    },
)

VPCConnectionSummaryTypeDef = TypedDict(
    "VPCConnectionSummaryTypeDef",
    {
        "VPCConnectionId": NotRequired[str],
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "VPCId": NotRequired[str],
        "SecurityGroupIds": NotRequired[List[str]],
        "DnsResolvers": NotRequired[List[str]],
        "Status": NotRequired[VPCConnectionResourceStatusType],
        "AvailabilityStatus": NotRequired[VPCConnectionAvailabilityStatusType],
        "NetworkInterfaces": NotRequired[List[NetworkInterfaceTypeDef]],
        "RoleArn": NotRequired[str],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
    },
)

VPCConnectionTypeDef = TypedDict(
    "VPCConnectionTypeDef",
    {
        "VPCConnectionId": NotRequired[str],
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "VPCId": NotRequired[str],
        "SecurityGroupIds": NotRequired[List[str]],
        "DnsResolvers": NotRequired[List[str]],
        "Status": NotRequired[VPCConnectionResourceStatusType],
        "AvailabilityStatus": NotRequired[VPCConnectionAvailabilityStatusType],
        "NetworkInterfaces": NotRequired[List[NetworkInterfaceTypeDef]],
        "RoleArn": NotRequired[str],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
    },
)

NumericSeparatorConfigurationTypeDef = TypedDict(
    "NumericSeparatorConfigurationTypeDef",
    {
        "DecimalSeparator": NotRequired[NumericSeparatorSymbolType],
        "ThousandsSeparator": NotRequired[ThousandSeparatorOptionsTypeDef],
    },
)

NumericalAggregationFunctionTypeDef = TypedDict(
    "NumericalAggregationFunctionTypeDef",
    {
        "SimpleNumericalAggregation": NotRequired[SimpleNumericalAggregationFunctionType],
        "PercentileAggregation": NotRequired[PercentileAggregationTypeDef],
    },
)

VisibleRangeOptionsTypeDef = TypedDict(
    "VisibleRangeOptionsTypeDef",
    {
        "PercentRange": NotRequired[PercentVisibleRangeTypeDef],
    },
)

RadarChartSeriesSettingsTypeDef = TypedDict(
    "RadarChartSeriesSettingsTypeDef",
    {
        "AreaStyleSettings": NotRequired[RadarChartAreaStyleSettingsTypeDef],
    },
)

TopicRangeFilterConstantTypeDef = TypedDict(
    "TopicRangeFilterConstantTypeDef",
    {
        "ConstantType": NotRequired[ConstantTypeType],
        "RangeConstant": NotRequired[RangeConstantTypeDef],
    },
)

RedshiftParametersPaginatorTypeDef = TypedDict(
    "RedshiftParametersPaginatorTypeDef",
    {
        "Database": str,
        "Host": NotRequired[str],
        "Port": NotRequired[int],
        "ClusterId": NotRequired[str],
        "IAMParameters": NotRequired[RedshiftIAMParametersPaginatorTypeDef],
    },
)

RedshiftParametersTypeDef = TypedDict(
    "RedshiftParametersTypeDef",
    {
        "Database": str,
        "Host": NotRequired[str],
        "Port": NotRequired[int],
        "ClusterId": NotRequired[str],
        "IAMParameters": NotRequired[RedshiftIAMParametersTypeDef],
    },
)

RefreshFrequencyTypeDef = TypedDict(
    "RefreshFrequencyTypeDef",
    {
        "Interval": RefreshIntervalType,
        "RefreshOnDay": NotRequired[ScheduleRefreshOnEntityTypeDef],
        "Timezone": NotRequired[str],
        "TimeOfTheDay": NotRequired[str],
    },
)

RegisteredUserConsoleFeatureConfigurationsTypeDef = TypedDict(
    "RegisteredUserConsoleFeatureConfigurationsTypeDef",
    {
        "StatePersistence": NotRequired[StatePersistenceConfigurationsTypeDef],
    },
)

RegisteredUserDashboardFeatureConfigurationsTypeDef = TypedDict(
    "RegisteredUserDashboardFeatureConfigurationsTypeDef",
    {
        "StatePersistence": NotRequired[StatePersistenceConfigurationsTypeDef],
        "Bookmarks": NotRequired[BookmarksConfigurationsTypeDef],
    },
)

RowLevelPermissionTagConfigurationTypeDef = TypedDict(
    "RowLevelPermissionTagConfigurationTypeDef",
    {
        "TagRules": Sequence[RowLevelPermissionTagRuleTypeDef],
        "Status": NotRequired[StatusType],
        "TagRuleConfigurations": NotRequired[Sequence[Sequence[str]]],
    },
)

SnapshotS3DestinationConfigurationTypeDef = TypedDict(
    "SnapshotS3DestinationConfigurationTypeDef",
    {
        "BucketConfiguration": NotRequired[S3BucketConfigurationTypeDef],
    },
)

S3SourceTypeDef = TypedDict(
    "S3SourceTypeDef",
    {
        "DataSourceArn": str,
        "InputColumns": Sequence[InputColumnTypeDef],
        "UploadSettings": NotRequired[UploadSettingsTypeDef],
    },
)

SectionPageBreakConfigurationTypeDef = TypedDict(
    "SectionPageBreakConfigurationTypeDef",
    {
        "After": NotRequired[SectionAfterPageBreakTypeDef],
    },
)

SectionBasedLayoutPaperCanvasSizeOptionsTypeDef = TypedDict(
    "SectionBasedLayoutPaperCanvasSizeOptionsTypeDef",
    {
        "PaperSize": NotRequired[PaperSizeType],
        "PaperOrientation": NotRequired[PaperOrientationType],
        "PaperMargin": NotRequired[SpacingTypeDef],
    },
)

SectionStyleTypeDef = TypedDict(
    "SectionStyleTypeDef",
    {
        "Height": NotRequired[str],
        "Padding": NotRequired[SpacingTypeDef],
    },
)

SelectedSheetsFilterScopeConfigurationTypeDef = TypedDict(
    "SelectedSheetsFilterScopeConfigurationTypeDef",
    {
        "SheetVisualScopingConfigurations": NotRequired[
            Sequence[SheetVisualScopingConfigurationTypeDef]
        ],
    },
)

SheetElementRenderingRuleTypeDef = TypedDict(
    "SheetElementRenderingRuleTypeDef",
    {
        "Expression": str,
        "ConfigurationOverrides": SheetElementConfigurationOverridesTypeDef,
    },
)

VisualTitleLabelOptionsTypeDef = TypedDict(
    "VisualTitleLabelOptionsTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
        "FormatText": NotRequired[ShortFormatTextTypeDef],
    },
)

SnapshotUserConfigurationRedactedTypeDef = TypedDict(
    "SnapshotUserConfigurationRedactedTypeDef",
    {
        "AnonymousUsers": NotRequired[List[SnapshotAnonymousUserRedactedTypeDef]],
    },
)

SnapshotFileTypeDef = TypedDict(
    "SnapshotFileTypeDef",
    {
        "SheetSelections": List[SnapshotFileSheetSelectionTypeDef],
        "FormatType": SnapshotFileFormatTypeType,
    },
)

StringDatasetParameterTypeDef = TypedDict(
    "StringDatasetParameterTypeDef",
    {
        "Id": str,
        "Name": str,
        "ValueType": DatasetParameterValueTypeType,
        "DefaultValues": NotRequired[StringDatasetParameterDefaultValuesTypeDef],
    },
)

TableFieldImageConfigurationTypeDef = TypedDict(
    "TableFieldImageConfigurationTypeDef",
    {
        "SizingOptions": NotRequired[TableCellImageSizingConfigurationTypeDef],
    },
)

TopicNumericEqualityFilterTypeDef = TypedDict(
    "TopicNumericEqualityFilterTypeDef",
    {
        "Constant": NotRequired[TopicSingularFilterConstantTypeDef],
        "Aggregation": NotRequired[NamedFilterAggTypeType],
    },
)

TopicRelativeDateFilterTypeDef = TypedDict(
    "TopicRelativeDateFilterTypeDef",
    {
        "TimeGranularity": NotRequired[TopicTimeGranularityType],
        "RelativeDateFilterFunction": NotRequired[TopicRelativeDateFilterFunctionType],
        "Constant": NotRequired[TopicSingularFilterConstantTypeDef],
    },
)

CascadingControlConfigurationTypeDef = TypedDict(
    "CascadingControlConfigurationTypeDef",
    {
        "SourceControls": NotRequired[Sequence[CascadingControlSourceTypeDef]],
    },
)

DateTimeDefaultValuesTypeDef = TypedDict(
    "DateTimeDefaultValuesTypeDef",
    {
        "DynamicValue": NotRequired[DynamicDefaultValueTypeDef],
        "StaticValues": NotRequired[Sequence[TimestampTypeDef]],
        "RollingDate": NotRequired[RollingDateConfigurationTypeDef],
    },
)

DecimalDefaultValuesTypeDef = TypedDict(
    "DecimalDefaultValuesTypeDef",
    {
        "DynamicValue": NotRequired[DynamicDefaultValueTypeDef],
        "StaticValues": NotRequired[Sequence[float]],
    },
)

IntegerDefaultValuesTypeDef = TypedDict(
    "IntegerDefaultValuesTypeDef",
    {
        "DynamicValue": NotRequired[DynamicDefaultValueTypeDef],
        "StaticValues": NotRequired[Sequence[int]],
    },
)

StringDefaultValuesTypeDef = TypedDict(
    "StringDefaultValuesTypeDef",
    {
        "DynamicValue": NotRequired[DynamicDefaultValueTypeDef],
        "StaticValues": NotRequired[Sequence[str]],
    },
)

AnalysisTypeDef = TypedDict(
    "AnalysisTypeDef",
    {
        "AnalysisId": NotRequired[str],
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "Status": NotRequired[ResourceStatusType],
        "Errors": NotRequired[List[AnalysisErrorTypeDef]],
        "DataSetArns": NotRequired[List[str]],
        "ThemeArn": NotRequired[str],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
        "Sheets": NotRequired[List[SheetTypeDef]],
    },
)

DashboardVersionTypeDef = TypedDict(
    "DashboardVersionTypeDef",
    {
        "CreatedTime": NotRequired[datetime],
        "Errors": NotRequired[List[DashboardErrorTypeDef]],
        "VersionNumber": NotRequired[int],
        "Status": NotRequired[ResourceStatusType],
        "Arn": NotRequired[str],
        "SourceEntityArn": NotRequired[str],
        "DataSetArns": NotRequired[List[str]],
        "Description": NotRequired[str],
        "ThemeArn": NotRequired[str],
        "Sheets": NotRequired[List[SheetTypeDef]],
    },
)

AnalysisSourceEntityTypeDef = TypedDict(
    "AnalysisSourceEntityTypeDef",
    {
        "SourceTemplate": NotRequired[AnalysisSourceTemplateTypeDef],
    },
)

DashboardSourceEntityTypeDef = TypedDict(
    "DashboardSourceEntityTypeDef",
    {
        "SourceTemplate": NotRequired[DashboardSourceTemplateTypeDef],
    },
)

TemplateSourceEntityTypeDef = TypedDict(
    "TemplateSourceEntityTypeDef",
    {
        "SourceAnalysis": NotRequired[TemplateSourceAnalysisTypeDef],
        "SourceTemplate": NotRequired[TemplateSourceTemplateTypeDef],
    },
)

AnonymousUserEmbeddingExperienceConfigurationTypeDef = TypedDict(
    "AnonymousUserEmbeddingExperienceConfigurationTypeDef",
    {
        "Dashboard": NotRequired[AnonymousUserDashboardEmbeddingConfigurationTypeDef],
        "DashboardVisual": NotRequired[AnonymousUserDashboardVisualEmbeddingConfigurationTypeDef],
        "QSearchBar": NotRequired[AnonymousUserQSearchBarEmbeddingConfigurationTypeDef],
    },
)

DescribeAssetBundleExportJobResponseTypeDef = TypedDict(
    "DescribeAssetBundleExportJobResponseTypeDef",
    {
        "JobStatus": AssetBundleExportJobStatusType,
        "DownloadUrl": str,
        "Errors": List[AssetBundleExportJobErrorTypeDef],
        "Arn": str,
        "CreatedTime": datetime,
        "AssetBundleExportJobId": str,
        "AwsAccountId": str,
        "ResourceArns": List[str],
        "IncludeAllDependencies": bool,
        "ExportFormat": AssetBundleExportFormatType,
        "CloudFormationOverridePropertyConfiguration": (
            AssetBundleCloudFormationOverridePropertyConfigurationTypeDef
        ),
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartAssetBundleExportJobRequestRequestTypeDef = TypedDict(
    "StartAssetBundleExportJobRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AssetBundleExportJobId": str,
        "ResourceArns": Sequence[str],
        "ExportFormat": AssetBundleExportFormatType,
        "IncludeAllDependencies": NotRequired[bool],
        "CloudFormationOverridePropertyConfiguration": NotRequired[
            AssetBundleCloudFormationOverridePropertyConfigurationTypeDef
        ],
    },
)

NumericAxisOptionsTypeDef = TypedDict(
    "NumericAxisOptionsTypeDef",
    {
        "Scale": NotRequired[AxisScaleTypeDef],
        "Range": NotRequired[AxisDisplayRangeTypeDef],
    },
)

CategoryFilterTypeDef = TypedDict(
    "CategoryFilterTypeDef",
    {
        "FilterId": str,
        "Column": ColumnIdentifierTypeDef,
        "Configuration": CategoryFilterConfigurationTypeDef,
    },
)

ClusterMarkerConfigurationTypeDef = TypedDict(
    "ClusterMarkerConfigurationTypeDef",
    {
        "ClusterMarker": NotRequired[ClusterMarkerTypeDef],
    },
)

TopicCategoryFilterTypeDef = TypedDict(
    "TopicCategoryFilterTypeDef",
    {
        "CategoryFilterFunction": NotRequired[CategoryFilterFunctionType],
        "CategoryFilterType": NotRequired[CategoryFilterTypeType],
        "Constant": NotRequired[TopicCategoryFilterConstantTypeDef],
        "Inverse": NotRequired[bool],
    },
)

TagColumnOperationTypeDef = TypedDict(
    "TagColumnOperationTypeDef",
    {
        "ColumnName": str,
        "Tags": Sequence[ColumnTagTypeDef],
    },
)

DataSetConfigurationTypeDef = TypedDict(
    "DataSetConfigurationTypeDef",
    {
        "Placeholder": NotRequired[str],
        "DataSetSchema": NotRequired[DataSetSchemaTypeDef],
        "ColumnGroupSchemaList": NotRequired[Sequence[ColumnGroupSchemaTypeDef]],
    },
)

ConditionalFormattingIconTypeDef = TypedDict(
    "ConditionalFormattingIconTypeDef",
    {
        "IconSet": NotRequired[ConditionalFormattingIconSetTypeDef],
        "CustomCondition": NotRequired[ConditionalFormattingCustomIconConditionTypeDef],
    },
)

DescribeDashboardPermissionsResponseTypeDef = TypedDict(
    "DescribeDashboardPermissionsResponseTypeDef",
    {
        "DashboardId": str,
        "DashboardArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "Status": int,
        "RequestId": str,
        "LinkSharingConfiguration": LinkSharingConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDashboardPermissionsResponseTypeDef = TypedDict(
    "UpdateDashboardPermissionsResponseTypeDef",
    {
        "DashboardArn": str,
        "DashboardId": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "LinkSharingConfiguration": LinkSharingConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDataSetsResponseTypeDef = TypedDict(
    "ListDataSetsResponseTypeDef",
    {
        "DataSetSummaries": List[DataSetSummaryTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchDataSetsResponseTypeDef = TypedDict(
    "SearchDataSetsResponseTypeDef",
    {
        "DataSetSummaries": List[DataSetSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CustomValuesConfigurationTypeDef = TypedDict(
    "CustomValuesConfigurationTypeDef",
    {
        "CustomValues": CustomParameterValuesTypeDef,
        "IncludeNullValue": NotRequired[bool],
    },
)

DateTimeDatasetParameterTypeDef = TypedDict(
    "DateTimeDatasetParameterTypeDef",
    {
        "Id": str,
        "Name": str,
        "ValueType": DatasetParameterValueTypeType,
        "TimeGranularity": NotRequired[TimeGranularityType],
        "DefaultValues": NotRequired[DateTimeDatasetParameterDefaultValuesTypeDef],
    },
)

ParametersTypeDef = TypedDict(
    "ParametersTypeDef",
    {
        "StringParameters": NotRequired[Sequence[StringParameterTypeDef]],
        "IntegerParameters": NotRequired[Sequence[IntegerParameterTypeDef]],
        "DecimalParameters": NotRequired[Sequence[DecimalParameterTypeDef]],
        "DateTimeParameters": NotRequired[Sequence[DateTimeParameterTypeDef]],
    },
)

OverrideDatasetParameterOperationTypeDef = TypedDict(
    "OverrideDatasetParameterOperationTypeDef",
    {
        "ParameterName": str,
        "NewParameterName": NotRequired[str],
        "NewDefaultValues": NotRequired[NewDefaultValuesTypeDef],
    },
)

DrillDownFilterTypeDef = TypedDict(
    "DrillDownFilterTypeDef",
    {
        "NumericEqualityFilter": NotRequired[NumericEqualityDrillDownFilterTypeDef],
        "CategoryFilter": NotRequired[CategoryDrillDownFilterTypeDef],
        "TimeRangeFilter": NotRequired[TimeRangeDrillDownFilterTypeDef],
    },
)

CreateTopicRefreshScheduleRequestRequestTypeDef = TypedDict(
    "CreateTopicRefreshScheduleRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TopicId": str,
        "DatasetArn": str,
        "RefreshSchedule": TopicRefreshScheduleTypeDef,
        "DatasetName": NotRequired[str],
    },
)

DescribeTopicRefreshScheduleResponseTypeDef = TypedDict(
    "DescribeTopicRefreshScheduleResponseTypeDef",
    {
        "TopicId": str,
        "TopicArn": str,
        "DatasetArn": str,
        "RefreshSchedule": TopicRefreshScheduleTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TopicRefreshScheduleSummaryTypeDef = TypedDict(
    "TopicRefreshScheduleSummaryTypeDef",
    {
        "DatasetId": NotRequired[str],
        "DatasetArn": NotRequired[str],
        "DatasetName": NotRequired[str],
        "RefreshSchedule": NotRequired[TopicRefreshScheduleTypeDef],
    },
)

UpdateTopicRefreshScheduleRequestRequestTypeDef = TypedDict(
    "UpdateTopicRefreshScheduleRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TopicId": str,
        "DatasetId": str,
        "RefreshSchedule": TopicRefreshScheduleTypeDef,
    },
)

ForecastScenarioTypeDef = TypedDict(
    "ForecastScenarioTypeDef",
    {
        "WhatIfPointScenario": NotRequired[WhatIfPointScenarioTypeDef],
        "WhatIfRangeScenario": NotRequired[WhatIfRangeScenarioTypeDef],
    },
)

DashboardPublishOptionsTypeDef = TypedDict(
    "DashboardPublishOptionsTypeDef",
    {
        "AdHocFilteringOption": NotRequired[AdHocFilteringOptionTypeDef],
        "ExportToCSVOption": NotRequired[ExportToCSVOptionTypeDef],
        "SheetControlsOption": NotRequired[SheetControlsOptionTypeDef],
        "VisualPublishOptions": NotRequired[DashboardVisualPublishOptionsTypeDef],
        "SheetLayoutElementMaximizationOption": NotRequired[
            SheetLayoutElementMaximizationOptionTypeDef
        ],
        "VisualMenuOption": NotRequired[VisualMenuOptionTypeDef],
        "VisualAxisSortOption": NotRequired[VisualAxisSortOptionTypeDef],
        "ExportWithHiddenFieldsOption": NotRequired[ExportWithHiddenFieldsOptionTypeDef],
        "DataPointDrillUpDownOption": NotRequired[DataPointDrillUpDownOptionTypeDef],
        "DataPointMenuLabelOption": NotRequired[DataPointMenuLabelOptionTypeDef],
        "DataPointTooltipOption": NotRequired[DataPointTooltipOptionTypeDef],
    },
)

VisualPaletteTypeDef = TypedDict(
    "VisualPaletteTypeDef",
    {
        "ChartColor": NotRequired[str],
        "ColorMap": NotRequired[Sequence[DataPathColorTypeDef]],
    },
)

PivotTableFieldCollapseStateOptionTypeDef = TypedDict(
    "PivotTableFieldCollapseStateOptionTypeDef",
    {
        "Target": PivotTableFieldCollapseStateTargetTypeDef,
        "State": NotRequired[PivotTableFieldCollapseStateType],
    },
)

TimeRangeFilterTypeDef = TypedDict(
    "TimeRangeFilterTypeDef",
    {
        "FilterId": str,
        "Column": ColumnIdentifierTypeDef,
        "NullOption": FilterNullOptionType,
        "IncludeMinimum": NotRequired[bool],
        "IncludeMaximum": NotRequired[bool],
        "RangeMinimumValue": NotRequired[TimeRangeFilterValueTypeDef],
        "RangeMaximumValue": NotRequired[TimeRangeFilterValueTypeDef],
        "ExcludePeriodConfiguration": NotRequired[ExcludePeriodConfigurationTypeDef],
        "TimeGranularity": NotRequired[TimeGranularityType],
    },
)

DefaultFormattingTypeDef = TypedDict(
    "DefaultFormattingTypeDef",
    {
        "DisplayFormat": NotRequired[DisplayFormatType],
        "DisplayFormatOptions": NotRequired[DisplayFormatOptionsTypeDef],
    },
)

CustomActionFilterOperationTypeDef = TypedDict(
    "CustomActionFilterOperationTypeDef",
    {
        "SelectedFieldsConfiguration": FilterOperationSelectedFieldsConfigurationTypeDef,
        "TargetVisualsConfiguration": FilterOperationTargetVisualsConfigurationTypeDef,
    },
)

AxisLabelOptionsTypeDef = TypedDict(
    "AxisLabelOptionsTypeDef",
    {
        "FontConfiguration": NotRequired[FontConfigurationTypeDef],
        "CustomLabel": NotRequired[str],
        "ApplyTo": NotRequired[AxisLabelReferenceOptionsTypeDef],
    },
)

DataLabelOptionsTypeDef = TypedDict(
    "DataLabelOptionsTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
        "CategoryLabelVisibility": NotRequired[VisibilityType],
        "MeasureLabelVisibility": NotRequired[VisibilityType],
        "DataLabelTypes": NotRequired[Sequence[DataLabelTypeTypeDef]],
        "Position": NotRequired[DataLabelPositionType],
        "LabelContent": NotRequired[DataLabelContentType],
        "LabelFontConfiguration": NotRequired[FontConfigurationTypeDef],
        "LabelColor": NotRequired[str],
        "Overlap": NotRequired[DataLabelOverlapType],
        "TotalsVisibility": NotRequired[VisibilityType],
    },
)

FunnelChartDataLabelOptionsTypeDef = TypedDict(
    "FunnelChartDataLabelOptionsTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
        "CategoryLabelVisibility": NotRequired[VisibilityType],
        "MeasureLabelVisibility": NotRequired[VisibilityType],
        "Position": NotRequired[DataLabelPositionType],
        "LabelFontConfiguration": NotRequired[FontConfigurationTypeDef],
        "LabelColor": NotRequired[str],
        "MeasureDataLabelStyle": NotRequired[FunnelChartMeasureDataLabelStyleType],
    },
)

LabelOptionsTypeDef = TypedDict(
    "LabelOptionsTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
        "FontConfiguration": NotRequired[FontConfigurationTypeDef],
        "CustomLabel": NotRequired[str],
    },
)

PanelTitleOptionsTypeDef = TypedDict(
    "PanelTitleOptionsTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
        "FontConfiguration": NotRequired[FontConfigurationTypeDef],
        "HorizontalTextAlignment": NotRequired[HorizontalTextAlignmentType],
    },
)

TableFieldCustomTextContentTypeDef = TypedDict(
    "TableFieldCustomTextContentTypeDef",
    {
        "FontConfiguration": FontConfigurationTypeDef,
        "Value": NotRequired[str],
    },
)

DefaultFreeFormLayoutConfigurationTypeDef = TypedDict(
    "DefaultFreeFormLayoutConfigurationTypeDef",
    {
        "CanvasSizeOptions": FreeFormLayoutCanvasSizeOptionsTypeDef,
    },
)

SnapshotUserConfigurationTypeDef = TypedDict(
    "SnapshotUserConfigurationTypeDef",
    {
        "AnonymousUsers": NotRequired[Sequence[SnapshotAnonymousUserTypeDef]],
    },
)

GeospatialHeatmapConfigurationTypeDef = TypedDict(
    "GeospatialHeatmapConfigurationTypeDef",
    {
        "HeatmapColor": NotRequired[GeospatialHeatmapColorScaleTypeDef],
    },
)

GlobalTableBorderOptionsTypeDef = TypedDict(
    "GlobalTableBorderOptionsTypeDef",
    {
        "UniformBorder": NotRequired[TableBorderOptionsTypeDef],
        "SideSpecificBorder": NotRequired[TableSideBorderOptionsTypeDef],
    },
)

ConditionalFormattingGradientColorTypeDef = TypedDict(
    "ConditionalFormattingGradientColorTypeDef",
    {
        "Expression": str,
        "Color": GradientColorTypeDef,
    },
)

DefaultGridLayoutConfigurationTypeDef = TypedDict(
    "DefaultGridLayoutConfigurationTypeDef",
    {
        "CanvasSizeOptions": GridLayoutCanvasSizeOptionsTypeDef,
    },
)

GridLayoutConfigurationTypeDef = TypedDict(
    "GridLayoutConfigurationTypeDef",
    {
        "Elements": Sequence[GridLayoutElementTypeDef],
        "CanvasSizeOptions": NotRequired[GridLayoutCanvasSizeOptionsTypeDef],
    },
)

RefreshConfigurationTypeDef = TypedDict(
    "RefreshConfigurationTypeDef",
    {
        "IncrementalRefresh": IncrementalRefreshTypeDef,
    },
)

DescribeIngestionResponseTypeDef = TypedDict(
    "DescribeIngestionResponseTypeDef",
    {
        "Ingestion": IngestionTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListIngestionsResponseTypeDef = TypedDict(
    "ListIngestionsResponseTypeDef",
    {
        "Ingestions": List[IngestionTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LogicalTableSourceTypeDef = TypedDict(
    "LogicalTableSourceTypeDef",
    {
        "JoinInstruction": NotRequired[JoinInstructionTypeDef],
        "PhysicalTableId": NotRequired[str],
        "DataSetArn": NotRequired[str],
    },
)

DataFieldSeriesItemTypeDef = TypedDict(
    "DataFieldSeriesItemTypeDef",
    {
        "FieldId": str,
        "AxisBinding": AxisBindingType,
        "FieldValue": NotRequired[str],
        "Settings": NotRequired[LineChartSeriesSettingsTypeDef],
    },
)

FieldSeriesItemTypeDef = TypedDict(
    "FieldSeriesItemTypeDef",
    {
        "FieldId": str,
        "AxisBinding": AxisBindingType,
        "Settings": NotRequired[LineChartSeriesSettingsTypeDef],
    },
)

SheetStyleTypeDef = TypedDict(
    "SheetStyleTypeDef",
    {
        "Tile": NotRequired[TileStyleTypeDef],
        "TileLayout": NotRequired[TileLayoutStyleTypeDef],
    },
)

TopicNamedEntityTypeDef = TypedDict(
    "TopicNamedEntityTypeDef",
    {
        "EntityName": str,
        "EntityDescription": NotRequired[str],
        "EntitySynonyms": NotRequired[Sequence[str]],
        "SemanticEntityType": NotRequired[SemanticEntityTypeTypeDef],
        "Definition": NotRequired[Sequence[NamedEntityDefinitionTypeDef]],
    },
)

DescribeNamespaceResponseTypeDef = TypedDict(
    "DescribeNamespaceResponseTypeDef",
    {
        "Namespace": NamespaceInfoV2TypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListNamespacesResponseTypeDef = TypedDict(
    "ListNamespacesResponseTypeDef",
    {
        "Namespaces": List[NamespaceInfoV2TypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVPCConnectionsResponseTypeDef = TypedDict(
    "ListVPCConnectionsResponseTypeDef",
    {
        "VPCConnectionSummaries": List[VPCConnectionSummaryTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeVPCConnectionResponseTypeDef = TypedDict(
    "DescribeVPCConnectionResponseTypeDef",
    {
        "VPCConnection": VPCConnectionTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CurrencyDisplayFormatConfigurationTypeDef = TypedDict(
    "CurrencyDisplayFormatConfigurationTypeDef",
    {
        "Prefix": NotRequired[str],
        "Suffix": NotRequired[str],
        "SeparatorConfiguration": NotRequired[NumericSeparatorConfigurationTypeDef],
        "Symbol": NotRequired[str],
        "DecimalPlacesConfiguration": NotRequired[DecimalPlacesConfigurationTypeDef],
        "NumberScale": NotRequired[NumberScaleType],
        "NegativeValueConfiguration": NotRequired[NegativeValueConfigurationTypeDef],
        "NullValueFormatConfiguration": NotRequired[NullValueFormatConfigurationTypeDef],
    },
)

NumberDisplayFormatConfigurationTypeDef = TypedDict(
    "NumberDisplayFormatConfigurationTypeDef",
    {
        "Prefix": NotRequired[str],
        "Suffix": NotRequired[str],
        "SeparatorConfiguration": NotRequired[NumericSeparatorConfigurationTypeDef],
        "DecimalPlacesConfiguration": NotRequired[DecimalPlacesConfigurationTypeDef],
        "NumberScale": NotRequired[NumberScaleType],
        "NegativeValueConfiguration": NotRequired[NegativeValueConfigurationTypeDef],
        "NullValueFormatConfiguration": NotRequired[NullValueFormatConfigurationTypeDef],
    },
)

PercentageDisplayFormatConfigurationTypeDef = TypedDict(
    "PercentageDisplayFormatConfigurationTypeDef",
    {
        "Prefix": NotRequired[str],
        "Suffix": NotRequired[str],
        "SeparatorConfiguration": NotRequired[NumericSeparatorConfigurationTypeDef],
        "DecimalPlacesConfiguration": NotRequired[DecimalPlacesConfigurationTypeDef],
        "NegativeValueConfiguration": NotRequired[NegativeValueConfigurationTypeDef],
        "NullValueFormatConfiguration": NotRequired[NullValueFormatConfigurationTypeDef],
    },
)

AggregationFunctionTypeDef = TypedDict(
    "AggregationFunctionTypeDef",
    {
        "NumericalAggregationFunction": NotRequired[NumericalAggregationFunctionTypeDef],
        "CategoricalAggregationFunction": NotRequired[CategoricalAggregationFunctionType],
        "DateAggregationFunction": NotRequired[DateAggregationFunctionType],
        "AttributeAggregationFunction": NotRequired[AttributeAggregationFunctionTypeDef],
    },
)

ScrollBarOptionsTypeDef = TypedDict(
    "ScrollBarOptionsTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
        "VisibleRange": NotRequired[VisibleRangeOptionsTypeDef],
    },
)

TopicDateRangeFilterTypeDef = TypedDict(
    "TopicDateRangeFilterTypeDef",
    {
        "Inclusive": NotRequired[bool],
        "Constant": NotRequired[TopicRangeFilterConstantTypeDef],
    },
)

TopicNumericRangeFilterTypeDef = TypedDict(
    "TopicNumericRangeFilterTypeDef",
    {
        "Inclusive": NotRequired[bool],
        "Constant": NotRequired[TopicRangeFilterConstantTypeDef],
        "Aggregation": NotRequired[NamedFilterAggTypeType],
    },
)

DataSourceParametersPaginatorTypeDef = TypedDict(
    "DataSourceParametersPaginatorTypeDef",
    {
        "AmazonElasticsearchParameters": NotRequired[AmazonElasticsearchParametersTypeDef],
        "AthenaParameters": NotRequired[AthenaParametersTypeDef],
        "AuroraParameters": NotRequired[AuroraParametersTypeDef],
        "AuroraPostgreSqlParameters": NotRequired[AuroraPostgreSqlParametersTypeDef],
        "AwsIotAnalyticsParameters": NotRequired[AwsIotAnalyticsParametersTypeDef],
        "JiraParameters": NotRequired[JiraParametersTypeDef],
        "MariaDbParameters": NotRequired[MariaDbParametersTypeDef],
        "MySqlParameters": NotRequired[MySqlParametersTypeDef],
        "OracleParameters": NotRequired[OracleParametersTypeDef],
        "PostgreSqlParameters": NotRequired[PostgreSqlParametersTypeDef],
        "PrestoParameters": NotRequired[PrestoParametersTypeDef],
        "RdsParameters": NotRequired[RdsParametersTypeDef],
        "RedshiftParameters": NotRequired[RedshiftParametersPaginatorTypeDef],
        "S3Parameters": NotRequired[S3ParametersTypeDef],
        "ServiceNowParameters": NotRequired[ServiceNowParametersTypeDef],
        "SnowflakeParameters": NotRequired[SnowflakeParametersTypeDef],
        "SparkParameters": NotRequired[SparkParametersTypeDef],
        "SqlServerParameters": NotRequired[SqlServerParametersTypeDef],
        "TeradataParameters": NotRequired[TeradataParametersTypeDef],
        "TwitterParameters": NotRequired[TwitterParametersTypeDef],
        "AmazonOpenSearchParameters": NotRequired[AmazonOpenSearchParametersTypeDef],
        "ExasolParameters": NotRequired[ExasolParametersTypeDef],
        "DatabricksParameters": NotRequired[DatabricksParametersTypeDef],
    },
)

DataSourceParametersTypeDef = TypedDict(
    "DataSourceParametersTypeDef",
    {
        "AmazonElasticsearchParameters": NotRequired[AmazonElasticsearchParametersTypeDef],
        "AthenaParameters": NotRequired[AthenaParametersTypeDef],
        "AuroraParameters": NotRequired[AuroraParametersTypeDef],
        "AuroraPostgreSqlParameters": NotRequired[AuroraPostgreSqlParametersTypeDef],
        "AwsIotAnalyticsParameters": NotRequired[AwsIotAnalyticsParametersTypeDef],
        "JiraParameters": NotRequired[JiraParametersTypeDef],
        "MariaDbParameters": NotRequired[MariaDbParametersTypeDef],
        "MySqlParameters": NotRequired[MySqlParametersTypeDef],
        "OracleParameters": NotRequired[OracleParametersTypeDef],
        "PostgreSqlParameters": NotRequired[PostgreSqlParametersTypeDef],
        "PrestoParameters": NotRequired[PrestoParametersTypeDef],
        "RdsParameters": NotRequired[RdsParametersTypeDef],
        "RedshiftParameters": NotRequired[RedshiftParametersTypeDef],
        "S3Parameters": NotRequired[S3ParametersTypeDef],
        "ServiceNowParameters": NotRequired[ServiceNowParametersTypeDef],
        "SnowflakeParameters": NotRequired[SnowflakeParametersTypeDef],
        "SparkParameters": NotRequired[SparkParametersTypeDef],
        "SqlServerParameters": NotRequired[SqlServerParametersTypeDef],
        "TeradataParameters": NotRequired[TeradataParametersTypeDef],
        "TwitterParameters": NotRequired[TwitterParametersTypeDef],
        "AmazonOpenSearchParameters": NotRequired[AmazonOpenSearchParametersTypeDef],
        "ExasolParameters": NotRequired[ExasolParametersTypeDef],
        "DatabricksParameters": NotRequired[DatabricksParametersTypeDef],
    },
)

RefreshScheduleTypeDef = TypedDict(
    "RefreshScheduleTypeDef",
    {
        "ScheduleId": str,
        "ScheduleFrequency": RefreshFrequencyTypeDef,
        "RefreshType": IngestionTypeType,
        "StartAfterDateTime": NotRequired[TimestampTypeDef],
        "Arn": NotRequired[str],
    },
)

RegisteredUserQuickSightConsoleEmbeddingConfigurationTypeDef = TypedDict(
    "RegisteredUserQuickSightConsoleEmbeddingConfigurationTypeDef",
    {
        "InitialPath": NotRequired[str],
        "FeatureConfigurations": NotRequired[RegisteredUserConsoleFeatureConfigurationsTypeDef],
    },
)

RegisteredUserDashboardEmbeddingConfigurationTypeDef = TypedDict(
    "RegisteredUserDashboardEmbeddingConfigurationTypeDef",
    {
        "InitialDashboardId": str,
        "FeatureConfigurations": NotRequired[RegisteredUserDashboardFeatureConfigurationsTypeDef],
    },
)

SnapshotDestinationConfigurationTypeDef = TypedDict(
    "SnapshotDestinationConfigurationTypeDef",
    {
        "S3Destinations": NotRequired[List[SnapshotS3DestinationConfigurationTypeDef]],
    },
)

SnapshotJobS3ResultTypeDef = TypedDict(
    "SnapshotJobS3ResultTypeDef",
    {
        "S3DestinationConfiguration": NotRequired[SnapshotS3DestinationConfigurationTypeDef],
        "S3Uri": NotRequired[str],
        "ErrorInfo": NotRequired[List[SnapshotJobResultErrorInfoTypeDef]],
    },
)

PhysicalTableTypeDef = TypedDict(
    "PhysicalTableTypeDef",
    {
        "RelationalTable": NotRequired[RelationalTableTypeDef],
        "CustomSql": NotRequired[CustomSqlTypeDef],
        "S3Source": NotRequired[S3SourceTypeDef],
    },
)

SectionBasedLayoutCanvasSizeOptionsTypeDef = TypedDict(
    "SectionBasedLayoutCanvasSizeOptionsTypeDef",
    {
        "PaperCanvasSizeOptions": NotRequired[SectionBasedLayoutPaperCanvasSizeOptionsTypeDef],
    },
)

FilterScopeConfigurationTypeDef = TypedDict(
    "FilterScopeConfigurationTypeDef",
    {
        "SelectedSheets": NotRequired[SelectedSheetsFilterScopeConfigurationTypeDef],
        "AllSheets": NotRequired[Mapping[str, Any]],
    },
)

FreeFormLayoutElementTypeDef = TypedDict(
    "FreeFormLayoutElementTypeDef",
    {
        "ElementId": str,
        "ElementType": LayoutElementTypeType,
        "XAxisLocation": str,
        "YAxisLocation": str,
        "Width": str,
        "Height": str,
        "Visibility": NotRequired[VisibilityType],
        "RenderingRules": NotRequired[Sequence[SheetElementRenderingRuleTypeDef]],
        "BorderStyle": NotRequired[FreeFormLayoutElementBorderStyleTypeDef],
        "SelectedBorderStyle": NotRequired[FreeFormLayoutElementBorderStyleTypeDef],
        "BackgroundStyle": NotRequired[FreeFormLayoutElementBackgroundStyleTypeDef],
        "LoadingAnimation": NotRequired[LoadingAnimationTypeDef],
    },
)

SnapshotFileGroupTypeDef = TypedDict(
    "SnapshotFileGroupTypeDef",
    {
        "Files": NotRequired[List[SnapshotFileTypeDef]],
    },
)

DateTimeParameterDeclarationTypeDef = TypedDict(
    "DateTimeParameterDeclarationTypeDef",
    {
        "Name": str,
        "DefaultValues": NotRequired[DateTimeDefaultValuesTypeDef],
        "TimeGranularity": NotRequired[TimeGranularityType],
        "ValueWhenUnset": NotRequired[DateTimeValueWhenUnsetConfigurationTypeDef],
        "MappedDataSetParameters": NotRequired[Sequence[MappedDataSetParameterTypeDef]],
    },
)

DecimalParameterDeclarationTypeDef = TypedDict(
    "DecimalParameterDeclarationTypeDef",
    {
        "ParameterValueType": ParameterValueTypeType,
        "Name": str,
        "DefaultValues": NotRequired[DecimalDefaultValuesTypeDef],
        "ValueWhenUnset": NotRequired[DecimalValueWhenUnsetConfigurationTypeDef],
        "MappedDataSetParameters": NotRequired[Sequence[MappedDataSetParameterTypeDef]],
    },
)

IntegerParameterDeclarationTypeDef = TypedDict(
    "IntegerParameterDeclarationTypeDef",
    {
        "ParameterValueType": ParameterValueTypeType,
        "Name": str,
        "DefaultValues": NotRequired[IntegerDefaultValuesTypeDef],
        "ValueWhenUnset": NotRequired[IntegerValueWhenUnsetConfigurationTypeDef],
        "MappedDataSetParameters": NotRequired[Sequence[MappedDataSetParameterTypeDef]],
    },
)

StringParameterDeclarationTypeDef = TypedDict(
    "StringParameterDeclarationTypeDef",
    {
        "ParameterValueType": ParameterValueTypeType,
        "Name": str,
        "DefaultValues": NotRequired[StringDefaultValuesTypeDef],
        "ValueWhenUnset": NotRequired[StringValueWhenUnsetConfigurationTypeDef],
        "MappedDataSetParameters": NotRequired[Sequence[MappedDataSetParameterTypeDef]],
    },
)

DescribeAnalysisResponseTypeDef = TypedDict(
    "DescribeAnalysisResponseTypeDef",
    {
        "Analysis": AnalysisTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DashboardTypeDef = TypedDict(
    "DashboardTypeDef",
    {
        "DashboardId": NotRequired[str],
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "Version": NotRequired[DashboardVersionTypeDef],
        "CreatedTime": NotRequired[datetime],
        "LastPublishedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
    },
)

GenerateEmbedUrlForAnonymousUserRequestRequestTypeDef = TypedDict(
    "GenerateEmbedUrlForAnonymousUserRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
        "AuthorizedResourceArns": Sequence[str],
        "ExperienceConfiguration": AnonymousUserEmbeddingExperienceConfigurationTypeDef,
        "SessionLifetimeInMinutes": NotRequired[int],
        "SessionTags": NotRequired[Sequence[SessionTagTypeDef]],
        "AllowedDomains": NotRequired[Sequence[str]],
    },
)

AxisDataOptionsTypeDef = TypedDict(
    "AxisDataOptionsTypeDef",
    {
        "NumericAxisOptions": NotRequired[NumericAxisOptionsTypeDef],
        "DateAxisOptions": NotRequired[DateAxisOptionsTypeDef],
    },
)

TemplateVersionTypeDef = TypedDict(
    "TemplateVersionTypeDef",
    {
        "CreatedTime": NotRequired[datetime],
        "Errors": NotRequired[List[TemplateErrorTypeDef]],
        "VersionNumber": NotRequired[int],
        "Status": NotRequired[ResourceStatusType],
        "DataSetConfigurations": NotRequired[List[DataSetConfigurationTypeDef]],
        "Description": NotRequired[str],
        "SourceEntityArn": NotRequired[str],
        "ThemeArn": NotRequired[str],
        "Sheets": NotRequired[List[SheetTypeDef]],
    },
)

DestinationParameterValueConfigurationTypeDef = TypedDict(
    "DestinationParameterValueConfigurationTypeDef",
    {
        "CustomValuesConfiguration": NotRequired[CustomValuesConfigurationTypeDef],
        "SelectAllValueOptions": NotRequired[Literal["ALL_VALUES"]],
        "SourceParameterName": NotRequired[str],
        "SourceField": NotRequired[str],
        "SourceColumn": NotRequired[ColumnIdentifierTypeDef],
    },
)

DatasetParameterTypeDef = TypedDict(
    "DatasetParameterTypeDef",
    {
        "StringDatasetParameter": NotRequired[StringDatasetParameterTypeDef],
        "DecimalDatasetParameter": NotRequired[DecimalDatasetParameterTypeDef],
        "IntegerDatasetParameter": NotRequired[IntegerDatasetParameterTypeDef],
        "DateTimeDatasetParameter": NotRequired[DateTimeDatasetParameterTypeDef],
    },
)

TransformOperationTypeDef = TypedDict(
    "TransformOperationTypeDef",
    {
        "ProjectOperation": NotRequired[ProjectOperationTypeDef],
        "FilterOperation": NotRequired[FilterOperationTypeDef],
        "CreateColumnsOperation": NotRequired[CreateColumnsOperationTypeDef],
        "RenameColumnOperation": NotRequired[RenameColumnOperationTypeDef],
        "CastColumnTypeOperation": NotRequired[CastColumnTypeOperationTypeDef],
        "TagColumnOperation": NotRequired[TagColumnOperationTypeDef],
        "UntagColumnOperation": NotRequired[UntagColumnOperationTypeDef],
        "OverrideDatasetParameterOperation": NotRequired[OverrideDatasetParameterOperationTypeDef],
    },
)

DateTimeHierarchyTypeDef = TypedDict(
    "DateTimeHierarchyTypeDef",
    {
        "HierarchyId": str,
        "DrillDownFilters": NotRequired[Sequence[DrillDownFilterTypeDef]],
    },
)

ExplicitHierarchyTypeDef = TypedDict(
    "ExplicitHierarchyTypeDef",
    {
        "HierarchyId": str,
        "Columns": Sequence[ColumnIdentifierTypeDef],
        "DrillDownFilters": NotRequired[Sequence[DrillDownFilterTypeDef]],
    },
)

PredefinedHierarchyTypeDef = TypedDict(
    "PredefinedHierarchyTypeDef",
    {
        "HierarchyId": str,
        "Columns": Sequence[ColumnIdentifierTypeDef],
        "DrillDownFilters": NotRequired[Sequence[DrillDownFilterTypeDef]],
    },
)

ListTopicRefreshSchedulesResponseTypeDef = TypedDict(
    "ListTopicRefreshSchedulesResponseTypeDef",
    {
        "TopicId": str,
        "TopicArn": str,
        "RefreshSchedules": List[TopicRefreshScheduleSummaryTypeDef],
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ForecastConfigurationTypeDef = TypedDict(
    "ForecastConfigurationTypeDef",
    {
        "ForecastProperties": NotRequired[TimeBasedForecastPropertiesTypeDef],
        "Scenario": NotRequired[ForecastScenarioTypeDef],
    },
)

PivotTableFieldOptionsTypeDef = TypedDict(
    "PivotTableFieldOptionsTypeDef",
    {
        "SelectedFieldOptions": NotRequired[Sequence[PivotTableFieldOptionTypeDef]],
        "DataPathOptions": NotRequired[Sequence[PivotTableDataPathOptionTypeDef]],
        "CollapseStateOptions": NotRequired[Sequence[PivotTableFieldCollapseStateOptionTypeDef]],
    },
)

TopicCalculatedFieldTypeDef = TypedDict(
    "TopicCalculatedFieldTypeDef",
    {
        "CalculatedFieldName": str,
        "Expression": str,
        "CalculatedFieldDescription": NotRequired[str],
        "CalculatedFieldSynonyms": NotRequired[Sequence[str]],
        "IsIncludedInTopic": NotRequired[bool],
        "DisableIndexing": NotRequired[bool],
        "ColumnDataRole": NotRequired[ColumnDataRoleType],
        "TimeGranularity": NotRequired[TopicTimeGranularityType],
        "DefaultFormatting": NotRequired[DefaultFormattingTypeDef],
        "Aggregation": NotRequired[DefaultAggregationType],
        "ComparativeOrder": NotRequired[ComparativeOrderTypeDef],
        "SemanticType": NotRequired[SemanticTypeTypeDef],
        "AllowedAggregations": NotRequired[Sequence[AuthorSpecifiedAggregationType]],
        "NotAllowedAggregations": NotRequired[Sequence[AuthorSpecifiedAggregationType]],
        "NeverAggregateInFilter": NotRequired[bool],
        "CellValueSynonyms": NotRequired[Sequence[CellValueSynonymTypeDef]],
        "NonAdditive": NotRequired[bool],
    },
)

TopicColumnTypeDef = TypedDict(
    "TopicColumnTypeDef",
    {
        "ColumnName": str,
        "ColumnFriendlyName": NotRequired[str],
        "ColumnDescription": NotRequired[str],
        "ColumnSynonyms": NotRequired[Sequence[str]],
        "ColumnDataRole": NotRequired[ColumnDataRoleType],
        "Aggregation": NotRequired[DefaultAggregationType],
        "IsIncludedInTopic": NotRequired[bool],
        "DisableIndexing": NotRequired[bool],
        "ComparativeOrder": NotRequired[ComparativeOrderTypeDef],
        "SemanticType": NotRequired[SemanticTypeTypeDef],
        "TimeGranularity": NotRequired[TopicTimeGranularityType],
        "AllowedAggregations": NotRequired[Sequence[AuthorSpecifiedAggregationType]],
        "NotAllowedAggregations": NotRequired[Sequence[AuthorSpecifiedAggregationType]],
        "DefaultFormatting": NotRequired[DefaultFormattingTypeDef],
        "NeverAggregateInFilter": NotRequired[bool],
        "CellValueSynonyms": NotRequired[Sequence[CellValueSynonymTypeDef]],
        "NonAdditive": NotRequired[bool],
    },
)

ChartAxisLabelOptionsTypeDef = TypedDict(
    "ChartAxisLabelOptionsTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
        "SortIconVisibility": NotRequired[VisibilityType],
        "AxisLabelOptions": NotRequired[Sequence[AxisLabelOptionsTypeDef]],
    },
)

AxisTickLabelOptionsTypeDef = TypedDict(
    "AxisTickLabelOptionsTypeDef",
    {
        "LabelOptions": NotRequired[LabelOptionsTypeDef],
        "RotationAngle": NotRequired[float],
    },
)

DateTimePickerControlDisplayOptionsTypeDef = TypedDict(
    "DateTimePickerControlDisplayOptionsTypeDef",
    {
        "TitleOptions": NotRequired[LabelOptionsTypeDef],
        "DateTimeFormat": NotRequired[str],
        "InfoIconLabelOptions": NotRequired[SheetControlInfoIconLabelOptionsTypeDef],
    },
)

DropDownControlDisplayOptionsTypeDef = TypedDict(
    "DropDownControlDisplayOptionsTypeDef",
    {
        "SelectAllOptions": NotRequired[ListControlSelectAllOptionsTypeDef],
        "TitleOptions": NotRequired[LabelOptionsTypeDef],
        "InfoIconLabelOptions": NotRequired[SheetControlInfoIconLabelOptionsTypeDef],
    },
)

LegendOptionsTypeDef = TypedDict(
    "LegendOptionsTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
        "Title": NotRequired[LabelOptionsTypeDef],
        "Position": NotRequired[LegendPositionType],
        "Width": NotRequired[str],
        "Height": NotRequired[str],
    },
)

ListControlDisplayOptionsTypeDef = TypedDict(
    "ListControlDisplayOptionsTypeDef",
    {
        "SearchOptions": NotRequired[ListControlSearchOptionsTypeDef],
        "SelectAllOptions": NotRequired[ListControlSelectAllOptionsTypeDef],
        "TitleOptions": NotRequired[LabelOptionsTypeDef],
        "InfoIconLabelOptions": NotRequired[SheetControlInfoIconLabelOptionsTypeDef],
    },
)

RelativeDateTimeControlDisplayOptionsTypeDef = TypedDict(
    "RelativeDateTimeControlDisplayOptionsTypeDef",
    {
        "TitleOptions": NotRequired[LabelOptionsTypeDef],
        "DateTimeFormat": NotRequired[str],
        "InfoIconLabelOptions": NotRequired[SheetControlInfoIconLabelOptionsTypeDef],
    },
)

SliderControlDisplayOptionsTypeDef = TypedDict(
    "SliderControlDisplayOptionsTypeDef",
    {
        "TitleOptions": NotRequired[LabelOptionsTypeDef],
        "InfoIconLabelOptions": NotRequired[SheetControlInfoIconLabelOptionsTypeDef],
    },
)

TextAreaControlDisplayOptionsTypeDef = TypedDict(
    "TextAreaControlDisplayOptionsTypeDef",
    {
        "TitleOptions": NotRequired[LabelOptionsTypeDef],
        "PlaceholderOptions": NotRequired[TextControlPlaceholderOptionsTypeDef],
        "InfoIconLabelOptions": NotRequired[SheetControlInfoIconLabelOptionsTypeDef],
    },
)

TextFieldControlDisplayOptionsTypeDef = TypedDict(
    "TextFieldControlDisplayOptionsTypeDef",
    {
        "TitleOptions": NotRequired[LabelOptionsTypeDef],
        "PlaceholderOptions": NotRequired[TextControlPlaceholderOptionsTypeDef],
        "InfoIconLabelOptions": NotRequired[SheetControlInfoIconLabelOptionsTypeDef],
    },
)

PanelConfigurationTypeDef = TypedDict(
    "PanelConfigurationTypeDef",
    {
        "Title": NotRequired[PanelTitleOptionsTypeDef],
        "BorderVisibility": NotRequired[VisibilityType],
        "BorderThickness": NotRequired[str],
        "BorderStyle": NotRequired[PanelBorderStyleType],
        "BorderColor": NotRequired[str],
        "GutterVisibility": NotRequired[VisibilityType],
        "GutterSpacing": NotRequired[str],
        "BackgroundVisibility": NotRequired[VisibilityType],
        "BackgroundColor": NotRequired[str],
    },
)

TableFieldLinkContentConfigurationTypeDef = TypedDict(
    "TableFieldLinkContentConfigurationTypeDef",
    {
        "CustomTextContent": NotRequired[TableFieldCustomTextContentTypeDef],
        "CustomIconContent": NotRequired[TableFieldCustomIconContentTypeDef],
    },
)

GeospatialPointStyleOptionsTypeDef = TypedDict(
    "GeospatialPointStyleOptionsTypeDef",
    {
        "SelectedPointStyle": NotRequired[GeospatialSelectedPointStyleType],
        "ClusterMarkerConfiguration": NotRequired[ClusterMarkerConfigurationTypeDef],
        "HeatmapConfiguration": NotRequired[GeospatialHeatmapConfigurationTypeDef],
    },
)

TableCellStyleTypeDef = TypedDict(
    "TableCellStyleTypeDef",
    {
        "Visibility": NotRequired[VisibilityType],
        "FontConfiguration": NotRequired[FontConfigurationTypeDef],
        "TextWrap": NotRequired[TextWrapType],
        "HorizontalTextAlignment": NotRequired[HorizontalTextAlignmentType],
        "VerticalTextAlignment": NotRequired[VerticalTextAlignmentType],
        "BackgroundColor": NotRequired[str],
        "Height": NotRequired[int],
        "Border": NotRequired[GlobalTableBorderOptionsTypeDef],
    },
)

ConditionalFormattingColorTypeDef = TypedDict(
    "ConditionalFormattingColorTypeDef",
    {
        "Solid": NotRequired[ConditionalFormattingSolidColorTypeDef],
        "Gradient": NotRequired[ConditionalFormattingGradientColorTypeDef],
    },
)

DefaultInteractiveLayoutConfigurationTypeDef = TypedDict(
    "DefaultInteractiveLayoutConfigurationTypeDef",
    {
        "Grid": NotRequired[DefaultGridLayoutConfigurationTypeDef],
        "FreeForm": NotRequired[DefaultFreeFormLayoutConfigurationTypeDef],
    },
)

SheetControlLayoutConfigurationTypeDef = TypedDict(
    "SheetControlLayoutConfigurationTypeDef",
    {
        "GridLayout": NotRequired[GridLayoutConfigurationTypeDef],
    },
)

DataSetRefreshPropertiesTypeDef = TypedDict(
    "DataSetRefreshPropertiesTypeDef",
    {
        "RefreshConfiguration": RefreshConfigurationTypeDef,
    },
)

SeriesItemTypeDef = TypedDict(
    "SeriesItemTypeDef",
    {
        "FieldSeriesItem": NotRequired[FieldSeriesItemTypeDef],
        "DataFieldSeriesItem": NotRequired[DataFieldSeriesItemTypeDef],
    },
)

ThemeConfigurationTypeDef = TypedDict(
    "ThemeConfigurationTypeDef",
    {
        "DataColorPalette": NotRequired[DataColorPaletteTypeDef],
        "UIColorPalette": NotRequired[UIColorPaletteTypeDef],
        "Sheet": NotRequired[SheetStyleTypeDef],
        "Typography": NotRequired[TypographyTypeDef],
    },
)

ComparisonFormatConfigurationTypeDef = TypedDict(
    "ComparisonFormatConfigurationTypeDef",
    {
        "NumberDisplayFormatConfiguration": NotRequired[NumberDisplayFormatConfigurationTypeDef],
        "PercentageDisplayFormatConfiguration": NotRequired[
            PercentageDisplayFormatConfigurationTypeDef
        ],
    },
)

NumericFormatConfigurationTypeDef = TypedDict(
    "NumericFormatConfigurationTypeDef",
    {
        "NumberDisplayFormatConfiguration": NotRequired[NumberDisplayFormatConfigurationTypeDef],
        "CurrencyDisplayFormatConfiguration": NotRequired[
            CurrencyDisplayFormatConfigurationTypeDef
        ],
        "PercentageDisplayFormatConfiguration": NotRequired[
            PercentageDisplayFormatConfigurationTypeDef
        ],
    },
)

AggregationSortConfigurationTypeDef = TypedDict(
    "AggregationSortConfigurationTypeDef",
    {
        "Column": ColumnIdentifierTypeDef,
        "SortDirection": SortDirectionType,
        "AggregationFunction": NotRequired[AggregationFunctionTypeDef],
    },
)

ColumnSortTypeDef = TypedDict(
    "ColumnSortTypeDef",
    {
        "SortBy": ColumnIdentifierTypeDef,
        "Direction": SortDirectionType,
        "AggregationFunction": NotRequired[AggregationFunctionTypeDef],
    },
)

ColumnTooltipItemTypeDef = TypedDict(
    "ColumnTooltipItemTypeDef",
    {
        "Column": ColumnIdentifierTypeDef,
        "Label": NotRequired[str],
        "Visibility": NotRequired[VisibilityType],
        "Aggregation": NotRequired[AggregationFunctionTypeDef],
    },
)

NumericEqualityFilterTypeDef = TypedDict(
    "NumericEqualityFilterTypeDef",
    {
        "FilterId": str,
        "Column": ColumnIdentifierTypeDef,
        "MatchOperator": NumericEqualityMatchOperatorType,
        "NullOption": FilterNullOptionType,
        "Value": NotRequired[float],
        "SelectAllOptions": NotRequired[Literal["FILTER_ALL_VALUES"]],
        "AggregationFunction": NotRequired[AggregationFunctionTypeDef],
        "ParameterName": NotRequired[str],
    },
)

NumericRangeFilterTypeDef = TypedDict(
    "NumericRangeFilterTypeDef",
    {
        "FilterId": str,
        "Column": ColumnIdentifierTypeDef,
        "NullOption": FilterNullOptionType,
        "IncludeMinimum": NotRequired[bool],
        "IncludeMaximum": NotRequired[bool],
        "RangeMinimum": NotRequired[NumericRangeFilterValueTypeDef],
        "RangeMaximum": NotRequired[NumericRangeFilterValueTypeDef],
        "SelectAllOptions": NotRequired[Literal["FILTER_ALL_VALUES"]],
        "AggregationFunction": NotRequired[AggregationFunctionTypeDef],
    },
)

ReferenceLineDynamicDataConfigurationTypeDef = TypedDict(
    "ReferenceLineDynamicDataConfigurationTypeDef",
    {
        "Column": ColumnIdentifierTypeDef,
        "Calculation": NumericalAggregationFunctionTypeDef,
        "MeasureAggregationFunction": NotRequired[AggregationFunctionTypeDef],
    },
)

TopicFilterTypeDef = TypedDict(
    "TopicFilterTypeDef",
    {
        "FilterName": str,
        "OperandFieldName": str,
        "FilterDescription": NotRequired[str],
        "FilterClass": NotRequired[FilterClassType],
        "FilterSynonyms": NotRequired[Sequence[str]],
        "FilterType": NotRequired[NamedFilterTypeType],
        "CategoryFilter": NotRequired[TopicCategoryFilterTypeDef],
        "NumericEqualityFilter": NotRequired[TopicNumericEqualityFilterTypeDef],
        "NumericRangeFilter": NotRequired[TopicNumericRangeFilterTypeDef],
        "DateRangeFilter": NotRequired[TopicDateRangeFilterTypeDef],
        "RelativeDateFilter": NotRequired[TopicRelativeDateFilterTypeDef],
    },
)

DataSourcePaginatorTypeDef = TypedDict(
    "DataSourcePaginatorTypeDef",
    {
        "Arn": NotRequired[str],
        "DataSourceId": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[DataSourceTypeType],
        "Status": NotRequired[ResourceStatusType],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
        "DataSourceParameters": NotRequired[DataSourceParametersPaginatorTypeDef],
        "AlternateDataSourceParameters": NotRequired[List[DataSourceParametersPaginatorTypeDef]],
        "VpcConnectionProperties": NotRequired[VpcConnectionPropertiesTypeDef],
        "SslProperties": NotRequired[SslPropertiesTypeDef],
        "ErrorInfo": NotRequired[DataSourceErrorInfoTypeDef],
        "SecretArn": NotRequired[str],
    },
)

AssetBundleImportJobDataSourceOverrideParametersTypeDef = TypedDict(
    "AssetBundleImportJobDataSourceOverrideParametersTypeDef",
    {
        "DataSourceId": str,
        "Name": NotRequired[str],
        "DataSourceParameters": NotRequired[DataSourceParametersTypeDef],
        "VpcConnectionProperties": NotRequired[VpcConnectionPropertiesTypeDef],
        "SslProperties": NotRequired[SslPropertiesTypeDef],
        "Credentials": NotRequired[AssetBundleImportJobDataSourceCredentialsTypeDef],
    },
)

CredentialPairTypeDef = TypedDict(
    "CredentialPairTypeDef",
    {
        "Username": str,
        "Password": str,
        "AlternateDataSourceParameters": NotRequired[Sequence[DataSourceParametersTypeDef]],
    },
)

DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "Arn": NotRequired[str],
        "DataSourceId": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[DataSourceTypeType],
        "Status": NotRequired[ResourceStatusType],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
        "DataSourceParameters": NotRequired[DataSourceParametersTypeDef],
        "AlternateDataSourceParameters": NotRequired[List[DataSourceParametersTypeDef]],
        "VpcConnectionProperties": NotRequired[VpcConnectionPropertiesTypeDef],
        "SslProperties": NotRequired[SslPropertiesTypeDef],
        "ErrorInfo": NotRequired[DataSourceErrorInfoTypeDef],
        "SecretArn": NotRequired[str],
    },
)

CreateRefreshScheduleRequestRequestTypeDef = TypedDict(
    "CreateRefreshScheduleRequestRequestTypeDef",
    {
        "DataSetId": str,
        "AwsAccountId": str,
        "Schedule": RefreshScheduleTypeDef,
    },
)

DescribeRefreshScheduleResponseTypeDef = TypedDict(
    "DescribeRefreshScheduleResponseTypeDef",
    {
        "RefreshSchedule": RefreshScheduleTypeDef,
        "Status": int,
        "RequestId": str,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRefreshSchedulesResponseTypeDef = TypedDict(
    "ListRefreshSchedulesResponseTypeDef",
    {
        "RefreshSchedules": List[RefreshScheduleTypeDef],
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRefreshScheduleRequestRequestTypeDef = TypedDict(
    "UpdateRefreshScheduleRequestRequestTypeDef",
    {
        "DataSetId": str,
        "AwsAccountId": str,
        "Schedule": RefreshScheduleTypeDef,
    },
)

RegisteredUserEmbeddingExperienceConfigurationTypeDef = TypedDict(
    "RegisteredUserEmbeddingExperienceConfigurationTypeDef",
    {
        "Dashboard": NotRequired[RegisteredUserDashboardEmbeddingConfigurationTypeDef],
        "QuickSightConsole": NotRequired[
            RegisteredUserQuickSightConsoleEmbeddingConfigurationTypeDef
        ],
        "QSearchBar": NotRequired[RegisteredUserQSearchBarEmbeddingConfigurationTypeDef],
        "DashboardVisual": NotRequired[RegisteredUserDashboardVisualEmbeddingConfigurationTypeDef],
    },
)

SnapshotJobResultFileGroupTypeDef = TypedDict(
    "SnapshotJobResultFileGroupTypeDef",
    {
        "Files": NotRequired[List[SnapshotFileTypeDef]],
        "S3Results": NotRequired[List[SnapshotJobS3ResultTypeDef]],
    },
)

DefaultSectionBasedLayoutConfigurationTypeDef = TypedDict(
    "DefaultSectionBasedLayoutConfigurationTypeDef",
    {
        "CanvasSizeOptions": SectionBasedLayoutCanvasSizeOptionsTypeDef,
    },
)

FreeFormLayoutConfigurationTypeDef = TypedDict(
    "FreeFormLayoutConfigurationTypeDef",
    {
        "Elements": Sequence[FreeFormLayoutElementTypeDef],
        "CanvasSizeOptions": NotRequired[FreeFormLayoutCanvasSizeOptionsTypeDef],
    },
)

FreeFormSectionLayoutConfigurationTypeDef = TypedDict(
    "FreeFormSectionLayoutConfigurationTypeDef",
    {
        "Elements": Sequence[FreeFormLayoutElementTypeDef],
    },
)

SnapshotConfigurationTypeDef = TypedDict(
    "SnapshotConfigurationTypeDef",
    {
        "FileGroups": List[SnapshotFileGroupTypeDef],
        "DestinationConfiguration": NotRequired[SnapshotDestinationConfigurationTypeDef],
        "Parameters": NotRequired[ParametersTypeDef],
    },
)

ParameterDeclarationTypeDef = TypedDict(
    "ParameterDeclarationTypeDef",
    {
        "StringParameterDeclaration": NotRequired[StringParameterDeclarationTypeDef],
        "DecimalParameterDeclaration": NotRequired[DecimalParameterDeclarationTypeDef],
        "IntegerParameterDeclaration": NotRequired[IntegerParameterDeclarationTypeDef],
        "DateTimeParameterDeclaration": NotRequired[DateTimeParameterDeclarationTypeDef],
    },
)

DescribeDashboardResponseTypeDef = TypedDict(
    "DescribeDashboardResponseTypeDef",
    {
        "Dashboard": DashboardTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TemplateTypeDef = TypedDict(
    "TemplateTypeDef",
    {
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "Version": NotRequired[TemplateVersionTypeDef],
        "TemplateId": NotRequired[str],
        "LastUpdatedTime": NotRequired[datetime],
        "CreatedTime": NotRequired[datetime],
    },
)

SetParameterValueConfigurationTypeDef = TypedDict(
    "SetParameterValueConfigurationTypeDef",
    {
        "DestinationParameterName": str,
        "Value": DestinationParameterValueConfigurationTypeDef,
    },
)

LogicalTableTypeDef = TypedDict(
    "LogicalTableTypeDef",
    {
        "Alias": str,
        "Source": LogicalTableSourceTypeDef,
        "DataTransforms": NotRequired[Sequence[TransformOperationTypeDef]],
    },
)

ColumnHierarchyTypeDef = TypedDict(
    "ColumnHierarchyTypeDef",
    {
        "ExplicitHierarchy": NotRequired[ExplicitHierarchyTypeDef],
        "DateTimeHierarchy": NotRequired[DateTimeHierarchyTypeDef],
        "PredefinedHierarchy": NotRequired[PredefinedHierarchyTypeDef],
    },
)

AxisDisplayOptionsTypeDef = TypedDict(
    "AxisDisplayOptionsTypeDef",
    {
        "TickLabelOptions": NotRequired[AxisTickLabelOptionsTypeDef],
        "AxisLineVisibility": NotRequired[VisibilityType],
        "GridLineVisibility": NotRequired[VisibilityType],
        "DataOptions": NotRequired[AxisDataOptionsTypeDef],
        "ScrollbarOptions": NotRequired[ScrollBarOptionsTypeDef],
        "AxisOffset": NotRequired[str],
    },
)

FilterDateTimePickerControlTypeDef = TypedDict(
    "FilterDateTimePickerControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "DisplayOptions": NotRequired[DateTimePickerControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlDateTimePickerTypeType],
    },
)

ParameterDateTimePickerControlTypeDef = TypedDict(
    "ParameterDateTimePickerControlTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
        "DisplayOptions": NotRequired[DateTimePickerControlDisplayOptionsTypeDef],
    },
)

FilterDropDownControlTypeDef = TypedDict(
    "FilterDropDownControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "DisplayOptions": NotRequired[DropDownControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[FilterSelectableValuesTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationTypeDef],
    },
)

ParameterDropDownControlTypeDef = TypedDict(
    "ParameterDropDownControlTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
        "DisplayOptions": NotRequired[DropDownControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[ParameterSelectableValuesTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationTypeDef],
    },
)

FilterListControlTypeDef = TypedDict(
    "FilterListControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "DisplayOptions": NotRequired[ListControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[FilterSelectableValuesTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationTypeDef],
    },
)

ParameterListControlTypeDef = TypedDict(
    "ParameterListControlTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
        "DisplayOptions": NotRequired[ListControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[ParameterSelectableValuesTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationTypeDef],
    },
)

FilterRelativeDateTimeControlTypeDef = TypedDict(
    "FilterRelativeDateTimeControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "DisplayOptions": NotRequired[RelativeDateTimeControlDisplayOptionsTypeDef],
    },
)

FilterSliderControlTypeDef = TypedDict(
    "FilterSliderControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "MaximumValue": float,
        "MinimumValue": float,
        "StepSize": float,
        "DisplayOptions": NotRequired[SliderControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlSliderTypeType],
    },
)

ParameterSliderControlTypeDef = TypedDict(
    "ParameterSliderControlTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
        "MaximumValue": float,
        "MinimumValue": float,
        "StepSize": float,
        "DisplayOptions": NotRequired[SliderControlDisplayOptionsTypeDef],
    },
)

FilterTextAreaControlTypeDef = TypedDict(
    "FilterTextAreaControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "Delimiter": NotRequired[str],
        "DisplayOptions": NotRequired[TextAreaControlDisplayOptionsTypeDef],
    },
)

ParameterTextAreaControlTypeDef = TypedDict(
    "ParameterTextAreaControlTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
        "Delimiter": NotRequired[str],
        "DisplayOptions": NotRequired[TextAreaControlDisplayOptionsTypeDef],
    },
)

FilterTextFieldControlTypeDef = TypedDict(
    "FilterTextFieldControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "DisplayOptions": NotRequired[TextFieldControlDisplayOptionsTypeDef],
    },
)

ParameterTextFieldControlTypeDef = TypedDict(
    "ParameterTextFieldControlTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
        "DisplayOptions": NotRequired[TextFieldControlDisplayOptionsTypeDef],
    },
)

SmallMultiplesOptionsTypeDef = TypedDict(
    "SmallMultiplesOptionsTypeDef",
    {
        "MaxVisibleRows": NotRequired[int],
        "MaxVisibleColumns": NotRequired[int],
        "PanelConfiguration": NotRequired[PanelConfigurationTypeDef],
        "XAxis": NotRequired[SmallMultiplesAxisPropertiesTypeDef],
        "YAxis": NotRequired[SmallMultiplesAxisPropertiesTypeDef],
    },
)

TableFieldLinkConfigurationTypeDef = TypedDict(
    "TableFieldLinkConfigurationTypeDef",
    {
        "Target": URLTargetConfigurationType,
        "Content": TableFieldLinkContentConfigurationTypeDef,
    },
)

PivotTableOptionsTypeDef = TypedDict(
    "PivotTableOptionsTypeDef",
    {
        "MetricPlacement": NotRequired[PivotTableMetricPlacementType],
        "SingleMetricVisibility": NotRequired[VisibilityType],
        "ColumnNamesVisibility": NotRequired[VisibilityType],
        "ToggleButtonsVisibility": NotRequired[VisibilityType],
        "ColumnHeaderStyle": NotRequired[TableCellStyleTypeDef],
        "RowHeaderStyle": NotRequired[TableCellStyleTypeDef],
        "CellStyle": NotRequired[TableCellStyleTypeDef],
        "RowFieldNamesStyle": NotRequired[TableCellStyleTypeDef],
        "RowAlternateColorOptions": NotRequired[RowAlternateColorOptionsTypeDef],
        "CollapsedRowDimensionsVisibility": NotRequired[VisibilityType],
        "RowsLayout": NotRequired[PivotTableRowsLayoutType],
        "RowsLabelOptions": NotRequired[PivotTableRowsLabelOptionsTypeDef],
        "DefaultCellWidth": NotRequired[str],
    },
)

PivotTotalOptionsTypeDef = TypedDict(
    "PivotTotalOptionsTypeDef",
    {
        "TotalsVisibility": NotRequired[VisibilityType],
        "Placement": NotRequired[TableTotalsPlacementType],
        "ScrollStatus": NotRequired[TableTotalsScrollStatusType],
        "CustomLabel": NotRequired[str],
        "TotalCellStyle": NotRequired[TableCellStyleTypeDef],
        "ValueCellStyle": NotRequired[TableCellStyleTypeDef],
        "MetricHeaderCellStyle": NotRequired[TableCellStyleTypeDef],
    },
)

SubtotalOptionsTypeDef = TypedDict(
    "SubtotalOptionsTypeDef",
    {
        "TotalsVisibility": NotRequired[VisibilityType],
        "CustomLabel": NotRequired[str],
        "FieldLevel": NotRequired[PivotTableSubtotalLevelType],
        "FieldLevelOptions": NotRequired[Sequence[PivotTableFieldSubtotalOptionsTypeDef]],
        "TotalCellStyle": NotRequired[TableCellStyleTypeDef],
        "ValueCellStyle": NotRequired[TableCellStyleTypeDef],
        "MetricHeaderCellStyle": NotRequired[TableCellStyleTypeDef],
        "StyleTargets": NotRequired[Sequence[TableStyleTargetTypeDef]],
    },
)

TableOptionsTypeDef = TypedDict(
    "TableOptionsTypeDef",
    {
        "Orientation": NotRequired[TableOrientationType],
        "HeaderStyle": NotRequired[TableCellStyleTypeDef],
        "CellStyle": NotRequired[TableCellStyleTypeDef],
        "RowAlternateColorOptions": NotRequired[RowAlternateColorOptionsTypeDef],
    },
)

TotalOptionsTypeDef = TypedDict(
    "TotalOptionsTypeDef",
    {
        "TotalsVisibility": NotRequired[VisibilityType],
        "Placement": NotRequired[TableTotalsPlacementType],
        "ScrollStatus": NotRequired[TableTotalsScrollStatusType],
        "CustomLabel": NotRequired[str],
        "TotalCellStyle": NotRequired[TableCellStyleTypeDef],
    },
)

GaugeChartArcConditionalFormattingTypeDef = TypedDict(
    "GaugeChartArcConditionalFormattingTypeDef",
    {
        "ForegroundColor": NotRequired[ConditionalFormattingColorTypeDef],
    },
)

GaugeChartPrimaryValueConditionalFormattingTypeDef = TypedDict(
    "GaugeChartPrimaryValueConditionalFormattingTypeDef",
    {
        "TextColor": NotRequired[ConditionalFormattingColorTypeDef],
        "Icon": NotRequired[ConditionalFormattingIconTypeDef],
    },
)

KPIActualValueConditionalFormattingTypeDef = TypedDict(
    "KPIActualValueConditionalFormattingTypeDef",
    {
        "TextColor": NotRequired[ConditionalFormattingColorTypeDef],
        "Icon": NotRequired[ConditionalFormattingIconTypeDef],
    },
)

KPIComparisonValueConditionalFormattingTypeDef = TypedDict(
    "KPIComparisonValueConditionalFormattingTypeDef",
    {
        "TextColor": NotRequired[ConditionalFormattingColorTypeDef],
        "Icon": NotRequired[ConditionalFormattingIconTypeDef],
    },
)

KPIPrimaryValueConditionalFormattingTypeDef = TypedDict(
    "KPIPrimaryValueConditionalFormattingTypeDef",
    {
        "TextColor": NotRequired[ConditionalFormattingColorTypeDef],
        "Icon": NotRequired[ConditionalFormattingIconTypeDef],
    },
)

KPIProgressBarConditionalFormattingTypeDef = TypedDict(
    "KPIProgressBarConditionalFormattingTypeDef",
    {
        "ForegroundColor": NotRequired[ConditionalFormattingColorTypeDef],
    },
)

ShapeConditionalFormatTypeDef = TypedDict(
    "ShapeConditionalFormatTypeDef",
    {
        "BackgroundColor": ConditionalFormattingColorTypeDef,
    },
)

TableRowConditionalFormattingTypeDef = TypedDict(
    "TableRowConditionalFormattingTypeDef",
    {
        "BackgroundColor": NotRequired[ConditionalFormattingColorTypeDef],
        "TextColor": NotRequired[ConditionalFormattingColorTypeDef],
    },
)

TextConditionalFormatTypeDef = TypedDict(
    "TextConditionalFormatTypeDef",
    {
        "BackgroundColor": NotRequired[ConditionalFormattingColorTypeDef],
        "TextColor": NotRequired[ConditionalFormattingColorTypeDef],
        "Icon": NotRequired[ConditionalFormattingIconTypeDef],
    },
)

SheetControlLayoutTypeDef = TypedDict(
    "SheetControlLayoutTypeDef",
    {
        "Configuration": SheetControlLayoutConfigurationTypeDef,
    },
)

DescribeDataSetRefreshPropertiesResponseTypeDef = TypedDict(
    "DescribeDataSetRefreshPropertiesResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "DataSetRefreshProperties": DataSetRefreshPropertiesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutDataSetRefreshPropertiesRequestRequestTypeDef = TypedDict(
    "PutDataSetRefreshPropertiesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
        "DataSetRefreshProperties": DataSetRefreshPropertiesTypeDef,
    },
)

CreateThemeRequestRequestTypeDef = TypedDict(
    "CreateThemeRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "Name": str,
        "BaseThemeId": str,
        "Configuration": ThemeConfigurationTypeDef,
        "VersionDescription": NotRequired[str],
        "Permissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

ThemeVersionTypeDef = TypedDict(
    "ThemeVersionTypeDef",
    {
        "VersionNumber": NotRequired[int],
        "Arn": NotRequired[str],
        "Description": NotRequired[str],
        "BaseThemeId": NotRequired[str],
        "CreatedTime": NotRequired[datetime],
        "Configuration": NotRequired[ThemeConfigurationTypeDef],
        "Errors": NotRequired[List[ThemeErrorTypeDef]],
        "Status": NotRequired[ResourceStatusType],
    },
)

UpdateThemeRequestRequestTypeDef = TypedDict(
    "UpdateThemeRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "BaseThemeId": str,
        "Name": NotRequired[str],
        "VersionDescription": NotRequired[str],
        "Configuration": NotRequired[ThemeConfigurationTypeDef],
    },
)

ComparisonConfigurationTypeDef = TypedDict(
    "ComparisonConfigurationTypeDef",
    {
        "ComparisonMethod": NotRequired[ComparisonMethodType],
        "ComparisonFormat": NotRequired[ComparisonFormatConfigurationTypeDef],
    },
)

DateTimeFormatConfigurationTypeDef = TypedDict(
    "DateTimeFormatConfigurationTypeDef",
    {
        "DateTimeFormat": NotRequired[str],
        "NullValueFormatConfiguration": NotRequired[NullValueFormatConfigurationTypeDef],
        "NumericFormatConfiguration": NotRequired[NumericFormatConfigurationTypeDef],
    },
)

NumberFormatConfigurationTypeDef = TypedDict(
    "NumberFormatConfigurationTypeDef",
    {
        "FormatConfiguration": NotRequired[NumericFormatConfigurationTypeDef],
    },
)

ReferenceLineValueLabelConfigurationTypeDef = TypedDict(
    "ReferenceLineValueLabelConfigurationTypeDef",
    {
        "RelativePosition": NotRequired[ReferenceLineValueLabelRelativePositionType],
        "FormatConfiguration": NotRequired[NumericFormatConfigurationTypeDef],
    },
)

StringFormatConfigurationTypeDef = TypedDict(
    "StringFormatConfigurationTypeDef",
    {
        "NullValueFormatConfiguration": NotRequired[NullValueFormatConfigurationTypeDef],
        "NumericFormatConfiguration": NotRequired[NumericFormatConfigurationTypeDef],
    },
)

TopBottomFilterTypeDef = TypedDict(
    "TopBottomFilterTypeDef",
    {
        "FilterId": str,
        "Column": ColumnIdentifierTypeDef,
        "AggregationSortConfigurations": Sequence[AggregationSortConfigurationTypeDef],
        "Limit": NotRequired[int],
        "TimeGranularity": NotRequired[TimeGranularityType],
        "ParameterName": NotRequired[str],
    },
)

FieldSortOptionsTypeDef = TypedDict(
    "FieldSortOptionsTypeDef",
    {
        "FieldSort": NotRequired[FieldSortTypeDef],
        "ColumnSort": NotRequired[ColumnSortTypeDef],
    },
)

PivotTableSortByTypeDef = TypedDict(
    "PivotTableSortByTypeDef",
    {
        "Field": NotRequired[FieldSortTypeDef],
        "Column": NotRequired[ColumnSortTypeDef],
        "DataPath": NotRequired[DataPathSortTypeDef],
    },
)

TooltipItemTypeDef = TypedDict(
    "TooltipItemTypeDef",
    {
        "FieldTooltipItem": NotRequired[FieldTooltipItemTypeDef],
        "ColumnTooltipItem": NotRequired[ColumnTooltipItemTypeDef],
    },
)

ReferenceLineDataConfigurationTypeDef = TypedDict(
    "ReferenceLineDataConfigurationTypeDef",
    {
        "StaticConfiguration": NotRequired[ReferenceLineStaticDataConfigurationTypeDef],
        "DynamicConfiguration": NotRequired[ReferenceLineDynamicDataConfigurationTypeDef],
        "AxisBinding": NotRequired[AxisBindingType],
    },
)

DatasetMetadataTypeDef = TypedDict(
    "DatasetMetadataTypeDef",
    {
        "DatasetArn": str,
        "DatasetName": NotRequired[str],
        "DatasetDescription": NotRequired[str],
        "DataAggregation": NotRequired[DataAggregationTypeDef],
        "Filters": NotRequired[Sequence[TopicFilterTypeDef]],
        "Columns": NotRequired[Sequence[TopicColumnTypeDef]],
        "CalculatedFields": NotRequired[Sequence[TopicCalculatedFieldTypeDef]],
        "NamedEntities": NotRequired[Sequence[TopicNamedEntityTypeDef]],
    },
)

ListDataSourcesResponsePaginatorTypeDef = TypedDict(
    "ListDataSourcesResponsePaginatorTypeDef",
    {
        "DataSources": List[DataSourcePaginatorTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssetBundleImportJobOverrideParametersTypeDef = TypedDict(
    "AssetBundleImportJobOverrideParametersTypeDef",
    {
        "ResourceIdOverrideConfiguration": NotRequired[
            AssetBundleImportJobResourceIdOverrideConfigurationTypeDef
        ],
        "VPCConnections": NotRequired[
            List[AssetBundleImportJobVPCConnectionOverrideParametersTypeDef]
        ],
        "RefreshSchedules": NotRequired[
            List[AssetBundleImportJobRefreshScheduleOverrideParametersTypeDef]
        ],
        "DataSources": NotRequired[List[AssetBundleImportJobDataSourceOverrideParametersTypeDef]],
        "DataSets": NotRequired[List[AssetBundleImportJobDataSetOverrideParametersTypeDef]],
        "Themes": NotRequired[List[AssetBundleImportJobThemeOverrideParametersTypeDef]],
        "Analyses": NotRequired[List[AssetBundleImportJobAnalysisOverrideParametersTypeDef]],
        "Dashboards": NotRequired[List[AssetBundleImportJobDashboardOverrideParametersTypeDef]],
    },
)

DataSourceCredentialsTypeDef = TypedDict(
    "DataSourceCredentialsTypeDef",
    {
        "CredentialPair": NotRequired[CredentialPairTypeDef],
        "CopySourceArn": NotRequired[str],
        "SecretArn": NotRequired[str],
    },
)

DescribeDataSourceResponseTypeDef = TypedDict(
    "DescribeDataSourceResponseTypeDef",
    {
        "DataSource": DataSourceTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDataSourcesResponseTypeDef = TypedDict(
    "ListDataSourcesResponseTypeDef",
    {
        "DataSources": List[DataSourceTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateEmbedUrlForRegisteredUserRequestRequestTypeDef = TypedDict(
    "GenerateEmbedUrlForRegisteredUserRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "UserArn": str,
        "ExperienceConfiguration": RegisteredUserEmbeddingExperienceConfigurationTypeDef,
        "SessionLifetimeInMinutes": NotRequired[int],
        "AllowedDomains": NotRequired[Sequence[str]],
    },
)

AnonymousUserSnapshotJobResultTypeDef = TypedDict(
    "AnonymousUserSnapshotJobResultTypeDef",
    {
        "FileGroups": NotRequired[List[SnapshotJobResultFileGroupTypeDef]],
    },
)

DefaultPaginatedLayoutConfigurationTypeDef = TypedDict(
    "DefaultPaginatedLayoutConfigurationTypeDef",
    {
        "SectionBased": NotRequired[DefaultSectionBasedLayoutConfigurationTypeDef],
    },
)

SectionLayoutConfigurationTypeDef = TypedDict(
    "SectionLayoutConfigurationTypeDef",
    {
        "FreeFormLayout": FreeFormSectionLayoutConfigurationTypeDef,
    },
)

DescribeDashboardSnapshotJobResponseTypeDef = TypedDict(
    "DescribeDashboardSnapshotJobResponseTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "SnapshotJobId": str,
        "UserConfiguration": SnapshotUserConfigurationRedactedTypeDef,
        "SnapshotConfiguration": SnapshotConfigurationTypeDef,
        "Arn": str,
        "JobStatus": SnapshotJobStatusType,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartDashboardSnapshotJobRequestRequestTypeDef = TypedDict(
    "StartDashboardSnapshotJobRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "SnapshotJobId": str,
        "UserConfiguration": SnapshotUserConfigurationTypeDef,
        "SnapshotConfiguration": SnapshotConfigurationTypeDef,
    },
)

DescribeTemplateResponseTypeDef = TypedDict(
    "DescribeTemplateResponseTypeDef",
    {
        "Template": TemplateTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CustomActionSetParametersOperationTypeDef = TypedDict(
    "CustomActionSetParametersOperationTypeDef",
    {
        "ParameterValueConfigurations": Sequence[SetParameterValueConfigurationTypeDef],
    },
)

CreateDataSetRequestRequestTypeDef = TypedDict(
    "CreateDataSetRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
        "Name": str,
        "PhysicalTableMap": Mapping[str, PhysicalTableTypeDef],
        "ImportMode": DataSetImportModeType,
        "LogicalTableMap": NotRequired[Mapping[str, LogicalTableTypeDef]],
        "ColumnGroups": NotRequired[Sequence[ColumnGroupTypeDef]],
        "FieldFolders": NotRequired[Mapping[str, FieldFolderTypeDef]],
        "Permissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
        "RowLevelPermissionDataSet": NotRequired[RowLevelPermissionDataSetTypeDef],
        "RowLevelPermissionTagConfiguration": NotRequired[
            RowLevelPermissionTagConfigurationTypeDef
        ],
        "ColumnLevelPermissionRules": NotRequired[Sequence[ColumnLevelPermissionRuleTypeDef]],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "DataSetUsageConfiguration": NotRequired[DataSetUsageConfigurationTypeDef],
        "DatasetParameters": NotRequired[Sequence[DatasetParameterTypeDef]],
    },
)

DataSetTypeDef = TypedDict(
    "DataSetTypeDef",
    {
        "Arn": NotRequired[str],
        "DataSetId": NotRequired[str],
        "Name": NotRequired[str],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
        "PhysicalTableMap": NotRequired[Dict[str, PhysicalTableTypeDef]],
        "LogicalTableMap": NotRequired[Dict[str, LogicalTableTypeDef]],
        "OutputColumns": NotRequired[List[OutputColumnTypeDef]],
        "ImportMode": NotRequired[DataSetImportModeType],
        "ConsumedSpiceCapacityInBytes": NotRequired[int],
        "ColumnGroups": NotRequired[List[ColumnGroupTypeDef]],
        "FieldFolders": NotRequired[Dict[str, FieldFolderTypeDef]],
        "RowLevelPermissionDataSet": NotRequired[RowLevelPermissionDataSetTypeDef],
        "RowLevelPermissionTagConfiguration": NotRequired[
            RowLevelPermissionTagConfigurationTypeDef
        ],
        "ColumnLevelPermissionRules": NotRequired[List[ColumnLevelPermissionRuleTypeDef]],
        "DataSetUsageConfiguration": NotRequired[DataSetUsageConfigurationTypeDef],
        "DatasetParameters": NotRequired[List[DatasetParameterTypeDef]],
    },
)

UpdateDataSetRequestRequestTypeDef = TypedDict(
    "UpdateDataSetRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
        "Name": str,
        "PhysicalTableMap": Mapping[str, PhysicalTableTypeDef],
        "ImportMode": DataSetImportModeType,
        "LogicalTableMap": NotRequired[Mapping[str, LogicalTableTypeDef]],
        "ColumnGroups": NotRequired[Sequence[ColumnGroupTypeDef]],
        "FieldFolders": NotRequired[Mapping[str, FieldFolderTypeDef]],
        "RowLevelPermissionDataSet": NotRequired[RowLevelPermissionDataSetTypeDef],
        "RowLevelPermissionTagConfiguration": NotRequired[
            RowLevelPermissionTagConfigurationTypeDef
        ],
        "ColumnLevelPermissionRules": NotRequired[Sequence[ColumnLevelPermissionRuleTypeDef]],
        "DataSetUsageConfiguration": NotRequired[DataSetUsageConfigurationTypeDef],
        "DatasetParameters": NotRequired[Sequence[DatasetParameterTypeDef]],
    },
)

LineSeriesAxisDisplayOptionsTypeDef = TypedDict(
    "LineSeriesAxisDisplayOptionsTypeDef",
    {
        "AxisOptions": NotRequired[AxisDisplayOptionsTypeDef],
        "MissingDataConfigurations": NotRequired[Sequence[MissingDataConfigurationTypeDef]],
    },
)

FilterControlTypeDef = TypedDict(
    "FilterControlTypeDef",
    {
        "DateTimePicker": NotRequired[FilterDateTimePickerControlTypeDef],
        "List": NotRequired[FilterListControlTypeDef],
        "Dropdown": NotRequired[FilterDropDownControlTypeDef],
        "TextField": NotRequired[FilterTextFieldControlTypeDef],
        "TextArea": NotRequired[FilterTextAreaControlTypeDef],
        "Slider": NotRequired[FilterSliderControlTypeDef],
        "RelativeDateTime": NotRequired[FilterRelativeDateTimeControlTypeDef],
    },
)

ParameterControlTypeDef = TypedDict(
    "ParameterControlTypeDef",
    {
        "DateTimePicker": NotRequired[ParameterDateTimePickerControlTypeDef],
        "List": NotRequired[ParameterListControlTypeDef],
        "Dropdown": NotRequired[ParameterDropDownControlTypeDef],
        "TextField": NotRequired[ParameterTextFieldControlTypeDef],
        "TextArea": NotRequired[ParameterTextAreaControlTypeDef],
        "Slider": NotRequired[ParameterSliderControlTypeDef],
    },
)

TableFieldURLConfigurationTypeDef = TypedDict(
    "TableFieldURLConfigurationTypeDef",
    {
        "LinkConfiguration": NotRequired[TableFieldLinkConfigurationTypeDef],
        "ImageConfiguration": NotRequired[TableFieldImageConfigurationTypeDef],
    },
)

PivotTableTotalOptionsTypeDef = TypedDict(
    "PivotTableTotalOptionsTypeDef",
    {
        "RowSubtotalOptions": NotRequired[SubtotalOptionsTypeDef],
        "ColumnSubtotalOptions": NotRequired[SubtotalOptionsTypeDef],
        "RowTotalOptions": NotRequired[PivotTotalOptionsTypeDef],
        "ColumnTotalOptions": NotRequired[PivotTotalOptionsTypeDef],
    },
)

GaugeChartConditionalFormattingOptionTypeDef = TypedDict(
    "GaugeChartConditionalFormattingOptionTypeDef",
    {
        "PrimaryValue": NotRequired[GaugeChartPrimaryValueConditionalFormattingTypeDef],
        "Arc": NotRequired[GaugeChartArcConditionalFormattingTypeDef],
    },
)

KPIConditionalFormattingOptionTypeDef = TypedDict(
    "KPIConditionalFormattingOptionTypeDef",
    {
        "PrimaryValue": NotRequired[KPIPrimaryValueConditionalFormattingTypeDef],
        "ProgressBar": NotRequired[KPIProgressBarConditionalFormattingTypeDef],
        "ActualValue": NotRequired[KPIActualValueConditionalFormattingTypeDef],
        "ComparisonValue": NotRequired[KPIComparisonValueConditionalFormattingTypeDef],
    },
)

FilledMapShapeConditionalFormattingTypeDef = TypedDict(
    "FilledMapShapeConditionalFormattingTypeDef",
    {
        "FieldId": str,
        "Format": NotRequired[ShapeConditionalFormatTypeDef],
    },
)

PivotTableCellConditionalFormattingTypeDef = TypedDict(
    "PivotTableCellConditionalFormattingTypeDef",
    {
        "FieldId": str,
        "TextFormat": NotRequired[TextConditionalFormatTypeDef],
        "Scope": NotRequired[PivotTableConditionalFormattingScopeTypeDef],
        "Scopes": NotRequired[Sequence[PivotTableConditionalFormattingScopeTypeDef]],
    },
)

TableCellConditionalFormattingTypeDef = TypedDict(
    "TableCellConditionalFormattingTypeDef",
    {
        "FieldId": str,
        "TextFormat": NotRequired[TextConditionalFormatTypeDef],
    },
)

ThemeTypeDef = TypedDict(
    "ThemeTypeDef",
    {
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "ThemeId": NotRequired[str],
        "Version": NotRequired[ThemeVersionTypeDef],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
        "Type": NotRequired[ThemeTypeType],
    },
)

GaugeChartOptionsTypeDef = TypedDict(
    "GaugeChartOptionsTypeDef",
    {
        "PrimaryValueDisplayType": NotRequired[PrimaryValueDisplayTypeType],
        "Comparison": NotRequired[ComparisonConfigurationTypeDef],
        "ArcAxis": NotRequired[ArcAxisConfigurationTypeDef],
        "Arc": NotRequired[ArcConfigurationTypeDef],
        "PrimaryValueFontConfiguration": NotRequired[FontConfigurationTypeDef],
    },
)

KPIOptionsTypeDef = TypedDict(
    "KPIOptionsTypeDef",
    {
        "ProgressBar": NotRequired[ProgressBarOptionsTypeDef],
        "TrendArrows": NotRequired[TrendArrowOptionsTypeDef],
        "SecondaryValue": NotRequired[SecondaryValueOptionsTypeDef],
        "Comparison": NotRequired[ComparisonConfigurationTypeDef],
        "PrimaryValueDisplayType": NotRequired[PrimaryValueDisplayTypeType],
        "PrimaryValueFontConfiguration": NotRequired[FontConfigurationTypeDef],
        "SecondaryValueFontConfiguration": NotRequired[FontConfigurationTypeDef],
        "Sparkline": NotRequired[KPISparklineOptionsTypeDef],
        "VisualLayoutOptions": NotRequired[KPIVisualLayoutOptionsTypeDef],
    },
)

DateDimensionFieldTypeDef = TypedDict(
    "DateDimensionFieldTypeDef",
    {
        "FieldId": str,
        "Column": ColumnIdentifierTypeDef,
        "DateGranularity": NotRequired[TimeGranularityType],
        "HierarchyId": NotRequired[str],
        "FormatConfiguration": NotRequired[DateTimeFormatConfigurationTypeDef],
    },
)

DateMeasureFieldTypeDef = TypedDict(
    "DateMeasureFieldTypeDef",
    {
        "FieldId": str,
        "Column": ColumnIdentifierTypeDef,
        "AggregationFunction": NotRequired[DateAggregationFunctionType],
        "FormatConfiguration": NotRequired[DateTimeFormatConfigurationTypeDef],
    },
)

NumericalDimensionFieldTypeDef = TypedDict(
    "NumericalDimensionFieldTypeDef",
    {
        "FieldId": str,
        "Column": ColumnIdentifierTypeDef,
        "HierarchyId": NotRequired[str],
        "FormatConfiguration": NotRequired[NumberFormatConfigurationTypeDef],
    },
)

NumericalMeasureFieldTypeDef = TypedDict(
    "NumericalMeasureFieldTypeDef",
    {
        "FieldId": str,
        "Column": ColumnIdentifierTypeDef,
        "AggregationFunction": NotRequired[NumericalAggregationFunctionTypeDef],
        "FormatConfiguration": NotRequired[NumberFormatConfigurationTypeDef],
    },
)

ReferenceLineLabelConfigurationTypeDef = TypedDict(
    "ReferenceLineLabelConfigurationTypeDef",
    {
        "ValueLabelConfiguration": NotRequired[ReferenceLineValueLabelConfigurationTypeDef],
        "CustomLabelConfiguration": NotRequired[ReferenceLineCustomLabelConfigurationTypeDef],
        "FontConfiguration": NotRequired[FontConfigurationTypeDef],
        "FontColor": NotRequired[str],
        "HorizontalPosition": NotRequired[ReferenceLineLabelHorizontalPositionType],
        "VerticalPosition": NotRequired[ReferenceLineLabelVerticalPositionType],
    },
)

CategoricalDimensionFieldTypeDef = TypedDict(
    "CategoricalDimensionFieldTypeDef",
    {
        "FieldId": str,
        "Column": ColumnIdentifierTypeDef,
        "HierarchyId": NotRequired[str],
        "FormatConfiguration": NotRequired[StringFormatConfigurationTypeDef],
    },
)

CategoricalMeasureFieldTypeDef = TypedDict(
    "CategoricalMeasureFieldTypeDef",
    {
        "FieldId": str,
        "Column": ColumnIdentifierTypeDef,
        "AggregationFunction": NotRequired[CategoricalAggregationFunctionType],
        "FormatConfiguration": NotRequired[StringFormatConfigurationTypeDef],
    },
)

FormatConfigurationTypeDef = TypedDict(
    "FormatConfigurationTypeDef",
    {
        "StringFormatConfiguration": NotRequired[StringFormatConfigurationTypeDef],
        "NumberFormatConfiguration": NotRequired[NumberFormatConfigurationTypeDef],
        "DateTimeFormatConfiguration": NotRequired[DateTimeFormatConfigurationTypeDef],
    },
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "CategoryFilter": NotRequired[CategoryFilterTypeDef],
        "NumericRangeFilter": NotRequired[NumericRangeFilterTypeDef],
        "NumericEqualityFilter": NotRequired[NumericEqualityFilterTypeDef],
        "TimeEqualityFilter": NotRequired[TimeEqualityFilterTypeDef],
        "TimeRangeFilter": NotRequired[TimeRangeFilterTypeDef],
        "RelativeDatesFilter": NotRequired[RelativeDatesFilterTypeDef],
        "TopBottomFilter": NotRequired[TopBottomFilterTypeDef],
    },
)

BarChartSortConfigurationTypeDef = TypedDict(
    "BarChartSortConfigurationTypeDef",
    {
        "CategorySort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "CategoryItemsLimit": NotRequired[ItemsLimitConfigurationTypeDef],
        "ColorSort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "ColorItemsLimit": NotRequired[ItemsLimitConfigurationTypeDef],
        "SmallMultiplesSort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "SmallMultiplesLimitConfiguration": NotRequired[ItemsLimitConfigurationTypeDef],
    },
)

BoxPlotSortConfigurationTypeDef = TypedDict(
    "BoxPlotSortConfigurationTypeDef",
    {
        "CategorySort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "PaginationConfiguration": NotRequired[PaginationConfigurationTypeDef],
    },
)

ComboChartSortConfigurationTypeDef = TypedDict(
    "ComboChartSortConfigurationTypeDef",
    {
        "CategorySort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "CategoryItemsLimit": NotRequired[ItemsLimitConfigurationTypeDef],
        "ColorSort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "ColorItemsLimit": NotRequired[ItemsLimitConfigurationTypeDef],
    },
)

FilledMapSortConfigurationTypeDef = TypedDict(
    "FilledMapSortConfigurationTypeDef",
    {
        "CategorySort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
    },
)

FunnelChartSortConfigurationTypeDef = TypedDict(
    "FunnelChartSortConfigurationTypeDef",
    {
        "CategorySort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "CategoryItemsLimit": NotRequired[ItemsLimitConfigurationTypeDef],
    },
)

HeatMapSortConfigurationTypeDef = TypedDict(
    "HeatMapSortConfigurationTypeDef",
    {
        "HeatMapRowSort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "HeatMapColumnSort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "HeatMapRowItemsLimitConfiguration": NotRequired[ItemsLimitConfigurationTypeDef],
        "HeatMapColumnItemsLimitConfiguration": NotRequired[ItemsLimitConfigurationTypeDef],
    },
)

KPISortConfigurationTypeDef = TypedDict(
    "KPISortConfigurationTypeDef",
    {
        "TrendGroupSort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
    },
)

LineChartSortConfigurationTypeDef = TypedDict(
    "LineChartSortConfigurationTypeDef",
    {
        "CategorySort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "CategoryItemsLimitConfiguration": NotRequired[ItemsLimitConfigurationTypeDef],
        "ColorItemsLimitConfiguration": NotRequired[ItemsLimitConfigurationTypeDef],
        "SmallMultiplesSort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "SmallMultiplesLimitConfiguration": NotRequired[ItemsLimitConfigurationTypeDef],
    },
)

PieChartSortConfigurationTypeDef = TypedDict(
    "PieChartSortConfigurationTypeDef",
    {
        "CategorySort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "CategoryItemsLimit": NotRequired[ItemsLimitConfigurationTypeDef],
        "SmallMultiplesSort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "SmallMultiplesLimitConfiguration": NotRequired[ItemsLimitConfigurationTypeDef],
    },
)

RadarChartSortConfigurationTypeDef = TypedDict(
    "RadarChartSortConfigurationTypeDef",
    {
        "CategorySort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "CategoryItemsLimit": NotRequired[ItemsLimitConfigurationTypeDef],
        "ColorSort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "ColorItemsLimit": NotRequired[ItemsLimitConfigurationTypeDef],
    },
)

SankeyDiagramSortConfigurationTypeDef = TypedDict(
    "SankeyDiagramSortConfigurationTypeDef",
    {
        "WeightSort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "SourceItemsLimit": NotRequired[ItemsLimitConfigurationTypeDef],
        "DestinationItemsLimit": NotRequired[ItemsLimitConfigurationTypeDef],
    },
)

TableSortConfigurationTypeDef = TypedDict(
    "TableSortConfigurationTypeDef",
    {
        "RowSort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "PaginationConfiguration": NotRequired[PaginationConfigurationTypeDef],
    },
)

TreeMapSortConfigurationTypeDef = TypedDict(
    "TreeMapSortConfigurationTypeDef",
    {
        "TreeMapSort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "TreeMapGroupItemsLimitConfiguration": NotRequired[ItemsLimitConfigurationTypeDef],
    },
)

WaterfallChartSortConfigurationTypeDef = TypedDict(
    "WaterfallChartSortConfigurationTypeDef",
    {
        "CategorySort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
        "BreakdownItemsLimit": NotRequired[ItemsLimitConfigurationTypeDef],
    },
)

WordCloudSortConfigurationTypeDef = TypedDict(
    "WordCloudSortConfigurationTypeDef",
    {
        "CategoryItemsLimit": NotRequired[ItemsLimitConfigurationTypeDef],
        "CategorySort": NotRequired[Sequence[FieldSortOptionsTypeDef]],
    },
)

PivotFieldSortOptionsTypeDef = TypedDict(
    "PivotFieldSortOptionsTypeDef",
    {
        "FieldId": str,
        "SortBy": PivotTableSortByTypeDef,
    },
)

FieldBasedTooltipTypeDef = TypedDict(
    "FieldBasedTooltipTypeDef",
    {
        "AggregationVisibility": NotRequired[VisibilityType],
        "TooltipTitleType": NotRequired[TooltipTitleTypeType],
        "TooltipFields": NotRequired[Sequence[TooltipItemTypeDef]],
    },
)

TopicDetailsTypeDef = TypedDict(
    "TopicDetailsTypeDef",
    {
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "DataSets": NotRequired[Sequence[DatasetMetadataTypeDef]],
    },
)

DescribeAssetBundleImportJobResponseTypeDef = TypedDict(
    "DescribeAssetBundleImportJobResponseTypeDef",
    {
        "JobStatus": AssetBundleImportJobStatusType,
        "Errors": List[AssetBundleImportJobErrorTypeDef],
        "RollbackErrors": List[AssetBundleImportJobErrorTypeDef],
        "Arn": str,
        "CreatedTime": datetime,
        "AssetBundleImportJobId": str,
        "AwsAccountId": str,
        "AssetBundleImportSource": AssetBundleImportSourceDescriptionTypeDef,
        "OverrideParameters": AssetBundleImportJobOverrideParametersTypeDef,
        "FailureAction": AssetBundleImportFailureActionType,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartAssetBundleImportJobRequestRequestTypeDef = TypedDict(
    "StartAssetBundleImportJobRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AssetBundleImportJobId": str,
        "AssetBundleImportSource": AssetBundleImportSourceTypeDef,
        "OverrideParameters": NotRequired[AssetBundleImportJobOverrideParametersTypeDef],
        "FailureAction": NotRequired[AssetBundleImportFailureActionType],
    },
)

CreateDataSourceRequestRequestTypeDef = TypedDict(
    "CreateDataSourceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
        "Name": str,
        "Type": DataSourceTypeType,
        "DataSourceParameters": NotRequired[DataSourceParametersTypeDef],
        "Credentials": NotRequired[DataSourceCredentialsTypeDef],
        "Permissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
        "VpcConnectionProperties": NotRequired[VpcConnectionPropertiesTypeDef],
        "SslProperties": NotRequired[SslPropertiesTypeDef],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

UpdateDataSourceRequestRequestTypeDef = TypedDict(
    "UpdateDataSourceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
        "Name": str,
        "DataSourceParameters": NotRequired[DataSourceParametersTypeDef],
        "Credentials": NotRequired[DataSourceCredentialsTypeDef],
        "VpcConnectionProperties": NotRequired[VpcConnectionPropertiesTypeDef],
        "SslProperties": NotRequired[SslPropertiesTypeDef],
    },
)

SnapshotJobResultTypeDef = TypedDict(
    "SnapshotJobResultTypeDef",
    {
        "AnonymousUsers": NotRequired[List[AnonymousUserSnapshotJobResultTypeDef]],
    },
)

DefaultNewSheetConfigurationTypeDef = TypedDict(
    "DefaultNewSheetConfigurationTypeDef",
    {
        "InteractiveLayoutConfiguration": NotRequired[DefaultInteractiveLayoutConfigurationTypeDef],
        "PaginatedLayoutConfiguration": NotRequired[DefaultPaginatedLayoutConfigurationTypeDef],
        "SheetContentType": NotRequired[SheetContentTypeType],
    },
)

BodySectionContentTypeDef = TypedDict(
    "BodySectionContentTypeDef",
    {
        "Layout": NotRequired[SectionLayoutConfigurationTypeDef],
    },
)

HeaderFooterSectionConfigurationTypeDef = TypedDict(
    "HeaderFooterSectionConfigurationTypeDef",
    {
        "SectionId": str,
        "Layout": SectionLayoutConfigurationTypeDef,
        "Style": NotRequired[SectionStyleTypeDef],
    },
)

VisualCustomActionOperationTypeDef = TypedDict(
    "VisualCustomActionOperationTypeDef",
    {
        "FilterOperation": NotRequired[CustomActionFilterOperationTypeDef],
        "NavigationOperation": NotRequired[CustomActionNavigationOperationTypeDef],
        "URLOperation": NotRequired[CustomActionURLOperationTypeDef],
        "SetParametersOperation": NotRequired[CustomActionSetParametersOperationTypeDef],
    },
)

DescribeDataSetResponseTypeDef = TypedDict(
    "DescribeDataSetResponseTypeDef",
    {
        "DataSet": DataSetTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TableFieldOptionTypeDef = TypedDict(
    "TableFieldOptionTypeDef",
    {
        "FieldId": str,
        "Width": NotRequired[str],
        "CustomLabel": NotRequired[str],
        "Visibility": NotRequired[VisibilityType],
        "URLStyling": NotRequired[TableFieldURLConfigurationTypeDef],
    },
)

GaugeChartConditionalFormattingTypeDef = TypedDict(
    "GaugeChartConditionalFormattingTypeDef",
    {
        "ConditionalFormattingOptions": NotRequired[
            Sequence[GaugeChartConditionalFormattingOptionTypeDef]
        ],
    },
)

KPIConditionalFormattingTypeDef = TypedDict(
    "KPIConditionalFormattingTypeDef",
    {
        "ConditionalFormattingOptions": NotRequired[
            Sequence[KPIConditionalFormattingOptionTypeDef]
        ],
    },
)

FilledMapConditionalFormattingOptionTypeDef = TypedDict(
    "FilledMapConditionalFormattingOptionTypeDef",
    {
        "Shape": FilledMapShapeConditionalFormattingTypeDef,
    },
)

PivotTableConditionalFormattingOptionTypeDef = TypedDict(
    "PivotTableConditionalFormattingOptionTypeDef",
    {
        "Cell": NotRequired[PivotTableCellConditionalFormattingTypeDef],
    },
)

TableConditionalFormattingOptionTypeDef = TypedDict(
    "TableConditionalFormattingOptionTypeDef",
    {
        "Cell": NotRequired[TableCellConditionalFormattingTypeDef],
        "Row": NotRequired[TableRowConditionalFormattingTypeDef],
    },
)

DescribeThemeResponseTypeDef = TypedDict(
    "DescribeThemeResponseTypeDef",
    {
        "Theme": ThemeTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReferenceLineTypeDef = TypedDict(
    "ReferenceLineTypeDef",
    {
        "DataConfiguration": ReferenceLineDataConfigurationTypeDef,
        "Status": NotRequired[WidgetStatusType],
        "StyleConfiguration": NotRequired[ReferenceLineStyleConfigurationTypeDef],
        "LabelConfiguration": NotRequired[ReferenceLineLabelConfigurationTypeDef],
    },
)

DimensionFieldTypeDef = TypedDict(
    "DimensionFieldTypeDef",
    {
        "NumericalDimensionField": NotRequired[NumericalDimensionFieldTypeDef],
        "CategoricalDimensionField": NotRequired[CategoricalDimensionFieldTypeDef],
        "DateDimensionField": NotRequired[DateDimensionFieldTypeDef],
    },
)

MeasureFieldTypeDef = TypedDict(
    "MeasureFieldTypeDef",
    {
        "NumericalMeasureField": NotRequired[NumericalMeasureFieldTypeDef],
        "CategoricalMeasureField": NotRequired[CategoricalMeasureFieldTypeDef],
        "DateMeasureField": NotRequired[DateMeasureFieldTypeDef],
        "CalculatedMeasureField": NotRequired[CalculatedMeasureFieldTypeDef],
    },
)

ColumnConfigurationTypeDef = TypedDict(
    "ColumnConfigurationTypeDef",
    {
        "Column": ColumnIdentifierTypeDef,
        "FormatConfiguration": NotRequired[FormatConfigurationTypeDef],
        "Role": NotRequired[ColumnRoleType],
        "ColorsConfiguration": NotRequired[ColorsConfigurationTypeDef],
    },
)

UnaggregatedFieldTypeDef = TypedDict(
    "UnaggregatedFieldTypeDef",
    {
        "FieldId": str,
        "Column": ColumnIdentifierTypeDef,
        "FormatConfiguration": NotRequired[FormatConfigurationTypeDef],
    },
)

FilterGroupTypeDef = TypedDict(
    "FilterGroupTypeDef",
    {
        "FilterGroupId": str,
        "Filters": Sequence[FilterTypeDef],
        "ScopeConfiguration": FilterScopeConfigurationTypeDef,
        "CrossDataset": CrossDatasetTypesType,
        "Status": NotRequired[WidgetStatusType],
    },
)

PivotTableSortConfigurationTypeDef = TypedDict(
    "PivotTableSortConfigurationTypeDef",
    {
        "FieldSortOptions": NotRequired[Sequence[PivotFieldSortOptionsTypeDef]],
    },
)

TooltipOptionsTypeDef = TypedDict(
    "TooltipOptionsTypeDef",
    {
        "TooltipVisibility": NotRequired[VisibilityType],
        "SelectedTooltipType": NotRequired[SelectedTooltipTypeType],
        "FieldBasedTooltip": NotRequired[FieldBasedTooltipTypeDef],
    },
)

CreateTopicRequestRequestTypeDef = TypedDict(
    "CreateTopicRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TopicId": str,
        "Topic": TopicDetailsTypeDef,
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

DescribeTopicResponseTypeDef = TypedDict(
    "DescribeTopicResponseTypeDef",
    {
        "Arn": str,
        "TopicId": str,
        "Topic": TopicDetailsTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTopicRequestRequestTypeDef = TypedDict(
    "UpdateTopicRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TopicId": str,
        "Topic": TopicDetailsTypeDef,
    },
)

DescribeDashboardSnapshotJobResultResponseTypeDef = TypedDict(
    "DescribeDashboardSnapshotJobResultResponseTypeDef",
    {
        "Arn": str,
        "JobStatus": SnapshotJobStatusType,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "Result": SnapshotJobResultTypeDef,
        "ErrorInfo": SnapshotJobErrorInfoTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AnalysisDefaultsTypeDef = TypedDict(
    "AnalysisDefaultsTypeDef",
    {
        "DefaultNewSheetConfiguration": DefaultNewSheetConfigurationTypeDef,
    },
)

BodySectionConfigurationTypeDef = TypedDict(
    "BodySectionConfigurationTypeDef",
    {
        "SectionId": str,
        "Content": BodySectionContentTypeDef,
        "Style": NotRequired[SectionStyleTypeDef],
        "PageBreakConfiguration": NotRequired[SectionPageBreakConfigurationTypeDef],
    },
)

VisualCustomActionTypeDef = TypedDict(
    "VisualCustomActionTypeDef",
    {
        "CustomActionId": str,
        "Name": str,
        "Trigger": VisualCustomActionTriggerType,
        "ActionOperations": Sequence[VisualCustomActionOperationTypeDef],
        "Status": NotRequired[WidgetStatusType],
    },
)

TableFieldOptionsTypeDef = TypedDict(
    "TableFieldOptionsTypeDef",
    {
        "SelectedFieldOptions": NotRequired[Sequence[TableFieldOptionTypeDef]],
        "Order": NotRequired[Sequence[str]],
        "PinnedFieldOptions": NotRequired[TablePinnedFieldOptionsTypeDef],
    },
)

FilledMapConditionalFormattingTypeDef = TypedDict(
    "FilledMapConditionalFormattingTypeDef",
    {
        "ConditionalFormattingOptions": Sequence[FilledMapConditionalFormattingOptionTypeDef],
    },
)

PivotTableConditionalFormattingTypeDef = TypedDict(
    "PivotTableConditionalFormattingTypeDef",
    {
        "ConditionalFormattingOptions": NotRequired[
            Sequence[PivotTableConditionalFormattingOptionTypeDef]
        ],
    },
)

TableConditionalFormattingTypeDef = TypedDict(
    "TableConditionalFormattingTypeDef",
    {
        "ConditionalFormattingOptions": NotRequired[
            Sequence[TableConditionalFormattingOptionTypeDef]
        ],
    },
)

UniqueValuesComputationTypeDef = TypedDict(
    "UniqueValuesComputationTypeDef",
    {
        "ComputationId": str,
        "Name": NotRequired[str],
        "Category": NotRequired[DimensionFieldTypeDef],
    },
)

BarChartAggregatedFieldWellsTypeDef = TypedDict(
    "BarChartAggregatedFieldWellsTypeDef",
    {
        "Category": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Values": NotRequired[Sequence[MeasureFieldTypeDef]],
        "Colors": NotRequired[Sequence[DimensionFieldTypeDef]],
        "SmallMultiples": NotRequired[Sequence[DimensionFieldTypeDef]],
    },
)

BoxPlotAggregatedFieldWellsTypeDef = TypedDict(
    "BoxPlotAggregatedFieldWellsTypeDef",
    {
        "GroupBy": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Values": NotRequired[Sequence[MeasureFieldTypeDef]],
    },
)

ComboChartAggregatedFieldWellsTypeDef = TypedDict(
    "ComboChartAggregatedFieldWellsTypeDef",
    {
        "Category": NotRequired[Sequence[DimensionFieldTypeDef]],
        "BarValues": NotRequired[Sequence[MeasureFieldTypeDef]],
        "Colors": NotRequired[Sequence[DimensionFieldTypeDef]],
        "LineValues": NotRequired[Sequence[MeasureFieldTypeDef]],
    },
)

FilledMapAggregatedFieldWellsTypeDef = TypedDict(
    "FilledMapAggregatedFieldWellsTypeDef",
    {
        "Geospatial": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Values": NotRequired[Sequence[MeasureFieldTypeDef]],
    },
)

ForecastComputationTypeDef = TypedDict(
    "ForecastComputationTypeDef",
    {
        "ComputationId": str,
        "Name": NotRequired[str],
        "Time": NotRequired[DimensionFieldTypeDef],
        "Value": NotRequired[MeasureFieldTypeDef],
        "PeriodsForward": NotRequired[int],
        "PeriodsBackward": NotRequired[int],
        "UpperBoundary": NotRequired[float],
        "LowerBoundary": NotRequired[float],
        "PredictionInterval": NotRequired[int],
        "Seasonality": NotRequired[ForecastComputationSeasonalityType],
        "CustomSeasonalityValue": NotRequired[int],
    },
)

FunnelChartAggregatedFieldWellsTypeDef = TypedDict(
    "FunnelChartAggregatedFieldWellsTypeDef",
    {
        "Category": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Values": NotRequired[Sequence[MeasureFieldTypeDef]],
    },
)

GaugeChartFieldWellsTypeDef = TypedDict(
    "GaugeChartFieldWellsTypeDef",
    {
        "Values": NotRequired[Sequence[MeasureFieldTypeDef]],
        "TargetValues": NotRequired[Sequence[MeasureFieldTypeDef]],
    },
)

GeospatialMapAggregatedFieldWellsTypeDef = TypedDict(
    "GeospatialMapAggregatedFieldWellsTypeDef",
    {
        "Geospatial": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Values": NotRequired[Sequence[MeasureFieldTypeDef]],
        "Colors": NotRequired[Sequence[DimensionFieldTypeDef]],
    },
)

GrowthRateComputationTypeDef = TypedDict(
    "GrowthRateComputationTypeDef",
    {
        "ComputationId": str,
        "Name": NotRequired[str],
        "Time": NotRequired[DimensionFieldTypeDef],
        "Value": NotRequired[MeasureFieldTypeDef],
        "PeriodSize": NotRequired[int],
    },
)

HeatMapAggregatedFieldWellsTypeDef = TypedDict(
    "HeatMapAggregatedFieldWellsTypeDef",
    {
        "Rows": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Columns": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Values": NotRequired[Sequence[MeasureFieldTypeDef]],
    },
)

HistogramAggregatedFieldWellsTypeDef = TypedDict(
    "HistogramAggregatedFieldWellsTypeDef",
    {
        "Values": NotRequired[Sequence[MeasureFieldTypeDef]],
    },
)

KPIFieldWellsTypeDef = TypedDict(
    "KPIFieldWellsTypeDef",
    {
        "Values": NotRequired[Sequence[MeasureFieldTypeDef]],
        "TargetValues": NotRequired[Sequence[MeasureFieldTypeDef]],
        "TrendGroups": NotRequired[Sequence[DimensionFieldTypeDef]],
    },
)

LineChartAggregatedFieldWellsTypeDef = TypedDict(
    "LineChartAggregatedFieldWellsTypeDef",
    {
        "Category": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Values": NotRequired[Sequence[MeasureFieldTypeDef]],
        "Colors": NotRequired[Sequence[DimensionFieldTypeDef]],
        "SmallMultiples": NotRequired[Sequence[DimensionFieldTypeDef]],
    },
)

MaximumMinimumComputationTypeDef = TypedDict(
    "MaximumMinimumComputationTypeDef",
    {
        "ComputationId": str,
        "Type": MaximumMinimumComputationTypeType,
        "Name": NotRequired[str],
        "Time": NotRequired[DimensionFieldTypeDef],
        "Value": NotRequired[MeasureFieldTypeDef],
    },
)

MetricComparisonComputationTypeDef = TypedDict(
    "MetricComparisonComputationTypeDef",
    {
        "ComputationId": str,
        "Name": NotRequired[str],
        "Time": NotRequired[DimensionFieldTypeDef],
        "FromValue": NotRequired[MeasureFieldTypeDef],
        "TargetValue": NotRequired[MeasureFieldTypeDef],
    },
)

PeriodOverPeriodComputationTypeDef = TypedDict(
    "PeriodOverPeriodComputationTypeDef",
    {
        "ComputationId": str,
        "Name": NotRequired[str],
        "Time": NotRequired[DimensionFieldTypeDef],
        "Value": NotRequired[MeasureFieldTypeDef],
    },
)

PeriodToDateComputationTypeDef = TypedDict(
    "PeriodToDateComputationTypeDef",
    {
        "ComputationId": str,
        "Name": NotRequired[str],
        "Time": NotRequired[DimensionFieldTypeDef],
        "Value": NotRequired[MeasureFieldTypeDef],
        "PeriodTimeGranularity": NotRequired[TimeGranularityType],
    },
)

PieChartAggregatedFieldWellsTypeDef = TypedDict(
    "PieChartAggregatedFieldWellsTypeDef",
    {
        "Category": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Values": NotRequired[Sequence[MeasureFieldTypeDef]],
        "SmallMultiples": NotRequired[Sequence[DimensionFieldTypeDef]],
    },
)

PivotTableAggregatedFieldWellsTypeDef = TypedDict(
    "PivotTableAggregatedFieldWellsTypeDef",
    {
        "Rows": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Columns": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Values": NotRequired[Sequence[MeasureFieldTypeDef]],
    },
)

RadarChartAggregatedFieldWellsTypeDef = TypedDict(
    "RadarChartAggregatedFieldWellsTypeDef",
    {
        "Category": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Color": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Values": NotRequired[Sequence[MeasureFieldTypeDef]],
    },
)

SankeyDiagramAggregatedFieldWellsTypeDef = TypedDict(
    "SankeyDiagramAggregatedFieldWellsTypeDef",
    {
        "Source": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Destination": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Weight": NotRequired[Sequence[MeasureFieldTypeDef]],
    },
)

ScatterPlotCategoricallyAggregatedFieldWellsTypeDef = TypedDict(
    "ScatterPlotCategoricallyAggregatedFieldWellsTypeDef",
    {
        "XAxis": NotRequired[Sequence[MeasureFieldTypeDef]],
        "YAxis": NotRequired[Sequence[MeasureFieldTypeDef]],
        "Category": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Size": NotRequired[Sequence[MeasureFieldTypeDef]],
        "Label": NotRequired[Sequence[DimensionFieldTypeDef]],
    },
)

ScatterPlotUnaggregatedFieldWellsTypeDef = TypedDict(
    "ScatterPlotUnaggregatedFieldWellsTypeDef",
    {
        "XAxis": NotRequired[Sequence[DimensionFieldTypeDef]],
        "YAxis": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Size": NotRequired[Sequence[MeasureFieldTypeDef]],
        "Category": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Label": NotRequired[Sequence[DimensionFieldTypeDef]],
    },
)

TableAggregatedFieldWellsTypeDef = TypedDict(
    "TableAggregatedFieldWellsTypeDef",
    {
        "GroupBy": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Values": NotRequired[Sequence[MeasureFieldTypeDef]],
    },
)

TopBottomMoversComputationTypeDef = TypedDict(
    "TopBottomMoversComputationTypeDef",
    {
        "ComputationId": str,
        "Type": TopBottomComputationTypeType,
        "Name": NotRequired[str],
        "Time": NotRequired[DimensionFieldTypeDef],
        "Category": NotRequired[DimensionFieldTypeDef],
        "Value": NotRequired[MeasureFieldTypeDef],
        "MoverSize": NotRequired[int],
        "SortOrder": NotRequired[TopBottomSortOrderType],
    },
)

TopBottomRankedComputationTypeDef = TypedDict(
    "TopBottomRankedComputationTypeDef",
    {
        "ComputationId": str,
        "Type": TopBottomComputationTypeType,
        "Name": NotRequired[str],
        "Category": NotRequired[DimensionFieldTypeDef],
        "Value": NotRequired[MeasureFieldTypeDef],
        "ResultSize": NotRequired[int],
    },
)

TotalAggregationComputationTypeDef = TypedDict(
    "TotalAggregationComputationTypeDef",
    {
        "ComputationId": str,
        "Name": NotRequired[str],
        "Value": NotRequired[MeasureFieldTypeDef],
    },
)

TreeMapAggregatedFieldWellsTypeDef = TypedDict(
    "TreeMapAggregatedFieldWellsTypeDef",
    {
        "Groups": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Sizes": NotRequired[Sequence[MeasureFieldTypeDef]],
        "Colors": NotRequired[Sequence[MeasureFieldTypeDef]],
    },
)

WaterfallChartAggregatedFieldWellsTypeDef = TypedDict(
    "WaterfallChartAggregatedFieldWellsTypeDef",
    {
        "Categories": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Values": NotRequired[Sequence[MeasureFieldTypeDef]],
        "Breakdowns": NotRequired[Sequence[DimensionFieldTypeDef]],
    },
)

WordCloudAggregatedFieldWellsTypeDef = TypedDict(
    "WordCloudAggregatedFieldWellsTypeDef",
    {
        "GroupBy": NotRequired[Sequence[DimensionFieldTypeDef]],
        "Size": NotRequired[Sequence[MeasureFieldTypeDef]],
    },
)

TableUnaggregatedFieldWellsTypeDef = TypedDict(
    "TableUnaggregatedFieldWellsTypeDef",
    {
        "Values": NotRequired[Sequence[UnaggregatedFieldTypeDef]],
    },
)

SectionBasedLayoutConfigurationTypeDef = TypedDict(
    "SectionBasedLayoutConfigurationTypeDef",
    {
        "HeaderSections": Sequence[HeaderFooterSectionConfigurationTypeDef],
        "BodySections": Sequence[BodySectionConfigurationTypeDef],
        "FooterSections": Sequence[HeaderFooterSectionConfigurationTypeDef],
        "CanvasSizeOptions": SectionBasedLayoutCanvasSizeOptionsTypeDef,
    },
)

CustomContentVisualTypeDef = TypedDict(
    "CustomContentVisualTypeDef",
    {
        "VisualId": str,
        "DataSetIdentifier": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[CustomContentConfigurationTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
    },
)

EmptyVisualTypeDef = TypedDict(
    "EmptyVisualTypeDef",
    {
        "VisualId": str,
        "DataSetIdentifier": str,
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
    },
)

BarChartFieldWellsTypeDef = TypedDict(
    "BarChartFieldWellsTypeDef",
    {
        "BarChartAggregatedFieldWells": NotRequired[BarChartAggregatedFieldWellsTypeDef],
    },
)

BoxPlotFieldWellsTypeDef = TypedDict(
    "BoxPlotFieldWellsTypeDef",
    {
        "BoxPlotAggregatedFieldWells": NotRequired[BoxPlotAggregatedFieldWellsTypeDef],
    },
)

ComboChartFieldWellsTypeDef = TypedDict(
    "ComboChartFieldWellsTypeDef",
    {
        "ComboChartAggregatedFieldWells": NotRequired[ComboChartAggregatedFieldWellsTypeDef],
    },
)

FilledMapFieldWellsTypeDef = TypedDict(
    "FilledMapFieldWellsTypeDef",
    {
        "FilledMapAggregatedFieldWells": NotRequired[FilledMapAggregatedFieldWellsTypeDef],
    },
)

FunnelChartFieldWellsTypeDef = TypedDict(
    "FunnelChartFieldWellsTypeDef",
    {
        "FunnelChartAggregatedFieldWells": NotRequired[FunnelChartAggregatedFieldWellsTypeDef],
    },
)

GaugeChartConfigurationTypeDef = TypedDict(
    "GaugeChartConfigurationTypeDef",
    {
        "FieldWells": NotRequired[GaugeChartFieldWellsTypeDef],
        "GaugeChartOptions": NotRequired[GaugeChartOptionsTypeDef],
        "DataLabels": NotRequired[DataLabelOptionsTypeDef],
        "TooltipOptions": NotRequired[TooltipOptionsTypeDef],
        "VisualPalette": NotRequired[VisualPaletteTypeDef],
    },
)

GeospatialMapFieldWellsTypeDef = TypedDict(
    "GeospatialMapFieldWellsTypeDef",
    {
        "GeospatialMapAggregatedFieldWells": NotRequired[GeospatialMapAggregatedFieldWellsTypeDef],
    },
)

HeatMapFieldWellsTypeDef = TypedDict(
    "HeatMapFieldWellsTypeDef",
    {
        "HeatMapAggregatedFieldWells": NotRequired[HeatMapAggregatedFieldWellsTypeDef],
    },
)

HistogramFieldWellsTypeDef = TypedDict(
    "HistogramFieldWellsTypeDef",
    {
        "HistogramAggregatedFieldWells": NotRequired[HistogramAggregatedFieldWellsTypeDef],
    },
)

KPIConfigurationTypeDef = TypedDict(
    "KPIConfigurationTypeDef",
    {
        "FieldWells": NotRequired[KPIFieldWellsTypeDef],
        "SortConfiguration": NotRequired[KPISortConfigurationTypeDef],
        "KPIOptions": NotRequired[KPIOptionsTypeDef],
    },
)

LineChartFieldWellsTypeDef = TypedDict(
    "LineChartFieldWellsTypeDef",
    {
        "LineChartAggregatedFieldWells": NotRequired[LineChartAggregatedFieldWellsTypeDef],
    },
)

PieChartFieldWellsTypeDef = TypedDict(
    "PieChartFieldWellsTypeDef",
    {
        "PieChartAggregatedFieldWells": NotRequired[PieChartAggregatedFieldWellsTypeDef],
    },
)

PivotTableFieldWellsTypeDef = TypedDict(
    "PivotTableFieldWellsTypeDef",
    {
        "PivotTableAggregatedFieldWells": NotRequired[PivotTableAggregatedFieldWellsTypeDef],
    },
)

RadarChartFieldWellsTypeDef = TypedDict(
    "RadarChartFieldWellsTypeDef",
    {
        "RadarChartAggregatedFieldWells": NotRequired[RadarChartAggregatedFieldWellsTypeDef],
    },
)

SankeyDiagramFieldWellsTypeDef = TypedDict(
    "SankeyDiagramFieldWellsTypeDef",
    {
        "SankeyDiagramAggregatedFieldWells": NotRequired[SankeyDiagramAggregatedFieldWellsTypeDef],
    },
)

ScatterPlotFieldWellsTypeDef = TypedDict(
    "ScatterPlotFieldWellsTypeDef",
    {
        "ScatterPlotCategoricallyAggregatedFieldWells": NotRequired[
            ScatterPlotCategoricallyAggregatedFieldWellsTypeDef
        ],
        "ScatterPlotUnaggregatedFieldWells": NotRequired[ScatterPlotUnaggregatedFieldWellsTypeDef],
    },
)

ComputationTypeDef = TypedDict(
    "ComputationTypeDef",
    {
        "TopBottomRanked": NotRequired[TopBottomRankedComputationTypeDef],
        "TopBottomMovers": NotRequired[TopBottomMoversComputationTypeDef],
        "TotalAggregation": NotRequired[TotalAggregationComputationTypeDef],
        "MaximumMinimum": NotRequired[MaximumMinimumComputationTypeDef],
        "MetricComparison": NotRequired[MetricComparisonComputationTypeDef],
        "PeriodOverPeriod": NotRequired[PeriodOverPeriodComputationTypeDef],
        "PeriodToDate": NotRequired[PeriodToDateComputationTypeDef],
        "GrowthRate": NotRequired[GrowthRateComputationTypeDef],
        "UniqueValues": NotRequired[UniqueValuesComputationTypeDef],
        "Forecast": NotRequired[ForecastComputationTypeDef],
    },
)

TreeMapFieldWellsTypeDef = TypedDict(
    "TreeMapFieldWellsTypeDef",
    {
        "TreeMapAggregatedFieldWells": NotRequired[TreeMapAggregatedFieldWellsTypeDef],
    },
)

WaterfallChartFieldWellsTypeDef = TypedDict(
    "WaterfallChartFieldWellsTypeDef",
    {
        "WaterfallChartAggregatedFieldWells": NotRequired[
            WaterfallChartAggregatedFieldWellsTypeDef
        ],
    },
)

WordCloudFieldWellsTypeDef = TypedDict(
    "WordCloudFieldWellsTypeDef",
    {
        "WordCloudAggregatedFieldWells": NotRequired[WordCloudAggregatedFieldWellsTypeDef],
    },
)

TableFieldWellsTypeDef = TypedDict(
    "TableFieldWellsTypeDef",
    {
        "TableAggregatedFieldWells": NotRequired[TableAggregatedFieldWellsTypeDef],
        "TableUnaggregatedFieldWells": NotRequired[TableUnaggregatedFieldWellsTypeDef],
    },
)

LayoutConfigurationTypeDef = TypedDict(
    "LayoutConfigurationTypeDef",
    {
        "GridLayout": NotRequired[GridLayoutConfigurationTypeDef],
        "FreeFormLayout": NotRequired[FreeFormLayoutConfigurationTypeDef],
        "SectionBasedLayout": NotRequired[SectionBasedLayoutConfigurationTypeDef],
    },
)

BarChartConfigurationTypeDef = TypedDict(
    "BarChartConfigurationTypeDef",
    {
        "FieldWells": NotRequired[BarChartFieldWellsTypeDef],
        "SortConfiguration": NotRequired[BarChartSortConfigurationTypeDef],
        "Orientation": NotRequired[BarChartOrientationType],
        "BarsArrangement": NotRequired[BarsArrangementType],
        "VisualPalette": NotRequired[VisualPaletteTypeDef],
        "SmallMultiplesOptions": NotRequired[SmallMultiplesOptionsTypeDef],
        "CategoryAxis": NotRequired[AxisDisplayOptionsTypeDef],
        "CategoryLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "ValueAxis": NotRequired[AxisDisplayOptionsTypeDef],
        "ValueLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "ColorLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "Legend": NotRequired[LegendOptionsTypeDef],
        "DataLabels": NotRequired[DataLabelOptionsTypeDef],
        "Tooltip": NotRequired[TooltipOptionsTypeDef],
        "ReferenceLines": NotRequired[Sequence[ReferenceLineTypeDef]],
        "ContributionAnalysisDefaults": NotRequired[Sequence[ContributionAnalysisDefaultTypeDef]],
    },
)

BoxPlotChartConfigurationTypeDef = TypedDict(
    "BoxPlotChartConfigurationTypeDef",
    {
        "FieldWells": NotRequired[BoxPlotFieldWellsTypeDef],
        "SortConfiguration": NotRequired[BoxPlotSortConfigurationTypeDef],
        "BoxPlotOptions": NotRequired[BoxPlotOptionsTypeDef],
        "CategoryAxis": NotRequired[AxisDisplayOptionsTypeDef],
        "CategoryLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "PrimaryYAxisDisplayOptions": NotRequired[AxisDisplayOptionsTypeDef],
        "PrimaryYAxisLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "Legend": NotRequired[LegendOptionsTypeDef],
        "Tooltip": NotRequired[TooltipOptionsTypeDef],
        "ReferenceLines": NotRequired[Sequence[ReferenceLineTypeDef]],
        "VisualPalette": NotRequired[VisualPaletteTypeDef],
    },
)

ComboChartConfigurationTypeDef = TypedDict(
    "ComboChartConfigurationTypeDef",
    {
        "FieldWells": NotRequired[ComboChartFieldWellsTypeDef],
        "SortConfiguration": NotRequired[ComboChartSortConfigurationTypeDef],
        "BarsArrangement": NotRequired[BarsArrangementType],
        "CategoryAxis": NotRequired[AxisDisplayOptionsTypeDef],
        "CategoryLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "PrimaryYAxisDisplayOptions": NotRequired[AxisDisplayOptionsTypeDef],
        "PrimaryYAxisLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "SecondaryYAxisDisplayOptions": NotRequired[AxisDisplayOptionsTypeDef],
        "SecondaryYAxisLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "ColorLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "Legend": NotRequired[LegendOptionsTypeDef],
        "BarDataLabels": NotRequired[DataLabelOptionsTypeDef],
        "LineDataLabels": NotRequired[DataLabelOptionsTypeDef],
        "Tooltip": NotRequired[TooltipOptionsTypeDef],
        "ReferenceLines": NotRequired[Sequence[ReferenceLineTypeDef]],
        "VisualPalette": NotRequired[VisualPaletteTypeDef],
    },
)

FilledMapConfigurationTypeDef = TypedDict(
    "FilledMapConfigurationTypeDef",
    {
        "FieldWells": NotRequired[FilledMapFieldWellsTypeDef],
        "SortConfiguration": NotRequired[FilledMapSortConfigurationTypeDef],
        "Legend": NotRequired[LegendOptionsTypeDef],
        "Tooltip": NotRequired[TooltipOptionsTypeDef],
        "WindowOptions": NotRequired[GeospatialWindowOptionsTypeDef],
        "MapStyleOptions": NotRequired[GeospatialMapStyleOptionsTypeDef],
    },
)

FunnelChartConfigurationTypeDef = TypedDict(
    "FunnelChartConfigurationTypeDef",
    {
        "FieldWells": NotRequired[FunnelChartFieldWellsTypeDef],
        "SortConfiguration": NotRequired[FunnelChartSortConfigurationTypeDef],
        "CategoryLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "ValueLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "Tooltip": NotRequired[TooltipOptionsTypeDef],
        "DataLabelOptions": NotRequired[FunnelChartDataLabelOptionsTypeDef],
        "VisualPalette": NotRequired[VisualPaletteTypeDef],
    },
)

GaugeChartVisualTypeDef = TypedDict(
    "GaugeChartVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[GaugeChartConfigurationTypeDef],
        "ConditionalFormatting": NotRequired[GaugeChartConditionalFormattingTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
    },
)

GeospatialMapConfigurationTypeDef = TypedDict(
    "GeospatialMapConfigurationTypeDef",
    {
        "FieldWells": NotRequired[GeospatialMapFieldWellsTypeDef],
        "Legend": NotRequired[LegendOptionsTypeDef],
        "Tooltip": NotRequired[TooltipOptionsTypeDef],
        "WindowOptions": NotRequired[GeospatialWindowOptionsTypeDef],
        "MapStyleOptions": NotRequired[GeospatialMapStyleOptionsTypeDef],
        "PointStyleOptions": NotRequired[GeospatialPointStyleOptionsTypeDef],
        "VisualPalette": NotRequired[VisualPaletteTypeDef],
    },
)

HeatMapConfigurationTypeDef = TypedDict(
    "HeatMapConfigurationTypeDef",
    {
        "FieldWells": NotRequired[HeatMapFieldWellsTypeDef],
        "SortConfiguration": NotRequired[HeatMapSortConfigurationTypeDef],
        "RowLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "ColumnLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "ColorScale": NotRequired[ColorScaleTypeDef],
        "Legend": NotRequired[LegendOptionsTypeDef],
        "DataLabels": NotRequired[DataLabelOptionsTypeDef],
        "Tooltip": NotRequired[TooltipOptionsTypeDef],
    },
)

HistogramConfigurationTypeDef = TypedDict(
    "HistogramConfigurationTypeDef",
    {
        "FieldWells": NotRequired[HistogramFieldWellsTypeDef],
        "XAxisDisplayOptions": NotRequired[AxisDisplayOptionsTypeDef],
        "XAxisLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "YAxisDisplayOptions": NotRequired[AxisDisplayOptionsTypeDef],
        "BinOptions": NotRequired[HistogramBinOptionsTypeDef],
        "DataLabels": NotRequired[DataLabelOptionsTypeDef],
        "Tooltip": NotRequired[TooltipOptionsTypeDef],
        "VisualPalette": NotRequired[VisualPaletteTypeDef],
    },
)

KPIVisualTypeDef = TypedDict(
    "KPIVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[KPIConfigurationTypeDef],
        "ConditionalFormatting": NotRequired[KPIConditionalFormattingTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
        "ColumnHierarchies": NotRequired[Sequence[ColumnHierarchyTypeDef]],
    },
)

LineChartConfigurationTypeDef = TypedDict(
    "LineChartConfigurationTypeDef",
    {
        "FieldWells": NotRequired[LineChartFieldWellsTypeDef],
        "SortConfiguration": NotRequired[LineChartSortConfigurationTypeDef],
        "ForecastConfigurations": NotRequired[Sequence[ForecastConfigurationTypeDef]],
        "Type": NotRequired[LineChartTypeType],
        "SmallMultiplesOptions": NotRequired[SmallMultiplesOptionsTypeDef],
        "XAxisDisplayOptions": NotRequired[AxisDisplayOptionsTypeDef],
        "XAxisLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "PrimaryYAxisDisplayOptions": NotRequired[LineSeriesAxisDisplayOptionsTypeDef],
        "PrimaryYAxisLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "SecondaryYAxisDisplayOptions": NotRequired[LineSeriesAxisDisplayOptionsTypeDef],
        "SecondaryYAxisLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "DefaultSeriesSettings": NotRequired[LineChartDefaultSeriesSettingsTypeDef],
        "Series": NotRequired[Sequence[SeriesItemTypeDef]],
        "Legend": NotRequired[LegendOptionsTypeDef],
        "DataLabels": NotRequired[DataLabelOptionsTypeDef],
        "ReferenceLines": NotRequired[Sequence[ReferenceLineTypeDef]],
        "Tooltip": NotRequired[TooltipOptionsTypeDef],
        "ContributionAnalysisDefaults": NotRequired[Sequence[ContributionAnalysisDefaultTypeDef]],
        "VisualPalette": NotRequired[VisualPaletteTypeDef],
    },
)

PieChartConfigurationTypeDef = TypedDict(
    "PieChartConfigurationTypeDef",
    {
        "FieldWells": NotRequired[PieChartFieldWellsTypeDef],
        "SortConfiguration": NotRequired[PieChartSortConfigurationTypeDef],
        "DonutOptions": NotRequired[DonutOptionsTypeDef],
        "SmallMultiplesOptions": NotRequired[SmallMultiplesOptionsTypeDef],
        "CategoryLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "ValueLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "Legend": NotRequired[LegendOptionsTypeDef],
        "DataLabels": NotRequired[DataLabelOptionsTypeDef],
        "Tooltip": NotRequired[TooltipOptionsTypeDef],
        "VisualPalette": NotRequired[VisualPaletteTypeDef],
        "ContributionAnalysisDefaults": NotRequired[Sequence[ContributionAnalysisDefaultTypeDef]],
    },
)

PivotTableConfigurationTypeDef = TypedDict(
    "PivotTableConfigurationTypeDef",
    {
        "FieldWells": NotRequired[PivotTableFieldWellsTypeDef],
        "SortConfiguration": NotRequired[PivotTableSortConfigurationTypeDef],
        "TableOptions": NotRequired[PivotTableOptionsTypeDef],
        "TotalOptions": NotRequired[PivotTableTotalOptionsTypeDef],
        "FieldOptions": NotRequired[PivotTableFieldOptionsTypeDef],
        "PaginatedReportOptions": NotRequired[PivotTablePaginatedReportOptionsTypeDef],
    },
)

RadarChartConfigurationTypeDef = TypedDict(
    "RadarChartConfigurationTypeDef",
    {
        "FieldWells": NotRequired[RadarChartFieldWellsTypeDef],
        "SortConfiguration": NotRequired[RadarChartSortConfigurationTypeDef],
        "Shape": NotRequired[RadarChartShapeType],
        "BaseSeriesSettings": NotRequired[RadarChartSeriesSettingsTypeDef],
        "StartAngle": NotRequired[float],
        "VisualPalette": NotRequired[VisualPaletteTypeDef],
        "AlternateBandColorsVisibility": NotRequired[VisibilityType],
        "AlternateBandEvenColor": NotRequired[str],
        "AlternateBandOddColor": NotRequired[str],
        "CategoryAxis": NotRequired[AxisDisplayOptionsTypeDef],
        "CategoryLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "ColorAxis": NotRequired[AxisDisplayOptionsTypeDef],
        "ColorLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "Legend": NotRequired[LegendOptionsTypeDef],
        "AxesRangeScale": NotRequired[RadarChartAxesRangeScaleType],
    },
)

SankeyDiagramChartConfigurationTypeDef = TypedDict(
    "SankeyDiagramChartConfigurationTypeDef",
    {
        "FieldWells": NotRequired[SankeyDiagramFieldWellsTypeDef],
        "SortConfiguration": NotRequired[SankeyDiagramSortConfigurationTypeDef],
        "DataLabels": NotRequired[DataLabelOptionsTypeDef],
    },
)

ScatterPlotConfigurationTypeDef = TypedDict(
    "ScatterPlotConfigurationTypeDef",
    {
        "FieldWells": NotRequired[ScatterPlotFieldWellsTypeDef],
        "XAxisLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "XAxisDisplayOptions": NotRequired[AxisDisplayOptionsTypeDef],
        "YAxisLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "YAxisDisplayOptions": NotRequired[AxisDisplayOptionsTypeDef],
        "Legend": NotRequired[LegendOptionsTypeDef],
        "DataLabels": NotRequired[DataLabelOptionsTypeDef],
        "Tooltip": NotRequired[TooltipOptionsTypeDef],
        "VisualPalette": NotRequired[VisualPaletteTypeDef],
    },
)

InsightConfigurationTypeDef = TypedDict(
    "InsightConfigurationTypeDef",
    {
        "Computations": NotRequired[Sequence[ComputationTypeDef]],
        "CustomNarrative": NotRequired[CustomNarrativeOptionsTypeDef],
    },
)

TreeMapConfigurationTypeDef = TypedDict(
    "TreeMapConfigurationTypeDef",
    {
        "FieldWells": NotRequired[TreeMapFieldWellsTypeDef],
        "SortConfiguration": NotRequired[TreeMapSortConfigurationTypeDef],
        "GroupLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "SizeLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "ColorLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "ColorScale": NotRequired[ColorScaleTypeDef],
        "Legend": NotRequired[LegendOptionsTypeDef],
        "DataLabels": NotRequired[DataLabelOptionsTypeDef],
        "Tooltip": NotRequired[TooltipOptionsTypeDef],
    },
)

WaterfallChartConfigurationTypeDef = TypedDict(
    "WaterfallChartConfigurationTypeDef",
    {
        "FieldWells": NotRequired[WaterfallChartFieldWellsTypeDef],
        "SortConfiguration": NotRequired[WaterfallChartSortConfigurationTypeDef],
        "WaterfallChartOptions": NotRequired[WaterfallChartOptionsTypeDef],
        "CategoryAxisLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "CategoryAxisDisplayOptions": NotRequired[AxisDisplayOptionsTypeDef],
        "PrimaryYAxisLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "PrimaryYAxisDisplayOptions": NotRequired[AxisDisplayOptionsTypeDef],
        "Legend": NotRequired[LegendOptionsTypeDef],
        "DataLabels": NotRequired[DataLabelOptionsTypeDef],
        "VisualPalette": NotRequired[VisualPaletteTypeDef],
    },
)

WordCloudChartConfigurationTypeDef = TypedDict(
    "WordCloudChartConfigurationTypeDef",
    {
        "FieldWells": NotRequired[WordCloudFieldWellsTypeDef],
        "SortConfiguration": NotRequired[WordCloudSortConfigurationTypeDef],
        "CategoryLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "WordCloudOptions": NotRequired[WordCloudOptionsTypeDef],
    },
)

TableConfigurationTypeDef = TypedDict(
    "TableConfigurationTypeDef",
    {
        "FieldWells": NotRequired[TableFieldWellsTypeDef],
        "SortConfiguration": NotRequired[TableSortConfigurationTypeDef],
        "TableOptions": NotRequired[TableOptionsTypeDef],
        "TotalOptions": NotRequired[TotalOptionsTypeDef],
        "FieldOptions": NotRequired[TableFieldOptionsTypeDef],
        "PaginatedReportOptions": NotRequired[TablePaginatedReportOptionsTypeDef],
        "TableInlineVisualizations": NotRequired[Sequence[TableInlineVisualizationTypeDef]],
    },
)

LayoutTypeDef = TypedDict(
    "LayoutTypeDef",
    {
        "Configuration": LayoutConfigurationTypeDef,
    },
)

BarChartVisualTypeDef = TypedDict(
    "BarChartVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[BarChartConfigurationTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
        "ColumnHierarchies": NotRequired[Sequence[ColumnHierarchyTypeDef]],
    },
)

BoxPlotVisualTypeDef = TypedDict(
    "BoxPlotVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[BoxPlotChartConfigurationTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
        "ColumnHierarchies": NotRequired[Sequence[ColumnHierarchyTypeDef]],
    },
)

ComboChartVisualTypeDef = TypedDict(
    "ComboChartVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[ComboChartConfigurationTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
        "ColumnHierarchies": NotRequired[Sequence[ColumnHierarchyTypeDef]],
    },
)

FilledMapVisualTypeDef = TypedDict(
    "FilledMapVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[FilledMapConfigurationTypeDef],
        "ConditionalFormatting": NotRequired[FilledMapConditionalFormattingTypeDef],
        "ColumnHierarchies": NotRequired[Sequence[ColumnHierarchyTypeDef]],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
    },
)

FunnelChartVisualTypeDef = TypedDict(
    "FunnelChartVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[FunnelChartConfigurationTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
        "ColumnHierarchies": NotRequired[Sequence[ColumnHierarchyTypeDef]],
    },
)

GeospatialMapVisualTypeDef = TypedDict(
    "GeospatialMapVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[GeospatialMapConfigurationTypeDef],
        "ColumnHierarchies": NotRequired[Sequence[ColumnHierarchyTypeDef]],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
    },
)

HeatMapVisualTypeDef = TypedDict(
    "HeatMapVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[HeatMapConfigurationTypeDef],
        "ColumnHierarchies": NotRequired[Sequence[ColumnHierarchyTypeDef]],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
    },
)

HistogramVisualTypeDef = TypedDict(
    "HistogramVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[HistogramConfigurationTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
    },
)

LineChartVisualTypeDef = TypedDict(
    "LineChartVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[LineChartConfigurationTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
        "ColumnHierarchies": NotRequired[Sequence[ColumnHierarchyTypeDef]],
    },
)

PieChartVisualTypeDef = TypedDict(
    "PieChartVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[PieChartConfigurationTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
        "ColumnHierarchies": NotRequired[Sequence[ColumnHierarchyTypeDef]],
    },
)

PivotTableVisualTypeDef = TypedDict(
    "PivotTableVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[PivotTableConfigurationTypeDef],
        "ConditionalFormatting": NotRequired[PivotTableConditionalFormattingTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
    },
)

RadarChartVisualTypeDef = TypedDict(
    "RadarChartVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[RadarChartConfigurationTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
        "ColumnHierarchies": NotRequired[Sequence[ColumnHierarchyTypeDef]],
    },
)

SankeyDiagramVisualTypeDef = TypedDict(
    "SankeyDiagramVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[SankeyDiagramChartConfigurationTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
    },
)

ScatterPlotVisualTypeDef = TypedDict(
    "ScatterPlotVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[ScatterPlotConfigurationTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
        "ColumnHierarchies": NotRequired[Sequence[ColumnHierarchyTypeDef]],
    },
)

InsightVisualTypeDef = TypedDict(
    "InsightVisualTypeDef",
    {
        "VisualId": str,
        "DataSetIdentifier": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "InsightConfiguration": NotRequired[InsightConfigurationTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
    },
)

TreeMapVisualTypeDef = TypedDict(
    "TreeMapVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[TreeMapConfigurationTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
        "ColumnHierarchies": NotRequired[Sequence[ColumnHierarchyTypeDef]],
    },
)

WaterfallVisualTypeDef = TypedDict(
    "WaterfallVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[WaterfallChartConfigurationTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
        "ColumnHierarchies": NotRequired[Sequence[ColumnHierarchyTypeDef]],
    },
)

WordCloudVisualTypeDef = TypedDict(
    "WordCloudVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[WordCloudChartConfigurationTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
        "ColumnHierarchies": NotRequired[Sequence[ColumnHierarchyTypeDef]],
    },
)

TableVisualTypeDef = TypedDict(
    "TableVisualTypeDef",
    {
        "VisualId": str,
        "Title": NotRequired[VisualTitleLabelOptionsTypeDef],
        "Subtitle": NotRequired[VisualSubtitleLabelOptionsTypeDef],
        "ChartConfiguration": NotRequired[TableConfigurationTypeDef],
        "ConditionalFormatting": NotRequired[TableConditionalFormattingTypeDef],
        "Actions": NotRequired[Sequence[VisualCustomActionTypeDef]],
    },
)

VisualTypeDef = TypedDict(
    "VisualTypeDef",
    {
        "TableVisual": NotRequired[TableVisualTypeDef],
        "PivotTableVisual": NotRequired[PivotTableVisualTypeDef],
        "BarChartVisual": NotRequired[BarChartVisualTypeDef],
        "KPIVisual": NotRequired[KPIVisualTypeDef],
        "PieChartVisual": NotRequired[PieChartVisualTypeDef],
        "GaugeChartVisual": NotRequired[GaugeChartVisualTypeDef],
        "LineChartVisual": NotRequired[LineChartVisualTypeDef],
        "HeatMapVisual": NotRequired[HeatMapVisualTypeDef],
        "TreeMapVisual": NotRequired[TreeMapVisualTypeDef],
        "GeospatialMapVisual": NotRequired[GeospatialMapVisualTypeDef],
        "FilledMapVisual": NotRequired[FilledMapVisualTypeDef],
        "FunnelChartVisual": NotRequired[FunnelChartVisualTypeDef],
        "ScatterPlotVisual": NotRequired[ScatterPlotVisualTypeDef],
        "ComboChartVisual": NotRequired[ComboChartVisualTypeDef],
        "BoxPlotVisual": NotRequired[BoxPlotVisualTypeDef],
        "WaterfallVisual": NotRequired[WaterfallVisualTypeDef],
        "HistogramVisual": NotRequired[HistogramVisualTypeDef],
        "WordCloudVisual": NotRequired[WordCloudVisualTypeDef],
        "InsightVisual": NotRequired[InsightVisualTypeDef],
        "SankeyDiagramVisual": NotRequired[SankeyDiagramVisualTypeDef],
        "CustomContentVisual": NotRequired[CustomContentVisualTypeDef],
        "EmptyVisual": NotRequired[EmptyVisualTypeDef],
        "RadarChartVisual": NotRequired[RadarChartVisualTypeDef],
    },
)

SheetDefinitionTypeDef = TypedDict(
    "SheetDefinitionTypeDef",
    {
        "SheetId": str,
        "Title": NotRequired[str],
        "Description": NotRequired[str],
        "Name": NotRequired[str],
        "ParameterControls": NotRequired[Sequence[ParameterControlTypeDef]],
        "FilterControls": NotRequired[Sequence[FilterControlTypeDef]],
        "Visuals": NotRequired[Sequence[VisualTypeDef]],
        "TextBoxes": NotRequired[Sequence[SheetTextBoxTypeDef]],
        "Layouts": NotRequired[Sequence[LayoutTypeDef]],
        "SheetControlLayouts": NotRequired[Sequence[SheetControlLayoutTypeDef]],
        "ContentType": NotRequired[SheetContentTypeType],
    },
)

AnalysisDefinitionTypeDef = TypedDict(
    "AnalysisDefinitionTypeDef",
    {
        "DataSetIdentifierDeclarations": Sequence[DataSetIdentifierDeclarationTypeDef],
        "Sheets": NotRequired[Sequence[SheetDefinitionTypeDef]],
        "CalculatedFields": NotRequired[Sequence[CalculatedFieldTypeDef]],
        "ParameterDeclarations": NotRequired[Sequence[ParameterDeclarationTypeDef]],
        "FilterGroups": NotRequired[Sequence[FilterGroupTypeDef]],
        "ColumnConfigurations": NotRequired[Sequence[ColumnConfigurationTypeDef]],
        "AnalysisDefaults": NotRequired[AnalysisDefaultsTypeDef],
    },
)

DashboardVersionDefinitionTypeDef = TypedDict(
    "DashboardVersionDefinitionTypeDef",
    {
        "DataSetIdentifierDeclarations": Sequence[DataSetIdentifierDeclarationTypeDef],
        "Sheets": NotRequired[Sequence[SheetDefinitionTypeDef]],
        "CalculatedFields": NotRequired[Sequence[CalculatedFieldTypeDef]],
        "ParameterDeclarations": NotRequired[Sequence[ParameterDeclarationTypeDef]],
        "FilterGroups": NotRequired[Sequence[FilterGroupTypeDef]],
        "ColumnConfigurations": NotRequired[Sequence[ColumnConfigurationTypeDef]],
        "AnalysisDefaults": NotRequired[AnalysisDefaultsTypeDef],
    },
)

TemplateVersionDefinitionTypeDef = TypedDict(
    "TemplateVersionDefinitionTypeDef",
    {
        "DataSetConfigurations": Sequence[DataSetConfigurationTypeDef],
        "Sheets": NotRequired[Sequence[SheetDefinitionTypeDef]],
        "CalculatedFields": NotRequired[Sequence[CalculatedFieldTypeDef]],
        "ParameterDeclarations": NotRequired[Sequence[ParameterDeclarationTypeDef]],
        "FilterGroups": NotRequired[Sequence[FilterGroupTypeDef]],
        "ColumnConfigurations": NotRequired[Sequence[ColumnConfigurationTypeDef]],
        "AnalysisDefaults": NotRequired[AnalysisDefaultsTypeDef],
    },
)

CreateAnalysisRequestRequestTypeDef = TypedDict(
    "CreateAnalysisRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
        "Name": str,
        "Parameters": NotRequired[ParametersTypeDef],
        "Permissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
        "SourceEntity": NotRequired[AnalysisSourceEntityTypeDef],
        "ThemeArn": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "Definition": NotRequired[AnalysisDefinitionTypeDef],
        "ValidationStrategy": NotRequired[ValidationStrategyTypeDef],
    },
)

DescribeAnalysisDefinitionResponseTypeDef = TypedDict(
    "DescribeAnalysisDefinitionResponseTypeDef",
    {
        "AnalysisId": str,
        "Name": str,
        "Errors": List[AnalysisErrorTypeDef],
        "ResourceStatus": ResourceStatusType,
        "ThemeArn": str,
        "Definition": AnalysisDefinitionTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAnalysisRequestRequestTypeDef = TypedDict(
    "UpdateAnalysisRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
        "Name": str,
        "Parameters": NotRequired[ParametersTypeDef],
        "SourceEntity": NotRequired[AnalysisSourceEntityTypeDef],
        "ThemeArn": NotRequired[str],
        "Definition": NotRequired[AnalysisDefinitionTypeDef],
        "ValidationStrategy": NotRequired[ValidationStrategyTypeDef],
    },
)

CreateDashboardRequestRequestTypeDef = TypedDict(
    "CreateDashboardRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "Name": str,
        "Parameters": NotRequired[ParametersTypeDef],
        "Permissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
        "SourceEntity": NotRequired[DashboardSourceEntityTypeDef],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "VersionDescription": NotRequired[str],
        "DashboardPublishOptions": NotRequired[DashboardPublishOptionsTypeDef],
        "ThemeArn": NotRequired[str],
        "Definition": NotRequired[DashboardVersionDefinitionTypeDef],
        "ValidationStrategy": NotRequired[ValidationStrategyTypeDef],
    },
)

DescribeDashboardDefinitionResponseTypeDef = TypedDict(
    "DescribeDashboardDefinitionResponseTypeDef",
    {
        "DashboardId": str,
        "Errors": List[DashboardErrorTypeDef],
        "Name": str,
        "ResourceStatus": ResourceStatusType,
        "ThemeArn": str,
        "Definition": DashboardVersionDefinitionTypeDef,
        "Status": int,
        "RequestId": str,
        "DashboardPublishOptions": DashboardPublishOptionsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDashboardRequestRequestTypeDef = TypedDict(
    "UpdateDashboardRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "Name": str,
        "SourceEntity": NotRequired[DashboardSourceEntityTypeDef],
        "Parameters": NotRequired[ParametersTypeDef],
        "VersionDescription": NotRequired[str],
        "DashboardPublishOptions": NotRequired[DashboardPublishOptionsTypeDef],
        "ThemeArn": NotRequired[str],
        "Definition": NotRequired[DashboardVersionDefinitionTypeDef],
        "ValidationStrategy": NotRequired[ValidationStrategyTypeDef],
    },
)

CreateTemplateRequestRequestTypeDef = TypedDict(
    "CreateTemplateRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "Name": NotRequired[str],
        "Permissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
        "SourceEntity": NotRequired[TemplateSourceEntityTypeDef],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "VersionDescription": NotRequired[str],
        "Definition": NotRequired[TemplateVersionDefinitionTypeDef],
        "ValidationStrategy": NotRequired[ValidationStrategyTypeDef],
    },
)

DescribeTemplateDefinitionResponseTypeDef = TypedDict(
    "DescribeTemplateDefinitionResponseTypeDef",
    {
        "Name": str,
        "TemplateId": str,
        "Errors": List[TemplateErrorTypeDef],
        "ResourceStatus": ResourceStatusType,
        "ThemeArn": str,
        "Definition": TemplateVersionDefinitionTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTemplateRequestRequestTypeDef = TypedDict(
    "UpdateTemplateRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "SourceEntity": NotRequired[TemplateSourceEntityTypeDef],
        "VersionDescription": NotRequired[str],
        "Name": NotRequired[str],
        "Definition": NotRequired[TemplateVersionDefinitionTypeDef],
        "ValidationStrategy": NotRequired[ValidationStrategyTypeDef],
    },
)
