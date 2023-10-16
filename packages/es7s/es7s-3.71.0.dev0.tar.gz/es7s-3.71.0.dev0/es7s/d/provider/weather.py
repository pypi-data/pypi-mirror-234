# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from ._base import DataProvider
from es7s.shared import WeatherInfo, get_merged_uconfig


class WeatherProvider(DataProvider[WeatherInfo]):
    URL_TEMPLATE = "https://wttr.in/%(loc)s?format=%(fmt)s"
    QUERY_FORMAT = "%c|%t|%w&M"

    def __init__(self):
        self._location = get_merged_uconfig().get('provider.weather', 'location')

        super().__init__('weather', 'weather', 30.0)

    def _collect(self) -> WeatherInfo:
        url = self.URL_TEMPLATE % {'loc': self._location, 'fmt': self.QUERY_FORMAT}
        response = self._make_request(url)
        fields = response.text.split('|')
        return WeatherInfo(self._location, fields)
