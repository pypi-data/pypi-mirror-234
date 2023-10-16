# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
A module containing the helper functions useful when integrating asset creation, asset updates, data ingestion, etc
into the Switch Automation Platform.
"""
import json
import sys
import pandas
import pandas as pd
import requests
import logging
import uuid
import pyodbc
from typing import Union
from ._utils import _get_sql_connection_string, _extract_sql_credentials
from .._utils._constants import QUERY_LANGUAGE
from .._utils._constants import RESPONSE_TYPE, AMORTISATION_METHOD
from .._utils._utils import ApiInputs, _column_name_cap, requests_retry_session, requests_retry_session2

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setLevel(logging.INFO)

logger.addHandler(consoleHandler)
formatter = logging.Formatter('%(asctime)s  switch_api.%(module)s.%(funcName)s  %(levelname)s: %(message)s',
                              datefmt='%Y-%m-%dT%H:%M:%S')
consoleHandler.setFormatter(formatter)


def get_operation_state(upload_id: uuid.UUID, api_inputs: ApiInputs):
    """Get operation state

    Parameters
    ----------
    upload_id: uuid.UUID
        uploadId returned from the Data Operation
    api_inputs : ApiInputs
        Object returned by initialize() function.

    Returns
    -------
    df : pandas.DataFrame


    """
    # payload = {}
    if api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    headers = api_inputs.api_headers.default

    # upload Blobs to folder
    url = f"{api_inputs.api_projects_endpoint}/{api_inputs.api_project_id}/adx/operation-state?operationId={upload_id}"
    logger.info("Sending request: GET %s", url)

    response = requests.request("GET", url, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.url)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text)
    df = df.drop(columns=['NodeId', 'RootActivityId', 'Principal', 'User', 'Database'])
    return df


def load_data(dev_mode_path, api_inputs: ApiInputs):
    """Load data

    Parameters
    ----------
    dev_mode_path :

    api_inputs : ApiInputs
        Object returned by initialize() function.

    Returns
    -------
    pandas.DataFrame

    """
    if api_inputs.api_projects_endpoint == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    df = pandas.read_csv(dev_mode_path)

    return df


def data_table_exists(table_name: str, api_inputs: ApiInputs):
    """Validate if data table exists.

    Parameters
    ----------
    table_name: str :
        Table name to validate.
    api_inputs: ApiInputs
        Object returned by initialize() function.

    Returns
    -------
    bool
        True if the datatable exists. False if the table does not exist.

    """
    # payload = {}
    if api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    headers = api_inputs.api_headers.default

    url = f"{api_inputs.api_projects_endpoint}/{api_inputs.api_project_id}/adx/table?name={table_name}"
    logger.info("Sending request: GET %s", url)

    response = requests.request("GET", url, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.url)
        return response_status

    if response.text == 'true':
        logger.info("Response status: %s", response_status)
        logger.info("Data table '%s' exists.", table_name)
        return True
    else:
        logger.info("Response status: %s", response_status)
        logger.info("Data table '%s' does not exist.", table_name)
        return False


def get_sites(api_inputs: ApiInputs, include_tag_groups: Union[list, bool] = False,
              sql_where_clause: str = None, top_count: int = None):
    """Retrieve site information.

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.
    include_tag_groups : Union[list, bool], default = False
        If False, no tag groups are included. If True, all tag groups will be returned. Else, if list, the Tag Groups
        in the list are retrieved as columns.
    sql_where_clause : str, default = None
        Optional `WHERE` clause in SQL syntax. Use field names only and do not include the "WHERE".
    top_count: int, default = None
        For use during testing to limit the number of records returned.


    Returns
    -------
    df : pandas.DataFrame

    """

    if top_count is None:
        top_count = 0

    tags_mode = False
    tag_groups = []
    if type(include_tag_groups) is list:
        tags_mode = True
        tag_groups = include_tag_groups
    elif type(include_tag_groups) is bool:
        tag_groups = []
        tags_mode = include_tag_groups

    if sql_where_clause is not None:
        if sql_where_clause.startswith('WHERE') or sql_where_clause.startswith('where'):
            sql_where_clause = sql_where_clause.removeprefix('WHERE')
            sql_where_clause = sql_where_clause.removeprefix('where')

    payload = {
        "tagsMode": tags_mode,
        "includeTagColumns": tag_groups,
        "sqlWhereClause": sql_where_clause,
        "topCount": top_count,
    }

    if api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    headers = api_inputs.api_headers.default

    url = f"{api_inputs.api_projects_endpoint}/{api_inputs.api_project_id}/installations/sites-ingestion"
    logger.info("Sending request: POST %s", url)

    response = requests.post(url, json=payload, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.url)
        return response_status

    df = pandas.read_json(response.text, dtype={'InstallationCode': str})

    return df


def get_device_sensors(api_inputs: ApiInputs, include_tag_groups: Union[list, bool] = False,
                       include_metadata_keys: Union[list, bool] = False, sql_where_clause: str = None,
                       top_count: int = None, retries: int=5, backoff_factor: Union[int, float] = 0.3):
    """Retrieve device and sensor information.

    Optionally include all or a subset of tag groups and/or metadata keys depending on the configuration of the
    `include_tag_groups` and `include_metadata_keys` parameters. Whilst testing, there is the option to limit the number
    of records returned via the `top_count` parameter. If this parameter is not set, then the function will return all
    records.

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.
    include_tag_groups : Union[list, bool], default = False
        If False, no tag groups are included. If True, all tag groups will be returned. Else, if list, the Tag Groups
        in the list are retrieved as columns.
    include_metadata_keys : Union[list, bool], default = False
        If False, no metadata keys are included. If True, all metadata keys will be returned. Else, if list,
        the metadata keys in the list are retrieved as columns.
    sql_where_clause : str, optional
        optional `WHERE` clause in SQL syntax.
    top_count: int, default = None
        For use during testing to limit the number of records returned.
    retries : int
        Number of retries the retry would do before declaring it as an exception.  Max retries = 10.
        Defaults to 5.
    backoff_factor : Union[int, float]
        A backoff factor to apply between attempts after the second try (most errors are resolved immediately by a
        second try without a delay).
        {backoff factor} * (2 ** ({number of total retries} - 1)) seconds
        Defaults to 0.3

    Returns
    -------
    df : pandas.DataFrame

    """
    if (include_tag_groups is True or type(include_tag_groups) == list) and \
            (include_metadata_keys is True or type(include_metadata_keys) == list):
        logger.exception('Tags and Metadata cannot be returned in a single call. Please set either include_tag_groups '
                         'or include_metadata_keys to False. ')
        return

    if type(include_metadata_keys)==list:
        portfolio_metadata_keys = get_metadata_keys(api_inputs=api_inputs)
        if set(include_metadata_keys).issubset(portfolio_metadata_keys['MetadataKey'].values):
            logger.info('The required Metadata Keys exist in this portfolio. ')
        else:
            logger.exception('The required Metadata Keys do not exist in this portfolio. Unable to retrieve devices and '
                         'sensors. ')
            return pd.DataFrame()

    if type(include_tag_groups)==list:
        portfolio_tag_groups = get_tag_groups(api_inputs=api_inputs)
        if set(include_tag_groups).issubset(portfolio_tag_groups['TagGroup'].values):
            logger.info('The required Tag Groups exist in this portfolio. ')
        else:
            logger.exception('The required Tag Groups do not exist in this portfolio. Unable to retrieve devices and '
                         'sensors. ')
            return pd.DataFrame()


    limit = 50000
    offset = 0
    is_finished = False

    if top_count is None:
        top_count = 0

    if top_count > 0:
        limit = 0

    tags_mode = False
    tag_groups = []
    if type(include_tag_groups) is list:
        tags_mode = True
        tag_groups = include_tag_groups
    elif type(include_tag_groups) is bool:
        tag_groups = []
        tags_mode = include_tag_groups

    metadata_mode = False
    metadata_keys = []
    if type(include_metadata_keys) is list:
        metadata_mode = True
        metadata_keys = include_metadata_keys
    elif type(include_metadata_keys) is bool:
        metadata_keys = []
        metadata_mode = include_metadata_keys

    payload = {
        "tagsMode": tags_mode,
        "metadataMode": metadata_mode,
        "includeTagColumns": tag_groups,
        "includeMetadataColumns": metadata_keys,
        "sqlWhereClause": sql_where_clause,
        "topCount": top_count,
        "limit": limit,
        "offset": offset
    }

    if api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    headers = api_inputs.api_headers.default

    url = f"{api_inputs.api_projects_endpoint}/{api_inputs.api_project_id}/devices/device-sensors"
    logger.info("Sending request: POST %s", url)

    df_master = pandas.DataFrame()
    # holder of paginated dataframes
    df_data_chunks = []
    # Loop through pagination until encountered error message or empty Next URL
    while is_finished == False:
        df_data = ''
        # df_message = ''

        try:
            response = requests_retry_session2(
                retries=retries, backoff_factor=backoff_factor,
                status_forcelist=[408, 429, 500, 502, 503, 504]).post(url, json=payload, headers=headers)
            retries = requests_retry_session2.retries

            # response = requests.post(url, json=payload, headers=headers)
            response_status = '{} {}'.format(response.status_code, response.reason)

            if response.status_code != 200:
                logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                             response.reason)
                return response_status
            elif len(response.text) == 0:
                logger.error('No data returned for this API call. %s', response.request.url)
                return response_status

            response_dict = json.loads(response.text)

            if 'Message' in response_dict.keys() and len(response_dict['Message']) != 0 and response_dict['Message'] != '':
                logger.error(response_dict['Message'])
                is_finished = True
                return response_status, response_dict['Message']

            if 'Data' in response_dict.keys() and len(response_dict['Data'])==0 and len(df_data_chunks)==0:
                logger.error(f'No data returned for this API call. {response.request.url}')
                is_finished = True
                return pandas.DataFrame()
            elif 'Data' in response_dict.keys() and len(response_dict['Data']) != 0:
                df_data = pandas.DataFrame(response_dict['Data'])
                df_data_chunks.append(df_data)

            if 'NextUrl' in response_dict.keys() and len(response_dict['NextUrl']) != 0:
                payload = json.loads(response_dict['NextUrl'])
            else:
                is_finished = True
                df_master = pandas.concat(df_data_chunks, ignore_index=True)
                df_master.rename(columns={"InstallationID": "InstallationId", "ObjectPropertyID": "ObjectPropertyId"},
                                 inplace=True)
                return df_master
        except Exception as ex:
            logger.error("API Call was not successful. ", ex)
            is_finished = True
            return pandas.DataFrame()

    return df_master


def get_data(query_text, api_inputs: ApiInputs, query_language: QUERY_LANGUAGE = "kql",
             response_type: RESPONSE_TYPE = 'dataframe', retries: int = 5, backoff_factor: Union[int, float] = 2):
    """Retrieve data.

    Parameters
    ----------
    query_text : str
        SQL statement used to retrieve data.
    api_inputs : ApiInputs
        Object returned by initialize() function.
    query_language : QUERY_LANGUAGE, optional
        The query language the query_text is written in (Default value = 'sql').
    response_type : RESPONSE_TYPE, optional
        The type of the response to be provided - either dataframe or json
    retries :0 < int < 10
        Number of retries the retry would do before declaring it as an exception. Max retries = 10.
        Defaults to 5.
    backoff_factor : Union[int, float]
        A backoff factor to apply between attempts after the second try (most errors are resolved immediately by a
        second try without a delay).
        {backoff factor} * (2 ** ({number of total retries} - 1)) seconds
        Defaults to 2

    Returns
    -------
    df : pandas.DataFrame

    """
    payload = {
        "queryText": query_text,
        "queryLanguage": str(query_language)
    }

    if api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    headers = api_inputs.api_headers.default

    if not set([query_language]).issubset(set(QUERY_LANGUAGE.__args__)):
        logger.error('query_language parameter must be set to one of the allowed values defined by the '
                     'QUERY_LANGUAGE literal: %s', QUERY_LANGUAGE.__args__)
        return False

    url = f"{api_inputs.api_projects_endpoint}/{api_inputs.api_project_id}/adx/data"
    logger.info("Sending request: POST %s", url)

    # response = requests.post(url, json=payload, headers=headers)
    # response_status = '{} {}'.format(response.status_code, response.reason)
    # if response.status_code != 200:
    #     logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
    #                  response.reason)
    #     return response_status
    # elif len(response.text) == 0:
    #     logger.error('No data returned for this API call. %s', response.request.url)
    #     return response_status
    #
    # if response_type == 'dataframe':
    #     return pandas.read_json(response.text)
    # elif response_type == 'json':
    #     return json.loads(response.text)
    # else:
    #     return response.text
    try:
        response = requests_retry_session2(
            retries=retries, backoff_factor=backoff_factor,
            status_forcelist=[408, 429, 500, 502, 503, 504]).post(url, json=payload, headers=headers)
        retries=requests_retry_session2.retries

        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error(f"API Call was not successful. Max retries reached: {retries}. Response Status: {response.status_code}. Reason: {response.reason}.")
            return response_status
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.url)
            return response_status

        if response_type == 'dataframe':
            response_data_frame = pandas.read_json(response.text)
            return pandas.read_json(response.text)
        elif response_type == 'json':
            return json.loads(response.text)
        else:
            return response.text
    except Exception as ex:
        logger.error("API Call was not successful. ", ex)
        return pandas.DataFrame()


def get_states_by_country(api_inputs: ApiInputs, country: str):
    """Get list of States for selected country.

        Parameters
        ----------
        api_inputs : ApiInputs
            Object returned by initialize() function.
        country: str
            Country to lookup states for.

        Returns
        -------
        df : pandas.DataFrame
            Data frame containing the states for the given country.

        """
    # payload = {}
    if api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    headers = api_inputs.api_headers.default

    url = f"{api_inputs.api_base_url}/country/{country}/states"
    logger.info("Sending request: GET %s", url)

    response = requests.request("GET", url, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.url)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text)
    df.columns = _column_name_cap(df.columns)

    return df


def get_templates(api_inputs: ApiInputs, object_property_type: str = None):
    """Get list of Templates by Type.

    Also retrieves the default unit of measure for the given template.

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.
    object_property_type : str, Optional
        The object property type to filter to.

    Returns
    -------
    df : pandas.DataFrame
        Data frame containing the templates by type including the default unit of measure.

    """
    # payload = {}
    if api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    headers = api_inputs.api_headers.default

    url = ''
    if object_property_type is None:
        url = f"{api_inputs.api_projects_endpoint}/{api_inputs.api_project_id}/data-ingestion/templates"
    elif object_property_type is not None:
        url = f"{api_inputs.api_projects_endpoint}/{api_inputs.api_project_id}/data-ingestion/templates?type=" \
              f"{object_property_type}"

    logger.info("Sending request: GET %s", url)

    response = requests.request("GET", url, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.url)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text)
    df.columns = _column_name_cap(df.columns)

    return df


def get_tag_groups(api_inputs: ApiInputs):
    """Get the sensor-level tag groups present for a portfolio.

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.

    Returns
    -------
    df : pandas.DataFrame
        Data frame containing the tag groups present in the given portfolio.

    """
    # payload = {}
    if api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    headers = api_inputs.api_headers.default

    url = f"{api_inputs.api_projects_endpoint}/{api_inputs.api_project_id}/tags/tag-groups"

    logger.info("Sending request: GET %s", url)

    response = requests.request("GET", url, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.url)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text)
    df.columns = ['TagGroup']

    return df


def get_metadata_keys(api_inputs: ApiInputs):
    """Get the device-level metadata keys for a portfolio.

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.

    Returns
    -------
    df : pandas.DataFrame
        Data frame containing the metadata keys present in the portfolio.

    """
    # payload = {}
    if api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    headers = api_inputs.api_headers.default

    url = f"{api_inputs.api_projects_endpoint}/{api_inputs.api_project_id}/data-ingestion/metadata/all-type"
    logger.info("Sending request: GET %s", url)

    response = requests.request("GET", url, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.url)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text)
    if df.shape[1] == 0:
        df = pd.DataFrame({'MetadataKey':[]})
    else:
        df.columns = ['MetadataKey']

    return df


def get_units_of_measure(api_inputs: ApiInputs, object_property_type: str = None):
    """Get list of units of measure by type.

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.
    object_property_type : str, Optional
        The ObjectPropertyType to filter on.

    Returns
    -------
    df : pandas.DataFrame
        Data frame containing the units of measure by type.

    """
    # payload = {}

    if api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    headers = api_inputs.api_headers.default

    url = ''

    if object_property_type is None:
        url = f"{api_inputs.api_projects_endpoint}/{api_inputs.api_project_id}/data-ingestion/units"
    elif object_property_type is not None:
        url = f"{api_inputs.api_projects_endpoint}/{api_inputs.api_project_id}/data-ingestion/units?type=" \
              f"{object_property_type}"

    logger.info("Sending request: GET %s", url)

    response = requests.request("GET", url, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.url)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text)
    df.columns = _column_name_cap(df.columns)

    return df


def get_equipment_classes(api_inputs: ApiInputs):
    """Get list of Equipment Classes.

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.

    Returns
    -------
    df : pandas.DataFrame
        Data frame containing the equipment classes.

    """
    # payload = {}
    if api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    headers = api_inputs.api_headers.default

    url = f"{api_inputs.api_projects_endpoint}/{api_inputs.api_project_id}/installation/" \
          f"00000000-0000-0000-0000-000000000000/equipment/integration-classes"

    logger.info("Sending request: GET %s", url)

    if api_inputs.api_projects_endpoint == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    response = requests.request("GET", url, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.url)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text)
    df.columns = ['EquipmentClass']

    return df


def get_timezones(api_inputs: ApiInputs):
    """Get timezones

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.

    Returns
    -------
    df : pandas.DataFrame
    """
    headers = api_inputs.api_headers.default

    if api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    url = f"{api_inputs.api_base_url}/timezones/all"
    logger.info("Sending request: GET %s", url)

    response = requests.request("GET", url, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.url)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text)
    df.columns = _column_name_cap(df.columns)

    return df


def connect_to_sql(api_inputs: ApiInputs):
    """Create a pyodbc connection to SQL

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.

    Returns
    -------
    conn : pyodbc.Connection
    """
    cs = _get_sql_connection_string(api_inputs=api_inputs)
    sql_server_name, sql_server_user_name, sql_server_password = _extract_sql_credentials(cs)

    conn = pyodbc.connect(
        f'Driver={{ODBC Driver 17 for SQL Server}};SERVER={sql_server_name}'
        f';DATABASE=Switch;UID={sql_server_user_name};PWD={sql_server_password};ApplicationIntent=ReadOnly',
        readonly=True)

    return conn

# def get_portfolios(api_inputs: ApiInputs, search_term: str = None):
#     """Get list of units of measure by type.
#
#     Parameters
#     ----------
#     api_inputs : ApiInputs
#         Object returned by initialize() function.
#     search_term : str
#         The search_term used to filter list of portfolios to be retrieved.
#
#     Returns
#     -------
#     df : pandas.DataFrame
#         A list of portfolios.
#
#     """
#     payload = {}
#     headers = {
#         'x-functions-key': api_inputs.api_key,
#         'Content-Type': 'application/json; charset=utf-8',
#         'user-key': api_inputs.user_id
#     }
#
#     if api_inputs.datacentre == '' or api_inputs.api_key == '':
#         logger.error("You must call initialize() before using API.")
#         return pandas.DataFrame()
#
#     if search_term is None:
#         search_term = '*'
#
#     url = api_prefix + "Portfolios/" + search_term
#     response = requests.request("GET", url, timeout=20, headers=headers)
#     response_status = '{} {}'.format(response.status_code, response.reason)
#     if response.status_code != 200:
#         logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
#                      response.reason)
#         return response_status, pandas.DataFrame()
#     elif len(response.text) == 0:
#         logger.error('No data returned for this API call. %s', response.request.url)
#         return response_status, pandas.DataFrame()
#
#     df = pandas.read_json(response.text)
#
#     return df


