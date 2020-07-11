export interface Demon {
  id: number;
  name: string;
  race: string;
  resistances: string;
  level: number;
  health: number;
  mana: number;
  strength: number;
  dexterity: number;
  magic: number;
  agility: number;
  luck: number;
}

export interface Skill {
  name: string;
  type: string;
  damage?: string;
  effect?: string;
  hits?: string;
  target?: string;
}
