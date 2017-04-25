# encoding: utf-8
# Copyright (C) 2017 John Törnblom
#
# This file is part of pyxtuml.
#
# pyxtuml is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# pyxtuml is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with pyxtuml. If not, see <http://www.gnu.org/licenses/>.

import unittest
import bridgepoint
import xtuml


class TestSchemaGen(unittest.TestCase):
    """
    -- root-types-contained: ModelClass_c,Association_c,ClassAsSubtype_c,ClassAsLink_c
    -- generics
    -- BP 7.1 content: StreamData syschar: 3 persistence-version: 7.1.6
    
    INSERT INTO O_OBJ
        VALUES ("3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        'Class',
        1,
        'Class',
        '',
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO O_NBATTR
        VALUES ("f94afef8-ed1a-4b9b-bb29-36149617b861",
        "3beb857e-8f3e-41c8-a1d5-e3dd66d836db");
    INSERT INTO O_BATTR
        VALUES ("f94afef8-ed1a-4b9b-bb29-36149617b861",
        "3beb857e-8f3e-41c8-a1d5-e3dd66d836db");
    INSERT INTO O_ATTR
        VALUES ("f94afef8-ed1a-4b9b-bb29-36149617b861",
        "3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        "00000000-0000-0000-0000-000000000000",
        'Id',
        '',
        '',
        'Id',
        0,
        "ba5eda7a-def5-0000-0000-000000000005",
        '',
        '');
    INSERT INTO O_REF
        VALUES ("3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        "7ef7999e-5513-4984-8744-9c1a5cf46412",
        0,
        "990c9f1b-71a8-4246-af0e-de20a069e784",
        "3ae58522-7f90-48b3-85b4-35df51c6192a",
        "b3f14c88-fd1b-4aa8-a5ae-15d202bee5d6",
        "9d8b6602-75c8-44b6-ac4f-9da04573b957",
        "6fdefe7f-3f99-4c57-8009-8825066fa637",
        "9197e43d-966a-4435-8393-0ff6514947f6",
        "00000000-0000-0000-0000-000000000000",
        0,
        '',
        'Supertype',
        'Id',
        'R3');
    INSERT INTO O_RATTR
        VALUES ("6fdefe7f-3f99-4c57-8009-8825066fa637",
        "3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        "ee277c43-a11a-4ac9-bc82-2bb8a82fd437",
        "419dc876-6997-44cb-a671-41acc466044a",
        1,
        'Id');
    INSERT INTO O_ATTR
        VALUES ("6fdefe7f-3f99-4c57-8009-8825066fa637",
        "3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        "f94afef8-ed1a-4b9b-bb29-36149617b861",
        'Other_Id',
        '',
        'Other_',
        'Id',
        1,
        "ba5eda7a-def5-0000-0000-000000000007",
        '',
        '');
    INSERT INTO O_ID
        VALUES (0,
        "3beb857e-8f3e-41c8-a1d5-e3dd66d836db");
    INSERT INTO O_OIDA
        VALUES ("f94afef8-ed1a-4b9b-bb29-36149617b861",
        "3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        0,
        'Id');
    INSERT INTO O_ID
        VALUES (1,
        "3beb857e-8f3e-41c8-a1d5-e3dd66d836db");
    INSERT INTO O_ID
        VALUES (2,
        "3beb857e-8f3e-41c8-a1d5-e3dd66d836db");
    INSERT INTO PE_PE
        VALUES ("3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        1,
        "b48a6732-c56c-4e98-8773-afe91fcb30e4",
        "00000000-0000-0000-0000-000000000000",
        4);
    INSERT INTO GD_GE
        VALUES ("210a115a-1c94-41b9-b811-2f86d59a6d31",
        "1344bf4e-528f-4e2b-b8cc-4db9e48e1967",
        "3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        21,
        0,
        'Test_Schema_Gen::Package::Class');
    INSERT INTO GD_SHP
        VALUES ("210a115a-1c94-41b9-b811-2f86d59a6d31");
    INSERT INTO GD_NCS
        VALUES ("210a115a-1c94-41b9-b811-2f86d59a6d31");
    INSERT INTO DIM_ND
        VALUES (204.000000,
        156.000000,
        "210a115a-1c94-41b9-b811-2f86d59a6d31");
    INSERT INTO DIM_GE
        VALUES (4248.000000,
        3108.000000,
        "210a115a-1c94-41b9-b811-2f86d59a6d31",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("210a115a-1c94-41b9-b811-2f86d59a6d31",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_CON
        VALUES ("695fd096-c898-4f1e-9505-a036da9cf287",
        4344.000000,
        3264.000000,
        "210a115a-1c94-41b9-b811-2f86d59a6d31");
    INSERT INTO DIM_CON
        VALUES ("9e246129-772e-4e7e-9b8b-8dd68e80b065",
        4452.000000,
        3204.000000,
        "210a115a-1c94-41b9-b811-2f86d59a6d31");
    INSERT INTO O_OBJ
        VALUES ("68553234-715f-43ce-a1ce-4b93d6483cf5",
        'Reflexive_Class',
        2,
        'Reflexive_Class',
        '',
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO O_REF
        VALUES ("68553234-715f-43ce-a1ce-4b93d6483cf5",
        "3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        0,
        "f94afef8-ed1a-4b9b-bb29-36149617b861",
        "131ece0d-48e6-40d3-a3c2-baac77f9f32c",
        "fb42f65b-cd41-411a-b022-a3cf2f481a99",
        "fe0e8e09-edef-4be6-b8d7-0cb86053f640",
        "64853c2b-640f-4738-a363-40892f8d4757",
        "644754bf-f80c-4e00-9693-75d2dc620d54",
        "00000000-0000-0000-0000-000000000000",
        0,
        '',
        'Class',
        'Id',
        'R4');
    INSERT INTO O_RATTR
        VALUES ("64853c2b-640f-4738-a363-40892f8d4757",
        "68553234-715f-43ce-a1ce-4b93d6483cf5",
        "f94afef8-ed1a-4b9b-bb29-36149617b861",
        "3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        1,
        'Id');
    INSERT INTO O_ATTR
        VALUES ("64853c2b-640f-4738-a363-40892f8d4757",
        "68553234-715f-43ce-a1ce-4b93d6483cf5",
        "00000000-0000-0000-0000-000000000000",
        'Id',
        '',
        '',
        'Id',
        0,
        "ba5eda7a-def5-0000-0000-000000000007",
        '',
        '');
    INSERT INTO O_ID
        VALUES (0,
        "68553234-715f-43ce-a1ce-4b93d6483cf5");
    INSERT INTO O_OIDA
        VALUES ("64853c2b-640f-4738-a363-40892f8d4757",
        "68553234-715f-43ce-a1ce-4b93d6483cf5",
        0,
        'Id');
    INSERT INTO O_ID
        VALUES (1,
        "68553234-715f-43ce-a1ce-4b93d6483cf5");
    INSERT INTO O_ID
        VALUES (2,
        "68553234-715f-43ce-a1ce-4b93d6483cf5");
    INSERT INTO PE_PE
        VALUES ("68553234-715f-43ce-a1ce-4b93d6483cf5",
        1,
        "b48a6732-c56c-4e98-8773-afe91fcb30e4",
        "00000000-0000-0000-0000-000000000000",
        4);
    INSERT INTO GD_GE
        VALUES ("ce5eb32f-79fe-419f-a56d-8c439930f96d",
        "1344bf4e-528f-4e2b-b8cc-4db9e48e1967",
        "68553234-715f-43ce-a1ce-4b93d6483cf5",
        21,
        0,
        'Test_Schema_Gen::Package::Reflexive_Class');
    INSERT INTO GD_SHP
        VALUES ("ce5eb32f-79fe-419f-a56d-8c439930f96d");
    INSERT INTO GD_NCS
        VALUES ("ce5eb32f-79fe-419f-a56d-8c439930f96d");
    INSERT INTO DIM_ND
        VALUES (204.000000,
        144.000000,
        "ce5eb32f-79fe-419f-a56d-8c439930f96d");
    INSERT INTO DIM_GE
        VALUES (4740.000000,
        3108.000000,
        "ce5eb32f-79fe-419f-a56d-8c439930f96d",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("ce5eb32f-79fe-419f-a56d-8c439930f96d",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_CON
        VALUES ("26b28f41-8966-4148-98f5-91f5505b5c92",
        4944.000000,
        3168.000000,
        "ce5eb32f-79fe-419f-a56d-8c439930f96d");
    INSERT INTO DIM_CON
        VALUES ("8d6716fa-92c3-46e4-8116-2ab556e15f4e",
        4824.000000,
        3108.000000,
        "ce5eb32f-79fe-419f-a56d-8c439930f96d");
    INSERT INTO DIM_CON
        VALUES ("6ef83aa3-47e5-43f8-bbfa-058e9a2032f5",
        4740.000000,
        3204.000000,
        "ce5eb32f-79fe-419f-a56d-8c439930f96d");
    INSERT INTO R_REL
        VALUES ("4cfe4e7d-1919-4ef2-a4db-03c85c772b2a",
        1,
        '',
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO R_ASSOC
        VALUES ("4cfe4e7d-1919-4ef2-a4db-03c85c772b2a");
    INSERT INTO R_AONE
        VALUES ("68553234-715f-43ce-a1ce-4b93d6483cf5",
        "4cfe4e7d-1919-4ef2-a4db-03c85c772b2a",
        "04310dd4-9b14-4b59-9a59-9e9dc5d99468",
        0,
        1,
        'other');
    INSERT INTO O_RTIDA
        VALUES ("64853c2b-640f-4738-a363-40892f8d4757",
        "68553234-715f-43ce-a1ce-4b93d6483cf5",
        0,
        "4cfe4e7d-1919-4ef2-a4db-03c85c772b2a",
        "04310dd4-9b14-4b59-9a59-9e9dc5d99468");
    INSERT INTO R_RTO
        VALUES ("68553234-715f-43ce-a1ce-4b93d6483cf5",
        "4cfe4e7d-1919-4ef2-a4db-03c85c772b2a",
        "04310dd4-9b14-4b59-9a59-9e9dc5d99468",
        0);
    INSERT INTO R_OIR
        VALUES ("68553234-715f-43ce-a1ce-4b93d6483cf5",
        "4cfe4e7d-1919-4ef2-a4db-03c85c772b2a",
        "04310dd4-9b14-4b59-9a59-9e9dc5d99468",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO R_AOTH
        VALUES ("68553234-715f-43ce-a1ce-4b93d6483cf5",
        "4cfe4e7d-1919-4ef2-a4db-03c85c772b2a",
        "aeb07e49-c4f9-42dc-93d2-bf42134687b4",
        0,
        1,
        'one');
    INSERT INTO O_RTIDA
        VALUES ("64853c2b-640f-4738-a363-40892f8d4757",
        "68553234-715f-43ce-a1ce-4b93d6483cf5",
        0,
        "4cfe4e7d-1919-4ef2-a4db-03c85c772b2a",
        "aeb07e49-c4f9-42dc-93d2-bf42134687b4");
    INSERT INTO R_RTO
        VALUES ("68553234-715f-43ce-a1ce-4b93d6483cf5",
        "4cfe4e7d-1919-4ef2-a4db-03c85c772b2a",
        "aeb07e49-c4f9-42dc-93d2-bf42134687b4",
        0);
    INSERT INTO R_OIR
        VALUES ("68553234-715f-43ce-a1ce-4b93d6483cf5",
        "4cfe4e7d-1919-4ef2-a4db-03c85c772b2a",
        "aeb07e49-c4f9-42dc-93d2-bf42134687b4",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO R_ASSR
        VALUES ("bd62e326-bbc2-4c55-8ee1-69a59e5146d3",
        "4cfe4e7d-1919-4ef2-a4db-03c85c772b2a",
        "bc18e358-1a8c-41d3-9ed5-5013ba99339c",
        0);
    INSERT INTO R_RGO
        VALUES ("bd62e326-bbc2-4c55-8ee1-69a59e5146d3",
        "4cfe4e7d-1919-4ef2-a4db-03c85c772b2a",
        "bc18e358-1a8c-41d3-9ed5-5013ba99339c");
    INSERT INTO R_OIR
        VALUES ("bd62e326-bbc2-4c55-8ee1-69a59e5146d3",
        "4cfe4e7d-1919-4ef2-a4db-03c85c772b2a",
        "bc18e358-1a8c-41d3-9ed5-5013ba99339c",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO PE_PE
        VALUES ("4cfe4e7d-1919-4ef2-a4db-03c85c772b2a",
        1,
        "b48a6732-c56c-4e98-8773-afe91fcb30e4",
        "00000000-0000-0000-0000-000000000000",
        9);
    INSERT INTO GD_GE
        VALUES ("7bd1fcbb-abc0-435a-af67-11079f2b1404",
        "1344bf4e-528f-4e2b-b8cc-4db9e48e1967",
        "4cfe4e7d-1919-4ef2-a4db-03c85c772b2a",
        24,
        0,
        'Test_Schema_Gen::Package::R1');
    INSERT INTO GD_CON
        VALUES ("7bd1fcbb-abc0-435a-af67-11079f2b1404",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_CTXT
        VALUES ("6c59d5ff-5c41-4e5d-bec3-6a7608db86c3",
        "7bd1fcbb-abc0-435a-af67-11079f2b1404",
        1,
        0.000000,
        0.000000);
    INSERT INTO DIM_ND
        VALUES (0.000000,
        0.000000,
        "6c59d5ff-5c41-4e5d-bec3-6a7608db86c3");
    INSERT INTO DIM_GE
        VALUES (4954.000000,
        3178.000000,
        "6c59d5ff-5c41-4e5d-bec3-6a7608db86c3",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("6c59d5ff-5c41-4e5d-bec3-6a7608db86c3",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_CTXT
        VALUES ("d3e5f1ba-bcff-47ab-92ae-0cce0d3a416b",
        "7bd1fcbb-abc0-435a-af67-11079f2b1404",
        3,
        0.000000,
        0.000000);
    INSERT INTO DIM_ND
        VALUES (0.000000,
        0.000000,
        "d3e5f1ba-bcff-47ab-92ae-0cce0d3a416b");
    INSERT INTO DIM_GE
        VALUES (4955.000000,
        3106.000000,
        "d3e5f1ba-bcff-47ab-92ae-0cce0d3a416b",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("d3e5f1ba-bcff-47ab-92ae-0cce0d3a416b",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_CTXT
        VALUES ("a0e511d2-2174-4ad6-9f3b-9b3502929f8a",
        "7bd1fcbb-abc0-435a-af67-11079f2b1404",
        2,
        0.000000,
        0.000000);
    INSERT INTO DIM_ND
        VALUES (0.000000,
        0.000000,
        "a0e511d2-2174-4ad6-9f3b-9b3502929f8a");
    INSERT INTO DIM_GE
        VALUES (4834.000000,
        3081.000000,
        "a0e511d2-2174-4ad6-9f3b-9b3502929f8a",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("a0e511d2-2174-4ad6-9f3b-9b3502929f8a",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_LS
        VALUES ("6d15d3b0-8cad-49b7-9b9e-0db3cfa4ac05",
        "7bd1fcbb-abc0-435a-af67-11079f2b1404",
        "00000000-0000-0000-0000-000000000000",
        "76c98002-bf63-4027-a727-d84c74c0d612",
        "b4c22ed9-4a33-4629-976a-79db62426ea6");
    INSERT INTO GD_LS
        VALUES ("b392c3bc-222a-4c84-8eef-e14c9442e110",
        "7bd1fcbb-abc0-435a-af67-11079f2b1404",
        "6d15d3b0-8cad-49b7-9b9e-0db3cfa4ac05",
        "b4c22ed9-4a33-4629-976a-79db62426ea6",
        "0d565025-f494-43bd-9bff-ae4bf62bc727");
    INSERT INTO GD_AOS
        VALUES ("bc2759d4-1947-4b2d-b842-9faece1ecc82",
        "b392c3bc-222a-4c84-8eef-e14c9442e110");
    INSERT INTO GD_LS
        VALUES ("a911e69d-97ed-454e-a494-7828c0ba57ee",
        "7bd1fcbb-abc0-435a-af67-11079f2b1404",
        "b392c3bc-222a-4c84-8eef-e14c9442e110",
        "0d565025-f494-43bd-9bff-ae4bf62bc727",
        "53cd2b79-85ba-474d-9090-46ac0fe88f7f");
    INSERT INTO GD_LS
        VALUES ("f148f99d-15ab-4bd3-9aab-42301a186edb",
        "7bd1fcbb-abc0-435a-af67-11079f2b1404",
        "a911e69d-97ed-454e-a494-7828c0ba57ee",
        "53cd2b79-85ba-474d-9090-46ac0fe88f7f",
        "a44fd264-30ef-463e-8524-c49407b83d3a");
    INSERT INTO DIM_WAY
        VALUES ("76c98002-bf63-4027-a727-d84c74c0d612",
        4944.000000,
        3168.000000,
        "7bd1fcbb-abc0-435a-af67-11079f2b1404",
        "00000000-0000-0000-0000-000000000000",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_WAY
        VALUES ("a44fd264-30ef-463e-8524-c49407b83d3a",
        4824.000000,
        3108.000000,
        "7bd1fcbb-abc0-435a-af67-11079f2b1404",
        "00000000-0000-0000-0000-000000000000",
        "76c98002-bf63-4027-a727-d84c74c0d612");
    INSERT INTO DIM_WAY
        VALUES ("b4c22ed9-4a33-4629-976a-79db62426ea6",
        4994.000000,
        3168.000000,
        "7bd1fcbb-abc0-435a-af67-11079f2b1404",
        "00000000-0000-0000-0000-000000000000",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_WAY
        VALUES ("0d565025-f494-43bd-9bff-ae4bf62bc727",
        4994.000000,
        3059.000000,
        "7bd1fcbb-abc0-435a-af67-11079f2b1404",
        "00000000-0000-0000-0000-000000000000",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_WAY
        VALUES ("53cd2b79-85ba-474d-9090-46ac0fe88f7f",
        4824.000000,
        3059.000000,
        "7bd1fcbb-abc0-435a-af67-11079f2b1404",
        "00000000-0000-0000-0000-000000000000",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_GE
        VALUES (0.000000,
        0.000000,
        "7bd1fcbb-abc0-435a-af67-11079f2b1404",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("7bd1fcbb-abc0-435a-af67-11079f2b1404",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_CON
        VALUES ("bc2759d4-1947-4b2d-b842-9faece1ecc82",
        4994.000000,
        3059.000000,
        "7bd1fcbb-abc0-435a-af67-11079f2b1404");
    INSERT INTO DIM_ED
        VALUES ("26b28f41-8966-4148-98f5-91f5505b5c92",
        "8d6716fa-92c3-46e4-8116-2ab556e15f4e",
        "7bd1fcbb-abc0-435a-af67-11079f2b1404");
    INSERT INTO O_OBJ
        VALUES ("7ef7999e-5513-4984-8744-9c1a5cf46412",
        'Supertype',
        3,
        'Supertype',
        '',
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO O_REF
        VALUES ("7ef7999e-5513-4984-8744-9c1a5cf46412",
        "419dc876-6997-44cb-a671-41acc466044a",
        0,
        "ee277c43-a11a-4ac9-bc82-2bb8a82fd437",
        "ca692c8a-5b63-4c1c-b24e-c99f10a22360",
        "dfca81f1-7154-44ce-90e1-66b28dd10093",
        "5b750bea-fdb5-42f2-83fe-dcbf34b0f73b",
        "990c9f1b-71a8-4246-af0e-de20a069e784",
        "2e2f0436-ad26-449f-9fbc-dfcfc110c5c2",
        "00000000-0000-0000-0000-000000000000",
        0,
        '',
        'Subtype',
        'Id',
        'R2');
    INSERT INTO O_RATTR
        VALUES ("990c9f1b-71a8-4246-af0e-de20a069e784",
        "7ef7999e-5513-4984-8744-9c1a5cf46412",
        "ee277c43-a11a-4ac9-bc82-2bb8a82fd437",
        "419dc876-6997-44cb-a671-41acc466044a",
        1,
        'Id');
    INSERT INTO O_ATTR
        VALUES ("990c9f1b-71a8-4246-af0e-de20a069e784",
        "7ef7999e-5513-4984-8744-9c1a5cf46412",
        "00000000-0000-0000-0000-000000000000",
        'Id',
        '',
        '',
        'Id',
        0,
        "ba5eda7a-def5-0000-0000-000000000007",
        '',
        '');
    INSERT INTO O_ID
        VALUES (0,
        "7ef7999e-5513-4984-8744-9c1a5cf46412");
    INSERT INTO O_OIDA
        VALUES ("990c9f1b-71a8-4246-af0e-de20a069e784",
        "7ef7999e-5513-4984-8744-9c1a5cf46412",
        0,
        'Id');
    INSERT INTO O_ID
        VALUES (1,
        "7ef7999e-5513-4984-8744-9c1a5cf46412");
    INSERT INTO O_ID
        VALUES (2,
        "7ef7999e-5513-4984-8744-9c1a5cf46412");
    INSERT INTO PE_PE
        VALUES ("7ef7999e-5513-4984-8744-9c1a5cf46412",
        1,
        "b48a6732-c56c-4e98-8773-afe91fcb30e4",
        "00000000-0000-0000-0000-000000000000",
        4);
    INSERT INTO GD_GE
        VALUES ("79aca22c-cf37-4577-ba92-e707cb1a5a00",
        "1344bf4e-528f-4e2b-b8cc-4db9e48e1967",
        "7ef7999e-5513-4984-8744-9c1a5cf46412",
        21,
        0,
        'Test_Schema_Gen::Package::Supertype');
    INSERT INTO GD_SHP
        VALUES ("79aca22c-cf37-4577-ba92-e707cb1a5a00");
    INSERT INTO GD_NCS
        VALUES ("79aca22c-cf37-4577-ba92-e707cb1a5a00");
    INSERT INTO DIM_ND
        VALUES (204.000000,
        156.000000,
        "79aca22c-cf37-4577-ba92-e707cb1a5a00");
    INSERT INTO DIM_GE
        VALUES (4248.000000,
        3384.000000,
        "79aca22c-cf37-4577-ba92-e707cb1a5a00",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("79aca22c-cf37-4577-ba92-e707cb1a5a00",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_CON
        VALUES ("600d4cd2-9ac4-4b2a-9f34-04e21b7b9e2e",
        4452.000000,
        3456.000000,
        "79aca22c-cf37-4577-ba92-e707cb1a5a00");
    INSERT INTO DIM_CON
        VALUES ("5d0a2f7c-52a1-4a2a-b547-8698a26116d6",
        4344.000000,
        3384.000000,
        "79aca22c-cf37-4577-ba92-e707cb1a5a00");
    INSERT INTO O_OBJ
        VALUES ("419dc876-6997-44cb-a671-41acc466044a",
        'Subtype',
        4,
        'Subtype',
        '',
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO O_NBATTR
        VALUES ("ee277c43-a11a-4ac9-bc82-2bb8a82fd437",
        "419dc876-6997-44cb-a671-41acc466044a");
    INSERT INTO O_BATTR
        VALUES ("ee277c43-a11a-4ac9-bc82-2bb8a82fd437",
        "419dc876-6997-44cb-a671-41acc466044a");
    INSERT INTO O_ATTR
        VALUES ("ee277c43-a11a-4ac9-bc82-2bb8a82fd437",
        "419dc876-6997-44cb-a671-41acc466044a",
        "00000000-0000-0000-0000-000000000000",
        'Id',
        '',
        '',
        'Id',
        0,
        "ba5eda7a-def5-0000-0000-000000000005",
        '',
        '');
    INSERT INTO O_ID
        VALUES (0,
        "419dc876-6997-44cb-a671-41acc466044a");
    INSERT INTO O_OIDA
        VALUES ("ee277c43-a11a-4ac9-bc82-2bb8a82fd437",
        "419dc876-6997-44cb-a671-41acc466044a",
        0,
        'Id');
    INSERT INTO O_ID
        VALUES (1,
        "419dc876-6997-44cb-a671-41acc466044a");
    INSERT INTO O_ID
        VALUES (2,
        "419dc876-6997-44cb-a671-41acc466044a");
    INSERT INTO PE_PE
        VALUES ("419dc876-6997-44cb-a671-41acc466044a",
        1,
        "b48a6732-c56c-4e98-8773-afe91fcb30e4",
        "00000000-0000-0000-0000-000000000000",
        4);
    INSERT INTO GD_GE
        VALUES ("89013d61-2e68-484d-9cd1-5b8a45e822e5",
        "1344bf4e-528f-4e2b-b8cc-4db9e48e1967",
        "419dc876-6997-44cb-a671-41acc466044a",
        21,
        0,
        'Test_Schema_Gen::Package::Subtype');
    INSERT INTO GD_SHP
        VALUES ("89013d61-2e68-484d-9cd1-5b8a45e822e5");
    INSERT INTO GD_NCS
        VALUES ("89013d61-2e68-484d-9cd1-5b8a45e822e5");
    INSERT INTO DIM_ND
        VALUES (204.000000,
        144.000000,
        "89013d61-2e68-484d-9cd1-5b8a45e822e5");
    INSERT INTO DIM_GE
        VALUES (4752.000000,
        3384.000000,
        "89013d61-2e68-484d-9cd1-5b8a45e822e5",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("89013d61-2e68-484d-9cd1-5b8a45e822e5",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_CON
        VALUES ("31631bcb-2ac4-4d50-9642-9c8d19567a55",
        4752.000000,
        3456.000000,
        "89013d61-2e68-484d-9cd1-5b8a45e822e5");
    INSERT INTO R_REL
        VALUES ("ca692c8a-5b63-4c1c-b24e-c99f10a22360",
        2,
        '',
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO R_SUBSUP
        VALUES ("ca692c8a-5b63-4c1c-b24e-c99f10a22360");
    INSERT INTO R_SUPER
        VALUES ("419dc876-6997-44cb-a671-41acc466044a",
        "ca692c8a-5b63-4c1c-b24e-c99f10a22360",
        "5b750bea-fdb5-42f2-83fe-dcbf34b0f73b");
    INSERT INTO O_RTIDA
        VALUES ("ee277c43-a11a-4ac9-bc82-2bb8a82fd437",
        "419dc876-6997-44cb-a671-41acc466044a",
        0,
        "ca692c8a-5b63-4c1c-b24e-c99f10a22360",
        "5b750bea-fdb5-42f2-83fe-dcbf34b0f73b");
    INSERT INTO R_RTO
        VALUES ("419dc876-6997-44cb-a671-41acc466044a",
        "ca692c8a-5b63-4c1c-b24e-c99f10a22360",
        "5b750bea-fdb5-42f2-83fe-dcbf34b0f73b",
        0);
    INSERT INTO R_OIR
        VALUES ("419dc876-6997-44cb-a671-41acc466044a",
        "ca692c8a-5b63-4c1c-b24e-c99f10a22360",
        "5b750bea-fdb5-42f2-83fe-dcbf34b0f73b",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO R_SUB
        VALUES ("7ef7999e-5513-4984-8744-9c1a5cf46412",
        "ca692c8a-5b63-4c1c-b24e-c99f10a22360",
        "dfca81f1-7154-44ce-90e1-66b28dd10093");
    INSERT INTO R_RGO
        VALUES ("7ef7999e-5513-4984-8744-9c1a5cf46412",
        "ca692c8a-5b63-4c1c-b24e-c99f10a22360",
        "dfca81f1-7154-44ce-90e1-66b28dd10093");
    INSERT INTO R_OIR
        VALUES ("7ef7999e-5513-4984-8744-9c1a5cf46412",
        "ca692c8a-5b63-4c1c-b24e-c99f10a22360",
        "dfca81f1-7154-44ce-90e1-66b28dd10093",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO PE_PE
        VALUES ("ca692c8a-5b63-4c1c-b24e-c99f10a22360",
        1,
        "b48a6732-c56c-4e98-8773-afe91fcb30e4",
        "00000000-0000-0000-0000-000000000000",
        9);
    INSERT INTO GD_GE
        VALUES ("4de2c013-f1a6-4eda-b88d-44ce07f25e7e",
        "1344bf4e-528f-4e2b-b8cc-4db9e48e1967",
        "ca692c8a-5b63-4c1c-b24e-c99f10a22360",
        36,
        0,
        'Test_Schema_Gen::Package::R2');
    INSERT INTO GD_CON
        VALUES ("4de2c013-f1a6-4eda-b88d-44ce07f25e7e",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_CTXT
        VALUES ("69027323-0038-4e79-a453-bd46450bee6c",
        "4de2c013-f1a6-4eda-b88d-44ce07f25e7e",
        1,
        0.000000,
        0.000000);
    INSERT INTO DIM_ND
        VALUES (0.000000,
        0.000000,
        "69027323-0038-4e79-a453-bd46450bee6c");
    INSERT INTO DIM_GE
        VALUES (0.000000,
        0.000000,
        "69027323-0038-4e79-a453-bd46450bee6c",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("69027323-0038-4e79-a453-bd46450bee6c",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_CTXT
        VALUES ("2c6c2ec4-539d-47d6-8227-45ab1e368f63",
        "4de2c013-f1a6-4eda-b88d-44ce07f25e7e",
        3,
        0.000000,
        0.000000);
    INSERT INTO DIM_ND
        VALUES (0.000000,
        0.000000,
        "2c6c2ec4-539d-47d6-8227-45ab1e368f63");
    INSERT INTO DIM_GE
        VALUES (0.000000,
        0.000000,
        "2c6c2ec4-539d-47d6-8227-45ab1e368f63",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("2c6c2ec4-539d-47d6-8227-45ab1e368f63",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_CTXT
        VALUES ("2d996854-73d5-49fa-bcaa-c1ad545c06f7",
        "4de2c013-f1a6-4eda-b88d-44ce07f25e7e",
        2,
        0.000000,
        0.000000);
    INSERT INTO DIM_ND
        VALUES (0.000000,
        0.000000,
        "2d996854-73d5-49fa-bcaa-c1ad545c06f7");
    INSERT INTO DIM_GE
        VALUES (4690.000000,
        3466.000000,
        "2d996854-73d5-49fa-bcaa-c1ad545c06f7",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("2d996854-73d5-49fa-bcaa-c1ad545c06f7",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_LS
        VALUES ("fd2cbf3c-464d-4edf-b0e6-eddf3419f6a8",
        "4de2c013-f1a6-4eda-b88d-44ce07f25e7e",
        "00000000-0000-0000-0000-000000000000",
        "084b93a5-1703-4f1e-9919-78c736fea417",
        "f7ffc992-9a46-40f4-be36-2f23fd77226b");
    INSERT INTO GD_AOS
        VALUES ("e1eb1982-33ca-4f6d-a252-27f7a81ce028",
        "fd2cbf3c-464d-4edf-b0e6-eddf3419f6a8");
    INSERT INTO DIM_WAY
        VALUES ("084b93a5-1703-4f1e-9919-78c736fea417",
        4752.000000,
        3456.000000,
        "4de2c013-f1a6-4eda-b88d-44ce07f25e7e",
        "00000000-0000-0000-0000-000000000000",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_WAY
        VALUES ("f7ffc992-9a46-40f4-be36-2f23fd77226b",
        4680.000000,
        3456.000000,
        "4de2c013-f1a6-4eda-b88d-44ce07f25e7e",
        "00000000-0000-0000-0000-000000000000",
        "084b93a5-1703-4f1e-9919-78c736fea417");
    INSERT INTO DIM_GE
        VALUES (0.000000,
        0.000000,
        "4de2c013-f1a6-4eda-b88d-44ce07f25e7e",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("4de2c013-f1a6-4eda-b88d-44ce07f25e7e",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_CON
        VALUES ("e1eb1982-33ca-4f6d-a252-27f7a81ce028",
        4680.000000,
        3456.000000,
        "4de2c013-f1a6-4eda-b88d-44ce07f25e7e");
    INSERT INTO DIM_ED
        VALUES ("31631bcb-2ac4-4d50-9642-9c8d19567a55",
        "00000000-0000-0000-0000-000000000000",
        "4de2c013-f1a6-4eda-b88d-44ce07f25e7e");
    INSERT INTO GD_GE
        VALUES ("efbe981c-68c9-40a1-a16f-6c7ccebdc003",
        "1344bf4e-528f-4e2b-b8cc-4db9e48e1967",
        "dfca81f1-7154-44ce-90e1-66b28dd10093",
        35,
        0,
        'Test_Schema_Gen::Package::R2::Supertype');
    INSERT INTO GD_CON
        VALUES ("efbe981c-68c9-40a1-a16f-6c7ccebdc003",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_CTXT
        VALUES ("a0df184b-f045-4eb9-9976-f6b51a8154fa",
        "efbe981c-68c9-40a1-a16f-6c7ccebdc003",
        1,
        0.000000,
        0.000000);
    INSERT INTO DIM_ND
        VALUES (0.000000,
        0.000000,
        "a0df184b-f045-4eb9-9976-f6b51a8154fa");
    INSERT INTO DIM_GE
        VALUES (0.000000,
        0.000000,
        "a0df184b-f045-4eb9-9976-f6b51a8154fa",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("a0df184b-f045-4eb9-9976-f6b51a8154fa",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_CTXT
        VALUES ("d2017075-da48-487b-834e-be43bb16b1a1",
        "efbe981c-68c9-40a1-a16f-6c7ccebdc003",
        3,
        0.000000,
        0.000000);
    INSERT INTO DIM_ND
        VALUES (0.000000,
        0.000000,
        "d2017075-da48-487b-834e-be43bb16b1a1");
    INSERT INTO DIM_GE
        VALUES (0.000000,
        0.000000,
        "d2017075-da48-487b-834e-be43bb16b1a1",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("d2017075-da48-487b-834e-be43bb16b1a1",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_CTXT
        VALUES ("a847a23e-35ae-4a70-863e-a003fe46297e",
        "efbe981c-68c9-40a1-a16f-6c7ccebdc003",
        2,
        0.000000,
        0.000000);
    INSERT INTO DIM_ND
        VALUES (0.000000,
        0.000000,
        "a847a23e-35ae-4a70-863e-a003fe46297e");
    INSERT INTO DIM_GE
        VALUES (0.000000,
        0.000000,
        "a847a23e-35ae-4a70-863e-a003fe46297e",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("a847a23e-35ae-4a70-863e-a003fe46297e",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_LS
        VALUES ("bf5f42ff-588f-4a88-92d8-42f6820f6ecb",
        "efbe981c-68c9-40a1-a16f-6c7ccebdc003",
        "00000000-0000-0000-0000-000000000000",
        "9e96af85-25de-44ec-bf21-b42b433ebffa",
        "ebdb9a6d-6f16-43fc-834d-2068c9a99b92");
    INSERT INTO DIM_WAY
        VALUES ("9e96af85-25de-44ec-bf21-b42b433ebffa",
        4452.000000,
        3456.000000,
        "efbe981c-68c9-40a1-a16f-6c7ccebdc003",
        "00000000-0000-0000-0000-000000000000",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_WAY
        VALUES ("ebdb9a6d-6f16-43fc-834d-2068c9a99b92",
        4680.000000,
        3456.000000,
        "efbe981c-68c9-40a1-a16f-6c7ccebdc003",
        "00000000-0000-0000-0000-000000000000",
        "9e96af85-25de-44ec-bf21-b42b433ebffa");
    INSERT INTO DIM_GE
        VALUES (0.000000,
        0.000000,
        "efbe981c-68c9-40a1-a16f-6c7ccebdc003",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("efbe981c-68c9-40a1-a16f-6c7ccebdc003",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ED
        VALUES ("600d4cd2-9ac4-4b2a-9f34-04e21b7b9e2e",
        "e1eb1982-33ca-4f6d-a252-27f7a81ce028",
        "efbe981c-68c9-40a1-a16f-6c7ccebdc003");
    INSERT INTO R_REL
        VALUES ("3ae58522-7f90-48b3-85b4-35df51c6192a",
        3,
        '',
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO R_SIMP
        VALUES ("3ae58522-7f90-48b3-85b4-35df51c6192a");
    INSERT INTO R_FORM
        VALUES ("3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        "3ae58522-7f90-48b3-85b4-35df51c6192a",
        "b3f14c88-fd1b-4aa8-a5ae-15d202bee5d6",
        1,
        1,
        '');
    INSERT INTO R_RGO
        VALUES ("3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        "3ae58522-7f90-48b3-85b4-35df51c6192a",
        "b3f14c88-fd1b-4aa8-a5ae-15d202bee5d6");
    INSERT INTO R_OIR
        VALUES ("3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        "3ae58522-7f90-48b3-85b4-35df51c6192a",
        "b3f14c88-fd1b-4aa8-a5ae-15d202bee5d6",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO R_PART
        VALUES ("7ef7999e-5513-4984-8744-9c1a5cf46412",
        "3ae58522-7f90-48b3-85b4-35df51c6192a",
        "9d8b6602-75c8-44b6-ac4f-9da04573b957",
        0,
        0,
        '');
    INSERT INTO O_RTIDA
        VALUES ("990c9f1b-71a8-4246-af0e-de20a069e784",
        "7ef7999e-5513-4984-8744-9c1a5cf46412",
        0,
        "3ae58522-7f90-48b3-85b4-35df51c6192a",
        "9d8b6602-75c8-44b6-ac4f-9da04573b957");
    INSERT INTO R_RTO
        VALUES ("7ef7999e-5513-4984-8744-9c1a5cf46412",
        "3ae58522-7f90-48b3-85b4-35df51c6192a",
        "9d8b6602-75c8-44b6-ac4f-9da04573b957",
        0);
    INSERT INTO R_OIR
        VALUES ("7ef7999e-5513-4984-8744-9c1a5cf46412",
        "3ae58522-7f90-48b3-85b4-35df51c6192a",
        "9d8b6602-75c8-44b6-ac4f-9da04573b957",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO PE_PE
        VALUES ("3ae58522-7f90-48b3-85b4-35df51c6192a",
        1,
        "b48a6732-c56c-4e98-8773-afe91fcb30e4",
        "00000000-0000-0000-0000-000000000000",
        9);
    INSERT INTO GD_GE
        VALUES ("6ba08f56-c2f9-4a88-9b58-f704f6854e52",
        "1344bf4e-528f-4e2b-b8cc-4db9e48e1967",
        "3ae58522-7f90-48b3-85b4-35df51c6192a",
        24,
        0,
        'Test_Schema_Gen::Package::R3');
    INSERT INTO GD_CON
        VALUES ("6ba08f56-c2f9-4a88-9b58-f704f6854e52",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_CTXT
        VALUES ("8dfb356b-0d77-46ea-8855-a5ba37d8ff15",
        "6ba08f56-c2f9-4a88-9b58-f704f6854e52",
        1,
        0.000000,
        0.000000);
    INSERT INTO DIM_ND
        VALUES (0.000000,
        0.000000,
        "8dfb356b-0d77-46ea-8855-a5ba37d8ff15");
    INSERT INTO DIM_GE
        VALUES (0.000000,
        0.000000,
        "8dfb356b-0d77-46ea-8855-a5ba37d8ff15",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("8dfb356b-0d77-46ea-8855-a5ba37d8ff15",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_CTXT
        VALUES ("3c1d46f9-ab6e-490a-a8e3-162d318c2012",
        "6ba08f56-c2f9-4a88-9b58-f704f6854e52",
        3,
        0.000000,
        0.000000);
    INSERT INTO DIM_ND
        VALUES (0.000000,
        0.000000,
        "3c1d46f9-ab6e-490a-a8e3-162d318c2012");
    INSERT INTO DIM_GE
        VALUES (4305.000000,
        3316.000000,
        "3c1d46f9-ab6e-490a-a8e3-162d318c2012",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("3c1d46f9-ab6e-490a-a8e3-162d318c2012",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_CTXT
        VALUES ("7de675d0-3599-4597-af10-f95c19e4b88d",
        "6ba08f56-c2f9-4a88-9b58-f704f6854e52",
        2,
        0.000000,
        0.000000);
    INSERT INTO DIM_ND
        VALUES (0.000000,
        0.000000,
        "7de675d0-3599-4597-af10-f95c19e4b88d");
    INSERT INTO DIM_GE
        VALUES (0.000000,
        0.000000,
        "7de675d0-3599-4597-af10-f95c19e4b88d",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("7de675d0-3599-4597-af10-f95c19e4b88d",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_LS
        VALUES ("fe7c1f3d-0d73-4636-a75c-7c422e81cea4",
        "6ba08f56-c2f9-4a88-9b58-f704f6854e52",
        "00000000-0000-0000-0000-000000000000",
        "2b37073b-2797-4ce1-a214-89176c2e1eab",
        "39bb5949-4f3b-4816-b225-70804b654aa0");
    INSERT INTO DIM_WAY
        VALUES ("2b37073b-2797-4ce1-a214-89176c2e1eab",
        4344.000000,
        3264.000000,
        "6ba08f56-c2f9-4a88-9b58-f704f6854e52",
        "00000000-0000-0000-0000-000000000000",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_WAY
        VALUES ("39bb5949-4f3b-4816-b225-70804b654aa0",
        4344.000000,
        3384.000000,
        "6ba08f56-c2f9-4a88-9b58-f704f6854e52",
        "00000000-0000-0000-0000-000000000000",
        "2b37073b-2797-4ce1-a214-89176c2e1eab");
    INSERT INTO DIM_GE
        VALUES (0.000000,
        0.000000,
        "6ba08f56-c2f9-4a88-9b58-f704f6854e52",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("6ba08f56-c2f9-4a88-9b58-f704f6854e52",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ED
        VALUES ("695fd096-c898-4f1e-9505-a036da9cf287",
        "5d0a2f7c-52a1-4a2a-b547-8698a26116d6",
        "6ba08f56-c2f9-4a88-9b58-f704f6854e52");
    INSERT INTO R_REL
        VALUES ("131ece0d-48e6-40d3-a3c2-baac77f9f32c",
        4,
        '',
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO R_SIMP
        VALUES ("131ece0d-48e6-40d3-a3c2-baac77f9f32c");
    INSERT INTO R_PART
        VALUES ("3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        "131ece0d-48e6-40d3-a3c2-baac77f9f32c",
        "fe0e8e09-edef-4be6-b8d7-0cb86053f640",
        0,
        0,
        '');
    INSERT INTO O_RTIDA
        VALUES ("f94afef8-ed1a-4b9b-bb29-36149617b861",
        "3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        0,
        "131ece0d-48e6-40d3-a3c2-baac77f9f32c",
        "fe0e8e09-edef-4be6-b8d7-0cb86053f640");
    INSERT INTO R_RTO
        VALUES ("3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        "131ece0d-48e6-40d3-a3c2-baac77f9f32c",
        "fe0e8e09-edef-4be6-b8d7-0cb86053f640",
        0);
    INSERT INTO R_OIR
        VALUES ("3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        "131ece0d-48e6-40d3-a3c2-baac77f9f32c",
        "fe0e8e09-edef-4be6-b8d7-0cb86053f640",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO R_FORM
        VALUES ("68553234-715f-43ce-a1ce-4b93d6483cf5",
        "131ece0d-48e6-40d3-a3c2-baac77f9f32c",
        "fb42f65b-cd41-411a-b022-a3cf2f481a99",
        1,
        1,
        '');
    INSERT INTO R_RGO
        VALUES ("68553234-715f-43ce-a1ce-4b93d6483cf5",
        "131ece0d-48e6-40d3-a3c2-baac77f9f32c",
        "fb42f65b-cd41-411a-b022-a3cf2f481a99");
    INSERT INTO R_OIR
        VALUES ("68553234-715f-43ce-a1ce-4b93d6483cf5",
        "131ece0d-48e6-40d3-a3c2-baac77f9f32c",
        "fb42f65b-cd41-411a-b022-a3cf2f481a99",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO PE_PE
        VALUES ("131ece0d-48e6-40d3-a3c2-baac77f9f32c",
        1,
        "b48a6732-c56c-4e98-8773-afe91fcb30e4",
        "00000000-0000-0000-0000-000000000000",
        9);
    INSERT INTO GD_GE
        VALUES ("a099b13e-ed73-489b-a170-610bc3665d56",
        "1344bf4e-528f-4e2b-b8cc-4db9e48e1967",
        "131ece0d-48e6-40d3-a3c2-baac77f9f32c",
        24,
        0,
        'Test_Schema_Gen::Package::R4');
    INSERT INTO GD_CON
        VALUES ("a099b13e-ed73-489b-a170-610bc3665d56",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_CTXT
        VALUES ("35f54702-d6fc-47af-908b-155701489c82",
        "a099b13e-ed73-489b-a170-610bc3665d56",
        1,
        0.000000,
        0.000000);
    INSERT INTO DIM_ND
        VALUES (0.000000,
        0.000000,
        "35f54702-d6fc-47af-908b-155701489c82");
    INSERT INTO DIM_GE
        VALUES (0.000000,
        0.000000,
        "35f54702-d6fc-47af-908b-155701489c82",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("35f54702-d6fc-47af-908b-155701489c82",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_CTXT
        VALUES ("09c808ad-4cd1-463a-abdf-af47037a9994",
        "a099b13e-ed73-489b-a170-610bc3665d56",
        3,
        0.000000,
        0.000000);
    INSERT INTO DIM_ND
        VALUES (0.000000,
        0.000000,
        "09c808ad-4cd1-463a-abdf-af47037a9994");
    INSERT INTO DIM_GE
        VALUES (4589.000000,
        3162.000000,
        "09c808ad-4cd1-463a-abdf-af47037a9994",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("09c808ad-4cd1-463a-abdf-af47037a9994",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_CTXT
        VALUES ("ee5cc3d8-26bd-4f7f-8f28-7af26484d739",
        "a099b13e-ed73-489b-a170-610bc3665d56",
        2,
        0.000000,
        0.000000);
    INSERT INTO DIM_ND
        VALUES (0.000000,
        0.000000,
        "ee5cc3d8-26bd-4f7f-8f28-7af26484d739");
    INSERT INTO DIM_GE
        VALUES (0.000000,
        0.000000,
        "ee5cc3d8-26bd-4f7f-8f28-7af26484d739",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("ee5cc3d8-26bd-4f7f-8f28-7af26484d739",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_LS
        VALUES ("62c05ce8-3657-46de-92ab-5d263d9e62b1",
        "a099b13e-ed73-489b-a170-610bc3665d56",
        "00000000-0000-0000-0000-000000000000",
        "7d8f35b5-b078-4369-841d-04f4476389d4",
        "a69e3281-962a-43cf-977b-e541f46f73dc");
    INSERT INTO DIM_WAY
        VALUES ("7d8f35b5-b078-4369-841d-04f4476389d4",
        4452.000000,
        3204.000000,
        "a099b13e-ed73-489b-a170-610bc3665d56",
        "00000000-0000-0000-0000-000000000000",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_WAY
        VALUES ("a69e3281-962a-43cf-977b-e541f46f73dc",
        4740.000000,
        3204.000000,
        "a099b13e-ed73-489b-a170-610bc3665d56",
        "00000000-0000-0000-0000-000000000000",
        "7d8f35b5-b078-4369-841d-04f4476389d4");
    INSERT INTO DIM_GE
        VALUES (0.000000,
        0.000000,
        "a099b13e-ed73-489b-a170-610bc3665d56",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("a099b13e-ed73-489b-a170-610bc3665d56",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ED
        VALUES ("9e246129-772e-4e7e-9b8b-8dd68e80b065",
        "6ef83aa3-47e5-43f8-bbfa-058e9a2032f5",
        "a099b13e-ed73-489b-a170-610bc3665d56");
    INSERT INTO O_OBJ
        VALUES ("bd62e326-bbc2-4c55-8ee1-69a59e5146d3",
        'Assoc_Class',
        5,
        'Assoc_Class',
        '',
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO O_REF
        VALUES ("bd62e326-bbc2-4c55-8ee1-69a59e5146d3",
        "68553234-715f-43ce-a1ce-4b93d6483cf5",
        0,
        "64853c2b-640f-4738-a363-40892f8d4757",
        "4cfe4e7d-1919-4ef2-a4db-03c85c772b2a",
        "bc18e358-1a8c-41d3-9ed5-5013ba99339c",
        "04310dd4-9b14-4b59-9a59-9e9dc5d99468",
        "9011bff4-2a98-4e04-956a-40afb80db518",
        "da2bbbb4-1f61-4f3d-bd41-c13d075b9de3",
        "00000000-0000-0000-0000-000000000000",
        0,
        '',
        'Reflexive_Class',
        'Id',
        'R1.''other''');
    INSERT INTO O_RATTR
        VALUES ("9011bff4-2a98-4e04-956a-40afb80db518",
        "bd62e326-bbc2-4c55-8ee1-69a59e5146d3",
        "f94afef8-ed1a-4b9b-bb29-36149617b861",
        "3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        1,
        'Id');
    INSERT INTO O_ATTR
        VALUES ("9011bff4-2a98-4e04-956a-40afb80db518",
        "bd62e326-bbc2-4c55-8ee1-69a59e5146d3",
        "00000000-0000-0000-0000-000000000000",
        'Other_Id',
        '',
        'Other_',
        'Id',
        1,
        "ba5eda7a-def5-0000-0000-000000000007",
        '',
        '');
    INSERT INTO O_REF
        VALUES ("bd62e326-bbc2-4c55-8ee1-69a59e5146d3",
        "68553234-715f-43ce-a1ce-4b93d6483cf5",
        0,
        "64853c2b-640f-4738-a363-40892f8d4757",
        "4cfe4e7d-1919-4ef2-a4db-03c85c772b2a",
        "bc18e358-1a8c-41d3-9ed5-5013ba99339c",
        "aeb07e49-c4f9-42dc-93d2-bf42134687b4",
        "86f8146a-5d3f-4ff0-9119-6338bcb1d53f",
        "fc3810e5-50ec-41f2-9998-27236801e3f4",
        "00000000-0000-0000-0000-000000000000",
        0,
        '',
        'Reflexive_Class',
        'Id',
        'R1.''one''');
    INSERT INTO O_RATTR
        VALUES ("86f8146a-5d3f-4ff0-9119-6338bcb1d53f",
        "bd62e326-bbc2-4c55-8ee1-69a59e5146d3",
        "f94afef8-ed1a-4b9b-bb29-36149617b861",
        "3beb857e-8f3e-41c8-a1d5-e3dd66d836db",
        1,
        'Id');
    INSERT INTO O_ATTR
        VALUES ("86f8146a-5d3f-4ff0-9119-6338bcb1d53f",
        "bd62e326-bbc2-4c55-8ee1-69a59e5146d3",
        "9011bff4-2a98-4e04-956a-40afb80db518",
        'One_Id',
        '',
        'One_',
        'Id',
        1,
        "ba5eda7a-def5-0000-0000-000000000007",
        '',
        '');
    INSERT INTO O_ID
        VALUES (0,
        "bd62e326-bbc2-4c55-8ee1-69a59e5146d3");
    INSERT INTO O_OIDA
        VALUES ("9011bff4-2a98-4e04-956a-40afb80db518",
        "bd62e326-bbc2-4c55-8ee1-69a59e5146d3",
        0,
        'Other_Id');
    INSERT INTO O_OIDA
        VALUES ("86f8146a-5d3f-4ff0-9119-6338bcb1d53f",
        "bd62e326-bbc2-4c55-8ee1-69a59e5146d3",
        0,
        'One_Id');
    INSERT INTO O_ID
        VALUES (1,
        "bd62e326-bbc2-4c55-8ee1-69a59e5146d3");
    INSERT INTO O_ID
        VALUES (2,
        "bd62e326-bbc2-4c55-8ee1-69a59e5146d3");
    INSERT INTO PE_PE
        VALUES ("bd62e326-bbc2-4c55-8ee1-69a59e5146d3",
        1,
        "b48a6732-c56c-4e98-8773-afe91fcb30e4",
        "00000000-0000-0000-0000-000000000000",
        4);
    INSERT INTO GD_GE
        VALUES ("ff43aac8-2d20-4e64-b96a-4b5499633df3",
        "1344bf4e-528f-4e2b-b8cc-4db9e48e1967",
        "bd62e326-bbc2-4c55-8ee1-69a59e5146d3",
        21,
        0,
        'Test_Schema_Gen::Package::Assoc_Class');
    INSERT INTO GD_SHP
        VALUES ("ff43aac8-2d20-4e64-b96a-4b5499633df3");
    INSERT INTO GD_NCS
        VALUES ("ff43aac8-2d20-4e64-b96a-4b5499633df3");
    INSERT INTO DIM_ND
        VALUES (204.000000,
        144.000000,
        "ff43aac8-2d20-4e64-b96a-4b5499633df3");
    INSERT INTO DIM_GE
        VALUES (5052.000000,
        2892.000000,
        "ff43aac8-2d20-4e64-b96a-4b5499633df3",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("ff43aac8-2d20-4e64-b96a-4b5499633df3",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_CON
        VALUES ("d8027605-c5c5-4f0f-9c1a-18011924e4f7",
        5052.000000,
        3034.000000,
        "ff43aac8-2d20-4e64-b96a-4b5499633df3");
    INSERT INTO GD_GE
        VALUES ("df68e95e-64e3-4f29-a097-a408048a4399",
        "1344bf4e-528f-4e2b-b8cc-4db9e48e1967",
        "4cfe4e7d-1919-4ef2-a4db-03c85c772b2a",
        34,
        0,
        'Test_Schema_Gen::Package::R1::Assoc_Class');
    INSERT INTO GD_CON
        VALUES ("df68e95e-64e3-4f29-a097-a408048a4399",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_CTXT
        VALUES ("3867a3c3-9d8a-4b31-80c0-ab20ec032c14",
        "df68e95e-64e3-4f29-a097-a408048a4399",
        1,
        0.000000,
        0.000000);
    INSERT INTO DIM_ND
        VALUES (0.000000,
        0.000000,
        "3867a3c3-9d8a-4b31-80c0-ab20ec032c14");
    INSERT INTO DIM_GE
        VALUES (0.000000,
        0.000000,
        "3867a3c3-9d8a-4b31-80c0-ab20ec032c14",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("3867a3c3-9d8a-4b31-80c0-ab20ec032c14",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_CTXT
        VALUES ("b4bd7874-bb29-4c55-ad5a-dd0c39ffa704",
        "df68e95e-64e3-4f29-a097-a408048a4399",
        3,
        0.000000,
        0.000000);
    INSERT INTO DIM_ND
        VALUES (0.000000,
        0.000000,
        "b4bd7874-bb29-4c55-ad5a-dd0c39ffa704");
    INSERT INTO DIM_GE
        VALUES (0.000000,
        0.000000,
        "b4bd7874-bb29-4c55-ad5a-dd0c39ffa704",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("b4bd7874-bb29-4c55-ad5a-dd0c39ffa704",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_CTXT
        VALUES ("654909ae-f193-4496-8254-34f8d3909641",
        "df68e95e-64e3-4f29-a097-a408048a4399",
        2,
        0.000000,
        0.000000);
    INSERT INTO DIM_ND
        VALUES (0.000000,
        0.000000,
        "654909ae-f193-4496-8254-34f8d3909641");
    INSERT INTO DIM_GE
        VALUES (0.000000,
        0.000000,
        "654909ae-f193-4496-8254-34f8d3909641",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("654909ae-f193-4496-8254-34f8d3909641",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO GD_LS
        VALUES ("e8c9a444-4942-4b30-bb2e-88684284d17d",
        "df68e95e-64e3-4f29-a097-a408048a4399",
        "00000000-0000-0000-0000-000000000000",
        "c71b6092-0b55-4fc3-8365-b0c8c301d4e7",
        "5a6aa846-482c-45d3-8da2-0b08a214e22b");
    INSERT INTO DIM_WAY
        VALUES ("c71b6092-0b55-4fc3-8365-b0c8c301d4e7",
        5052.000000,
        3034.000000,
        "df68e95e-64e3-4f29-a097-a408048a4399",
        "00000000-0000-0000-0000-000000000000",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_WAY
        VALUES ("5a6aa846-482c-45d3-8da2-0b08a214e22b",
        4994.000000,
        3059.000000,
        "df68e95e-64e3-4f29-a097-a408048a4399",
        "00000000-0000-0000-0000-000000000000",
        "c71b6092-0b55-4fc3-8365-b0c8c301d4e7");
    INSERT INTO DIM_GE
        VALUES (0.000000,
        0.000000,
        "df68e95e-64e3-4f29-a097-a408048a4399",
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ELE
        VALUES ("df68e95e-64e3-4f29-a097-a408048a4399",
        0,
        "00000000-0000-0000-0000-000000000000");
    INSERT INTO DIM_ED
        VALUES ("d8027605-c5c5-4f0f-9c1a-18011924e4f7",
        "bc2759d4-1947-4b2d-b842-9faece1ecc82",
        "df68e95e-64e3-4f29-a097-a408048a4399");
    """
    
    def test_simple_class(self):
        l = bridgepoint.ModelLoader()
        l.input(self.__doc__, '<test model>')
        m = l.build_component()
        
        cls = m.new('Class')
        self.assertTrue(cls.Id)
        
        supertype = m.new('Supertype')
        subtype = m.new('Subtype')
        self.assertTrue(xtuml.relate(supertype, subtype, 2))
        self.assertTrue(xtuml.relate(supertype, cls, 3))
        self.assertTrue(supertype.Id)
        self.assertTrue(subtype.Id)
        
        reflexive_class1 = m.new('Reflexive_Class')
        reflexive_class2 = m.new('Reflexive_Class')
        self.assertTrue(xtuml.relate(reflexive_class1, cls, 4))
        self.assertTrue(xtuml.relate(reflexive_class2, cls, 4))
        
        assoc_class = m.new('Assoc_Class')
        self.assertTrue(xtuml.relate(reflexive_class1, assoc_class, 1, 'one'))
        self.assertTrue(xtuml.relate(reflexive_class2, assoc_class, 1, 'other'))

        
if __name__ == "__main__":
    unittest.main()
    
