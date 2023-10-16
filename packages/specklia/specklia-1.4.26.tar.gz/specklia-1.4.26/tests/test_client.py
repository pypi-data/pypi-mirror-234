"""Unit tests for the Specklia Client."""
from datetime import datetime
from http import HTTPStatus
from typing import Dict
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch

import geopandas as gpd
import pandas as pd
import pytest
from shapely import MultiPolygon, Point, Polygon

from specklia import Specklia

_QUERY_DATASET_DICT = {
    'dataset_id': 'sheffield',
    "epsg4326_polygon": Polygon(((0, 0), (0, 1), (1, 1), (0, 0))),
    'min_timestamp': datetime(2000, 1, 1),
    'max_timestamp': datetime(2000, 1, 2),
    'columns_to_return': ['croissant'],
    'additional_filters': [
        {'column': 'cheese', 'operator': '<', 'threshold': 6.57},
        {'column': 'wine', 'operator': '>=', 'threshold': -23}]}


@pytest.fixture()
def example_geodataframe() -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame({
        'geometry': [Point(lon, lat) for lon, lat in zip([1, 2, 3, 4, 5], [0, 1, 2, 3, 4])],
        'timestamp': [2, 3, 4, 5, 6]},
        crs="EPSG:4326")


@pytest.fixture()
def example_datasets_dataframe() -> pd.DataFrame:
    return pd.DataFrame([{'columns': {'description': 'hobbit height in cm',
                                      'max_value': '150',
                                      'min_value': '0',
                                      'name': 'height',
                                      'type': 'int',
                                      'unit': 'centimetres'},
                          'created_timestamp': 'Sat, 1 Jan 2000 15:44:24',
                          'dataset_id': 'sauron',
                          'dataset_name': 'hobbit_height',
                          'description': 'The height of some hobbits',
                          'epsg4326_coverage': 'MULTIPOLYGON(((0 0, 1 1, 1 0, 0 0)), ((0 0, 0 1, 1 0, 0 0)))',
                          'last_modified_timestamp': 'Sun, 2 Jan 2000 15:44:24',
                          'last_queried_timestamp': 'Sun, 2 Jan 2000 12:14:44',
                          'max_timestamp': 'Wed, 1 Dec 1999 12:10:54',
                          'min_timestamp': 'Mon, 1 Nov 1999 00:41:25',
                          'owning_group_id': 'pippin',
                          'owning_group_name': 'merry',
                          'size_rows': 4,
                          'size_uncompressed_bytes': 726
                          }])


@pytest.fixture()
def test_client():
    with patch.object(Specklia, '_fetch_user_id'):
        return Specklia(auth_token='fake_token', url='https://localhost')


def test_create_client(test_client: Specklia):
    assert test_client is not None


def test_user_id(test_client: Specklia, patched_requests_with_response: Dict[str, MagicMock]):
    patched_requests_with_response['response'].json.return_value = 'fake_user_id'
    test_client._fetch_user_id()
    patched_requests_with_response['requests'].post.assert_has_calls([
        call('https://localhost/users', headers={'Authorization': 'Bearer fake_token'})])
    assert test_client.user_id == 'fake_user_id'


def test_list_users(test_client: Specklia, patched_requests_with_response: Dict[str, MagicMock]):
    patched_requests_with_response['response'].json.return_value = [{'name': 'fred', 'email': 'fred@fred.fred'}]
    test_client.list_users(group_id='hazbin')
    patched_requests_with_response['requests'].get.assert_has_calls([
        call('https://localhost/users', headers={'Authorization': 'Bearer fake_token'},
             params={"group_id": "hazbin"})])


def test_add_points_to_dataset(test_client: Specklia, example_geodataframe: gpd.GeoDataFrame):
    with (patch('specklia.client.simple_websocket') as mock_simple_websocket,
            patch('specklia.client._websocket_helpers') as mock_websocket_helpers):
        mock_client = MagicMock(name="mock_client")
        mock_simple_websocket.Client.return_value = mock_client
        mock_websocket_helpers.receive_object_from_websocket.return_value = {'status': HTTPStatus.OK}
        test_client.add_points_to_dataset(
            dataset_id='dummy_dataset', new_points=example_geodataframe, source_description={'reference': 'cheese'})

        mock_websocket_helpers.send_object_to_websocket.assert_called_with(
            mock_client, {
                'dataset_id': 'dummy_dataset', 'gdf': example_geodataframe, 'source': {'reference': 'cheese'}})


