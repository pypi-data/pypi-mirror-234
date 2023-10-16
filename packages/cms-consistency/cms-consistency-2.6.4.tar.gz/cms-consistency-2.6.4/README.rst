CMS Rucio Consistency Tools
===========================

Tools description
-----------------

XRootD Scanner
~~~~~~~~~~~~~~
The XRootD Scanner is a tool designed to produce the list of files physically found in the RSE. 
The output of the Scanner is a partitioned list of LFNs for the files found under the set of site "root" directories, recursively.
The Scanner configuration includes:
    
* list of ``root`` directories for the site (typically the same for all sites)
* specification of the conversion from physical path to LFN
* for each ``root``, list of subdirectories to ignore, i.e. not to scan and not to include their contents in the output LFN list

Database Replica Dump
~~~~~~~~~~~~~~~~~~~~~
Database Replica Dump is a tool to dump the list of replica LFNs, which are supposed to be present in the RSE according to the
Rucio database. The tool is configured to limit results to given top directory in LFN space and optionally to remove
some subdirectories from the output.

Configuration File
~~~~~~~~~~~~~~~~~~

Currently the toolkit reads configuration in YAML format. Here is the configuration file sample:

.. code-block::

    database:		# optional. rucio.cfg can be used instead 
            host:           cmsr1-s.cern.ch
            port:           10121
            service:        cmsr.cern.ch
            schema:         CMS_RUCIO_INT
            user:           cms_rucio_int_r
            password:       "password"

    rses:
      "*": # default
        partitions:     5
        scanner:
          include_sizes: yes
          recursion:      1
          nworkers:        8
          timeout:        300
          server_root: /store/
          remove_prefix: /
          add_prefix: /store/
          roots:
          - path: express
            ignore:
                - path/relative/to/root
          - path: mc
          - path: data
          - path: generator
          - path: results
          - path: hidata
          - path: himc
          - path: relval
        dbdump:
          path_root:   /
          ignore:
              - path/to/ignore_a
              - path/to/ignore_b
      T0_CH_CERN_Disk:
        scanner:
          include_sizes: no
          server: eoscms.cern.ch
          server_root: /eos/cms/tier0/store/
      T1_US_FNAL_Disk:
        scanner:
          server: cmsdcadisk.fnal.gov
          server_root: /dcache/uscmsdisk/store/
          roots:
          - path: express
            ignore:
                - path/relative/to/root
          - path: mc
          - path: data

The "database" section configures the database connection. This section is used only by the ``db_dump.py`` tool.
The tool can also read the database connection configuration from ``rucio.cfg`` file, so the "database" section in the YAML
configuration file is optional.

The "rses" section of the file is a dictionary indexed by the RSE name. It contains defaults section (RSE name "*") and 
RSE-specifc sections, one per RSE. Generally, the tools, when they are looking for a configuration parameter value, look it up
by checking the RSE-specific portion first and then, if the option is not present there, looking into the defaults section.
Therefore, the defaults and RSE-specific sections follow the same structure, but typically RSE-specific sections are much shorter
and most of the configuration paraneters are specified in the defaults section.

Here is the structure of the configuration file for each RSE, including the defaults:

* partitions:  integer, default: 10 - number of partitions for file lists. Must be the same for scanner and DB dump.
* scanner:

  * include_sizes: yes/no, default: yes
  * recursion: integer, default: 3 - the directory depth relative to the scanning root, where to start attempting recursive scanning
  * nworkers: integer, default: 10 - number of parallel scanners to run for the RSE
  * timeout: integer, default: 60 - timeout in seconds to receive scanning results for a single directory
  * server_root: string - top path for the RSE
  * remove_prefix: string - prefix to remove from physical path
  * add_prefix: string - add prefix to physical path after removing ``remove_prefix``. ``remove_prefix`` and ``add_prefix`` are
    used to convert physical path to LFN.
  * roots: list - list of dictionaries, describing scanning roots. For each site the scanner recursively scans "root" directories
    one by one. For each ``root``, the following parameters can be configured

    * path: string, required - top of the area to scan, relative to the ``server_root``
    * ignore: list of strings - list of paths relative to the ``root`` not to scan and to exclude from scan results
    
