# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from pts.website.testing import PTS_WEBSITE_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that pts.website is properly installed."""

    layer = PTS_WEBSITE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if pts.website is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'pts.website'))

    def test_browserlayer(self):
        """Test that IPtsWebsiteLayer is registered."""
        from pts.website.interfaces import (
            IPtsWebsiteLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IPtsWebsiteLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = PTS_WEBSITE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['pts.website'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if pts.website is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'pts.website'))

    def test_browserlayer_removed(self):
        """Test that IPtsWebsiteLayer is removed."""
        from pts.website.interfaces import \
            IPtsWebsiteLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IPtsWebsiteLayer,
            utils.registered_layers())
