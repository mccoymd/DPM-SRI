args = commandArgs(trailingOnly=TRUE)
if (length(args) > 0){
  survival_min = as.numeric(args[1])
  survival_max = as.numeric(args[2]) 
}else{
  survival_min = 0
  survival_max = 1845  
}

outcomeTable = args[3]
outputTable = args[4]

outcomes = read.csv(outcomeTable,header=TRUE)
outcomes = outcomes[outcomes$strategy0 >= survival_min & outcomes$strategy0 <= survival_max,]
write.csv(outcomes,file=outputTable,row.names = FALSE)
