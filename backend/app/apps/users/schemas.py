from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserPasswordSchema(BaseModel):
    password: str


class UserBaseFieldsSchema(BaseModel):
    email: EmailStr
    name: str

    model_config = ConfigDict(
        str_strip_whitespace=True
    )


class RegisterUserSchema(UserPasswordSchema, UserBaseFieldsSchema):
    pass