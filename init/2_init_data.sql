INSERT INTO rarity_rates (rarity, rate) VALUES
(1, 0.3500),
(2, 0.3000),
(3, 0.2000),
(4, 0.1000),
(5, 0.0500)
ON CONFLICT (rarity) DO NOTHING;

-- Initialize artist data
INSERT INTO artist (artist_id, artist_name) VALUES
(1, 'NewJeans'),
(2, 'LE SSERAFIM'),
(3, 'ITZY'),
(4, 'aespa'),
(5, 'BIGBANG')
ON CONFLICT (artist_id) DO NOTHING;

-- Initialize card_set data
INSERT INTO card_set (card_set_id, card_set_name, description) VALUES
(1, 'Regular', 'Regular pool.')
ON CONFLICT (card_set_id) DO NOTHING;

-- Idols (members only)
INSERT INTO idol (idol_id, idol_name, artist_id) VALUES
(1, 'Hanni', 1),
(2, 'Minji', 1),
(3, 'Danielle', 1),
(4, 'Haerin', 1),
(5, 'Hyein', 1),
(6, 'Chaewon', 2),
(7, 'Sakura', 2),
(8, 'Yunjin', 2),
(9, 'Kazuha', 2),
(10, 'Eunchae', 2),
(11, 'Yeji', 3),
(12, 'Lia', 3),
(13, 'Ryujin', 3),
(14, 'Chaeryeong', 3),
(15, 'Yuna', 3),
(16, 'Karina', 4),
(17, 'Giselle', 4),
(18, 'Winter', 4),
(19, 'Ningning', 4),
(20, 'G-DRAGON', 5),
(21, 'T.O.P', 5),
(22, 'Taeyang', 5),
(23, 'Daesung', 5)
ON CONFLICT (idol_id) DO NOTHING;

