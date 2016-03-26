#!/usr/bin/env python3

from typing import Tuple

import equipment
import items


class Class:
    def __init__(self, name: str='', hd: int=0, md: int=0, sd: int=0, speed: int=0,
                 pdef: int=0, mdef: float=0.0, pred: float=0.0, mred: float=0.0,
                 reg: float=0.0, vis: int=0, pac: float=0.0, mac: float=0.0,
                 ath: int=0, ste: int=0, fort: int=0, apt: int=0, per: int=0, spe: int=0,
                 starting_abilities: int=0,
                 use_melee_light: bool=False, use_melee_medium: bool=False,
                 use_melee_heavy: bool=False, use_ranged_light: bool=False,
                 use_ranged_medium: bool=False, use_ranged_heavy: bool=False,
                 use_magic_light: bool=False, use_magic_medium: bool=False,
                 use_magic_heavy: bool=False, use_light_armor: bool=False,
                 use_medium_armor: bool=False, use_heavy_armor: bool=False):
        self.name = name
        self.hd = hd
        self.md = md
        self.sd = sd
        self.speed = speed
        self.pdef = pdef
        self.mdef = mdef
        self.pred = pred
        self.mred = mred
        self.reg = reg
        self.vis = vis
        self.pac = pac
        self.mac = mac
        self.ath = ath
        self.ste = ste
        self.fort = fort
        self.apt = apt
        self.per = per
        self.spe = spe
        self.starting_abilities = starting_abilities
        self.use_melee_light = use_melee_light
        self.use_melee_medium = use_melee_medium
        self.use_melee_heavy = use_melee_heavy
        self.use_ranged_light = use_ranged_light
        self.use_ranged_medium = use_ranged_medium
        self.use_ranged_heavy = use_ranged_heavy
        self.use_magic_light = use_magic_light
        self.use_magic_medium = use_magic_medium
        self.use_magic_heavy = use_magic_heavy
        self.use_light_armor = use_light_armor
        self.use_medium_armor = use_medium_armor
        self.use_heavy_armor = use_heavy_armor


