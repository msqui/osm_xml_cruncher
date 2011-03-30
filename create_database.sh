#!/usr/bin/env bash

"/usr/local/pgsql/bin/createdb" --template=template0 --encoding=UTF8 --locale=en_US.UTF-8 openstreet
"/usr/local/pgsql/bin/createlang" plpgsql openstreet
psql -d openstreet -f "/usr/local/pgsql/share/contrib/postgis-1.5/postgis.sql"
psql -d openstreet -f "/usr/local/pgsql/share/contrib/postgis-1.5/spatial_ref_sys.sql"
psql -d openstreet -f "/usr/local/pgsql/share/contrib/btree_gist.sql"

echo '
CREATE TABLE "public"."places" (
    "id" int4 NOT NULL,
    "type_class" varchar NOT NULL,
    "type_name" varchar NOT NULL,
    "name" varchar NOT NULL,
    PRIMARY KEY ("id")
)
WITH (OIDS=FALSE);
' | psql -d openstreet

echo "
SELECT AddGeometryColumn('', 'places', 'coord', -1, 'POINT', 2);
ALTER TABLE \"public\".\"places\" ALTER COLUMN \"coord\" SET NOT NULL;
" | psql -d openstreet

echo "
CREATE INDEX \"places__type_class__type_name__coord\" ON \"public\".\"places\" USING gist(type_class, type_name, coord);
" | psql -d openstreet
