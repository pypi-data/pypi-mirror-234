import logging
import pandas as pd
import io
import os
import requests
from requests.auth import HTTPBasicAuth
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy import units as u
from timewise import ParentSampleBase, WISEDataDESYCluster

from timewise_sup.config_loader import TimewiseSUPConfig


logger = logging.getLogger(__name__)


def get_bts_config():
    wise_data = WISEDataDESYCluster(
        base_name="bts_sample",
        parent_sample_class=BTSParentSample,
        n_chunks=1,
        min_sep_arcsec=6
    )
    config = TimewiseSUPConfig(
        database_name=wise_data.base_name,
        wise_data=wise_data
    )
    return config


class BTSParentSample(ParentSampleBase):

    default_keymap = {
        "ra": "ra_deg",
        "dec": "dec_deg",
        "id": "IAUID"
    }

    base_name = "bts_sample"

    url = (
        "https://sites.astro.caltech.edu/ztf/rcf/explorer.php?f=s&"
        "coverage=any&samprcf=y&sampdeep=y&subsample=cantrans&classstring=&classexclude=&quality=y&ztflink=fritz&"
        "startsavedate=&startpeakdate=&startlastdate=&startra=&startdec=&startz=&startdur=&startrise=&startfade=&"
        "startpeakmag=&startlastmag=&startabsmag=&starthostabs=&starthostcol=&startsavevis=&startlatevis=&"
        "startcurrvis=&startb=&startav=&endsavedate=&endpeakdate=&endlastdate=&endra=&enddec=&endz=&enddur=&endrise=&"
        "endfade=&endpeakmag=&endlastmag=&endabsmag=&endhostabs=&endhostcol=&endsavevis=&endlatevis=&endcurrvis=&"
        "endb=&endav=&sort=savedate&format=csv"
    )

    def __init__(self):
        super(BTSParentSample, self).__init__(base_name=BTSParentSample.base_name)

        if not os.path.isfile(self.local_sample_copy):
            self.df = self.make_sample()
            self.save_local()

        self.df = pd.read_csv(
            self.local_sample_copy,
            index_col=0
        )

    @staticmethod
    def make_sample():
        logger.info("downloading BTS sample")

        auth = HTTPBasicAuth("bts", "rcf")
        res = requests.get(BTSParentSample.url, auth=auth)

        if res.status_code != 200:
            msg = f"Trying to load BTS sample resulted in status code {res.status_code}!"
            raise requests.exceptions.ConnectionError(msg)

        else:
            logger.info("download successful")

        df = pd.read_csv(io.StringIO(res.content.decode()))
        logger.debug(f"{len(df)} objects")

        logger.info("converting coordinates to degrees")
        coord = SkyCoord(df["RA"], df["Dec"], unit=(u.hourangle, u.deg))
        df["ra_deg"] = coord.ra.value
        df["dec_deg"] = coord.dec.value

        logger.info("converting times to mjds")
        df["peakt_mjd"] = Time(df["peakt"] + 2458000, format="jd").mjd

        logger.info("done")
        return df
