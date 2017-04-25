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

import os
import logging
import xtuml

from xtuml import navigate_one as one
from xtuml import navigate_many as many
from xtuml import navigate_subtype as subtype
from xtuml import where_eq as where


logger = logging.getLogger(__name__)


__version__ = 4.2


schema = '''
CREATE TABLE S_AW (
         Brg_ID    UNIQUE_ID,
         Sync_ID    UNIQUE_ID );
CREATE TABLE V_LOC (
         Id    UNIQUE_ID,
         LineNumber    INTEGER,
         StartPosition    INTEGER,
         EndPosition    INTEGER,
         Var_ID    UNIQUE_ID );
CREATE TABLE V_VAR (
         Var_ID    UNIQUE_ID,
         Block_ID    UNIQUE_ID,
         Name    STRING,
         Declared    BOOLEAN,
         DT_ID    UNIQUE_ID );
CREATE TABLE V_VAL (
         Value_ID    UNIQUE_ID,
         isLValue    BOOLEAN,
         isImplicit    BOOLEAN,
         LineNumber    INTEGER,
         StartPosition    INTEGER,
         EndPosition    INTEGER,
         firstParameterLabelLineNumber    INTEGER,
         firstParameterLabelColumn    INTEGER,
         currentLaterParameterLabelLineNumber    INTEGER,
         currentLaterParameterLabelColumn    INTEGER,
         DT_ID    UNIQUE_ID,
         Block_ID    UNIQUE_ID );
CREATE TABLE V_UNY (
         Value_ID    UNIQUE_ID,
         Operand_Value_ID    UNIQUE_ID,
         Operator    STRING );
CREATE TABLE V_TRN (
         Var_ID    UNIQUE_ID,
         DT_ID    UNIQUE_ID,
         Dimensions    STRING );
CREATE TABLE V_TVL (
         Value_ID    UNIQUE_ID,
         Var_ID    UNIQUE_ID );
CREATE TABLE V_SCV (
         Value_ID    UNIQUE_ID,
         Const_ID    UNIQUE_ID,
         DT_ID    UNIQUE_ID );
CREATE TABLE V_SLR (
         Value_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID,
         Attr_ID    UNIQUE_ID,
         Op_Value_ID    UNIQUE_ID );
CREATE TABLE V_PVL (
         Value_ID    UNIQUE_ID,
         BParm_ID    UNIQUE_ID,
         SParm_ID    UNIQUE_ID,
         TParm_ID    UNIQUE_ID,
         PP_Id    UNIQUE_ID );
CREATE TABLE V_TRV (
         Value_ID    UNIQUE_ID,
         Tfr_ID    UNIQUE_ID,
         Var_ID    UNIQUE_ID,
         ParmListOK    BOOLEAN,
         modelClassKeyLettersLineNumber    INTEGER,
         modelClassKeyLettersColumn    INTEGER );
CREATE TABLE V_MSV (
         Value_ID    UNIQUE_ID,
         PEP_Id    UNIQUE_ID,
         REP_Id    UNIQUE_ID,
         ParmListOK    BOOLEAN,
         ownerNameLineNumber    INTEGER,
         ownerNameColumn    INTEGER,
         Target_Value_ID    UNIQUE_ID );
CREATE TABLE V_MVL (
         Value_ID    UNIQUE_ID,
         Root_Value_ID    UNIQUE_ID,
         Member_ID    UNIQUE_ID,
         DT_DT_ID    UNIQUE_ID );
CREATE TABLE V_LST (
         Value_ID    UNIQUE_ID,
         Value    STRING );
CREATE TABLE V_LRL (
         Value_ID    UNIQUE_ID,
         Value    STRING );
CREATE TABLE V_LIN (
         Value_ID    UNIQUE_ID,
         Value    STRING );
CREATE TABLE V_LEN (
         Value_ID    UNIQUE_ID,
         Enum_ID    UNIQUE_ID,
         dataTypeNameLineNumber    INTEGER,
         dataTypeNameColumn    INTEGER );
CREATE TABLE V_LBO (
         Value_ID    UNIQUE_ID,
         Value    STRING );
CREATE TABLE V_ISR (
         Value_ID    UNIQUE_ID,
         Var_ID    UNIQUE_ID );
CREATE TABLE V_INS (
         Var_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID );
CREATE TABLE V_IRF (
         Value_ID    UNIQUE_ID,
         Var_ID    UNIQUE_ID );
CREATE TABLE V_INT (
         Var_ID    UNIQUE_ID,
         IsImplicitInFor    BOOLEAN,
         Obj_ID    UNIQUE_ID );
CREATE TABLE V_FNV (
         Value_ID    UNIQUE_ID,
         Sync_ID    UNIQUE_ID,
         ParmListOK    BOOLEAN );
CREATE TABLE V_EPR (
         Value_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMedi_ID    UNIQUE_ID,
         PP_Id    UNIQUE_ID );
CREATE TABLE V_EDV (
         Value_ID    UNIQUE_ID );
CREATE TABLE V_BRV (
         Value_ID    UNIQUE_ID,
         Brg_ID    UNIQUE_ID,
         ParmListOK    BOOLEAN,
         externalEntityKeyLettersLineNumber    INTEGER,
         externalEntityKeyLettersColumn    INTEGER );
CREATE TABLE V_BIN (
         Value_ID    UNIQUE_ID,
         Right_Value_ID    UNIQUE_ID,
         Left_Value_ID    UNIQUE_ID,
         Operator    STRING );
CREATE TABLE V_AVL (
         Value_ID    UNIQUE_ID,
         Root_Value_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID,
         Attr_ID    UNIQUE_ID );
CREATE TABLE V_ALV (
         Value_ID    UNIQUE_ID,
         Array_Value_ID    UNIQUE_ID );
CREATE TABLE V_AER (
         Value_ID    UNIQUE_ID,
         Root_Value_ID    UNIQUE_ID,
         Index_Value_ID    UNIQUE_ID );
CREATE TABLE V_PAR (
         Value_ID    UNIQUE_ID,
         Statement_ID    UNIQUE_ID,
         Invocation_Value_ID    UNIQUE_ID,
         Name    STRING,
         Next_Value_ID    UNIQUE_ID,
         labelLineNumber    INTEGER,
         labelColumn    INTEGER );
CREATE TABLE UC_UIU (
         Package_ID    UNIQUE_ID );
CREATE TABLE UC_UCC (
         Package_ID    UNIQUE_ID,
         Dom_ID    UNIQUE_ID,
         SS_ID    UNIQUE_ID,
         Parent_Package_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         Sys_ID    UNIQUE_ID,
         Component_Package_ID    UNIQUE_ID,
         Component_Id    UNIQUE_ID );
CREATE TABLE UC_UCA (
         Assoc_ID    UNIQUE_ID,
         Source_Part_ID    UNIQUE_ID,
         Destination_Part_ID    UNIQUE_ID );
CREATE TABLE UC_PIUC (
         Package_ID    UNIQUE_ID,
         Part_ID    UNIQUE_ID );
CREATE TABLE UC_I (
         Assoc_ID    UNIQUE_ID,
         Descrip    STRING );
CREATE TABLE UC_G (
         Assoc_ID    UNIQUE_ID,
         Descrip    STRING );
CREATE TABLE UC_E (
         Assoc_ID    UNIQUE_ID,
         Descrip    STRING );
CREATE TABLE UC_BA (
         Assoc_ID    UNIQUE_ID,
         Descrip    STRING );
CREATE TABLE UC_AIUC (
         Assoc_ID    UNIQUE_ID,
         Package_ID    UNIQUE_ID );
CREATE TABLE SLD_SDP (
         Sys_ID    UNIQUE_ID,
         Package_ID    UNIQUE_ID );
CREATE TABLE SLD_SDINP (
         Package_ID    UNIQUE_ID,
         DT_ID    UNIQUE_ID,
         Sys_ID    UNIQUE_ID );
CREATE TABLE SLD_SCINP (
         Sys_ID    UNIQUE_ID,
         Package_ID    UNIQUE_ID,
         Constant_Spec_ID    UNIQUE_ID );
CREATE TABLE O_RTIDA (
         Attr_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID,
         Oid_ID    INTEGER,
         Rel_ID    UNIQUE_ID,
         OIR_ID    UNIQUE_ID );
CREATE TABLE O_RATTR (
         Attr_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID,
         BAttr_ID    UNIQUE_ID,
         BObj_ID    UNIQUE_ID,
         Ref_Mode    INTEGER,
         BaseAttrName    STRING );
CREATE TABLE O_TPARM (
         TParm_ID    UNIQUE_ID,
         Tfr_ID    UNIQUE_ID,
         Name    STRING,
         DT_ID    UNIQUE_ID,
         By_Ref    INTEGER,
         Dimensions    STRING,
         Previous_TParm_ID    UNIQUE_ID,
         Descrip    STRING );
CREATE TABLE O_TFR (
         Tfr_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         DT_ID    UNIQUE_ID,
         Instance_Based    INTEGER,
         Action_Semantics_internal    STRING,
         Suc_Pars    INTEGER,
         Return_Dimensions    STRING,
         Previous_Tfr_ID    UNIQUE_ID );
CREATE TABLE O_NBATTR (
         Attr_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID );
CREATE TABLE O_OBJ (
         Obj_ID    UNIQUE_ID,
         Name    STRING,
         Numb    INTEGER,
         Key_Lett    STRING,
         Descrip    STRING,
         SS_ID    UNIQUE_ID );
CREATE TABLE O_IOBJ (
         IObj_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID,
         Modl_Typ    INTEGER,
         SS_ID    UNIQUE_ID,
         Obj_Name    STRING,
         Obj_KL    STRING );
CREATE TABLE O_DBATTR (
         Attr_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID,
         Action_Semantics_internal    STRING,
         Suc_Pars    INTEGER );
CREATE TABLE O_OIDA (
         Attr_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID,
         Oid_ID    INTEGER,
         localAttributeName    STRING );
CREATE TABLE O_ID (
         Oid_ID    INTEGER,
         Obj_ID    UNIQUE_ID );
CREATE TABLE O_BATTR (
         Attr_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID );
CREATE TABLE O_REF (
         Obj_ID    UNIQUE_ID,
         RObj_ID    UNIQUE_ID,
         ROid_ID    INTEGER,
         RAttr_ID    UNIQUE_ID,
         Rel_ID    UNIQUE_ID,
         OIR_ID    UNIQUE_ID,
         ROIR_ID    UNIQUE_ID,
         Attr_ID    UNIQUE_ID,
         ARef_ID    UNIQUE_ID,
         PARef_ID    UNIQUE_ID,
         Is_Cstrd    BOOLEAN,
         Descrip    STRING,
         RObj_Name    STRING,
         RAttr_Name    STRING,
         Rel_Name    STRING );
CREATE TABLE O_ATTR (
         Attr_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID,
         PAttr_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         Prefix    STRING,
         Root_Nam    STRING,
         Pfx_Mode    INTEGER,
         DT_ID    UNIQUE_ID,
         Dimensions    STRING,
         DefaultValue    STRING );
CREATE TABLE SM_TAH (
         Act_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         Trans_ID    UNIQUE_ID );
CREATE TABLE SM_TXN (
         Trans_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMstt_ID    UNIQUE_ID,
         SMspd_ID    UNIQUE_ID );
CREATE TABLE SM_SDI (
         SMedi_ID    UNIQUE_ID,
         SMspd_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID );
CREATE TABLE SM_STATE (
         SMstt_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMspd_ID    UNIQUE_ID,
         Name    STRING,
         Numb    INTEGER,
         Final    INTEGER );
CREATE TABLE SM_EVTDI (
         SMedi_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         DT_ID    UNIQUE_ID,
         Dimensions    STRING,
         SMevt_ID    UNIQUE_ID,
         Previous_SMedi_ID    UNIQUE_ID );
CREATE TABLE SM_EVT (
         SMevt_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMspd_ID    UNIQUE_ID,
         Numb    INTEGER,
         Mning    STRING,
         Is_Lbl_U    INTEGER,
         Unq_Lbl    STRING,
         Drv_Lbl    STRING,
         Descrip    STRING );
CREATE TABLE SM_SM (
         SM_ID    UNIQUE_ID,
         Descrip    STRING,
         Config_ID    INTEGER );
CREATE TABLE SM_SEME (
         SMstt_ID    UNIQUE_ID,
         SMevt_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMspd_ID    UNIQUE_ID );
CREATE TABLE SM_SGEVT (
         SMevt_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMspd_ID    UNIQUE_ID,
         Provided_Signal_Id    UNIQUE_ID,
         Required_Signal_Id    UNIQUE_ID,
         signal_name    STRING );
CREATE TABLE SM_SEVT (
         SMevt_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMspd_ID    UNIQUE_ID );
CREATE TABLE SM_PEVT (
         SMevt_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMspd_ID    UNIQUE_ID,
         localClassName    STRING,
         localClassKL    STRING,
         localEventMning    STRING );
CREATE TABLE SM_NLEVT (
         SMevt_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMspd_ID    UNIQUE_ID,
         polySMevt_ID    UNIQUE_ID,
         polySM_ID    UNIQUE_ID,
         polySMspd_ID    UNIQUE_ID,
         Local_Meaning    STRING );
CREATE TABLE SM_NETXN (
         Trans_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMstt_ID    UNIQUE_ID,
         SMspd_ID    UNIQUE_ID );
CREATE TABLE SM_NSTXN (
         Trans_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMstt_ID    UNIQUE_ID,
         SMevt_ID    UNIQUE_ID,
         SMspd_ID    UNIQUE_ID );
CREATE TABLE SM_MOORE (
         SM_ID    UNIQUE_ID );
CREATE TABLE SM_MOAH (
         Act_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMstt_ID    UNIQUE_ID );
CREATE TABLE SM_MEALY (
         SM_ID    UNIQUE_ID );
CREATE TABLE SM_MEAH (
         Act_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         Trans_ID    UNIQUE_ID );
CREATE TABLE SM_LEVT (
         SMevt_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMspd_ID    UNIQUE_ID );
CREATE TABLE SM_ISM (
         SM_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID );
CREATE TABLE SM_SUPDT (
         SMspd_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         Non_Local    BOOLEAN );
CREATE TABLE SM_EIGN (
         SMstt_ID    UNIQUE_ID,
         SMevt_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMspd_ID    UNIQUE_ID,
         Descrip    STRING );
CREATE TABLE SM_CRTXN (
         Trans_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMevt_ID    UNIQUE_ID,
         SMspd_ID    UNIQUE_ID );
CREATE TABLE SM_ASM (
         SM_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID );
CREATE TABLE SM_CH (
         SMstt_ID    UNIQUE_ID,
         SMevt_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMspd_ID    UNIQUE_ID,
         Descrip    STRING );
CREATE TABLE SM_AH (
         Act_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID );
CREATE TABLE SM_ACT (
         Act_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         Suc_Pars    INTEGER,
         Action_Semantics_internal    STRING,
         Descrip    STRING );
CREATE TABLE SQ_SIS (
         Package_ID    UNIQUE_ID );
CREATE TABLE SQ_S (
         Package_ID    UNIQUE_ID,
         Dom_ID    UNIQUE_ID,
         Name    STRING,
         SS_ID    UNIQUE_ID,
         Prev_Package_ID    UNIQUE_ID,
         Descrip    STRING,
         Sys_ID    UNIQUE_ID,
         Component_Package_ID    UNIQUE_ID,
         Component_Id    UNIQUE_ID );
CREATE TABLE SQ_MIS (
         Msg_ID    UNIQUE_ID,
         Package_ID    UNIQUE_ID );
CREATE TABLE ACT_SRW (
         Statement_ID    UNIQUE_ID,
         Where_Clause_Value_ID    UNIQUE_ID );
CREATE TABLE ACT_SR (
         Statement_ID    UNIQUE_ID );
CREATE TABLE ACT_FIW (
         Statement_ID    UNIQUE_ID,
         Var_ID    UNIQUE_ID,
         is_implicit    BOOLEAN,
         cardinality    STRING,
         Where_Clause_Value_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID,
         extentLineNumber    INTEGER,
         extentColumn    INTEGER );
CREATE TABLE ACT_FIO (
         Statement_ID    UNIQUE_ID,
         Var_ID    UNIQUE_ID,
         is_implicit    BOOLEAN,
         cardinality    STRING,
         Obj_ID    UNIQUE_ID,
         extentLineNumber    INTEGER,
         extentColumn    INTEGER );
CREATE TABLE ACT_SEL (
         Statement_ID    UNIQUE_ID,
         Var_ID    UNIQUE_ID,
         is_implicit    BOOLEAN,
         cardinality    STRING,
         Value_ID    UNIQUE_ID );
CREATE TABLE ACT_LNK (
         Link_ID    UNIQUE_ID,
         Rel_Phrase    STRING,
         Statement_ID    UNIQUE_ID,
         Rel_ID    UNIQUE_ID,
         Next_Link_ID    UNIQUE_ID,
         Mult    INTEGER,
         Obj_ID    UNIQUE_ID,
         modelClassKeyLettersLineNumber    INTEGER,
         modelClassKeyLettersColumn    INTEGER,
         associationNumberLineNumber    INTEGER,
         associationNumberColumn    INTEGER,
         phraseLineNumber    INTEGER,
         phraseColumn    INTEGER );
CREATE TABLE SR_SR (
         Id    UNIQUE_ID,
         Engine_Id    UNIQUE_ID,
         MatchedParticipant_Id    UNIQUE_ID );
CREATE TABLE SR_NM (
         Id    UNIQUE_ID,
         Unnamed_Attribute    INTEGER );
CREATE TABLE SR_M (
         Id    UNIQUE_ID,
         Result_Id    UNIQUE_ID );
CREATE TABLE SR_CMR (
         Id    UNIQUE_ID,
         startPosition    INTEGER,
         length    INTEGER );
CREATE TABLE SR_CM (
         Id    UNIQUE_ID,
         startPosition    INTEGER,
         matchLength    INTEGER );
CREATE TABLE SQU_R (
         Id    UNIQUE_ID );
CREATE TABLE SQU_Q (
         Id    UNIQUE_ID,
         Engine_Id    UNIQUE_ID,
         pattern    STRING,
         regEx    BOOLEAN,
         caseSensitive    BOOLEAN,
         scope    INTEGER );
CREATE TABLE SQU_DE (
         Id    UNIQUE_ID );
CREATE TABLE SQU_D (
         Id    UNIQUE_ID );
CREATE TABLE SQU_A (
         Id    UNIQUE_ID );
CREATE TABLE SP_SE (
         Id    UNIQUE_ID,
         Participant_Id    UNIQUE_ID,
         modelRootId    STRING,
         className    STRING,
         elementId    INTEGER );
CREATE TABLE SP_SP (
         Id    UNIQUE_ID,
         Engine_Id    UNIQUE_ID );
CREATE TABLE SP_NS (
         Id    UNIQUE_ID,
         searchableValue    STRING );
CREATE TABLE SP_DS (
         Id    UNIQUE_ID,
         searchableValue    STRING );
CREATE TABLE SP_ALS (
         Id    UNIQUE_ID,
         searchableValue    STRING );
CREATE TABLE SEN_E (
         Id    UNIQUE_ID );
CREATE TABLE SEN_RE (
         Id    UNIQUE_ID );
CREATE TABLE SEN_DE (
         Id    UNIQUE_ID );
CREATE TABLE SEN_DCE (
         Id    UNIQUE_ID );
CREATE TABLE SEN_ALE (
         Id    UNIQUE_ID );
CREATE TABLE ACT_URU (
         Statement_ID    UNIQUE_ID,
         One_Side_Var_ID    UNIQUE_ID,
         Other_Side_Var_ID    UNIQUE_ID,
         Associative_Var_ID    UNIQUE_ID,
         relationship_phrase    STRING,
         Rel_ID    UNIQUE_ID,
         associationNumberLineNumber    INTEGER,
         associationNumberColumn    INTEGER,
         associationPhraseLineNumber    INTEGER,
         associationPhraseColumn    INTEGER );
CREATE TABLE ACT_UNR (
         Statement_ID    UNIQUE_ID,
         One_Side_Var_ID    UNIQUE_ID,
         Other_Side_Var_ID    UNIQUE_ID,
         relationship_phrase    STRING,
         Rel_ID    UNIQUE_ID,
         associationNumberLineNumber    INTEGER,
         associationNumberColumn    INTEGER,
         associationPhraseLineNumber    INTEGER,
         associationPhraseColumn    INTEGER );
CREATE TABLE ACT_RU (
         Statement_ID    UNIQUE_ID,
         One_Side_Var_ID    UNIQUE_ID,
         Other_Side_Var_ID    UNIQUE_ID,
         Associative_Var_ID    UNIQUE_ID,
         relationship_phrase    STRING,
         Rel_ID    UNIQUE_ID,
         associationNumberLineNumber    INTEGER,
         associationNumberColumn    INTEGER,
         associationPhraseLineNumber    INTEGER,
         associationPhraseColumn    INTEGER );
CREATE TABLE ACT_REL (
         Statement_ID    UNIQUE_ID,
         One_Side_Var_ID    UNIQUE_ID,
         Other_Side_Var_ID    UNIQUE_ID,
         relationship_phrase    STRING,
         Rel_ID    UNIQUE_ID,
         associationNumberLineNumber    INTEGER,
         associationNumberColumn    INTEGER,
         associationPhraseLineNumber    INTEGER,
         associationPhraseColumn    INTEGER );
CREATE TABLE PA_SICP (
         ComponentPackage_ID    UNIQUE_ID,
         Satisfaction_Id    UNIQUE_ID );
CREATE TABLE PA_SIC (
         Component_Id    UNIQUE_ID,
         Satisfaction_Id    UNIQUE_ID );
CREATE TABLE PA_DIC (
         Component_Id    UNIQUE_ID,
         Delegation_Id    UNIQUE_ID );
CREATE TABLE PE_PE (
         Element_ID    UNIQUE_ID,
         Visibility    INTEGER,
         Package_ID    UNIQUE_ID,
         Component_ID    UNIQUE_ID,
         type    INTEGER );
CREATE TABLE MSG_SM (
         Msg_ID    UNIQUE_ID,
         InformalName    STRING,
         Descrip    STRING,
         GuardCondition    STRING,
         ResultTarget    STRING,
         ReturnValue    STRING,
         isFormal    BOOLEAN,
         Label    STRING,
         SequenceNumb    STRING );
CREATE TABLE MSG_SIG (
         Msg_ID    UNIQUE_ID,
         Id    UNIQUE_ID );
CREATE TABLE MSG_R (
         Msg_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         GuardCondition    STRING,
         ResultTarget    STRING,
         ReturnValue    STRING,
         SequenceNumb    STRING );
CREATE TABLE MSG_O (
         Msg_ID    UNIQUE_ID,
         Tfr_ID    UNIQUE_ID );
CREATE TABLE MSG_OA (
         Arg_ID    UNIQUE_ID,
         TParm_ID    UNIQUE_ID );
CREATE TABLE MSG_A (
         Arg_ID    UNIQUE_ID,
         Informal_Msg_ID    UNIQUE_ID,
         Formal_Msg_ID    UNIQUE_ID,
         Label    STRING,
         Value    STRING,
         InformalName    STRING,
         Descrip    STRING,
         isFormal    BOOLEAN );
CREATE TABLE MSG_M (
         Msg_ID    UNIQUE_ID,
         Receiver_Part_ID    UNIQUE_ID,
         Sender_Part_ID    UNIQUE_ID,
         participatesInCommunication    BOOLEAN );
CREATE TABLE MSG_IOP (
         Msg_ID    UNIQUE_ID,
         Id    UNIQUE_ID );
CREATE TABLE MSG_ISM (
         Msg_ID    UNIQUE_ID );
CREATE TABLE MSG_IAM (
         Msg_ID    UNIQUE_ID );
CREATE TABLE MSG_IA (
         Arg_ID    UNIQUE_ID );
CREATE TABLE MSG_F (
         Msg_ID    UNIQUE_ID,
         Sync_ID    UNIQUE_ID );
CREATE TABLE MSG_FA (
         Arg_ID    UNIQUE_ID,
         SParm_ID    UNIQUE_ID );
CREATE TABLE MSG_EPA (
         Arg_ID    UNIQUE_ID,
         PP_Id    UNIQUE_ID );
CREATE TABLE MSG_E (
         Msg_ID    UNIQUE_ID,
         SMevt_ID    UNIQUE_ID );
CREATE TABLE MSG_EA (
         Arg_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMedi_ID    UNIQUE_ID );
CREATE TABLE MSG_B (
         Msg_ID    UNIQUE_ID,
         Brg_ID    UNIQUE_ID );
CREATE TABLE MSG_BA (
         Arg_ID    UNIQUE_ID,
         BParm_ID    UNIQUE_ID );
CREATE TABLE MSG_AM (
         Msg_ID    UNIQUE_ID,
         InformalName    STRING,
         Descrip    STRING,
         GuardCondition    STRING,
         DurationObservation    STRING,
         DurationConstraint    STRING,
         isFormal    BOOLEAN,
         Label    STRING,
         SequenceNumb    STRING );
CREATE TABLE ACT_SGN (
         Statement_ID    UNIQUE_ID,
         sigNameLineNumber    INTEGER,
         sigNameColumn    INTEGER,
         ownerNameLineNumber    INTEGER,
         ownerNameColumn    INTEGER,
         ProvidedSig_Id    UNIQUE_ID,
         RequiredSig_Id    UNIQUE_ID,
         Value_ID    UNIQUE_ID );
CREATE TABLE ACT_RET (
         Statement_ID    UNIQUE_ID,
         Value_ID    UNIQUE_ID );
CREATE TABLE ACT_TFM (
         Statement_ID    UNIQUE_ID,
         Tfr_ID    UNIQUE_ID,
         Var_ID    UNIQUE_ID,
         operationNameLineNumber    INTEGER,
         operationNameColumn    INTEGER,
         modelClassKeyLettersLineNumber    INTEGER,
         modelClassKeyLettersColumn    INTEGER );
CREATE TABLE ACT_IOP (
         Statement_ID    UNIQUE_ID,
         opNameLineNumber    INTEGER,
         opNameColumn    INTEGER,
         ownerNameLineNumber    INTEGER,
         ownerNameColumn    INTEGER,
         ProvidedOp_Id    UNIQUE_ID,
         RequiredOp_Id    UNIQUE_ID,
         Value_ID    UNIQUE_ID );
CREATE TABLE ACT_FNC (
         Statement_ID    UNIQUE_ID,
         Sync_ID    UNIQUE_ID,
         functionNameLineNumber    INTEGER,
         functionNameColumn    INTEGER );
CREATE TABLE ACT_BRG (
         Statement_ID    UNIQUE_ID,
         Brg_ID    UNIQUE_ID,
         bridgeNameLineNumber    INTEGER,
         bridgeNameColumn    INTEGER,
         externalEntityKeyLettersLineNumber    INTEGER,
         externalEntityKeyLettersColumn    INTEGER );
CREATE TABLE IP_IPINIP (
         Package_ID    UNIQUE_ID );
CREATE TABLE IP_IP (
         Package_ID    UNIQUE_ID,
         Parent_Package_ID    UNIQUE_ID,
         Direct_Sys_ID    UNIQUE_ID,
         Sys_ID    UNIQUE_ID,
         Component_Id    UNIQUE_ID,
         Component_Package_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING );
CREATE TABLE IA_UCP (
         Part_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING );
CREATE TABLE SQ_TM (
         Mark_ID    UNIQUE_ID,
         Name    STRING,
         Part_ID    UNIQUE_ID,
         Descrip    STRING );
CREATE TABLE SQ_TS (
         Span_ID    UNIQUE_ID,
         Mark_ID    UNIQUE_ID,
         Prev_Mark_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING );
CREATE TABLE SQ_PP (
         Part_ID    UNIQUE_ID,
         Package_ID    UNIQUE_ID,
         Label    STRING,
         InformalName    STRING,
         Descrip    STRING,
         isFormal    BOOLEAN );
CREATE TABLE SQ_LS (
         Part_ID    UNIQUE_ID,
         Source_Part_ID    UNIQUE_ID,
         Descrip    STRING,
         Destroyed    BOOLEAN );
CREATE TABLE SQ_P (
         Part_ID    UNIQUE_ID,
         Sequence_Package_ID    UNIQUE_ID );
CREATE TABLE SQ_AV (
         Av_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID,
         Attr_ID    UNIQUE_ID,
         Label    STRING,
         Value    STRING,
         InformalName    STRING,
         Informal_Part_ID    UNIQUE_ID,
         Formal_Part_ID    UNIQUE_ID,
         Descrip    STRING,
         isFormal    BOOLEAN );
CREATE TABLE SQ_IAV (
         Av_ID    UNIQUE_ID );
CREATE TABLE SQ_IA (
         Ia_ID    UNIQUE_ID );
CREATE TABLE SQ_FPP (
         Part_ID    UNIQUE_ID,
         FunPack_ID    UNIQUE_ID,
         Label    STRING,
         InformalName    STRING,
         Descrip    STRING,
         isFormal    BOOLEAN );
CREATE TABLE SQ_FAV (
         Av_ID    UNIQUE_ID );
CREATE TABLE SQ_FA (
         Ia_ID    UNIQUE_ID );
CREATE TABLE SQ_EEP (
         Part_ID    UNIQUE_ID,
         EE_ID    UNIQUE_ID,
         Label    STRING,
         InformalName    STRING,
         Descrip    STRING,
         isFormal    BOOLEAN );
CREATE TABLE SQ_COP (
         Part_ID    UNIQUE_ID,
         Component_Id    UNIQUE_ID,
         Label    STRING,
         InformalComponentName    STRING,
         Descrip    STRING,
         isFormal    BOOLEAN );
CREATE TABLE SQ_CPA (
         Ia_ID    UNIQUE_ID,
         Name    STRING,
         Type    STRING,
         Part_ID    UNIQUE_ID,
         Descrip    STRING );
CREATE TABLE SQ_CP (
         Part_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID,
         Label    STRING,
         InformalName    STRING,
         Descrip    STRING,
         isFormal    BOOLEAN );
CREATE TABLE SQ_CIP (
         Part_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID,
         Name    STRING,
         InformalClassName    STRING,
         Label    STRING,
         Descrip    STRING,
         isFormal    BOOLEAN );
CREATE TABLE SQ_AP (
         Part_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         LS_Part_ID    UNIQUE_ID );
CREATE TABLE ACT_DEL (
         Statement_ID    UNIQUE_ID,
         Var_ID    UNIQUE_ID );
CREATE TABLE ACT_CNV (
         Statement_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID,
         modelClassKeyLettersLineNumber    INTEGER,
         modelClassKeyLettersColumn    INTEGER );
CREATE TABLE ACT_CR (
         Statement_ID    UNIQUE_ID,
         Var_ID    UNIQUE_ID,
         is_implicit    BOOLEAN,
         Obj_ID    UNIQUE_ID,
         modelClassKeyLettersLineNumber    INTEGER,
         modelClassKeyLettersColumn    INTEGER );
CREATE TABLE ACT_AI (
         Statement_ID    UNIQUE_ID,
         r_Value_ID    UNIQUE_ID,
         l_Value_ID    UNIQUE_ID,
         attributeLineNumber    INTEGER,
         attributeColumn    INTEGER );
CREATE TABLE I_TIM (
         Timer_ID    UNIQUE_ID,
         delay    INTEGER,
         running    BOOLEAN,
         recurring    BOOLEAN,
         Event_ID    UNIQUE_ID,
         Label    STRING,
         expiration    STRING );
CREATE TABLE I_EVI (
         Event_ID    UNIQUE_ID,
         isExecuting    BOOLEAN,
         isCreation    BOOLEAN,
         SMevt_ID    UNIQUE_ID,
         Target_Inst_ID    UNIQUE_ID,
         nextEvent_ID    UNIQUE_ID,
         Sent_By_Inst_ID    UNIQUE_ID,
         next_self_Event_ID    UNIQUE_ID,
         Execution_Engine_ID    UNIQUE_ID,
         Originating_Execution_Engine_ID    UNIQUE_ID,
         Label    STRING );
CREATE TABLE I_LIP (
         Participation_ID    UNIQUE_ID,
         Rel_ID    UNIQUE_ID,
         Inst_ID    UNIQUE_ID,
         Label    STRING );
CREATE TABLE I_LNK (
         Link_ID    UNIQUE_ID,
         Rel_ID    UNIQUE_ID,
         Participation_ID    UNIQUE_ID,
         Formalizing_Participation_ID    UNIQUE_ID,
         Associator_Participation_ID    UNIQUE_ID );
CREATE TABLE I_INS (
         Inst_ID    UNIQUE_ID,
         Name    STRING,
         SM_ID    UNIQUE_ID,
         SMstt_ID    UNIQUE_ID,
         Execution_Engine_ID    UNIQUE_ID,
         Trans_ID    UNIQUE_ID,
         Label    STRING,
         Default_Name    STRING );
CREATE TABLE I_DIV (
         DIV_ID    UNIQUE_ID,
         Event_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMedi_ID    UNIQUE_ID,
         PP_Id    UNIQUE_ID );
CREATE TABLE I_CIN (
         Container_ID    UNIQUE_ID );
CREATE TABLE I_EXE (
         Running    BOOLEAN,
         Execution_Engine_ID    UNIQUE_ID,
         Dom_ID    UNIQUE_ID,
         Component_Id    UNIQUE_ID,
         Package_ID    UNIQUE_ID,
         Next_Unique_ID    INTEGER,
         Next_Instance_ID    INTEGER,
         ImportedComponent_Id    UNIQUE_ID,
         Label    STRING,
         EQE_Lock    INTEGER,
         SQE_Lock    INTEGER,
         Container_ID    UNIQUE_ID,
         RealizedBy    INTEGER );
CREATE TABLE I_AVL (
         Inst_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID,
         Attr_ID    UNIQUE_ID,
         Value    STRING,
         Label    STRING );
CREATE TABLE G_EIS (
         Element_ID    UNIQUE_ID,
         Sys_ID    UNIQUE_ID );
CREATE TABLE E_GEE (
         Statement_ID    UNIQUE_ID,
         EE_ID    UNIQUE_ID,
         EEevt_ID    UNIQUE_ID );
CREATE TABLE E_GEC (
         Statement_ID    UNIQUE_ID );
CREATE TABLE E_GAR (
         Statement_ID    UNIQUE_ID );
CREATE TABLE E_GSME (
         Statement_ID    UNIQUE_ID,
         SMevt_ID    UNIQUE_ID );
CREATE TABLE E_GPR (
         Statement_ID    UNIQUE_ID,
         Value_ID    UNIQUE_ID );
CREATE TABLE E_GES (
         Statement_ID    UNIQUE_ID );
CREATE TABLE E_GEN (
         Statement_ID    UNIQUE_ID,
         Var_ID    UNIQUE_ID );
CREATE TABLE E_ESS (
         Statement_ID    UNIQUE_ID,
         ParmListOK    BOOLEAN,
         PEIndicated    BOOLEAN,
         eventDerivedLabelLineNumber    INTEGER,
         eventDerivedLabelColumn    INTEGER,
         eventMeaningLineNumber    INTEGER,
         eventMeaningColumn    INTEGER,
         eventTargetKeyLettersLineNumber    INTEGER,
         eventTargetKeyLettersColumn    INTEGER,
         firstEventDataItemNameLineNumber    INTEGER,
         firstEventDataItemNameColumn    INTEGER,
         currentLaterEventDataItemNameLineNumber    INTEGER,
         currentLaterEventDataItemNameColumn    INTEGER );
CREATE TABLE E_CSME (
         Statement_ID    UNIQUE_ID,
         SMevt_ID    UNIQUE_ID );
CREATE TABLE E_CEI (
         Statement_ID    UNIQUE_ID,
         Var_ID    UNIQUE_ID );
CREATE TABLE E_CEE (
         Statement_ID    UNIQUE_ID,
         EE_ID    UNIQUE_ID,
         EEevt_ID    UNIQUE_ID );
CREATE TABLE E_CEC (
         Statement_ID    UNIQUE_ID );
CREATE TABLE E_CEA (
         Statement_ID    UNIQUE_ID );
CREATE TABLE E_CES (
         Statement_ID    UNIQUE_ID,
         is_implicit    BOOLEAN,
         Var_ID    UNIQUE_ID );
CREATE TABLE EP_SPKG (
         Package_ID    UNIQUE_ID,
         Container_Package_ID    UNIQUE_ID );
CREATE TABLE EP_PIP (
         Parent_Package_ID    UNIQUE_ID,
         Child_Package_ID    UNIQUE_ID );
CREATE TABLE EP_PKG (
         Package_ID    UNIQUE_ID,
         Sys_ID    UNIQUE_ID,
         Direct_Sys_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         Num_Rng    INTEGER );
CREATE TABLE S_UDT (
         DT_ID    UNIQUE_ID,
         CDT_DT_ID    UNIQUE_ID,
         Gen_Type    INTEGER );
CREATE TABLE S_SYS (
         Sys_ID    UNIQUE_ID,
         Name    STRING,
         useGlobals    BOOLEAN );
CREATE TABLE S_SIS (
         Parent_SS_ID    UNIQUE_ID,
         Child_SS_ID    UNIQUE_ID );
CREATE TABLE S_SID (
         Dom_ID    UNIQUE_ID,
         SS_ID    UNIQUE_ID );
CREATE TABLE S_SS (
         SS_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         Prefix    STRING,
         Num_Rng    INTEGER,
         Dom_ID    UNIQUE_ID,
         Config_ID    UNIQUE_ID );
CREATE TABLE S_SDT (
         DT_ID    UNIQUE_ID );
CREATE TABLE S_MBR (
         Member_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         Parent_DT_DT_ID    UNIQUE_ID,
         DT_ID    UNIQUE_ID,
         Previous_Member_ID    UNIQUE_ID,
         Dimensions    STRING );
CREATE TABLE PL_FPID (
         FunPack_ID    UNIQUE_ID,
         Dom_ID    UNIQUE_ID );
CREATE TABLE PL_EEPID (
         Dom_ID    UNIQUE_ID,
         EEPack_ID    UNIQUE_ID );
CREATE TABLE S_IRDT (
         DT_ID    UNIQUE_ID,
         isSet    BOOLEAN,
         Obj_ID    UNIQUE_ID );
CREATE TABLE S_SPARM (
         SParm_ID    UNIQUE_ID,
         Sync_ID    UNIQUE_ID,
         Name    STRING,
         DT_ID    UNIQUE_ID,
         By_Ref    INTEGER,
         Dimensions    STRING,
         Previous_SParm_ID    UNIQUE_ID,
         Descrip    STRING );
CREATE TABLE S_FPIP (
         FunPack_ID    UNIQUE_ID );
CREATE TABLE S_FPK (
         FunPack_ID    UNIQUE_ID,
         Name    STRING,
         Dom_ID    UNIQUE_ID,
         Parent_FunPack_ID    UNIQUE_ID );
CREATE TABLE S_FIP (
         FunPack_ID    UNIQUE_ID,
         Sync_ID    UNIQUE_ID );
CREATE TABLE S_SYNC (
         Sync_ID    UNIQUE_ID,
         Dom_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         Action_Semantics_internal    STRING,
         DT_ID    UNIQUE_ID,
         Suc_Pars    INTEGER,
         Return_Dimensions    STRING );
CREATE TABLE S_EEPK (
         EEPack_ID    UNIQUE_ID,
         Name    STRING,
         Dom_ID    UNIQUE_ID,
         Parent_EEPack_ID    UNIQUE_ID );
CREATE TABLE S_EEIP (
         EEPack_ID    UNIQUE_ID,
         EE_ID    UNIQUE_ID );
CREATE TABLE S_EEM (
         EEmod_ID    UNIQUE_ID,
         EE_ID    UNIQUE_ID,
         Modl_Typ    INTEGER,
         SS_ID    UNIQUE_ID );
CREATE TABLE S_EEEDI (
         EEedi_ID    UNIQUE_ID,
         EE_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         DT_ID    UNIQUE_ID );
CREATE TABLE S_EEEDT (
         EE_ID    UNIQUE_ID,
         EEevt_ID    UNIQUE_ID,
         EEedi_ID    UNIQUE_ID );
CREATE TABLE S_EEEVT (
         EEevt_ID    UNIQUE_ID,
         EE_ID    UNIQUE_ID,
         Numb    INTEGER,
         Mning    STRING,
         Is_Lbl_U    INTEGER,
         Unq_Lbl    STRING,
         Drv_Lbl    STRING,
         Descrip    STRING );
CREATE TABLE S_EEDI (
         EEdi_ID    UNIQUE_ID,
         EE_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         DT_ID    UNIQUE_ID );
CREATE TABLE S_EE (
         EE_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         Key_Lett    STRING,
         Dom_ID    UNIQUE_ID,
         Realized_Class_Path    STRING,
         Label    STRING,
         isRealized    BOOLEAN );
CREATE TABLE S_ENUM (
         Enum_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         EDT_DT_ID    UNIQUE_ID,
         Previous_Enum_ID    UNIQUE_ID );
CREATE TABLE S_EDT (
         DT_ID    UNIQUE_ID );
CREATE TABLE S_EEPIP (
         EEPack_ID    UNIQUE_ID );
CREATE TABLE S_DOM (
         Dom_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         Full_Der    INTEGER,
         Config_ID    UNIQUE_ID,
         Sys_ID    UNIQUE_ID );
CREATE TABLE S_DIM (
         elementCount    INTEGER,
         dimensionCount    INTEGER,
         Sync_ID    UNIQUE_ID,
         SParm_ID    UNIQUE_ID,
         BParm_ID    UNIQUE_ID,
         Brg_ID    UNIQUE_ID,
         Id    UNIQUE_ID,
         Obj_ID    UNIQUE_ID,
         Attr_ID    UNIQUE_ID,
         TParm_ID    UNIQUE_ID,
         Tfr_ID    UNIQUE_ID,
         Member_ID    UNIQUE_ID,
         DT_ID    UNIQUE_ID,
         PP_Id    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         SMedi_ID    UNIQUE_ID,
         DIM_ID    UNIQUE_ID,
         Var_ID    UNIQUE_ID );
CREATE TABLE S_DIS (
         Dom_ID    UNIQUE_ID,
         DT_ID    UNIQUE_ID );
CREATE TABLE S_DPIP (
         Package_ID    UNIQUE_ID );
CREATE TABLE S_DPK (
         Package_ID    UNIQUE_ID,
         Name    STRING,
         Dom_ID    UNIQUE_ID,
         Parent_Package_ID    UNIQUE_ID );
CREATE TABLE S_DIP (
         Package_ID    UNIQUE_ID,
         DT_ID    UNIQUE_ID );
CREATE TABLE S_DT (
         DT_ID    UNIQUE_ID,
         Dom_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         DefaultValue    STRING );
CREATE TABLE S_CDT (
         DT_ID    UNIQUE_ID,
         Core_Typ    INTEGER );
CREATE TABLE S_BPARM (
         BParm_ID    UNIQUE_ID,
         Brg_ID    UNIQUE_ID,
         Name    STRING,
         DT_ID    UNIQUE_ID,
         By_Ref    INTEGER,
         Dimensions    STRING,
         Previous_BParm_ID    UNIQUE_ID,
         Descrip    STRING );
CREATE TABLE S_BRG (
         Brg_ID    UNIQUE_ID,
         EE_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         Brg_Typ    INTEGER,
         DT_ID    UNIQUE_ID,
         Action_Semantics_internal    STRING,
         Suc_Pars    INTEGER,
         Return_Dimensions    STRING );
CREATE TABLE CNST_SYC (
         Const_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         DT_ID    UNIQUE_ID,
         Constant_Spec_ID    UNIQUE_ID,
         Previous_Const_ID    UNIQUE_ID,
         Previous_DT_DT_ID    UNIQUE_ID );
CREATE TABLE CNST_LSC (
         Const_ID    UNIQUE_ID,
         DT_ID    UNIQUE_ID,
         Value    STRING );
CREATE TABLE CNST_LFSC (
         Const_ID    UNIQUE_ID,
         DT_ID    UNIQUE_ID );
CREATE TABLE CNST_CSP (
         Constant_Spec_ID    UNIQUE_ID,
         InformalGroupName    STRING,
         Descrip    STRING );
CREATE TABLE CNST_CIP (
         Constant_Spec_ID    UNIQUE_ID,
         Package_ID    UNIQUE_ID );
CREATE TABLE SPR_RS (
         Id    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         Action_Semantics_internal    STRING,
         Suc_Pars    INTEGER );
CREATE TABLE SPR_RO (
         Id    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         Action_Semantics_internal    STRING,
         Suc_Pars    INTEGER );
CREATE TABLE SPR_REP (
         Id    UNIQUE_ID,
         ExecutableProperty_Id    UNIQUE_ID,
         Requirement_Id    UNIQUE_ID );
CREATE TABLE SPR_PS (
         Id    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         Action_Semantics_internal    STRING,
         Suc_Pars    INTEGER );
CREATE TABLE SPR_PO (
         Id    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         Action_Semantics_internal    STRING,
         Suc_Pars    INTEGER );
CREATE TABLE SPR_PEP (
         Id    UNIQUE_ID,
         ExecutableProperty_Id    UNIQUE_ID,
         Provision_Id    UNIQUE_ID );
CREATE TABLE C_SF (
         Id    UNIQUE_ID,
         Requirement_Id    UNIQUE_ID,
         Provision_Id    UNIQUE_ID,
         Descrip    STRING,
         Label    STRING );
CREATE TABLE C_R (
         Requirement_Id    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         InformalName    STRING,
         reversePathFromComponent    STRING );
CREATE TABLE C_P (
         Provision_Id    UNIQUE_ID,
         Name    STRING,
         InformalName    STRING,
         Descrip    STRING,
         pathFromComponent    STRING );
CREATE TABLE C_PP (
         PP_Id    UNIQUE_ID,
         Signal_Id    UNIQUE_ID,
         DT_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         By_Ref    INTEGER,
         Dimensions    STRING,
         Previous_PP_Id    UNIQUE_ID );
CREATE TABLE C_PO (
         Id    UNIQUE_ID,
         Component_Id    UNIQUE_ID,
         Name    STRING,
         Mult    INTEGER,
         DoNotShowPortOnCanvas    BOOLEAN );
CREATE TABLE C_AS (
         Id    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         Direction    INTEGER,
         Previous_Id    UNIQUE_ID );
CREATE TABLE C_RID (
         Reference_Id    UNIQUE_ID,
         Delegation_Id    UNIQUE_ID );
CREATE TABLE C_IR (
         Id    UNIQUE_ID,
         Formal_Interface_Id    UNIQUE_ID,
         Delegation_Id    UNIQUE_ID,
         Port_Id    UNIQUE_ID );
CREATE TABLE C_IO (
         Id    UNIQUE_ID,
         DT_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         Direction    INTEGER,
         Return_Dimensions    STRING,
         Previous_Id    UNIQUE_ID );
CREATE TABLE C_I (
         Id    UNIQUE_ID,
         Package_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING );
CREATE TABLE C_EP (
         Id    UNIQUE_ID,
         Interface_Id    UNIQUE_ID,
         Direction    INTEGER,
         Name    STRING,
         Descrip    STRING );
CREATE TABLE C_DG (
         Id    UNIQUE_ID,
         Name    STRING );
CREATE TABLE CP_CPINP (
         Id    UNIQUE_ID,
         Parent_Package_ID    UNIQUE_ID );
CREATE TABLE CP_CP (
         Package_ID    UNIQUE_ID,
         ParentLink_Id    UNIQUE_ID,
         Sys_ID    UNIQUE_ID,
         Containing_Sys_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING );
CREATE TABLE CN_DC (
         Id    UNIQUE_ID,
         Dom_ID    UNIQUE_ID );
CREATE TABLE CN_CIC (
         Id    UNIQUE_ID,
         Parent_Id    UNIQUE_ID );
CREATE TABLE CL_IR (
         Id    UNIQUE_ID,
         Satisfaction_Element_Id    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING );
CREATE TABLE CL_IIR (
         Id    UNIQUE_ID,
         Ref_Id    UNIQUE_ID,
         ImportedComp_Id    UNIQUE_ID,
         Delegation_Id    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING );
CREATE TABLE CL_IPINS (
         Satisfaction_Id    UNIQUE_ID,
         ImportedProvision_Id    UNIQUE_ID );
CREATE TABLE CL_IP (
         Id    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING );
CREATE TABLE CL_IC (
         Id    UNIQUE_ID,
         AssignedComp_Id    UNIQUE_ID,
         ParentComp_Id    UNIQUE_ID,
         Component_Package_ID    UNIQUE_ID,
         Mult    INTEGER,
         ClassifierName    STRING,
         Name    STRING,
         Descrip    STRING );
CREATE TABLE C_C (
         Id    UNIQUE_ID,
         Package_ID    UNIQUE_ID,
         NestedComponent_Id    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         Mult    INTEGER,
         Root_Package_ID    UNIQUE_ID,
         isRealized    BOOLEAN,
         Realized_Class_Path    STRING );
CREATE TABLE CA_SMSME (
         CPath_ID    UNIQUE_ID,
         SMevt_ID    UNIQUE_ID );
CREATE TABLE CA_SMSMC (
         CPath_ID    UNIQUE_ID,
         OSM_ID    UNIQUE_ID,
         DSM_ID    UNIQUE_ID,
         OIObj_ID    UNIQUE_ID,
         DIObj_ID    UNIQUE_ID );
CREATE TABLE CA_SMOAA (
         APath_ID    UNIQUE_ID,
         Attr_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID );
CREATE TABLE CA_SMOA (
         APath_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID,
         IObj_ID    UNIQUE_ID );
CREATE TABLE CA_SMEEE (
         CPath_ID    UNIQUE_ID,
         EE_ID    UNIQUE_ID,
         EEevt_ID    UNIQUE_ID );
CREATE TABLE CA_SMEED (
         APath_ID    UNIQUE_ID,
         EEdi_ID    UNIQUE_ID,
         EE_ID    UNIQUE_ID );
CREATE TABLE CA_SMEEC (
         CPath_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         EE_ID    UNIQUE_ID,
         EEmod_ID    UNIQUE_ID );
CREATE TABLE CA_SMEEA (
         APath_ID    UNIQUE_ID,
         EE_ID    UNIQUE_ID,
         EEmod_ID    UNIQUE_ID );
CREATE TABLE CA_EESME (
         CPath_ID    UNIQUE_ID,
         SMevt_ID    UNIQUE_ID );
CREATE TABLE CA_EESMC (
         CPath_ID    UNIQUE_ID,
         EEmod_ID    UNIQUE_ID,
         EE_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID );
CREATE TABLE CA_COMM (
         CPath_ID    UNIQUE_ID,
         SS_ID    UNIQUE_ID );
CREATE TABLE CA_ACC (
         APath_ID    UNIQUE_ID,
         SS_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         IObj_ID    UNIQUE_ID );
CREATE TABLE COMM_PIC (
         Package_ID    UNIQUE_ID,
         Part_ID    UNIQUE_ID );
CREATE TABLE COMM_MIC (
         Package_ID    UNIQUE_ID,
         Msg_ID    UNIQUE_ID );
CREATE TABLE COMM_LNK (
         Link_ID    UNIQUE_ID,
         Rel_ID    UNIQUE_ID,
         Numb    STRING,
         Descrip    STRING,
         StartText    STRING,
         EndText    STRING,
         isFormal    BOOLEAN,
         StartVisibility    INTEGER,
         EndVisibility    INTEGER,
         Start_Part_ID    UNIQUE_ID,
         Destination_Part_ID    UNIQUE_ID );
CREATE TABLE COMM_CIC (
         Package_ID    UNIQUE_ID );
CREATE TABLE COMM_COMM (
         Package_ID    UNIQUE_ID,
         Dom_ID    UNIQUE_ID,
         SS_ID    UNIQUE_ID,
         CIC_Package_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         Sys_ID    UNIQUE_ID,
         Component_Package_ID    UNIQUE_ID,
         Component_Id    UNIQUE_ID );
CREATE TABLE ACT_WHL (
         Statement_ID    UNIQUE_ID,
         Value_ID    UNIQUE_ID,
         Block_ID    UNIQUE_ID );
CREATE TABLE ACT_TAB (
         Action_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         Act_ID    UNIQUE_ID );
CREATE TABLE ACT_SMT (
         Statement_ID    UNIQUE_ID,
         Block_ID    UNIQUE_ID,
         Previous_Statement_ID    UNIQUE_ID,
         LineNumber    INTEGER,
         StartPosition    INTEGER,
         Label    STRING );
CREATE TABLE ACT_SAB (
         Action_ID    UNIQUE_ID,
         SM_ID    UNIQUE_ID,
         Act_ID    UNIQUE_ID );
CREATE TABLE ACT_RSB (
         Action_ID    UNIQUE_ID,
         Id    UNIQUE_ID );
CREATE TABLE ACT_ROB (
         Action_ID    UNIQUE_ID,
         Id    UNIQUE_ID );
CREATE TABLE ACT_PSB (
         Action_ID    UNIQUE_ID,
         Id    UNIQUE_ID );
CREATE TABLE ACT_POB (
         Action_ID    UNIQUE_ID,
         Id    UNIQUE_ID );
CREATE TABLE ACT_OPB (
         Action_ID    UNIQUE_ID,
         Tfr_ID    UNIQUE_ID );
CREATE TABLE ACT_IF (
         Statement_ID    UNIQUE_ID,
         Block_ID    UNIQUE_ID,
         Value_ID    UNIQUE_ID,
         Elif_Statement_ID    UNIQUE_ID,
         Else_Statement_ID    UNIQUE_ID );
CREATE TABLE ACT_FNB (
         Action_ID    UNIQUE_ID,
         Sync_ID    UNIQUE_ID );
CREATE TABLE ACT_FOR (
         Statement_ID    UNIQUE_ID,
         Block_ID    UNIQUE_ID,
         is_implicit    BOOLEAN,
         Loop_Var_ID    UNIQUE_ID,
         Set_Var_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID );
CREATE TABLE ACT_EL (
         Statement_ID    UNIQUE_ID,
         Block_ID    UNIQUE_ID,
         Value_ID    UNIQUE_ID,
         If_Statement_ID    UNIQUE_ID );
CREATE TABLE ACT_E (
         Statement_ID    UNIQUE_ID,
         Block_ID    UNIQUE_ID,
         If_Statement_ID    UNIQUE_ID );
CREATE TABLE ACT_DAB (
         Action_ID    UNIQUE_ID,
         Obj_ID    UNIQUE_ID,
         Attr_ID    UNIQUE_ID,
         AttributeWritten    BOOLEAN );
CREATE TABLE ACT_CTL (
         Statement_ID    UNIQUE_ID );
CREATE TABLE ACT_CON (
         Statement_ID    UNIQUE_ID );
CREATE TABLE ACT_BRB (
         Action_ID    UNIQUE_ID,
         Brg_ID    UNIQUE_ID );
CREATE TABLE ACT_BRK (
         Statement_ID    UNIQUE_ID );
CREATE TABLE ACT_ACT (
         Action_ID    UNIQUE_ID,
         Type    STRING,
         LoopLevel    INTEGER,
         Block_ID    UNIQUE_ID,
         CurrentScope_ID    UNIQUE_ID,
         return_value    INTEGER,
         Label    STRING,
         Parsed_Block_ID    UNIQUE_ID );
CREATE TABLE ACT_BLK (
         Block_ID    UNIQUE_ID,
         WhereSpecOK    BOOLEAN,
         InWhereSpec    BOOLEAN,
         SelectedFound    BOOLEAN,
         TempBuffer    STRING,
         SupData1    STRING,
         SupData2    STRING,
         CurrentLine    INTEGER,
         CurrentCol    INTEGER,
         currentKeyLettersLineNumber    INTEGER,
         currentKeyLettersColumn    INTEGER,
         currentParameterAssignmentNameLineNumber    INTEGER,
         currentParameterAssignmentNameColumn    INTEGER,
         currentAssociationNumberLineNumber    INTEGER,
         currentAssociationNumberColumn    INTEGER,
         currentAssociationPhraseLineNumber    INTEGER,
         currentAssociationPhraseColumn    INTEGER,
         currentDataTypeNameLineNumber    INTEGER,
         currentDataTypeNameColumn    INTEGER,
         blockInStackFrameCreated    BOOLEAN,
         Action_ID    UNIQUE_ID,
         Parsed_Action_ID    UNIQUE_ID );
CREATE TABLE R_SUBSUP (
         Rel_ID    UNIQUE_ID );
CREATE TABLE R_SIMP (
         Rel_ID    UNIQUE_ID );
CREATE TABLE R_RGO (
         Obj_ID    UNIQUE_ID,
         Rel_ID    UNIQUE_ID,
         OIR_ID    UNIQUE_ID );
CREATE TABLE R_RTO (
         Obj_ID    UNIQUE_ID,
         Rel_ID    UNIQUE_ID,
         OIR_ID    UNIQUE_ID,
         Oid_ID    INTEGER );
CREATE TABLE R_ASSOC (
         Rel_ID    UNIQUE_ID );
CREATE TABLE R_COMP (
         Rel_ID    UNIQUE_ID,
         Rel_Chn    STRING );
CREATE TABLE R_OIR (
         Obj_ID    UNIQUE_ID,
         Rel_ID    UNIQUE_ID,
         OIR_ID    UNIQUE_ID,
         IObj_ID    UNIQUE_ID );
CREATE TABLE R_SUPER (
         Obj_ID    UNIQUE_ID,
         Rel_ID    UNIQUE_ID,
         OIR_ID    UNIQUE_ID );
CREATE TABLE R_SUB (
         Obj_ID    UNIQUE_ID,
         Rel_ID    UNIQUE_ID,
         OIR_ID    UNIQUE_ID );
CREATE TABLE R_PART (
         Obj_ID    UNIQUE_ID,
         Rel_ID    UNIQUE_ID,
         OIR_ID    UNIQUE_ID,
         Mult    INTEGER,
         Cond    INTEGER,
         Txt_Phrs    STRING );
CREATE TABLE R_FORM (
         Obj_ID    UNIQUE_ID,
         Rel_ID    UNIQUE_ID,
         OIR_ID    UNIQUE_ID,
         Mult    INTEGER,
         Cond    INTEGER,
         Txt_Phrs    STRING );
CREATE TABLE R_ASSR (
         Obj_ID    UNIQUE_ID,
         Rel_ID    UNIQUE_ID,
         OIR_ID    UNIQUE_ID,
         Mult    INTEGER );
CREATE TABLE R_COTH (
         Obj_ID    UNIQUE_ID,
         Rel_ID    UNIQUE_ID,
         OIR_ID    UNIQUE_ID,
         Mult    INTEGER,
         Cond    INTEGER,
         Txt_Phrs    STRING );
CREATE TABLE R_CONE (
         Obj_ID    UNIQUE_ID,
         Rel_ID    UNIQUE_ID,
         OIR_ID    UNIQUE_ID,
         Mult    INTEGER,
         Cond    INTEGER,
         Txt_Phrs    STRING );
CREATE TABLE R_AOTH (
         Obj_ID    UNIQUE_ID,
         Rel_ID    UNIQUE_ID,
         OIR_ID    UNIQUE_ID,
         Mult    INTEGER,
         Cond    INTEGER,
         Txt_Phrs    STRING );
CREATE TABLE R_AONE (
         Obj_ID    UNIQUE_ID,
         Rel_ID    UNIQUE_ID,
         OIR_ID    UNIQUE_ID,
         Mult    INTEGER,
         Cond    INTEGER,
         Txt_Phrs    STRING );
CREATE TABLE R_REL (
         Rel_ID    UNIQUE_ID,
         Numb    INTEGER,
         Descrip    STRING,
         SS_ID    UNIQUE_ID );
CREATE TABLE A_SS (
         Id    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING );
CREATE TABLE A_OBJ (
         Id    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING );
CREATE TABLE A_INI (
         Id    UNIQUE_ID,
         Descrip    STRING );
CREATE TABLE A_FJ (
         Id    UNIQUE_ID,
         Descrip    STRING,
         GuardCondition    STRING );
CREATE TABLE A_FF (
         Id    UNIQUE_ID,
         Descrip    STRING );
CREATE TABLE A_DM (
         Id    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING );
CREATE TABLE A_CTL (
         Id    UNIQUE_ID );
CREATE TABLE A_AP (
         Id    UNIQUE_ID,
         Package_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING );
CREATE TABLE A_N (
         Id    UNIQUE_ID,
         Package_ID    UNIQUE_ID );
CREATE TABLE A_AIA (
         Package_ID    UNIQUE_ID );
CREATE TABLE A_AF (
         Id    UNIQUE_ID,
         Descrip    STRING );
CREATE TABLE A_E (
         Id    UNIQUE_ID,
         Package_ID    UNIQUE_ID,
         Guard    STRING,
         Descrip    STRING,
         TargetId    UNIQUE_ID,
         SourceId    UNIQUE_ID );
CREATE TABLE A_GA (
         Id    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING );
CREATE TABLE A_A (
         Package_ID    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING,
         Dom_ID    UNIQUE_ID,
         SS_ID    UNIQUE_ID,
         Parent_Package_ID    UNIQUE_ID,
         Sys_ID    UNIQUE_ID,
         Component_Package_ID    UNIQUE_ID,
         Component_Id    UNIQUE_ID );
CREATE TABLE A_ACT (
         Id    UNIQUE_ID );
CREATE TABLE A_ATE (
         Id    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING );
CREATE TABLE A_AEA (
         Id    UNIQUE_ID,
         Name    STRING,
         Descrip    STRING );
CREATE TABLE A_AE (
         Id    UNIQUE_ID );

CREATE ROP REF_ID R3201 FROM MC     S_AW     ( Sync_ID )
                 TO 1C  S_SYNC     ( Sync_ID );
CREATE ROP REF_ID R3200 FROM 1C     S_AW     ( Brg_ID )
                 TO 1      S_BRG     ( Brg_ID );
CREATE ROP REF_ID R800 FROM 1C     V_PAR     ( Value_ID )
                 TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R804 FROM 1C     V_UNY     ( Operand_Value_ID )
                 TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R803 FROM 1C     V_BIN     ( Right_Value_ID )
                 TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R802 FROM 1C     V_BIN     ( Left_Value_ID )
                 TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_FNV     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_PVL     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_SLR     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_BRV     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_IRF     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_AVL     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_LIN     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_LST     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_UNY     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_TRV     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_ISR     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_EDV     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_TVL     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_LRL     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_LBO     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_BIN     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_LEN     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_MVL     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_AER     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_ALV     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_MSV     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R801 FROM 1C     V_SCV     ( Value_ID )
             TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R814 FROM 1C     V_INT     ( Var_ID )
             TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R814 FROM 1C     V_INS     ( Var_ID )
             TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R814 FROM 1C     V_TRN     ( Var_ID )
             TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R805 FROM MC     V_TVL     ( Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R808 FROM MC     V_IRF     ( Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R809 FROM MC     V_ISR     ( Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R818 FROM MC     V_INT     ( Obj_ID )
                 TO 1      O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R819 FROM MC     V_INS     ( Obj_ID )
                 TO 1      O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R820 FROM MC     V_VAL     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R821 FROM MC     V_TRN     ( DT_ID )
                 TO 1C  S_DT     ( DT_ID );
CREATE ROP REF_ID R823 FROM MC     V_VAR     ( Block_ID )
                 TO 1      ACT_BLK     ( Block_ID );
CREATE ROP REF_ID R806 FROM MC     V_AVL     ( Attr_ID , Obj_ID )
                 TO 1      O_ATTR     ( Attr_ID , Obj_ID );
CREATE ROP REF_ID R824 FROM MC     V_LEN     ( Enum_ID )
                 TO 1      S_ENUM     ( Enum_ID );
CREATE ROP REF_ID R825 FROM 1C     V_SLR     ( Op_Value_ID )
                 TO 1C  V_TRV     ( Value_ID );
CREATE ROP REF_ID R826 FROM MC     V_VAL     ( Block_ID )
                 TO 1      ACT_BLK     ( Block_ID );
CREATE ROP REF_ID R817 FROM MC     V_PAR     ( Invocation_Value_ID )
                 TO 1C  V_FNV     ( Value_ID );
CREATE ROP REF_ID R810 FROM MC     V_PAR     ( Invocation_Value_ID )
                 TO 1C  V_BRV     ( Value_ID );
CREATE ROP REF_ID R811 FROM MC     V_PAR     ( Invocation_Value_ID )
                 TO 1C  V_TRV     ( Value_ID );
CREATE ROP REF_ID R827 FROM MC     V_FNV     ( Sync_ID )
                 TO 1      S_SYNC     ( Sync_ID );
CREATE ROP REF_ID R828 FROM MC     V_BRV     ( Brg_ID )
                 TO 1      S_BRG     ( Brg_ID );
CREATE ROP REF_ID R829 FROM MC     V_TRV     ( Tfr_ID )
                 TO 1      O_TFR     ( Tfr_ID );
CREATE ROP REF_ID R816 FROM 1C     V_PAR     ( Next_Value_ID )  PHRASE 'precedes'
                 TO 1C  V_PAR     ( Value_ID )  PHRASE 'succeeds';
CREATE ROP REF_ID R830 FROM MC     V_TRV     ( Var_ID )
                 TO 1C  V_VAR     ( Var_ID );
CREATE ROP REF_ID R831 FROM MC     V_PVL     ( BParm_ID )
                 TO 1C  S_BPARM     ( BParm_ID );
CREATE ROP REF_ID R832 FROM MC     V_PVL     ( SParm_ID )
                 TO 1C  S_SPARM     ( SParm_ID );
CREATE ROP REF_ID R833 FROM MC     V_PVL     ( TParm_ID )
                 TO 1C  O_TPARM     ( TParm_ID );
CREATE ROP REF_ID R835 FROM M     V_LOC     ( Var_ID )
                 TO 1C  V_VAR     ( Var_ID );
CREATE ROP REF_ID R812 FROM MC     V_SLR     ( Attr_ID , Obj_ID )
                 TO 1C  O_ATTR     ( Attr_ID , Obj_ID );
CREATE ROP REF_ID R836 FROM MC     V_MVL     ( Member_ID , DT_DT_ID )
                 TO 1      S_MBR     ( Member_ID , Parent_DT_DT_ID );
CREATE ROP REF_ID R837 FROM 1C     V_MVL     ( Root_Value_ID )
                 TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R807 FROM 1C     V_AVL     ( Root_Value_ID )
                 TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R838 FROM 1C     V_AER     ( Root_Value_ID )
                 TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R839 FROM 1C     V_AER     ( Index_Value_ID )
                 TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R840 FROM 1C     V_ALV     ( Array_Value_ID )
                 TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R842 FROM MC     V_PAR     ( Invocation_Value_ID )
                 TO 1C  V_MSV     ( Value_ID );
CREATE ROP REF_ID R843 FROM MC     V_PVL     ( PP_Id )
                 TO 1C  C_PP     ( PP_Id );
CREATE ROP REF_ID R844 FROM MC     S_DIM     ( Var_ID )
                 TO 1C  V_TRN     ( Var_ID );
CREATE ROP REF_ID R841 FROM MC     V_MSV     ( PEP_Id )
                 TO 1C  SPR_PEP     ( Id );
CREATE ROP REF_ID R845 FROM MC     V_MSV     ( REP_Id )
                 TO 1C  SPR_REP     ( Id );
CREATE ROP REF_ID R834 FROM MC     V_EPR     ( Value_ID )
                 TO 1      V_EDV     ( Value_ID );
CREATE ROP REF_ID R846 FROM MC     V_EPR     ( SM_ID , SMedi_ID )
                 TO 1C  SM_EVTDI     ( SM_ID , SMedi_ID );
CREATE ROP REF_ID R847 FROM MC     V_EPR     ( PP_Id )
                 TO 1C  C_PP     ( PP_Id );
CREATE ROP REF_ID R848 FROM MC     V_VAR     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R849 FROM MC     S_DIM     ( Var_ID )
                 TO 1C  V_VAR     ( Var_ID );
CREATE ROP REF_ID R850 FROM MC     V_SCV     ( Const_ID , DT_ID )
                 TO 1      CNST_SYC     ( Const_ID , DT_ID );
CREATE ROP REF_ID R851 FROM MC     V_MSV     ( Target_Value_ID )
                 TO 1C  V_VAL     ( Value_ID );
CREATE ROP REF_ID R1201 FROM MC     UC_UCC     ( Dom_ID )
                 TO 1C  S_DOM     ( Dom_ID );
CREATE ROP REF_ID R1202 FROM MC     UC_UCC     ( SS_ID )
                 TO 1C  S_SS     ( SS_ID );
CREATE ROP REF_ID R1208 FROM 1C     UC_UIU     ( Package_ID )
                 TO 1      UC_UCC     ( Package_ID );
CREATE ROP REF_ID R1209 FROM MC     UC_UCC     ( Parent_Package_ID )
                 TO 1C  UC_UIU     ( Package_ID );
CREATE ROP REF_ID R1210 FROM 1C     UC_E     ( Assoc_ID )
             TO 1      UC_UCA     ( Assoc_ID );
CREATE ROP REF_ID R1210 FROM 1C     UC_G     ( Assoc_ID )
             TO 1      UC_UCA     ( Assoc_ID );
CREATE ROP REF_ID R1210 FROM 1C     UC_I     ( Assoc_ID )
             TO 1      UC_UCA     ( Assoc_ID );
CREATE ROP REF_ID R1210 FROM 1C     UC_BA     ( Assoc_ID )
             TO 1      UC_UCA     ( Assoc_ID );
CREATE ROP REF_ID R1203 FROM MC     UC_PIUC     ( Package_ID )
                 TO 1      UC_UCC     ( Package_ID );
CREATE ROP REF_ID R1203 FROM 1C     UC_PIUC     ( Part_ID )
                 TO 1      SQ_P     ( Part_ID );
CREATE ROP REF_ID R1206 FROM MC     UC_UCA     ( Source_Part_ID )
                 TO 1      SQ_P     ( Part_ID );
CREATE ROP REF_ID R1207 FROM MC     UC_UCA     ( Destination_Part_ID )
                 TO 1      SQ_P     ( Part_ID );
CREATE ROP REF_ID R1211 FROM MC     UC_UCC     ( Sys_ID )
                 TO 1C  S_SYS     ( Sys_ID );
CREATE ROP REF_ID R1212 FROM MC     UC_UCC     ( Component_Package_ID )
                 TO 1C  CP_CP     ( Package_ID );
CREATE ROP REF_ID R1213 FROM MC     UC_UCC     ( Component_Id )
                 TO 1C  C_C     ( Id );
CREATE ROP REF_ID R1214 FROM MC     UC_AIUC     ( Package_ID )
                 TO 1      UC_UCC     ( Package_ID );
CREATE ROP REF_ID R1215 FROM 1C     UC_AIUC     ( Assoc_ID )
                 TO 1      UC_UCA     ( Assoc_ID );
CREATE ROP REF_ID R4400 FROM MC     SLD_SDP     ( Sys_ID )
                 TO 1      S_SYS     ( Sys_ID );
CREATE ROP REF_ID R4400 FROM 1C     SLD_SDP     ( Package_ID )
                 TO 1      S_DPK     ( Package_ID );
CREATE ROP REF_ID R4401 FROM MC     SLD_SDINP     ( Package_ID )
                 TO 1      S_DPK     ( Package_ID );
CREATE ROP REF_ID R4401 FROM MC     SLD_SDINP     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R4402 FROM MC     SLD_SDINP     ( Sys_ID )
                 TO 1      S_SYS     ( Sys_ID );
CREATE ROP REF_ID R4404 FROM MC     SLD_SCINP     ( Sys_ID )
                 TO 1      S_SYS     ( Sys_ID );
CREATE ROP REF_ID R4403 FROM MC     SLD_SCINP     ( Package_ID )
                 TO 1      S_DPK     ( Package_ID );
CREATE ROP REF_ID R4403 FROM MC     SLD_SCINP     ( Constant_Spec_ID )
                 TO 1      CNST_CSP     ( Constant_Spec_ID );
CREATE ROP REF_ID R117 FROM MC     O_TPARM     ( Tfr_ID )
                 TO 1      O_TFR     ( Tfr_ID );
CREATE ROP REF_ID R118 FROM MC     O_TPARM     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R116 FROM MC     O_TFR     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R115 FROM MC     O_TFR     ( Obj_ID )
                 TO 1      O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R102 FROM MC     O_ATTR     ( Obj_ID )
                 TO 1      O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R103 FROM 1C     O_ATTR     ( PAttr_ID , Obj_ID )  PHRASE 'succeeds'
                 TO 1C  O_ATTR     ( Attr_ID , Obj_ID )  PHRASE 'precedes';
CREATE ROP REF_ID R114 FROM MC     O_ATTR     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R106 FROM 1C     O_BATTR     ( Attr_ID , Obj_ID )
             TO 1      O_ATTR     ( Attr_ID , Obj_ID );
CREATE ROP REF_ID R106 FROM 1C     O_RATTR     ( Attr_ID , Obj_ID )
             TO 1      O_ATTR     ( Attr_ID , Obj_ID );
CREATE ROP REF_ID R113 FROM MC     O_RATTR     ( BAttr_ID , BObj_ID )
                 TO 1      O_BATTR     ( Attr_ID , Obj_ID );
CREATE ROP REF_ID R107 FROM 1C     O_DBATTR     ( Attr_ID , Obj_ID )
             TO 1      O_BATTR     ( Attr_ID , Obj_ID );
CREATE ROP REF_ID R107 FROM 1C     O_NBATTR     ( Attr_ID , Obj_ID )
             TO 1      O_BATTR     ( Attr_ID , Obj_ID );
CREATE ROP REF_ID R108 FROM M     O_REF     ( Attr_ID , Obj_ID )
                 TO 1      O_RATTR     ( Attr_ID , Obj_ID );
CREATE ROP REF_ID R112 FROM 1C     O_REF     ( PARef_ID )  PHRASE 'succeeds'
                 TO 1C  O_REF     ( ARef_ID )  PHRASE 'precedes';
CREATE ROP REF_ID R105 FROM MC     O_OIDA     ( Oid_ID , Obj_ID )
                 TO 1      O_ID     ( Oid_ID , Obj_ID );
CREATE ROP REF_ID R105 FROM MC     O_OIDA     ( Attr_ID , Obj_ID )
                 TO 1      O_ATTR     ( Attr_ID , Obj_ID );
CREATE ROP REF_ID R104 FROM MC     O_ID     ( Obj_ID )
                 TO 1      O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R101 FROM MC     O_IOBJ     ( Obj_ID )
                 TO 1C  O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R110 FROM MC    O_RTIDA     ( Oid_ID , OIR_ID , Obj_ID , Rel_ID )
                 TO 1      R_RTO     ( Oid_ID , OIR_ID , Obj_ID , Rel_ID );
CREATE ROP REF_ID R110 FROM MC     O_RTIDA     ( Attr_ID , Oid_ID , Obj_ID )
                 TO 1      O_OIDA     ( Attr_ID , Oid_ID , Obj_ID );
CREATE ROP REF_ID R109 FROM MC     R_RTO     ( Oid_ID , Obj_ID )
                 TO 1C  O_ID     ( Oid_ID , Obj_ID );
CREATE ROP REF_ID R111 FROM MC     O_REF     ( OIR_ID , Obj_ID , Rel_ID )
                 TO 1      R_RGO     ( OIR_ID , Obj_ID , Rel_ID );
CREATE ROP REF_ID R111 FROM MC     O_REF     ( RAttr_ID , ROIR_ID , ROid_ID , RObj_ID , Rel_ID )
                 TO 1      O_RTIDA     ( Attr_ID , OIR_ID , Oid_ID , Obj_ID , Rel_ID );
CREATE ROP REF_ID R120 FROM MC     S_DIM     ( Attr_ID , Obj_ID )
                 TO 1C  O_ATTR     ( Attr_ID , Obj_ID );
CREATE ROP REF_ID R121 FROM MC     S_DIM     ( TParm_ID )
                 TO 1C  O_TPARM     ( TParm_ID );
CREATE ROP REF_ID R122 FROM MC     S_DIM     ( Tfr_ID )
                 TO 1C  O_TFR     ( Tfr_ID );
CREATE ROP REF_ID R123 FROM MC     S_IRDT     ( Obj_ID )
                 TO 1      O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R124 FROM 1C     O_TPARM     ( Previous_TParm_ID )  PHRASE 'succeeds'
                 TO 1C  O_TPARM     ( TParm_ID )  PHRASE 'precedes';
CREATE ROP REF_ID R125 FROM 1C     O_TFR     ( Previous_Tfr_ID )  PHRASE 'succeeds'
                 TO 1C  O_TFR     ( Tfr_ID )  PHRASE 'precedes';
CREATE ROP REF_ID R502 FROM MC     SM_EVT     ( SM_ID )
                 TO 1      SM_SM     ( SM_ID );
CREATE ROP REF_ID R501 FROM MC     SM_STATE     ( SM_ID )
                 TO 1      SM_SM     ( SM_ID );
CREATE ROP REF_ID R504 FROM 1C     SM_EIGN     ( SMspd_ID , SMevt_ID , SM_ID , SMstt_ID )
             TO 1      SM_SEME     ( SMspd_ID , SMevt_ID , SM_ID , SMstt_ID );
CREATE ROP REF_ID R504 FROM 1C     SM_CH     ( SMspd_ID , SMevt_ID , SM_ID , SMstt_ID )
             TO 1      SM_SEME     ( SMspd_ID , SMevt_ID , SM_ID , SMstt_ID );
CREATE ROP REF_ID R504 FROM 1C     SM_NSTXN     ( SMspd_ID , SMevt_ID , SM_ID , SMstt_ID )
             TO 1      SM_SEME     ( SMspd_ID , SMevt_ID , SM_ID , SMstt_ID );
CREATE ROP REF_ID R507 FROM 1C     SM_NETXN     ( Trans_ID , SM_ID )
             TO 1      SM_TXN     ( Trans_ID , SM_ID );
CREATE ROP REF_ID R507 FROM 1C     SM_CRTXN     ( Trans_ID , SM_ID )
             TO 1      SM_TXN     ( Trans_ID , SM_ID );
CREATE ROP REF_ID R507 FROM 1C     SM_NSTXN     ( Trans_ID , SM_ID )
             TO 1      SM_TXN     ( Trans_ID , SM_ID );
CREATE ROP REF_ID R508 FROM MC     SM_NETXN     ( SM_ID , SMstt_ID )
                 TO 1      SM_STATE     ( SM_ID , SMstt_ID );
CREATE ROP REF_ID R506 FROM MC     SM_TXN     ( SMspd_ID , SMstt_ID , SM_ID )
                 TO 1      SM_STATE     ( SMspd_ID , SMstt_ID , SM_ID );
CREATE ROP REF_ID R505 FROM MC     SM_TXN     ( SM_ID )
                 TO 1      SM_SM     ( SM_ID );
CREATE ROP REF_ID R510 FROM 1C     SM_MEALY     ( SM_ID )
             TO 1      SM_SM     ( SM_ID );
CREATE ROP REF_ID R510 FROM 1C     SM_MOORE     ( SM_ID )
             TO 1      SM_SM     ( SM_ID );
CREATE ROP REF_ID R511 FROM MC     SM_MOAH     ( SM_ID )
                 TO 1      SM_MOORE     ( SM_ID );
CREATE ROP REF_ID R511 FROM 1C     SM_MOAH     ( SM_ID , SMstt_ID )
                 TO 1      SM_STATE     ( SM_ID , SMstt_ID );
CREATE ROP REF_ID R512 FROM M     SM_MEAH     ( SM_ID )
                 TO 1      SM_MEALY     ( SM_ID );
CREATE ROP REF_ID R512 FROM 1C     SM_MEAH     ( Trans_ID , SM_ID )
                 TO 1      SM_TXN     ( Trans_ID , SM_ID );
CREATE ROP REF_ID R513 FROM 1C     SM_MOAH     ( Act_ID , SM_ID )
             TO 1      SM_AH     ( Act_ID , SM_ID );
CREATE ROP REF_ID R513 FROM 1C     SM_MEAH     ( Act_ID , SM_ID )
             TO 1      SM_AH     ( Act_ID , SM_ID );
CREATE ROP REF_ID R513 FROM 1C     SM_TAH     ( Act_ID , SM_ID )
             TO 1      SM_AH     ( Act_ID , SM_ID );
CREATE ROP REF_ID R514 FROM 1      SM_AH    ( SM_ID , Act_ID )
                 TO 1      SM_ACT     ( SM_ID , Act_ID );
CREATE ROP REF_ID R515 FROM MC     SM_ACT     ( SM_ID )
                 TO 1      SM_SM     ( SM_ID );
CREATE ROP REF_ID R517 FROM 1C     SM_ISM     ( SM_ID )
             TO 1      SM_SM     ( SM_ID );
CREATE ROP REF_ID R517 FROM 1C     SM_ASM     ( SM_ID )
             TO 1      SM_SM     ( SM_ID );
CREATE ROP REF_ID R518 FROM 1C     SM_ISM     ( Obj_ID )
                 TO 1      O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R519 FROM 1C     SM_ASM     ( Obj_ID )
                 TO 1      O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R516 FROM MC     SM_EVTDI     ( SM_ID )
                 TO 1      SM_SM     ( SM_ID );
CREATE ROP REF_ID R521 FROM MC     SM_STATE     ( SMspd_ID , SM_ID )
                 TO 1C  SM_SUPDT     ( SMspd_ID , SM_ID );
CREATE ROP REF_ID R520 FROM M     SM_EVT     ( SMspd_ID , SM_ID )
                 TO 1C  SM_SUPDT     ( SMspd_ID , SM_ID );
CREATE ROP REF_ID R522 FROM MC     SM_SDI     ( SMspd_ID , SM_ID )
                 TO 1      SM_SUPDT     ( SMspd_ID , SM_ID );
CREATE ROP REF_ID R522 FROM MC     SM_SDI     ( SM_ID , SMedi_ID )
                 TO 1      SM_EVTDI     ( SM_ID , SMedi_ID );
CREATE ROP REF_ID R523 FROM MC     SM_SUPDT     ( SM_ID )
                 TO 1      SM_SM     ( SM_ID );
CREATE ROP REF_ID R524 FROM MC     SM_EVTDI     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R525 FROM 1C     SM_SEVT     ( SM_ID , SMevt_ID , SMspd_ID )
             TO 1      SM_EVT     ( SM_ID , SMevt_ID , SMspd_ID );
CREATE ROP REF_ID R525 FROM 1C     SM_PEVT     ( SM_ID , SMevt_ID , SMspd_ID )
             TO 1      SM_EVT     ( SM_ID , SMevt_ID , SMspd_ID );
CREATE ROP REF_ID R503 FROM MC     SM_SEME     ( SM_ID , SMstt_ID )
                 TO 1      SM_STATE     ( SM_ID , SMstt_ID );
CREATE ROP REF_ID R503 FROM MC     SM_SEME     ( SMevt_ID , SM_ID , SMspd_ID )
                 TO 1      SM_SEVT     ( SMevt_ID , SM_ID , SMspd_ID );
CREATE ROP REF_ID R526 FROM 1C     SM_NLEVT     ( SMevt_ID , SM_ID , SMspd_ID )
             TO 1      SM_SEVT     ( SMevt_ID , SM_ID , SMspd_ID );
CREATE ROP REF_ID R526 FROM 1C     SM_LEVT     ( SMevt_ID , SM_ID , SMspd_ID )
             TO 1      SM_SEVT     ( SMevt_ID , SM_ID , SMspd_ID );
CREATE ROP REF_ID R526 FROM 1C     SM_SGEVT     ( SMevt_ID , SM_ID , SMspd_ID )
             TO 1      SM_SEVT     ( SMevt_ID , SM_ID , SMspd_ID );
CREATE ROP REF_ID R509 FROM 1C     SM_CRTXN     ( SM_ID , SMevt_ID )
                 TO 1C  SM_LEVT     ( SM_ID , SMevt_ID );
CREATE ROP REF_ID R527 FROM MC     SM_NLEVT     ( polySM_ID , polySMevt_ID )
                 TO 1      SM_PEVT     ( SM_ID , SMevt_ID );
CREATE ROP REF_ID R528 FROM 1C     SM_SGEVT     ( Provided_Signal_Id )
                 TO 1C  SPR_PS     ( Id );
CREATE ROP REF_ID R529 FROM 1C     SM_SGEVT     ( Required_Signal_Id )
                 TO 1C  SPR_RS     ( Id );
CREATE ROP REF_ID R530 FROM 1C     SM_TAH     ( Trans_ID , SM_ID )
                 TO 1      SM_TXN     ( Trans_ID , SM_ID );
CREATE ROP REF_ID R531 FROM MC     S_DIM     ( SM_ID , SMedi_ID )
                 TO 1C  SM_EVTDI     ( SM_ID , SMedi_ID );
CREATE ROP REF_ID R532 FROM MC     SM_EVTDI     ( SMevt_ID )
                 TO 1      SM_EVT     ( SMevt_ID );
CREATE ROP REF_ID R533 FROM 1C     SM_EVTDI     ( SM_ID , Previous_SMedi_ID )  PHRASE 'succeeds'
                 TO 1C  SM_EVTDI     ( SM_ID , SMedi_ID )  PHRASE 'precedes';
CREATE ROP REF_ID R913 FROM MC     SQ_S     ( Dom_ID )
                 TO 1C  S_DOM     ( Dom_ID );
CREATE ROP REF_ID R914 FROM MC     SQ_S     ( SS_ID )
                 TO 1C  S_SS     ( SS_ID );
CREATE ROP REF_ID R928 FROM MC     SQ_S     ( Prev_Package_ID )
                 TO 1C  SQ_SIS     ( Package_ID );
CREATE ROP REF_ID R911 FROM 1C     SQ_SIS     ( Package_ID )
                 TO 1      SQ_S     ( Package_ID );
CREATE ROP REF_ID R929 FROM MC     SQ_P     ( Sequence_Package_ID )
                 TO 1C  SQ_S     ( Package_ID );
CREATE ROP REF_ID R950 FROM MC     SQ_S     ( Sys_ID )
                 TO 1C  S_SYS     ( Sys_ID );
CREATE ROP REF_ID R951 FROM MC     SQ_S     ( Component_Package_ID )
                 TO 1C  CP_CP     ( Package_ID );
CREATE ROP REF_ID R952 FROM MC     SQ_S     ( Component_Id )
                 TO 1C  C_C     ( Id );
CREATE ROP REF_ID R953 FROM MC     SQ_MIS     ( Package_ID )
                 TO 1      SQ_S     ( Package_ID );
CREATE ROP REF_ID R954 FROM 1C     SQ_MIS     ( Msg_ID )
                 TO 1      MSG_M     ( Msg_ID );
CREATE ROP REF_ID R604 FROM 1C     ACT_LNK     ( Next_Link_ID )  PHRASE 'precedes'
                 TO 1C  ACT_LNK     ( Link_ID )  PHRASE 'succeeds';
CREATE ROP REF_ID R664 FROM 1C     ACT_SRW     ( Statement_ID )
             TO 1      ACT_SEL     ( Statement_ID );
CREATE ROP REF_ID R664 FROM 1C     ACT_SR     ( Statement_ID )
             TO 1      ACT_SEL     ( Statement_ID );
CREATE ROP REF_ID R610 FROM 1C     ACT_FIW     ( Where_Clause_Value_ID )
                 TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R611 FROM 1C     ACT_SRW     ( Where_Clause_Value_ID )
                 TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R665 FROM MC     ACT_FIW     ( Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R639 FROM MC     ACT_FIO     ( Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R638 FROM MC     ACT_SEL     ( Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R676 FROM MC     ACT_FIW     ( Obj_ID )
                 TO 1C  O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R677 FROM MC     ACT_FIO     ( Obj_ID )
                 TO 1C  O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R678 FROM MC     ACT_LNK     ( Obj_ID )
                 TO 1      O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R681 FROM MC     ACT_LNK     ( Rel_ID )
                 TO 1      R_REL     ( Rel_ID );
CREATE ROP REF_ID R637 FROM 1      ACT_LNK    ( Statement_ID )
                 TO 1C  ACT_SEL     ( Statement_ID );
CREATE ROP REF_ID R613 FROM 1C     ACT_SEL     ( Value_ID )
                 TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R9800 FROM MC     SR_M     ( Result_Id )
                 TO 1      SR_SR     ( Id );
CREATE ROP REF_ID R9801 FROM 1C     SR_NM     ( Id )
             TO 1      SR_M     ( Id );
CREATE ROP REF_ID R9801 FROM 1C     SR_CM     ( Id )
             TO 1      SR_M     ( Id );
CREATE ROP REF_ID R9802 FROM 1C     SR_SR     ( MatchedParticipant_Id )
                 TO 1      SP_SP     ( Id );
CREATE ROP REF_ID R9600 FROM 1C     SQU_D     ( Id )
             TO 1      SQU_Q     ( Id );
CREATE ROP REF_ID R9600 FROM 1C     SQU_R     ( Id )
             TO 1      SQU_Q     ( Id );
CREATE ROP REF_ID R9600 FROM 1C     SQU_DE     ( Id )
             TO 1      SQU_Q     ( Id );
CREATE ROP REF_ID R9600 FROM 1C     SQU_A     ( Id )
             TO 1      SQU_Q     ( Id );
CREATE ROP REF_ID R9700 FROM 1      SP_SE    ( Participant_Id )
                 TO 1      SP_SP     ( Id );
CREATE ROP REF_ID R9702 FROM 1C     SP_NS     ( Id )
             TO 1      SP_SE     ( Id );
CREATE ROP REF_ID R9702 FROM 1C     SP_ALS     ( Id )
             TO 1      SP_SE     ( Id );
CREATE ROP REF_ID R9702 FROM 1C     SP_DS     ( Id )
             TO 1      SP_SE     ( Id );
CREATE ROP REF_ID R9500 FROM 1      SQU_Q    ( Engine_Id )
                 TO 1C  SEN_E     ( Id );
CREATE ROP REF_ID R9501 FROM 1C     SEN_ALE     ( Id )
             TO 1      SEN_E     ( Id );
CREATE ROP REF_ID R9501 FROM 1C     SEN_DE     ( Id )
             TO 1      SEN_E     ( Id );
CREATE ROP REF_ID R9501 FROM 1C     SEN_DCE     ( Id )
             TO 1      SEN_E     ( Id );
CREATE ROP REF_ID R9501 FROM 1C     SEN_RE     ( Id )
             TO 1      SEN_E     ( Id );
CREATE ROP REF_ID R9502 FROM MC     SP_SP     ( Engine_Id )
                 TO 1      SEN_E     ( Id );
CREATE ROP REF_ID R9503 FROM MC     SR_SR     ( Engine_Id )
                 TO 1      SEN_E     ( Id );
CREATE ROP REF_ID R615 FROM MC     ACT_REL     ( One_Side_Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R616 FROM MC     ACT_REL     ( Other_Side_Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R617 FROM MC     ACT_RU     ( One_Side_Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R618 FROM MC     ACT_RU     ( Other_Side_Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R619 FROM MC     ACT_RU     ( Associative_Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R620 FROM MC     ACT_UNR     ( One_Side_Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R621 FROM MC     ACT_UNR     ( Other_Side_Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R622 FROM MC     ACT_URU     ( One_Side_Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R623 FROM MC     ACT_URU     ( Other_Side_Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R624 FROM MC     ACT_URU     ( Associative_Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R653 FROM MC     ACT_REL     ( Rel_ID )
                 TO 1      R_REL     ( Rel_ID );
CREATE ROP REF_ID R654 FROM MC     ACT_RU     ( Rel_ID )
                 TO 1      R_REL     ( Rel_ID );
CREATE ROP REF_ID R655 FROM MC     ACT_UNR     ( Rel_ID )
                 TO 1      R_REL     ( Rel_ID );
CREATE ROP REF_ID R656 FROM MC     ACT_URU     ( Rel_ID )
                 TO 1      R_REL     ( Rel_ID );
CREATE ROP REF_ID R9002 FROM MC     PA_DIC     ( Component_Id )
                 TO 1      C_C     ( Id );
CREATE ROP REF_ID R9002 FROM 1      PA_DIC     ( Delegation_Id )
                 TO 1      C_DG     ( Id );
CREATE ROP REF_ID R9001 FROM 1C     PA_SICP     ( Satisfaction_Id )
                 TO 1      C_SF     ( Id );
CREATE ROP REF_ID R9001 FROM MC     PA_SICP     ( ComponentPackage_ID )
                 TO 1      CP_CP     ( Package_ID );
CREATE ROP REF_ID R9000 FROM MC     PA_SIC     ( Component_Id )
                 TO 1      C_C     ( Id );
CREATE ROP REF_ID R9000 FROM 1C     PA_SIC     ( Satisfaction_Id )
                 TO 1      C_SF     ( Id );
CREATE ROP REF_ID R8000 FROM MC     PE_PE     ( Package_ID )
                 TO 1C  EP_PKG     ( Package_ID );
CREATE ROP REF_ID R8001 FROM 1C     S_DT     ( DT_ID )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8001 FROM 1C     SQ_P     ( Part_ID )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8001 FROM 1C     UC_UCA     ( Assoc_ID )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8001 FROM 1C     A_N     ( Id )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8001 FROM 1C     O_OBJ     ( Obj_ID )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8001 FROM 1C     C_C     ( Id )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8001 FROM 1C     CL_IC     ( Id )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8001 FROM 1C     C_I     ( Id )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8001 FROM 1C     EP_PKG     ( Package_ID )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8001 FROM 1C     CNST_CSP     ( Constant_Spec_ID )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8001 FROM 1C     A_AP     ( Id )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8001 FROM 1C     A_E     ( Id )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8001 FROM 1C     MSG_M     ( Msg_ID )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8001 FROM 1C     O_IOBJ     ( IObj_ID )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8001 FROM 1C     R_REL     ( Rel_ID )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8001 FROM 1C     S_EE     ( EE_ID )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8001 FROM 1C     S_SYNC     ( Sync_ID )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8001 FROM 1C     C_SF     ( Id )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8001 FROM 1C     C_DG     ( Id )
             TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R8003 FROM MC     PE_PE     ( Component_ID )
                 TO 1C  C_C     ( Id );
CREATE ROP REF_ID R1000 FROM MC     MSG_A     ( Informal_Msg_ID )
                 TO 1C  MSG_M     ( Msg_ID );
CREATE ROP REF_ID R1001 FROM MC     MSG_A     ( Formal_Msg_ID )
                 TO 1C  MSG_M     ( Msg_ID );
CREATE ROP REF_ID R1007 FROM MC     MSG_M     ( Sender_Part_ID )
                 TO 1C  SQ_P     ( Part_ID );
CREATE ROP REF_ID R1008 FROM MC     MSG_M     ( Receiver_Part_ID )
                 TO 1C  SQ_P     ( Part_ID );
CREATE ROP REF_ID R1009 FROM MC     MSG_E     ( SMevt_ID )
                 TO 1C  SM_EVT     ( SMevt_ID );
CREATE ROP REF_ID R1010 FROM MC     MSG_F     ( Sync_ID )
                 TO 1C  S_SYNC     ( Sync_ID );
CREATE ROP REF_ID R1011 FROM MC     MSG_O     ( Tfr_ID )
                 TO 1C  O_TFR     ( Tfr_ID );
CREATE ROP REF_ID R1012 FROM MC     MSG_B     ( Brg_ID )
                 TO 1C  S_BRG     ( Brg_ID );
CREATE ROP REF_ID R1013 FROM 1C     MSG_BA     ( Arg_ID )
             TO 1      MSG_A     ( Arg_ID );
CREATE ROP REF_ID R1013 FROM 1C     MSG_OA     ( Arg_ID )
             TO 1      MSG_A     ( Arg_ID );
CREATE ROP REF_ID R1013 FROM 1C     MSG_FA     ( Arg_ID )
             TO 1      MSG_A     ( Arg_ID );
CREATE ROP REF_ID R1013 FROM 1C     MSG_EA     ( Arg_ID )
             TO 1      MSG_A     ( Arg_ID );
CREATE ROP REF_ID R1013 FROM 1C     MSG_IA     ( Arg_ID )
             TO 1      MSG_A     ( Arg_ID );
CREATE ROP REF_ID R1013 FROM 1C     MSG_EPA     ( Arg_ID )
             TO 1      MSG_A     ( Arg_ID );
CREATE ROP REF_ID R1014 FROM MC     MSG_BA     ( BParm_ID )
                 TO 1C  S_BPARM     ( BParm_ID );
CREATE ROP REF_ID R1015 FROM MC     MSG_OA     ( TParm_ID )
                 TO 1C  O_TPARM     ( TParm_ID );
CREATE ROP REF_ID R1016 FROM MC     MSG_FA     ( SParm_ID )
                 TO 1C  S_SPARM     ( SParm_ID );
CREATE ROP REF_ID R1017 FROM MC     MSG_EA     ( SM_ID , SMedi_ID )
                 TO 1C  SM_EVTDI     ( SM_ID , SMedi_ID );
CREATE ROP REF_ID R1018 FROM 1C     MSG_AM     ( Msg_ID )
             TO 1      MSG_M     ( Msg_ID );
CREATE ROP REF_ID R1018 FROM 1C     MSG_SM     ( Msg_ID )
             TO 1      MSG_M     ( Msg_ID );
CREATE ROP REF_ID R1018 FROM 1C     MSG_R     ( Msg_ID )
             TO 1      MSG_M     ( Msg_ID );
CREATE ROP REF_ID R1019 FROM 1C     MSG_E     ( Msg_ID )
             TO 1      MSG_AM     ( Msg_ID );
CREATE ROP REF_ID R1019 FROM 1C     MSG_IAM     ( Msg_ID )
             TO 1      MSG_AM     ( Msg_ID );
CREATE ROP REF_ID R1019 FROM 1C     MSG_SIG     ( Msg_ID )
             TO 1      MSG_AM     ( Msg_ID );
CREATE ROP REF_ID R1020 FROM 1C     MSG_F     ( Msg_ID )
             TO 1      MSG_SM     ( Msg_ID );
CREATE ROP REF_ID R1020 FROM 1C     MSG_O     ( Msg_ID )
             TO 1      MSG_SM     ( Msg_ID );
CREATE ROP REF_ID R1020 FROM 1C     MSG_B     ( Msg_ID )
             TO 1      MSG_SM     ( Msg_ID );
CREATE ROP REF_ID R1020 FROM 1C     MSG_ISM     ( Msg_ID )
             TO 1      MSG_SM     ( Msg_ID );
CREATE ROP REF_ID R1020 FROM 1C     MSG_IOP     ( Msg_ID )
             TO 1      MSG_SM     ( Msg_ID );
CREATE ROP REF_ID R1021 FROM MC     MSG_SIG     ( Id )
                 TO 1C  C_AS     ( Id );
CREATE ROP REF_ID R1022 FROM MC     MSG_IOP     ( Id )
                 TO 1C  C_IO     ( Id );
CREATE ROP REF_ID R1023 FROM MC     MSG_EPA     ( PP_Id )
                 TO 1C  C_PP     ( PP_Id );
CREATE ROP REF_ID R668 FROM 1C     ACT_RET     ( Value_ID )
                 TO 1C  V_VAL     ( Value_ID );
CREATE ROP REF_ID R669 FROM MC     V_PAR     ( Statement_ID )
                 TO 1C  ACT_FNC     ( Statement_ID );
CREATE ROP REF_ID R628 FROM MC     V_PAR     ( Statement_ID )
                 TO 1C  ACT_BRG     ( Statement_ID );
CREATE ROP REF_ID R627 FROM MC     V_PAR     ( Statement_ID )
                 TO 1C  ACT_TFM     ( Statement_ID );
CREATE ROP REF_ID R667 FROM MC     ACT_TFM     ( Var_ID )
                 TO 1C  V_VAR     ( Var_ID );
CREATE ROP REF_ID R673 FROM MC     ACT_TFM     ( Tfr_ID )
                 TO 1C  O_TFR     ( Tfr_ID );
CREATE ROP REF_ID R674 FROM MC     ACT_BRG     ( Brg_ID )
                 TO 1C  S_BRG     ( Brg_ID );
CREATE ROP REF_ID R675 FROM MC     ACT_FNC     ( Sync_ID )
                 TO 1C  S_SYNC     ( Sync_ID );
CREATE ROP REF_ID R679 FROM MC     V_PAR     ( Statement_ID )
                 TO 1C  ACT_IOP     ( Statement_ID );
CREATE ROP REF_ID R662 FROM MC     V_PAR     ( Statement_ID )
                 TO 1C  ACT_SGN     ( Statement_ID );
CREATE ROP REF_ID R663 FROM MC     ACT_SGN     ( ProvidedSig_Id )
                 TO 1C  SPR_PS     ( Id );
CREATE ROP REF_ID R660 FROM MC     ACT_SGN     ( RequiredSig_Id )
                 TO 1C  SPR_RS     ( Id );
CREATE ROP REF_ID R680 FROM MC     ACT_IOP     ( ProvidedOp_Id )
                 TO 1C  SPR_PO     ( Id );
CREATE ROP REF_ID R657 FROM MC     ACT_IOP     ( RequiredOp_Id )
                 TO 1C  SPR_RO     ( Id );
CREATE ROP REF_ID R630 FROM MC     ACT_SGN     ( Value_ID )
                 TO 1C  V_VAL     ( Value_ID );
CREATE ROP REF_ID R629 FROM MC     ACT_IOP     ( Value_ID )
                 TO 1C  V_VAL     ( Value_ID );
CREATE ROP REF_ID R4300 FROM 1C     IP_IPINIP     ( Package_ID )
                 TO 1      IP_IP     ( Package_ID );
CREATE ROP REF_ID R4301 FROM MC     IP_IP     ( Parent_Package_ID )
                 TO 1C  IP_IPINIP     ( Package_ID );
CREATE ROP REF_ID R4302 FROM MC     IP_IP     ( Direct_Sys_ID )
                 TO 1C  S_SYS     ( Sys_ID );
CREATE ROP REF_ID R4303 FROM MC     C_I     ( Package_ID )
                 TO 1C  IP_IP     ( Package_ID );
CREATE ROP REF_ID R4304 FROM MC     IP_IP     ( Sys_ID )
                 TO 1      S_SYS     ( Sys_ID );
CREATE ROP REF_ID R941 FROM MC     SQ_TS     ( Prev_Mark_ID )
                 TO 1      SQ_TM     ( Mark_ID );
CREATE ROP REF_ID R931 FROM MC     SQ_TM     ( Part_ID )
                 TO 1      SQ_LS     ( Part_ID );
CREATE ROP REF_ID R942 FROM MC     SQ_TS     ( Mark_ID )
                 TO 1      SQ_TM     ( Mark_ID );
CREATE ROP REF_ID R930 FROM 1C     SQ_CIP     ( Part_ID )
             TO 1      SQ_P     ( Part_ID );
CREATE ROP REF_ID R930 FROM 1C     SQ_EEP     ( Part_ID )
             TO 1      SQ_P     ( Part_ID );
CREATE ROP REF_ID R930 FROM 1C     SQ_FPP     ( Part_ID )
             TO 1      SQ_P     ( Part_ID );
CREATE ROP REF_ID R930 FROM 1C     SQ_CP     ( Part_ID )
             TO 1      SQ_P     ( Part_ID );
CREATE ROP REF_ID R930 FROM 1C     SQ_AP     ( Part_ID )
             TO 1      SQ_P     ( Part_ID );
CREATE ROP REF_ID R930 FROM 1C     SQ_LS     ( Part_ID )
             TO 1      SQ_P     ( Part_ID );
CREATE ROP REF_ID R930 FROM 1C     IA_UCP     ( Part_ID )
             TO 1      SQ_P     ( Part_ID );
CREATE ROP REF_ID R930 FROM 1C     SQ_COP     ( Part_ID )
             TO 1      SQ_P     ( Part_ID );
CREATE ROP REF_ID R930 FROM 1C     SQ_PP     ( Part_ID )
             TO 1      SQ_P     ( Part_ID );
CREATE ROP REF_ID R932 FROM MC     SQ_FPP     ( FunPack_ID )
                 TO 1C  S_FPK     ( FunPack_ID );
CREATE ROP REF_ID R933 FROM MC     SQ_EEP     ( EE_ID )
                 TO 1C  S_EE     ( EE_ID );
CREATE ROP REF_ID R934 FROM MC     SQ_CIP     ( Obj_ID )
                 TO 1C  O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R935 FROM MC     SQ_CPA     ( Part_ID )
                 TO 1      SQ_CP     ( Part_ID );
CREATE ROP REF_ID R936 FROM MC     SQ_AV     ( Informal_Part_ID )
                 TO 1C  SQ_CIP     ( Part_ID );
CREATE ROP REF_ID R937 FROM MC     SQ_AV     ( Formal_Part_ID )
                 TO 1C  SQ_CIP     ( Part_ID );
CREATE ROP REF_ID R938 FROM MC     SQ_AV     ( Attr_ID , Obj_ID )
                 TO 1C  O_ATTR     ( Attr_ID , Obj_ID );
CREATE ROP REF_ID R939 FROM MC     SQ_CP     ( Obj_ID )
                 TO 1C  O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R947 FROM 1C     SQ_IA     ( Ia_ID )
             TO 1      SQ_CPA     ( Ia_ID );
CREATE ROP REF_ID R947 FROM 1C     SQ_FA     ( Ia_ID )
             TO 1      SQ_CPA     ( Ia_ID );
CREATE ROP REF_ID R948 FROM 1C     SQ_IAV     ( Av_ID )
             TO 1      SQ_AV     ( Av_ID );
CREATE ROP REF_ID R948 FROM 1C     SQ_FAV     ( Av_ID )
             TO 1      SQ_AV     ( Av_ID );
CREATE ROP REF_ID R940 FROM 1C     SQ_LS     ( Source_Part_ID )
                 TO 1      SQ_P     ( Part_ID );
CREATE ROP REF_ID R955 FROM MC     SQ_COP     ( Component_Id )
                 TO 1C  C_C     ( Id );
CREATE ROP REF_ID R949 FROM 1C     SQ_AP     ( LS_Part_ID )
                 TO 1C  SQ_LS     ( Part_ID );
CREATE ROP REF_ID R956 FROM MC     SQ_PP     ( Package_ID )
                 TO 1C  EP_PKG     ( Package_ID );
CREATE ROP REF_ID R609 FROM 1C     ACT_AI     ( r_Value_ID )
                 TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R633 FROM MC     ACT_CR     ( Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R634 FROM MC     ACT_DEL     ( Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R671 FROM MC     ACT_CR     ( Obj_ID )
                 TO 1      O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R672 FROM MC     ACT_CNV     ( Obj_ID )
                 TO 1      O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R689 FROM 1C     ACT_AI     ( l_Value_ID )
                 TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R2904 FROM MC     I_LNK     ( Rel_ID )
                 TO 1      R_REL     ( Rel_ID );
CREATE ROP REF_ID R2906 FROM MC     I_EVI     ( SMevt_ID )
                 TO 1      SM_EVT     ( SMevt_ID );
CREATE ROP REF_ID R2908 FROM 1C     I_EVI     ( nextEvent_ID )  PHRASE 'will_be_processed_after'
                 TO 1C  I_EVI     ( Event_ID )  PHRASE 'will_be_processed_before';
CREATE ROP REF_ID R2910 FROM MC     I_AVL     ( Attr_ID , Obj_ID )
                 TO 1      O_ATTR     ( Attr_ID , Obj_ID );
CREATE ROP REF_ID R2907 FROM MC     I_EVI     ( Target_Inst_ID )
                 TO 1C  I_INS     ( Inst_ID );
CREATE ROP REF_ID R2915 FROM MC     I_INS     ( SM_ID , SMstt_ID )
                 TO 1C  SM_STATE     ( SM_ID , SMstt_ID );
CREATE ROP REF_ID R2909 FROM MC     I_AVL     ( Inst_ID )
                 TO 1      I_INS     ( Inst_ID );
CREATE ROP REF_ID R2933 FROM MC     I_DIV     ( Event_ID )
                 TO 1      I_EVI     ( Event_ID );
CREATE ROP REF_ID R2934 FROM MC     I_DIV     ( SM_ID , SMedi_ID )
                 TO 1C  SM_EVTDI     ( SM_ID , SMedi_ID );
CREATE ROP REF_ID R2935 FROM MC     I_EVI     ( Target_Inst_ID )
                 TO 1C  I_INS     ( Inst_ID );
CREATE ROP REF_ID R2937 FROM MC     I_EVI     ( Sent_By_Inst_ID )
                 TO 1C  I_INS     ( Inst_ID );
CREATE ROP REF_ID R2939 FROM 1C     I_EVI     ( next_self_Event_ID )  PHRASE 'will_be_processed_before'
                 TO 1C  I_EVI     ( Event_ID )  PHRASE 'will_be_processed_after';
CREATE ROP REF_ID R2940 FROM 1C     I_TIM     ( Event_ID )
                 TO 1C  I_EVI     ( Event_ID );
CREATE ROP REF_ID R2948 FROM 1C     I_EXE     ( Dom_ID )
                 TO 1C  S_DOM     ( Dom_ID );
CREATE ROP REF_ID R2953 FROM MC     I_INS     ( Trans_ID , SM_ID )
                 TO 1      SM_TXN     ( Trans_ID , SM_ID );
CREATE ROP REF_ID R2955 FROM MC     I_EXE     ( Component_Id )
                 TO 1C  C_C     ( Id );
CREATE ROP REF_ID R2956 FROM MC     I_DIV     ( PP_Id )
                 TO 1C  C_PP     ( PP_Id );
CREATE ROP REF_ID R2957 FROM MC     I_INS     ( Execution_Engine_ID )
                 TO 1      I_EXE     ( Execution_Engine_ID );
CREATE ROP REF_ID R2958 FROM MC     I_LIP     ( Inst_ID )
                 TO 1      I_INS     ( Inst_ID );
CREATE ROP REF_ID R2959 FROM MC     I_LIP     ( Rel_ID )
                 TO 1      R_REL     ( Rel_ID );
CREATE ROP REF_ID R2901 FROM 1C     I_LNK     ( Rel_ID , Participation_ID )
                 TO 1      I_LIP     ( Rel_ID , Participation_ID );
CREATE ROP REF_ID R2902 FROM 1C     I_LNK     ( Rel_ID , Formalizing_Participation_ID )
                 TO 1      I_LIP     ( Rel_ID , Participation_ID );
CREATE ROP REF_ID R2903 FROM 1C     I_LNK     ( Rel_ID , Associator_Participation_ID )
                 TO 1C  I_LIP     ( Rel_ID , Participation_ID );
CREATE ROP REF_ID R2963 FROM MC     I_EXE     ( ImportedComponent_Id )
                 TO 1C  CL_IC     ( Id );
CREATE ROP REF_ID R2964 FROM MC     I_EVI     ( Execution_Engine_ID )
                 TO 1      I_EXE     ( Execution_Engine_ID );
CREATE ROP REF_ID R2970 FROM 1C     I_EXE     ( Package_ID )
                 TO 1C  EP_PKG     ( Package_ID );
CREATE ROP REF_ID R2974 FROM 1C     I_CIN     ( Container_ID )
                 TO 1      I_EXE     ( Execution_Engine_ID );
CREATE ROP REF_ID R2975 FROM MC     I_EXE     ( Container_ID )
                 TO 1C  I_CIN     ( Container_ID );
CREATE ROP REF_ID R2976 FROM MC     I_EVI     ( Originating_Execution_Engine_ID )
                 TO 1C  I_EXE     ( Execution_Engine_ID );
CREATE ROP REF_ID R9100 FROM MC     G_EIS     ( Element_ID )
                 TO 1      PE_PE     ( Element_ID );
CREATE ROP REF_ID R9100 FROM MC     G_EIS     ( Sys_ID )
                 TO 1      S_SYS     ( Sys_ID );
CREATE ROP REF_ID R712 FROM MC     E_GEN     ( Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R711 FROM MC     E_CEI     ( Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R708 FROM MC     E_CEE     ( EEevt_ID , EE_ID )
                 TO 1      S_EEEVT     ( EEevt_ID , EE_ID );
CREATE ROP REF_ID R709 FROM MC     E_GEE     ( EEevt_ID , EE_ID )
                 TO 1      S_EEEVT     ( EEevt_ID , EE_ID );
CREATE ROP REF_ID R701 FROM 1C     E_CES     ( Statement_ID )
             TO 1      E_ESS     ( Statement_ID );
CREATE ROP REF_ID R701 FROM 1C     E_GES     ( Statement_ID )
             TO 1      E_ESS     ( Statement_ID );
CREATE ROP REF_ID R710 FROM MC     E_CES     ( Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R702 FROM 1C     E_CEE     ( Statement_ID )
             TO 1      E_CES     ( Statement_ID );
CREATE ROP REF_ID R702 FROM 1C     E_CSME     ( Statement_ID )
             TO 1      E_CES     ( Statement_ID );
CREATE ROP REF_ID R703 FROM 1C     E_GEE     ( Statement_ID )
             TO 1      E_GES     ( Statement_ID );
CREATE ROP REF_ID R703 FROM 1C     E_GSME     ( Statement_ID )
             TO 1      E_GES     ( Statement_ID );
CREATE ROP REF_ID R706 FROM MC     E_CSME     ( SMevt_ID )
                 TO 1      SM_EVT     ( SMevt_ID );
CREATE ROP REF_ID R704 FROM 1C     E_CEI     ( Statement_ID )
             TO 1      E_CSME     ( Statement_ID );
CREATE ROP REF_ID R704 FROM 1C     E_CEA     ( Statement_ID )
             TO 1      E_CSME     ( Statement_ID );
CREATE ROP REF_ID R704 FROM 1C     E_CEC     ( Statement_ID )
             TO 1      E_CSME     ( Statement_ID );
CREATE ROP REF_ID R705 FROM 1C     E_GEN     ( Statement_ID )
             TO 1      E_GSME     ( Statement_ID );
CREATE ROP REF_ID R705 FROM 1C     E_GAR     ( Statement_ID )
             TO 1      E_GSME     ( Statement_ID );
CREATE ROP REF_ID R705 FROM 1C     E_GEC     ( Statement_ID )
             TO 1      E_GSME     ( Statement_ID );
CREATE ROP REF_ID R707 FROM MC     E_GSME     ( SMevt_ID )
                 TO 1      SM_EVT     ( SMevt_ID );
CREATE ROP REF_ID R700 FROM MC     V_PAR     ( Statement_ID )
                 TO 1C  E_ESS     ( Statement_ID );
CREATE ROP REF_ID R714 FROM 1C     E_GPR     ( Value_ID )
                 TO 1C  V_VAL     ( Value_ID );
CREATE ROP REF_ID R1402 FROM 1C     A_A     ( Package_ID )
             TO 1      EP_SPKG     ( Package_ID );
CREATE ROP REF_ID R1402 FROM 1C     COMM_COMM     ( Package_ID )
             TO 1      EP_SPKG     ( Package_ID );
CREATE ROP REF_ID R1402 FROM 1C     CP_CP     ( Package_ID )
             TO 1      EP_SPKG     ( Package_ID );
CREATE ROP REF_ID R1402 FROM 1C     S_DPK     ( Package_ID )
             TO 1      EP_SPKG     ( Package_ID );
CREATE ROP REF_ID R1402 FROM 1C     IP_IP     ( Package_ID )
             TO 1      EP_SPKG     ( Package_ID );
CREATE ROP REF_ID R1402 FROM 1C     UC_UCC     ( Package_ID )
             TO 1      EP_SPKG     ( Package_ID );
CREATE ROP REF_ID R1402 FROM 1C     SQ_S     ( Package_ID )
             TO 1      EP_SPKG     ( Package_ID );
CREATE ROP REF_ID R1401 FROM MC     EP_PKG     ( Sys_ID )
                 TO 1C  S_SYS     ( Sys_ID );
CREATE ROP REF_ID R1400 FROM MC     EP_SPKG     ( Container_Package_ID )
                 TO 1C  EP_PKG     ( Package_ID );
CREATE ROP REF_ID R1403 FROM MC     EP_PIP     ( Parent_Package_ID )
                 TO 1      EP_PKG     ( Package_ID );
CREATE ROP REF_ID R1404 FROM 1C     EP_PIP     ( Child_Package_ID )
                 TO 1      EP_PKG     ( Package_ID );
CREATE ROP REF_ID R1405 FROM MC     EP_PKG     ( Direct_Sys_ID )
                 TO 1      S_SYS     ( Sys_ID );
CREATE ROP REF_ID R1 FROM MC     S_SS     ( Dom_ID )
                 TO 1      S_DOM     ( Dom_ID );
CREATE ROP REF_ID R7 FROM MC     S_EEM     ( SS_ID )
                 TO 1      S_SS     ( SS_ID );
CREATE ROP REF_ID R9 FROM MC     S_EEM     ( EE_ID )
                 TO 1      S_EE     ( EE_ID );
CREATE ROP REF_ID R10 FROM MC     S_EEEVT     ( EE_ID )
                 TO 1      S_EE     ( EE_ID );
CREATE ROP REF_ID R12 FROM MC     S_EEEDI     ( EE_ID )
                 TO 1      S_EE     ( EE_ID );
CREATE ROP REF_ID R14 FROM MC     S_DT     ( Dom_ID )
                 TO 1C  S_DOM     ( Dom_ID );
CREATE ROP REF_ID R16 FROM MC     S_EEEDI     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R8 FROM MC     S_EE     ( Dom_ID )
                 TO 1C     S_DOM     ( Dom_ID );
CREATE ROP REF_ID R17 FROM 1C     S_CDT     ( DT_ID )
             TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R17 FROM 1C     S_UDT     ( DT_ID )
             TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R17 FROM 1C     S_EDT     ( DT_ID )
             TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R17 FROM 1C     S_SDT     ( DT_ID )
             TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R17 FROM 1C     S_IRDT     ( DT_ID )
             TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R20 FROM MC     S_BRG     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R21 FROM MC     S_BPARM     ( Brg_ID )
                 TO 1      S_BRG     ( Brg_ID );
CREATE ROP REF_ID R19 FROM MC     S_BRG     ( EE_ID )
                 TO 1      S_EE     ( EE_ID );
CREATE ROP REF_ID R15 FROM MC     S_EEDI     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R22 FROM MC     S_BPARM     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R11 FROM MC     S_EEDI     ( EE_ID )
                 TO 1      S_EE     ( EE_ID );
CREATE ROP REF_ID R13 FROM MC     S_EEEDT     ( EEedi_ID , EE_ID )
                 TO 1      S_EEEDI     ( EEedi_ID , EE_ID );
CREATE ROP REF_ID R13 FROM MC     S_EEEDT     ( EEevt_ID , EE_ID )
                 TO 1      S_EEEVT     ( EEevt_ID , EE_ID );
CREATE ROP REF_ID R2 FROM MC     O_OBJ     ( SS_ID )
                 TO 1C  S_SS     ( SS_ID );
CREATE ROP REF_ID R4 FROM MC     R_REL     ( SS_ID )
                 TO 1C  S_SS     ( SS_ID );
CREATE ROP REF_ID R5 FROM MC     CA_COMM     ( SS_ID )
                 TO 1      S_SS     ( SS_ID );
CREATE ROP REF_ID R6 FROM MC     CA_ACC     ( SS_ID )
                 TO 1      S_SS     ( SS_ID );
CREATE ROP REF_ID R3 FROM MC     O_IOBJ     ( SS_ID )
                 TO 1      S_SS     ( SS_ID );
CREATE ROP REF_ID R27 FROM MC     S_ENUM     ( EDT_DT_ID )
                 TO 1      S_EDT     ( DT_ID );
CREATE ROP REF_ID R23 FROM MC     S_SYNC     ( Dom_ID )
                 TO 1C      S_DOM     ( Dom_ID );
CREATE ROP REF_ID R25 FROM MC     S_SYNC     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R24 FROM MC     S_SPARM     ( Sync_ID )
                 TO 1      S_SYNC     ( Sync_ID );
CREATE ROP REF_ID R26 FROM MC     S_SPARM     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R28 FROM MC     S_DOM     ( Sys_ID )
                 TO 1C  S_SYS     ( Sys_ID );
CREATE ROP REF_ID R29 FROM MC     S_FPK     ( Dom_ID )
                 TO 1C  S_DOM     ( Dom_ID );
CREATE ROP REF_ID R31 FROM MC     S_FIP     ( FunPack_ID )
                 TO 1      S_FPK     ( FunPack_ID );
CREATE ROP REF_ID R31 FROM 1C      S_FIP     ( Sync_ID )
                 TO 1      S_SYNC     ( Sync_ID );
CREATE ROP REF_ID R30 FROM 1C     S_FPIP     ( FunPack_ID )
                 TO 1      S_FPK     ( FunPack_ID );
CREATE ROP REF_ID R32 FROM MC     S_FPK     ( Parent_FunPack_ID )
                 TO 1C  S_FPIP     ( FunPack_ID );
CREATE ROP REF_ID R33 FROM MC     S_EEIP     ( EEPack_ID )
                 TO 1      S_EEPK     ( EEPack_ID );
CREATE ROP REF_ID R33 FROM 1C      S_EEIP     ( EE_ID )
                 TO 1      S_EE     ( EE_ID );
CREATE ROP REF_ID R34 FROM 1C     S_EEPIP     ( EEPack_ID )
                 TO 1      S_EEPK     ( EEPack_ID );
CREATE ROP REF_ID R35 FROM MC     S_EEPK     ( Parent_EEPack_ID )
                 TO 1C  S_EEPIP     ( EEPack_ID );
CREATE ROP REF_ID R36 FROM MC     S_EEPK     ( Dom_ID )
                 TO 1C  S_DOM     ( Dom_ID );
CREATE ROP REF_ID R37 FROM 1C     S_DPIP     ( Package_ID )
                 TO 1      S_DPK     ( Package_ID );
CREATE ROP REF_ID R38 FROM MC     S_DPK     ( Parent_Package_ID )
                 TO 1C  S_DPIP     ( Package_ID );
CREATE ROP REF_ID R39 FROM 1C     S_DIP     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R39 FROM MC     S_DIP     ( Package_ID )
                 TO 1      S_DPK     ( Package_ID );
CREATE ROP REF_ID R40 FROM MC     S_DPK     ( Dom_ID )
                 TO 1C  S_DOM     ( Dom_ID );
CREATE ROP REF_ID R42 FROM 1C     S_SIS     ( Child_SS_ID )
                 TO 1      S_SS     ( SS_ID );
CREATE ROP REF_ID R41 FROM MC     S_SIS     ( Parent_SS_ID )
                 TO 1      S_SS     ( SS_ID );
CREATE ROP REF_ID R43 FROM 1C     S_SID     ( SS_ID )
                 TO 1      S_SS     ( SS_ID );
CREATE ROP REF_ID R43 FROM MC     S_SID     ( Dom_ID )
                 TO 1      S_DOM     ( Dom_ID );
CREATE ROP REF_ID R44 FROM MC     S_MBR     ( Parent_DT_DT_ID )
                 TO 1      S_SDT     ( DT_ID );
CREATE ROP REF_ID R45 FROM MC     S_MBR     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R46 FROM 1C     S_MBR     ( Previous_Member_ID , Parent_DT_DT_ID )  PHRASE 'succeeds'
                 TO 1C  S_MBR     ( Member_ID , Parent_DT_DT_ID )  PHRASE 'precedes';
CREATE ROP REF_ID R47 FROM MC     S_DIS     ( Dom_ID )
                 TO 1      S_DOM     ( Dom_ID );
CREATE ROP REF_ID R47 FROM MC     S_DIS     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R49 FROM MC     S_DIM     ( BParm_ID )
                 TO 1C  S_BPARM     ( BParm_ID );
CREATE ROP REF_ID R50 FROM MC     S_DIM     ( Brg_ID )
                 TO 1C  S_BRG     ( Brg_ID );
CREATE ROP REF_ID R51 FROM MC     S_DIM     ( Sync_ID )
                 TO 1C  S_SYNC     ( Sync_ID );
CREATE ROP REF_ID R52 FROM MC     S_DIM     ( SParm_ID )
                 TO 1C  S_SPARM     ( SParm_ID );
CREATE ROP REF_ID R53 FROM MC     S_DIM     ( Member_ID , DT_ID )
                 TO 1C  S_MBR     ( Member_ID , Parent_DT_DT_ID );
CREATE ROP REF_ID R54 FROM 1C     S_SPARM     ( Previous_SParm_ID )  PHRASE 'succeeds'
                 TO 1C  S_SPARM     ( SParm_ID )  PHRASE 'precedes';
CREATE ROP REF_ID R55 FROM 1C     S_BPARM     ( Previous_BParm_ID )  PHRASE 'succeeds'
                 TO 1C  S_BPARM     ( BParm_ID )  PHRASE 'precedes';
CREATE ROP REF_ID R56 FROM 1C     S_ENUM     ( Previous_Enum_ID )  PHRASE 'succeeds'
                 TO 1C  S_ENUM     ( Enum_ID )  PHRASE 'precedes';
CREATE ROP REF_ID R18 FROM MC     S_UDT     ( CDT_DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R300 FROM MC     PL_EEPID     ( Dom_ID )
                 TO 1      S_DOM     ( Dom_ID );
CREATE ROP REF_ID R300 FROM 1      PL_EEPID     ( EEPack_ID )
                 TO 1      S_EEPK     ( EEPack_ID );
CREATE ROP REF_ID R301 FROM 1      PL_FPID     ( FunPack_ID )
                 TO 1      S_FPK     ( FunPack_ID );
CREATE ROP REF_ID R301 FROM MC     PL_FPID     ( Dom_ID )
                 TO 1      S_DOM     ( Dom_ID );
CREATE ROP REF_ID R1500 FROM MC     CNST_SYC     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R1502 FROM 1C     CNST_LFSC     ( Const_ID , DT_ID )
             TO 1      CNST_SYC     ( Const_ID , DT_ID );
CREATE ROP REF_ID R1503 FROM 1C     CNST_LSC     ( Const_ID , DT_ID )
             TO 1      CNST_LFSC     ( Const_ID , DT_ID );
CREATE ROP REF_ID R1504 FROM MC     CNST_SYC     ( Constant_Spec_ID )
                 TO 1      CNST_CSP     ( Constant_Spec_ID );
CREATE ROP REF_ID R1505 FROM 1C     CNST_SYC     ( Previous_Const_ID , Previous_DT_DT_ID )  PHRASE 'succeeds'
                 TO 1C  CNST_SYC     ( Const_ID , DT_ID )  PHRASE 'precedes';
CREATE ROP REF_ID R1506 FROM 1C     CNST_CIP     ( Constant_Spec_ID )
                 TO 1      CNST_CSP     ( Constant_Spec_ID );
CREATE ROP REF_ID R1506 FROM MC     CNST_CIP     ( Package_ID )
                 TO 1      S_DPK     ( Package_ID );
CREATE ROP REF_ID R4002 FROM MC     C_SF     ( Requirement_Id )
                 TO 1      C_R     ( Requirement_Id );
CREATE ROP REF_ID R4002 FROM MC     C_SF     ( Provision_Id )
                 TO 1      C_P     ( Provision_Id );
CREATE ROP REF_ID R4003 FROM MC     C_EP     ( Interface_Id )
                 TO 1      C_I     ( Id );
CREATE ROP REF_ID R4004 FROM 1C     C_IO     ( Id )
             TO 1      C_EP     ( Id );
CREATE ROP REF_ID R4004 FROM 1C     C_AS     ( Id )
             TO 1      C_EP     ( Id );
CREATE ROP REF_ID R4006 FROM MC     C_PP     ( Signal_Id )
                 TO 1      C_EP     ( Id );
CREATE ROP REF_ID R4007 FROM MC     C_PP     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R4008 FROM MC     C_IO     ( DT_ID )
                 TO 1      S_DT     ( DT_ID );
CREATE ROP REF_ID R4009 FROM 1C     C_R     ( Requirement_Id )
             TO 1      C_IR     ( Id );
CREATE ROP REF_ID R4009 FROM 1C     C_P     ( Provision_Id )
             TO 1      C_IR     ( Id );
CREATE ROP REF_ID R4012 FROM MC     C_IR     ( Formal_Interface_Id )
                 TO 1C  C_I     ( Id );
CREATE ROP REF_ID R4013 FROM MC     C_RID     ( Reference_Id )
                 TO 1      C_IR     ( Id );
CREATE ROP REF_ID R4013 FROM MC     C_RID     ( Delegation_Id )
                 TO 1      C_DG     ( Id );
CREATE ROP REF_ID R4014 FROM MC     C_IR     ( Delegation_Id )
                 TO 1C  C_DG     ( Id );
CREATE ROP REF_ID R4010 FROM MC     C_PO     ( Component_Id )
                 TO 1      C_C     ( Id );
CREATE ROP REF_ID R4016 FROM MC     C_IR     ( Port_Id )
                 TO 1      C_PO     ( Id );
CREATE ROP REF_ID R4017 FROM MC     S_DIM     ( PP_Id )
                 TO 1C  C_PP     ( PP_Id );
CREATE ROP REF_ID R4018 FROM MC     S_DIM     ( Id )
                 TO 1C  C_IO     ( Id );
CREATE ROP REF_ID R4019 FROM 1C     C_IO     ( Previous_Id )  PHRASE 'succeeds'
                 TO 1C  C_IO     ( Id )  PHRASE 'precedes';
CREATE ROP REF_ID R4020 FROM 1C     C_AS     ( Previous_Id )  PHRASE 'succeeds'
                 TO 1C  C_AS     ( Id )  PHRASE 'precedes';
CREATE ROP REF_ID R4021 FROM 1C     C_PP     ( Previous_PP_Id )  PHRASE 'succeeds'
                 TO 1C  C_PP     ( PP_Id )  PHRASE 'precedes';
CREATE ROP REF_ID R4500 FROM MC     SPR_REP     ( ExecutableProperty_Id )
                 TO 1      C_EP     ( Id );
CREATE ROP REF_ID R4500 FROM MC     SPR_REP     ( Requirement_Id )
                 TO 1      C_R     ( Requirement_Id );
CREATE ROP REF_ID R4501 FROM MC     SPR_PEP     ( ExecutableProperty_Id )
                 TO 1      C_EP     ( Id );
CREATE ROP REF_ID R4501 FROM MC     SPR_PEP     ( Provision_Id )
                 TO 1      C_P     ( Provision_Id );
CREATE ROP REF_ID R4502 FROM 1C     SPR_RS     ( Id )
             TO 1      SPR_REP     ( Id );
CREATE ROP REF_ID R4502 FROM 1C     SPR_RO     ( Id )
             TO 1      SPR_REP     ( Id );
CREATE ROP REF_ID R4503 FROM 1C     SPR_PO     ( Id )
             TO 1      SPR_PEP     ( Id );
CREATE ROP REF_ID R4503 FROM 1C     SPR_PS     ( Id )
             TO 1      SPR_PEP     ( Id );
CREATE ROP REF_ID R4600 FROM MC     CP_CPINP     ( Parent_Package_ID )
                 TO 1      CP_CP     ( Package_ID );
CREATE ROP REF_ID R4601 FROM 1      CP_CP    ( ParentLink_Id )
                 TO 1C  CP_CPINP     ( Id );
CREATE ROP REF_ID R4602 FROM MC     CP_CP     ( Sys_ID )
                 TO 1C  S_SYS     ( Sys_ID );
CREATE ROP REF_ID R4604 FROM MC     C_C     ( Package_ID )
                 TO 1C  CP_CP     ( Package_ID );
CREATE ROP REF_ID R4606 FROM MC     CP_CP     ( Containing_Sys_ID )
                 TO 1      S_SYS     ( Sys_ID );
CREATE ROP REF_ID R4607 FROM MC     IP_IP     ( Component_Package_ID )
                 TO 1C  CP_CP     ( Package_ID );
CREATE ROP REF_ID R4605 FROM MC     CL_IC     ( Component_Package_ID )
                 TO 1C  CP_CP     ( Package_ID );
CREATE ROP REF_ID R4608 FROM MC     C_C     ( Root_Package_ID )
                 TO 1C  CP_CP     ( Package_ID );
CREATE ROP REF_ID R4202 FROM MC     CN_CIC     ( Parent_Id )
                 TO 1      C_C     ( Id );
CREATE ROP REF_ID R4203 FROM 1      C_C    ( NestedComponent_Id )
                 TO 1C  CN_CIC     ( Id );
CREATE ROP REF_ID R4204 FROM 1C     CN_DC     ( Id )
                 TO 1      C_C     ( Id );
CREATE ROP REF_ID R4204 FROM 1C     CN_DC     ( Dom_ID )
                 TO 1      S_DOM     ( Dom_ID );
CREATE ROP REF_ID R4206 FROM MC     IP_IP     ( Component_Id )
                 TO 1C  C_C     ( Id );
CREATE ROP REF_ID R4201 FROM MC     CL_IC     ( AssignedComp_Id )
                 TO 1C  C_C     ( Id );
CREATE ROP REF_ID R4205 FROM MC     CL_IC     ( ParentComp_Id )
                 TO 1C  C_C     ( Id );
CREATE ROP REF_ID R4700 FROM MC     CL_IIR     ( ImportedComp_Id )
                 TO 1      CL_IC     ( Id );
CREATE ROP REF_ID R4701 FROM MC     CL_IIR     ( Ref_Id )
                 TO 1C  C_IR     ( Id );
CREATE ROP REF_ID R4703 FROM 1C     CL_IP     ( Id )
             TO 1      CL_IIR     ( Id );
CREATE ROP REF_ID R4703 FROM 1C     CL_IR     ( Id )
             TO 1      CL_IIR     ( Id );
CREATE ROP REF_ID R4704 FROM 1C     CL_IIR     ( Delegation_Id )
                 TO 1C  C_DG     ( Id );
CREATE ROP REF_ID R4705 FROM 1C     CL_IPINS     ( Satisfaction_Id )
                 TO 1      C_SF     ( Id );
CREATE ROP REF_ID R4705 FROM MC     CL_IPINS     ( ImportedProvision_Id )
                 TO 1      CL_IP     ( Id );
CREATE ROP REF_ID R4706 FROM 1C     CL_IR     ( Satisfaction_Element_Id )
                 TO 1C  C_SF     ( Id );
CREATE ROP REF_ID R401 FROM 1C     CA_EESMC     ( CPath_ID )
             TO 1      CA_COMM     ( CPath_ID );
CREATE ROP REF_ID R401 FROM 1C     CA_SMEEC     ( CPath_ID )
             TO 1      CA_COMM     ( CPath_ID );
CREATE ROP REF_ID R401 FROM 1C     CA_SMSMC     ( CPath_ID )
             TO 1      CA_COMM     ( CPath_ID );
CREATE ROP REF_ID R404 FROM MC     CA_EESME     ( CPath_ID )
                 TO 1      CA_EESMC     ( CPath_ID );
CREATE ROP REF_ID R408 FROM MC     CA_SMSME     ( CPath_ID )
                 TO 1      CA_SMSMC     ( CPath_ID );
CREATE ROP REF_ID R412 FROM MC     CA_SMEEE     ( CPath_ID )
                 TO 1      CA_SMEEC     ( CPath_ID );
CREATE ROP REF_ID R413 FROM MC     CA_SMEEE     ( EEevt_ID , EE_ID )
                 TO 1      S_EEEVT     ( EEevt_ID , EE_ID );
CREATE ROP REF_ID R414 FROM MC     CA_SMSMC     ( DIObj_ID )
                 TO 1C  O_IOBJ     ( IObj_ID );
CREATE ROP REF_ID R415 FROM 1C     CA_SMOA     ( APath_ID )
             TO 1      CA_ACC     ( APath_ID );
CREATE ROP REF_ID R415 FROM 1C     CA_SMEEA     ( APath_ID )
             TO 1      CA_ACC     ( APath_ID );
CREATE ROP REF_ID R417 FROM MC     CA_SMOA     ( Obj_ID )
                 TO 1      O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R418 FROM MC     CA_SMOAA     ( APath_ID , Obj_ID )
                 TO 1      CA_SMOA     ( APath_ID , Obj_ID );
CREATE ROP REF_ID R419 FROM MC     CA_SMOAA     ( Attr_ID , Obj_ID )
                 TO 1      O_ATTR     ( Attr_ID , Obj_ID );
CREATE ROP REF_ID R420 FROM MC     CA_SMOA     ( IObj_ID )
                 TO 1C  O_IOBJ     ( IObj_ID );
CREATE ROP REF_ID R421 FROM MC     CA_SMEEA     ( EEmod_ID , EE_ID )
                 TO 1      S_EEM     ( EEmod_ID , EE_ID );
CREATE ROP REF_ID R422 FROM MC     CA_SMEED     ( APath_ID , EE_ID )
                 TO 1      CA_SMEEA     ( APath_ID , EE_ID );
CREATE ROP REF_ID R423 FROM MC     CA_SMEED     ( EEdi_ID , EE_ID )
                 TO 1      S_EEDI     ( EEdi_ID , EE_ID );
CREATE ROP REF_ID R424 FROM MC     CA_SMSMC     ( OIObj_ID )
                 TO 1C  O_IOBJ     ( IObj_ID );
CREATE ROP REF_ID R425 FROM MC     CA_ACC     ( IObj_ID )
                 TO 1C  O_IOBJ     ( IObj_ID );
CREATE ROP REF_ID R405 FROM MC     CA_EESME     ( SMevt_ID )
                 TO 1      SM_EVT     ( SMevt_ID );
CREATE ROP REF_ID R409 FROM MC     CA_SMSME     ( SMevt_ID )
                 TO 1      SM_EVT     ( SMevt_ID );
CREATE ROP REF_ID R403 FROM MC     CA_EESMC     ( SM_ID )
                 TO 1      SM_SM     ( SM_ID );
CREATE ROP REF_ID R402 FROM MC     CA_EESMC     ( EEmod_ID , EE_ID )
                 TO 1      S_EEM     ( EEmod_ID , EE_ID );
CREATE ROP REF_ID R410 FROM MC     CA_SMEEC     ( SM_ID )
                 TO 1      SM_SM     ( SM_ID );
CREATE ROP REF_ID R411 FROM MC     CA_SMEEC     ( EEmod_ID , EE_ID )
                 TO 1      S_EEM     ( EEmod_ID , EE_ID );
CREATE ROP REF_ID R406 FROM MC     CA_SMSMC     ( OSM_ID )
                 TO 1      SM_SM     ( SM_ID );
CREATE ROP REF_ID R407 FROM MC     CA_SMSMC     ( DSM_ID )
                 TO 1      SM_SM     ( SM_ID );
CREATE ROP REF_ID R416 FROM MC     CA_ACC     ( SM_ID )
                 TO 1      SM_SM     ( SM_ID );
CREATE ROP REF_ID R1129 FROM MC     COMM_COMM     ( CIC_Package_ID )
                 TO 1C  COMM_CIC     ( Package_ID );
CREATE ROP REF_ID R1130 FROM 1C     COMM_CIC     ( Package_ID )
                 TO 1      COMM_COMM     ( Package_ID );
CREATE ROP REF_ID R1132 FROM MC     COMM_COMM     ( Dom_ID )
                 TO 1C  S_DOM     ( Dom_ID );
CREATE ROP REF_ID R1126 FROM MC     COMM_PIC     ( Package_ID )
                 TO 1      COMM_COMM     ( Package_ID );
CREATE ROP REF_ID R1126 FROM 1C     COMM_PIC     ( Part_ID )
                 TO 1      SQ_P     ( Part_ID );
CREATE ROP REF_ID R1131 FROM MC     COMM_COMM     ( SS_ID )
                 TO 1C  S_SS     ( SS_ID );
CREATE ROP REF_ID R1128 FROM MC     COMM_LNK     ( Rel_ID )
                 TO 1C  R_REL     ( Rel_ID );
CREATE ROP REF_ID R1133 FROM MC     COMM_LNK     ( Start_Part_ID )
                 TO 1      SQ_P     ( Part_ID );
CREATE ROP REF_ID R1134 FROM MC     COMM_LNK     ( Destination_Part_ID )
                 TO 1      SQ_P     ( Part_ID );
CREATE ROP REF_ID R1135 FROM MC     COMM_MIC     ( Package_ID )
                 TO 1      COMM_COMM     ( Package_ID );
CREATE ROP REF_ID R1135 FROM 1C     COMM_MIC     ( Msg_ID )
                 TO 1      MSG_M     ( Msg_ID );
CREATE ROP REF_ID R1136 FROM MC     COMM_COMM     ( Sys_ID )
                 TO 1C  S_SYS     ( Sys_ID );
CREATE ROP REF_ID R1137 FROM MC     COMM_COMM     ( Component_Package_ID )
                 TO 1C  CP_CP     ( Package_ID );
CREATE ROP REF_ID R1138 FROM MC     COMM_COMM     ( Component_Id )
                 TO 1C  C_C     ( Id );
CREATE ROP REF_ID R666 FROM 1C     ACT_ACT     ( Block_ID )
                 TO 1C  ACT_BLK     ( Block_ID );
CREATE ROP REF_ID R661 FROM 1C     ACT_SMT     ( Previous_Statement_ID , Block_ID )  PHRASE 'succeeds'
                 TO 1C  ACT_SMT     ( Statement_ID , Block_ID )  PHRASE 'precedes';
CREATE ROP REF_ID R658 FROM 1C     ACT_EL     ( Block_ID )
                 TO 1      ACT_BLK     ( Block_ID );
CREATE ROP REF_ID R608 FROM 1C     ACT_WHL     ( Block_ID )
                 TO 1      ACT_BLK     ( Block_ID );
CREATE ROP REF_ID R606 FROM 1C     ACT_E     ( Block_ID )
                 TO 1      ACT_BLK     ( Block_ID );
CREATE ROP REF_ID R605 FROM 1C     ACT_FOR     ( Block_ID )
                 TO 1      ACT_BLK     ( Block_ID );
CREATE ROP REF_ID R607 FROM 1C     ACT_IF     ( Block_ID )
                 TO 1      ACT_BLK     ( Block_ID );
CREATE ROP REF_ID R602 FROM MC     ACT_SMT     ( Block_ID )
                 TO 1      ACT_BLK     ( Block_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_FOR     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_WHL     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_IF     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_EL     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_E     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_BRG     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_FNC     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_RET     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_TFM     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_AI     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_DEL     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_CNV     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_CR     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_SEL     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_FIO     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_FIW     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_URU     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_UNR     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_RU     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_REL     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_CTL     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_BRK     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_CON     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     E_ESS     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     E_GPR     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_IOP     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R603 FROM 1C     ACT_SGN     ( Statement_ID )
             TO 1      ACT_SMT     ( Statement_ID );
CREATE ROP REF_ID R614 FROM MC     ACT_FOR     ( Loop_Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R626 FROM 1C     ACT_WHL     ( Value_ID )
                 TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R625 FROM 1C     ACT_IF     ( Value_ID )
                 TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R659 FROM 1C     ACT_EL     ( Value_ID )
                 TO 1      V_VAL     ( Value_ID );
CREATE ROP REF_ID R670 FROM MC     ACT_FOR     ( Obj_ID )
                 TO 1      O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R601 FROM MC     ACT_BLK     ( Action_ID )
                 TO 1      ACT_ACT     ( Action_ID );
CREATE ROP REF_ID R652 FROM MC     ACT_FOR     ( Set_Var_ID )
                 TO 1      V_VAR     ( Var_ID );
CREATE ROP REF_ID R682 FROM MC     ACT_EL     ( If_Statement_ID )
                 TO 1      ACT_IF     ( Statement_ID );
CREATE ROP REF_ID R683 FROM 1C     ACT_E     ( If_Statement_ID )
                 TO 1      ACT_IF     ( Statement_ID );
CREATE ROP REF_ID R691 FROM 1C     ACT_SAB     ( SM_ID , Act_ID )
                 TO 1      SM_ACT     ( SM_ID , Act_ID );
CREATE ROP REF_ID R693 FROM 1C     ACT_DAB     ( Attr_ID , Obj_ID )
                 TO 1      O_DBATTR     ( Attr_ID , Obj_ID );
CREATE ROP REF_ID R695 FROM 1C     ACT_FNB     ( Sync_ID )
                 TO 1      S_SYNC     ( Sync_ID );
CREATE ROP REF_ID R696 FROM 1C     ACT_OPB     ( Tfr_ID )
                 TO 1      O_TFR     ( Tfr_ID );
CREATE ROP REF_ID R697 FROM 1C     ACT_BRB     ( Brg_ID )
                 TO 1      S_BRG     ( Brg_ID );
CREATE ROP REF_ID R698 FROM 1C     ACT_SAB     ( Action_ID )
             TO 1      ACT_ACT     ( Action_ID );
CREATE ROP REF_ID R698 FROM 1C     ACT_DAB     ( Action_ID )
             TO 1      ACT_ACT     ( Action_ID );
CREATE ROP REF_ID R698 FROM 1C     ACT_FNB     ( Action_ID )
             TO 1      ACT_ACT     ( Action_ID );
CREATE ROP REF_ID R698 FROM 1C     ACT_OPB     ( Action_ID )
             TO 1      ACT_ACT     ( Action_ID );
CREATE ROP REF_ID R698 FROM 1C     ACT_BRB     ( Action_ID )
             TO 1      ACT_ACT     ( Action_ID );
CREATE ROP REF_ID R698 FROM 1C     ACT_POB     ( Action_ID )
             TO 1      ACT_ACT     ( Action_ID );
CREATE ROP REF_ID R698 FROM 1C     ACT_PSB     ( Action_ID )
             TO 1      ACT_ACT     ( Action_ID );
CREATE ROP REF_ID R698 FROM 1C     ACT_ROB     ( Action_ID )
             TO 1      ACT_ACT     ( Action_ID );
CREATE ROP REF_ID R698 FROM 1C     ACT_RSB     ( Action_ID )
             TO 1      ACT_ACT     ( Action_ID );
CREATE ROP REF_ID R698 FROM 1C     ACT_TAB     ( Action_ID )
             TO 1      ACT_ACT     ( Action_ID );
CREATE ROP REF_ID R699 FROM 1C     ACT_ACT     ( CurrentScope_ID )
                 TO 1C  ACT_BLK     ( Block_ID );
CREATE ROP REF_ID R690 FROM 1C     ACT_IF     ( Elif_Statement_ID )
                 TO 1C  ACT_EL     ( Statement_ID );
CREATE ROP REF_ID R692 FROM 1C     ACT_IF     ( Else_Statement_ID )
                 TO 1C  ACT_E     ( Statement_ID );
CREATE ROP REF_ID R684 FROM 1C     ACT_RSB     ( Id )
                 TO 1      SPR_RS     ( Id );
CREATE ROP REF_ID R685 FROM 1C     ACT_ROB     ( Id )
                 TO 1      SPR_RO     ( Id );
CREATE ROP REF_ID R686 FROM 1C     ACT_PSB     ( Id )
                 TO 1      SPR_PS     ( Id );
CREATE ROP REF_ID R687 FROM 1C     ACT_POB     ( Id )
                 TO 1      SPR_PO     ( Id );
CREATE ROP REF_ID R688 FROM 1C     ACT_TAB     ( SM_ID , Act_ID )
                 TO 1      SM_ACT     ( SM_ID , Act_ID );
CREATE ROP REF_ID R201 FROM M     R_OIR     ( Rel_ID )
                 TO 1      R_REL     ( Rel_ID );
CREATE ROP REF_ID R201 FROM MC     R_OIR     ( Obj_ID )
                 TO 1      O_OBJ     ( Obj_ID );
CREATE ROP REF_ID R206 FROM 1C     R_SIMP     ( Rel_ID )
             TO 1      R_REL     ( Rel_ID );
CREATE ROP REF_ID R206 FROM 1C     R_COMP     ( Rel_ID )
             TO 1      R_REL     ( Rel_ID );
CREATE ROP REF_ID R206 FROM 1C     R_ASSOC     ( Rel_ID )
             TO 1      R_REL     ( Rel_ID );
CREATE ROP REF_ID R206 FROM 1C     R_SUBSUP     ( Rel_ID )
             TO 1      R_REL     ( Rel_ID );
CREATE ROP REF_ID R207 FROM M     R_PART     ( Rel_ID )
                 TO 1      R_SIMP     ( Rel_ID );
CREATE ROP REF_ID R208 FROM 1C     R_FORM     ( Rel_ID )
                 TO 1      R_SIMP     ( Rel_ID );
CREATE ROP REF_ID R209 FROM 1      R_AONE    ( Rel_ID )
                 TO 1      R_ASSOC     ( Rel_ID );
CREATE ROP REF_ID R210 FROM 1      R_AOTH    ( Rel_ID )
                 TO 1      R_ASSOC     ( Rel_ID );
CREATE ROP REF_ID R211 FROM 1      R_ASSR    ( Rel_ID )
                 TO 1      R_ASSOC     ( Rel_ID );
CREATE ROP REF_ID R212 FROM 1      R_SUPER    ( Rel_ID )
                 TO 1      R_SUBSUP     ( Rel_ID );
CREATE ROP REF_ID R213 FROM MC     R_SUB     ( Rel_ID )
                 TO 1      R_SUBSUP     ( Rel_ID );
CREATE ROP REF_ID R214 FROM 1      R_CONE    ( Rel_ID )
                 TO 1      R_COMP     ( Rel_ID );
CREATE ROP REF_ID R215 FROM 1      R_COTH    ( Rel_ID )
                 TO 1      R_COMP     ( Rel_ID );
CREATE ROP REF_ID R203 FROM 1C     R_RTO     ( OIR_ID , Obj_ID , Rel_ID )
             TO 1      R_OIR     ( OIR_ID , Obj_ID , Rel_ID );
CREATE ROP REF_ID R203 FROM 1C     R_RGO     ( OIR_ID , Obj_ID , Rel_ID )
             TO 1      R_OIR     ( OIR_ID , Obj_ID , Rel_ID );
CREATE ROP REF_ID R203 FROM 1C     R_CONE     ( OIR_ID , Obj_ID , Rel_ID )
             TO 1      R_OIR     ( OIR_ID , Obj_ID , Rel_ID );
CREATE ROP REF_ID R203 FROM 1C     R_COTH     ( OIR_ID , Obj_ID , Rel_ID )
             TO 1      R_OIR     ( OIR_ID , Obj_ID , Rel_ID );
CREATE ROP REF_ID R205 FROM 1C     R_SUB     ( OIR_ID , Obj_ID , Rel_ID )
             TO 1      R_RGO     ( OIR_ID , Obj_ID , Rel_ID );
CREATE ROP REF_ID R205 FROM 1C     R_FORM     ( OIR_ID , Obj_ID , Rel_ID )
             TO 1      R_RGO     ( OIR_ID , Obj_ID , Rel_ID );
CREATE ROP REF_ID R205 FROM 1C     R_ASSR     ( OIR_ID , Obj_ID , Rel_ID )
             TO 1      R_RGO     ( OIR_ID , Obj_ID , Rel_ID );
CREATE ROP REF_ID R204 FROM 1C     R_SUPER     ( OIR_ID , Obj_ID , Rel_ID )
             TO 1      R_RTO     ( OIR_ID , Obj_ID , Rel_ID );
CREATE ROP REF_ID R204 FROM 1C     R_PART     ( OIR_ID , Obj_ID , Rel_ID )
             TO 1      R_RTO     ( OIR_ID , Obj_ID , Rel_ID );
CREATE ROP REF_ID R204 FROM 1C     R_AONE     ( OIR_ID , Obj_ID , Rel_ID )
             TO 1      R_RTO     ( OIR_ID , Obj_ID , Rel_ID );
CREATE ROP REF_ID R204 FROM 1C     R_AOTH     ( OIR_ID , Obj_ID , Rel_ID )
             TO 1      R_RTO     ( OIR_ID , Obj_ID , Rel_ID );
CREATE ROP REF_ID R202 FROM MC     R_OIR     ( IObj_ID )
                 TO 1C  O_IOBJ     ( IObj_ID );
CREATE ROP REF_ID R1100 FROM MC     A_A     ( Dom_ID )
                 TO 1C  S_DOM     ( Dom_ID );
CREATE ROP REF_ID R1108 FROM MC     A_A     ( SS_ID )
                 TO 1C  S_SS     ( SS_ID );
CREATE ROP REF_ID R1109 FROM 1C     A_AIA     ( Package_ID )
                 TO 1      A_A     ( Package_ID );
CREATE ROP REF_ID R1110 FROM MC     A_A     ( Parent_Package_ID )
                 TO 1C  A_AIA     ( Package_ID );
CREATE ROP REF_ID R1111 FROM MC     A_AP     ( Package_ID )
                 TO 1      A_A     ( Package_ID );
CREATE ROP REF_ID R1102 FROM MC     A_E     ( Package_ID )
                 TO 1C     A_A     ( Package_ID );
CREATE ROP REF_ID R1101 FROM MC     A_N     ( Package_ID )
                 TO 1C  A_A     ( Package_ID );
CREATE ROP REF_ID R1103 FROM MC     A_E     ( TargetId )
                 TO 1      A_N     ( Id );
CREATE ROP REF_ID R1104 FROM MC     A_E     ( SourceId )
                 TO 1      A_N     ( Id );
CREATE ROP REF_ID R1105 FROM 1C     A_ACT     ( Id )
             TO 1      A_N     ( Id );
CREATE ROP REF_ID R1105 FROM 1C     A_OBJ     ( Id )
             TO 1      A_N     ( Id );
CREATE ROP REF_ID R1105 FROM 1C     A_CTL     ( Id )
             TO 1      A_N     ( Id );
CREATE ROP REF_ID R1107 FROM 1C     A_AE     ( Id )
             TO 1      A_ACT     ( Id );
CREATE ROP REF_ID R1107 FROM 1C     A_GA     ( Id )
             TO 1      A_ACT     ( Id );
CREATE ROP REF_ID R1107 FROM 1C     A_SS     ( Id )
             TO 1      A_ACT     ( Id );
CREATE ROP REF_ID R1106 FROM 1C     A_FF     ( Id )
             TO 1      A_CTL     ( Id );
CREATE ROP REF_ID R1106 FROM 1C     A_AF     ( Id )
             TO 1      A_CTL     ( Id );
CREATE ROP REF_ID R1106 FROM 1C     A_INI     ( Id )
             TO 1      A_CTL     ( Id );
CREATE ROP REF_ID R1106 FROM 1C     A_DM     ( Id )
             TO 1      A_CTL     ( Id );
CREATE ROP REF_ID R1106 FROM 1C     A_FJ     ( Id )
             TO 1      A_CTL     ( Id );
CREATE ROP REF_ID R1112 FROM 1C     A_ATE     ( Id )
             TO 1      A_AE     ( Id );
CREATE ROP REF_ID R1112 FROM 1C     A_AEA     ( Id )
             TO 1      A_AE     ( Id );
CREATE ROP REF_ID R1113 FROM MC     A_A     ( Sys_ID )
                 TO 1C  S_SYS     ( Sys_ID );
CREATE ROP REF_ID R1114 FROM MC     A_A     ( Component_Package_ID )
                 TO 1C  CP_CP     ( Package_ID );
CREATE ROP REF_ID R1115 FROM MC     A_A     ( Component_Id )
                 TO 1C  C_C     ( Id );
                 
CREATE UNIQUE INDEX I1 ON ACT_ACT (Action_ID);
CREATE UNIQUE INDEX I1 ON ACT_AI (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_BLK (Block_ID);
CREATE UNIQUE INDEX I1 ON ACT_BRB (Action_ID);
CREATE UNIQUE INDEX I1 ON ACT_BRG (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_BRK (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_CNV (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_CON (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_CR (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_CTL (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_DAB (Action_ID);
CREATE UNIQUE INDEX I1 ON ACT_DEL (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_E (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_EL (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_FIO (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_FIW (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_FNB (Action_ID);
CREATE UNIQUE INDEX I1 ON ACT_FNC (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_FOR (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_IF (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_IOP (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_LNK (Link_ID);
CREATE UNIQUE INDEX I1 ON ACT_OPB (Action_ID);
CREATE UNIQUE INDEX I1 ON ACT_POB (Action_ID);
CREATE UNIQUE INDEX I1 ON ACT_PSB (Action_ID);
CREATE UNIQUE INDEX I1 ON ACT_REL (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_RET (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_ROB (Action_ID);
CREATE UNIQUE INDEX I1 ON ACT_RSB (Action_ID);
CREATE UNIQUE INDEX I1 ON ACT_RU (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_SAB (Action_ID);
CREATE UNIQUE INDEX I1 ON ACT_SEL (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_SGN (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_SMT (Statement_ID);
CREATE UNIQUE INDEX I2 ON ACT_SMT (Statement_ID, Block_ID);
CREATE UNIQUE INDEX I1 ON ACT_SR (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_SRW (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_TAB (Action_ID);
CREATE UNIQUE INDEX I1 ON ACT_TFM (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_UNR (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_URU (Statement_ID);
CREATE UNIQUE INDEX I1 ON ACT_WHL (Statement_ID);
CREATE UNIQUE INDEX I1 ON A_A (Package_ID);
CREATE UNIQUE INDEX I1 ON A_ACT (Id);
CREATE UNIQUE INDEX I1 ON A_AE (Id);
CREATE UNIQUE INDEX I1 ON A_AEA (Id);
CREATE UNIQUE INDEX I1 ON A_AF (Id);
CREATE UNIQUE INDEX I1 ON A_AIA (Package_ID);
CREATE UNIQUE INDEX I1 ON A_AP (Id);
CREATE UNIQUE INDEX I1 ON A_ATE (Id);
CREATE UNIQUE INDEX I1 ON A_CTL (Id);
CREATE UNIQUE INDEX I1 ON A_DM (Id);
CREATE UNIQUE INDEX I1 ON A_E (Id);
CREATE UNIQUE INDEX I1 ON A_FF (Id);
CREATE UNIQUE INDEX I1 ON A_FJ (Id);
CREATE UNIQUE INDEX I1 ON A_GA (Id);
CREATE UNIQUE INDEX I1 ON A_INI (Id);
CREATE UNIQUE INDEX I1 ON A_N (Id);
CREATE UNIQUE INDEX I1 ON A_OBJ (Id);
CREATE UNIQUE INDEX I1 ON A_SS (Id);
CREATE UNIQUE INDEX I1 ON CA_ACC (APath_ID);
CREATE UNIQUE INDEX I1 ON CA_COMM (CPath_ID);
CREATE UNIQUE INDEX I1 ON CA_EESMC (CPath_ID);
CREATE UNIQUE INDEX I1 ON CA_EESME (SMevt_ID, CPath_ID);
CREATE UNIQUE INDEX I1 ON CA_SMEEA (APath_ID);
CREATE UNIQUE INDEX I2 ON CA_SMEEA (APath_ID, EE_ID);
CREATE UNIQUE INDEX I1 ON CA_SMEEC (CPath_ID);
CREATE UNIQUE INDEX I2 ON CA_SMEEC (SM_ID, EE_ID);
CREATE UNIQUE INDEX I1 ON CA_SMEED (APath_ID, EEdi_ID, EE_ID);
CREATE UNIQUE INDEX I1 ON CA_SMEEE (EEevt_ID, CPath_ID, EE_ID);
CREATE UNIQUE INDEX I1 ON CA_SMOA (APath_ID);
CREATE UNIQUE INDEX I2 ON CA_SMOA (APath_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON CA_SMOAA (APath_ID, Attr_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON CA_SMSMC (CPath_ID);
CREATE UNIQUE INDEX I2 ON CA_SMSMC (DSM_ID, OSM_ID);
CREATE UNIQUE INDEX I1 ON CA_SMSME (SMevt_ID, CPath_ID);
CREATE UNIQUE INDEX I1 ON CL_IC (Id);
CREATE UNIQUE INDEX I1 ON CL_IIR (Id);
CREATE UNIQUE INDEX I1 ON CL_IP (Id);
CREATE UNIQUE INDEX I1 ON CL_IPINS (Satisfaction_Id, ImportedProvision_Id);
CREATE UNIQUE INDEX I1 ON CL_IR (Id);
CREATE UNIQUE INDEX I1 ON CNST_CIP (Package_ID, Constant_Spec_ID);
CREATE UNIQUE INDEX I1 ON CNST_CSP (Constant_Spec_ID);
CREATE UNIQUE INDEX I1 ON CNST_LFSC (Const_ID, DT_ID);
CREATE UNIQUE INDEX I1 ON CNST_LSC (Const_ID, DT_ID);
CREATE UNIQUE INDEX I1 ON CNST_SYC (Const_ID, DT_ID);
CREATE UNIQUE INDEX I1 ON CN_CIC (Id);
CREATE UNIQUE INDEX I1 ON CN_DC (Dom_ID, Id);
CREATE UNIQUE INDEX I1 ON COMM_CIC (Package_ID);
CREATE UNIQUE INDEX I1 ON COMM_COMM (Package_ID);
CREATE UNIQUE INDEX I1 ON COMM_LNK (Link_ID);
CREATE UNIQUE INDEX I1 ON COMM_MIC (Package_ID, Msg_ID);
CREATE UNIQUE INDEX I1 ON COMM_PIC (Package_ID, Part_ID);
CREATE UNIQUE INDEX I1 ON CP_CP (Package_ID);
CREATE UNIQUE INDEX I1 ON CP_CPINP (Id);
CREATE UNIQUE INDEX I1 ON C_AS (Id);
CREATE UNIQUE INDEX I1 ON C_C (Id);
CREATE UNIQUE INDEX I1 ON C_DG (Id);
CREATE UNIQUE INDEX I1 ON C_EP (Id);
CREATE UNIQUE INDEX I1 ON C_I (Id);
CREATE UNIQUE INDEX I1 ON C_IO (Id);
CREATE UNIQUE INDEX I1 ON C_IR (Id);
CREATE UNIQUE INDEX I1 ON C_P (Provision_Id);
CREATE UNIQUE INDEX I1 ON C_PO (Id);
CREATE UNIQUE INDEX I1 ON C_PP (PP_Id);
CREATE UNIQUE INDEX I1 ON C_R (Requirement_Id);
CREATE UNIQUE INDEX I1 ON C_RID (Reference_Id, Delegation_Id);
CREATE UNIQUE INDEX I1 ON C_SF (Id);
CREATE UNIQUE INDEX I2 ON C_SF (Provision_Id, Requirement_Id);
CREATE UNIQUE INDEX I1 ON EP_PIP (Parent_Package_ID, Child_Package_ID);
CREATE UNIQUE INDEX I1 ON EP_PKG (Package_ID);
CREATE UNIQUE INDEX I1 ON EP_SPKG (Package_ID);
CREATE UNIQUE INDEX I1 ON E_CEA (Statement_ID);
CREATE UNIQUE INDEX I1 ON E_CEC (Statement_ID);
CREATE UNIQUE INDEX I1 ON E_CEE (Statement_ID);
CREATE UNIQUE INDEX I1 ON E_CEI (Statement_ID);
CREATE UNIQUE INDEX I1 ON E_CES (Statement_ID);
CREATE UNIQUE INDEX I1 ON E_CSME (Statement_ID);
CREATE UNIQUE INDEX I1 ON E_ESS (Statement_ID);
CREATE UNIQUE INDEX I1 ON E_GAR (Statement_ID);
CREATE UNIQUE INDEX I1 ON E_GEC (Statement_ID);
CREATE UNIQUE INDEX I1 ON E_GEE (Statement_ID);
CREATE UNIQUE INDEX I1 ON E_GEN (Statement_ID);
CREATE UNIQUE INDEX I1 ON E_GES (Statement_ID);
CREATE UNIQUE INDEX I1 ON E_GPR (Statement_ID);
CREATE UNIQUE INDEX I1 ON E_GSME (Statement_ID);
CREATE UNIQUE INDEX I1 ON G_EIS (Element_ID, Sys_ID);
CREATE UNIQUE INDEX I1 ON IA_UCP (Part_ID);
CREATE UNIQUE INDEX I1 ON IP_IP (Package_ID);
CREATE UNIQUE INDEX I1 ON IP_IPINIP (Package_ID);
CREATE UNIQUE INDEX I1 ON I_AVL (Attr_ID, Inst_ID);
CREATE UNIQUE INDEX I1 ON I_CIN (Container_ID);
CREATE UNIQUE INDEX I1 ON I_DIV (DIV_ID);
CREATE UNIQUE INDEX I1 ON I_EVI (Event_ID);
CREATE UNIQUE INDEX I1 ON I_EXE (Execution_Engine_ID);
CREATE UNIQUE INDEX I1 ON I_INS (Inst_ID);
CREATE UNIQUE INDEX I1 ON I_LIP (Rel_ID, Inst_ID);
CREATE UNIQUE INDEX I1 ON I_LNK (Link_ID);
CREATE UNIQUE INDEX I1 ON I_TIM (Timer_ID);
CREATE UNIQUE INDEX I1 ON MSG_A (Arg_ID);
CREATE UNIQUE INDEX I1 ON MSG_AM (Msg_ID);
CREATE UNIQUE INDEX I1 ON MSG_B (Msg_ID);
CREATE UNIQUE INDEX I1 ON MSG_BA (Arg_ID);
CREATE UNIQUE INDEX I1 ON MSG_E (Msg_ID);
CREATE UNIQUE INDEX I1 ON MSG_EA (Arg_ID);
CREATE UNIQUE INDEX I1 ON MSG_EPA (Arg_ID);
CREATE UNIQUE INDEX I1 ON MSG_F (Msg_ID);
CREATE UNIQUE INDEX I1 ON MSG_FA (Arg_ID);
CREATE UNIQUE INDEX I1 ON MSG_IA (Arg_ID);
CREATE UNIQUE INDEX I1 ON MSG_IAM (Msg_ID);
CREATE UNIQUE INDEX I1 ON MSG_IOP (Msg_ID);
CREATE UNIQUE INDEX I1 ON MSG_ISM (Msg_ID);
CREATE UNIQUE INDEX I1 ON MSG_M (Msg_ID);
CREATE UNIQUE INDEX I1 ON MSG_O (Msg_ID);
CREATE UNIQUE INDEX I1 ON MSG_OA (Arg_ID);
CREATE UNIQUE INDEX I1 ON MSG_R (Msg_ID);
CREATE UNIQUE INDEX I1 ON MSG_SIG (Msg_ID);
CREATE UNIQUE INDEX I1 ON MSG_SM (Msg_ID);
CREATE UNIQUE INDEX I1 ON O_ATTR (Attr_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON O_BATTR (Attr_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON O_DBATTR (Attr_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON O_ID (Oid_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON O_IOBJ (IObj_ID);
CREATE UNIQUE INDEX I1 ON O_NBATTR (Attr_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON O_OBJ (Obj_ID);
CREATE UNIQUE INDEX I1 ON O_OIDA (Attr_ID, Oid_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON O_RATTR (Attr_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON O_REF (ROIR_ID, RObj_ID, ROid_ID, Obj_ID, RAttr_ID, OIR_ID, Rel_ID);
CREATE UNIQUE INDEX I2 ON O_REF (ARef_ID);
CREATE UNIQUE INDEX I1 ON O_RTIDA (OIR_ID, Rel_ID, Attr_ID, Oid_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON O_TFR (Tfr_ID);
CREATE UNIQUE INDEX I1 ON O_TPARM (TParm_ID);
CREATE UNIQUE INDEX I1 ON PA_DIC (Component_Id, Delegation_Id);
CREATE UNIQUE INDEX I1 ON PA_SIC (Satisfaction_Id, Component_Id);
CREATE UNIQUE INDEX I1 ON PA_SICP (ComponentPackage_ID, Satisfaction_Id);
CREATE UNIQUE INDEX I1 ON PE_PE (Element_ID);
CREATE UNIQUE INDEX I1 ON PL_EEPID (Dom_ID, EEPack_ID);
CREATE UNIQUE INDEX I1 ON PL_FPID (Dom_ID, FunPack_ID);
CREATE UNIQUE INDEX I1 ON R_AONE (OIR_ID, Rel_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON R_AOTH (OIR_ID, Rel_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON R_ASSOC (Rel_ID);
CREATE UNIQUE INDEX I1 ON R_ASSR (OIR_ID, Rel_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON R_COMP (Rel_ID);
CREATE UNIQUE INDEX I1 ON R_CONE (OIR_ID, Rel_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON R_COTH (OIR_ID, Rel_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON R_FORM (OIR_ID, Rel_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON R_OIR (OIR_ID, Rel_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON R_PART (OIR_ID, Rel_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON R_REL (Rel_ID);
CREATE UNIQUE INDEX I1 ON R_RGO (OIR_ID, Rel_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON R_RTO (OIR_ID, Rel_ID, Obj_ID);
CREATE UNIQUE INDEX I2 ON R_RTO (OIR_ID, Rel_ID, Oid_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON R_SIMP (Rel_ID);
CREATE UNIQUE INDEX I1 ON R_SUB (OIR_ID, Rel_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON R_SUBSUP (Rel_ID);
CREATE UNIQUE INDEX I1 ON R_SUPER (OIR_ID, Rel_ID, Obj_ID);
CREATE UNIQUE INDEX I1 ON SLD_SCINP (Package_ID, Constant_Spec_ID);
CREATE UNIQUE INDEX I1 ON SLD_SDINP (Package_ID, DT_ID);
CREATE UNIQUE INDEX I1 ON SLD_SDP (Package_ID, Sys_ID);
CREATE UNIQUE INDEX I1 ON SM_ACT (SM_ID, Act_ID);
CREATE UNIQUE INDEX I1 ON SM_AH (SM_ID, Act_ID);
CREATE UNIQUE INDEX I1 ON SM_ASM (SM_ID);
CREATE UNIQUE INDEX I1 ON SM_CH (SM_ID, SMstt_ID, SMspd_ID, SMevt_ID);
CREATE UNIQUE INDEX I1 ON SM_CRTXN (SM_ID, Trans_ID);
CREATE UNIQUE INDEX I1 ON SM_EIGN (SM_ID, SMstt_ID, SMevt_ID, SMspd_ID);
CREATE UNIQUE INDEX I1 ON SM_EVT (SMevt_ID);
CREATE UNIQUE INDEX I2 ON SM_EVT (SM_ID, SMevt_ID, SMspd_ID);
CREATE UNIQUE INDEX I1 ON SM_EVTDI (SM_ID, SMedi_ID);
CREATE UNIQUE INDEX I1 ON SM_ISM (SM_ID);
CREATE UNIQUE INDEX I1 ON SM_LEVT (SM_ID, SMevt_ID);
CREATE UNIQUE INDEX I1 ON SM_MEAH (SM_ID, Trans_ID);
CREATE UNIQUE INDEX I2 ON SM_MEAH (SM_ID, Act_ID);
CREATE UNIQUE INDEX I1 ON SM_MEALY (SM_ID);
CREATE UNIQUE INDEX I1 ON SM_MOAH (SM_ID, SMstt_ID);
CREATE UNIQUE INDEX I2 ON SM_MOAH (SM_ID, Act_ID);
CREATE UNIQUE INDEX I1 ON SM_MOORE (SM_ID);
CREATE UNIQUE INDEX I1 ON SM_NETXN (SM_ID, Trans_ID);
CREATE UNIQUE INDEX I1 ON SM_NLEVT (SM_ID, SMspd_ID, SMevt_ID);
CREATE UNIQUE INDEX I1 ON SM_NSTXN (SMstt_ID, SM_ID, SMevt_ID, SMspd_ID);
CREATE UNIQUE INDEX I2 ON SM_NSTXN (SM_ID, Trans_ID);
CREATE UNIQUE INDEX I1 ON SM_PEVT (SM_ID, SMevt_ID);
CREATE UNIQUE INDEX I1 ON SM_SDI (SM_ID, SMedi_ID, SMspd_ID);
CREATE UNIQUE INDEX I1 ON SM_SEME (SM_ID, SMstt_ID, SMspd_ID, SMevt_ID);
CREATE UNIQUE INDEX I1 ON SM_SEVT (SM_ID, SMevt_ID, SMspd_ID);
CREATE UNIQUE INDEX I1 ON SM_SGEVT (SM_ID, SMevt_ID, SMspd_ID);
CREATE UNIQUE INDEX I1 ON SM_SM (SM_ID);
CREATE UNIQUE INDEX I1 ON SM_STATE (SM_ID, SMstt_ID);
CREATE UNIQUE INDEX I2 ON SM_STATE (SMstt_ID, SMspd_ID, SM_ID);
CREATE UNIQUE INDEX I1 ON SM_SUPDT (SM_ID, SMspd_ID);
CREATE UNIQUE INDEX I1 ON SM_TAH (SM_ID, Act_ID);
CREATE UNIQUE INDEX I1 ON SM_TXN (SM_ID, Trans_ID);
CREATE UNIQUE INDEX I1 ON SPR_PEP (Id);
CREATE UNIQUE INDEX I1 ON SPR_PO (Id);
CREATE UNIQUE INDEX I1 ON SPR_PS (Id);
CREATE UNIQUE INDEX I1 ON SPR_REP (Id);
CREATE UNIQUE INDEX I1 ON SPR_RO (Id);
CREATE UNIQUE INDEX I1 ON SPR_RS (Id);
CREATE UNIQUE INDEX I1 ON SQ_AP (Part_ID);
CREATE UNIQUE INDEX I1 ON SQ_AV (Av_ID);
CREATE UNIQUE INDEX I1 ON SQ_CIP (Part_ID);
CREATE UNIQUE INDEX I1 ON SQ_COP (Part_ID);
CREATE UNIQUE INDEX I1 ON SQ_CP (Part_ID);
CREATE UNIQUE INDEX I1 ON SQ_CPA (Ia_ID);
CREATE UNIQUE INDEX I1 ON SQ_EEP (Part_ID);
CREATE UNIQUE INDEX I1 ON SQ_FA (Ia_ID);
CREATE UNIQUE INDEX I1 ON SQ_FAV (Av_ID);
CREATE UNIQUE INDEX I1 ON SQ_FPP (Part_ID);
CREATE UNIQUE INDEX I1 ON SQ_IA (Ia_ID);
CREATE UNIQUE INDEX I1 ON SQ_IAV (Av_ID);
CREATE UNIQUE INDEX I1 ON SQ_LS (Part_ID);
CREATE UNIQUE INDEX I1 ON SQ_MIS (Package_ID, Msg_ID);
CREATE UNIQUE INDEX I1 ON SQ_P (Part_ID);
CREATE UNIQUE INDEX I1 ON SQ_PP (Part_ID);
CREATE UNIQUE INDEX I1 ON SQ_S (Package_ID);
CREATE UNIQUE INDEX I1 ON SQ_SIS (Package_ID);
CREATE UNIQUE INDEX I1 ON SQ_TM (Mark_ID);
CREATE UNIQUE INDEX I1 ON SQ_TS (Span_ID);
CREATE UNIQUE INDEX I1 ON S_BPARM (BParm_ID);
CREATE UNIQUE INDEX I1 ON S_BRG (Brg_ID);
CREATE UNIQUE INDEX I1 ON S_CDT (DT_ID);
CREATE UNIQUE INDEX I1 ON S_DIM (DIM_ID);
CREATE UNIQUE INDEX I1 ON S_DIP (Package_ID, DT_ID);
CREATE UNIQUE INDEX I1 ON S_DIS (Dom_ID, DT_ID);
CREATE UNIQUE INDEX I1 ON S_DOM (Dom_ID);
CREATE UNIQUE INDEX I1 ON S_DPIP (Package_ID);
CREATE UNIQUE INDEX I1 ON S_DPK (Package_ID);
CREATE UNIQUE INDEX I1 ON S_DT (DT_ID);
CREATE UNIQUE INDEX I2 ON S_DT (DT_ID);
CREATE UNIQUE INDEX I1 ON S_EDT (DT_ID);
CREATE UNIQUE INDEX I1 ON S_EE (EE_ID);
CREATE UNIQUE INDEX I1 ON S_EEDI (EEdi_ID, EE_ID);
CREATE UNIQUE INDEX I1 ON S_EEEDI (EEedi_ID, EE_ID);
CREATE UNIQUE INDEX I1 ON S_EEEDT (EEevt_ID, EEedi_ID, EE_ID);
CREATE UNIQUE INDEX I1 ON S_EEEVT (EEevt_ID, EE_ID);
CREATE UNIQUE INDEX I1 ON S_EEIP (EEPack_ID, EE_ID);
CREATE UNIQUE INDEX I1 ON S_EEM (EEmod_ID, EE_ID);
CREATE UNIQUE INDEX I1 ON S_EEPIP (EEPack_ID);
CREATE UNIQUE INDEX I1 ON S_EEPK (EEPack_ID);
CREATE UNIQUE INDEX I1 ON S_ENUM (Enum_ID);
CREATE UNIQUE INDEX I1 ON S_FIP (Sync_ID, FunPack_ID);
CREATE UNIQUE INDEX I1 ON S_FPIP (FunPack_ID);
CREATE UNIQUE INDEX I1 ON S_FPK (FunPack_ID);
CREATE UNIQUE INDEX I1 ON S_IRDT (DT_ID);
CREATE UNIQUE INDEX I1 ON S_MBR (Parent_DT_DT_ID, Member_ID);
CREATE UNIQUE INDEX I1 ON S_SDT (DT_ID);
CREATE UNIQUE INDEX I1 ON S_SID (Dom_ID, SS_ID);
CREATE UNIQUE INDEX I1 ON S_SIS (Child_SS_ID, Parent_SS_ID);
CREATE UNIQUE INDEX I1 ON S_SPARM (SParm_ID);
CREATE UNIQUE INDEX I1 ON S_SS (SS_ID);
CREATE UNIQUE INDEX I1 ON S_SYNC (Sync_ID);
CREATE UNIQUE INDEX I1 ON S_SYS (Sys_ID);
CREATE UNIQUE INDEX I1 ON S_UDT (DT_ID);
CREATE UNIQUE INDEX I1 ON UC_BA (Assoc_ID);
CREATE UNIQUE INDEX I1 ON UC_E (Assoc_ID);
CREATE UNIQUE INDEX I1 ON UC_G (Assoc_ID);
CREATE UNIQUE INDEX I1 ON UC_I (Assoc_ID);
CREATE UNIQUE INDEX I1 ON UC_PIUC (Package_ID, Part_ID);
CREATE UNIQUE INDEX I1 ON UC_UCA (Assoc_ID);
CREATE UNIQUE INDEX I1 ON UC_UCC (Package_ID);
CREATE UNIQUE INDEX I1 ON UC_UIU (Package_ID);
CREATE UNIQUE INDEX I1 ON V_AER (Value_ID);
CREATE UNIQUE INDEX I1 ON V_ALV (Value_ID);
CREATE UNIQUE INDEX I1 ON V_AVL (Value_ID);
CREATE UNIQUE INDEX I1 ON V_BIN (Value_ID);
CREATE UNIQUE INDEX I1 ON V_BRV (Value_ID);
CREATE UNIQUE INDEX I1 ON V_EDV (Value_ID);
CREATE UNIQUE INDEX I1 ON V_EPR (SM_ID, SMedi_ID, Value_ID, PP_Id);
CREATE UNIQUE INDEX I1 ON V_FNV (Value_ID);
CREATE UNIQUE INDEX I1 ON V_INS (Var_ID);
CREATE UNIQUE INDEX I1 ON V_INT (Var_ID);
CREATE UNIQUE INDEX I1 ON V_IRF (Value_ID);
CREATE UNIQUE INDEX I1 ON V_ISR (Value_ID);
CREATE UNIQUE INDEX I1 ON V_LBO (Value_ID);
CREATE UNIQUE INDEX I1 ON V_LEN (Value_ID);
CREATE UNIQUE INDEX I1 ON V_LIN (Value_ID);
CREATE UNIQUE INDEX I1 ON V_LOC (Id);
CREATE UNIQUE INDEX I1 ON V_LRL (Value_ID);
CREATE UNIQUE INDEX I1 ON V_LST (Value_ID);
CREATE UNIQUE INDEX I1 ON V_MSV (Value_ID);
CREATE UNIQUE INDEX I1 ON V_MVL (Value_ID);
CREATE UNIQUE INDEX I1 ON V_PAR (Value_ID);
CREATE UNIQUE INDEX I1 ON V_PVL (Value_ID);
CREATE UNIQUE INDEX I1 ON V_SCV (Value_ID);
CREATE UNIQUE INDEX I1 ON V_SLR (Value_ID);
CREATE UNIQUE INDEX I1 ON V_TRN (Var_ID);
CREATE UNIQUE INDEX I1 ON V_TRV (Value_ID);
CREATE UNIQUE INDEX I1 ON V_TVL (Value_ID);
CREATE UNIQUE INDEX I1 ON V_UNY (Value_ID);
CREATE UNIQUE INDEX I1 ON V_VAL (Value_ID);
CREATE UNIQUE INDEX I1 ON V_VAR (Var_ID);
'''