* dbdump:   - database replicas dump configuration

  * path_root: string - top directory in LFN space to list. All LFNs found outside of ``path_root`` will be removed from the
    database dump
  * ignore: list of strings - list of paths, relative to ``path_root``, to remove from the output.

Moving configuration into Rucio
-------------------------------

Consistency Enformenet Procedures (CEP) will get their configuration from 2 sources in live Rucio instance:

-  Rucio Configuration - part of Rucio database, which mimics popular .ini configuratiin file format.
   This portion will be used to store common, RSE-independent configuration and RSE configuration defaults.

- RSE attributes will be used to store RSE-specific parameters such as xrootd server address and server root
  path, list of roots to scan.

Configuration Conversion
~~~~~~~~~~~~~~~~~~~~~~~~

1. Have Rucio client configured and log in as Rucio root account

2. Pull the code repository

.. code-block:: bash

  $ git pull https://github.com/ivmfnal/cms_consistency.git cms-consistency-new
  $ cd cms-consistency-new
  $ git checkout config_in_rucio
  $ cd rucio-config

   
3. Import existing configuration into Rucio

.. code-block:: bash
        
    $ python import_cc_config.py config.yaml


This will create ``consistency_enforcement`` section in the Rucio configuration and 2 subsections: ``consistency_enforcement.scanner`` and 
``consistency_enforcement.dbdump``. If these sections existed before, all their contents will be removed and replaced
with new values.
    
        
4. View the results

.. code-block:: bash
        
    $ rucio-admin config get
    $ rucio-admin rse info <RSE name>

        
Running CC tools with old and new configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash
    
    $ python xrootd_scanner.py -c config.yaml ...          # use the config file
    $ python xrootd_scanner.py ...                         # use the configuration stored in Rucio
    
    $ python db_dump.py -c config.yaml ...                 # use the config file
    $ python db_dump.py ...                                # use the configuration stored in Rucio


Configuration structure
~~~~~~~~~~~~~~~~~~~~~~~

RSE defaults
............

RSE defaults are stored in the Rucio database, which mimics the .ini file structure, implemented by the standard Python library class
ConfigParser. The configiration is organized into named sections and each section is a set of named attributes with their values.
Rucio supports only scalar sctings as configuration parameter values. Integer values are represented as decimals and interpreted
by the CC tools.

RSE defaults are organized into 3 sections:

Section consistency_enforcement
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

This section has only one parameter ``npartitions`` - the number of partitions to split file lists into. This parameter is used
by both DB dump tool and the xrootd scanner.
    
Section consistency_enforcement.scanner
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

This section has parameters used only by the xrootd scanner:

recursion - integer
    Directory depth level, relative to the root, at which to start attempting recursive scanning
    
nworkers - integer
    The number of parallel scanners to run
    
timeout - integer
    Time-out for scanning an individual directory. If the directory is scanned recursively and the scanning times-out, the
    scanner will attempt to scan it non-recursively and then scan recursively all its subdirectories
    
server_root, string
    Path to the very top of the server namespace. Scan roots are specified relative to the ``server_root``
    
remove_prefix, add_prexix - strings
    These two parameters specify the path-to-LFN conversion procedure applied to each file path found by the scanner
    
    1. Remove the ``remove_prefix`` from physical path
    2. Add the ``add_prefix``
        
    Defaults are "/"
    
roots - string
    JSON representation of the list of root configuration dictionaries. Each dictionary contains the following elements
    
    * path - required, path of the ``root``, relative to the ``server_root``
    * ignore - optional, list of subdirectory paths, relative to the ``root``, to remove from the scanner output
        
Section consistency_enforcement.dbdump
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

This section has parameters used by the DB dump tool:

path_root - string
    The top of the LFN namespace tree to dump. Default is "/"
    
ignore - string
    Space-separated list of paths to ignore, relative to the ``path_root``


    