def test_query_dataset(test_client: Specklia):
    with (patch('specklia.client.simple_websocket') as mock_simple_websocket,
            patch('specklia.client._websocket_helpers') as mock_websocket_helpers):
        mock_client = MagicMock(name="mock_client")
        mock_simple_websocket.Client.return_value = mock_client
        mock_websocket_helpers.receive_object_from_websocket.return_value = {
            'status': HTTPStatus.OK, 'gdf': 'dummy', 'sources': {}}
        test_client.query_dataset(
            dataset_id='dummy_dataset',
            epsg4326_polygon=Polygon(((0, 0), (0, 1), (1, 1), (0, 0))),
            min_datetime=datetime(2020, 5, 6),
            max_datetime=datetime(2020, 5, 10),
            columns_to_return=['lat', 'lon'],
            additional_filters=[
                {'column': 'cheese', 'operator': '<', 'threshold': 6.57},
                {'column': 'wine', 'operator': '>=', 'threshold': -23}])

        mock_websocket_helpers.send_object_to_websocket.assert_called_with(
            mock_client, {
                'dataset_id': 'dummy_dataset', 'min_timestamp': 1588719600, 'max_timestamp': 1589065200,
                'epsg4326_search_area': {
                    'type': 'Polygon', 'coordinates': [[[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [0.0, 0.0]]]},
                'columns_to_return': ['lat', 'lon'],
                'additional_filters': [
                    {'column': 'cheese', 'operator': '<', 'threshold': 6.57},
                    {'column': 'wine', 'operator': '>=', 'threshold': -23}]})


@pytest.mark.parametrize(
    ('invalid_json', 'expected_exception', 'expected_match'),
    # invalid espg4326_search_area type
    [(dict(_QUERY_DATASET_DICT, epsg4326_polygon='my back garden'),
      TypeError, "provide only Geometry objects"),
     # invalid min_datetime type
     (dict(_QUERY_DATASET_DICT, min_timestamp='a long time ago'),
      AttributeError, "object has no attribute 'timestamp'"),
     # invalid max_datetime type
     (dict(_QUERY_DATASET_DICT, max_timestamp='the year 3000'),
      AttributeError, "object has no attribute 'timestamp'")
     ])
def test_query_dataset_invalid_request(test_client: Specklia, invalid_json: dict,
                                       expected_exception: Exception, expected_match: str):
    with (patch('specklia.client.simple_websocket') as mock_simple_websocket,
            patch('specklia.client._websocket_helpers') as mock_websocket_helpers,
            pytest.raises(expected_exception, match=expected_match)):
        test_client.query_dataset(
            dataset_id=invalid_json['dataset_id'],
            epsg4326_polygon=invalid_json['epsg4326_polygon'],
            min_datetime=invalid_json['min_timestamp'],
            max_datetime=invalid_json['max_timestamp'],
            columns_to_return=invalid_json['columns_to_return'],
            additional_filters=invalid_json['additional_filters'])
    mock_websocket_helpers.assert_not_called()
    mock_simple_websocket.assert_not_called()


def test_list_all_groups(patched_requests_with_response: Dict[str, MagicMock]):
    patched_requests_with_response['response'].json.return_value = ['ducks']
    Specklia(url='https://localhost', auth_token='fake_token').list_all_groups()
    patched_requests_with_response['requests'].get.assert_has_calls([
        call('https://localhost/groups', headers={'Authorization': 'Bearer fake_token'})])


def test_create_group(patched_requests_with_response: Dict[str, MagicMock]):
    Specklia(url='https://localhost', auth_token='fake_token').create_group("ducks")
    patched_requests_with_response['requests'].post.assert_has_calls([
        call('https://localhost/groups',
             json={"group_name": "ducks"},
             headers={'Authorization': 'Bearer fake_token'})])


def test_update_group_name(patched_requests_with_response: Dict[str, MagicMock]):
    Specklia(url='https://localhost', auth_token='fake_token').update_group_name(
        group_id="ducks",
        new_group_name="pigeons")
    patched_requests_with_response['requests'].put.assert_has_calls([
        call('https://localhost/groups',
             json={"group_id": "ducks", "new_group_name": "pigeons"},
             headers={'Authorization': 'Bearer fake_token'})])


def test_delete_group(patched_requests_with_response: Dict[str, MagicMock]):
    Specklia(url='https://localhost', auth_token='fake_token').delete_group(group_id="ducks")
    patched_requests_with_response['requests'].delete.assert_has_calls([
        call('https://localhost/groups', headers={'Authorization': 'Bearer fake_token'},
             json={"group_id": "ducks"})])


def test_list_groups(patched_requests_with_response: Dict[str, MagicMock]):
    patched_requests_with_response['response'].json.return_value = ['ducks']
    Specklia(url='https://localhost', auth_token='fake_token').list_groups()
    patched_requests_with_response['requests'].get.assert_has_calls([
        call('https://localhost/groupmembership', headers={'Authorization': 'Bearer fake_token'})])


def test_add_user_to_group(patched_requests_with_response: Dict[str, MagicMock]):
    Specklia(url='https://localhost', auth_token='fake_token').add_user_to_group(group_id='ducks',
                                                                                 user_to_add_id='donald')
    patched_requests_with_response['requests'].post.assert_has_calls([
        call('https://localhost/groupmembership',
             json={"group_id": "ducks", "user_to_add_id": "donald"},
             headers={'Authorization': 'Bearer fake_token'})])


def test_update_user_privileges(patched_requests_with_response: Dict[str, MagicMock]):
    Specklia(url='https://localhost', auth_token='fake_token').update_user_privileges(group_id="ducks",
                                                                                      user_to_update_id="donald",
                                                                                      new_privileges="ADMIN")
    patched_requests_with_response['requests'].put.assert_has_calls([
        call('https://localhost/groupmembership',
             json={"group_id": "ducks", "user_to_update_id": "donald", "new_privileges": "ADMIN"},
             headers={'Authorization': 'Bearer fake_token'})])


def test_delete_user_from_group(patched_requests_with_response: Dict[str, MagicMock]):
    Specklia(url='https://localhost', auth_token='fake_token').delete_user_from_group(group_id="ducks",
                                                                                      user_to_delete_id="donald")
    patched_requests_with_response['requests'].delete.assert_has_calls([
        call('https://localhost/groupmembership', headers={'Authorization': 'Bearer fake_token'},
             json={"group_id": "ducks", "user_to_delete_id": "donald"})])


def test_list_datasets(patched_requests_with_response: Dict[str, MagicMock], example_datasets_dataframe: pd.DataFrame):
    patched_requests_with_response['response'].json.return_value = example_datasets_dataframe.to_dict(orient='records')
    datasets = Specklia(url='https://localhost', auth_token='fake_token').list_datasets()
    assert type(datasets['epsg4326_coverage'][0]) is MultiPolygon
    for column in datasets.columns:
        if 'timestamp' in column:
            assert type(datasets[column][0]) is pd.Timestamp
    patched_requests_with_response['requests'].get.assert_has_calls([
        call('https://localhost/metadata', headers={'Authorization': 'Bearer fake_token'})])


def test_create_dataset(patched_requests_with_response: Dict[str, MagicMock]):
    Specklia(url='https://localhost', auth_token='fake_token').create_dataset(
        dataset_name='am', description='wibble', columns=[
            {'name': 'hobbits', 'type': 'halflings', 'description': 'concerning hobbits'},
            {'name': 'cats', 'type': 'pets', 'description': 'concerning cats'}])

    patched_requests_with_response['requests'].post.assert_has_calls([
        call('https://localhost/metadata',
             json={'dataset_name': 'am',
                   'description': 'wibble',
                   'columns':
                   [{'name': 'hobbits', 'type': 'halflings', 'description': 'concerning hobbits'},
                    {'name': 'cats', 'type': 'pets', 'description': 'concerning cats'}]},
             headers={'Authorization': 'Bearer fake_token'})])


def test_update_dataset_ownership(patched_requests_with_response: Dict[str, MagicMock]):
    Specklia(url='https://localhost', auth_token='fake_token').update_dataset_ownership(
        dataset_id='bside', new_owning_group_id='arctic monkeys'
    )
    patched_requests_with_response['requests'].put.assert_has_calls([
        call('https://localhost/metadata',
             json={'dataset_id': 'bside',
                   'new_owning_group_id': 'arctic monkeys'},
             headers={'Authorization': 'Bearer fake_token'})
    ])


def test_delete_dataset(patched_requests_with_response: Dict[str, MagicMock]):
    Specklia(url='https://localhost', auth_token='fake_token').delete_dataset(
        dataset_id='bside'
    )
    patched_requests_with_response['requests'].delete.assert_has_calls([
        call('https://localhost/metadata',
             json={'dataset_id': 'bside'},
             headers={'Authorization': 'Bearer fake_token'})
    ])
