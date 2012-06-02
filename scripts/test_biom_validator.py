#!/usr/bin/env python

from unittest import TestCase, main
from biom_validator import valid_format_url, valid_rows,\
        valid_columns, valid_data, valid_datetime,\
        valid_sparse_data, valid_dense_data, \
        valid_shape, valid_matrix_type, valid_matrix_element_type,\
        valid_biom, valid_type, valid_generated_by, valid_format, \
        valid_metadata
import json

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2012, The BIOM-Format Project"
__credits__ = ["Daniel McDonald", "Jose Clemente", "Greg Caporaso", 
               "Jai Rideout", "Justin Kuczynski", "Andreas Wilke",
               "Tobias Paczian", "Rob Knight", "Folker Meyer", 
               "Sue Huse"]
__url__ = "http://biom-format.org"
__license__ = "GPL"
__version__ = "1.0.0c"
__maintainer__ = "Daniel McDonald"
__email__ = "daniel.mcdonald@colorado.edu"
__status__ = "Development"

class ParserTests(TestCase):
    def setUp(self):
        self.min_sparse_otu = json.loads(min_sparse_otu)
        self.rich_sparse_otu = json.loads(rich_sparse_otu)
        self.rich_dense_otu = json.loads(rich_dense_otu)
        self.min_dense_otu = json.loads(min_dense_otu)
        
    def test_valid_biom(self):
        """validates a table"""
        self.assertEqual(valid_biom(self.min_sparse_otu), None)
        self.assertEqual(valid_biom(self.rich_sparse_otu), None)

    def test_valid_format_url(self):
        """validates format url"""
        table = self.min_sparse_otu
        self.assertEqual(valid_format_url(table), None)
        table['format_url'] = 'foo'
        self.assertRaises(ValueError, valid_format_url, table)

    def test_valid_format(self):
        """Should match format string"""
        table = self.min_sparse_otu
        self.assertEqual(valid_format(table), None)
        table['format'] = 'foo'
        self.assertRaises(ValueError, valid_format, table)

    def test_valid_type(self):
        """Should be valid table type"""
        table = self.min_sparse_otu
        self.assertEqual(valid_type(table), None)
        table['type'] = 'otu table' # should not be case sensitive
        self.assertEqual(valid_type(table), None)
        table['type'] = 'Pathway table'
        self.assertEqual(valid_type(table), None)
        table['type'] = 'Function table'
        self.assertEqual(valid_type(table), None)
        table['type'] = 'Ortholog table'
        self.assertEqual(valid_type(table), None)
        table['type'] = 'Gene table'
        self.assertEqual(valid_type(table), None)
        table['type'] = 'Metabolite table'
        self.assertEqual(valid_type(table), None)
        table['type'] = 'OTU table'
        self.assertEqual(valid_type(table), None)
        table['type'] = 'Taxon table'
        self.assertEqual(valid_type(table), None)
        table['type'] = 'foo'
        self.assertRaises(ValueError, valid_type, table)

    def test_valid_generated_by(self):
        """Should have some string for generated by"""
        table = self.min_sparse_otu
        self.assertEqual(valid_generated_by(table), None)
        table['generated_by'] = None
        self.assertRaises(ValueError, valid_generated_by, table)

    def test_valid_nullable_id(self):
        """Should just work."""
        pass

    def test_valid_metadata(self):
        """Can be nullable or an object"""
        table = self.min_sparse_otu

        table['rows'][2]['metadata'] = None
        self.assertEqual(valid_metadata(table['rows'][2]), None)
        
        table['rows'][2]['metadata'] = {10:20}
        self.assertEqual(valid_metadata(table['rows'][2]), None)
        
        table['rows'][2]['metadata'] = ""
        self.assertRaises(ValueError, valid_metadata, table['rows'][2])

        table['rows'][2]['metadata'] = "asdasda"
        self.assertRaises(ValueError, valid_metadata, table['rows'][2])

        table['rows'][2]['metadata'] = [{'a':'b'},{'c':'d'}]
        self.assertRaises(ValueError, valid_metadata, table['rows'][2])

    def test_valid_matrix_type(self):
        """Make sure we have a valid matrix type"""
        self.assertEqual(valid_matrix_type(self.min_dense_otu), None)
        self.assertEqual(valid_matrix_type(self.min_sparse_otu), None)
        table = self.min_dense_otu
        table['matrix_type'] = 'spARSe'
        self.assertRaises(ValueError, valid_matrix_type, table)
        table['matrix_type'] = 'sparse_asdasd'
        self.assertRaises(ValueError, valid_matrix_type, table)

    def test_valid_matrix_element_type(self):
        """Make sure we have a valid matrix type"""
        min_sparse_otu = self.min_sparse_otu
        self.assertEqual(valid_matrix_element_type(min_sparse_otu), None)
        min_sparse_otu['matrix_element_type'] = u'int'
        self.assertEqual(valid_matrix_element_type(min_sparse_otu), None)
        min_sparse_otu['matrix_element_type'] = 'float'
        self.assertEqual(valid_matrix_element_type(min_sparse_otu), None)
        min_sparse_otu['matrix_element_type'] = u'float'
        self.assertEqual(valid_matrix_element_type(min_sparse_otu), None)
        min_sparse_otu['matrix_element_type'] = 'str'
        self.assertEqual(valid_matrix_element_type(min_sparse_otu), None)
        min_sparse_otu['matrix_element_type'] = u'str'
        self.assertEqual(valid_matrix_element_type(min_sparse_otu), None)

        min_sparse_otu['matrix_element_type'] = 'obj'
        self.assertRaises(ValueError, valid_matrix_element_type, min_sparse_otu)
        min_sparse_otu['matrix_element_type'] = u'asd'
        self.assertRaises(ValueError, valid_matrix_element_type, min_sparse_otu)

    def test_valid_datetime(self):
        """Make sure we have a datetime stamp"""
        min_sparse_otu = self.min_sparse_otu
        self.assertEqual(valid_datetime(min_sparse_otu), None)
        min_sparse_otu['date'] = "1999-11-11T10:11:12"
        self.assertEqual(valid_datetime(min_sparse_otu), None)
        min_sparse_otu['date'] = "10-11-1999 10:11:12"
        self.assertEqual(valid_datetime(min_sparse_otu), None)
        min_sparse_otu['date'] = "10-11-1asdfasd:12"
        self.assertRaises(ValueError, valid_datetime, min_sparse_otu)

    def test_valid_sparse_data(self):
        """Takes a sparse matrix field and validates"""
        table = self.min_sparse_otu
        self.assertEqual(valid_sparse_data(table), None)

        # incorrect type
        table['matrix_element_type'] = 'float'
        self.assertRaises(ValueError, valid_sparse_data, table)
        
        # not balanced
        table['matrix_element_type'] = 'int'
        table['data'][5] = [0,10]
        self.assertRaises(ValueError, valid_sparse_data, table)
        
        # odd type for index
        table['data'][5] = [1.2,5,10]
        self.assertRaises(ValueError, valid_sparse_data, table)

    def test_valid_dense_data(self):
        """Takes a dense matrix field and validates"""
        table = self.min_dense_otu
        self.assertEqual(valid_dense_data(table), None)

        # incorrect type
        table['matrix_element_type'] = 'float'
        self.assertRaises(ValueError, valid_dense_data, table)

        # not balanced
        table['matrix_element_type'] = 'int'
        table['data'][1] = [0,10]
        self.assertRaises(ValueError, valid_dense_data, table)

        # bad type in a field
        table['data'][1] = [5, 1, 0, 2.3, 3, 1]
        self.assertRaises(ValueError, valid_dense_data, table)

    def test_valid_shape(self):
        """validates shape information"""
        self.assertEqual(valid_shape(self.min_sparse_otu), None)
        self.assertEqual(valid_shape(self.rich_sparse_otu), None)
    
        bad_shape = self.min_sparse_otu.copy()
        bad_shape['shape'] = ['asd',10]
        self.assertRaises(ValueError, valid_shape, bad_shape)
        
    def test_valid_rows(self):
        """validates rows: field"""
        table = self.rich_dense_otu
        self.assertEqual(valid_rows(table), None)

        table['rows'][0]['id'] = ""
        self.assertRaises(ValueError, valid_rows, table)

        table['rows'][0]['id'] = None
        self.assertRaises(ValueError, valid_rows, table)
        
        del table['rows'][0]['id']
        self.assertRaises(AttributeError, valid_rows, table)

        table['rows'][0]['id'] = 'asd'
        table['rows'][0]['metadata'] = None
        self.assertEqual(valid_rows(table), None)

        # since this is an OTU table, metadata is a required key
        del table['rows'][0]['metadata']
        self.assertRaises(AttributeError, valid_rows, table)

    def test_valid_columns(self):
        """validates table:columns: fields"""
        table = self.rich_dense_otu
        self.assertEqual(valid_columns(table), None)

        table['columns'][0]['id'] = ""
        self.assertRaises(ValueError, valid_columns, table)

        table['columns'][0]['id'] = None
        self.assertRaises(ValueError, valid_columns, table)
        
        del table['columns'][0]['id']
        self.assertRaises(AttributeError, valid_columns, table)

        table['columns'][0]['id'] = 'asd'
        table['columns'][0]['metadata'] = None
        self.assertEqual(valid_columns(table), None)

        # since this is an OTU table, metadata is a required key
        del table['columns'][0]['metadata']
        self.assertRaises(AttributeError, valid_columns, table)

    def test_valid_data(self):
        """validates data: fields"""
        # the burden of validating data is passed on to valid_sparse_data
        # and valid_dense_data
        table = self.rich_sparse_otu
        self.assertEqual(valid_data(table), None)
        
        table['matrix_type'] = 'foo'
        self.assertRaises(AttributeError, valid_data, table)