globals = '''
-- BP 7.1 content: Globals syschar: 3 persistence-version: 7.1.5

INSERT INTO PE_PE
    VALUES ("ba5eda7a-def5-0000-0000-000000000000",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("ba5eda7a-def5-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    'void',
    '',
    '');
INSERT INTO S_CDT
    VALUES ("ba5eda7a-def5-0000-0000-000000000000",
    0);
INSERT INTO PE_PE
    VALUES ("ba5eda7a-def5-0000-0000-000000000001",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("ba5eda7a-def5-0000-0000-000000000001",
    "00000000-0000-0000-0000-000000000000",
    'boolean',
    '',
    '');
INSERT INTO S_CDT
    VALUES ("ba5eda7a-def5-0000-0000-000000000001",
    1);
INSERT INTO PE_PE
    VALUES ("ba5eda7a-def5-0000-0000-000000000002",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("ba5eda7a-def5-0000-0000-000000000002",
    "00000000-0000-0000-0000-000000000000",
    'integer',
    '',
    '');
INSERT INTO S_CDT
    VALUES ("ba5eda7a-def5-0000-0000-000000000002",
    2);
INSERT INTO PE_PE
    VALUES ("ba5eda7a-def5-0000-0000-000000000003",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("ba5eda7a-def5-0000-0000-000000000003",
    "00000000-0000-0000-0000-000000000000",
    'real',
    '',
    '');
INSERT INTO S_CDT
    VALUES ("ba5eda7a-def5-0000-0000-000000000003",
    3);
INSERT INTO PE_PE
    VALUES ("ba5eda7a-def5-0000-0000-000000000004",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("ba5eda7a-def5-0000-0000-000000000004",
    "00000000-0000-0000-0000-000000000000",
    'string',
    '',
    '');
INSERT INTO S_CDT
    VALUES ("ba5eda7a-def5-0000-0000-000000000004",
    4);
INSERT INTO PE_PE
    VALUES ("ba5eda7a-def5-0000-0000-000000000005",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("ba5eda7a-def5-0000-0000-000000000005",
    "00000000-0000-0000-0000-000000000000",
    'unique_id',
    '',
    '');
INSERT INTO S_CDT
    VALUES ("ba5eda7a-def5-0000-0000-000000000005",
    5);
INSERT INTO PE_PE
    VALUES ("ba5eda7a-def5-0000-0000-000000000006",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("ba5eda7a-def5-0000-0000-000000000006",
    "00000000-0000-0000-0000-000000000000",
    'state<State_Model>',
    '',
    '');
INSERT INTO S_CDT
    VALUES ("ba5eda7a-def5-0000-0000-000000000006",
    6);
INSERT INTO PE_PE
    VALUES ("ba5eda7a-def5-0000-0000-000000000007",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("ba5eda7a-def5-0000-0000-000000000007",
    "00000000-0000-0000-0000-000000000000",
    'same_as<Base_Attribute>',
    '',
    '');
INSERT INTO S_CDT
    VALUES ("ba5eda7a-def5-0000-0000-000000000007",
    7);
INSERT INTO PE_PE
    VALUES ("ba5eda7a-def5-0000-0000-000000000008",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("ba5eda7a-def5-0000-0000-000000000008",
    "00000000-0000-0000-0000-000000000000",
    'inst_ref<Object>',
    '',
    '');
INSERT INTO S_CDT
    VALUES ("ba5eda7a-def5-0000-0000-000000000008",
    8);
INSERT INTO PE_PE
    VALUES ("ba5eda7a-def5-0000-0000-000000000009",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("ba5eda7a-def5-0000-0000-000000000009",
    "00000000-0000-0000-0000-000000000000",
    'inst_ref_set<Object>',
    '',
    '');
INSERT INTO S_CDT
    VALUES ("ba5eda7a-def5-0000-0000-000000000009",
    9);
INSERT INTO PE_PE
    VALUES ("ba5eda7a-def5-0000-0000-00000000000a",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("ba5eda7a-def5-0000-0000-00000000000a",
    "00000000-0000-0000-0000-000000000000",
    'inst<Event>',
    '',
    '');
INSERT INTO S_CDT
    VALUES ("ba5eda7a-def5-0000-0000-00000000000a",
    10);
INSERT INTO PE_PE
    VALUES ("ba5eda7a-def5-0000-0000-00000000000b",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("ba5eda7a-def5-0000-0000-00000000000b",
    "00000000-0000-0000-0000-000000000000",
    'inst<Mapping>',
    '',
    '');
INSERT INTO S_CDT
    VALUES ("ba5eda7a-def5-0000-0000-00000000000b",
    11);
INSERT INTO PE_PE
    VALUES ("ba5eda7a-def5-0000-0000-00000000000c",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("ba5eda7a-def5-0000-0000-00000000000c",
    "00000000-0000-0000-0000-000000000000",
    'inst_ref<Mapping>',
    '',
    '');
INSERT INTO S_CDT
    VALUES ("ba5eda7a-def5-0000-0000-00000000000c",
    12);
INSERT INTO PE_PE
    VALUES ("ba5eda7a-def5-0000-0000-00000000000d",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("ba5eda7a-def5-0000-0000-00000000000d",
    "00000000-0000-0000-0000-000000000000",
    'component_ref',
    '',
    '');
INSERT INTO S_CDT
    VALUES ("ba5eda7a-def5-0000-0000-00000000000d",
    13);
INSERT INTO PE_PE
    VALUES ("ba5eda7a-def5-0000-0000-00000000000e",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("ba5eda7a-def5-0000-0000-00000000000e",
    "00000000-0000-0000-0000-000000000000",
    'date',
    '',
    '');
INSERT INTO S_UDT
    VALUES ("ba5eda7a-def5-0000-0000-00000000000e",
    "ba5eda7a-def5-0000-0000-00000000000b",
    1);
INSERT INTO PE_PE
    VALUES ("ba5eda7a-def5-0000-0000-00000000000f",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("ba5eda7a-def5-0000-0000-00000000000f",
    "00000000-0000-0000-0000-000000000000",
    'inst_ref<Timer>',
    '',
    '');
INSERT INTO S_UDT
    VALUES ("ba5eda7a-def5-0000-0000-00000000000f",
    "ba5eda7a-def5-0000-0000-00000000000c",
    3);
INSERT INTO PE_PE
    VALUES ("ba5eda7a-def5-0000-0000-000000000010",
    1,
    "00000000-0000-0000-0000-000000000000",
    "00000000-0000-0000-0000-000000000000",
    3);
INSERT INTO S_DT
    VALUES ("ba5eda7a-def5-0000-0000-000000000010",
    "00000000-0000-0000-0000-000000000000",
    'timestamp',
    '',
    '');
INSERT INTO S_UDT
    VALUES ("ba5eda7a-def5-0000-0000-000000000010",
    "ba5eda7a-def5-0000-0000-00000000000b",
    2);
'''


