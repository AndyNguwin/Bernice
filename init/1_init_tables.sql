-- Instead of card code counter as a global to prevent race conditions
CREATE SEQUENCE IF NOT EXISTS card_code_seq
  START WITH 1
  INCREMENT BY 1
  MINVALUE 1;

-- Create USER table (no dependencies)
CREATE TABLE IF NOT EXISTS "user" (
    discord_id BIGINT PRIMARY KEY
);

-- Create ARTIST table (no dependencies)
CREATE TABLE IF NOT EXISTS artist (
    artist_id SERIAL PRIMARY KEY,
    artist_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS card_set (
    card_set_id SERIAL PRIMARY KEY,
    card_set_name VARCHAR(255) NOT NULL,
    description TEXT
);

-- Create IDOL table (depends on ARTIST, CARD_SET)
CREATE TABLE IF NOT EXISTS idol (
    idol_id SERIAL PRIMARY KEY,
    idol_name VARCHAR(255) NOT NULL,
    artist_id INTEGER NOT NULL,
    card_set_id INTEGER NOT NULL,
    current_print INTEGER DEFAULT 0 NOT NULL,
    image_url TEXT,
    FOREIGN KEY (artist_id) REFERENCES artist(artist_id) ON DELETE CASCADE,
    FOREIGN KEY (card_set_id) REFERENCES card_set(card_set_id) ON DELETE CASCADE
);

-- Create CARD table (depends on USER and IDOL)
CREATE TABLE IF NOT EXISTS card (
    card_id BIGSERIAL PRIMARY KEY,
    public_code VARCHAR(6) NOT NULL UNIQUE,
    CONSTRAINT card_instance_public_code_format
        CHECK (public_code ~ '^[A-HJ-NP-Za-hj-np-z2-9]{6}$'),

    idol_id INTEGER NOT NULL,
    print_number INTEGER NOT NULL,
    owner_id BIGINT NOT NULL,
    acquired_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idol_id) REFERENCES idol(idol_id) ON DELETE CASCADE,
    FOREIGN KEY (owner_id) REFERENCES "user"(discord_id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_card_discord_id ON card(owner_id);
CREATE INDEX IF NOT EXISTS idx_card_public_code ON card(public_code);