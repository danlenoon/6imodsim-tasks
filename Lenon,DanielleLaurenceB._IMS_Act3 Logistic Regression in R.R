#Lenon, Danielle Laurence B. | CS-301 | 8.26.2025

model <- glm(vs ~ wt + hp, data = mtcars, family = 'binomial')
summary(model)