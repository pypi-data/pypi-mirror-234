import pandas as pd
import wbpy

def _get_dataframe(self, indicator, country_codes=None,
            **kwargs):
    """Download data and return it as a dataframe."""
    dataset = self.get_dataset(indicator, country_codes=country_codes, **kwargs)
    data_df = pd.DataFrame.from_dict(dataset.as_dict()).T.melt(var_name='year',
                                                               value_name=indicator,
                                                               ignore_index=False)

    data_df = pd.merge(self.countries["name"], data_df, left_index=True, right_index=True) \
                    .rename(columns={"name":"country"}) \
                    .sort_values(by=["year", "country"]) \
                    .reset_index(drop=True)
    
    return data_df

def wbapi():
    """Dummy api wrapper to accommodate JupyterLite / Pyodide."""
    wbpy.IndicatorAPI.get_dataframe = _get_dataframe
    try:
        import pyodide
        def fetch_patch(url):
            with pyodide.http.open_url(url) as f:
                return f.getvalue()
        api = wbpy.IndicatorAPI(fetch=fetch_patch)
        api.BASE_URL = "https://api.worldbank.org/v2/"
    except:
        api = wbpy.IndicatorAPI()

    api.countries = pd.DataFrame.from_dict(api.get_countries()).T
    return api