def is_contained_in(pe_pe, root):
    '''
    Determine if a PE_PE is contained within a EP_PKG or a C_C.
    '''
    if not pe_pe:
        return False
    
    if pe_pe.__class__.__name__ != 'PE_PE':
        pe_pe = one(pe_pe).PE_PE[8001]()
    
    ep_pkg = one(pe_pe).EP_PKG[8000]()
    c_c = one(pe_pe).C_C[8003]()
    
    if root in [ep_pkg, c_c]:
        return True
    
    elif is_contained_in(ep_pkg, root):
        return True
    
    elif is_contained_in(c_c, root):
        return True
    
    else:
        return False
    

def is_global(pe_pe):
    '''
    Check if a PE_PE is globally defined, i.e. not inside a C_C
    '''
    if pe_pe.__class__.__name__ != 'PE_PE':
        pe_pe = one(pe_pe).PE_PE[8001]()
    
    if one(pe_pe).C_C[8003]():
        return False
    
    pe_pe = one(pe_pe).EP_PKG[8000].PE_PE[8001]()
    if not pe_pe:
        return True
    
    return is_global(pe_pe)


def get_data_type_name(s_dt):
    '''
    Convert a BridgePoint data type to a pyxtuml meta model type.
    '''
    s_cdt = one(s_dt).S_CDT[17]()
    if s_cdt and s_cdt.Core_Typ in range(1, 6):
        return s_dt.Name
    
    if one(s_dt).S_EDT[17]():
        return 'INTEGER'
    
    s_dt = one(s_dt).S_UDT[17].S_DT[18]()
    if s_dt:
        return get_data_type_name(s_dt)
    

