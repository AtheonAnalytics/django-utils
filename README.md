# django-utils

## feature-flag

Feature flag package which enable per client feature flags (through customizable client field reference)

## logger

 - `RequestsHelper` wrapper for `requests` library to log `outbound` API requests
 - `APILoggingMixin` to log `inbound` API requests
 - `AdminActivityMiddleware` to log django admin activity
 - `CleanedJsonFormatter` logging formatter to clean sensitive data from json logs 
 - `log_with_time` context manager to log code execution time

## misc

 - `RealIPMiddleware` to capture real user IP address (behind proxy)
 - `AdminLinkMixin` gives generic admin url to change form
