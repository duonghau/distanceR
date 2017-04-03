library(Biostrings)

#' K-mer distance between 2 sequences
#'
#' @param x: DNAString object.
#' @param y: DNAString object.
#' @param k: k-mer
#' @param type: distance mesure (euclid,manhattan,pearson,spearman)
#' @return The distance bettwen two sequences
#' @examples
#' dist_kmer(x, y, 4, "euclid")

dist_kmer<-function(x, y, k=4, type="euclid"){
  vec_x = oligonucleotideFrequency(x,k)
  vec_y = oligonucleotideFrequency(y,k)
  distance<-function(x,y,type){
    switch (type,
      euclid = as.numeric(dist(rbind(vec_x, vec_y), method = "euclidean")),
      manhattan = as.numeric(dist(rbind(vec_x, vec_y), method = "manhattan")),
      pearson = cor(vec_x, vec_y, method = "pearson"),
      spearman= cor(vec_x, vec_y, method = "spearman")
    )
  }
  return(distance(vec_x,vec_y,type))
}

#' K-mer distance between 2 sets of sequence
#'
#' @param x: DNAStringSet object.
#' @param y: DNAStringSet object.
#' @param k: k-mer
#' @param type: distance mesure (euclid,manhattan,pearson,spearman)
#' @return The distance between two set of sequences
#' @examples
#' dist_kmers(x, y, 4, "euclid")

dist_kmers<-function(x, y, k, method="euclid"){

}
