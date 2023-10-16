# -*- coding: utf-8 -*-
"""
@author: Noemi E. Cazzaniga - 2023
@email: noemi.cazzaniga@polimi.it
"""


import requests
from pandas import DataFrame


__BASE_URL__ = 'https://fenixservices.fao.org/faostat/api/v1/en/'


def __getresp__(url, https_proxy, params=None):
    """
    Makes a request and returns the response.

    Parameters
    ----------
    url : str
        URL for the request.
    https_proxy : list
        parameters for https proxy: 
        [username, password, url:port].
    params : dict, optional
        parameters to pass in URLs:
            {key: value, ...}.
        The default is None.

    Raises
    ------
    Exception
        if there is a connection problem,
        if the dataset was not found.

    Returns
    -------
    resp : response

    """
    try:
        if ':' not in https_proxy[2]:
            print("Error in proxy host. It must be in the form: 'url:port'")
            return
        proxydic = {'https': 'https://' +\
                    https_proxy[0] + ':' +\
                    requests.compat.quote(https_proxy[1]) + '@' +\
                    https_proxy[2]}
    except:
        proxydic = None
    with requests.get(url, params=params, timeout=120., proxies=proxydic) as resp:
        if resp.status_code == 500 and resp.text == 'Index: 0, Size: 0':
            print("{0} not found in the Faostat server".format(url.split('?')[0].split('/')[-1]))
            raise Exception()
        if resp.status_code == 524:
            raise TimeoutError()
        resp.raise_for_status()
        return resp


def __getlabcode__(url, https_proxy):
    """
    Make a request and return the response as a dict of label: code.

    Parameters
    ----------
    url : str
        URL for the request.
    https_proxy : list
        parameters for https proxy: 
        [username, password, url:port].

    Returns
    -------
    d : dict
        {label: code, ...}.

    """
    d = dict()
    response = __getresp__(url, https_proxy)
    data = response.json()['data']
    for el in data:
        d[el['label']] = el['code']
    return d


def list_datasets(https_proxy=None):
    """
    Returns a list of datasets available on the Faostat server.

    Parameters
    ----------
    https_proxy : list, optional
        parameters for https proxy: 
        [username, password, url:port].
        The default is None (no proxy).

    Returns
    -------
    l : list
        list of available datasets and some metadata.

    """
    l = [('code',
          'label',
          'date_update',
          'note_update',
          'release_current',
          'state_current',
          'year_current',
          'release_next',
          'state_next',
          'year_next'),
         ]
    response = __getresp__(__BASE_URL__ + 'groups', https_proxy)
    groups = [el['code'] for el in response.json()['data']]
    for group_code in groups:
        url = __BASE_URL__ + 'domains/' + group_code
        response = __getresp__(url, https_proxy)
        domains = response.json()['data']
        for d in domains:
            if d.get('date_update', None) is not None:
                l.append((d.get('code', None),
                          d.get('label', None),
                          d['date_update'],
                          d.get('note_update', None),
                          d.get('release_current', None),
                          d.get('state_current', None),
                          d.get('year_current', None),
                          d.get('release_next', None),
                          d.get('state_next', None),
                          d.get('year_next', None))
                          )
    return l


def list_datasets_df(https_proxy=None):
    """
    Returns a pandas dataframe listing the datasets available on the Faostat server.

    Parameters
    ----------
    https_proxy : list, optional
        parameters for https proxy: 
        [username, password, url:port].
        The default is None (no proxy).

    Returns
    -------
    l : dataframe
        list of available datasets and some metadata.

    """
    d = list_datasets(https_proxy)
    return DataFrame(d[1:], columns=d[0])


def get_areas(code, https_proxy=None):
    """
    DEPRECATED - use get_par instead
    Given the code of a Faostat dataset,
    returns the available areas as dict.

    Parameters
    ----------
    code : str
        code of the dataset.
    https_proxy : list, optional
        parameters for https proxy: 
        [username, password, url:port].
        The default is None (no proxy).

    Returns
    -------
    d : dict
        {label: code, ...}.

    """
    url = __BASE_URL__ + 'codes/area/' + code
    return __getlabcode__(url, https_proxy)


def get_years(code, https_proxy=None):
    """
    DEPRECATED - use get_par instead
    Given the code of a Faostat dataset,
    returns the available years as dict.

    Parameters
    ----------
    code : str
        code of the dataset.
    https_proxy : list, optional
        parameters for https proxy: 
        [username, password, url:port].
        The default is None (no proxy).

    Returns
    -------
    d : dict
        {label: code, ...}.

    """
    url = __BASE_URL__ + 'codes/year/' + code
    return __getlabcode__(url, https_proxy)