-- Catalog cards: set public_code yourself when adding rows; placeholders below
INSERT INTO idol_card (idol_card_id, public_code, idol_id, card_set_id, rarity, image_url, total_print_count) VALUES
(1, 'lsfYUNJ-S3-01', 8, 1, 3, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554488/lsfYUNJ-S3-01_pr6ru0.png', 0),
(2, 'lsfYUNJ-S2-01', 8, 1, 2, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554487/lsfYUNJ-S2-01_ang1aj.png', 0),
(3, 'lsfYUNJ-S1-01', 8, 1, 1, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554487/lsfYUNJ-S1-01_hwywbj.png', 0),
(4, 'lsfEUNC-S3-01', 10, 1, 3, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554485/lsfEUNC-S3-01_iivani.png', 0),
(5, 'lsfEUNC-S2-01', 10, 1, 2, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554483/lsfEUNC-S2-01_qc1fdb.png', 0),
(6, 'lsfEUNC-S1-01', 10, 1, 1, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554485/lsfEUNC-S1-01_ikumya.png', 0),
(7, 'lsfSAKU-S3-01', 7, 1, 3, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554485/lsfSAKU-S3-01_wwxike.png', 0),
(8, 'lsfSAKU-S2-01', 7, 1, 2, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554484/lsfSAKU-S2-01_iwggig.png', 0),
(9, 'lsfSAKU-S1-01', 7, 1, 1, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554484/lsfSAKU-S1-01_s0fimz.png', 0),
(10, 'lsfKAZU-S3-01', 9, 1, 3, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554484/lsfKAZU-S3-01_db1nlv.png', 0),
(11, 'lsfKAZU-S2-01', 9, 1, 2, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554484/lsfKAZU-S2-01_w3yu6f.png', 0),
(12, 'lsfKAZU-S1-01', 9, 1, 1, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554483/lsfKAZU-S1-01_tg1cbo.png', 0),
(13, 'lsfCHAE-S3-01', 6, 1, 3, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554483/lsfCHAE-S3-01_fceka1.png', 0),
(14, 'lsfCHAE-S2-01', 6, 1, 2, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554484/lsfCHAE-S2-01_whbecs.png', 0),
(15, 'lsfCHAE-S1-01', 6, 1, 1, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554483/lsfCHAE-S1-01_ybrnbm.png', 0),
(16, 'itzYEJI-S3-01', 11, 1, 3, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554520/itzYEJI-S3-01_lvfuuz.png', 0),
(17, 'itzYEJI-S2-01', 11, 1, 2, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554519/itzYEJI-S2-01_uzta22.png', 0),
(18, 'itzYEJI-S1-01', 11, 1, 1, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554519/itzYEJI-S1-01_mi7fx6.png', 0),
(19, 'itzLIA-S3-01', 12, 1, 3, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554516/itzLIA-S3-01_jtmuta.png', 0),
(20, 'itzLIA-S2-01', 12, 1, 2, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554515/itzLIA-S2-01_ozaiig.png', 0),
(21, 'itzLIA-S1-01', 12, 1, 1, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554514/itzLIA-S1-01_hfpqmm.png', 0),
(22, 'itzRYUJ-S3-01', 13, 1, 3, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554518/itzRYUJ-S3-01_dqrtj0.png', 0),
(23, 'itzRYUJ-S2-01', 13, 1, 2, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554517/itzRYUJ-S2-01_vc6u88.png', 0),
(24, 'itzRYUJ-S1-01', 13, 1, 1, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554516/itzRYUJ-S1-01_bwlihq.png', 0),
(25, 'itzCHRY-S3-01', 14, 1, 3, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554515/itzCHRY-S3-01_cfxgkw.png', 0),
(26, 'itzCHRY-S2-01', 14, 1, 2, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554513/itzCHRY-S2-01_rusfum.png', 0),
(27, 'itzCHRY-S1-01', 14, 1, 1, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554514/itzCHRY-S1-01_xeu1hj.png', 0),
(28, 'itzYUNA-S3-01', 15, 1, 3, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554521/itzYUNA-S3-01_u6zti8.png', 0),
(29, 'itzYUNA-S2-01', 15, 1, 2, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554522/itzYUNA-S2-01_pkzgfu.png', 0),
(30, 'itzYUNA-S1-01', 15, 1, 1, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778554521/itzYUNA-S1-01_cqajw8.png', 0),
(31, 'aesKARI-S3-01', 16, 1, 3, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778670307/aesKARI-S3-01_upajzf.png', 0),
(32, 'aesKARI-S2-01', 16, 1, 2, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778670307/aesKARI-S2-01_anwv9y.png', 0),
(33, 'aesKARI-S1-01', 16, 1, 1, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778670307/aesKARI-S1-01_ypwqbm.png', 0),
(34, 'aesGISE-S3-01', 17, 1, 3, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778670307/aesGISE-S3-01_dldedy.png', 0),
(35, 'aesGISE-S2-01', 17, 1, 2, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778670306/aesGISE-S2-01_iukpbc.png', 0),
(36, 'aesGISE-S1-01', 17, 1, 1, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778670307/aesGISE-S1-01_zlarjj.png', 0),
(37, 'aesWINT-S3-01', 18, 1, 3, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778670308/aesWINT-S3-01_cnppl7.png', 0),
(38, 'aesWINT-S2-01', 18, 1, 2, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778670308/aesWINT-S2-01_ibxww2.png', 0),
(39, 'aesWINT-S1-01', 18, 1, 1, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778670308/aesWINT-S1-01_aeakst.png', 0),
(40, 'aesNING-S3-01', 19, 1, 3, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778670308/aesNING-S3-01_qxjkvg.png', 0),
(41, 'aesNING-S2-01', 19, 1, 2, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778670308/aesNING-S2-01_jblg6d.png', 0),
(42, 'aesNING-S1-01', 19, 1, 1, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778670307/aesNING-S1-01_oc6b7k.png', 0),
(43, 'bbngGDRA-S2-01', 20, 1, 2, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778749104/bbngGDRA-S2-01_abg6ts.png', 0),
(44, 'bbngGDRA-S1-01', 20, 1, 1, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778749104/bbngGDRA-S1-01_bttnod.png', 0),
(45, 'bbngTOP-S2-01', 21, 1, 2, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778749103/bbngTOP-S2-01_ptubfj.png', 0),
(46, 'bbngTOP-S1-01', 21, 1, 1, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778749104/bbngTOP-S1-01_nqchvq.png', 0),
(47, 'bbngTAEY-S2-01', 22, 1, 2, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778749104/bbngTAEY-S2-01_ldeyqe.png', 0),
(48, 'bbngTAEY-S1-01', 22, 1, 1, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778749104/bbngTAEY-S1-01_lwcnrg.png', 0),
(49, 'bbngDAES-S2-01', 23, 1, 2, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778749104/bbngDAES-S2-01_xmexpu.png', 0),
(50, 'bbngDAES-S1-01', 23, 1, 1, 'https://res.cloudinary.com/dplcs6tbo/image/upload/v1778749103/bbngDAES-S1-01_yfs4ux.png', 0)
ON CONFLICT (idol_card_id) DO NOTHING;

-- Keep SERIAL sequences past explicit seed IDs
SELECT setval(pg_get_serial_sequence('artist', 'artist_id'), (SELECT COALESCE(MAX(artist_id), 1) FROM artist));
SELECT setval(pg_get_serial_sequence('card_set', 'card_set_id'), (SELECT COALESCE(MAX(card_set_id), 1) FROM card_set));
SELECT setval(pg_get_serial_sequence('idol', 'idol_id'), (SELECT COALESCE(MAX(idol_id), 1) FROM idol));
SELECT setval(pg_get_serial_sequence('idol_card', 'idol_card_id'), (SELECT COALESCE(MAX(idol_card_id), 1) FROM idol_card));
