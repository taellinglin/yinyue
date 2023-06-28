
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'COLON IDENTIFIER LABEL OSCILLATOR VALUEinstrument : label COLON instrument_bodylabel : LABELinstrument_body : parameter_list oscillator_listparameter_list : parameter parameter_list\n                      | emptyparameter : label COLON valueoscillator_list : oscillator oscillator_list\n                       | emptyoscillator : OSCILLATOR oscillator_bodyoscillator_body : parameter_listvalue : VALUEempty :'
    
_lr_action_items = {'LABEL':([0,4,8,14,16,17,],[3,3,3,3,-6,-11,]),'$end':([1,4,6,7,8,9,11,12,13,14,15,16,17,18,19,20,],[0,-12,-1,-12,-12,-5,-3,-12,-8,-12,-4,-6,-11,-7,-9,-10,]),'COLON':([2,3,5,],[4,-2,10,]),'OSCILLATOR':([4,7,8,9,12,14,15,16,17,19,20,],[-12,14,-12,-5,14,-12,-4,-6,-11,-9,-10,]),'VALUE':([10,],[17,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'instrument':([0,],[1,]),'label':([0,4,8,14,],[2,5,5,5,]),'instrument_body':([4,],[6,]),'parameter_list':([4,8,14,],[7,15,20,]),'parameter':([4,8,14,],[8,8,8,]),'empty':([4,7,8,12,14,],[9,13,9,13,9,]),'oscillator_list':([7,12,],[11,18,]),'oscillator':([7,12,],[12,12,]),'value':([10,],[16,]),'oscillator_body':([14,],[19,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> instrument","S'",1,None,None,None),
  ('instrument -> label COLON instrument_body','instrument',3,'p_instrument','subsynth.py',50),
  ('label -> LABEL','label',1,'p_label','subsynth.py',54),
  ('instrument_body -> parameter_list oscillator_list','instrument_body',2,'p_instrument_body','subsynth.py',58),
  ('parameter_list -> parameter parameter_list','parameter_list',2,'p_parameter_list','subsynth.py',62),
  ('parameter_list -> empty','parameter_list',1,'p_parameter_list','subsynth.py',63),
  ('parameter -> label COLON value','parameter',3,'p_parameter','subsynth.py',70),
  ('oscillator_list -> oscillator oscillator_list','oscillator_list',2,'p_oscillator_list','subsynth.py',74),
  ('oscillator_list -> empty','oscillator_list',1,'p_oscillator_list','subsynth.py',75),
  ('oscillator -> OSCILLATOR oscillator_body','oscillator',2,'p_oscillator','subsynth.py',82),
  ('oscillator_body -> parameter_list','oscillator_body',1,'p_oscillator_body','subsynth.py',86),
  ('value -> VALUE','value',1,'p_value','subsynth.py',90),
  ('empty -> <empty>','empty',0,'p_empty','subsynth.py',94),
]
