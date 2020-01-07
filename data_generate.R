time1 <- rnorm(500, mean = 5, sd = 0.5)
time2 <- rnorm(500, mean = 6, sd = 1)
vorschub <- rnorm(500,mean =10, sd =1)
ones<-replicate(500,1)
g1 <- matrix(nrow = 1000, ncol = 5)

g1[1:500,1] <- ones
g1[1:500,2] <- time1
g1[1:500,3] <- time2
g1[1:500,4] <- vorschub
g1[1:500,5] <- ones



time1_2 <- rnorm(500, mean = 2, sd = 1)
time2_2 <- rnorm(500, mean = 2, sd = 1)
vorschub_2 <- rnorm(500,mean =5, sd =1)
ones<-replicate(500,1)
zeros <- replicate(500,0)
g1_f <- matrix(nrow =1000, ncol = 5)
g<- matrix(nrow=1000,ncol=5)
g1[501:1000,] <- zeros
g1_f[1:500,]<- zeros
g1_f [501:1000,1] <- ones
g1_f [501:1000,2] <- time1_2
g1_f [501:1000,3] <- time2_2
g1_f [501:1000,4] <- vorschub_2
g1_f [501:1000,5] <- zeros
g <- g1 + g1_f
View(g)


write.csv(g,file="g1_data.csv")