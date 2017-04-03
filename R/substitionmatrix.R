library(Biostrings)
library(ape)

#' Distance pairwise between two sequences
#'
#' @param x: DNAString object.
#' @param y: DNAString object.
#' @param model: distance mesure ("raw", "N", "TS", "TV", "JC69", "K80" (the default),
#' "F81", "K81", "F84", "BH87", "T92", "TN93", "GG95", "logdet", "paralin", "indel", "indelblock")
#' @return The distance bettwen two sequences
#' @examples
#' dist_kmer(x, y, "K80")

dist_substitution<-function(x, y, model="K80",...){
  if (!is.null(x) && !is.null(y)){
    tmp = as.DNAbin(c(x,y))
    return(dist.dna(tmp,model,...))
  }else{
    print("x or y is null, verify your data")
  }
}
