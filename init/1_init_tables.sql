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

CREATE TABLE IF NOT EXISTS idol (
    idol_id SERIAL PRIMARY KEY,
    idol_name VARCHAR(255) NOT NULL,
    artist_id INTEGER NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES artist(artist_id) ON DELETE CASCADE
);

-- Catalog of cards
CREATE TABLE IF NOT EXISTS idol_card (
    idol_card_id BIGSERIAL PRIMARY KEY,
    public_code VARCHAR(15) NOT NULL UNIQUE,
    idol_id INTEGER NOT NULL,
    card_set_id INTEGER NOT NULL,
    rarity INTEGER NOT NULL,
    CONSTRAINT idol_card_rarity_range CHECK (rarity >= 1 AND rarity <= 5),
    image_url TEXT,
    total_print_count INTEGER DEFAULT 0 NOT NULL,
    FOREIGN KEY (idol_id) REFERENCES idol(idol_id) ON DELETE CASCADE,
    FOREIGN KEY (card_set_id) REFERENCES card_set(card_set_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_inventory (
    user_id BIGINT NOT NULL,
    idol_card_id BIGINT NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (user_id, idol_card_id),
    CONSTRAINT user_inventory_quantity_positive CHECK (quantity >= 1),
    FOREIGN KEY (user_id) REFERENCES "user"(discord_id) ON DELETE CASCADE,
    FOREIGN KEY (idol_card_id) REFERENCES idol_card(idol_card_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_user_inventory_user ON user_inventory(user_id);
CREATE INDEX IF NOT EXISTS idx_idol_card_public_code ON idol_card(public_code);
