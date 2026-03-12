-- Initialize artist data
INSERT INTO artist (artist_id, artist_name) VALUES
(1, 'NewJeans'),
(2, 'LE SSERAFIM')
ON CONFLICT (artist_id) DO NOTHING;

-- Initialize card_set data
INSERT INTO card_set (card_set_id, card_set_name, description) VALUES
(1, 'Base', 'Base card set on release.')
ON CONFLICT (card_set_id) DO NOTHING;

-- Initialize idol data
INSERT INTO idol (idol_id, idol_name, artist_id, card_set_id, current_print, image_url) VALUES
(1, 'Hanni Pham', 1, 1, 0, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1768812377/hanni_jrsrnj.png'),
(2, 'Kim Minji', 1, 1, 0, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1768812378/minji_urma3o.png'),
(3, 'Danielle Marsh', 1, 1, 0, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1768812377/danielle_hwxery.png'),
(4, 'Kang Haerin', 1, 1, 0, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1768812377/haerin_uwubml.png'),
(5, 'Lee Hyein', 1, 1, 0, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1768812378/hyein_mhpr1m.png'),
(6, 'Kim Chaewon', 2, 1, 0, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1772713067/chaewon_ourkwv.png'),
(7, 'Miyawaki Sakura', 2, 1, 0, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1772713554/sakura_mpybht.png'),
(8, 'Huh Yunjin', 2, 1, 0, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1772713067/yunjin_pbyrhg.png'),
(9, 'Nakamura Kazuha', 2, 1, 0, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1772713568/kazuha_x2zjlt.png'),
(10, 'Hong Eunchae', 2, 1, 0, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1772713068/eunchae_xjw6ta.png')
ON CONFLICT (idol_id) DO NOTHING;
