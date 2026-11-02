#Lenon, Danielle Laurence B. | CS-301 | 8.26.2025

library(tm)
library(wordcloud)
library(RColorBrewer)

text <- c("This is an example of a word cloud in R")
corpus <- Corpus(VectorSource(text))
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, removeWords, stopwords("english"))
dtm <- TermDocumentMatrix(corpus)
matrix <- as.matrix(dtm)
words <- sort(rowSums(matrix), decreasing=TRUE)
df <- data.frame(word = names(words), freq = words)
wordcloud(words = df$word, freq = df$freq, min.freq = 1,
          colors = brewer.pal(8, "Dark2"))