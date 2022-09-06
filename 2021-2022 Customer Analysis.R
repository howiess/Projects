library(tidyverse)
library(anytime)
library(eeptools)
library(ggplot2)
df19<-read_csv('C:/Users/CIS/OneDrive - Student Medicover Co/Internal Support/Internal Report/CIS/2020 & 2021 Customer Age Gap Analysis/6-1-2019 to 10-1-2019.csv')
df19<-df19[!(is.na(df19$`First Name`) | df19$`First Name`==""), ] # get rid of white space between lines 
empty_columns<- colSums(is.na(df19) | df19 == "") == nrow(df19) # identify empty columns
sm.wl.index<-grep('^SM|^TRI|^USR|^[0-9]*$',df19$`Order ID`) # find the index of these white labels from the list
df19<-df19[, !empty_columns] %>% .[sm.wl.index,]# reform the data with relevant columns only

df21<-read_csv('C:/Users/CIS/OneDrive - Student Medicover Co/Internal Support/Internal Report/CIS/2020 & 2021 Customer Age Gap Analysis/6-1-2021 to 10-1-2021.csv')
df21<-df21[!(is.na(df21$`First Name`) | df21$`First Name`==""), ] # get rid of white space between lines 
sm.wl.index<-grep('^SM|^TRI|^USR|^[0-9]*$',df21$`Order ID`) # find the index of these white labels from the list
df21<-df21[, !empty_columns] %>% .[sm.wl.index,] # reform the data with relevant columns only

df22<-read_csv('C:/Users/CIS/OneDrive - Student Medicover Co/Internal Support/Internal Report/CIS/2020 & 2021 Customer Age Gap Analysis/6-1-2022 to 8-15-2022.csv')
df22<-df22[!(is.na(df22$`First Name`) | df22$`First Name`==""), ] # get rid of white space between lines 
sm.wl.index<-grep('^SM|^TRI|^USR|^[0-9]*$',df22$`Order ID`) # find the index of these white labels from the list
df22<-df22[, !empty_columns] %>% .[sm.wl.index,]# reform the data with relevant columns only

rm(empty_columns)

# 1. Time Series
date19<-anydate(df19$`Purchase Date`) %>% data.frame() %>% cbind(data.frame(rep(2019,nrow(df19)))) %>% setNames(c('Date','Year'))
date21<-anydate(df21$`Purchase Date`) %>% data.frame() %>% cbind(data.frame(rep(2021,nrow(df21)))) %>% setNames(c('Date','Year'))
date22<-anydate(df22$`Purchase Date`) %>% data.frame() %>% cbind(data.frame(rep(2022,nrow(df22)))) %>% setNames(c('Date','Year'))
date.df<-rbind(date19,date21,date22)

date.sum.df<- data.frame(table(date.df$Date)) %>% setNames(c('Date','Count'))
date.sum.df$Date<-as.Date(date.sum.df$Date)

plot1 <- ggplot(date.sum.df, aes(Date, Count, group = 1)) +
  geom_point() +
  geom_line() +
  labs(x = "Date", y = "Number of Enrollments", 
       title = "Number of Enrollments Time Series") +
  scale_x_date(breaks = as.Date(c("2019-08-01","2021-08-01","2022-08-01")),
               date_minor_breaks = "1 month",
               date_labels = "%Y-%m")

plot(plot1)

date.sum.df1<-data.frame(split(date.sum.df, format(as.Date(date.sum.df$Date), "%Y"))[1:2])
date.sum.df1$X2019.Date<-format(as.Date(date.sum.df1$X2019.Date), "%m-%d")
date.sum.df1<-date.sum.df1[,-3] %>% setNames(c('Date','Value19','Value21'))

temp<-data.frame(split(date.sum.df, format(as.Date(date.sum.df$Date), "%Y"))[3])
temp$X2022.Date<-format(as.Date(temp$X2022.Date), "%m-%d")
temp<-setNames(temp,c('Date','Value22'))

date.sum.df1<-merge(date.sum.df1,temp,by='Date',all=T)
date.sum.df1$Date<-as.Date(date.sum.df1$Date, "%m-%d")

a<-date.sum.df1[,c(1,2)] %>% cbind((date19[,2])[1:nrow(date.sum.df1)]) %>% setNames(c('Date','Value','Year'))
b<-date.sum.df1[,c(1,3)] %>% cbind((date21[,2])[1:nrow(date.sum.df1)]) %>% setNames(c('Date','Value','Year'))
c<-date.sum.df1[,c(1,4)] %>% cbind((date22[,2])[1:nrow(date.sum.df1)]) %>% setNames(c('Date','Value','Year'))

date.sum.df2<-rbind(a,b,c)

plot2<-ggplot(date.sum.df2, aes(x=Date, y=Value)) + geom_line(aes(color = as.factor(Year)), size = 0.9) + 
  labs(x = "Date",
       y = "Number of Enrollments",
       color = "Year") +
  theme_bw()+
  scale_color_manual(values = c("Purple","Steelblue","Green")) +
  scale_x_date(date_breaks = "1 month",
               date_minor_breaks = "1 month",
               date_labels = "%m-%d") +
  theme(legend.position = "bottom")
  
rm(temp,date19,date21,date22,date.sum.df,date.sum.df1,date.sum.df2,a,b,c,sm.wl.index,date.df)

# 2. Sales vs. Geographic

library(leaflet)
library(maps)
library(urbnmapr)

world<- map_data("world")
b<-data.frame(table(df21$`Country of Origin`)) %>% setNames(c('Country','Value'))
c<-data.frame(table(df22$`Country of Origin`)) %>% setNames(c('Country','Value'))
country.df<-merge(b,c,by='Country') %>% setNames(c('Country','Value21',"Value22")) 
b<-country.df[,c(1,2)] %>% cbind(data.frame(rep('2021',nrow(country.df)))) %>% setNames(c('Country','Value','Year')) 
c<-country.df[,c(1,3)] %>% cbind(data.frame(rep('2022',nrow(country.df)))) %>% setNames(c('Country','Value','Year')) 
country.df<- rbind(b,c)
ggplot(country.df,aes(x=Country, y=Value,fill=as.factor(Year))) + geom_bar(position="dodge", stat="identity")

