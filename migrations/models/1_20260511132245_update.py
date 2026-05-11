from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "is_active" BOOL NOT NULL DEFAULT False;
        ALTER TABLE "user" ADD "is_email_verified" BOOL NOT NULL DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "is_active";
        ALTER TABLE "user" DROP COLUMN "is_email_verified";"""


MODELS_STATE = (
    "eJztmm1vmzoUx78K4s3tpN4ozdpura6ulAe6ZWuSqk3vrrZOyMFOYhUMw6ZZVPW7zzYQwE"
    "BS0vRReRMlxz7G/h1y+B+bW91xIbJpbegDQoHFsEv0Y+1WJ8BB/EtR866mA89LGoWBgZEt"
    "+zOl44hyi8V40xjYFHETRNTysRddSU+NrMnxNB95PqKIMEwmGtDGmABiYWBrqbE1G5NrBD"
    "Xm8h4zYNuI1cT1oGvxC3LHzQ8dEPwrQCZzJ4hNkc8v8OMnN2MC0W9E45/etTnGyIYZiBiK"
    "AaTdZHNP2i4vu50T2VNMe2Rarh04JOntzdnUJYvuQYBhTfiItgkiyAcMwRRWEth2FITYFM"
    "6YG5gfoMVUYWKAaAwCWwRH/2cckHD58kriY/9fPRcucRUFc2SyXCJCjQkTLG7vwlUla5ZW"
    "XVyq/bl5vvP+8J1cpUvZxJeNkoh+Jx0BA6Gr5JqABI4bEJaH2UEWdoBdzDNxUpjC0KsWea"
    "9DNjYkaJPbPGYbM9s4yI7R7vaapzt7jd2GpEl/2ZjJpf3XPJeY9+vvJNIEoVx8DmB7CnyD"
    "BI4k2OUT4P8LlCMZ+yoc+XSflJ3ePjc63eGxZvkIYnZFOkZL/IRohJmaBYqp6g74bdqITN"
    "iU/zxcAjkmGd6vLk9mYaLrRw0N0ZJFzOmxgK4LOfF+Osy6hwgUvPKsz4x+p9v/dKxFXa5I"
    "e9A7OzWGRocHwHU8nh8RvCInze6pMI0BthFcJwpH94jCUWkUjtQopNdRGIribKG4rRWDKL"
    "0+YZbIkmwcHNyDJe9VSlO2ZXnyP5tYsQmK8i9vYdhBxUiznmoSjlxr8ZeXmYZ1vgY4IPY8"
    "Cu8SvsNuz7gYNntnYiUO5UlZImoODdHSkNa5Ys2ll8Ug2rfu8LMmfmrfB31DfWgu+g2/62"
    "JOIGCuSdyZCWDqQR9bYzCZwAYeXDOwWc9tYJ81sNHkk7iG2tWsJj4zTpvUoM+qlFZITiHc"
    "x9eFijPkkSd44voIT8hXNM89zRVqUQX1bTHQiyWXWJMbzAezRUGTvTn4EvnCUKg3282Ldr"
    "Nj6BLlCFjXM+BDM8NUtLgNV7Es+uabnIajWgABE0lArEPMOoJ7SWVBlitbpX13Wb0axD1W"
    "FqpirOIyUoyhYaLxslCjc8qQk69FK3tvy82n+e/vLik3RWjk9wr6Me2zGQG/GucmteNB/R"
    "7S8aBeqhwPchUncnhJUAXhwuE18nsU7e0BSmcuz5JTQKdVUOYcn7l0f0lQtwXNm9C924Lm"
    "jQY2V9BgaspHg3mDfMzXUyBzWq5rI0BKlE6RvxLkER/gseJaLCw3oXFag8FpJoat7lDJhJ"
    "e9lnG+s6fsE3f7QyUrckjiHOSmQPSsgpv4baEWFJXlpZFabhbsHbcix5Ov58gGJbuTr7jU"
    "vHvM8jACUlAgJqjKS8RkC2B1kRiOV17o/UWjI0VthtlUGwFb7BpogMD0ESTN14+bHHhbWm"
    "4oQzygtIwCVPEoM+X1PGeZ9Vr9UUiudZS5FfBvQudtBfwbDWxOwIsHVcXziJTL9jRisVv9"
    "wLOIeFv8xVJbeRKRui2qnkOkXoVJCaOHKW7l9bjXw/VRZXeTl9nWVC+Q3VHLUtkNkj6rZH"
    "c5hg1L3S5hFZQuJrkiLLqXn3W7eiKu8ndjb//D/sf3h/sfeRc5k4Xlw5LcFW8YlCvbG+TT"
    "iu/cpFy2+9PJy478r1EBYtT9dQLcq9/n2In3KgUo25T6wCUMFb0u+uVi0C8pDBIXBeQl4Q"
    "v8AbHFdjUbU/bzZWJdQlGsOqMTY3g7veb/Ktf26aCl6hMxQKvaztbmHy93fwBWZhoV"
)