def amortise_across_days(raw_df: pandas.DataFrame, start_date_col:str, end_date_col: str, value_col: str,
                         amortise_method: AMORTISATION_METHOD = "Exclusive"):
    """Amortise data across days in period.

    The period is defined by the `start_date_col` and `end_date_col`.

    Parameters
    ----------
    raw_df : pandas.DataFrame
        The raw dataframe to be amortised.
    start_date_col : str
        The name of the column containing the start date of the period
    end_date_col : str
        The name of the column containing the end date of the period
    value_col : str
        The name of the column containing the numeric data to be amortised across the period.
    amortise_method : AMORTISATION_METHOD, optional
        Whether the amortisation should be inclusive or exclusive of the end date.

    Returns
    -------
    amortised_df : pandas.DataFrame
        Returned dataframe will contain three additional columns: num_days, amortised_value, Timestamp
    """

    if not set([start_date_col, end_date_col, value_col]).issubset(raw_df.columns):
        col_lookup = pandas.DataFrame({'ColumnType': ['start_date_col', 'end_date_col', 'value_col'],
                                     'ColumnName': [start_date_col, end_date_col, value_col]})
        logger.exception(f"The raw_df does not contain column(s) defined for the input parameter(s): "
                         f"{col_lookup[col_lookup.ColumnName.isin(list(set([start_date_col, end_date_col, value_col]).difference(raw_df.columns)))].ColumnType.values.tolist()}")
        return False

    start = start_date_col
    end = end_date_col

    if amortise_method == "Exclusive":
        raw_df['num_days'] = (raw_df[end] - raw_df[start]).dt.days
        raw_df['amortised_value'] = raw_df[value_col] / raw_df['num_days']

        def make_list(row):
            # make list of dates between Start Date & End Date (exclusive of the End Date).
            return pd.date_range(start=row[start], end=row[end], freq='D').to_list()[:-1]

        raw_df['Timestamp'] = raw_df[[start, end]].apply(lambda x: make_list(x), axis=1)
        explode_df = raw_df.explode(column='Timestamp')

        return explode_df
    elif amortise_method == "Inclusive":
        raw_df['num_days'] = (raw_df[end] - raw_df[start]).dt.days + 1
        raw_df['amortised_value'] = raw_df[value_col] / raw_df['num_days']

        def make_list(row):
            return pd.date_range(start=row[start], end=row[end], freq='D').to_list()

        raw_df['Timestamp'] = raw_df[[start, end]].apply(lambda x: make_list(x), axis=1)
        explode_df = raw_df.explode(column='Timestamp')

        return explode_df


def get_metadata_where_clause(meta_columns:list):
    sql_where_clause = ''.join(
        ['([' + col + '] IS NOT NULL) AND '
         if (col != meta_columns[-1])
         else '([' + col + '] IS NOT NULL)' for col in
         meta_columns])

    return sql_where_clause

