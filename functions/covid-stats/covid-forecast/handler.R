library(forecast)

covid_forecast <- function(region, cases, window, last) {
  ## API endpoint for region in global data set
  u <- paste0("https://hub.analythium.io/covid-19/api/v1/regions/", region)
  x <- jsonlite::fromJSON(u) # will throw error if region is not found
  ## check arguments
  if (missing(cases))
    cases <- "confirmed"
  cases <- match.arg(cases, c("confirmed", "deaths"))
  if (missing(window))
    window <- 14
  window <- round(window)
  if (window < 1)
    stop("window must be > 0")
  ## time series: daily new cases
  y <- pmax(0, diff(x$rawdata[[cases]]))
  ## dates
  z <- as.Date(x$rawdata$date[-1])
  ## trim time series according to last date
  if (!missing(last)) {
    last <- min(max(z), as.Date(last))
    y <- y[z <= last]
    z <- z[z <= last]
  } else {
    last <- z[length(z)]
  }
  ## fit exponential smoothing model
  m <- ets(y)
  ## forecast based on model and window
  f <- forecast(m, h=window)
  ## processing the forecast object
  p <- cbind(Date=seq(last+1, last+window, 1), as.data.frame(f))
  p[p < 0] <- 0
  as.list(p)
}


#* COVID
#* @get /
function(region, cases, window, last) {
  if (!missing(window))
    window <- as.numeric(window)
  covid_forecast(region, cases, window, last)
}