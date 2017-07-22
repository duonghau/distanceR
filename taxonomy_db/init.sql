CREATE TABLE nodes(
   tax_id  INT NOT NULL,
   parent INT NOT NULL,
   rank VARCHAR(50),
   PRIMARY KEY(tax_id)   
);
CREATE INDEX nodes_index ON nodes (tax_id);

CREATE TABLE names(
   tax_id  INT NOT NULL,
   name TEXT NOT NULL,
   PRIMARY KEY(tax_id)
);
CREATE INDEX names_index ON names (tax_id);

CREATE TABLE gi_taxid(
   gi  INT NOT NULL,
   tax_id INT NOT NULL,
   PRIMARY KEY(gi)
);
CREATE INDEX gi_taxid_index ON gi_taxid (gi);

select names.tax_id as tax_id, names.name as name, nodes.parent as parent, nodes.rank as rank into taxonomies from names, nodes where names.tax_id = nodes.tax_id;

CREATE or REPLACE FUNCTION full_taxonomy(integer) RETURNS VARCHAR as $$
DECLARE
taxon varchar:='';
current_taxon varchar;
current_id int :=$1;
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
$$ LANGUAGE plpgsql;