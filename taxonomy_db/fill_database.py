# -*- coding: utf-8 -*-
import psycopg2
import sys
import argparse
import os

def init_connection(database, username, pw, port):
    try:
        con = psycopg2.connect(database=database, user=username, password=pw, port=port)
        return con
    except Exception as e:
        raise e
        return None

def init_tables(con):
	cur=con.cursor()
	#create nodes table
	query = "CREATE TABLE nodes(tax_id  INT NOT NULL, parent INT NOT NULL,"\
	"rank VARCHAR(50), PRIMARY KEY(tax_id))"
	cur.execute(query)
	#create names table
	query = "CREATE TABLE names(tax_id  INT NOT NULL, name TEXT NOT NULL,"\
	" PRIMARY KEY(tax_id))"
	cur.execute(query)
	#create gi_taxid table
	query = "CREATE TABLE gi_taxid(gi  INT NOT NULL, tax_id INT NOT NULL,"\
	"PRIMARY KEY(gi))"
	cur.execute(query)
    #create full_taxonomy for store information from entrez
    query="CREATE TABLE full_taxonomy(gi  INT NOT NULL,taxon TEXT,PRIMARY KEY(gi))"
    cur.execute(query)
	#create index
	query = "CREATE INDEX nodes_index ON nodes (tax_id)"
	cur.execute(query)
	query = "CREATE INDEX names_index ON names (tax_id)"
	cur.execute(query)
	query = "CREATE INDEX gi_taxid_index ON gi_taxid (gi)"
	cur.execute(query)
    query = "CREATE INDEX full_taxon_index ON full_taxonomy (gi)"
    cur.execute(query)
	con.commit()

def init_sql_fun(con):
	# get taxonomy by taxid
	query= """
		CREATE or REPLACE FUNCTION taxonomy_by_taxid(taxid integer) RETURNS VARCHAR as $$
		DECLARE
		taxon varchar:='';
		current_taxon varchar;
		current_id int :=taxid;
		parent_id int;
		done boolean:=FALSE;
		BEGIN
			WHILE NOT done LOOP
				select name, parent INTO current_taxon, parent_id  from taxonomies where tax_id=current_id;
				-- Check if root
				IF taxon='' THEN
					taxon:= current_taxon;
				ELSE
					taxon:= concat(current_taxon,';',taxon);
				END IF;
				IF parent_id = current_id THEN
					done:=TRUE;
				ELSE
					current_id:= parent_id;
				END IF;
			END LOOP;
			RETURN taxon;
		END;
		$$ LANGUAGE plpgsql
	"""
	try:
		con.cursor().execute(query)
		con.commit()
	except Exception as e:
		raise e
	# get taxonomy by gi
	query= """
		CREATE or REPLACE FUNCTION taxonomy_by_gi(gid integer) RETURNS VARCHAR as $$
		DECLARE
		taxon varchar:='';
		current_taxon varchar;
		current_id int;
		parent_id int;
		done boolean:=FALSE;
		BEGIN
			current_id:=(select tax_id from gi_taxid where gi=gid);
			WHILE NOT done LOOP
				select name, parent INTO current_taxon, parent_id  from taxonomies where tax_id=current_id;
				-- Check if root
				IF taxon='' THEN
					taxon:= current_taxon;
				ELSE
					taxon:= concat(current_taxon,';',taxon);
				END IF;
				IF parent_id = current_id THEN
					done:=TRUE;
				ELSE
					current_id:= parent_id;
				END IF;
			END LOOP;
			RETURN taxon;
		END;
		$$ LANGUAGE plpgsql
	"""
	try:
		con.cursor().execute(query)
		con.commit()
	except Exception as e:
		raise e

def insert_nodes(cur, tax_id, parent, rank):
    query="INSERT INTO nodes(tax_id, parent, rank) VALUES({0},{1},'{2}')".format(
    	tax_id, parent, rank)
    cur.execute(query)

def insert_names(cur, tax_id, name):
    query="INSERT INTO names(tax_id, name) VALUES({0},'{1}')".format(tax_id,
    	name.replace("'",""))
    cur.execute(query)

def insert_gi_taxid(cur, gi, tax_id):
    query="INSERT INTO gi_taxid(gi, tax_id) VALUES({0},{1})".format(gi, tax_id)
    cur.execute(query)

def fill_nodes(con, file_path):
    cur=con.cursor()
    i=0
    with open(file_path,"r") as file_handle:
        for line in file_handle:
            record= line.split("\t|\t")
            tax_id= record[0]
            parent= record[1]
            rank= record[2]
            try:
                insert_nodes(cur, tax_id, parent, rank)
            except Exception as e:
                con.commit()
                print("Error:{0}".format(e))
            i+=1
            if i%1000 == 0:
                con.commit()
    con.commit()
    if i>0:
        print("{0} row(s) affected".format(i))

def fill_names(con, file_path):
    cur=con.cursor()
    i=0
    with open(file_path,"r") as file_handle:
        for line in file_handle:
            record= line.split("\t|\t")
            tax_id= record[0]
            name= record[1]
            try:
                insert_names(cur, tax_id, name)
            except Exeption as e:
                con.commit()
                print("Error: {0}".format(e))
            i+=1
            if i%1000 == 0:
                con.commit()
    con.commit()
    if i>0:
        print("{0} row(s) affected".format(i))

def fill_gi_taxid(con, file_path):
    cur=con.cursor()
    i=0
    with open(file_path,"r") as file_handle:
        for line in file_handle:
            record= line.split("\t")
            gi= record[0]
            tax_id = record[1]
            try:
                insert_gi_taxid(cur, gi, tax_id)
            except Exeption as e:
                con.commit()
                print("Error: {0}".format(e))
            i+=1
            if i%1000 == 0:
                con.commit()
    con.commit()
    if i>0:
        print("{0} row(s) affected".format(i))


if __name__=="__main__":
    FILE_NAMES="names.dmp"
    FILE_NODES="nodes.dmp"
    FILE_GI_TAXID="gi_taxid_nucl.dmp"
    parser = argparse.ArgumentParser()
    parser.add_argument('-db', action="store", dest="db",help='database name')
    parser.add_argument('-u', action="store", dest="dbuser",help='user name')
    parser.add_argument('-p', action="store", dest="dbpass",help='password')
    parser.add_argument('-port', action="store", dest="port", default="5432", help='port posgres')
    parser.add_argument('-d', action="store", dest="data_dir",help='data directory')
    args = parser.parse_args()
    try:
        con = init_connection(args.db, args.dbuser, args.dbpass, args.port)
        if con:
        	#init table
        	# print("Init all tables")
        	# init_tables(con)
        	# print("Init function sql")
        	# init_sql_fun(con)
            # print("Fill names table")
            # fill_names(con, os.path.join(args.data_dir, FILE_NAMES))
            # print("Fill nodes table")
            # fill_nodes(con, os.path.join(args.data_dir, FILE_NODES))
            print("Fill gi_taxid table")
            fill_gi_taxid(con, os.path.join(args.data_dir, FILE_GI_TAXID))
            print("Done")
        else:
            print("Couldn't connect to database")
    except Exception as e:
        print("Error: {0}".format(e))
    finally:
        if con:
            con.close()
# da tao ra mot tables "names" de luu taxid va full_name. Chi can lay thong tin tu day, 
# khong can truy nguoc lai cac tables "nodes","taxonomies" nua, chua update trong code