rich_sparse_otu = """{
     "id":null,
     "format": "Biological Observation Matrix v0.9",
     "format_url": "http://www.qiime.org/svn_documentation/documentation/biom_format.html",
     "type": "OTU table",
     "generated_by": "QIIME revision XYZ",
     "date": "2011-12-19T19:00:00",
     "rows":[
        {"id":"GG_OTU_1", "metadata":{"taxonomy":["k__Bacteria", "p__Proteobacteria", "c__Gammaproteobacteria", "o__Enterobacteriales", "f__Enterobacteriaceae", "g__Escherichia", "s__"]}},
        {"id":"GG_OTU_2", "metadata":{"taxonomy":["k__Bacteria", "p__Cyanobacteria", "c__Nostocophycideae", "o__Nostocales", "f__Nostocaceae", "g__Dolichospermum", "s__"]}},
        {"id":"GG_OTU_3", "metadata":{"taxonomy":["k__Archaea", "p__Euryarchaeota", "c__Methanomicrobia", "o__Methanosarcinales", "f__Methanosarcinaceae", "g__Methanosarcina", "s__"]}},
        {"id":"GG_OTU_4", "metadata":{"taxonomy":["k__Bacteria", "p__Firmicutes", "c__Clostridia", "o__Halanaerobiales", "f__Halanaerobiaceae", "g__Halanaerobium", "s__Halanaerobiumsaccharolyticum"]}},
        {"id":"GG_OTU_5", "metadata":{"taxonomy":["k__Bacteria", "p__Proteobacteria", "c__Gammaproteobacteria", "o__Enterobacteriales", "f__Enterobacteriaceae", "g__Escherichia", "s__"]}}
        ],
     "columns":[
        {"id":"Sample1", "metadata":{
                                 "BarcodeSequence":"CGCTTATCGAGA",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"gut",
                                 "Description":"human gut"}},
        {"id":"Sample2", "metadata":{
                                 "BarcodeSequence":"CATACCAGTAGC",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"gut",
                                 "Description":"human gut"}},
        {"id":"Sample3", "metadata":{
                                 "BarcodeSequence":"CTCTCTACCTGT",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"gut",
                                 "Description":"human gut"}},
        {"id":"Sample4", "metadata":{
                                 "BarcodeSequence":"CTCTCGGCCTGT",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"skin",
                                 "Description":"human skin"}},
        {"id":"Sample5", "metadata":{
                                 "BarcodeSequence":"CTCTCTACCAAT",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"skin",
                                 "Description":"human skin"}},
        {"id":"Sample6", "metadata":{
                                 "BarcodeSequence":"CTAACTACCAAT",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"skin",
                                 "Description":"human skin"}}
        ],
     "matrix_type": "sparse",
     "matrix_element_type": "int",
     "shape": [5, 6], 
     "data":[[0,2,1],
             [1,0,5],
             [1,1,1],
             [1,3,2],
             [1,4,3],
             [1,5,1],
             [2,2,1],
             [2,3,4],
             [2,5,2],
             [3,0,2],
             [3,1,1],
             [3,2,1],
             [3,5,1],
             [4,1,1],
             [4,2,1]
            ]
    }"""

