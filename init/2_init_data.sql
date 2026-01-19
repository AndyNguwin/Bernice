-- Initialize artist data
INSERT INTO artist (artist_id, artist_name) VALUES
(1, 'NewJeans')
ON CONFLICT (artist_id) DO NOTHING;

-- Initialize card_set data
INSERT INTO card_set (card_set_id, card_set_name, description) VALUES
(1, 'Base', 'Base card set on release.')
ON CONFLICT (card_set_id) DO NOTHING;

-- Initialize idol data
INSERT INTO idol (idol_id, idol_name, artist_id, card_set_id, current_print, image_url) VALUES
(1, 'Hanni', 1, 1, 0, 'img/hanni.png'),
(2, 'Minji', 1, 1, 0, 'img/minji.png'),
(3, 'Danielle', 1, 1, 0, 'img/danielle.png'),
(4, 'Haerin', 1, 1, 0, 'img/haerin.png'),
(5, 'Hyein', 1, 1, 0, 'img/hyein.png')
ON CONFLICT (idol_id) DO NOTHING;
