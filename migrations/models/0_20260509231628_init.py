from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password_hash" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "user" IS 'User model representing a user in the system.';
CREATE TABLE IF NOT EXISTS "wallet" (
    "id" UUID NOT NULL PRIMARY KEY,
    "balance" DECIMAL(12,2) NOT NULL DEFAULT 0,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "wallet" IS 'Wallet model representing a user''s wallet with balance and transactions.';
CREATE TABLE IF NOT EXISTS "transaction" (
    "id" UUID NOT NULL PRIMARY KEY,
    "amount" DECIMAL(12,2) NOT NULL,
    "type" VARCHAR(6) NOT NULL,
    "status" VARCHAR(9) NOT NULL DEFAULT 'pending',
    "description" VARCHAR(255),
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "wallet_id" UUID NOT NULL REFERENCES "wallet" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "transaction"."type" IS 'CREDIT: credit\nDEBIT: debit';
COMMENT ON COLUMN "transaction"."status" IS 'PENDING: pending\nCOMPLETED: completed\nFAILED: failed';
COMMENT ON TABLE "transaction" IS 'Transaction model representing a financial transaction linked to a wallet.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmv1v2jgYx/8VK79cJ3GIMtqt1emkFNIbtwJVS2+nrRMysQGriZPFzjFU9X8/20nIK9"
    "AwCrTiF0Qe+/HL53Gc7+PkUbMdhC1W7XuQMmhy4lDtHDxqFNpY/CkqrgANum5cKA0cDi1V"
    "n2cqDpmwmFwUjaDFsDAhzEyPuGFPWqJloNoDHnY9zDDlhI4BBCNCITUJtECibWAR+oAR4I"
    "6oMYWWhXlV9occU3QoHDfftE/JDx8PuDPGfII90cG378JMKMI/MYsu3YfBiGALpSASJBtQ"
    "9gGfucp2d9duXaqactjDgelYvk3j2u6MTxw6r+77BFWljywbY4o9yDFKYKW+ZYVBiEzBiI"
    "WBez6eDxXFBoRH0LdkcLQ/Rj4Npq96kj+NP7VcuGQvGcyhyXSoDDWhXLJ4fApmFc9ZWTXZ"
    "VfOTfnP0/vSdmqXD+NhThYqI9qQcIYeBq+Iag4S241Oeh9nCJrGhVcwzdsowRYFXNfReh2"
    "xkiNHGyzxiGzHbOMiW0Wx39Kuj43qlrmiyHxbhamr/6DcKc6P2TiGNEarJ5wA2J9AzqG8r"
    "gm0xAHFf4BzJyDfDUQx3q+y05o3RavfPgelhRPg9bRkX8hLhIeHZXaCYqmbDnwML0zGfiM"
    "vTJZAjksF6dcRmFmx03bCgLkvSiAU97rN1Icfe28OsuZgiySvP+trottrdv85BWOWeNnud"
    "6yujb7REABzbFfsjRvf0Um9fSdMIEgujdaJw9owonC2Mwlk2Csl5FIaieLfIuK0Vg3B73e"
    "IukSZZPzl5BktRayFNVZbmKW42OeMBLNp/RQknNi5GmvbMbsKhazX6s5/bsCbmgHrUmoXh"
    "XcK33+4Yt329cy1nYjOxKStEet+QJXVlnWWsue1l3gj40u5/AvISfO11jexDc16v/1WTY4"
    "I+dwbUmQ4gSjzoI2sEJhVY30VrBjbteQjsTgMbDj6Oa6BdB+XEZ8ppkxp0p0ppheSUwn30"
    "UKg4Ax55gpeOh8mYfsaz3NM8Qy3MoL7MG9pbcrE1XmAenM4TmvTiEFMUE8OB3mzqt029ZW"
    "gK5RCaD1PooUGKqSxx6k7GMq+bL7LrdtYCKRwrAnIectQh3DumErJc2qrslWX5qh/VWJmo"
    "yraK00jZBiAUiLQQsBnj2M7noqW9D+nmdu79ypJ0U4ZG/S+hH5M+mxHwq3FuUjue1J4hHU"
    "9qC5XjSS7jxLZICcognDu8Rn4vor1dyNjUEbvkBLJJGZQ5xx2n7vsE9ZDQvAnde0ho3mhg"
    "1eBz0nyxwMyK9oITuIvQ8fLzDbbggjOeVyzYn15SZIdACmR2jGqx0I4TqdVSO2hvsVz+jY"
    "UvZsCU8AkYQkvmXgBSlHyRw/IqfJMNHwT6Git2wwI9DFDJF0IJr928EapVay9Ccq0XQgcZ"
    "9CaelgcZ9EYDmzvXlQ+qkqe6CZfDme78zO8XT3Sjw8W9pbbyPDexLMqe5iY+KEgIo19T3J"
    "mPjF4P1xeV3Tr2iDnRCmR3WLJUdsO4zirZvRjDhqVum/ISSpfQXBIWruWdHvqNZS+/148b"
    "Hxof3582PooqaiRzy4cle1e721+hbP/DHiv55ULC5XDKF38yJm6NEhDD6q8T4HHtOYf3ot"
    "ZCgKoskx84lOOij+7+vu11FyQGsUsG5B0VE/yGiMkrwCKMf99PrEsoylmndGIE76ij/5vl"
    "2rzqXWT1iWzgokigbPPV6dP/8NA6Rg=="
)