min_sparse_otu = """{
        "id":null,
        "format": "Biological Observation Matrix v0.9",
        "format_url": "http://www.qiime.org/svn_documentation/documentation/biom_format.html",
        "type": "OTU table",
        "generated_by": "QIIME revision XYZ",
        "date": "2011-12-19T19:00:00",
        "rows":[
                {"id":"GG_OTU_1", "metadata":null},
                {"id":"GG_OTU_2", "metadata":null},
                {"id":"GG_OTU_3", "metadata":null},
                {"id":"GG_OTU_4", "metadata":null},
                {"id":"GG_OTU_5", "metadata":null}
            ],  
        "columns": [
                {"id":"Sample1", "metadata":null},
                {"id":"Sample2", "metadata":null},
                {"id":"Sample3", "metadata":null},
                {"id":"Sample4", "metadata":null},
                {"id":"Sample5", "metadata":null},
                {"id":"Sample6", "metadata":null}
            ],
        "matrix_type": "sparse",
        "matrix_element_type": "int",
        "shape": [5, 6], 
        "data":[[0,2,1],
                [1,0,5],
                [1,1,1],
                [1,3,2],
                [1,4,3],
                [1,5,1],
                [2,2,1],
                [2,3,4],
                [2,5,2],
                [3,0,2],
                [3,1,1],
                [3,2,1],
                [3,5,1],
                [4,1,1],
                [4,2,1]
               ]
    }"""

