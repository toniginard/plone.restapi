# -*- coding: utf-8 -*-
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.converters import json_compatible
from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.interfaces import ICatalogBrain
from Products.ZCatalog.Lazy import Lazy
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.interface import Interface


BRAIN_METHODS = ['getPath', 'getURL']


@implementer(ISerializeToJson)
@adapter(ICatalogBrain, Interface)
class BrainSerializer(object):
    """Serializes a catalog brain to a Python data structure that can in turn
    be serialized to JSON.
    """

    def __init__(self, brain, request):
        self.brain = brain
        self.request = request

    def _get_metadata_to_include(self, metadata_fields):
        if metadata_fields and '_all' in metadata_fields:
            site = getSite()
            catalog = getToolByName(site, 'portal_catalog')
            metadata_attrs = catalog.schema() + BRAIN_METHODS
            return metadata_attrs

        return metadata_fields

    def __call__(self, metadata_fields=('_all',)):
        metadata_to_include = self._get_metadata_to_include(metadata_fields)

        result = {}
        for attr in metadata_to_include:
            value = getattr(self.brain, attr, None)

            # Handle values that are provided via methods on brains, like
            # getPath or getURL (see ICatalogBrain for details)
            if attr in BRAIN_METHODS:
                value = value()

            value = json_compatible(value)

            # TODO: Deal with metadata attributes that already contain
            # timestamps as isoformat strings, like 'Created'
            result[attr] = value

        return result


@implementer(ISerializeToJson)
@adapter(Lazy, Interface)
class LazyCatalogResultSerializer(object):
    """Serializes a ZCatalog resultset (one of the subclasses of `Lazy`) to
    a Python data structure that can in turn be serialized to JSON.
    """

    def __init__(self, lazy_resultset, request):
        self.lazy_resultset = lazy_resultset
        self.request = request

    def __call__(self, metadata_fields=()):
        results = {}
        results['items_count'] = self.lazy_resultset.actual_result_count
        results['items'] = []

        for brain in self.lazy_resultset:
            result = getMultiAdapter(
                (brain, self.request), ISerializeToJsonSummary)()

            if metadata_fields:
                metadata = getMultiAdapter(
                    (brain, self.request),
                    ISerializeToJson)(metadata_fields=metadata_fields)
                result.update(metadata)

            results['items'].append(result)
        return results