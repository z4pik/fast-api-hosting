from fastapi import APIRouter

# from user.api import send_sms_code, after_verification, after_verification_request

from user.auth import SECRET

user_router = APIRouter()

# user_router.include_router(
#     fastapi_users.get_register_router(send_sms_code), prefix="/auth", tags=["auth"]
# )
# user_router.include_router(
#     fastapi_users.get_reset_password_router(
#         SECRET, after_forgot_password=on_after_forgot_password
#     ),
#     prefix="/auth",
#     tags=["auth"],
# )
user_router.include_router(
    fastapi_users.get_verify_router(
        SECRET,
        after_verification_request=after_verification_request,
        after_verification=after_verification
    ),
    prefix="/auth",
    tags=["auth"],
)
user_router.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])