def get_elements(code, https_proxy=None):
    """
    DEPRECATED - use get_par instead
    Given the code of a Faostat dataset,
    returns the available elements as dict.

    Parameters
    ----------
    code : str
        code of the dataset.
    https_proxy : list, optional
        parameters for https proxy: 
        [username, password, url:port].
        The default is None (no proxy).

    Returns
    -------
    d : dict
        {label: code, ...}.

    """
    url = __BASE_URL__ + 'codes/elements/' + code
    return __getlabcode__(url, https_proxy)


def get_items(code, https_proxy=None):
    """
    DEPRECATED - use get_par instead
    Given the code of a Faostat dataset,
    returns the available items as dict.

    Parameters
    ----------
    code : str
        code of the dataset.
    https_proxy : list, optional
        parameters for https proxy: 
        [username, password, url:port].
        The default is None (no proxy).

    Returns
    -------
    d : dict
        {label: code, ...}.

    """
    url = __BASE_URL__ + 'codes/items/' + code
    return __getlabcode__(url, https_proxy)


def list_pars(code, https_proxy=None):
    """
    Given the code of a Faostat dataset,
    returns the available parameters as list.

    Parameters
    ----------
    code : str
        code of the dataset.
    https_proxy : list, optional
        parameters for https proxy: 
        [username, password, url:port].
        The default is None (no proxy).

    Returns
    -------
    d : list
        parameters for data filtering.

    """
    url = __BASE_URL__ + 'dimensions/' + code
    d = []
    response = __getresp__(url, https_proxy)
    data = response.json()['data']
    for el in data:
        d.append(el['id'])
    return d


def get_par(code, par, https_proxy=None):
    """
    Given the code of a Faostat dataset,
    and the name of one of its parameters,
    returns the available values as dict.

    Parameters
    ----------
    code : str
        code of the dataset.
    https_proxy : list, optional
        parameters for https proxy: 
        [username, password, url:port].
        The default is None (no proxy).

    Returns
    -------
    d : dict
        {label: code, ...}.

    """
    url = __BASE_URL__ + 'codes/' + par + '/' + code
    return __getlabcode__(url, https_proxy)


def get_data(code, pars={}, show_flags=False, null_values=False, https_proxy=None):
    """
    Given the code of a Faostat dataset,
    returns the data as a list of tuples.
    To download only a subset of the dataset, you need to pass pars={key: value, ...}:
    from the codes obtained with get_par_list and get_par

    Parameters
    ----------
    code : str
        code of the dataset.
    pars : dict, optional
        parameters to retrieve a subset of the dataset:
            {key: value, ...}.
        The default is {}.
    show_flags : bool, optional
        True to download also the data flags.
        The default is False.
    https_proxy : list, optional
        parameters for https proxy: 
        [username, password, url:port].
        The default is None (no proxy).

    Returns
    -------
    l : list
        data with header.

    """
    url = __BASE_URL__ + 'data/' + code
    params = list(pars.items())
    params += [('area_cs', 'FAO'),
               ('show_code', True),
               ('show_unit', True),
               ('show_flags', show_flags),
               ('null_values', null_values),
               ('limit', -1),
               ('output_type', 'objects')
              ]
    response = __getresp__(url, https_proxy, params=params)
    try:
        dsd = response.json()['metadata']['dsd']
    except:
        print('Warning: seems like no data are available for your selection')
        return []
    header = tuple([d['label'] for d in dsd])
    l = [header,]
    data = response.json()['data']
    for row in data:
        l += [tuple([row.get(h,None) for h in header]),]
    return l


def get_data_df(code, pars={}, show_flags=False, null_values=False, https_proxy=None):
    """
    Given the code of a Faostat dataset,
    returns the data as pandas dataframe.
    To download only a subset of the dataset, you need to pass pars={key: value, ...}.
    key can be one or more of the following string:
        'areas', 'years', 'elements', 'items'
         value can be a number, a string or a list, from the codes obtained with
             get_areas, get_years, get_elements, get_items
     
    Parameters
    ----------
    code : str
        code of the dataset.
    pars : dict, optional
        parameters to retrieve a subset of the dataset:
            {key: value, ...}.
        The default is {}.
    show_flags : bool, optional
        True to download also the data flags.
        The default is False.
    https_proxy : list, optional
        parameters for https proxy: 
        [username, password, url:port].
        The default is None (no proxy).
     
    Returns
    -------
    l : dataframe
        data with header.
     
    """
    d = get_data(code, pars=pars, show_flags=show_flags, null_values=null_values, https_proxy=https_proxy)
    return DataFrame(d[1:], columns=d[0])
