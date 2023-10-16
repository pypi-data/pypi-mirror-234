from dataclasses import dataclass
from typing import List, Optional
from unittest import TestCase

from pycarlo.features.metadata import AllowBlockList, MetadataFilter, MetadataFiltersContainer, FilterEffectType, FilterType


@dataclass
class DatasetEntry:
    project: str
    dataset: str


def _redshift_encoder(column: str, value: str, type: FilterType) -> str:
    if type == FilterType.REGEXP:
        op = '~'
        encoded_value = f"'^({value})$'"
    elif type == FilterType.PREFIX:
        op = ' LIKE '
        encoded_value = f"'{value}%'"
    else:
        op = '='
        encoded_value = f"'{value}'"
    return f'{column}{op}{encoded_value}'


class TestDatasetFiltering(TestCase):
    DATASETS = [
        DatasetEntry('project_1', 'dataset_1'),
        DatasetEntry('project_1', 'dataset_2'),
        DatasetEntry('project_1', 'dataset_3'),
        DatasetEntry('project_2', 'dataset_1'),
        DatasetEntry('project_2', 'dataset_2'),
        DatasetEntry('project_2', 'dataset_3'),
        DatasetEntry('project_2', 'dataset_4'),
    ]
    DATASETS_FOR_REGEXP = [
        DatasetEntry('project_1', 'dataset_1'),
        DatasetEntry('project_1', 'dataset_2'),
        DatasetEntry('project_2', 'dataset_1'),
        DatasetEntry('project_2', 'ds_2'),
        DatasetEntry('prj_3', 'ds_1'),
        DatasetEntry('prj_3', 'ds_2'),
        DatasetEntry('prj_3', 'ds_3'),
    ]

    def test_block_single_dataset(self):
        # excludes only project_1.dataset_2
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_1', dataset='dataset_2', effect=FilterEffectType.BLOCK),
        ])
        self._validate_blocked_datasets(filters, [DatasetEntry(project='project_1', dataset='dataset_2')])

    def test_block_multi_datasets(self):
        # excludes project_1.dataset_3 and project_2.dataset_1
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_1', dataset='dataset_3', effect=FilterEffectType.BLOCK),
            MetadataFilter(project='project_2', dataset='dataset_1', effect=FilterEffectType.BLOCK),
        ])
        limits = self._validate_blocked_datasets(filters, [
            DatasetEntry(project='project_1', dataset='dataset_3'),
            DatasetEntry(project='project_2', dataset='dataset_1'),
        ])
        self.assertFalse(limits.is_whole_project_blocked('project_1'))
        self.assertFalse(limits.is_whole_project_blocked('project_2'))

    def test_block_single_project(self):
        # excludes all datasets in project_1
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_1', effect=FilterEffectType.BLOCK),
        ])
        blocked = list(filter(lambda d: d.project == 'project_1', self.DATASETS))
        limits = self._validate_blocked_datasets(filters, blocked)
        self.assertTrue(limits.is_whole_project_blocked('project_1'))
        self.assertFalse(limits.is_whole_project_blocked('project_2'))

    def test_block_second_project(self):
        # excludes all datasets in project_2
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_2', effect=FilterEffectType.BLOCK),
        ])
        blocked = list(filter(lambda d: d.project == 'project_2', self.DATASETS))
        limits = self._validate_blocked_datasets(filters, blocked)
        self.assertFalse(limits.is_whole_project_blocked('project_1'))
        self.assertTrue(limits.is_whole_project_blocked('project_2'))

    def test_block_single_project_regexp(self):
        # excludes all datasets in prj_3
        filters = AllowBlockList(filters=[
            MetadataFilter(project='prj_.*', type=FilterType.REGEXP, effect=FilterEffectType.BLOCK),
        ])
        blocked = list(filter(lambda d: d.project.startswith('prj_'), self.DATASETS_FOR_REGEXP))
        limits = self._validate_blocked_datasets(filters, blocked)
        self.assertFalse(limits.is_whole_project_blocked('project_1'))
        self.assertFalse(limits.is_whole_project_blocked('project_2'))
        self.assertTrue(limits.is_whole_project_blocked('prj_3'))

    def test_block_datasets_regexp(self):
        filters = AllowBlockList(filters=[
            MetadataFilter(project='.*', dataset='ds_.*', type=FilterType.REGEXP, effect=FilterEffectType.BLOCK),
        ])
        self._validate_dataset_prefix(filters)

    def test_block_datasets_prefix(self):
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_2', dataset='ds_', type=FilterType.PREFIX, effect=FilterEffectType.BLOCK),
            MetadataFilter(project='prj_3', dataset='ds_', type=FilterType.PREFIX, effect=FilterEffectType.BLOCK),
        ])
        self._validate_dataset_prefix(filters)

    def _validate_dataset_prefix(self, filters: AllowBlockList):
        blocked = list(filter(lambda d: d.project.startswith('ds_'), self.DATASETS_FOR_REGEXP))
        limits = self._validate_blocked_datasets(filters, blocked)

        self.assertFalse(limits.is_whole_project_blocked('project_1'))
        self.assertFalse(limits.is_whole_project_blocked('project_2'))
        self.assertFalse(limits.is_whole_project_blocked('prj_3'))
        self.assertFalse(limits.is_whole_project_blocked('new_project'))

        self.assertTrue(limits.is_dataset_allowed('project_2', 'dataset_1'))
        self.assertFalse(limits.is_dataset_allowed('project_2', 'ds_2'))
        self.assertFalse(limits.is_dataset_allowed('prj_3', 'ds_1'))
        self.assertFalse(limits.is_dataset_allowed('prj_3', 'ds_2'))

    def test_no_filters(self):
        expected_datasets = self.DATASETS.copy()
        filtered_datasets = self._filter_datasets(self.DATASETS, MetadataFiltersContainer())
        self.assertEqual(expected_datasets, filtered_datasets)

    def test_allow_single_dataset(self):
        # excludes all datasets in project_1
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_2', dataset='dataset_4', effect=FilterEffectType.ALLOW)
        ], default_effect=FilterEffectType.BLOCK)
        limits = self._validate_allowed_datasets(filters,
                                                 [DatasetEntry(project='project_2', dataset='dataset_4')]
                                                 )

        self.assertTrue(limits.is_whole_project_blocked('project_1'))
        self.assertFalse(limits.is_whole_project_blocked('project_2'))

    def test_allow_second_project(self):
        # excludes all datasets in project_1
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_2', effect=FilterEffectType.ALLOW),
        ], default_effect=FilterEffectType.BLOCK)
        allowed = list(filter(lambda d: d.project == 'project_2', self.DATASETS))
        limits = self._validate_allowed_datasets(filters, allowed)

        self.assertTrue(limits.is_whole_project_blocked('project_1'))
        self.assertFalse(limits.is_whole_project_blocked('project_2'))

    def test_sql_query_block_single_project(self):
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_2', effect=FilterEffectType.BLOCK),
        ])
        limits = MetadataFiltersContainer(metadata_filters=filters)
        self.assertTrue(limits.is_metadata_filtered)

        conditions = limits.get_sql_conditions({
            'project': 'database',
            'dataset': 'schema'
        }, _redshift_encoder)
        self.assertEqual("(NOT(LOWER(database)='project_2'))", conditions)

    def test_sql_query_block_project_prefix(self):
        filters = AllowBlockList(filters=[
            MetadataFilter(project='prj_', type=FilterType.PREFIX, effect=FilterEffectType.BLOCK),
        ])
        limits = MetadataFiltersContainer(metadata_filters=filters)
        self.assertTrue(limits.is_metadata_filtered)

        conditions = limits.get_sql_conditions({
            'project': 'database',
            'dataset': 'schema'
        }, _redshift_encoder)
        self.assertEqual("(NOT(LOWER(database) LIKE 'prj_%'))", conditions)

    def test_sql_query_block_project_dataset_prefix(self):
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_name',
                           dataset='ds_',
                           type=FilterType.PREFIX,
                           effect=FilterEffectType.BLOCK
                           ),
        ])
        limits = MetadataFiltersContainer(metadata_filters=filters)
        self.assertTrue(limits.is_metadata_filtered)

        conditions = limits.get_sql_conditions({
            'project': 'database',
            'dataset': 'schema'
        }, _redshift_encoder)
        self.assertEqual("(NOT(LOWER(database) LIKE 'project_name%' AND LOWER(schema) LIKE 'ds_%'))", conditions)

    def test_sql_query_block_single_dataset(self):
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_2', dataset='dataset_1', effect=FilterEffectType.BLOCK),
        ])
        limits = MetadataFiltersContainer(metadata_filters=filters)
        conditions = limits.get_sql_conditions({
            'project': 'database',
            'dataset': 'schema'
        }, _redshift_encoder)
        self.assertEqual("(NOT(LOWER(database)='project_2' AND LOWER(schema)='dataset_1'))", conditions)

    def test_sql_query_block_datasets_regexp(self):
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_2',
                           dataset='dataset_.+',
                           type=FilterType.REGEXP,
                           effect=FilterEffectType.BLOCK
                           ),
        ])
        limits = MetadataFiltersContainer(metadata_filters=filters)
        conditions = limits.get_sql_conditions({
            'project': 'database',
            'dataset': 'schema'
        }, _redshift_encoder)
        self.assertEqual("(NOT(LOWER(database)~'^(project_2)$' AND LOWER(schema)~'^(dataset_.+)$'))", conditions)

    def test_sql_query_block_datasets_regexp_with_exception(self):
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_2',
                           dataset='dataset_.+',
                           type=FilterType.REGEXP,
                           effect=FilterEffectType.BLOCK
                           ),
            MetadataFilter(project='project_2',
                           dataset='dataset_10',
                           effect=FilterEffectType.ALLOW
                           ),
        ])
        limits = MetadataFiltersContainer(metadata_filters=filters)
        conditions = limits.get_sql_conditions({
            'project': 'database',
            'dataset': 'schema'
        }, _redshift_encoder)
        self.assertEqual("(((LOWER(database)='project_2' AND LOWER(schema)='dataset_10')) OR "
                         "(NOT(LOWER(database)~'^(project_2)$' AND LOWER(schema)~'^(dataset_.+)$')))", conditions)

    def test_sql_query_project_block_single_dataset(self):
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_2', dataset='dataset_1', effect=FilterEffectType.BLOCK),
            MetadataFilter(project='project_1', dataset='dataset_2', effect=FilterEffectType.BLOCK),
        ])
        limits = MetadataFiltersContainer(metadata_filters=filters)
        conditions = limits.get_sql_conditions(
            project='project_2',
            column_mapping={
                'project': 'database',
                'dataset': 'schema'
            },
            encoder=_redshift_encoder
        )
        self.assertEqual("(NOT(LOWER(database)='project_2' AND LOWER(schema)='dataset_1'))", conditions)

    def test_sql_query_project_block_nothing(self):
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_1', dataset='dataset_2', effect=FilterEffectType.BLOCK),
        ])
        limits = MetadataFiltersContainer(metadata_filters=filters)
        self.assertFalse(limits.is_project_with_datasets_filtered('project_2'))
        conditions = limits.get_sql_conditions(
            project='project_2',
            column_mapping={
                'project': 'database',
                'dataset': 'schema'
            },
            encoder=_redshift_encoder
        )
        self.assertIsNone(conditions)

    def test_sql_query_block_multi_datasets(self):
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_2', dataset='dataset_1', effect=FilterEffectType.BLOCK),
            MetadataFilter(project='project_1', dataset='dataset_2', effect=FilterEffectType.BLOCK),
        ])
        limits = MetadataFiltersContainer(metadata_filters=filters)
        conditions = limits.get_sql_conditions({
            'project': 'database',
            'dataset': 'schema'
        }, _redshift_encoder)
        self.assertEqual("("
                         "NOT(LOWER(database)='project_2' AND LOWER(schema)='dataset_1') AND "
                         "NOT(LOWER(database)='project_1' AND LOWER(schema)='dataset_2')"
                         ")", conditions)

    def test_sql_query_allow_multi_datasets(self):
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_2', dataset='dataset_1', effect=FilterEffectType.ALLOW),
            MetadataFilter(project='project_1', dataset='dataset_2', effect=FilterEffectType.ALLOW),
        ], default_effect=FilterEffectType.BLOCK)
        limits = MetadataFiltersContainer(metadata_filters=filters)
        conditions = limits.get_sql_conditions({
            'project': 'database',
            'dataset': 'schema'
        }, _redshift_encoder)
        self.assertEqual("("
                         "(LOWER(database)='project_2' AND LOWER(schema)='dataset_1') OR "
                         "(LOWER(database)='project_1' AND LOWER(schema)='dataset_2')"
                         ")", conditions)

    def test_sql_query_block_case_insensitive(self):
        filters = AllowBlockList(filters=[
            MetadataFilter(project='SOME_PROJECT', effect=FilterEffectType.BLOCK, type=FilterType.EXACT_MATCH),
            MetadataFilter(project='PROJECT_', effect=FilterEffectType.BLOCK, type=FilterType.PREFIX),
            MetadataFilter(project='[A-Z]+[1-9]+', effect=FilterEffectType.BLOCK, type=FilterType.REGEXP),
        ])
        limits = MetadataFiltersContainer(metadata_filters=filters)
        self.assertTrue(limits.is_metadata_filtered)

        conditions = limits.get_sql_conditions({
            'project': 'database',
            'dataset': 'schema'
        }, _redshift_encoder)
        self.assertEqual("(NOT(LOWER(database)='some_project') AND "
                         "NOT(LOWER(database) LIKE 'project_%') AND "
                         "NOT(LOWER(database)~'^([a-z]+[1-9]+)$')"
                         ")"
                         , conditions)

    def test_whole_project_blocked(self):
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_2', dataset='dataset_1', effect=FilterEffectType.BLOCK),
        ], default_effect=FilterEffectType.BLOCK)
        limits = MetadataFiltersContainer(metadata_filters=filters)
        self.assertTrue(limits.is_metadata_blocked)
        self.assertTrue(limits.is_whole_project_blocked('project_2'))

        query = limits.get_sql_conditions({
            'project': 'database',
            'dataset': 'schema'
        }, _redshift_encoder)
        self.assertTrue(query)

    def test_case_insensitive_comparison_exact_match(self):
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_2', effect=FilterEffectType.BLOCK, type=FilterType.EXACT_MATCH),
        ])

        limits = MetadataFiltersContainer(metadata_filters=filters)
        self.assertTrue(limits.is_whole_project_blocked('PROJECT_2'))
        self.assertFalse(limits.is_whole_project_blocked('PROJECT_3'))

    def test_case_insensitive_comparison_prefix(self):
        filters = AllowBlockList(filters=[
            MetadataFilter(project='project_', effect=FilterEffectType.BLOCK, type=FilterType.PREFIX),
        ])

        limits = MetadataFiltersContainer(metadata_filters=filters)
        self.assertTrue(limits.is_whole_project_blocked('PROJECT_1'))
        self.assertFalse(limits.is_whole_project_blocked('OTHER_PROJECT'))

    def test_case_insensitive_comparison_regex(self):
        filters = AllowBlockList(filters=[
            MetadataFilter(project='[a-z]+_[1-9]+', effect=FilterEffectType.BLOCK, type=FilterType.REGEXP),
        ])

        limits = MetadataFiltersContainer(metadata_filters=filters)
        self.assertTrue(limits.is_whole_project_blocked('PROJECT_1'))
        self.assertFalse(limits.is_whole_project_blocked('PROJECT_'))

    def _validate_allowed_datasets(self,
                                   filters: AllowBlockList,
                                   expected_datasets: List,
                                   datasets: Optional[List] = None
                          ) -> MetadataFiltersContainer:
        limits = MetadataFiltersContainer(metadata_filters=filters)
        filtered_datasets = self._filter_datasets(datasets or self.DATASETS, limits)
        self.assertEqual(expected_datasets, filtered_datasets)
        return limits

    def _validate_blocked_datasets(self,
                                   filters: AllowBlockList,
                                   blocked_datasets: List,
                                   datasets: Optional[List] = None
                                   ) -> MetadataFiltersContainer:
        expected_datasets = list(filter(lambda d: d not in blocked_datasets, (datasets or self.DATASETS)))
        limits = MetadataFiltersContainer(metadata_filters=filters)
        filtered_datasets = self._filter_datasets(datasets or self.DATASETS, limits)
        self.assertEqual(expected_datasets, filtered_datasets)
        return limits

    @staticmethod
    def _filter_datasets(datasets: List[DatasetEntry], limits: MetadataFiltersContainer) -> List[DatasetEntry]:
        return [d for d in datasets if limits.is_dataset_allowed(d.project, d.dataset)]
