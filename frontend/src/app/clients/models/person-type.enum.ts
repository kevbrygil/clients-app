export enum PersonType {
  Fisica = '1',
  Moral = '2',
}

export const PersonTypeLabel = new Map<string, string>([
  [PersonType.Fisica, 'Persona Física'],
  [PersonType.Moral, 'Persona Moral'],
]);