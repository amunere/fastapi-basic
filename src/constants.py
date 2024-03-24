class ErrorMessage:
    AUTHENTICATION_REQUIRED = "Authentication required."
    AUTHORIZATION_FAILED = "Authorization failed. The user doesn't have access."
    INVALID_TOKEN = "Invalid token."
    INVALID_CREDENTIALS = "Could not validate credentials."
    EMAIL_TAKEN = "Email or username is already taken."
    ERROR = "Something unexpected happened! Server Error."
    INVALID_PASSWORD = "Invalid Password Reset Payload or Reset Link Expired."
    INVALID_CHECK_PASSWORD = "New password and confirm password are not same."
    IVALID_VERIFY = "Invalid or Reset Link Expired."
    USER_NOT_FOUND = "User not found."

class SuccessMessage:
    SUCCESSFULL_RESET_PASSWORD = "Password Rest Successfull!"
    SUCCESSFULL_ACTIVATION = "Activation Successfull!"