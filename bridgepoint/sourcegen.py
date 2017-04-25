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

import logging

from xtuml import navigate_one as one
from xtuml import navigate_any as any
from xtuml import navigate_many as many
from xtuml import navigate_subtype as subtype

from xtuml.tools import Walker


logger = logging.getLogger(__name__)


class ActionTextGenWalker(Walker):
    '''
    Walk the bridgepoint metamodel and translate action code
    to its textual representation.
    '''
    def __init__(self, level=-1):
        Walker.__init__(self)
        self._buf = ''
        self._lvl = level
        
    def __str__(self):
        return self._buf
    
    def __repr__(self):
        return self._buf
    
    def buf(self, value, *args):
        self._buf += value
        self._buf += ''.join(args)
        
    def buf_linebreak(self, *args):
        self._buf += ''.join(args)
        self._buf += '\n'
        self._buf += '    ' * self._lvl

    def default_accept(self, inst):
        print(inst.__class__.__name__)       
        
    def accept_S_BRG(self, inst):
        self.accept(one(inst).ACT_BRB[697].ACT_ACT[698]())
    
    def accept_O_TFR(self, inst):
        self.accept(one(inst).ACT_OPB[696].ACT_ACT[698]())
    
    def accept_S_SYNC(self, inst):
        self.accept(one(inst).ACT_FNB[695].ACT_ACT[698]())
    
    def accept_O_DBATTR(self, inst):
        self.accept(one(inst).ACT_DAB[693].ACT_ACT[698]())
    
    def accept_SM_ACT(self, inst):
        self.accept(one(inst).ACT_SAB[691].ACT_ACT[698]())
        self.accept(one(inst).ACT_TAB[688].ACT_ACT[698]())
    
    def accept_SPR_PO(self, inst):
        self.accept(one(inst).ACT_POB[687].ACT_ACT[698]())
    
    def accept_SPR_PS(self, inst):
        self.accept(one(inst).ACT_PSB[686].ACT_ACT[698]())
    
    def accept_SPR_RO(self, inst):
        self.accept(one(inst).ACT_ROB[685].ACT_ACT[698]())
    
    def accept_SPR_RS(self, inst):
        self.accept(one(inst).ACT_RSB[684].ACT_ACT[698]())
    
    def accept_ACT_ACT(self, inst):
        self.accept(one(inst).ACT_BLK[666]())
    
    def accept_ACT_BLK(self, inst):
        self._lvl += 1
        if self._lvl:
            self.buf_linebreak()
        
        first_filter = lambda sel: (not one(sel).ACT_SMT[661, 'succeeds']() and
                                    not one(sel).ACT_EL[603]() and
                                    not one(sel).ACT_E[603]())
        
        act_smt = one(inst).ACT_SMT[602](first_filter)
        while act_smt:
            self.accept(act_smt)
            act_smt = one(act_smt).ACT_SMT[661, 'precedes']()
            
        self._lvl -= 1
        self.buf_linebreak()
        
    def accept_ACT_SMT(self, inst):
        self.accept(subtype(inst, 603))
        self.buf_linebreak(';')
        
    def accept_ACT_RET(self, inst):
        self.buf('return ')
        self.accept(one(inst).V_VAL[668]())
        
    def accept_ACT_BRK(self, inst):
        self.buf('break')
        
    def accept_ACT_CON(self, inst):
        self.buf('continue')
        
    def accept_ACT_CTL(self, inst):
        self.buf('control stop')
        
    def accept_ACT_CR(self, inst):
        self.buf('create object instance ')
        self.accept(one(inst).V_VAR[633]())
        
        o_obj = one(inst).O_OBJ[671]()
        self.buf(' of ', o_obj.Key_Lett)
        
    def accept_ACT_CNV(self, inst):
        o_obj = one(inst).O_OBJ[672]()
        self.buf('create object instance of ', o_obj.Key_Lett)
        
    def accept_ACT_DEL(self, inst):
        self.buf('delete object instance ')
        self.accept(one(inst).V_VAR[634]())
        
    def accept_ACT_REL(self, inst):
        self.buf('relate ')
        self.accept(one(inst).V_VAR[615]())
        
        self.buf(' to ')
        self.accept(one(inst).V_VAR[616]())
        
        r_rel = one(inst).R_REL[653]()
        self.buf(' across R', str(r_rel.Numb))
        if inst.relationship_phrase:
            self.buf('.', inst.relationship_phrase)
        
    def accept_ACT_RU(self, inst):
        self.buf('relate ')
        self.accept(one(inst).V_VAR[617]())
        
        self.buf(' to ')
        self.accept(one(inst).V_VAR[618]())
        
        r_rel = one(inst).R_REL[654]()
        self.buf(' across R', str(r_rel.Numb))
        if inst.relationship_phrase:
            self.buf('.', inst.relationship_phrase)
            
        self.buf(' using ')
        self.accept(one(inst).V_VAR[619]())
        
    def accept_ACT_UNR(self, inst):
        self.buf('unrelate ')
        self.accept(one(inst).V_VAR[620]())
        
        self.buf(' from ')
        self.accept(one(inst).V_VAR[621]())
        
        r_rel = one(inst).R_REL[655]()
        self.buf(' across R', str(r_rel.Numb))
        if inst.relationship_phrase:
            self.buf('.', inst.relationship_phrase)
            
    def accept_ACT_URU(self, inst):
        self.buf('unrelate ')
        self.accept(one(inst).V_VAR[622]())
        
        self.buf(' from ')
        self.accept(one(inst).V_VAR[623]())
        
        r_rel = one(inst).R_REL[656]()
        self.buf(' across R', str(r_rel.Numb))
        if inst.relationship_phrase:
            self.buf('.', inst.relationship_phrase)
            
        self.buf(' using ')
        self.accept(one(inst).V_VAR[624]())
        
    def accept_ACT_FIO(self, inst):
        o_obj = one(inst).O_OBJ[677]()
        self.buf('select ', inst.cardinality, ' ')
        self.accept(one(inst).V_VAR[639]())
        self.buf(' from instances of ', o_obj.Key_Lett)
        
    def accept_ACT_SEL(self, inst):
        self.buf('select ', inst.cardinality, ' ')
        self.accept(one(inst).V_VAR[638]())
        self.buf(' related by ')
        self.accept(one(inst).V_VAL[613]())
        self.accept(one(inst).ACT_LNK[637]())
        self.accept(one(inst).ACT_SRW[664]())

    def accept_ACT_SRW(self, inst):
        self.buf('where ')
        self.accept(one(inst).V_VAL[611]())
        
    def accept_ACT_FIW(self, inst):
        o_obj = one(inst).O_OBJ[676]()
        self.buf('select ', inst.cardinality, ' ')
        self.accept(one(inst).V_VAR[665]())
        self.buf(' from instances of ', o_obj.Key_Lett)
        self.buf(' where ')
        self.accept(one(inst).V_VAL[610]())
        
    def accept_ACT_LNK(self, inst):
        o_obj = one(inst).O_OBJ[678]()
        r_rel = one(inst).R_REL[681]()
        self.buf('->', o_obj.Key_Lett, '[R', str(r_rel.Numb))
        if inst.Rel_Phrase:
            self.buf('.', inst.Rel_Phrase)
        self.buf(']')
        self.accept(one(inst).ACT_LNK[604, 'succeeds']())
        
    def accept_ACT_AI(self, inst):
        if one(inst).V_VAL[609].V_MSV[801]():
            self.buf('send ')
        else:
            self.buf('assign ')
            
        self.accept(one(inst).V_VAL[689]())
        self.buf(' = ')
        self.accept(one(inst).V_VAL[609]())

    def accept_ACT_WHL(self, inst):
        self.buf('while ')
        self.accept(one(inst).V_VAL[626]())
        self.accept(one(inst).ACT_BLK[608]())
        self.buf('end while')
        
    def accept_ACT_IF(self, inst):
        by_position = lambda inst: (one(inst).ACT_SMT[603]().LineNumber,
                                    one(inst).ACT_SMT[603]().StartPosition)
        
        self.buf('if ')
        self.accept(one(inst).V_VAL[625]())
        self.accept(one(inst).ACT_BLK[607]())
        
        for act_el in sorted(many(inst).ACT_EL[682](), key=by_position):
            self.accept(act_el)
        
        self.accept(one(inst).ACT_E[683]())
        
        self.buf('end if')
        
    def accept_ACT_EL(self, inst):
        self.buf('elif ')
        self.accept(one(inst).V_VAL[659]())
        self.accept(one(inst).ACT_BLK[658]())
        
    def accept_ACT_E(self, inst):
        self.buf('else')
        self.accept(one(inst).ACT_BLK[606]())

    def accept_ACT_FOR(self, inst):
        self.buf('for each ')
        self.accept(one(inst).V_VAR[614]())
        self.buf(' in ')
        self.accept(one(inst).V_VAR[652]())
        self.accept(one(inst).ACT_BLK[605]())
        self.buf('end for')

    def accept_ACT_FNC(self, inst):
        s_sync = one(inst).S_SYNC[675]()
        self.buf('::', s_sync.Name)
        self.buf('(')
        first_filter = lambda sel: one(sel).V_PAR[816, 'precedes']() is None
        self.accept(any(inst).V_PAR[669](first_filter))
        self.buf(')')
        
    def accept_ACT_BRG(self, inst):
        s_brg = one(inst).S_BRG[674]()
        s_ee = one(s_brg).S_EE[19]()
        self.buf('bridge ', s_ee.Key_Lett, '::', s_brg.Name)
        self.buf('(')
        first_filter = lambda sel: one(sel).V_PAR[816, 'precedes']() is None
        self.accept(any(inst).V_PAR[628](first_filter))
        self.buf(')')
        
    def accept_ACT_IOP(self, inst):
        self.accept(one(inst).SPR_PO[680].SPR_PEP[4503]())
        self.accept(one(inst).SPR_RO[657].SPR_REP[4502]())
        self.buf('(')
        first_filter = lambda sel: one(sel).V_PAR[816, 'precedes']() is None
        self.accept(any(inst).V_PAR[679](first_filter))
        self.buf(')')
        
    def accept_ACT_SGN(self, inst):
        self.accept(one(inst).SPR_PS[663].SPR_PEP[4503]())
        self.accept(one(inst).SPR_RS[660].SPR_REP[4502]())
        self.buf('(')
        first_filter = lambda sel: one(sel).V_PAR[816, 'precedes']() is None
        self.accept(any(inst).V_PAR[662](first_filter))
        self.buf(')')
        
    def accept_ACT_TFM(self, inst):
        o_tfr = one(inst).O_TFR[673]()
        o_obj = one(o_tfr).O_OBJ[115]()
        v_var = one(inst).V_VAR[667]()
        
        if not v_var:
            self.buf(o_obj.Key_Lett, "::", o_tfr.Name)
        else:
            self.buf('transform ')
            self.accept(v_var)
            self.buf('.', o_tfr.Name)
            
        self.buf('(')
        first_filter = lambda sel: one(sel).V_PAR[816, 'precedes']() is None
        self.accept(any(inst).V_PAR[627](first_filter))
        self.buf(')')
        
    def accept_V_VAL(self, inst):
        self.accept(subtype(inst, 801))
            
    def accept_V_TVL(self, inst):
        self.accept(one(inst).V_VAR[805]())

    def accept_V_ISR(self, inst):
        self.accept(one(inst).V_VAR[809]())
        
    def accept_V_VAR(self, inst):
        self.buf(inst.Name)
        
    def accept_V_IRF(self, inst):
        self.accept(one(inst).V_VAR[808]())
        
    def accept_V_PVL(self, inst):
        self.buf('param.')
        self.accept(one(inst).S_BPARM[831]())
        self.accept(one(inst).S_SPARM[832]())
        self.accept(one(inst).O_TPARM[833]())
        self.accept(one(inst).C_PP[843]())

    def accept_V_SLR(self, inst):
        self.buf('selected')
        
    def accept_V_MVL(self, inst):
        self.accept(one(inst).V_VAL[837]())
        s_mbr = one(inst).S_MBR[836]()
        self.buf('.', s_mbr.Name)
        
    def accept_V_AVL(self, inst):
        self.accept(one(inst).V_VAL[807]())
        o_attr = one(inst).O_ATTR[806]()
        self.buf('.', o_attr.Name)
        
    def accept_V_AER(self, inst):
        self.accept(one(inst).V_VAL[838]())
        self.buf('[')
        self.accept(one(inst).V_VAL[839]())
        self.buf(']')
        
    def accept_V_LIN(self, inst):
        self.buf(inst.Value)
        
    def accept_V_LRL(self, inst):
        self.buf(inst.Value)
        
    def accept_V_LST(self, inst):
        self.buf('"%s"' % inst.Value)
        
    def accept_V_LBO(self, inst):
        self.buf(inst.Value.lower())

    def accept_V_LEN(self, inst):
        s_enum = one(inst).S_ENUM[824]()
        s_dt = one(s_enum).S_EDT[27].S_DT[17]()
        self.buf(s_dt.Name, '::', s_enum.Name)
        
    def accept_V_BIN(self, inst):
        self.buf('(')
        self.accept(one(inst).V_VAL[802]())
        self.buf(' ', inst.Operator, ' ')
        self.accept(one(inst).V_VAL[803]())
        self.buf(')')

    def accept_V_UNY(self, inst):
        self.buf('(')
        self.buf(inst.Operator, ' ')
        self.accept(one(inst).V_VAL[804]())
        self.buf(')')

    def accept_V_PAR(self, inst):
        if one(inst).V_PAR[816, 'precedes']() is not None:
            self.buf(', ')
            
        self.buf(inst.Name, ': ')
        self.accept(one(inst).V_VAL[800]())
        self.accept(one(inst).V_PAR[816, 'succeeds']())

    def accept_V_EDV(self, inst):
        self.buf('rcvd_evt.')
        self.accept(any(inst).V_EPR[834]())  # TODO: this is a many-relation, why?
        
    def accept_V_EPR(self, inst):
        self.accept(one(inst).SM_EVTDI[846]())
        self.accept(one(inst).C_PP[847]())
        
    def accept_SM_EVTDI(self, inst):
        self.buf(inst.Name)
    
    def accept_V_FNV(self, inst):
        s_sync = one(inst).S_SYNC[827]()
        self.buf('::', s_sync.Name)
        self.buf('(')
        first_filter = lambda sel: one(sel).V_PAR[816, 'precedes']() is None
        self.accept(any(inst).V_PAR[817](first_filter))
        self.buf(')')
        
    def accept_V_BRV(self, inst):
        s_brg = one(inst).S_BRG[828]()
        s_ee = one(s_brg).S_EE[19]()
        self.buf('bridge ', s_ee.Key_Lett, '::', s_brg.Name)
        self.buf('(')
        first_filter = lambda sel: one(sel).V_PAR[816, 'precedes']() is None
        self.accept(any(inst).V_PAR[810](first_filter))
        self.buf(')')
        
    def accept_V_TRV(self, inst):
        o_tfr = one(inst).O_TFR[829]()
        o_obj = one(o_tfr).O_OBJ[115]()
        v_var = one(inst).V_VAR[830]()
        
        if not v_var:
            self.buf(o_obj.Key_Lett, "::", o_tfr.Name)
        else:
            self.buf('transform ')
            self.accept(v_var)
            self.buf('.', o_tfr.Name)
            
        self.buf('(')
        first_filter = lambda sel: one(sel).V_PAR[816, 'precedes']() is None
        self.accept(any(inst).V_PAR[811](first_filter))
        self.buf(')')
        
    def accept_V_MSV(self, inst):
        self.accept(one(inst).SPR_PEP[841]())
        self.accept(one(inst).SPR_REP[845]())
        self.buf('(')
        first_filter = lambda sel: one(sel).V_PAR[816, 'precedes']() is None
        self.accept(any(inst).V_PAR[842](first_filter))
        self.buf(')')
        
    def accept_SPR_PEP(self, inst):
        c_po = one(inst).C_P[4501].C_IR[4009].C_PO[4016]()
        c_ep = one(inst).C_EP[4501]()
        self.buf(c_po.Name, '::', c_ep.Name)
        
    def accept_SPR_REP(self, inst):
        c_po = one(inst).C_R[4500].C_IR[4009].C_PO[4016]()
        c_ep = one(inst).C_EP[4500]()
        self.buf(c_po.Name, '::', c_ep.Name)
        
    def accept_E_GPR(self, inst):
        self.buf('generate ')
        self.accept(one(inst).V_VAL[714]())
    
    def accept_E_ESS(self, inst):
        self.accept(one(inst).E_CES[701]())
        self.accept(one(inst).E_GES[701]())

        self.buf('(')
        first_filter = lambda sel: one(sel).V_PAR[816, 'precedes']() is None
        self.accept(any(inst).V_PAR[700](first_filter))
        self.buf(')')
        
        self.accept(one(inst).E_CES[701].E_CSME[702]())
        self.accept(one(inst).E_CES[701].E_CEE[702]())
        
        self.accept(one(inst).E_GES[701].E_GSME[703]())
        self.accept(one(inst).E_GES[701].E_GEE[703]())
        
    def accept_E_GES(self, inst):
        self.buf('generate ')
        self.accept(one(inst).E_GSME[703].SM_EVT[707]())
        self.accept(one(inst).E_GEE[703].S_EEEVT[709]())
        
    def accept_E_CES(self, inst):
        self.buf('create event instance ')
        self.accept(one(inst).V_VAR[710]())
        
        self.buf(' of ')
        
        self.accept(one(inst).E_CSME[702].SM_EVT[706]())
        self.accept(one(inst).E_CEE[702].S_EEEVT[708]())
                
    def accept_SM_EVT(self, inst):
        self.buf(inst.Drv_Lbl)
        if one(inst).SM_PEVT[525]():
            self.buf('*')
            
        self.buf(":'%s'" % inst.Mning)
        
    def accept_E_GSME(self, inst):
        self.buf(' to ')
        self.accept(one(inst).E_GEN[705].V_VAR[712]())
        self.accept(one(inst).E_GAR[705]())
        self.accept(one(inst).E_GEC[705]())
        
    def accept_E_GAR(self, inst):
        o_obj = one(inst).E_GSME[705].SM_EVT[707].SM_SM[502].SM_ASM[517].O_OBJ[519]()
        self.buf(o_obj.Key_Lett, ' class')
        
    def accept_E_GEC(self, inst):
        o_obj = one(inst).E_GSME[705].SM_EVT[707].SM_SM[502].SM_ISM[517].O_OBJ[518]()
        self.buf(o_obj.Key_Lett, ' creator')
        
    def accept_E_CSME(self, inst):
        self.buf(' to ')
        self.accept(one(inst).E_CEI[704].V_VAR[711]())
        self.accept(one(inst).E_CEA[704]())
        self.accept(one(inst).E_CEC[704]())
        
    def accept_E_CEA(self, inst):
        o_obj = one(inst).E_CSME[704].SM_EVT[706].SM_SM[502].SM_ASM[517].O_OBJ[519]()
        self.buf(o_obj.Key_Lett, ' class')
        
    def accept_E_CEC(self, inst):
        o_obj = one(inst).E_CSME[704].SM_EVT[706].SM_SM[502].SM_ISM[517].O_OBJ[518]()
        self.buf(o_obj.Key_Lett, ' creator')
        
    def accept_O_TPARM(self, inst):
        self.buf(inst.Name)

    def accept_S_SPARM(self, inst):
        self.buf(inst.Name)
        
    def accept_S_BPARM(self, inst):
        self.buf(inst.Name)
        
    def accept_C_PP(self, inst):
        self.buf(inst.Name)
    

def gen_text_action(instance):
    '''
    Generate textual OAL action code from an *instance* in the BridgePoint 
    metamodel. The input may be an instance of the following classes:

    - S_SYNC
    - S_BRG
    - O_TFR
    - O_DBATTR
    - SM_ACT
    - SPR_RO
    - SPR_RS
    - SPR_PO
    - SPR_PS
        
    In addition, anything in the ooaofooa subsystems Value or Body, e.g. ACT_SMT
    or V_VAL are also supported.
    '''
    w = ActionTextGenWalker(-1)
    w.accept(instance)
    return str(w)

