# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
App Menus
"""

import re
import logging
import warnings

from rattail.app import GenericHandler
from rattail.util import import_module_path, prettify, simple_error

from webhelpers2.html import tags, HTML

from tailbone.db import Session


log = logging.getLogger(__name__)


class MenuHandler(GenericHandler):
    """
    Base class and default implementation for menu handler.
    """

    def make_raw_menus(self, request, **kwargs):
        """
        Generate a full set of "raw" menus for the app.

        The "raw" menus are basically just a set of dicts to represent
        the final menus.
        """
        # first try to make menus from config, but this is highly
        # susceptible to failure, so try to warn user of problems
        try:
            menus = self.make_menus_from_config(request)
            if menus:
                return menus
        except Exception as error:

            # TODO: these messages show up multiple times on some pages?!
            # that must mean the BeforeRender event is firing multiple
            # times..but why??  seems like there is only 1 request...
            log.warning("failed to make menus from config", exc_info=True)
            request.session.flash(simple_error(error), 'error')
            request.session.flash("Menu config is invalid! Reverting to menus "
                                  "defined in code!", 'warning')
            msg = HTML.literal('Please edit your {} ASAP.'.format(
                tags.link_to("Menu Config", request.route_url('configure_menus'))))
            request.session.flash(msg, 'warning')

        # okay, no config, so menus must be built from code..

        # first check for a "simple menus" module; use that if defined
        menumod = self.config.get('tailbone', 'menus')
        if menumod:
            menumod = import_module_path(menumod)
            if (not hasattr(menumod, 'simple_menus')
                or not callable(menumod.simple_menus)):
                raise RuntimeError("module does not have a simple_menus() "
                                   "callable: {}".format(menumod))
            return menumod.simple_menus(request)

        # now we fallback to menu handler method
        return self.make_menus(request)

    def make_menus_from_config(self, request, **kwargs):
        """
        Try to build a complete menu set from config/settings.

        This will look in the DB settings table, or config file, for
        menu data.  If found, it constructs menus from that data.
        """
        # bail unless config defines top-level menu keys
        main_keys = self.config.getlist('tailbone.menu', 'menus')
        if not main_keys:
            return

        model = self.model
        menus = []

        # menu definition can come either from config file or db
        # settings, but if the latter then we want to optimize with
        # one big query
        if self.config.getbool('tailbone.menu', 'from_settings',
                               default=False):

            # fetch all menu-related settings at once
            query = Session().query(model.Setting)\
                             .filter(model.Setting.name.like('tailbone.menu.%'))
            settings = self.app.cache_model(Session(), model.Setting,
                                            query=query, key='name',
                                            normalizer=lambda s: s.value)
            for key in main_keys:
                menus.append(self.make_single_menu_from_settings(request, key,
                                                                 settings))

        else: # read from config file only
            for key in main_keys:
                menus.append(self.make_single_menu_from_config(request, key))

        return menus

    def make_single_menu_from_config(self, request, key, **kwargs):
        """
        Makes a single top-level menu dict from config file.  Note
        that this will read from config file(s) *only* and avoids
        querying the database, for efficiency.
        """
        menu = {
            'key': key,
            'type': 'menu',
            'items': [],
        }

        # title
        title = self.config.get('tailbone.menu',
                                'menu.{}.label'.format(key),
                                usedb=False)
        menu['title'] = title or prettify(key)

        # items
        item_keys = self.config.getlist('tailbone.menu',
                                        'menu.{}.items'.format(key),
                                        usedb=False)
        for item_key in item_keys:
            item = {}

            if item_key == 'SEP':
                item['type'] = 'sep'

            else:
                item['type'] = 'item'
                item['key'] = item_key

                # title
                title = self.config.get('tailbone.menu',
                                        'menu.{}.item.{}.label'.format(key, item_key),
                                        usedb=False)
                item['title'] = title or prettify(item_key)

                # route
                route = self.config.get('tailbone.menu',
                                        'menu.{}.item.{}.route'.format(key, item_key),
                                        usedb=False)
                if route:
                    item['route'] = route
                    item['url'] = request.route_url(route)

                else:

                    # url
                    url = self.config.get('tailbone.menu',
                                          'menu.{}.item.{}.url'.format(key, item_key),
                                          usedb=False)
                    if not url:
                        url = request.route_url(item_key)
                    elif url.startswith('route:'):
                        url = request.route_url(url[6:])
                    item['url'] = url

                # perm
                perm = self.config.get('tailbone.menu',
                                       'menu.{}.item.{}.perm'.format(key, item_key),
                                       usedb=False)
                item['perm'] = perm or '{}.list'.format(item_key)

            menu['items'].append(item)

        return menu

    def make_single_menu_from_settings(self, request, key, settings, **kwargs):
        """
        Makes a single top-level menu dict from DB settings.
        """
        menu = {
            'key': key,
            'type': 'menu',
            'items': [],
        }

        # title
        title = settings.get('tailbone.menu.menu.{}.label'.format(key))
        menu['title'] = title or prettify(key)

        # items
        item_keys = self.config.parse_list(
            settings.get('tailbone.menu.menu.{}.items'.format(key)))
        for item_key in item_keys:
            item = {}

            if item_key == 'SEP':
                item['type'] = 'sep'

            else:
                item['type'] = 'item'
                item['key'] = item_key

                # title
                title = settings.get('tailbone.menu.menu.{}.item.{}.label'.format(
                    key, item_key))
                item['title'] = title or prettify(item_key)

                # route
                route = settings.get('tailbone.menu.menu.{}.item.{}.route'.format(
                    key, item_key))
                if route:
                    item['route'] = route
                    item['url'] = request.route_url(route)

                else:

                    # url
                    url = settings.get('tailbone.menu.menu.{}.item.{}.url'.format(
                        key, item_key))
                    if not url:
                        url = request.route_url(item_key)
                    if url.startswith('route:'):
                        url = request.route_url(url[6:])
                    item['url'] = url

                # perm
                perm = settings.get('tailbone.menu.menu.{}.item.{}.perm'.format(
                    key, item_key))
                item['perm'] = perm or '{}.list'.format(item_key)

            menu['items'].append(item)

        return menu

    def make_menus(self, request, **kwargs):
        """
        Make the full set of menus for the app.

        This method provides a semi-sane menu set by default, but it
        is expected for most apps to override it.
        """
        menus = [
            self.make_custorders_menu(request),
            self.make_people_menu(request),
            self.make_products_menu(request),
            self.make_vendors_menu(request),
        ]

        integration_menus = self.make_integration_menus(request)
        if integration_menus:
            menus.extend(integration_menus)

        menus.extend([
            self.make_reports_menu(request, include_trainwreck=True),
            self.make_batches_menu(request),
            self.make_admin_menu(request, include_stores=True),
        ])

        return menus

    def make_integration_menus(self, request, **kwargs):
        """
        Make a set of menus for all registered system integrations.
        """
        menus = []
        for provider in self.tb.iter_providers():
            menu = provider.make_integration_menu(request)
            if menu:
                menus.append(menu)
        menus.sort(key=lambda menu: menu['title'].lower())
        return menus

    def make_custorders_menu(self, request, **kwargs):
        """
        Generate a typical Customer Orders menu
        """
        return {
            'title': "Orders",
            'type': 'menu',
            'items': [
                {
                    'title': "New Customer Order",
                    'route': 'custorders.create',
                    'perm': 'custorders.create',
                },
                {
                    'title': "All New Orders",
                    'route': 'new_custorders',
                    'perm': 'new_custorders.list',
                },
                {'type': 'sep'},
                {
                    'title': "All Customer Orders",
                    'route': 'custorders',
                    'perm': 'custorders.list',
                },
                {
                    'title': "All Order Items",
                    'route': 'custorders.items',
                    'perm': 'custorders.items.list',
                },
            ],
        }

    def make_people_menu(self, request, **kwargs):
        """
        Generate a typical People menu
        """
        return {
            'title': "People",
            'type': 'menu',
            'items': [
                {
                    'title': "Members",
                    'route': 'members',
                    'perm': 'members.list',
                },
                {
                    'title': "Member Equity Payments",
                    'route': 'member_equity_payments',
                    'perm': 'member_equity_payments.list',
                },
                {
                    'title': "Membership Types",
                    'route': 'membership_types',
                    'perm': 'membership_types.list',
                },
                {'type': 'sep'},
                {
                    'title': "Customers",
                    'route': 'customers',
                    'perm': 'customers.list',
                },
                {
                    'title': "Customer Shoppers",
                    'route': 'customer_shoppers',
                    'perm': 'customer_shoppers.list',
                },
                {
                    'title': "Customer Groups",
                    'route': 'customergroups',
                    'perm': 'customergroups.list',
                },
                {
                    'title': "Pending Customers",
                    'route': 'pending_customers',
                    'perm': 'pending_customers.list',
                },
                {'type': 'sep'},
                {
                    'title': "Employees",
                    'route': 'employees',
                    'perm': 'employees.list',
                },
                {'type': 'sep'},
                {
                    'title': "All People",
                    'route': 'people',
                    'perm': 'people.list',
                },
            ],
        }

    def make_products_menu(self, request, **kwargs):
        """
        Generate a typical Products menu
        """
        return {
            'title': "Products",
            'type': 'menu',
            'items': [
                {
                    'title': "Products",
                    'route': 'products',
                    'perm': 'products.list',
                },
                {
                    'title': "Departments",
                    'route': 'departments',
                    'perm': 'departments.list',
                },
                {
                    'title': "Subdepartments",
                    'route': 'subdepartments',
                    'perm': 'subdepartments.list',
                },
                {
                    'title': "Brands",
                    'route': 'brands',
                    'perm': 'brands.list',
                },
                {
                    'title': "Categories",
                    'route': 'categories',
                    'perm': 'categories.list',
                },
                {
                    'title': "Families",
                    'route': 'families',
                    'perm': 'families.list',
                },
                {
                    'title': "Report Codes",
                    'route': 'reportcodes',
                    'perm': 'reportcodes.list',
                },
                {
                    'title': "Units of Measure",
                    'route': 'uoms',
                    'perm': 'uoms.list',
                },
                {'type': 'sep'},
                {
                    'title': "Pending Products",
                    'route': 'pending_products',
                    'perm': 'pending_products.list',
                },
            ],
        }

    def make_vendors_menu(self, request, **kwargs):
        """
        Generate a typical Vendors menu
        """
        return {
            'title': "Vendors",
            'type': 'menu',
            'items': [
                {
                    'title': "Vendors",
                    'route': 'vendors',
                    'perm': 'vendors.list',
                },
                {'type': 'sep'},
                {
                    'title': "Ordering",
                    'route': 'ordering',
                    'perm': 'ordering.list',
                },
                {
                    'title': "Receiving",
                    'route': 'receiving',
                    'perm': 'receiving.list',
                },
                {
                    'title': "Invoice Costing",
                    'route': 'invoice_costing',
                    'perm': 'invoice_costing.list',
                },
                {'type': 'sep'},
                {
                    'title': "Purchases",
                    'route': 'purchases',
                    'perm': 'purchases.list',
                },
                {
                    'title': "Credits",
                    'route': 'purchases.credits',
                    'perm': 'purchases.credits.list',
                },
                {'type': 'sep'},
                {
                    'title': "Catalog Batches",
                    'route': 'vendorcatalogs',
                    'perm': 'vendorcatalogs.list',
                },
                {'type': 'sep'},
                {
                    'title': "Sample Files",
                    'route': 'vendorsamplefiles',
                    'perm': 'vendorsamplefiles.list',
                },
            ],
        }

    def make_batches_menu(self, request, **kwargs):
        """
        Generate a typical Batches menu
        """
        return {
            'title': "Batches",
            'type': 'menu',
            'items': [
                {
                    'title': "Handheld",
                    'route': 'batch.handheld',
                    'perm': 'batch.handheld.list',
                },
                {
                    'title': "Inventory",
                    'route': 'batch.inventory',
                    'perm': 'batch.inventory.list',
                },
                {
                    'title': "Import / Export",
                    'route': 'batch.importer',
                    'perm': 'batch.importer.list',
                },
                {
                    'title': "POS",
                    'route': 'batch.pos',
                    'perm': 'batch.pos.list',
                },
            ],
        }

    def make_reports_menu(self, request, **kwargs):
        """
        Generate a typical Reports menu
        """
        items = [
            {
                'title': "New Report",
                'route': 'report_output.create',
                'perm': 'report_output.create',
            },
            {
                'title': "Generated Reports",
                'route': 'report_output',
                'perm': 'report_output.list',
            },
            {
                'title': "Problem Reports",
                'route': 'problem_reports',
                'perm': 'problem_reports.list',
            },
        ]

        if kwargs.get('include_poser', False):
            items.extend([
                {'type': 'sep'},
                {
                    'title': "Poser Reports",
                    'route': 'poser_reports',
                    'perm': 'poser_reports.list',
                },
            ])

        if kwargs.get('include_worksheets', False):
            items.extend([
                {'type': 'sep'},
                {
                    'title': "Ordering Worksheet",
                    'route': 'reports.ordering',
                },
                {
                    'title': "Inventory Worksheet",
                    'route': 'reports.inventory',
                },
            ])

        if kwargs.get('include_trainwreck', False):
            items.extend([
                {'type': 'sep'},
                {
                    'title': "Trainwreck",
                    'route': 'trainwreck.transactions',
                    'perm': 'trainwreck.transactions.list',
                },
            ])

        return {
            'title': "Reports",
            'type': 'menu',
            'items': items,
        }

    def make_tempmon_menu(self, request, **kwargs):
        """
        Generate a typical TempMon menu
        """
        return {
            'title': "TempMon",
            'type': 'menu',
            'items': [
                {
                    'title': "Dashboard",
                    'route': 'tempmon.dashboard',
                    'perm': 'tempmon.appliances.dashboard',
                },
                {'type': 'sep'},
                {
                    'title': "Appliances",
                    'route': 'tempmon.appliances',
                    'perm': 'tempmon.appliances.list',
                },
                {
                    'title': "Clients",
                    'route': 'tempmon.clients',
                    'perm': 'tempmon.clients.list',
                },
                {
                    'title': "Probes",
                    'route': 'tempmon.probes',
                    'perm': 'tempmon.probes.list',
                },
                {
                    'title': "Readings",
                    'route': 'tempmon.readings',
                    'perm': 'tempmon.readings.list',
                },
            ],
        }

    def make_admin_menu(self, request, **kwargs):
        """
        Generate a typical Admin menu
        """
        items = []

        include_stores = kwargs.get('include_stores', True)
        include_tenders = kwargs.get('include_tenders', True)

        if include_stores or include_tenders:

            if include_stores:
                items.extend([
                    {
                        'title': "Stores",
                        'route': 'stores',
                        'perm': 'stores.list',
                    },
                ])

            if include_tenders:
                items.extend([
                    {
                        'title': "Tenders",
                        'route': 'tenders',
                        'perm': 'tenders.list',
                    },
                ])

            items.append({'type': 'sep'})

        items.extend([
            {
                'title': "Users",
                'route': 'users',
                'perm': 'users.list',
            },
            {
                'title': "Roles",
                'route': 'roles',
                'perm': 'roles.list',
            },
            {
                'title': "Raw Permissions",
                'route': 'permissions',
                'perm': 'permissions.list',
            },
            {'type': 'sep'},
            {
                'title': "Email Settings",
                'route': 'emailprofiles',
                'perm': 'emailprofiles.list',
            },
            {
                'title': "Email Attempts",
                'route': 'email_attempts',
                'perm': 'email_attempts.list',
            },
            {'type': 'sep'},
            {
                'title': "DataSync Status",
                'route': 'datasync.status',
                'perm': 'datasync.status',
            },
            {
                'title': "DataSync Changes",
                'route': 'datasyncchanges',
                'perm': 'datasync_changes.list',
            },
            {
                'title': "Importing / Exporting",
                'route': 'importing',
                'perm': 'importing.list',
            },
            {
                'title': "Luigi Tasks",
                'route': 'luigi',
                'perm': 'luigi.list',
            },
            {'type': 'sep'},
            {
                'title': "App Details",
                'route': 'appinfo',
                'perm': 'appinfo.list',
            },
        ])

        if kwargs.get('include_label_settings', False):
            items.extend([
                {
                    'title': "Label Settings",
                    'route': 'labelprofiles',
                    'perm': 'labelprofiles.list',
                },
            ])

        items.extend([
            {
                'title': "Raw Settings",
                'route': 'settings',
                'perm': 'settings.list',
            },
            {
                'title': "Upgrades",
                'route': 'upgrades',
                'perm': 'upgrades.list',
            },
        ])

        return {
            'title': "Admin",
            'type': 'menu',
            'items': items,
        }


def make_simple_menus(request):
    """
    Build the main menu list for the app.
    """
    app = request.rattail_config.get_app()
    tailbone_handler = app.get_tailbone_handler()
    menu_handler = tailbone_handler.get_menu_handler()

    raw_menus = menu_handler.make_raw_menus(request)

    # now we have "simple" (raw) menus definition, but must refine
    # that somewhat to produce our final menus
    mark_allowed(request, raw_menus)
    final_menus = []
    for topitem in raw_menus:

        if topitem['allowed']:

            if topitem.get('type') == 'link':
                final_menus.append(make_menu_entry(request, topitem))

            else: # assuming 'menu' type

                menu_items = []
                for item in topitem['items']:
                    if not item['allowed']:
                        continue

                    # nested submenu
                    if item.get('type') == 'menu':
                        submenu_items = []
                        for subitem in item['items']:
                            if subitem['allowed']:
                                submenu_items.append(make_menu_entry(request, subitem))
                        menu_items.append({
                            'type': 'submenu',
                            'title': item['title'],
                            'items': submenu_items,
                            'is_menu': True,
                            'is_sep': False,
                        })

                    elif item.get('type') == 'sep':
                        # we only want to add a sep, *if* we already have some
                        # menu items (i.e. there is something to separate)
                        # *and* the last menu item is not a sep (avoid doubles)
                        if menu_items and not menu_items[-1]['is_sep']:
                            menu_items.append(make_menu_entry(request, item))

                    else: # standard menu item
                        menu_items.append(make_menu_entry(request, item))

                # remove final separator if present
                if menu_items and menu_items[-1]['is_sep']:
                    menu_items.pop()

                # only add if we wound up with something
                assert menu_items
                if menu_items:
                    group = {
                        'type': 'menu',
                        'key': topitem.get('key'),
                        'title': topitem['title'],
                        'items': menu_items,
                        'is_menu': True,
                        'is_link':  False,
                    }

                    # topitem w/ no key likely means it did not come
                    # from config but rather explicit definition in
                    # code.  so we are free to "invent" a (safe) key
                    # for it, since that is only for editing config
                    if not group['key']:
                        group['key'] = make_menu_key(request.rattail_config,
                                                     topitem['title'])

                    final_menus.append(group)

    return final_menus


def make_menu_key(config, value):
    """
    Generate a normalized menu key for the given value.
    """
    return re.sub(r'\W', '', value.lower())


def make_menu_entry(request, item):
    """
    Convert a simple menu entry dict, into a proper menu-related object, for
    use in constructing final menu.
    """
    # separator
    if item.get('type') == 'sep':
        return {
            'type': 'sep',
            'is_menu': False,
            'is_sep': True,
        }

    # standard menu item
    entry = {
        'type': 'item',
        'title': item['title'],
        'perm': item.get('perm'),
        'target': item.get('target'),
        'is_link': True,
        'is_menu': False,
        'is_sep': False,
    }
    if item.get('route'):
        entry['route'] = item['route']
        try:
            entry['url'] = request.route_url(entry['route'])
        except KeyError:        # happens if no such route
            log.warning("invalid route name for menu entry: %s", entry)
            entry['url'] = entry['route']
        entry['key'] = entry['route']
    else:
        if item.get('url'):
            entry['url'] = item['url']
        entry['key'] = make_menu_key(request.rattail_config, entry['title'])
    return entry


def is_allowed(request, item):
    """
    Logic to determine if a given menu item is "allowed" for current user.
    """
    perm = item.get('perm')
    if perm:
        return request.has_perm(perm)
    return True


def mark_allowed(request, menus):
    """
    Traverse the menu set, and mark each item as "allowed" (or not) based on
    current user permissions.
    """
    for topitem in menus:

        if topitem.get('type', 'menu') == 'menu':
            topitem['allowed'] = False

            for item in topitem['items']:

                if item.get('type') == 'menu':
                    for subitem in item['items']:
                        subitem['allowed'] = is_allowed(request, subitem)

                    item['allowed'] = False
                    for subitem in item['items']:
                        if subitem['allowed'] and subitem.get('type') != 'sep':
                            item['allowed'] = True
                            break

                else:
                    item['allowed'] = is_allowed(request, item)

            for item in topitem['items']:
                if item['allowed'] and item.get('type') != 'sep':
                    topitem['allowed'] = True
                    break


def make_admin_menu(request, **kwargs):
    """
    Generate a typical Admin menu
    """
    warnings.warn("make_admin_menu() function is deprecated; please use "
                  "MenuHandler.make_admin_menu() instead",
                  DeprecationWarning, stacklevel=2)

    app = request.rattail_config.get_app()
    tailbone_handler = app.get_tailbone_handler()
    menu_handler = tailbone_handler.get_menu_handler()
    return menu_handler.make_admin_menu(request, **kwargs)
