args = commandArgs(trailingOnly=TRUE)
if (length(args) > 0){
  survival_min = as.numeric(args[1])
  survival_max = as.numeric(args[2]) 
}else{
  survival_min = 0
  survival_max = 1845  
}

outcomes = read.csv("./app/data/database/PNAS2012_allPatientSurvival_strategy0.csv",header=TRUE)
outcomes = outcomes[outcomes$Surv_0 >= survival_min & outcomes$Surv_0 <= survival_max,]
write.csv(outcomes,file='./app/data/appData/outcomes.csv',row.names = FALSE)
