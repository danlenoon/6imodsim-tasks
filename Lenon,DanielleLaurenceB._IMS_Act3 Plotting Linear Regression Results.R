#Lenon, Danielle Laurence B. | CS-301 | 8.26.2025

library(ggplot2)
ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point() +
  geom_smooth(method = 'lm')