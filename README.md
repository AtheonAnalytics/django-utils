# django-utils

## feature-flag

Feature flag package which enable per client feature flags (through customizable client field reference)

## helper 

 - `RequestsHelper` wrapper for `requests` library to handle basic auth vs token and log `outbound` API requests

## logger

 - `APILoggingMixin` to log `inbound` API requests
 - `AdminActivityMiddleware` to log django admin activity
 - `CleanedJsonFormatter` logging formatter to clean sensitive data from json logs 
 - `log_with_time` context manager to log code execution time

