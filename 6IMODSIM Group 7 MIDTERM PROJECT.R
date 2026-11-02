#this is testing still with regression now

change <- numeric(10)
ship_method <- character(10)
handling <- character(10)
time <- numeric(10)
updated_time <- numeric(10)
change <- numeric(10)
distance <- numeric(10)
quantity <- numeric(10)
weight <- numeric(10)
total_weight <- numeric(10)
inventory <- character(10)
functionality <- character(10)
satisfaction <- numeric(10)
order_ID <- numeric(10)

for (i in 1:10) {
  #user already inputs order
  order_ID[i] <- i
  #user picks shipment method
  ship_method[i] <- sample(c("Local", "Foreign"),1)
  
  #user gets a shipping date based on ship_method
  #time of delivery in days local(1-5days) and foreign(7-14days)
  if (ship_method[i] == "Local") {
    time[i] <- sample(1:5, 1)
  } else {
    time[i] <- sample(7:14, 1)
  }
  
  #generate random km distance in km
  if (ship_method[i] == "Foreign"){
    distance[i] <- round(runif(1, min=31, max=100),2)
  } else{
    distance[i] <- round(runif(1, min=1, max=30),2)
  }
  #the farther the distance, the longer delivery time. for every 20km, 1 day delivery increase
  time[i] <- time[i] + (distance[i] / 20)
  
  #-----PRODUCT THINGS-----#
  #user picks item quantity
  quantity[i] <- sample(1:10, 1)
  
  #generate random weight in kg PER ITEM
  weight[i] <- round(runif(1, min=1, max=20),2)
  total_weight[i] <- weight[i] * quantity[i]
  
  #if product is unavailable, wait for restock (1-3 days delay)
  inventory[i] <- sample(c("In-Stock", "Unavailable"),1)
  if (inventory[i] == "Unavailable") {
    delay <- sample(1:3, 1)
    time[i] <- time[i] + delay
    satisfaction[i] <- satisfaction[i] - (change[i] * .05)
  } 
  
  #-----USER SATISFACTION-----#
  #if poor(-50 to 80% satisfaction), average (no add or decrease), excellent(+50-80%)
  functionality[i] <- sample(c("Poor", "Average", "Excellent"),1)
  
  base_satisfaction <- runif(1, min=60, max=80)
  
  #Satisfactory Table
  # Quality of product
  if (functionality[i] == "Poor") {
    base_satisfaction <- base_satisfaction - (base_satisfaction * runif(1, min=.10, max=.20))
  } else if (functionality[i] == "Excellent"){
    base_satisfaction <- base_satisfaction + (base_satisfaction * runif(1, min=.10, max=.20))
  } 
  
  # Foreign Affairs
  if (ship_method[i] == "Foreign"){
    base_satisfaction <- base_satisfaction - (base_satisfaction * .10)
    if (functionality[i] == "Excellent"){
      base_satisfaction <- base_satisfaction + (base_satisfaction * runif(1, min=.10, max=.20))
      if (inventory[i] == "In-Stock"){
        base_satisfaction <- base_satisfaction + (base_satisfaction * runif(1, min=.10, max=.20))
      }
    } else if (functionality[i] == "Poor"){
      base_satisfaction <- base_satisfaction - (base_satisfaction * runif(1, min=.10, max=.20))
      if (inventory[i] == "Unavailable"){
        base_satisfaction <- base_satisfaction - (base_satisfaction * .30)
      }
    }
  } 
  
  time[i] = ceiling(time[i])
  #user selects handling (fragile, none, expedited)
  handling[i] <- sample(c("Expedited", "None", "Fragile"),1)
  if (handling[i] == "Expedited") {
    updated_time[i] <- time[i] * .5 #half the delivery time
  } else if (handling[i] == "Fragile") {
    delay <- time[i] * .5 #increase of half the delivery time
    updated_time[i] <- time[i] + delay
  }
  
  change[i] <-  updated_time[i] - time[i]
  
  #if the delay is higher than half of the initial delivery time, satisfaction goes down
  if (change[i] > (time[i] / 2)) {
    base_satisfaction <- base_satisfaction - (base_satisfaction * runif(1, min=.20, max=.50))
  }
  
  satisfaction[i] <- base_satisfaction
  if (handling[i] == "None"){
    change[i] = 0
  }
  
  # satisfaction limit
  if (satisfaction[i] > 100){
    satisfaction[i] = 100
  }
}

results <- data.frame(
  OrderNo = order_ID,
  Quantity = quantity,
  WeightPerItemKG = round(weight, 2),
  TotalWeightKG = round(total_weight,2),
  InventoryStatus = inventory,
  Functionality = functionality,
  ShippingMethod = ship_method,
  Handling = handling,
  DistanceKM = round(distance, 2),
  OriginalTimeDAYS = time,
  UpdatedTimeDAYS = ceiling(updated_time),
  ChangeDAYS = ceiling(change),
  Satisfaction = round(satisfaction, 2)
)

print(results)

#this predicts/checks how factors affect the total time to deliver an item
delivery <- lm(UpdatedTimeDAYS ~ Quantity + TotalWeightKG + DistanceKM + ShippingMethod + Handling + InventoryStatus, data = results)
summary(delivery)

#this predicts/checks how factors affect the customer satisfaction
customer <- lm(Satisfaction ~ UpdatedTimeDAYS + InventoryStatus + Functionality + ChangeDAYS + Handling, data = results)
summary(customer)