rich_dense_otu = """{
     "id":null,
     "format": "Biological Observation Matrix v0.9",
     "format_url": "http://www.qiime.org/svn_documentation/documentation/biom_format.html",
     "type": "OTU table",
     "generated_by": "QIIME revision XYZ",
     "date": "2011-12-19T19:00:00",  
     "rows":[
        {"id":"GG_OTU_1", "metadata":{"taxonomy":["k__Bacteria", "p__Proteobacteria", "c__Gammaproteobacteria", "o__Enterobacteriales", "f__Enterobacteriaceae", "g__Escherichia", "s__"]}},
        {"id":"GG_OTU_2", "metadata":{"taxonomy":["k__Bacteria", "p__Cyanobacteria", "c__Nostocophycideae", "o__Nostocales", "f__Nostocaceae", "g__Dolichospermum", "s__"]}},
        {"id":"GG_OTU_3", "metadata":{"taxonomy":["k__Archaea", "p__Euryarchaeota", "c__Methanomicrobia", "o__Methanosarcinales", "f__Methanosarcinaceae", "g__Methanosarcina", "s__"]}},
        {"id":"GG_OTU_4", "metadata":{"taxonomy":["k__Bacteria", "p__Firmicutes", "c__Clostridia", "o__Halanaerobiales", "f__Halanaerobiaceae", "g__Halanaerobium", "s__Halanaerobiumsaccharolyticum"]}},
        {"id":"GG_OTU_5", "metadata":{"taxonomy":["k__Bacteria", "p__Proteobacteria", "c__Gammaproteobacteria", "o__Enterobacteriales", "f__Enterobacteriaceae", "g__Escherichia", "s__"]}}
        ],  
     "columns":[
        {"id":"Sample1", "metadata":{
                                 "BarcodeSequence":"CGCTTATCGAGA",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"gut",
                                 "Description":"human gut"}},
        {"id":"Sample2", "metadata":{
                                 "BarcodeSequence":"CATACCAGTAGC",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"gut",
                                 "Description":"human gut"}},
        {"id":"Sample3", "metadata":{
                                 "BarcodeSequence":"CTCTCTACCTGT",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"gut",
                                 "Description":"human gut"}},
        {"id":"Sample4", "metadata":{
                                 "BarcodeSequence":"CTCTCGGCCTGT",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"skin",
                                 "Description":"human skin"}},
        {"id":"Sample5", "metadata":{
                                 "BarcodeSequence":"CTCTCTACCAAT",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"skin",
                                 "Description":"human skin"}},
        {"id":"Sample6", "metadata":{
                                 "BarcodeSequence":"CTAACTACCAAT",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"skin",
                                 "Description":"human skin"}}
                ],
     "matrix_type": "dense",
     "matrix_element_type": "int",
     "shape": [5,6],
     "data":  [[0,0,1,0,0,0], 
               [5,1,0,2,3,1],
               [0,0,1,4,2,0],
               [2,1,1,0,0,1],
               [0,1,1,0,0,0]]
    }"""

min_dense_otu = """ {
        "id":null,
        "format": "Biological Observation Matrix v0.9",
        "format_url": "http://www.qiime.org/svn_documentation/documentation/biom_format.html",
        "type": "OTU table",
        "generated_by": "QIIME revision XYZ",
        "date": "2011-12-19T19:00:00",
        "rows":[
                {"id":"GG_OTU_1", "metadata":null},
                {"id":"GG_OTU_2", "metadata":null},
                {"id":"GG_OTU_3", "metadata":null},
                {"id":"GG_OTU_4", "metadata":null},
                {"id":"GG_OTU_5", "metadata":null}
            ],  
        "columns": [
                {"id":"Sample1", "metadata":null},
                {"id":"Sample2", "metadata":null},
                {"id":"Sample3", "metadata":null},
                {"id":"Sample4", "metadata":null},
                {"id":"Sample5", "metadata":null},
                {"id":"Sample6", "metadata":null}
            ],  
        "matrix_type": "dense",
        "matrix_element_type": "int",
        "shape": [5,6],
        "data":  [[0,0,1,0,0,0], 
                  [5,1,0,2,3,1],
                  [0,0,1,4,2,0],
                  [2,1,1,0,0,1],
                  [0,1,1,0,0,0]]
    }"""

if __name__ == '__main__':
    main()

