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

from tests.test_bridgepoint.utils import PrebuildFunctionTestCase
from tests.test_bridgepoint.utils import prebuild_docstring

from xtuml import navigate_one as one
from xtuml import relate
from xtuml import where_eq as where


class TestGenerate(PrebuildFunctionTestCase):

    def setUp(self):
        PrebuildFunctionTestCase.setUp(self)
        sm_sm = self.metamodel.new('SM_SM')
        o_obj = self.metamodel.new('O_OBJ', Key_Lett='A')
        pe_pe = self.metamodel.new('PE_PE')
        relate(pe_pe, o_obj, 8001)
        
        self.metamodel.new('SM_EVT',
                           SM_ID=sm_sm.SM_ID,
                           SMspd_ID=self.metamodel.id_generator.next(),
                           Numb=2,
                           Drv_Lbl='A2',
                           Mning='my_event')
        
        self.metamodel.new('SM_ASM',
                           Obj_ID=o_obj.Obj_ID,
                           SM_ID=sm_sm.SM_ID)
        
        
        
        sm_sm = self.metamodel.new('SM_SM')       
        o_obj = self.metamodel.new('O_OBJ', Key_Lett='B')
        pe_pe = self.metamodel.new('PE_PE')
        relate(pe_pe, o_obj, 8001)
        
        self.metamodel.new('SM_EVT',
                           SM_ID=sm_sm.SM_ID,
                           SMspd_ID=self.metamodel.id_generator.next(),
                           Numb=2,
                           Drv_Lbl='B2',
                           Mning='my_second_event')
        
        self.metamodel.new('SM_ISM',
                           Obj_ID=o_obj.Obj_ID,
                           SM_ID=sm_sm.SM_ID)
        
        
        sm_sm = self.metamodel.new('SM_SM')       
        o_obj = self.metamodel.new('O_OBJ', Key_Lett='C')
        pe_pe = self.metamodel.new('PE_PE')
        relate(pe_pe, o_obj, 8001)
        sm_evt = self.metamodel.new('SM_EVT',
                                    SM_ID=sm_sm.SM_ID,
                                    SMspd_ID=self.metamodel.id_generator.next(),
                                    Numb=1,
                                    Drv_Lbl='C1',
                                    Mning='my_third_event')
        
        s_dt = self.metamodel.select_any('S_DT', where(Name='boolean'))
        self.metamodel.new('SM_EVTDI',
                           SM_ID=sm_sm.SM_ID,
                           SMevt_ID=sm_evt.SMevt_ID,
                           DT_ID=s_dt.DT_ID,
                           Name='di1')
        
        self.metamodel.new('SM_ISM',
                           Obj_ID=o_obj.Obj_ID,
                           SM_ID=sm_sm.SM_ID)
        
    @prebuild_docstring
    def test_generate_to_class(self):
        '''
        generate A2:my_event() to A class;
        '''
        e_gar = self.metamodel.select_one('E_GAR')
        self.assertIsNotNone(e_gar)

        e_gsme = one(e_gar).E_GSME[705]()
        self.assertIsNotNone(e_gsme)
        
        e_ges = one(e_gsme).E_GES[703]()
        self.assertIsNotNone(e_ges)
        
        sm_evt = one(e_gsme).SM_EVT[707]()
        self.assertEqual(sm_evt.Numb, 2)
        self.assertEqual(sm_evt.Mning, 'my_event')
        
        e_ess = one(e_ges).E_ESS[701]()
        self.assertIsNotNone(e_ess)
        
        act_smt = one(e_ess).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
    @prebuild_docstring
    def test_generate_to_creator(self):
        '''
        generate B2:my_second_event() to B creator;
        '''
        e_gec = self.metamodel.select_one('E_GEC')
        self.assertIsNotNone(e_gec)

        e_gsme = one(e_gec).E_GSME[705]()
        self.assertIsNotNone(e_gsme)
        
        e_ges = one(e_gsme).E_GES[703]()
        self.assertIsNotNone(e_ges)
        
        sm_evt = one(e_gsme).SM_EVT[707]()
        self.assertEqual(sm_evt.Numb, 2)
        self.assertEqual(sm_evt.Mning, 'my_second_event')
        
        e_ess = one(e_ges).E_ESS[701]()
        self.assertIsNotNone(e_ess)
        
        act_smt = one(e_ess).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)

    @prebuild_docstring
    def test_generate_to_instance(self):
        '''
        create object instance b of B;
        generate B2:my_second_event() to b;
        '''
        e_gen = self.metamodel.select_one('E_GEN')
        self.assertIsNotNone(e_gen)

        v_var = one(e_gen).V_VAR[712]()
        self.assertEqual(v_var.Name, 'b')
        
        e_gsme = one(e_gen).E_GSME[705]()
        self.assertIsNotNone(e_gsme)
        
        e_ges = one(e_gsme).E_GES[703]()
        self.assertIsNotNone(e_ges)
        
        sm_evt = one(e_gsme).SM_EVT[707]()
        self.assertEqual(sm_evt.Numb, 2)
        self.assertEqual(sm_evt.Mning, 'my_second_event')
        
        e_ess = one(e_ges).E_ESS[701]()
        self.assertIsNotNone(e_ess)
        
        act_smt = one(e_ess).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)

    @prebuild_docstring
    def test_create_event_instance(self):
        '''
        create object instance b of B;
        create event instance e of B2:my_second_event() to b;
        '''
        e_cei = self.metamodel.select_one('E_CEI')
        self.assertIsNotNone(e_cei)

        v_var = one(e_cei).V_VAR[711]()
        self.assertEqual(v_var.Name, 'b')
        
        e_csme = one(e_cei).E_CSME[704]()
        self.assertIsNotNone(e_csme)
        
        e_ces = one(e_csme).E_CES[702]()
        self.assertTrue(e_ces.is_implicit)
        
        v_var = one(e_ces).V_VAR[710]()
        self.assertEqual(v_var.Name, 'e')
        
        sm_evt = one(e_csme).SM_EVT[706]()
        self.assertEqual(sm_evt.Numb, 2)
        self.assertEqual(sm_evt.Mning, 'my_second_event')
        
        e_ess = one(e_ces).E_ESS[701]()
        self.assertIsNotNone(e_ess)
        
    @prebuild_docstring
    def test_create_event_creator(self):
        '''
        create event instance e of B2:my_second_event() to B creator;
        '''
        e_cec = self.metamodel.select_one('E_CEC')
        self.assertIsNotNone(e_cec)

        e_csme = one(e_cec).E_CSME[704]()
        self.assertIsNotNone(e_csme)
        
        e_ces = one(e_csme).E_CES[702]()
        self.assertTrue(e_ces.is_implicit)
        
        v_var = one(e_ces).V_VAR[710]()
        self.assertEqual(v_var.Name, 'e')
        
        sm_evt = one(e_csme).SM_EVT[706]()
        self.assertEqual(sm_evt.Numb, 2)
        self.assertEqual(sm_evt.Mning, 'my_second_event')
        
        e_ess = one(e_ces).E_ESS[701]()
        self.assertIsNotNone(e_ess)
        
    @prebuild_docstring
    def test_create_event_class(self):
        '''
        create event instance e of A2:my_event() to A class;
        '''
        e_cea = self.metamodel.select_one('E_CEA')
        self.assertIsNotNone(e_cea)

        e_csme = one(e_cea).E_CSME[704]()
        self.assertIsNotNone(e_csme)
        
        e_ces = one(e_csme).E_CES[702]()
        self.assertTrue(e_ces.is_implicit)
        
        v_var = one(e_ces).V_VAR[710]()
        self.assertEqual(v_var.Name, 'e')
        
        sm_evt = one(e_csme).SM_EVT[706]()
        self.assertEqual(sm_evt.Numb, 2)
        self.assertEqual(sm_evt.Mning, 'my_event')
        
        e_ess = one(e_ces).E_ESS[701]()
        self.assertIsNotNone(e_ess)
        
    @prebuild_docstring
    def test_generate_existing_event(self):
        '''
        create object instance b of B;
        create event instance e of B2:my_second_event() to b;
        generate e;
        '''
        e_gpr = self.metamodel.select_one('E_GPR')
        self.assertIsNotNone(e_gpr)

        v_val = one(e_gpr).V_VAL[714]()
        self.assertIsNotNone(v_val)

    @prebuild_docstring
    def test_create_event_with_data_item(self):
        '''
        create event instance e of C1:my_third_event(di1: 1) to C creator;
        '''
        e_ess = self.metamodel.select_one('E_ESS')
        self.assertIsNotNone(e_ess)

        v_par = one(e_ess).V_PAR[700]()
        self.assertEqual(v_par.Name, 'di1')


if __name__ == "__main__":
    import logging
    import unittest
    
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
    
