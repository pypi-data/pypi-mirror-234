"""
Generate a JWT token
"""
import os
import time
import attr
import jwt


@attr.s(slots=True)
class JWTHandler:
    """Handles the encoding and decoding of JSON Web Tokens (JWTs).

    This class provides methods for encoding data into JWTs and decoding JWTs back
    into data. It allows you to specify the secret key and algorithm for JWT
    operations, typically loaded from environment variables.

    Attributes:
        _secret_key (str): The secret key used for encoding and decoding JWTs.
        _algorithm (str): The encryption algorithm used for JWT operations.
        _decode_time (int): Time to be available this token

    Methods:
        encode(data: dict) -> str:
            Encode a dictionary of data into a JWT.

        decode(token: str) -> dict:
            Decode a JWT token into a dictionary of data.

    # Note:
        - Before using this class, ensure that the `SECRET_KEY` environment variable
          is defined, as it is required for JWT operations.

    Example Usage:
        >>> jwt_handler = JWTHandler()
        >>> data = {"user_id": 123, "role": "admin"}
        >>> encoded_token = jwt_handler.encode(data)
        >>> decoded_data = jwt_handler.decode(encoded_token)
    """
    _secret_key: str = attr.ib(default="")
    _algorithm: str = attr.ib(default="HS256")
    _decode_time: int = attr.ib(default=10080*60)

    def __attrs_post_init__(self):
        # Check if there's a secret key
        if os.environ.get("SECRET_KEY", None) is None:
            raise ValueError(
                "You need to define a `SECRET_KEY` as an environment variable")
        # Append it if it exist
        self._secret_key = os.environ.get("SECRET_KEY", "")
        if os.environ.get("ALGORITHM", None) is not None:
            self._algorithm = os.environ.get("ALGORITHM", "")
        if os.environ.get("TIME_TO_DECODE", None) is not None:
            self._decode_time = int(os.environ.get("TIME", 0))*60

    def encode(self, data: dict) -> str:
        """Encode a dictionary of data into a JWT.

        Args:
            data (dict): The data to be encoded into the JWT.

        Returns:
            str: The encoded JWT token.

        Raises:
            TypeError: If the data provided is not a dictionary.
        """
        if isinstance(data, dict) is False:
            raise TypeError("The data should be a dictionary")
        # Update the data to include the datetime
        data.update({"exp": time.time() + self._decode_time + 3600*6})
        # Encode the data
        return jwt.encode(
            payload=data,
            key=self._secret_key,
            algorithm=self._algorithm
        )

    def decode(self, token: str) -> dict:
        """Decode a JWT token into a dictionary of data.

        Args:
            token (str): The JWT token to be decoded.

        Returns:
            dict: The decoded data from the JWT.

        Raises:
            Warning: If the token cannot be decoded, typically due to invalid or
                tampered token data.
            ValueError: If the token has been expired.
        """
        try:
            decode_data = jwt.decode(
                jwt=token,
                key=self._secret_key,
                algorithms=[self._algorithm]
            )
            return decode_data
        except jwt.DecodeError as e:
            raise Warning("Token cannot be decoded.") from e
        except jwt.ExpiredSignatureError as e:
            raise ValueError("The token has expired.") from e