def get_attribute_type(o_attr):
    '''
    Get the pyxtuml meta model type associated with a BridgePoint class
    attribute.
    '''
    ref_o_attr = one(o_attr).O_RATTR[106].O_BATTR[113].O_ATTR[106]()
    if ref_o_attr:
        return get_attribute_type(ref_o_attr)
    else:
        s_dt = one(o_attr).S_DT[114]()
        return get_data_type_name(s_dt)
 
    
def get_related_attributes(r_rgo, r_rto):
    '''
    The two lists of attributes which relates two classes in an association.
    '''
    l1 = list()
    l2 = list()
    
    ref_filter = lambda ref: ref.OIR_ID == r_rgo.OIR_ID
    for o_ref in many(r_rto).O_RTIDA[110].O_REF[111](ref_filter):
        o_attr = one(o_ref).O_RATTR[108].O_ATTR[106]()
        l1.append(o_attr.Name)
        
        o_attr = one(o_ref).O_RTIDA[111].O_OIDA[110].O_ATTR[105]()
        l2.append(o_attr.Name)
        
    return l1, l2

            
def mk_class(m, o_obj, derived_attributes=False):
    '''
    Create a pyxtuml class from a BridgePoint class.
    '''
    first_filter = lambda selected: not one(selected).O_ATTR[103, 'precedes']()
    o_attr = one(o_obj).O_ATTR[102](first_filter)
    attributes = list()
        
    while o_attr:
        ty = get_attribute_type(o_attr)
        if not derived_attributes and one(o_attr).O_BATTR[106].O_DBATTR[107]():
            logger.warning('Omitting derived attribute %s.%s ' %
                           (o_obj.Key_Lett, o_attr.Name))
        elif not ty:
            logger.warning('Omitting unsupported attribute %s.%s ' %
                           (o_obj.Key_Lett, o_attr.Name))
        else:
            attributes.append((o_attr.Name, ty))
        
        o_attr = one(o_attr).O_ATTR[103, 'succeeds']()
            
    Cls = m.define_class(o_obj.Key_Lett, list(attributes), o_obj.Descrip)

    for o_id in many(o_obj).O_ID[104]():
        o_oida = many(o_id).O_OIDA[105]()
        o_attrs = many(o_oida).O_ATTR[105]()
        if not derived_attributes and one(o_attrs).O_BATTR[106].O_DBATTR[107]():
            logger.warning('Omitting unique identifier %s.I%d' %
                           (o_obj.Key_Lett, o_id.Oid_ID + 1))
            continue
        
        names = [o_attr.Name for o_attr in o_attrs]
        m.define_unique_identifier(o_obj.Key_Lett, o_id.Oid_ID + 1, *names)
    
    return Cls


