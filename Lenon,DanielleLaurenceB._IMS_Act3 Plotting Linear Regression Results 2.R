#Lenon, Danielle Laurence B. | CS-301 | 8.26.2025

library(ggplot2)
mtcars$prob <- predict(model, type = 'response')
ggplot(mtcars, aes(x = wt, y = prob)) +
  geom_point() +
  geom_smooth()