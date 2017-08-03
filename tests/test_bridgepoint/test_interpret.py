import unittest


model = """
-- root-types-contained: Package_c
-- BP 7.1 content: StreamData syschar: 3 persistence-version: 7.1.6

INSERT INTO EP_PKG
    VALUES ("96ec2ddc-da38-40da-8372-025532bfdb1d",
    "d8ca6d9b-7cf6-4f9b-9224-bf1bbd4de04a",
    "d8ca6d9b-7cf6-4f9b-9224-bf1bbd4de04a",
    'Stimuli',
    '',
    0);
INSERT INTO GD_MD
    VALUES ("47f372d5-f768-4a0a-94f3-341d16ad507d",
    112,
    "96ec2ddc-da38-40da-8372-025532bfdb1d",
    108,
    0,
    0,
    1,
    1,
    1,
    12,
    1,
    0,
    0,
    200,
    150,
    0,
    '4.1.17',
    'Test::Stimuli');
INSERT INTO GD_GE
    VALUES ("3c217645-a850-4d24-8e8e-5b0faad0cdb3",
    "47f372d5-f768-4a0a-94f3-341d16ad507d",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    21,
    0,
    'Test::Stimuli::Class');
INSERT INTO GD_SHP
    VALUES ("3c217645-a850-4d24-8e8e-5b0faad0cdb3");
INSERT INTO GD_NCS
    VALUES ("3c217645-a850-4d24-8e8e-5b0faad0cdb3");
INSERT INTO DIM_ND
    VALUES (589.000000,
    217.000000,
    "3c217645-a850-4d24-8e8e-5b0faad0cdb3");
INSERT INTO DIM_GE
    VALUES (24.000000,
    48.000000,
    "3c217645-a850-4d24-8e8e-5b0faad0cdb3",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("3c217645-a850-4d24-8e8e-5b0faad0cdb3",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_CON
    VALUES ("68bec42f-065f-49e6-a5c4-1572b894956b",
    613.000000,
    96.000000,
    "3c217645-a850-4d24-8e8e-5b0faad0cdb3");
INSERT INTO DIM_CON
    VALUES ("ccdc9074-dbe9-4686-be0b-464c278fa7a5",
    497.000000,
    265.000000,
    "3c217645-a850-4d24-8e8e-5b0faad0cdb3");
INSERT INTO DIM_CON
    VALUES ("ec7b54a2-3ed3-4f7a-8d3d-5ae469f6d4d8",
    204.000000,
    265.000000,
    "3c217645-a850-4d24-8e8e-5b0faad0cdb3");
INSERT INTO GD_GE
    VALUES ("cc3d9222-c7db-401f-88cb-b2912a95b268",
    "47f372d5-f768-4a0a-94f3-341d16ad507d",
    "83517940-72ca-47ec-ad7d-a04d06f560b6",
    24,
    0,
    'Test::Stimuli::R1');
INSERT INTO GD_CON
    VALUES ("cc3d9222-c7db-401f-88cb-b2912a95b268",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO GD_CTXT
    VALUES ("440f8de2-63e7-4476-af63-ed9d78d9582e",
    "cc3d9222-c7db-401f-88cb-b2912a95b268",
    1,
    0.000000,
    0.000000);
INSERT INTO DIM_ND
    VALUES (0.000000,
    0.000000,
    "440f8de2-63e7-4476-af63-ed9d78d9582e");
INSERT INTO DIM_GE
    VALUES (623.000000,
    106.000000,
    "440f8de2-63e7-4476-af63-ed9d78d9582e",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("440f8de2-63e7-4476-af63-ed9d78d9582e",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO GD_CTXT
    VALUES ("8e457573-102d-44c7-82c7-0c0713c22039",
    "cc3d9222-c7db-401f-88cb-b2912a95b268",
    3,
    0.000000,
    0.000000);
INSERT INTO DIM_ND
    VALUES (0.000000,
    0.000000,
    "8e457573-102d-44c7-82c7-0c0713c22039");
INSERT INTO DIM_GE
    VALUES (688.000000,
    295.000000,
    "8e457573-102d-44c7-82c7-0c0713c22039",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("8e457573-102d-44c7-82c7-0c0713c22039",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO GD_CTXT
    VALUES ("a79ba264-fe9a-4531-95fd-0a9cb1d36e77",
    "cc3d9222-c7db-401f-88cb-b2912a95b268",
    2,
    0.000000,
    0.000000);
INSERT INTO DIM_ND
    VALUES (0.000000,
    0.000000,
    "a79ba264-fe9a-4531-95fd-0a9cb1d36e77");
INSERT INTO DIM_GE
    VALUES (502.000000,
    270.000000,
    "a79ba264-fe9a-4531-95fd-0a9cb1d36e77",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("a79ba264-fe9a-4531-95fd-0a9cb1d36e77",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO GD_LS
    VALUES ("b9f1a5fb-6d7a-4d9a-bde2-ba149af8ff36",
    "cc3d9222-c7db-401f-88cb-b2912a95b268",
    "00000000-0000-0000-0000-000000000000",
    "b66f047f-0b04-44f7-b2cd-fb53b1e37ab2",
    "a03d45c1-af19-4e1d-ab1a-ea1c829cf0c3");
INSERT INTO GD_LS
    VALUES ("8b39f93c-62de-49af-9d91-f22f1d04e059",
    "cc3d9222-c7db-401f-88cb-b2912a95b268",
    "b9f1a5fb-6d7a-4d9a-bde2-ba149af8ff36",
    "a03d45c1-af19-4e1d-ab1a-ea1c829cf0c3",
    "49846951-7ed1-4c03-9406-bcd3ff7145d5");
INSERT INTO GD_LS
    VALUES ("1a7b7cde-5bdd-40c2-8771-25ce32f26e78",
    "cc3d9222-c7db-401f-88cb-b2912a95b268",
    "8b39f93c-62de-49af-9d91-f22f1d04e059",
    "49846951-7ed1-4c03-9406-bcd3ff7145d5",
    "90d8d349-9729-407e-a54c-85ea0e9170f6");
INSERT INTO GD_AOS
    VALUES ("2f920c1c-7f9d-4a65-9326-b971fd7db646",
    "1a7b7cde-5bdd-40c2-8771-25ce32f26e78");
INSERT INTO GD_LS
    VALUES ("c78816c0-1d71-4d2d-bb40-bcfb2ed9d410",
    "cc3d9222-c7db-401f-88cb-b2912a95b268",
    "1a7b7cde-5bdd-40c2-8771-25ce32f26e78",
    "90d8d349-9729-407e-a54c-85ea0e9170f6",
    "094fa291-d349-45b9-8bc8-9f2cdbf81794");
INSERT INTO DIM_WAY
    VALUES ("b66f047f-0b04-44f7-b2cd-fb53b1e37ab2",
    613.000000,
    96.000000,
    "cc3d9222-c7db-401f-88cb-b2912a95b268",
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_WAY
    VALUES ("094fa291-d349-45b9-8bc8-9f2cdbf81794",
    497.000000,
    265.000000,
    "cc3d9222-c7db-401f-88cb-b2912a95b268",
    "00000000-0000-0000-0000-000000000000",
    "b66f047f-0b04-44f7-b2cd-fb53b1e37ab2");
INSERT INTO DIM_WAY
    VALUES ("a03d45c1-af19-4e1d-ab1a-ea1c829cf0c3",
    663.000000,
    96.000000,
    "cc3d9222-c7db-401f-88cb-b2912a95b268",
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_WAY
    VALUES ("49846951-7ed1-4c03-9406-bcd3ff7145d5",
    663.000000,
    324.000000,
    "cc3d9222-c7db-401f-88cb-b2912a95b268",
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_WAY
    VALUES ("90d8d349-9729-407e-a54c-85ea0e9170f6",
    497.000000,
    324.000000,
    "cc3d9222-c7db-401f-88cb-b2912a95b268",
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_GE
    VALUES (0.000000,
    0.000000,
    "cc3d9222-c7db-401f-88cb-b2912a95b268",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("cc3d9222-c7db-401f-88cb-b2912a95b268",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_CON
    VALUES ("2f920c1c-7f9d-4a65-9326-b971fd7db646",
    588.000000,
    324.000000,
    "cc3d9222-c7db-401f-88cb-b2912a95b268");
INSERT INTO DIM_ED
    VALUES ("68bec42f-065f-49e6-a5c4-1572b894956b",
    "ccdc9074-dbe9-4686-be0b-464c278fa7a5",
    "cc3d9222-c7db-401f-88cb-b2912a95b268");
INSERT INTO GD_GE
    VALUES ("a7c794aa-76d0-4ded-b2f5-374559ef8a3c",
    "47f372d5-f768-4a0a-94f3-341d16ad507d",
    "64f50cf1-3265-4c67-8b20-8f67c6584598",
    21,
    0,
    'Test::Stimuli::Assoc');
INSERT INTO GD_SHP
    VALUES ("a7c794aa-76d0-4ded-b2f5-374559ef8a3c");
INSERT INTO GD_NCS
    VALUES ("a7c794aa-76d0-4ded-b2f5-374559ef8a3c");
INSERT INTO DIM_ND
    VALUES (229.000000,
    121.000000,
    "a7c794aa-76d0-4ded-b2f5-374559ef8a3c");
INSERT INTO DIM_GE
    VALUES (420.000000,
    384.000000,
    "a7c794aa-76d0-4ded-b2f5-374559ef8a3c",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("a7c794aa-76d0-4ded-b2f5-374559ef8a3c",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_CON
    VALUES ("aa81276a-ee69-4ceb-8116-2edc77a68e1e",
    588.000000,
    384.000000,
    "a7c794aa-76d0-4ded-b2f5-374559ef8a3c");
INSERT INTO GD_GE
    VALUES ("2e92522d-a662-4d14-a06a-02894f9a222c",
    "47f372d5-f768-4a0a-94f3-341d16ad507d",
    "83517940-72ca-47ec-ad7d-a04d06f560b6",
    34,
    0,
    'Test::Stimuli::R1::Assoc');
INSERT INTO GD_CON
    VALUES ("2e92522d-a662-4d14-a06a-02894f9a222c",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO GD_CTXT
    VALUES ("048e856f-5889-4582-964b-6faefe1a19a2",
    "2e92522d-a662-4d14-a06a-02894f9a222c",
    1,
    0.000000,
    0.000000);
INSERT INTO DIM_ND
    VALUES (0.000000,
    0.000000,
    "048e856f-5889-4582-964b-6faefe1a19a2");
INSERT INTO DIM_GE
    VALUES (0.000000,
    0.000000,
    "048e856f-5889-4582-964b-6faefe1a19a2",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("048e856f-5889-4582-964b-6faefe1a19a2",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO GD_CTXT
    VALUES ("42440c46-073b-4d33-98e9-f2a7da71e2e6",
    "2e92522d-a662-4d14-a06a-02894f9a222c",
    3,
    0.000000,
    0.000000);
INSERT INTO DIM_ND
    VALUES (0.000000,
    0.000000,
    "42440c46-073b-4d33-98e9-f2a7da71e2e6");
INSERT INTO DIM_GE
    VALUES (0.000000,
    0.000000,
    "42440c46-073b-4d33-98e9-f2a7da71e2e6",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("42440c46-073b-4d33-98e9-f2a7da71e2e6",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO GD_CTXT
    VALUES ("969134f8-f96a-4538-b2f6-1be6db77bfbf",
    "2e92522d-a662-4d14-a06a-02894f9a222c",
    2,
    0.000000,
    0.000000);
INSERT INTO DIM_ND
    VALUES (0.000000,
    0.000000,
    "969134f8-f96a-4538-b2f6-1be6db77bfbf");
INSERT INTO DIM_GE
    VALUES (0.000000,
    0.000000,
    "969134f8-f96a-4538-b2f6-1be6db77bfbf",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("969134f8-f96a-4538-b2f6-1be6db77bfbf",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO GD_LS
    VALUES ("a930d008-5e21-4e59-b0a5-816b0d299205",
    "2e92522d-a662-4d14-a06a-02894f9a222c",
    "00000000-0000-0000-0000-000000000000",
    "c7448b4b-a973-4321-a260-138ce3e1e283",
    "ba3d6a75-65f0-494d-9079-15c793380d91");
INSERT INTO DIM_WAY
    VALUES ("c7448b4b-a973-4321-a260-138ce3e1e283",
    588.000000,
    384.000000,
    "2e92522d-a662-4d14-a06a-02894f9a222c",
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_WAY
    VALUES ("ba3d6a75-65f0-494d-9079-15c793380d91",
    588.000000,
    324.000000,
    "2e92522d-a662-4d14-a06a-02894f9a222c",
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_GE
    VALUES (0.000000,
    0.000000,
    "2e92522d-a662-4d14-a06a-02894f9a222c",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("2e92522d-a662-4d14-a06a-02894f9a222c",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ED
    VALUES ("aa81276a-ee69-4ceb-8116-2edc77a68e1e",
    "2f920c1c-7f9d-4a65-9326-b971fd7db646",
    "2e92522d-a662-4d14-a06a-02894f9a222c");
INSERT INTO GD_GE
    VALUES ("302cadae-7055-4e33-a0fe-654d71848985",
    "47f372d5-f768-4a0a-94f3-341d16ad507d",
    "e38009f0-429b-474c-8dc9-a73076783263",
    12,
    0,
    'Test::Stimuli::Architecture');
INSERT INTO GD_SHP
    VALUES ("302cadae-7055-4e33-a0fe-654d71848985");
INSERT INTO GD_NCS
    VALUES ("302cadae-7055-4e33-a0fe-654d71848985");
INSERT INTO DIM_ND
    VALUES (200.000000,
    150.000000,
    "302cadae-7055-4e33-a0fe-654d71848985");
INSERT INTO DIM_GE
    VALUES (876.000000,
    108.000000,
    "302cadae-7055-4e33-a0fe-654d71848985",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("302cadae-7055-4e33-a0fe-654d71848985",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO GD_GE
    VALUES ("3463fd6a-5bb3-4a21-b855-fecba1c785ee",
    "47f372d5-f768-4a0a-94f3-341d16ad507d",
    "770ebc2c-a252-4f4a-8f8b-d6d669a3c690",
    12,
    0,
    'Test::Stimuli::Logging');
INSERT INTO GD_SHP
    VALUES ("3463fd6a-5bb3-4a21-b855-fecba1c785ee");
INSERT INTO GD_NCS
    VALUES ("3463fd6a-5bb3-4a21-b855-fecba1c785ee");
INSERT INTO DIM_ND
    VALUES (200.000000,
    150.000000,
    "3463fd6a-5bb3-4a21-b855-fecba1c785ee");
INSERT INTO DIM_GE
    VALUES (1096.000000,
    108.000000,
    "3463fd6a-5bb3-4a21-b855-fecba1c785ee",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("3463fd6a-5bb3-4a21-b855-fecba1c785ee",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO GD_GE
    VALUES ("c73d68fc-3e94-416e-8275-e86ceadceadf",
    "47f372d5-f768-4a0a-94f3-341d16ad507d",
    "6f37183c-b5c6-4a88-a6a5-22d58f5889f1",
    12,
    0,
    'Test::Stimuli::Time');
INSERT INTO GD_SHP
    VALUES ("c73d68fc-3e94-416e-8275-e86ceadceadf");
INSERT INTO GD_NCS
    VALUES ("c73d68fc-3e94-416e-8275-e86ceadceadf");
INSERT INTO DIM_ND
    VALUES (200.000000,
    150.000000,
    "c73d68fc-3e94-416e-8275-e86ceadceadf");
INSERT INTO DIM_GE
    VALUES (1316.000000,
    108.000000,
    "c73d68fc-3e94-416e-8275-e86ceadceadf",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("c73d68fc-3e94-416e-8275-e86ceadceadf",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO GD_GE
    VALUES ("7fc12262-2a21-4611-ac0b-df4abc259481",
    "47f372d5-f768-4a0a-94f3-341d16ad507d",
    "53446f65-84b1-424b-bc68-cf0164d24a57",
    21,
    0,
    'Test::Stimuli::Other_Class');
INSERT INTO GD_SHP
    VALUES ("7fc12262-2a21-4611-ac0b-df4abc259481");
INSERT INTO GD_NCS
    VALUES ("7fc12262-2a21-4611-ac0b-df4abc259481");
INSERT INTO DIM_ND
    VALUES (240.000000,
    144.000000,
    "7fc12262-2a21-4611-ac0b-df4abc259481");
INSERT INTO DIM_GE
    VALUES (84.000000,
    432.000000,
    "7fc12262-2a21-4611-ac0b-df4abc259481",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("7fc12262-2a21-4611-ac0b-df4abc259481",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_CON
    VALUES ("eafb3f5c-266f-49f5-ad9c-ac834866f6cb",
    204.000000,
    432.000000,
    "7fc12262-2a21-4611-ac0b-df4abc259481");
INSERT INTO GD_GE
    VALUES ("e0aa0de1-3cf6-4a01-9248-d8fa9e666c45",
    "47f372d5-f768-4a0a-94f3-341d16ad507d",
    "749e0026-f26e-4df3-a33c-1a16c865d54a",
    24,
    0,
    'Test::Stimuli::R2');
INSERT INTO GD_CON
    VALUES ("e0aa0de1-3cf6-4a01-9248-d8fa9e666c45",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO GD_CTXT
    VALUES ("c701e9d4-7d03-44a0-aec1-89d991dba745",
    "e0aa0de1-3cf6-4a01-9248-d8fa9e666c45",
    1,
    0.000000,
    0.000000);
INSERT INTO DIM_ND
    VALUES (0.000000,
    0.000000,
    "c701e9d4-7d03-44a0-aec1-89d991dba745");
INSERT INTO DIM_GE
    VALUES (0.000000,
    0.000000,
    "c701e9d4-7d03-44a0-aec1-89d991dba745",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("c701e9d4-7d03-44a0-aec1-89d991dba745",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO GD_CTXT
    VALUES ("8826ea45-bf5e-4752-8cc1-48dee667ff93",
    "e0aa0de1-3cf6-4a01-9248-d8fa9e666c45",
    3,
    0.000000,
    0.000000);
INSERT INTO DIM_ND
    VALUES (0.000000,
    0.000000,
    "8826ea45-bf5e-4752-8cc1-48dee667ff93");
INSERT INTO DIM_GE
    VALUES (221.000000,
    326.000000,
    "8826ea45-bf5e-4752-8cc1-48dee667ff93",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("8826ea45-bf5e-4752-8cc1-48dee667ff93",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO GD_CTXT
    VALUES ("a1b8bbbf-f8a6-42ca-a872-d8bea4b08641",
    "e0aa0de1-3cf6-4a01-9248-d8fa9e666c45",
    2,
    0.000000,
    0.000000);
INSERT INTO DIM_ND
    VALUES (0.000000,
    0.000000,
    "a1b8bbbf-f8a6-42ca-a872-d8bea4b08641");
INSERT INTO DIM_GE
    VALUES (0.000000,
    0.000000,
    "a1b8bbbf-f8a6-42ca-a872-d8bea4b08641",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("a1b8bbbf-f8a6-42ca-a872-d8bea4b08641",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO GD_LS
    VALUES ("67663959-4ce5-47d4-b0f5-e518522bc1ce",
    "e0aa0de1-3cf6-4a01-9248-d8fa9e666c45",
    "00000000-0000-0000-0000-000000000000",
    "71236bd3-9a44-46bd-9304-145f2fb06270",
    "ed8de97e-3217-46f5-9971-24e824b18fb6");
INSERT INTO DIM_WAY
    VALUES ("71236bd3-9a44-46bd-9304-145f2fb06270",
    204.000000,
    432.000000,
    "e0aa0de1-3cf6-4a01-9248-d8fa9e666c45",
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_WAY
    VALUES ("ed8de97e-3217-46f5-9971-24e824b18fb6",
    204.000000,
    265.000000,
    "e0aa0de1-3cf6-4a01-9248-d8fa9e666c45",
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_GE
    VALUES (0.000000,
    0.000000,
    "e0aa0de1-3cf6-4a01-9248-d8fa9e666c45",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("e0aa0de1-3cf6-4a01-9248-d8fa9e666c45",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ED
    VALUES ("eafb3f5c-266f-49f5-ad9c-ac834866f6cb",
    "ec7b54a2-3ed3-4f7a-8d3d-5ae469f6d4d8",
    "e0aa0de1-3cf6-4a01-9248-d8fa9e666c45");
INSERT INTO GD_GE
    VALUES ("2d64b6db-f30f-4636-a1cb-7347d1a4d6aa",
    "47f372d5-f768-4a0a-94f3-341d16ad507d",
    "0065df20-dd20-47f8-80fa-f2a356522d79",
    52,
    0,
    'Test::Stimuli::My_Enum');
INSERT INTO GD_SHP
    VALUES ("2d64b6db-f30f-4636-a1cb-7347d1a4d6aa");
INSERT INTO GD_NCS
    VALUES ("2d64b6db-f30f-4636-a1cb-7347d1a4d6aa");
INSERT INTO DIM_ND
    VALUES (200.000000,
    150.000000,
    "2d64b6db-f30f-4636-a1cb-7347d1a4d6aa");
INSERT INTO DIM_GE
    VALUES (1536.000000,
    108.000000,
    "2d64b6db-f30f-4636-a1cb-7347d1a4d6aa",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("2d64b6db-f30f-4636-a1cb-7347d1a4d6aa",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO GD_GE
    VALUES ("12d256e1-6472-4c90-bfe5-66df689bb0d6",
    "47f372d5-f768-4a0a-94f3-341d16ad507d",
    "0eff6918-06c2-4e6d-ade0-a89e852c4628",
    109,
    0,
    'Test::Stimuli::My_Constants');
INSERT INTO GD_SHP
    VALUES ("12d256e1-6472-4c90-bfe5-66df689bb0d6");
INSERT INTO GD_NCS
    VALUES ("12d256e1-6472-4c90-bfe5-66df689bb0d6");
INSERT INTO DIM_ND
    VALUES (200.000000,
    150.000000,
    "12d256e1-6472-4c90-bfe5-66df689bb0d6");
INSERT INTO DIM_GE
    VALUES (1756.000000,
    108.000000,
    "12d256e1-6472-4c90-bfe5-66df689bb0d6",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("12d256e1-6472-4c90-bfe5-66df689bb0d6",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO GD_GE
    VALUES ("fc91b55d-4cbd-4960-9e6c-6913808d263b",
    "47f372d5-f768-4a0a-94f3-341d16ad507d",
    "8d35d15f-ff91-47a8-a970-ec892e1f2714",
    101,
    0,
    'Test::Stimuli::My_Struct');
INSERT INTO GD_SHP
    VALUES ("fc91b55d-4cbd-4960-9e6c-6913808d263b");
INSERT INTO GD_NCS
    VALUES ("fc91b55d-4cbd-4960-9e6c-6913808d263b");
INSERT INTO DIM_ND
    VALUES (200.000000,
    150.000000,
    "fc91b55d-4cbd-4960-9e6c-6913808d263b");
INSERT INTO DIM_GE
    VALUES (1976.000000,
    108.000000,
    "fc91b55d-4cbd-4960-9e6c-6913808d263b",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("fc91b55d-4cbd-4960-9e6c-6913808d263b",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_DIA
    VALUES ("47f372d5-f768-4a0a-94f3-341d16ad507d",
    '',
    1.000000,
    0.000000,
    0.000000,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO PE_PE
    VALUES ("7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    1,
    "96ec2ddc-da38-40da-8372-025532bfdb1d",
    "00000000-0000-0000-0000-000000000000",
    4);
INSERT INTO O_OBJ
    VALUES ("7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    'Class',
    1,
    'Class',
    '',
    "00000000-0000-0000-0000-000000000000");
INSERT INTO O_TFR
    VALUES ("e758f1a3-58a7-4b23-ab94-1f532641886d",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    'Instance_Based_Operation',
    '',
    "ba5eda7a-def5-0000-0000-000000000002",
    1,
    'return param.P1 + param.P2 + self.Derived_Attribute;',
    1,
    '',
    "00000000-0000-0000-0000-000000000000",
    0);
INSERT INTO O_TPARM
    VALUES ("983f2053-433b-4237-bb78-e1f6cafdbc9b",
    "e758f1a3-58a7-4b23-ab94-1f532641886d",
    'P1',
    "ba5eda7a-def5-0000-0000-000000000002",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO O_TPARM
    VALUES ("2faf254a-033e-416a-892e-8258b0c5163c",
    "e758f1a3-58a7-4b23-ab94-1f532641886d",
    'P2',
    "ba5eda7a-def5-0000-0000-000000000002",
    0,
    '',
    "983f2053-433b-4237-bb78-e1f6cafdbc9b",
    '');
INSERT INTO O_TFR
    VALUES ("f7e47536-70cf-4c6d-8224-1c06e6dc43d5",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    'Class_Based_Operation',
    '',
    "ba5eda7a-def5-0000-0000-000000000002",
    0,
    'return param.P1 + param.P2;',
    1,
    '',
    "e758f1a3-58a7-4b23-ab94-1f532641886d",
    0);
INSERT INTO O_TPARM
    VALUES ("9b8a6a4b-c46e-4ee4-b2bf-ee151a370682",
    "f7e47536-70cf-4c6d-8224-1c06e6dc43d5",
    'P1',
    "ba5eda7a-def5-0000-0000-000000000002",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO O_TPARM
    VALUES ("436f7f35-a505-4202-98fb-9137182e00d9",
    "f7e47536-70cf-4c6d-8224-1c06e6dc43d5",
    'P2',
    "ba5eda7a-def5-0000-0000-000000000002",
    0,
    '',
    "9b8a6a4b-c46e-4ee4-b2bf-ee151a370682",
    '');
INSERT INTO O_TFR
    VALUES ("984c087c-6886-4ed5-b58c-3aac38dec6b2",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    'Transform_Function',
    '',
    "ba5eda7a-def5-0000-0000-000000000000",
    0,
    '',
    3,
    '',
    "f7e47536-70cf-4c6d-8224-1c06e6dc43d5",
    0);
INSERT INTO O_NBATTR
    VALUES ("429f668f-92bd-4661-a074-7328a5d4e4ba",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9");
INSERT INTO O_BATTR
    VALUES ("429f668f-92bd-4661-a074-7328a5d4e4ba",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9");
INSERT INTO O_ATTR
    VALUES ("429f668f-92bd-4661-a074-7328a5d4e4ba",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    "00000000-0000-0000-0000-000000000000",
    'ID',
    '',
    '',
    'ID',
    0,
    "ba5eda7a-def5-0000-0000-000000000005",
    '',
    '');
INSERT INTO O_DBATTR
    VALUES ("b8161e1a-e49e-4c4f-8938-289cb6ebe107",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    'self.Derived_Attribute = 42;',
    1,
    0);
INSERT INTO O_BATTR
    VALUES ("b8161e1a-e49e-4c4f-8938-289cb6ebe107",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9");
INSERT INTO O_ATTR
    VALUES ("b8161e1a-e49e-4c4f-8938-289cb6ebe107",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    "429f668f-92bd-4661-a074-7328a5d4e4ba",
    'Derived_Attribute',
    '',
    '',
    'Derived_Attribute',
    0,
    "ba5eda7a-def5-0000-0000-000000000002",
    '',
    '');
INSERT INTO O_ID
    VALUES (0,
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9");
INSERT INTO O_OIDA
    VALUES ("429f668f-92bd-4661-a074-7328a5d4e4ba",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    0,
    'ID');
INSERT INTO O_ID
    VALUES (1,
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9");
INSERT INTO O_ID
    VALUES (2,
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9");
INSERT INTO PE_PE
    VALUES ("83517940-72ca-47ec-ad7d-a04d06f560b6",
    1,
    "96ec2ddc-da38-40da-8372-025532bfdb1d",
    "00000000-0000-0000-0000-000000000000",
    9);
INSERT INTO R_REL
    VALUES ("83517940-72ca-47ec-ad7d-a04d06f560b6",
    1,
    '',
    "00000000-0000-0000-0000-000000000000");
INSERT INTO R_ASSOC
    VALUES ("83517940-72ca-47ec-ad7d-a04d06f560b6");
INSERT INTO R_AONE
    VALUES ("7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    "83517940-72ca-47ec-ad7d-a04d06f560b6",
    "a20ed88b-6494-4ecf-acf9-171949cb909c",
    0,
    1,
    'one');
INSERT INTO O_RTIDA
    VALUES ("429f668f-92bd-4661-a074-7328a5d4e4ba",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    0,
    "83517940-72ca-47ec-ad7d-a04d06f560b6",
    "a20ed88b-6494-4ecf-acf9-171949cb909c");
INSERT INTO R_RTO
    VALUES ("7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    "83517940-72ca-47ec-ad7d-a04d06f560b6",
    "a20ed88b-6494-4ecf-acf9-171949cb909c",
    0);
INSERT INTO R_OIR
    VALUES ("7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    "83517940-72ca-47ec-ad7d-a04d06f560b6",
    "a20ed88b-6494-4ecf-acf9-171949cb909c",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO R_AOTH
    VALUES ("7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    "83517940-72ca-47ec-ad7d-a04d06f560b6",
    "1721e766-d80d-4750-b780-e82bda8e3bc3",
    0,
    1,
    'other');
INSERT INTO O_RTIDA
    VALUES ("429f668f-92bd-4661-a074-7328a5d4e4ba",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    0,
    "83517940-72ca-47ec-ad7d-a04d06f560b6",
    "1721e766-d80d-4750-b780-e82bda8e3bc3");
INSERT INTO R_RTO
    VALUES ("7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    "83517940-72ca-47ec-ad7d-a04d06f560b6",
    "1721e766-d80d-4750-b780-e82bda8e3bc3",
    0);
INSERT INTO R_OIR
    VALUES ("7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    "83517940-72ca-47ec-ad7d-a04d06f560b6",
    "1721e766-d80d-4750-b780-e82bda8e3bc3",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO R_ASSR
    VALUES ("64f50cf1-3265-4c67-8b20-8f67c6584598",
    "83517940-72ca-47ec-ad7d-a04d06f560b6",
    "d129b4a8-22ca-4360-a33f-f384fe0cd6f6",
    0);
INSERT INTO R_RGO
    VALUES ("64f50cf1-3265-4c67-8b20-8f67c6584598",
    "83517940-72ca-47ec-ad7d-a04d06f560b6",
    "d129b4a8-22ca-4360-a33f-f384fe0cd6f6");
INSERT INTO R_OIR
    VALUES ("64f50cf1-3265-4c67-8b20-8f67c6584598",
    "83517940-72ca-47ec-ad7d-a04d06f560b6",
    "d129b4a8-22ca-4360-a33f-f384fe0cd6f6",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO PE_PE
    VALUES ("64f50cf1-3265-4c67-8b20-8f67c6584598",
    1,
    "96ec2ddc-da38-40da-8372-025532bfdb1d",
    "00000000-0000-0000-0000-000000000000",
    4);
INSERT INTO O_OBJ
    VALUES ("64f50cf1-3265-4c67-8b20-8f67c6584598",
    'Assoc',
    2,
    'Assoc',
    '',
    "00000000-0000-0000-0000-000000000000");
INSERT INTO O_REF
    VALUES ("64f50cf1-3265-4c67-8b20-8f67c6584598",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    0,
    "429f668f-92bd-4661-a074-7328a5d4e4ba",
    "83517940-72ca-47ec-ad7d-a04d06f560b6",
    "d129b4a8-22ca-4360-a33f-f384fe0cd6f6",
    "a20ed88b-6494-4ecf-acf9-171949cb909c",
    "2261d0fb-67d6-49cc-9796-9ce0d984e77e",
    "7b2cfbf2-323d-4192-8e10-821fa833cea0",
    "00000000-0000-0000-0000-000000000000",
    0,
    '',
    'Class',
    'ID',
    'R1.''one''');
INSERT INTO O_RATTR
    VALUES ("2261d0fb-67d6-49cc-9796-9ce0d984e77e",
    "64f50cf1-3265-4c67-8b20-8f67c6584598",
    "429f668f-92bd-4661-a074-7328a5d4e4ba",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    1,
    'ID');
INSERT INTO O_ATTR
    VALUES ("2261d0fb-67d6-49cc-9796-9ce0d984e77e",
    "64f50cf1-3265-4c67-8b20-8f67c6584598",
    "00000000-0000-0000-0000-000000000000",
    'One_ID',
    '',
    'One_',
    'ID',
    1,
    "ba5eda7a-def5-0000-0000-000000000002",
    '',
    '');
INSERT INTO O_REF
    VALUES ("64f50cf1-3265-4c67-8b20-8f67c6584598",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    0,
    "429f668f-92bd-4661-a074-7328a5d4e4ba",
    "83517940-72ca-47ec-ad7d-a04d06f560b6",
    "d129b4a8-22ca-4360-a33f-f384fe0cd6f6",
    "1721e766-d80d-4750-b780-e82bda8e3bc3",
    "057fa7d0-fe76-4dbc-85e4-5ebd0510d10d",
    "11832eed-df45-4211-aea8-cd9a9d42a825",
    "00000000-0000-0000-0000-000000000000",
    0,
    '',
    'Class',
    'ID',
    'R1.''other''');
INSERT INTO O_RATTR
    VALUES ("057fa7d0-fe76-4dbc-85e4-5ebd0510d10d",
    "64f50cf1-3265-4c67-8b20-8f67c6584598",
    "429f668f-92bd-4661-a074-7328a5d4e4ba",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    1,
    'ID');
INSERT INTO O_ATTR
    VALUES ("057fa7d0-fe76-4dbc-85e4-5ebd0510d10d",
    "64f50cf1-3265-4c67-8b20-8f67c6584598",
    "2261d0fb-67d6-49cc-9796-9ce0d984e77e",
    'Other_ID',
    '',
    'Other_',
    'ID',
    1,
    "ba5eda7a-def5-0000-0000-000000000002",
    '',
    '');
INSERT INTO O_ID
    VALUES (0,
    "64f50cf1-3265-4c67-8b20-8f67c6584598");
INSERT INTO O_OIDA
    VALUES ("2261d0fb-67d6-49cc-9796-9ce0d984e77e",
    "64f50cf1-3265-4c67-8b20-8f67c6584598",
    0,
    'One_ID');
INSERT INTO O_OIDA
    VALUES ("057fa7d0-fe76-4dbc-85e4-5ebd0510d10d",
    "64f50cf1-3265-4c67-8b20-8f67c6584598",
    0,
    'Other_ID');
INSERT INTO O_ID
    VALUES (1,
    "64f50cf1-3265-4c67-8b20-8f67c6584598");
INSERT INTO O_ID
    VALUES (2,
    "64f50cf1-3265-4c67-8b20-8f67c6584598");
INSERT INTO PE_PE
    VALUES ("9685d027-a90e-4cc6-8ec7-e0e354a5d7a0",
    1,
    "96ec2ddc-da38-40da-8372-025532bfdb1d",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("9685d027-a90e-4cc6-8ec7-e0e354a5d7a0",
    "00000000-0000-0000-0000-000000000000",
    'Function',
    '',
    '',
    "ba5eda7a-def5-0000-0000-000000000002",
    3,
    '',
    0);
INSERT INTO S_SPARM
    VALUES ("7f918896-4e70-4a91-beff-11adebc48e30",
    "9685d027-a90e-4cc6-8ec7-e0e354a5d7a0",
    'P1',
    "ba5eda7a-def5-0000-0000-000000000002",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_SPARM
    VALUES ("a2aaf229-5680-4349-ae5d-343269d27a3e",
    "9685d027-a90e-4cc6-8ec7-e0e354a5d7a0",
    'P2',
    "ba5eda7a-def5-0000-0000-000000000002",
    0,
    '',
    "7f918896-4e70-4a91-beff-11adebc48e30",
    '');
INSERT INTO PE_PE
    VALUES ("e38009f0-429b-474c-8dc9-a73076783263",
    1,
    "96ec2ddc-da38-40da-8372-025532bfdb1d",
    "00000000-0000-0000-0000-000000000000",
    5);
INSERT INTO S_EE
    VALUES ("e38009f0-429b-474c-8dc9-a73076783263",
    'Architecture',
    '',
    'ARCH',
    "00000000-0000-0000-0000-000000000000",
    '',
    'Architecture',
    1);
INSERT INTO S_BRG
    VALUES ("7219f7b0-0397-40dc-97f6-de0a41208412",
    "e38009f0-429b-474c-8dc9-a73076783263",
    'shutdown',
    '',
    0,
    "ba5eda7a-def5-0000-0000-000000000000",
    'control stop;',
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("770ebc2c-a252-4f4a-8f8b-d6d669a3c690",
    1,
    "96ec2ddc-da38-40da-8372-025532bfdb1d",
    "00000000-0000-0000-0000-000000000000",
    5);
INSERT INTO S_EE
    VALUES ("770ebc2c-a252-4f4a-8f8b-d6d669a3c690",
    'Logging',
    '',
    'LOG',
    "00000000-0000-0000-0000-000000000000",
    '',
    'Logging',
    1);
INSERT INTO S_BRG
    VALUES ("61fe08cd-9cf3-4023-a487-7aa292e7a20e",
    "770ebc2c-a252-4f4a-8f8b-d6d669a3c690",
    'LogSuccess',
    '',
    0,
    "ba5eda7a-def5-0000-0000-000000000000",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("c6072874-c495-4730-b5ec-5d5f1549bf1a",
    "61fe08cd-9cf3-4023-a487-7aa292e7a20e",
    'message',
    "ba5eda7a-def5-0000-0000-000000000004",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_BRG
    VALUES ("d3998ddd-97b6-4fae-b749-e4e9c6e3936d",
    "770ebc2c-a252-4f4a-8f8b-d6d669a3c690",
    'LogFailure',
    '',
    0,
    "ba5eda7a-def5-0000-0000-000000000000",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("a5b0512d-91d6-4c84-8265-c2422917dbd0",
    "d3998ddd-97b6-4fae-b749-e4e9c6e3936d",
    'message',
    "ba5eda7a-def5-0000-0000-000000000004",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_BRG
    VALUES ("9632064d-37ed-4279-afb5-d197096dca00",
    "770ebc2c-a252-4f4a-8f8b-d6d669a3c690",
    'LogInfo',
    '',
    0,
    "ba5eda7a-def5-0000-0000-000000000000",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("68318d83-f022-4f1f-8362-19701df14b42",
    "9632064d-37ed-4279-afb5-d197096dca00",
    'message',
    "ba5eda7a-def5-0000-0000-000000000004",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_BRG
    VALUES ("3c3863c6-d669-4c50-b129-48665a57b837",
    "770ebc2c-a252-4f4a-8f8b-d6d669a3c690",
    'LogDate',
    '',
    0,
    "ba5eda7a-def5-0000-0000-000000000000",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("99c0c5b7-9454-4438-963a-44cfabd43fdc",
    "3c3863c6-d669-4c50-b129-48665a57b837",
    'd',
    "ba5eda7a-def5-0000-0000-00000000000e",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_BPARM
    VALUES ("ad473ace-130f-4bed-9991-80821413bcfa",
    "3c3863c6-d669-4c50-b129-48665a57b837",
    'message',
    "ba5eda7a-def5-0000-0000-000000000004",
    0,
    '',
    "99c0c5b7-9454-4438-963a-44cfabd43fdc",
    '');
INSERT INTO S_BRG
    VALUES ("e8ecbf2e-2cd2-492c-aee8-0ae74a9e4f5d",
    "770ebc2c-a252-4f4a-8f8b-d6d669a3c690",
    'LogTime',
    '',
    0,
    "ba5eda7a-def5-0000-0000-000000000000",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("153a7d76-d2ca-40fc-99ce-c1069ea1a6f8",
    "e8ecbf2e-2cd2-492c-aee8-0ae74a9e4f5d",
    't',
    "ba5eda7a-def5-0000-0000-000000000010",
    0,
    '',
    "924677ab-5703-4dd9-bf11-62cd0f2a7bd5",
    '');
INSERT INTO S_BPARM
    VALUES ("924677ab-5703-4dd9-bf11-62cd0f2a7bd5",
    "e8ecbf2e-2cd2-492c-aee8-0ae74a9e4f5d",
    'message',
    "ba5eda7a-def5-0000-0000-000000000004",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_BRG
    VALUES ("6f3d4410-eb6d-4a2d-bfb4-27a52bb964d7",
    "770ebc2c-a252-4f4a-8f8b-d6d669a3c690",
    'LogReal',
    '',
    0,
    "ba5eda7a-def5-0000-0000-000000000000",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("eac566ab-d8d1-4ef1-a80f-85870d0f2e72",
    "6f3d4410-eb6d-4a2d-bfb4-27a52bb964d7",
    'r',
    "ba5eda7a-def5-0000-0000-000000000003",
    0,
    '',
    "3dc0dc76-4d72-4d8d-aaec-d38d894becc3",
    '');
INSERT INTO S_BPARM
    VALUES ("3dc0dc76-4d72-4d8d-aaec-d38d894becc3",
    "6f3d4410-eb6d-4a2d-bfb4-27a52bb964d7",
    'message',
    "ba5eda7a-def5-0000-0000-000000000004",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_BRG
    VALUES ("cbf6251f-5367-4bad-a673-a9a609eb4e53",
    "770ebc2c-a252-4f4a-8f8b-d6d669a3c690",
    'LogInteger',
    '',
    0,
    "ba5eda7a-def5-0000-0000-000000000000",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("cc97ce8d-7f54-465b-9998-ff94c43684cf",
    "cbf6251f-5367-4bad-a673-a9a609eb4e53",
    'message',
    "ba5eda7a-def5-0000-0000-000000000002",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO PE_PE
    VALUES ("6f37183c-b5c6-4a88-a6a5-22d58f5889f1",
    1,
    "96ec2ddc-da38-40da-8372-025532bfdb1d",
    "00000000-0000-0000-0000-000000000000",
    5);
INSERT INTO S_EE
    VALUES ("6f37183c-b5c6-4a88-a6a5-22d58f5889f1",
    'Time',
    'The Time external entity provides date, timestamp, and timer related operations.',
    'TIM',
    "00000000-0000-0000-0000-000000000000",
    '',
    'Time',
    1);
INSERT INTO S_BRG
    VALUES ("7170e958-105e-46a5-abe5-7f87287f3984",
    "6f37183c-b5c6-4a88-a6a5-22d58f5889f1",
    'current_date',
    '',
    1,
    "ba5eda7a-def5-0000-0000-00000000000e",
    '',
    1,
    '',
    0);
INSERT INTO S_BRG
    VALUES ("5c51f8f7-9ee4-4353-a408-7e1d773d7083",
    "6f37183c-b5c6-4a88-a6a5-22d58f5889f1",
    'create_date',
    '',
    1,
    "ba5eda7a-def5-0000-0000-00000000000e",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("7ac00be5-803f-4718-b33d-c37de04fc5fd",
    "5c51f8f7-9ee4-4353-a408-7e1d773d7083",
    'second',
    "ba5eda7a-def5-0000-0000-000000000002",
    0,
    '',
    "69ec20c5-d050-42fd-9cfd-b8bed00a9dfb",
    '');
INSERT INTO S_BPARM
    VALUES ("1e4627c5-8c62-4dc7-bc1b-37436e5d5bf3",
    "5c51f8f7-9ee4-4353-a408-7e1d773d7083",
    'minute',
    "ba5eda7a-def5-0000-0000-000000000002",
    0,
    '',
    "f8d0aa3c-a0a3-4208-9334-c796d06ad15a",
    '');
INSERT INTO S_BPARM
    VALUES ("f8d0aa3c-a0a3-4208-9334-c796d06ad15a",
    "5c51f8f7-9ee4-4353-a408-7e1d773d7083",
    'hour',
    "ba5eda7a-def5-0000-0000-000000000002",
    0,
    '',
    "65c22f3d-5b0d-4f67-a2dd-c0f7a0f40f31",
    '');
INSERT INTO S_BPARM
    VALUES ("65c22f3d-5b0d-4f67-a2dd-c0f7a0f40f31",
    "5c51f8f7-9ee4-4353-a408-7e1d773d7083",
    'day',
    "ba5eda7a-def5-0000-0000-000000000002",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_BPARM
    VALUES ("69ec20c5-d050-42fd-9cfd-b8bed00a9dfb",
    "5c51f8f7-9ee4-4353-a408-7e1d773d7083",
    'month',
    "ba5eda7a-def5-0000-0000-000000000002",
    0,
    '',
    "1e4627c5-8c62-4dc7-bc1b-37436e5d5bf3",
    '');
INSERT INTO S_BPARM
    VALUES ("e7d4f610-1a2d-4d22-978d-1738799e4cea",
    "5c51f8f7-9ee4-4353-a408-7e1d773d7083",
    'year',
    "ba5eda7a-def5-0000-0000-000000000002",
    0,
    '',
    "7ac00be5-803f-4718-b33d-c37de04fc5fd",
    '');
INSERT INTO S_BRG
    VALUES ("0441f231-1284-4094-aa46-5dee9c8b738f",
    "6f37183c-b5c6-4a88-a6a5-22d58f5889f1",
    'get_second',
    '',
    1,
    "ba5eda7a-def5-0000-0000-000000000002",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("fb50e6e5-09b0-4d0c-bde7-7a5c0d9fd0e8",
    "0441f231-1284-4094-aa46-5dee9c8b738f",
    'date',
    "ba5eda7a-def5-0000-0000-00000000000e",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_BRG
    VALUES ("a967695e-424d-43d6-979c-05c81a18883d",
    "6f37183c-b5c6-4a88-a6a5-22d58f5889f1",
    'get_minute',
    '',
    1,
    "ba5eda7a-def5-0000-0000-000000000002",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("846f87fe-15db-4e76-8e8e-fa5e207c78d3",
    "a967695e-424d-43d6-979c-05c81a18883d",
    'date',
    "ba5eda7a-def5-0000-0000-00000000000e",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_BRG
    VALUES ("f690ac85-7a78-450a-bbb0-86db7f6a7b09",
    "6f37183c-b5c6-4a88-a6a5-22d58f5889f1",
    'get_hour',
    '',
    1,
    "ba5eda7a-def5-0000-0000-000000000002",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("005b7517-8086-4cc4-91a9-94c5b1baa3ac",
    "f690ac85-7a78-450a-bbb0-86db7f6a7b09",
    'date',
    "ba5eda7a-def5-0000-0000-00000000000e",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_BRG
    VALUES ("f668b556-0ce1-4cc9-8c28-fc7640fafa7d",
    "6f37183c-b5c6-4a88-a6a5-22d58f5889f1",
    'get_day',
    '',
    1,
    "ba5eda7a-def5-0000-0000-000000000002",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("85aa9858-33df-4944-8caa-66bbbb9efc9d",
    "f668b556-0ce1-4cc9-8c28-fc7640fafa7d",
    'date',
    "ba5eda7a-def5-0000-0000-00000000000e",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_BRG
    VALUES ("1ca488a2-7e00-4d14-a33c-a392964c1105",
    "6f37183c-b5c6-4a88-a6a5-22d58f5889f1",
    'get_month',
    '',
    1,
    "ba5eda7a-def5-0000-0000-000000000002",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("35b5239a-eb3b-4d6f-9a85-0d202e9471f3",
    "1ca488a2-7e00-4d14-a33c-a392964c1105",
    'date',
    "ba5eda7a-def5-0000-0000-00000000000e",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_BRG
    VALUES ("e3caf312-3b09-47fd-843d-35df16332061",
    "6f37183c-b5c6-4a88-a6a5-22d58f5889f1",
    'get_year',
    '',
    1,
    "ba5eda7a-def5-0000-0000-000000000002",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("99c554c0-149e-4419-89be-87978653444f",
    "e3caf312-3b09-47fd-843d-35df16332061",
    'date',
    "ba5eda7a-def5-0000-0000-00000000000e",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_BRG
    VALUES ("73ca7c37-3ccd-4498-8bdd-735cf21f21f6",
    "6f37183c-b5c6-4a88-a6a5-22d58f5889f1",
    'current_clock',
    '',
    1,
    "ba5eda7a-def5-0000-0000-000000000010",
    '',
    1,
    '',
    0);
INSERT INTO S_BRG
    VALUES ("3aff102e-fb0d-49f1-b058-5692011d4547",
    "6f37183c-b5c6-4a88-a6a5-22d58f5889f1",
    'timer_start',
    'This bridge operation starts a timer set to expire in the specified number of
microseconds, generating the passed event upon expiration. Returns the instance
handle of the timer.',
    1,
    "ba5eda7a-def5-0000-0000-00000000000f",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("1e4b88e6-d7bd-44b3-b9a5-5e4b4e263652",
    "3aff102e-fb0d-49f1-b058-5692011d4547",
    'microseconds',
    "ba5eda7a-def5-0000-0000-000000000002",
    0,
    '',
    "87589024-8660-4248-9599-91be6b6cd684",
    '');
INSERT INTO S_BPARM
    VALUES ("87589024-8660-4248-9599-91be6b6cd684",
    "3aff102e-fb0d-49f1-b058-5692011d4547",
    'event_inst',
    "ba5eda7a-def5-0000-0000-00000000000a",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_BRG
    VALUES ("117f254c-2850-4253-b929-867f506ac3fe",
    "6f37183c-b5c6-4a88-a6a5-22d58f5889f1",
    'timer_start_recurring',
    'This bridge operation starts a timer set to expire in the specified number of
microseconds, generating the passed event upon expiration. Upon expiration, the
timer will be restarted and fire again in the specified number of microseconds
generating the passed event. This bridge operation returns the instance handle
of the timer.',
    1,
    "ba5eda7a-def5-0000-0000-00000000000f",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("90113d6f-cc00-49b4-979c-2e1e266d51c4",
    "117f254c-2850-4253-b929-867f506ac3fe",
    'microseconds',
    "ba5eda7a-def5-0000-0000-000000000002",
    0,
    '',
    "15253241-3d27-4b89-a5e7-ad1fd721e0e0",
    '');
INSERT INTO S_BPARM
    VALUES ("15253241-3d27-4b89-a5e7-ad1fd721e0e0",
    "117f254c-2850-4253-b929-867f506ac3fe",
    'event_inst',
    "ba5eda7a-def5-0000-0000-00000000000a",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_BRG
    VALUES ("23e76176-4a6d-4d95-8ee4-00190c9d69bb",
    "6f37183c-b5c6-4a88-a6a5-22d58f5889f1",
    'timer_remaining_time',
    'Returns the time remaining (in microseconds) for the passed timer instance. If
the timer has expired, a zero value is returned.',
    1,
    "ba5eda7a-def5-0000-0000-000000000002",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("37b23826-9cfc-4591-80de-b38559e09739",
    "23e76176-4a6d-4d95-8ee4-00190c9d69bb",
    'timer_inst_ref',
    "ba5eda7a-def5-0000-0000-00000000000f",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_BRG
    VALUES ("8e34546f-016d-44e9-bf83-09079f1ef3d2",
    "6f37183c-b5c6-4a88-a6a5-22d58f5889f1",
    'timer_reset_time',
    'This bridge operation attempts to set the passed existing timer to expire in
the specified number of microseconds. If the timer exists (that is, it has not
expired), a TRUE value is returned. If the timer no longer exists, a FALSE value
is returned.',
    1,
    "ba5eda7a-def5-0000-0000-000000000001",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("3640e433-1322-4ddc-a2ea-bb9a9aa8b716",
    "8e34546f-016d-44e9-bf83-09079f1ef3d2",
    'timer_inst_ref',
    "ba5eda7a-def5-0000-0000-00000000000f",
    0,
    '',
    "898578a1-a47b-43cd-b751-b9ee14c31b12",
    '');
INSERT INTO S_BPARM
    VALUES ("898578a1-a47b-43cd-b751-b9ee14c31b12",
    "8e34546f-016d-44e9-bf83-09079f1ef3d2",
    'microseconds',
    "ba5eda7a-def5-0000-0000-000000000002",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_BRG
    VALUES ("2d11503e-b9b3-4424-bc0e-e63fd1f7826d",
    "6f37183c-b5c6-4a88-a6a5-22d58f5889f1",
    'timer_add_time',
    'This bridge operation attempts to add the specified number of microseconds to a
passed existing timer. If the timer exists (that is, it has not expired), a TRUE
value is returned. If the timer no longer exists, a FALSE value is returned.',
    1,
    "ba5eda7a-def5-0000-0000-000000000001",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("c74fea9b-7bec-4074-a94d-d36a38ec7f7b",
    "2d11503e-b9b3-4424-bc0e-e63fd1f7826d",
    'timer_inst_ref',
    "ba5eda7a-def5-0000-0000-00000000000f",
    0,
    '',
    "814c3d46-0987-48b4-b81e-1f3711a3a026",
    '');
INSERT INTO S_BPARM
    VALUES ("814c3d46-0987-48b4-b81e-1f3711a3a026",
    "2d11503e-b9b3-4424-bc0e-e63fd1f7826d",
    'microseconds',
    "ba5eda7a-def5-0000-0000-000000000002",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_BRG
    VALUES ("3d225bb3-3e93-4136-aa66-840f43a4fc91",
    "6f37183c-b5c6-4a88-a6a5-22d58f5889f1",
    'timer_cancel',
    'This bridge operation cancels and deletes the passed timer instance. If the 
timer exists (that is, it had not expired), a TRUE value is returned. If the
timer no longer exists, a FALSE value is returned.',
    1,
    "ba5eda7a-def5-0000-0000-000000000001",
    '',
    1,
    '',
    0);
INSERT INTO S_BPARM
    VALUES ("fbbb00e3-6076-4b7e-a082-b90f7b7df417",
    "3d225bb3-3e93-4136-aa66-840f43a4fc91",
    'timer_inst_ref',
    "ba5eda7a-def5-0000-0000-00000000000f",
    0,
    '',
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO PE_PE
    VALUES ("53446f65-84b1-424b-bc68-cf0164d24a57",
    1,
    "96ec2ddc-da38-40da-8372-025532bfdb1d",
    "00000000-0000-0000-0000-000000000000",
    4);
INSERT INTO O_OBJ
    VALUES ("53446f65-84b1-424b-bc68-cf0164d24a57",
    'Other_Class',
    3,
    'Other_Class',
    '',
    "00000000-0000-0000-0000-000000000000");
INSERT INTO O_NBATTR
    VALUES ("e1e5b8ee-5304-4701-88fe-54f5f21e972e",
    "53446f65-84b1-424b-bc68-cf0164d24a57");
INSERT INTO O_BATTR
    VALUES ("e1e5b8ee-5304-4701-88fe-54f5f21e972e",
    "53446f65-84b1-424b-bc68-cf0164d24a57");
INSERT INTO O_ATTR
    VALUES ("e1e5b8ee-5304-4701-88fe-54f5f21e972e",
    "53446f65-84b1-424b-bc68-cf0164d24a57",
    "00000000-0000-0000-0000-000000000000",
    'ID',
    '',
    '',
    'ID',
    0,
    "ba5eda7a-def5-0000-0000-000000000005",
    '',
    '');
INSERT INTO O_REF
    VALUES ("53446f65-84b1-424b-bc68-cf0164d24a57",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    0,
    "429f668f-92bd-4661-a074-7328a5d4e4ba",
    "749e0026-f26e-4df3-a33c-1a16c865d54a",
    "6aad37f6-2c85-4cb8-991b-9d866a382f49",
    "54f4406e-145d-46f9-b866-d68d00b6a58f",
    "fbc0067c-bc8a-41d7-ae02-be016a67c320",
    "8faf711a-075c-43ac-958a-6d1f2106f49d",
    "00000000-0000-0000-0000-000000000000",
    0,
    '',
    'Class',
    'ID',
    'R2');
INSERT INTO O_RATTR
    VALUES ("fbc0067c-bc8a-41d7-ae02-be016a67c320",
    "53446f65-84b1-424b-bc68-cf0164d24a57",
    "429f668f-92bd-4661-a074-7328a5d4e4ba",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    1,
    'ID');
INSERT INTO O_ATTR
    VALUES ("fbc0067c-bc8a-41d7-ae02-be016a67c320",
    "53446f65-84b1-424b-bc68-cf0164d24a57",
    "e1e5b8ee-5304-4701-88fe-54f5f21e972e",
    'Class_ID',
    '',
    'Class_',
    'ID',
    1,
    "ba5eda7a-def5-0000-0000-000000000002",
    '',
    '');
INSERT INTO O_ID
    VALUES (0,
    "53446f65-84b1-424b-bc68-cf0164d24a57");
INSERT INTO O_OIDA
    VALUES ("e1e5b8ee-5304-4701-88fe-54f5f21e972e",
    "53446f65-84b1-424b-bc68-cf0164d24a57",
    0,
    'ID');
INSERT INTO O_ID
    VALUES (1,
    "53446f65-84b1-424b-bc68-cf0164d24a57");
INSERT INTO O_ID
    VALUES (2,
    "53446f65-84b1-424b-bc68-cf0164d24a57");
INSERT INTO PE_PE
    VALUES ("749e0026-f26e-4df3-a33c-1a16c865d54a",
    1,
    "96ec2ddc-da38-40da-8372-025532bfdb1d",
    "00000000-0000-0000-0000-000000000000",
    9);
INSERT INTO R_REL
    VALUES ("749e0026-f26e-4df3-a33c-1a16c865d54a",
    2,
    '',
    "00000000-0000-0000-0000-000000000000");
INSERT INTO R_SIMP
    VALUES ("749e0026-f26e-4df3-a33c-1a16c865d54a");
INSERT INTO R_FORM
    VALUES ("53446f65-84b1-424b-bc68-cf0164d24a57",
    "749e0026-f26e-4df3-a33c-1a16c865d54a",
    "6aad37f6-2c85-4cb8-991b-9d866a382f49",
    0,
    1,
    '');
INSERT INTO R_RGO
    VALUES ("53446f65-84b1-424b-bc68-cf0164d24a57",
    "749e0026-f26e-4df3-a33c-1a16c865d54a",
    "6aad37f6-2c85-4cb8-991b-9d866a382f49");
INSERT INTO R_OIR
    VALUES ("53446f65-84b1-424b-bc68-cf0164d24a57",
    "749e0026-f26e-4df3-a33c-1a16c865d54a",
    "6aad37f6-2c85-4cb8-991b-9d866a382f49",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO R_PART
    VALUES ("7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    "749e0026-f26e-4df3-a33c-1a16c865d54a",
    "54f4406e-145d-46f9-b866-d68d00b6a58f",
    0,
    0,
    '');
INSERT INTO O_RTIDA
    VALUES ("429f668f-92bd-4661-a074-7328a5d4e4ba",
    "7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    0,
    "749e0026-f26e-4df3-a33c-1a16c865d54a",
    "54f4406e-145d-46f9-b866-d68d00b6a58f");
INSERT INTO R_RTO
    VALUES ("7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    "749e0026-f26e-4df3-a33c-1a16c865d54a",
    "54f4406e-145d-46f9-b866-d68d00b6a58f",
    0);
INSERT INTO R_OIR
    VALUES ("7b476efe-6f27-47ac-80ba-00eca6ef4ad9",
    "749e0026-f26e-4df3-a33c-1a16c865d54a",
    "54f4406e-145d-46f9-b866-d68d00b6a58f",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO PE_PE
    VALUES ("0065df20-dd20-47f8-80fa-f2a356522d79",
    1,
    "96ec2ddc-da38-40da-8372-025532bfdb1d",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("0065df20-dd20-47f8-80fa-f2a356522d79",
    "00000000-0000-0000-0000-000000000000",
    'My_Enum',
    '',
    '');
INSERT INTO S_EDT
    VALUES ("0065df20-dd20-47f8-80fa-f2a356522d79");
INSERT INTO S_ENUM
    VALUES ("7ca13587-746c-419d-9354-6788971215d7",
    'E1',
    '',
    "0065df20-dd20-47f8-80fa-f2a356522d79",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO S_ENUM
    VALUES ("a66d6fac-f124-41cd-b761-c6d1f4e30b7e",
    'E2',
    '',
    "0065df20-dd20-47f8-80fa-f2a356522d79",
    "7ca13587-746c-419d-9354-6788971215d7");
INSERT INTO S_ENUM
    VALUES ("5c83431e-8337-43e5-b316-c3b0ca1ad858",
    'E3',
    '',
    "0065df20-dd20-47f8-80fa-f2a356522d79",
    "a66d6fac-f124-41cd-b761-c6d1f4e30b7e");
INSERT INTO PE_PE
    VALUES ("0eff6918-06c2-4e6d-ade0-a89e852c4628",
    1,
    "96ec2ddc-da38-40da-8372-025532bfdb1d",
    "00000000-0000-0000-0000-000000000000",
    10);
INSERT INTO CNST_CSP
    VALUES ("0eff6918-06c2-4e6d-ade0-a89e852c4628",
    'My_Constants',
    '');
INSERT INTO CNST_SYC
    VALUES ("fd9b7f62-283f-4fa9-ae4b-56e368f0f34f",
    'PI',
    '',
    "ba5eda7a-def5-0000-0000-000000000003",
    "0eff6918-06c2-4e6d-ade0-a89e852c4628",
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO CNST_LFSC
    VALUES ("fd9b7f62-283f-4fa9-ae4b-56e368f0f34f",
    "ba5eda7a-def5-0000-0000-000000000003");
INSERT INTO CNST_LSC
    VALUES ("fd9b7f62-283f-4fa9-ae4b-56e368f0f34f",
    "ba5eda7a-def5-0000-0000-000000000003",
    '3.14');
INSERT INTO PE_PE
    VALUES ("8d35d15f-ff91-47a8-a970-ec892e1f2714",
    1,
    "96ec2ddc-da38-40da-8372-025532bfdb1d",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("8d35d15f-ff91-47a8-a970-ec892e1f2714",
    "00000000-0000-0000-0000-000000000000",
    'My_Struct',
    '',
    '');
INSERT INTO S_SDT
    VALUES ("8d35d15f-ff91-47a8-a970-ec892e1f2714");
INSERT INTO S_MBR
    VALUES ("0af1de93-1245-4592-bc8f-6f87aa2e8982",
    'M1',
    '',
    "8d35d15f-ff91-47a8-a970-ec892e1f2714",
    "ba5eda7a-def5-0000-0000-000000000002",
    "00000000-0000-0000-0000-000000000000",
    '');
INSERT INTO S_MBR
    VALUES ("e1b8b5cd-616a-49df-abce-66e959122718",
    'M2',
    '',
    "8d35d15f-ff91-47a8-a970-ec892e1f2714",
    "ba5eda7a-def5-0000-0000-000000000002",
    "0af1de93-1245-4592-bc8f-6f87aa2e8982",
    '');
INSERT INTO S_MBR
    VALUES ("7cad597c-0c74-4b99-8aa6-a0ea5814bcea",
    'M3',
    '',
    "8d35d15f-ff91-47a8-a970-ec892e1f2714",
    "ba5eda7a-def5-0000-0000-000000000002",
    "e1b8b5cd-616a-49df-abce-66e959122718",
    '');
INSERT INTO PE_PE
    VALUES ("96ec2ddc-da38-40da-8372-025532bfdb1d",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    7);
INSERT INTO EP_PKG
    VALUES ("f70c1519-babf-4219-93e7-abd938a6ea5e",
    "d8ca6d9b-7cf6-4f9b-9224-bf1bbd4de04a",
    "d8ca6d9b-7cf6-4f9b-9224-bf1bbd4de04a",
    'Test_Cases',
    '',
    0);
INSERT INTO GD_MD
    VALUES ("07b38155-6b4a-4e98-8f8a-e6032b5ec52f",
    112,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    108,
    0,
    0,
    1,
    1,
    1,
    12,
    1,
    0,
    0,
    0,
    0,
    0,
    '',
    'Test::Test_Cases');
INSERT INTO DIM_DIA
    VALUES ("07b38155-6b4a-4e98-8f8a-e6032b5ec52f",
    '',
    1.000000,
    0.000000,
    0.000000,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO PE_PE
    VALUES ("d83582ce-8ebd-4c19-975b-db17b819e783",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("d83582ce-8ebd-4c19-975b-db17b819e783",
    "00000000-0000-0000-0000-000000000000",
    'Test',
    '',
    'rc = True;

if ::Test_Array()
    LOG::LogSuccess(message: "Test_Array");
else
    LOG::LogFailure(message: "Test_Array");
    rc = False;
end if;


if ::Test_Break_For_Each()
    LOG::LogSuccess(message: "Test_Break_For_Each");
else
    LOG::LogFailure(message: "Test_Break_For_Each");
    rc = False;
end if;


if ::Test_Break_While()
    LOG::LogSuccess(message: "Test_Break_While");
else
    LOG::LogFailure(message: "Test_Break_While");
    rc = False;
end if;

if ::Test_Continue_For_Each()
    LOG::LogSuccess(message: "Test_Continue_For_Each");
else
    LOG::LogFailure(message: "Test_Continue_For_Each");
    rc = False;
end if;

if ::Test_Continue_While()
    LOG::LogSuccess(message: "Test_Continue_While");
else
    LOG::LogFailure(message: "Test_Continue_While");
    rc = False;
end if;

if ::Test_Create_Object()
    LOG::LogSuccess(message: "Test_Create_Object");
else
    LOG::LogFailure(message: "Test_Create_Object");
    rc = False;
end if;

if ::Test_Create_Object_No_Var()
    LOG::LogSuccess(message: "Test_Create_Object_No_Var");
else
    LOG::LogFailure(message: "Test_Create_Object_No_Var");
    rc = False;
end if;

if ::Test_Delete_Object()
    LOG::LogSuccess(message: "Test_Delete_Object");
else
    LOG::LogFailure(message: "Test_Delete_Object");
    rc = False;
end if;

if ::Test_ElIf()
    LOG::LogSuccess(message: "Test_ElIf");
else
    LOG::LogFailure(message: "Test_ElIf");
    rc = False;
end if;

if ::Test_Else()
    LOG::LogSuccess(message: "Test_Else");
else
    LOG::LogFailure(message: "Test_Else");
    rc = False;
end if;

if ::Test_If()
    LOG::LogSuccess(message: "Test_If");
else
    LOG::LogFailure(message: "Test_If");
    rc = False;
end if;

if ::Test_Invoke()
    LOG::LogSuccess(message: "Test_Invoke");
else
    LOG::LogFailure(message: "Test_Invoke");
    rc = False;
end if;

if ::Test_Literals()
    LOG::LogSuccess(message: "Test_Literals");
else
    LOG::LogFailure(message: "Test_Literals");
    rc = False;
end if;

if ::Test_Relate()
    LOG::LogSuccess(message: "Test_Relate");
else
    LOG::LogFailure(message: "Test_Relate");
    rc = False;
end if;

if ::Test_Relate_Using()
    LOG::LogSuccess(message: "Test_Relate_Using");
else
    LOG::LogFailure(message: "Test_Relate_Using");
    rc = False;
end if;

if ::Test_Related_Where()
    LOG::LogSuccess(message: "Test_Related_Where");
else
    LOG::LogFailure(message: "Test_Related_Where");
    rc = False;
end if;

if ::Test_Unrelate()
    LOG::LogSuccess(message: "Test_Unrelate");
else
    LOG::LogFailure(message: "Test_Unrelate");
    rc = False;
end if;

if ::Test_Unrelate_Using()
    LOG::LogSuccess(message: "Test_Unrelate_Using");
else
    LOG::LogFailure(message: "Test_Unrelate_Using");
    rc = False;
end if;

if ::Test_Where()
    LOG::LogSuccess(message: "Test_Where");
else
    LOG::LogFailure(message: "Test_Where");
    rc = False;
end if;

return rc;
',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("79148343-ecb1-4291-8aab-cbc60fd2e85c",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("79148343-ecb1-4291-8aab-cbc60fd2e85c",
    "00000000-0000-0000-0000-000000000000",
    'Test_Break_While',
    '',
    'Loop_Count = 0;
Iter_Count = 0;
while Loop_Count < 10
    Loop_Count = Loop_Count + 1;
    if Loop_Count <= 5
        continue;
    end if;
    
    Iter_Count = Iter_Count + 1;
end while;

return Iter_Count == 5;

',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("1f9ed69b-ae26-414f-9d53-36e843a37d9f",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("1f9ed69b-ae26-414f-9d53-36e843a37d9f",
    "00000000-0000-0000-0000-000000000000",
    'Test_Continue_While',
    '',
    'Loop_Count = 0;

while True
    Loop_Count = Loop_Count + 1;
    if Loop_Count == 10
        break;
    end if;
end while;

return Loop_Count == 10;

',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("a7424729-766b-4f97-8045-a080603ba46d",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("a7424729-766b-4f97-8045-a080603ba46d",
    "00000000-0000-0000-0000-000000000000",
    'Test_Control_Stop',
    '',
    'control stop;
return False;',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("d059230f-8b33-49c5-bd1f-134ff65880fd",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("d059230f-8b33-49c5-bd1f-134ff65880fd",
    "00000000-0000-0000-0000-000000000000",
    'Test_Create_Object',
    '',
    'create object instance inst of Class;
return not_empty inst;
',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("4ac9fddb-6b8a-41f5-861a-1b05a3128760",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("4ac9fddb-6b8a-41f5-861a-1b05a3128760",
    "00000000-0000-0000-0000-000000000000",
    'Test_Create_Object_No_Var',
    '',
    'select many Classes from instances of Class;
count = cardinality Classes;

create object instance of Class;
create object instance of Class;
create object instance of Class;

select many Classes from instances of Class;
return (count + 3) == (cardinality Classes);
',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("fbceceb0-b1aa-411f-8fbb-2806dfa0e80e",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("fbceceb0-b1aa-411f-8fbb-2806dfa0e80e",
    "00000000-0000-0000-0000-000000000000",
    'Test_Delete_Object',
    '',
    'select many Classes from instances of Class;
count = cardinality Classes;

create object instance inst of Class;
delete object instance inst;

select many Classes from instances of Class;
return count == cardinality Classes;
',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("b3e8b823-6b8b-4170-ba05-af5a65de4578",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("b3e8b823-6b8b-4170-ba05-af5a65de4578",
    "00000000-0000-0000-0000-000000000000",
    'Test_For_Each',
    '',
    'create object instance of Class;
create object instance of Class;
create object instance of Class;

select many insts from instances of Class;
count = 0;

for each inst in insts
    count = count + 1;
end for;

return count == cardinality insts;
',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("6208aacb-10ee-4c47-984f-cfa10777df18",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("6208aacb-10ee-4c47-984f-cfa10777df18",
    "00000000-0000-0000-0000-000000000000",
    'Test_Break_For_Each',
    '',
    'create object instance of Class;
create object instance of Class;
create object instance of Class;

select many insts from instances of Class;
count = 0;

for each inst in insts
    count = count + 1;
    if count == 2
        break;
    end if;
end for;

return count == 2;
',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("9de8d2c7-3e23-4a25-a241-1f3ce4099550",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("9de8d2c7-3e23-4a25-a241-1f3ce4099550",
    "00000000-0000-0000-0000-000000000000",
    'Test_Continue_For_Each',
    '',
    'create object instance of Class;
create object instance of Class;
create object instance of Class;

select many insts from instances of Class;
count = 0;
chosen = 0;

for each inst in insts
    count = count + 1;
    if count > cardinality insts - 2
        chosen = chosen + 1;
    end if;
end for;

return chosen == 2;
',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("dc841230-2fa3-457d-a050-1473a55927e0",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("dc841230-2fa3-457d-a050-1473a55927e0",
    "00000000-0000-0000-0000-000000000000",
    'Test_If',
    '',
    'if True
    return True;
elif False
    return False;
else
    return False;
end if;

return False;
',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("04773d46-44ff-4616-aca7-fa5b9ed7f004",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("04773d46-44ff-4616-aca7-fa5b9ed7f004",
    "00000000-0000-0000-0000-000000000000",
    'Test_ElIf',
    '',
    'if False
    return False;
elif True
    return True;
else
    return False;
end if;

return False;
',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("9c26c61e-3850-499e-ac88-74a1b5f3d2a2",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("9c26c61e-3850-499e-ac88-74a1b5f3d2a2",
    "00000000-0000-0000-0000-000000000000",
    'Test_Else',
    '',
    'if False
    return False;
elif False
    return False;
else
    return True;
end if;

return False;
',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("06471909-c97f-414d-b2e2-99efa7b07984",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("06471909-c97f-414d-b2e2-99efa7b07984",
    "00000000-0000-0000-0000-000000000000",
    'Test_Relate_Using',
    '',
    'create object instance inst1 of Class;
create object instance inst2 of Class;
create object instance assoc of Assoc;

relate inst1 to inst2 across R1.''one'' using assoc;

return (assoc.Other_ID == inst1.ID);
',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("c16f0659-2296-4833-b7ba-c47b981cc083",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("c16f0659-2296-4833-b7ba-c47b981cc083",
    "00000000-0000-0000-0000-000000000000",
    'Test_Relate',
    '',
    'create object instance cls of Class;
create object instance other_cls of Other_Class;
relate cls to other_cls across R2;

return cls.ID == other_cls.Class_ID;

',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("68c929c4-1c74-4098-a42a-c5556b0e9027",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("68c929c4-1c74-4098-a42a-c5556b0e9027",
    "00000000-0000-0000-0000-000000000000",
    'Test_Unrelate',
    '',
    'create object instance cls of Class;
create object instance other_cls of Other_Class;
relate cls to other_cls across R2;

select one inst related by cls->Other_Class[R2];
if empty inst
    return False;
end if;


unrelate cls from other_cls across R2;

select one inst related by cls->Other_Class[R2];
return empty inst;


',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("e01ab4f8-fbe8-4e44-8740-2c6ddd206922",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("e01ab4f8-fbe8-4e44-8740-2c6ddd206922",
    "00000000-0000-0000-0000-000000000000",
    'Test_Unrelate_Using',
    '',
    'create object instance inst1 of Class;
create object instance inst2 of Class;
create object instance assoc of Assoc;

relate inst1 to inst2 across R1.''one'' using assoc;

select one inst related by inst1->Assoc[R1.''one''];
if empty inst
    return False;
end if;

unrelate inst1 from inst2 across R1.''one'' using assoc;

select one inst related by inst1->Assoc[R1.''one''];

return empty inst;

',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("5f789389-381f-4191-9e54-b026a8d23e8e",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("5f789389-381f-4191-9e54-b026a8d23e8e",
    "00000000-0000-0000-0000-000000000000",
    'Test_Literals',
    '',
    'if 0 > 1
    return False;
end if;

if "s1" == "s2"
    return False;
end if;

if 1.0 < 0.0
    return False;
end if;

if True == False
    return False;
end if;

if 3.0 > PI
    return False;
end if;

if 3.2 < PI
    return False;
end if;

if My_Enum::E1 == My_Enum::E2 
    return False;
end if;

return True;',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("48f306e1-877a-4e2b-83a8-4c8803fd77e3",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("48f306e1-877a-4e2b-83a8-4c8803fd77e3",
    "00000000-0000-0000-0000-000000000000",
    'Test_Array',
    '',
    'Array[10][10] = 10;
Array[10][9] = 9;
Array[10][8] = 8;

if Array[10][9] != 9
    return False;
end if;

return True;


',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("2d12fbab-0014-4ebd-9831-65935a36a401",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("2d12fbab-0014-4ebd-9831-65935a36a401",
    "00000000-0000-0000-0000-000000000000",
    'Test_Invoke',
    '',
    'transform Class::Transform_Function();

if 3 != Class::Class_Based_Operation(P1: 1, P2: 2)
    return False;
end if;

create object instance inst of Class;
if 44 != inst.Instance_Based_Operation(P1: 1, P2: 1)
    return False;
end if;


return True;',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("d2d385ce-dd8e-4556-97ad-59746c93516b",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("d2d385ce-dd8e-4556-97ad-59746c93516b",
    "00000000-0000-0000-0000-000000000000",
    'Test_Where',
    '',
    'create object instance inst1 of Class;
create object instance inst2 of Class;

select any inst from instances of Class where (False);
if not_empty inst
    return False;
end if;

select any inst3 from instances of Class where (selected.ID == inst1.ID);

return inst1.ID == inst3.ID;

',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("bed3ece3-e50c-453f-aa1d-03ad64f60cdf",
    1,
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    "00000000-0000-0000-0000-000000000000",
    1);
INSERT INTO S_SYNC
    VALUES ("bed3ece3-e50c-453f-aa1d-03ad64f60cdf",
    "00000000-0000-0000-0000-000000000000",
    'Test_Related_Where',
    '',
    'create object instance inst1 of Class;
create object instance inst2 of Other_Class;

relate inst1 to inst2 across R2;

select one inst related by inst2->Class[R2] where (False);
if not_empty inst
    return False;
end if;

select one inst3 related by inst2->Class[R2] where (selected.ID == inst1.ID);

return inst1.ID == inst3.ID;

',
    "ba5eda7a-def5-0000-0000-000000000001",
    1,
    '',
    0);
INSERT INTO PE_PE
    VALUES ("f70c1519-babf-4219-93e7-abd938a6ea5e",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    7);
INSERT INTO GD_GE
    VALUES ("bf019bfd-2759-48e0-a435-8c2cc80314df",
    "42f26458-c76d-4c4d-9a77-185fb21c49aa",
    "96ec2ddc-da38-40da-8372-025532bfdb1d",
    108,
    0,
    'Test::Stimuli');
INSERT INTO GD_SHP
    VALUES ("bf019bfd-2759-48e0-a435-8c2cc80314df");
INSERT INTO GD_NCS
    VALUES ("bf019bfd-2759-48e0-a435-8c2cc80314df");
INSERT INTO DIM_ND
    VALUES (200.000000,
    150.000000,
    "bf019bfd-2759-48e0-a435-8c2cc80314df");
INSERT INTO DIM_GE
    VALUES (220.000000,
    0.000000,
    "bf019bfd-2759-48e0-a435-8c2cc80314df",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("bf019bfd-2759-48e0-a435-8c2cc80314df",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO GD_GE
    VALUES ("8d93b8a9-a6fe-4f59-8997-dabb2df460a0",
    "42f26458-c76d-4c4d-9a77-185fb21c49aa",
    "f70c1519-babf-4219-93e7-abd938a6ea5e",
    108,
    0,
    'Test::Test_Cases');
INSERT INTO GD_SHP
    VALUES ("8d93b8a9-a6fe-4f59-8997-dabb2df460a0");
INSERT INTO GD_NCS
    VALUES ("8d93b8a9-a6fe-4f59-8997-dabb2df460a0");
INSERT INTO DIM_ND
    VALUES (200.000000,
    150.000000,
    "8d93b8a9-a6fe-4f59-8997-dabb2df460a0");
INSERT INTO DIM_GE
    VALUES (0.000000,
    0.000000,
    "8d93b8a9-a6fe-4f59-8997-dabb2df460a0",
    "00000000-0000-0000-0000-000000000000");
INSERT INTO DIM_ELE
    VALUES ("8d93b8a9-a6fe-4f59-8997-dabb2df460a0",
    0,
    "00000000-0000-0000-0000-000000000000");
INSERT INTO S_SYS_PROXY
    VALUES ("d8ca6d9b-7cf6-4f9b-9224-bf1bbd4de04a",
    'Test',
    1,
    '../Test.xtuml');
"""


from bridgepoint import ooaofooa


class TestModel(unittest.TestCase):

    def test_model(self):
        l = ooaofooa.Loader(load_globals=True)
        l.input(model, 'Test model')
        c = l.build_component()
        func = c.find_symbol('Test')
        self.assertTrue(func())



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()