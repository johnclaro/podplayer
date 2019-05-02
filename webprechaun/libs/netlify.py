import logging
import copy
from urllib.parse import urljoin
from dataclasses import dataclass, field
from typing import Dict

import requests


class Netlify:

    def __init__(
        self, 
        access_token: str, 
        scheme: str='https', 
        host: str='api.netlify.com', 
        version: str='/api/v1/'
    ):
        """The primary Netlify class.

            :param access_token: Personal access token generated by Netlify.
            :param scheme: Scheme of Netlify's API url.
            :param host: Host of Netlify's API url.
            :param version: Version of Netlify's API url.
        """
        self.access_token = access_token
        self.scheme = scheme
        self.host = host
        self.version = version
        self.url = f'{scheme}://{host}{version}'
        self.headers = {'Authorization': f'Bearer {access_token}'}
        self.URL_SITES = urljoin(self.url, 'sites')

    def create_site(self, name: str) -> dict:
        """Create site in Netlify.

            :param name: Name of site.
        """
        data = {'name': name}
        response = requests.post(
            self.URL_SITES, 
            data=data, 
            headers=self.headers
        )

        return response.json()

    def get_sites(self) -> list:
        """Get list of sites in Netlify."""
        response = requests.get(self.URL_SITES, headers=self.headers)

        return response.json()

    def deploy_site(self, name: str) -> dict:
        """Deploy new or updated version of website.

        Netlify supports two ways of doing deploys:

        1. Sending a digest of all files in your deploy and then uploading any
        files Netlify doesn't already have on its storage servers.

        2. Sending a zipped website and letting Netlify unzip and deploy.

        This function uses the latter.

            :param site: Name of site.
        """
        headers = copy.deepcopy(self.headers)
        headers['Content-Type'] = 'application/zip'

        sites = self.get_sites()
        for site in sites:
            if site['name'] == name:
                site_id = site['id']
                break

        if not site_id:
            logging.warning(f"Site '{site_id}' not found.")

        logging.debug('Opening zip file...')
        try:
            with open('webprechaun.zip', 'rb') as zip_file:
                url = f'{self.URL_SITES}/{site_id}/deploys'
                response = requests.post(url, headers=headers, data=zip_file)
                return response.json()
        except FileNotFoundError as file_not_found_error:
            logging.error(file_not_found_error)
            # TODO: What would be a good fallback if app zip file is missing?
            return {'status': 'error', 'reason': file_not_found_error}