def mk_simple_association(m, inst):
    '''
    Create a pyxtuml association from a simple association in BridgePoint.
    '''
    r_rel = one(inst).R_REL[206]()

    r_form = one(inst).R_FORM[208]()
    r_part = one(inst).R_PART[207]()
    
    if None in [r_form, r_part]:
        logger.info('Omitting unformalized association R%s' % (r_rel.Numb))
        return
    
    r_rgo = one(r_form).R_RGO[205]()
    r_rto = one(r_part).R_RTO[204]()
    
    source_o_obj = one(r_rgo).R_OIR[203].O_OBJ[201]()
    target_o_obj = one(r_rto).R_OIR[203].O_OBJ[201]()
    source_ids, target_ids = get_related_attributes(r_rgo, r_rto)

    if source_o_obj.Obj_ID != target_o_obj.Obj_ID:
        source_phrase = target_phrase = ''
    else:
        source_phrase = r_part.Txt_Phrs
        target_phrase = r_form.Txt_Phrs
            
    m.define_association(rel_id=r_rel.Numb, 
                         source_kind=source_o_obj.Key_Lett,
                         target_kind=target_o_obj.Key_Lett,
                         source_keys=source_ids,
                         target_keys=target_ids,
                         source_conditional=r_form.Cond,
                         target_conditional=r_part.Cond,
                         source_phrase=source_phrase,
                         target_phrase=target_phrase,
                         source_many=r_form.Mult,
                         target_many=r_part.Mult,)