class Character:
    atp_lvl_mod = 2
    ap_lvl_mod = 2
    hp_lvl_con_mod = 1.5
    mp_lvl_int_mod = 1
    sp_lvl_int_mod = 1
    pred_con_mod = 0.5
    mred_int_mod = 0.5
    starting_reg = 18
    speed_dex_mod = 0.5
    vis_con_mod = 0.5
    bpac_lvl_str_mod = 1
    bmac_lvl_cha_mod = 1

    def __init__(self, cls: Class=Class(), lvl: int=0,
                 stren: int=0, dex: int=0, con: int=0, intel: int=0, wis: int=0, cha: int=0,
                 starting_ap: int=0,
                 utilities: Tuple[equipment.Utility, equipment.Utility, equipment.Utility,
                                  equipment.Utility]=(
                                     items.empty_utility, items.empty_utility, items.empty_utility,
                                     items.empty_utility),
                 head: equipment.Head=items.empty_head,
                 neck: equipment.Neck=items.empty_neck, chest: equipment.Chest=items.empty_chest,
                 shield: equipment.Shield=items.empty_shield,
                 feet: equipment.Feet=items.empty_feet,
                 right_hand: equipment.Hand=items.empty_hand,
                 left_hand: equipment.Hand=items.empty_hand,
                 weapons: Tuple[equipment.Weapon, equipment.Weapon, equipment.Weapon]=(
                    items.empty_weapon, items.empty_weapon, items.empty_weapon)):
        self.cls = cls
        self.lvl = lvl
        self.str = stren
        self.dex = dex
        self.con = con
        self.int = intel
        self.wis = wis
        self.cha = cha
        self.starting_ap = starting_ap
        self.head = head
        self.neck = neck
        self.chest = chest
        self.shield = shield
        self.right_hand = right_hand
        self.left_hand = left_hand
        self.feet = feet
        self.utility1 = utilities[0]
        self.utility2 = utilities[1]
        self.utility3 = utilities[2]
        self.utility4 = utilities[3]
        self.weapon1 = weapons[0]
        self.weapon2 = weapons[1]
        self.weapon3 = weapons[2]

    @property
    def wearables(self) -> Tuple[equipment.Wearable, ...]:
        return (self.head, self.neck, self.chest, self.shield, self.right_hand, self.left_hand,
                self.feet, self.utility1, self.utility2, self.utility3, self.utility4,
                self.weapon1, self.weapon2, self.weapon3)

    @property
    def max_atp(self) -> int:
        return self.lvl * self.atp_lvl_mod

    @property
    def ap(self) -> int:
        return (self.starting_ap + (self.ap_lvl_mod * self.lvl) + self.wis + self.cha +
                sum([wearable.stats.ap for wearable in self.wearables]))

    @property
    def hp(self) -> int:
        return round(self.lvl * self.hp_lvl_con_mod * self.con +
                     sum([wearable.stats.hp for wearable in self.wearables]))

    @property
    def mp(self) -> int:
        return self.lvl * self.mp_lvl_int_mod * self.int

    @property
    def max_sp(self) -> int:
        return (self.lvl * self.sp_lvl_int_mod * self.int +
                sum([wearable.stats.sp for wearable in self.wearables]))

    @property
    def pdef(self) -> int:
        return self.cls.pdef + self.dex + sum([wearable.stats.pdef for wearable in self.wearables])

    @property
    def mdef(self) -> int:
        return round(self.cls.mdef * self.lvl +
                     sum([wearable.stats.mdef for wearable in self.wearables]))

    @property
    def pred(self) -> int:
        return round(self.cls.pred + (self.pred_con_mod * self.con) +
                     sum([wearable.stats.pred for wearable in self.wearables]))

    @property
    def mred(self) -> int:
        return round(self.cls.mred + (self.mred_int_mod * self.int) +
                     sum([wearable.stats.mred for wearable in self.wearables]))

    @property
    def reg(self) -> int:
        return round(self.starting_reg - (self.cls.reg * self.lvl) - self.cha -
                     sum([wearable.stats.reg for wearable in self.wearables]))

    @property
    def rd(self) -> str:
        # TODO: 0.25 * CHA + wearables
        if self.lvl <= 3:
            return 'd2'
        elif 4 <= self.lvl <= 6:
            return 'd4'
        elif 7 <= self.lvl <= 9:
            return 'd6'
        elif 10 <= self.lvl <= 12:
            return 'd8'
        elif 13 <= self.lvl <= 15:
            return 'd10'
        else:
            return 'd12'

    @property
    def speed(self) -> int:
        return round(self.cls.speed + (self.speed_dex_mod * self.dex) +
                     sum([wearable.stats.speed for wearable in self.wearables]))

    @property
    def vis(self) -> int:
        return round(self.cls.vis + (self.vis_con_mod * self.con) +
                     sum([wearable.stats.vis for wearable in self.wearables]))

    @property
    def bpac(self) -> int:
        return round(self.cls.pac + (self.bpac_lvl_str_mod * self.str) +
                     sum([wearable.stats.bpac for wearable in self.wearables]))

    @property
    def bmac(self) -> int:
        return round(self.cls.mac + (self.bmac_lvl_cha_mod * self.cha) +
                     sum([wearable.stats.bmac for wearable in self.wearables]))

    @property
    def ath(self) -> int:
        return (self.str * self.cls.ath) + sum([wearable.stats.ath for wearable in self.wearables])

    @property
    def ste(self) -> int:
        return (self.dex * self.cls.ste) + sum([wearable.stats.ste for wearable in self.wearables])

    @property
    def fort(self) -> int:
        return (self.con * self.cls.fort) + sum([wearable.stats.fort for wearable in
                                                 self.wearables])

    @property
    def apt(self) -> int:
        return (self.int * self.cls.apt) + sum([wearable.stats.apt for wearable in self.wearables])

    @property
    def per(self) -> int:
        return (self.wis * self.cls.per) + sum([wearable.stats.per for wearable in self.wearables])

    @property
    def spe(self) -> int:
        return self.cha * self.cls.spe + sum([wearable.stats.spe for wearable in self.wearables])
