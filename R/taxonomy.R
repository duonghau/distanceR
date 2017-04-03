library(RPostgreSQL)

filter_blast<-function(data, min_lenght, ident, evalue){

}

parse_blast<-function(filename,...){
  blast_info<-lict()
  blast_df <- read.table(filename, header=FALSE)
  apply(blast_df,1,function(x){blast_info[[as.character(x[1])]]<<-c(blast_info[[as.character(x[1])]], strsplit(x[2],split="\\|")[[1]][2]);NULL})
  return(blast_info)
}

get_taxonomy_info <- function(taxids, db="taxonomy", u="student", pw="123456", p="5432"){
  taxinfors = list()
  #read data from database
  pg = dbDriver("PostgreSQL")
  con = dbConnect(pg, user=u, password=pw,
                  host="localhost", port=p, dbname=db)
  query=paste("select tax_id, taxonomy_by_taxid(tax_id) from names where tax_id in (",paste(taxids, collapse = ', '),")",sep="")
  result=dbGetQuery(con,query)
  #fill list
  apply(result,1,function(x){taxinfors[[as.character(x[1])]]<<-strsplit(x[2],split=';')[[1]];NULL})
  return(taxinfors)
}

get_taxid_from_gi <- function(gis, db="taxonomy", u="student", pw="123456", p="5432"){
  gi_taxid<-list()
  pg = dbDriver("PostgreSQL")
  con = dbConnect(pg, user=u, password=pw,
                  host="localhost", port=p, dbname=db)
  query=paste("select gi,tax_id from gi_taxid where gi in (",paste(gis, collapse = ', '),")",sep="")
  result=dbGetQuery(con,query)
  apply(result,1,function(x){gi_taxid[[as.character(x[1])]]<<-as.character(x[[2]]);NULL})
  return(gi_taxid)
}

#x, y is gi
#taxonomies is list that contain all taxonomy information

dist_taxon <- function(taxon_x, taxon_y){
  length_x <- length(taxon_x)
  length_y  <- length(taxon_y)
  i<-1
  while(i<=min(length_x, length_y)){
    if (taxon_x[i] == taxon_y[i]){
      i<-i+1
    }else{
      break
    }
  }
  return ((length_x-i+1)+(length_y-i+1))
}

dist_taxons <- function(x, y,...){
  gi_taxids <- get_taxid_from_gi(c(x,y),...)
  taxon_infors <- get_taxonomy_info(unique(unlist(gi_taxid)),...)
  x_<-parse_blast(file_x)
  y_<-parse_blast(file_y)
}