def mk_linked_association(m, inst):
    '''
    Create pyxtuml associations from a linked association in BridgePoint.
    '''
    r_rel = one(inst).R_REL[206]()
    r_rgo = one(inst).R_ASSR[211].R_RGO[205]()
    source_o_obj = one(r_rgo).R_OIR[203].O_OBJ[201]()
    
    def _mk_assoc(side1, side2):
        r_rto = one(side1).R_RTO[204]()

        target_o_obj = one(r_rto).R_OIR[203].O_OBJ[201]()
        source_ids, target_ids = get_related_attributes(r_rgo, r_rto)
        if side1.Obj_ID != side2.Obj_ID:
            source_phrase = target_phrase = ''
        else:
            source_phrase = side1.Txt_Phrs
            target_phrase = side2.Txt_Phrs
            
        m.define_association(rel_id=r_rel.Numb, 
                             source_kind=source_o_obj.Key_Lett,
                             target_kind=target_o_obj.Key_Lett,
                             source_keys=source_ids,
                             target_keys=target_ids,
                             source_conditional=side2.Cond,
                             target_conditional=False,
                             source_phrase=source_phrase,
                             target_phrase=target_phrase,
                             source_many=side2.Mult,
                             target_many=False)
        
    r_aone = one(inst).R_AONE[209]()
    r_aoth = one(inst).R_AOTH[210]()
    
    if None in [r_rgo, r_aone, r_aoth]:
        logger.info('Omitting unformalized association R%s' % (r_rel.Numb))
        return
    
    _mk_assoc(r_aone, r_aoth)
    _mk_assoc(r_aoth, r_aone)
  
    
