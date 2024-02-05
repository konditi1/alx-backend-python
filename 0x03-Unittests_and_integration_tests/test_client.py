#!/usr/bin/env python3
""" Module for testing client """

import json

import unittest

from client import GithubOrgClient

from parameterized import parameterized, parameterized_class

from fixtures import TEST_PAYLOAD

from unittest.mock import patch, PropertyMock, Mock


class TestGithubOrgClient(unittest.TestCase):
    """ Class for Testing Github Org Client """

    @parameterized.expand([
        ('google'),
        ('abc')
    ])
    @patch('client.get_json')
    def test_org(self, input, mock):
        """Test that GithubOrgClient.org returns the correct value"""
        test_class = GithubOrgClient(input)
        test_class.org()
        mock.assert_called_once_with(f'https://api.github.com/orgs/{input}')

    def test_public_repos_url(self):
        """ Test that the result of _public_repos_url is the expected one
        based on the mocked payload
        """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock:
            payload = {"repos_url": "World"}
            mock.return_value = payload
            test_class = GithubOrgClient('test')
            result = test_class._public_repos_url
            self.assertEqual(result, payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_json):
        """
        Test that the list of repos is what you expect from the chosen payload.
        Test that the mocked property and the mocked get_json was called once.
        """
        json_payload = [{"name": "Google"}, {"name": "Twitter"}]
        mock_json.return_value = json_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public:

            mock_public.return_value = "hello/world"
            test_class = GithubOrgClient('test')
            result = test_class.public_repos()

            check = [i["name"] for i in json_payload]
            self.assertEqual(result, check)

            mock_public.assert_called_once()
            mock_json.assert_called_once()

@parameterized.expand([
    # Test case for when the license key matches the expected license key
    ({"license": {"key": "my_license"}}, "my_license", True),
    # Test case for when the license key does not match the expected license key
    ({"license": {"key": "other_license"}}, "my_license", False)
])
def test_has_license(self, repo, license_key, expected):
    """
    Unit test for GithubOrgClient.has_license.

    Args:
        repo (dict): The repository object.
        license_key (str): The license key to check.
        expected (bool): The expected result of the has_license method.

    Returns:
        None
    """
    # Call the has_license method and store the result
    result = GithubOrgClient.has_license(repo, license_key)
    # Assert that the result matches the expected value
    self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Class for Integration test of fixtures """

    @classmethod
    def setUpClass(cls):
        """A class method called before tests in an individual class are run"""

        config = {'return_value.json.side_effect':
                  [
                      cls.org_payload, cls.repos_payload,
                      cls.org_payload, cls.repos_payload
                  ]
                  }
        cls.get_patcher = patch('requests.get', **config)

        cls.mock = cls.get_patcher.start()

def test_public_repos(self):
    """Test for the public_repos method of GithubOrgClient."""

    # Setup
    test_class = GithubOrgClient("google")

    # Assertions
    self.assertEqual(test_class.org, self.org_payload)
    self.assertEqual(test_class.repos_payload, self.repos_payload)
    self.assertEqual(test_class.public_repos(), self.expected_repos)
    self.assertEqual(test_class.public_repos("XLICENSE"), [])
    
    # Teardown
    self.mock.assert_called()

def test_public_repos_with_license(self):
    """Test for retrieving public repositories with a specified license."""
    # Initialize the GithubOrgClient with the organization name "google"
    test_class = GithubOrgClient("google")

    # Assert that calling public_repos() returns the expected_repos list
    self.assertEqual(test_class.public_repos(), self.expected_repos)

    # Assert that calling public_repos("XLICENSE") returns an empty list
    self.assertEqual(test_class.public_repos("XLICENSE"), [])

    # Assert that calling public_repos("apache-2.0") returns the apache2_repos list
    self.assertEqual(test_class.public_repos("apache-2.0"), self.apache2_repos)

    # Ensure that the mock object's assert_called method was called
    self.mock.assert_called()

@classmethod
def tearDownClass(cls):
    """Teardown the test class after all tests have run."""
    # Stop the patcher to clean up resources
    cls.get_patcher.stop()