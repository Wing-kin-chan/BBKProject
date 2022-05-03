================================================= DATABASE DOCUMENTATION ==========================================================
 - Author: Wing-kin Chan

The database uses a single table with accession numbers as the primary key for referencing. The table columns are as follows:
    - Accession VARCHAR(12) PRIMARY KEY
    - Date DATE NOT NULL
    - Locus VARCHAR(40) NOT NULL
    - GeneID VARCHAR(8) NOT NULL
    - Product VARCHAR(255) NOT NULL
    - Description VARCHAR(255) NOT NULL
    - Source VARCHAR(60) NOT NULL
    - Sequence LONGBLOB NOT NULL
    - Frame INT(1) NOT NULL
    - Translation LONGBLOB NOT NULL
    - Coding_seq LONGBLOB
    - Coding_regions BLOB NOT NULL
    - Complement ENUM('Y', 'N') NOT NULL
    
To parse the GenBank file and store into a database, simply run createdb.py in Pandora's Python console.