def mk_subsuper_association(m, inst):
    '''
    Create pyxtuml associations from a sub/super association in BridgePoint.
    '''
    r_rel = one(inst).R_REL[206]()
    r_rto = one(inst).R_SUPER[212].R_RTO[204]()
    target_o_obj = one(r_rto).R_OIR[203].O_OBJ[201]()
    
    if not r_rto:
        logger.info('Omitting unformalized association R%s' % (r_rel.Numb))
        return
    
    for r_sub in many(inst).R_SUB[213]():
        r_rgo = one(r_sub).R_RGO[205]()

        source_o_obj = one(r_rgo).R_OIR[203].O_OBJ[201]()
        source_ids, target_ids = get_related_attributes(r_rgo, r_rto)
        m.define_association(rel_id=r_rel.Numb, 
                             source_kind=source_o_obj.Key_Lett,
                             target_kind=target_o_obj.Key_Lett,
                             source_keys=source_ids,
                             target_keys=target_ids,
                             source_conditional=True,
                             target_conditional=False,
                             source_phrase='',
                             target_phrase='',
                             source_many=False,
                             target_many=False)
                           

def mk_derived_association(m, inst):
    '''
    Create a pyxtuml association from a derived association in BridgePoint.
    '''
    pass


def mk_association(m, r_rel):
    '''
    Create a pyxtuml association from a R_REL in ooaofooa.
    '''
    handler = {
        'R_SIMP': mk_simple_association,
        'R_ASSOC': mk_linked_association,
        'R_SUBSUP': mk_subsuper_association,
        'R_COMP': mk_derived_association,
    }
    inst = subtype(r_rel, 206)
    fn = handler.get(inst.__class__.__name__)
    return fn(m, inst)


