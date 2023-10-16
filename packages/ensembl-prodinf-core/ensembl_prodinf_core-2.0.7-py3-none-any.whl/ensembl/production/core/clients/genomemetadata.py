#   See the NOTICE file distributed with this work for additional information
#   regarding copyright ownership.
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from ensembl.production.core.rest import RestClient
from ensembl.production.core.utils import json_decode_error_context


class GenomeMetadataRestClient(RestClient):
    """
       Client for interacting with the Ensembl metadata REST API.
    """

    dataset_endpoint = '{}api/genome_metadata/datasets/'
    dataset_uuid_endpoint = '{}api/genome_metadata/datasets/{}'
    genome_endpoint = '{}api/genome_metadata/genomes/'
    genome_uuid_endpoint = '{}api/genome_metadata/genomes/{}'

    def __init__(self, uri):
        super().__init__(uri)

    def _session(self, use_ssl=False):
        session = super()._session(use_ssl)
        return session

    def create_dataset(self, dataset):
        """
        Create a new dataset using the provided details.
        """
        with self._session() as session:
            r = session.post(self.dataset_endpoint.format(self.uri), json=dataset)
        r.raise_for_status()
        return r.json()

    def get_all_datasets(self):
        """
        Get all datasets.
        """
        with self._session() as session:
            r = session.get(self.dataset_endpoint.format(self.uri))
        r.raise_for_status()
        return r.json()

    def get_dataset_by_uuid(self, uuid):
        """
        Get a dataset by its UUID.
        """
        with self._session() as session:
            r = session.get(self.dataset_uuid_endpoint.format(self.uri, uuid))
        r.raise_for_status()
        return r.json()

    def get_all_genomes(self):
        """
        Get all genomes.
        """
        with self._session() as session:
            r = session.get(self.genome_endpoint.format(self.uri))
        r.raise_for_status()
        return r.json()

    def get_genome_by_uuid(self, uuid):
        """
        Get a genome by its UUID.
        """
        with self._session() as session:
            r = session.get(self.genome_uuid_endpoint.format(self.uri, uuid))
        r.raise_for_status()
        return r.json()

