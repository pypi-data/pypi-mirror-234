# Class for performing search operations using the client


class Search:
    def __init__(self, client):
        self.client = client
        self.session = self.client.session

    def get_systems(self):
        # Get system data
        response = self.session.get(self.client.url + "/system")

        # Check response error code
        if response.status_code != 200:
            raise Exception("Error getting systems: " + response.text)

        # Return systems
        return response.json()

    def get_antigens(self):
        # Get antigen data
        response = self.session.get(self.client.url + "/antigen")

        # Check response error code
        if response.status_code != 200:
            raise Exception("Error getting antigens: " + response.text)

        # Return antigens
        return response.json()

    def get_alleles(self):
        # Get allele data
        response = self.session.get(self.client.url + "/allele")

        # Check response error code
        if response.status_code != 200:
            raise Exception("Error getting alleles: " + response.text)

        # Return alleles
        return response.json()

    def get_variants(self):
        # Get variant data
        response = self.session.get(self.client.url + "/variant")

        # Check response error code
        if response.status_code != 200:
            raise Exception("Error getting variants: " + response.text)

        # Return variants
        return response.json()

    def get_phenotypes(self):
        # Get phenotype data
        response = self.session.get(self.client.url + "/phenotype")

        # Check response error code
        if response.status_code != 200:
            raise Exception("Error getting phenotypes: " + response.text)

        # Return phenotypes
        return response.json()

    def get_genes(self):
        # Get genes data
        response = self.session.get(self.client.url + "/gene")

        # Check response error code
        if response.status_code != 200:
            raise Exception("Error getting genes: " + response.text)

        # Return genes
        return response.json()