def mk_component(bp_model, c_c=None, derived_attributes=False):
    '''
    Create a pyxtuml meta model from a BridgePoint model. 
    Optionally, restrict to classes and associations contained in the
    component c_c.
    '''
    target = xtuml.MetaModel()

    c_c_filt = lambda sel: c_c is None or is_contained_in(sel, c_c)
    
    for o_obj in bp_model.select_many('O_OBJ', c_c_filt):
        mk_class(target, o_obj, derived_attributes)
        
    for r_rel in bp_model.select_many('R_REL', c_c_filt):
        mk_association(target, r_rel)
        
    return target


class ModelLoader(xtuml.ModelLoader):
    '''
    A *xtuml.MetaModel* loader with ooaofooa schema and globals pre-defined.
    '''
    
    def __init__(self, load_globals=True):
        xtuml.ModelLoader.__init__(self)
        self.input(schema, 'ooaofooa schema (v%02.1f)' % __version__)
        if load_globals:
            self.input(globals, 'predefined globals (v%02.1f)' % __version__)
        
    def filename_input(self, path_or_filename):
        '''
        Open and read input from a *path or filename*, and parse its content.
        
        If the filename is a directory, files that ends with .xtuml located
        somewhere in the directory or sub directories will be loaded as well.
        '''
        if os.path.isdir(path_or_filename):
            for path, _, files in os.walk(path_or_filename):
                for name in files:
                    if name.endswith('.xtuml'):
                        xtuml.ModelLoader.filename_input(self, os.path.join(path, name))
        else:
            xtuml.ModelLoader.filename_input(self, path_or_filename)

    def build_component(self, name=None, derived_attributes=False):
        '''
        Instantiate and build a component from ooaofooa named *name* as a
        pyxtuml model. Classes, associations, attributes and unique identifers,
        i.e. O_OBJ, R_REL, O_ATTR in ooaofooa, are defined in the resulting
        pyxtuml model.
        
        Optionally, control whether *derived attributes* shall be mapped into
        the resulting pyxtuml model as attributes or not.
        
        Futhermore, if no *name* is provided, the entire content of the ooaofooa
        model is instantiated into the pyxtuml model.
        '''
        mm = self.build_metamodel()
        c_c = mm.select_any('C_C', where(Name=name))
        if c_c:
            return mk_component(mm, c_c, derived_attributes)
        elif name:
            raise Exception('Unable to find the component %s' % name)
        else:
            return mk_component(mm, c_c, derived_attributes)


def load_metamodel(resource=None, load_globals=True):
    '''
    Load and return a metamodel expressed in ooaofooa from a *resource*.
    The resource may be either a filename, a path, or a list of filenames
    and/or paths.
    '''
    resource = resource or list()
        
    if isinstance(resource, str):
        resource = [resource]
        
    loader = Loader(load_globals)
    for filename in resource:
        loader.filename_input(filename)
    
    return loader.build_metamodel()


# Backwards compatabillity with older versions of pyxtuml
Loader = ModelLoader
empty_model = load_metamodel

